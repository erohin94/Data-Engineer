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
