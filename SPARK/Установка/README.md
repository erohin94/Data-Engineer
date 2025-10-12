## Локальная установка PySpark на Windows

**Скачивание**

Необходимо скачать непосредственно Spark: [ссылка](https://spark.apache.org/downloads.html)

Тут выбираем 3 пункт:

<img width="1151" height="295" alt="image" src="https://github.com/user-attachments/assets/243d5e22-51bd-429b-9b27-7979daaa30d1" />

И далее в новом окне:

<img width="1298" height="648" alt="image" src="https://github.com/user-attachments/assets/66091377-5c73-4400-9412-fc500594bb2c" />

Следущее - скачать JAVA JDK [ссылка](https://www.oracle.com/java/technologies/downloads/)

Выбираем Windows и скачиваем 21 версию:

<img width="1405" height="683" alt="image" src="https://github.com/user-attachments/assets/6e3243ca-786a-48b7-b9f2-0427cb2a78ee" />

Скачать утилиту Winutils.exe. Найти и скачать её нужно на GitHub:  [ссылка](https://github.com/steveloughran/winutils/tree/master/hadoop-3.0.0/bin)

<img width="1575" height="911" alt="image" src="https://github.com/user-attachments/assets/1e5e8818-7053-41c7-a967-38e85807d48a" />

Что получается в итоге:

1)Spark

2)JAVA JDK

3)Winutils.exe

<img width="403" height="180" alt="image" src="https://github.com/user-attachments/assets/214018e2-89f4-4125-8440-8a77effd24c4" />

**Установка**

1) Устанавливаем JAVA.

Двойной клик по значку с чашкой, затем Next, немного подождать и готово!

<img width="632" height="487" alt="image" src="https://github.com/user-attachments/assets/f4299821-d946-4dd4-bcde-bbc53e49344e" />

2)Следующим на очереди будет Spark. Создаем на диске С:/ папку Spark, копируем в нее скачанный ранее архив Spark и распаковываем его туда :

<img width="627" height="119" alt="image" src="https://github.com/user-attachments/assets/5e8ba2d8-2405-4f16-97ce-748e40057659" />

Также на диске C:/создаем папку Hadoop, а в ней папку bin, и копируем в нее утилиту Winutils.exe:

<img width="637" height="92" alt="image" src="https://github.com/user-attachments/assets/48ca774b-d78f-465d-827c-34a672b9023f" />

4) Теперь необходимо добавить в системные переменные наши 3 переменные.

Для этого пишем в поиске "Среды" и нажимаем на результаты поисковой выдачи:

<img width="386" height="270" alt="image" src="https://github.com/user-attachments/assets/1eea5cdf-bb2b-4918-9cba-d984d2732050" />

В появившемся окне выбираем "Переменные среды":

<img width="407" height="480" alt="image" src="https://github.com/user-attachments/assets/c7356f8e-b575-4dff-8092-06d7fd2d4d25" />

И уже через интерфейс добавляем системную переменную Имя: HADOOP_HOME Значение: C:\Hadoop:

<img width="622" height="626" alt="image" src="https://github.com/user-attachments/assets/977a93de-e382-4a50-a06a-d95bf7866278" />

Теперь добавляем еще одну системную переменную: Имя: SPARK_HOME Значение: C:\Spark\spark-X.X.X-bin-hadoopX (смотрите на имя папки распакованного архива со Spark!!!!!)

<img width="553" height="595" alt="image" src="https://github.com/user-attachments/assets/4354e5d8-526b-44a8-be08-21a5f79cb54f" />

Осталось добавить последнюю системную переменную: Имя: JAVA_HOME Значение: C:\Program Files\Java\jdk-21 (версия может быть другой!!! ) Чтобы найти СВОЮ версию JAVA, посмотрите в диске C:\Program Files\Java\ там будет находиться установленная недавно JAVA, путь к ней и нужно использовать в качестве значения. 

<img width="569" height="582" alt="image" src="https://github.com/user-attachments/assets/7c0e79f8-c56c-4397-94c3-6d16be11064a" />


