## Установка соединения c PostgreSQL

Рассмотрим работу PySpark с двумя базами данных, это PostgreSQL и Clickhouse. И, начнем с первого. Развернем образ PostgreSQL в докере, локально.

1. Зайдем в VsCode и создадим проект.

2. Далее создадим `Dockerfile` в структуре, настроим его и запустим.

```
# Используем официальный образ PostgreSQL
FROM postgres:latest

# Устанавливаем переменные среды для пользователя, базы данных и пароля
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword
ENV POSTGRES_DB=mydatabase

# Порт, который будет использоваться
EXPOSE 5432
```
                  
Откроем терминал и начнем сборку докер образа.

`docker build -t my_postgres_image .`

<img width="1020" height="849" alt="image" src="https://github.com/user-attachments/assets/c185d87f-7d3d-4efb-8f33-dfd809aaaaa7" />

Далее запустим контейнер.

`docker run --name my_postgres_container -p 5432:5432 -d my_postgres_image`
               
Введем команду docker ps и увидим, что контейнер запустился.

<img width="1292" height="108" alt="image" src="https://github.com/user-attachments/assets/966baadb-cd87-4567-9eea-390a3ee2f814" />

3. Зайдем в DBeaver. Сделаем новое соединение в PostgreSQL. Записываем все параметры, как в докер файле, а именно

User - myuser

Password -  mypassword

BD - mydatabase

Нажимаем тест соединения. Значит - теперь все ок. Нажмем ок и появится соединение.

<img width="694" height="624" alt="image" src="https://github.com/user-attachments/assets/9893afa8-41af-4ebc-9f70-03714cea0955" />

<img width="236" height="218" alt="image" src="https://github.com/user-attachments/assets/fc280d19-82b8-4c81-96d9-420dbab992a3" />

4. Следующим шагом будет создание таблицы, а также ее наполнение.

Введем в Dbeaver следующую команду.

Правой кнопкой по схеме public -> редактор SQL -> Новый редактор SQL.

```
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(100),
    salary DECIMAL(10, 2),
    hire_date DATE
);
```

В терминале Dbeaver будем видеть следующее.

<img width="257" height="229" alt="image" src="https://github.com/user-attachments/assets/54f617d6-8864-4af4-a7f4-9d79c52c954e" />

Далее наполним данными эту таблицу.

```
INSERT INTO employees (name, position, salary, hire_date) VALUES

('Alice', 'Engineer', 75000.00, '2021-06-15'),

('Bob', 'Manager', 90000.00, '2020-05-01'),

('Charlie', 'HR', 60000.00, '2019-04-12');
```

Далее проверим, все ли вставилось. Видим, что все ок.

<img width="492" height="91" alt="image" src="https://github.com/user-attachments/assets/8039d46f-3c5f-4a9f-8f0f-40d901ded1c0" />

5. Теперь все необходимо настроить в PySpark.

