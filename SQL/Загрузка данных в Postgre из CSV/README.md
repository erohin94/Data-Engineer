# Пример: создание таблицы и загрузка данных из CSV в PostgreSQL (Docker)

   Например, у нас есть CSV файл с таблицей и мы хотим на основе него создать таблицу в БД Postgre.
   
   ⚠ Важно понимать:
   COPY ... FROM 'path' выполняется **на стороне PostgreSQL-сервера**,
   а сервер находится **внутри Docker-контейнера**, а НЕ на Windows.

   Поэтому путь к файлу должен существовать внутри контейнера PostgreSQL.

   ---------------------------------------------------------------------
   ШАГ 1. Подготовка локальной папки с файлом
   ---------------------------------------------------------------------
   На Windows создайте папку:

       C:\Users\erohi\Desktop\spark_data_mart\notebooks\data

   Поместите туда CSV-файл:

       costs_postgres.csv

   Итоговый путь на хосте:
       C:\Users\erohi\Desktop\spark_data_mart\notebooks\data\costs_postgres.csv

<img width="625" height="181" alt="image" src="https://github.com/user-attachments/assets/caf0cdc9-7241-469a-81ec-344542fbaefd" />

   ---------------------------------------------------------------------
   ШАГ 2. Прописать volume в docker-compose.yml
   ---------------------------------------------------------------------
   В сервис postgres добавьте:

       volumes:
         - ./notebooks/data:/data

   Теперь папка notebooks/data → смонтирована как /data в контейнере.

<img width="730" height="695" alt="image" src="https://github.com/user-attachments/assets/0c8ee46b-9901-407c-9b69-932f77f1565e" />


   ---------------------------------------------------------------------
   ШАГ 3. Пересоздать контейнер PostgreSQL
   ---------------------------------------------------------------------
   После изменения volume обязательно пересоздайте контейнер:

       docker compose down
       docker compose up -d


   ---------------------------------------------------------------------
   ШАГ 4. Проверить наличие файла внутри контейнера
   ---------------------------------------------------------------------

       docker exec -it postgres bash
       ls /data

   Ожидаемый вывод:
       costs_postgres.csv

<img width="776" height="329" alt="image" src="https://github.com/user-attachments/assets/4d6df412-ea35-4d22-910d-fbf8faf4e44b" />

```
/* Создание таблицы (если отсутствует) */
CREATE TABLE IF NOT EXISTS costs_test (
    date        date,
    campaign_id int,
    costs       float,
    clicks      int,
    views       int
);


/* Загрузка данных из CSV, который доступен внутри контейнера по пути /data */
COPY costs_test
FROM '/data/costs_postgres.csv'
DELIMITER ','
CSV HEADER;


/* Проверка результата */
SELECT * FROM costs_test;
```