Нажимаем OK и идем дальше

5)На данном шаге этого "квеста" нужно сконфигурировать переменные среды.

В этом же окне выбираем среду Path и нажимаем  Изменить.

<img width="570" height="605" alt="image" src="https://github.com/user-attachments/assets/3e33056e-657a-4e97-ac73-e3a6517fb93a" />

Далее нажимаем Создать и добавляем такие значения:

```
%SPARK_HOME%\bin 

%HADOOP_HOME%\bin  

%SPARK_HOME%\python 

%PYTHONPATH%
```

И еще одно, которое выглядит как путь к архиву, лежащему в распакованной папке Spark из скачанного архива. Внутри папки Spark есть папка python, а в ней lib Нам нужен полный путь к архиву, находящемуся в папке lib включая его расширение zip: `C:\Spark\spark-3.5.3-bin-hadoop3\python\lib\py4j-0.10.9.7-src.zip`  БУДЬТЕ ВНИМАТЕЛЬНЫ!!!

<img width="754" height="183" alt="image" src="https://github.com/user-attachments/assets/9d85225f-dc89-48f3-acc5-258ea7840144" />

В итоге должно получиться 5 добавленных значений:

<img width="548" height="595" alt="image" src="https://github.com/user-attachments/assets/eea090e9-fc10-4bb4-81cb-bebf103de059" />

Нажимаем ОК.

6) Далее нужно открыть командную строку и выполнить команду:

`spark-submit --version`
                 
В результате можно увидеть заветное окно: (если не появилось - проверяйте пути/переменные/буквы/расширения из материала выше - все работает: сам все несколько раз проверял для 100% результата)

<img width="595" height="280" alt="image" src="https://github.com/user-attachments/assets/49141305-d3be-48e7-8bbe-e663f9fc94bf" />

7) Открываем VsCode и создаем новую папку, например 123.

Создаем в этой папке файл `main.py`

Создаем вирт окружение.

Из папки `C:\Spark\spark-4.0.1-bin-hadoop3\python\lib` копируем два архиваи вставляем в папку с проектом `123` и распаковываем в этой папке

<img width="625" height="203" alt="image" src="https://github.com/user-attachments/assets/c10f0304-c982-4353-9898-3896af7785ff" />

Делаем `pip install pyspark` и пробуем запустить

```
from pyspark.sql import SparkSession
# creating spark session
spark = SparkSession.builder.master("local[1]") \
 .appName('SparkByExamples.com') \
 .getOrCreate()
```

Получим следующее

<img width="1245" height="388" alt="image" src="https://github.com/user-attachments/assets/f233eded-e74c-4a99-ac8a-085999b6bf26" />

Если будут ошиби, попробовать в начало добавить

```
import findspark
findspark.init()
```

Так же для теста можно запустить следующее

```
from pyspark.sql import SparkSession
import findspark

findspark.init()
# Создаём SparkSession
spark = SparkSession.builder \
    .appName("SparkTest") \
    .getOrCreate()

# Выводим версию Spark
print("✅ Spark версия:", spark.version)

# Создаём тестовый DataFrame
data = [("Анна", 31), ("Иван", 28), ("Мария", 35)]
columns = ["Имя", "Возраст"]

df = spark.createDataFrame(data, columns)

# Показываем данные
print("✅ Пример данных:")
df.show()

# Выполним простое преобразование — отбор людей старше 30
df_filtered = df.filter(df["Возраст"] > 30)

print("✅ Фильтрованные данные (Возраст > 30):")
df_filtered.show()

# Завершаем сессию
spark.stop()
print("✅ SparkSession успешно завершена.")
```

Увидим

<img width="1165" height="478" alt="image" src="https://github.com/user-attachments/assets/39c3fef4-8237-4f0e-96f5-0acaeac7f745" />

Так же могут быть ошибки из за версии JDK драйвера, и спарк прилоржение не будет запускаться, поробовать переустановить другую версию JDK.