Добавим его внутрь нашего проекта. [postgresql-42.2.23.jar](https://github.com/erohin94/Data-Engineer/blob/main/SPARK/%D0%9A%D0%B0%D0%BA%20%D0%BF%D0%BE%D0%B4%D0%BA%D0%BB%D1%8E%D1%87%D0%B8%D1%82%D1%8C%D1%81%D1%8F%20%D0%B8%D0%B7%20PySpark%20%D0%BA%20%D0%B1%D0%B0%D0%B7%D0%B0%D0%BC%20%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85%3F/postgresql-42.2.23.jar) 

И так же добавить две папки `py4j` и `pyspark`, для работы spark. см.[Установка](https://github.com/erohin94/Data-Engineer/tree/main/SPARK/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0)

<img width="640" height="193" alt="image" src="https://github.com/user-attachments/assets/7a162bba-268a-4058-9389-c4a601c5b96f" />

Далее в `main.py` введем следующий скрипт. Должен быть уже установлен PySpark.

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PySpark PostgreSQL Connection").config("spark.jars", "postgresql-42.2.23.jar").getOrCreate()

url = "jdbc:postgresql://localhost:5432/mydatabase"
properties = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(url=url, table="employees", properties=properties)

df.show()

spark.stop()
```

На что здесь стоит обратить внимание? 

- На путь. Если Вы его положили ровно также, как и я - то заработает. Иначе - указывайте полный путь до файла.

- На порт, логин, пароль, базу данных и таблицу. Все как в примере.

Если запустить этот код, то увидим готовое соединение. 

<img width="1008" height="220" alt="image" src="https://github.com/user-attachments/assets/8f4515b1-97cd-474d-8e6d-79c86e3798d2" />

Может появлятся предупреждение `java.io.IOException: Failed to delete: C:\Users\erohi\AppData\Local\Temp\`

<img width="1397" height="239" alt="image" src="https://github.com/user-attachments/assets/d7b55369-9843-4c7c-97f8-4b4e44ec91a4" />

Это предупреждение появляется при очистке временных файлов Spark после завершения сессии. Можно не обращать внимание.

Spark создаёт временные каталоги (в C:\Users\<какой_то_пользователь>\AppData\Local\Temp\spark-*), куда кладёт: временные JAR-файлы (например, postgresql-42.2.23.jar драйвер), промежуточные данные выполнения.

Когда Spark останавливается, он пытается удалить эти временные файлы. Но Windows не позволяет — потому что: файл всё ещё используется JVM-процессом (Java), или антивирус/другой процесс заблокировал доступ к файлу,
или недостаточно прав для удаления этого пути.

Убедившись что все работает можно запустить код.Обработать таблицу средствами PySpark.

```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PySpark PostgreSQL Connection").config("spark.jars", "postgresql-42.2.23.jar").getOrCreate()

url = "jdbc:postgresql://localhost:5432/mydatabase"
properties = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}

df = spark.read.jdbc(url=url, table="employees", properties=properties)
df.show()

df.createOrReplaceTempView("my_table_view")
spark.sql("SELECT * FROM my_table_view WHERE salary >= 65000").show()

spark.stop()
```

Получим

<img width="1030" height="344" alt="image" src="https://github.com/user-attachments/assets/ba34bc01-7052-441b-8e3b-9cf10a8c9d5c" />

6. Операции с чтением были выше, теперь запись или создание таблиц из PySpark, но в PostgreSQL.

Представим, что у нет данных с PostgreSQL, а есть данные только в PySpark.

Добавить следующие строки в скрипт, без них у меня была ошибка 

```
import os

#Эта переменная PYSPARK_PYTHON говорит Spark, какой Python использовать для воркеров (то есть процессов, которые выполняют вычисления).
os.environ["PYSPARK_PYTHON"] = r'C:/Users/erohi/AppData/Local/Programs/Python/Python311/python.exe'

#Эта переменная задаёт Python для драйвера Spark, то есть для основного скрипта.
#Драйвер — это процесс, который управляет воркерами и распределяет задачи.
#Обычно в Windows нужно, чтобы драйвер и воркеры использовали один и тот же Python.
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:/Users/erohi/AppData/Local/Programs/Python/Python311/python.exe"# Без этого Ошибка
```

Запускаю код
```
from pyspark.sql import SparkSession
import os 
os.environ["PYSPARK_PYTHON"] = r'C:/Users/erohi/AppData/Local/Programs/Python/Python311/python.exe'
os.environ["PYSPARK_DRIVER_PYTHON"] = r'C:/Users/erohi/AppData/Local/Programs/Python/Python311/python.exe'


spark = SparkSession.builder.appName("PySpark PostgreSQL Connection").config("spark.jars", "postgresql-42.2.23.jar").getOrCreate()

url = "jdbc:postgresql://localhost:5432/mydatabase"
properties = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}

data = [
    ("Alice", "Engineer", 75000, "2021-06-15"),
    ("Bob", "Manager", 90000, "2020-05-01"),
    ("Charlie", "HR", 60000, "2019-04-12"),
    ("Diana", "Sales", 50000, "2018-01-25")
]
columns = ["name", "position", "salary", "hire_date"]

df = spark.createDataFrame(data, columns)

df.show()

spark.stop()
```

Увижу

<img width="1010" height="238" alt="image" src="https://github.com/user-attachments/assets/cad59ccc-64a4-45eb-b748-38f56bdef366" />

Теперь надо залить эти данные в любую postgresql. Но, предварительно, сделаем фильтр данных. Пропадет одна строчка.

```
filtered_df = df.filter(df.salary >= 60000)

filtered_df.show()
```

Как залить данные? Для начала создадим коннект и вынесем его в словарь.

```
url = "jdbc:postgresql://localhost:5432/mydatabase"
properties = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}
```

После этого делаем запись.

```
filtered_df.write.jdbc(
    url=url,
    table="high_salary_employees",
    mode="overwrite",  # "overwrite" - если таблица уже существует, она будет перезаписана
    properties=properties
)
```

Весь код целиком

```
from pyspark.sql import SparkSession
import os 
os.environ["PYSPARK_PYTHON"] = r'C:/Users/erohi/AppData/Local/Programs/Python/Python311/python.exe'
os.environ["PYSPARK_DRIVER_PYTHON"] = r'C:/Users/erohi/AppData/Local/Programs/Python/Python311/python.exe'


spark = SparkSession.builder.appName("PySpark PostgreSQL Connection").config("spark.jars", "postgresql-42.2.23.jar").getOrCreate()

url = "jdbc:postgresql://localhost:5432/mydatabase"
properties = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}

data = [
    ("Alice", "Engineer", 75000, "2021-06-15"),
    ("Bob", "Manager", 90000, "2020-05-01"),
    ("Charlie", "HR", 60000, "2019-04-12"),
    ("Diana", "Sales", 50000, "2018-01-25")
]
columns = ["name", "position", "salary", "hire_date"]

df = spark.createDataFrame(data, columns)
df.show()

filtered_df = df.filter(df.salary >= 60000)
filtered_df.show()

url = "jdbc:postgresql://localhost:5432/mydatabase"
properties = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}

filtered_df.write.jdbc(
    url=url,
    table="high_salary_employees",
    mode="overwrite",  # "overwrite" - если таблица уже существует, она будет перезаписана
    properties=properties
)
print("Данные успешно записаны в таблицу high_salary_employees")

spark.stop()
```

Запускаем и увидим

<img width="1017" height="358" alt="image" src="https://github.com/user-attachments/assets/a9aade77-3565-432c-a2a4-75a238b18310" />

Ну и в Dbeaver будет видно таблицу которую создали в спарк

<img width="484" height="141" alt="image" src="https://github.com/user-attachments/assets/6f52e5bb-2080-4ecf-b4a1-b1cf1d6d33db" />

<img width="470" height="213" alt="image" src="https://github.com/user-attachments/assets/a8251426-d0c7-4c29-9eb8-a44acb3a7aad" />

Запустив код вставки еще раз и повторив запрос SELECT, то увидим все те же самые данные. Потому что таблица будет перезаписана. Но, если такое не устраивает, то можно менять формат вставки.


**`overwrite`:**

- Если таблица уже существует, все данные будут перезаписаны.

- Это означает, что старая таблица будет удалена, и вместо нее будет создана новая с данными, которые записываем.

**`append`:**

- Если таблица уже существует, новые данные будут добавлены к существующим данным.

- Используется, когда хотим добавить новые записи в существующую таблицу.
  
**`error (или errorifexists) (по умолчанию)`:**

- Если таблица уже существует, будет выброшена ошибка.

- Этот режим используется для защиты данных от случайного перезаписывания.

```
# Запись данных с перезаписью таблицы (overwrite)
df.write.mode("overwrite").jdbc(url=url, table="my_table", properties=properties)

# Запись данных с добавлением новых записей (append)
df.write.mode("append").jdbc(url=url, table="my_table", properties=properties)

# Запись данных с ошибкой при существующей таблице (error)
df.write.mode("error").jdbc(url=url, table="my_table", properties=properties)
```

Пример с error `df.write.mode("error").jdbc(url=url, table="my_table", properties=properties)`

<img width="1054" height="566" alt="image" src="https://github.com/user-attachments/assets/38902a0b-5e02-4170-ae47-41ff6817728d" />


Если что, то данные через psycopg2 также можно считать, но питоном, а далее перекинуть на PySpark, что не очень удобно и оставляет желать лучшего при оптимизации кода. При остановке и запуске Docker контейнера - данные остаются!
