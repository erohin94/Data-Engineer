# **В postgresql**

Предположим есть датафрейм

```
import pandas as pd

resumes_id_list_all = [['aaa111', 111111, 'test1', 'test_11', 10011, 'active', 'data'],  
                       ['aaa222', 22222, 'test2', 'test_22', 10012, 'active', 'data2']]

df_resumes_list = pd.DataFrame(resumes_id_list_all, columns=['resume_id', 'owner_id', 'url', 'url_w_contacts', 'vacancy_code', 'search_status', 't_changed_dttm']).drop_duplicates()
```

![image](https://github.com/user-attachments/assets/6d9a74e0-9b2a-4427-b8a5-975ca8e1ff52)

```
#Получаем список кортежей
#Кортеж (tuple) — неизменяемый тип данных. my_tuple = (1, 2, 3)
#Множество (set) — изменяемый тип данных. my_set = {1, 2, 3}

df = df_resumes_list
tuples = list(set([tuple(x) for x in df.to_numpy()]))
tuples

-----------------------------------------------
[('aaa222', 22222, 'test2', 'test_22', 10012, 'active', 'data2'),
 ('aaa111', 111111, 'test1', 'test_11', 10011, 'active', 'data')]
```

```
columns = ', '.join(list(df.columns))
---------------
resume_id, owner_id, url, url_w_contacts, vacancy_code, search_status, t_changed_dttm
```

```
column_cnt = len(df.columns)
--------------------
7
```

Делаем подключение к БД

```
import psycopg2

# Подключение к базе данных (параметры подключения нужно заменить на свои)
conn = psycopg2.connect(dbname="your_db", user="your_user", password="your_password", host="localhost")
cursor = conn.cursor()

# Подготовка запроса
db_schema = 'schema'
db_table = 'tablica'
query = "INSERT INTO {0}.{1}({2}) VALUES ({3})".format(db_schema, db_table, columns, ','.join(['%s'] * column_cnt))
#INSERT INTO schema.tablica(resume_id, owner_id, url, url_w_contacts, vacancy_code, search_status, t_changed_dttm) VALUES (%s,%s,%s,%s,%s,%s,%s)


# Вставка данных
cursor.executemany(query, tuples)

# Подтверждение изменений и закрытие соединения
conn.commit()
cursor.close()
conn.close()
```

**Результат:** Запрос будет выполнен, и данные из DataFrame будут вставлены в таблицу. Для каждой строки DataFrame будет выполнена вставка в таблицу с подставленными значениями.

Для каждой строки из DataFrame создается отдельная запись в SQL-запросе.

Данные преобразуются в формат, который может быть подставлен в запрос через параметры (%s).

Вставка выполняется с использованием метода executemany() для пакетной вставки данных.

Таким образом, каждый ряд из DataFrame будет вставлен в таблицу через одно выполнение запроса.

Пакетная вставка данных (или batch insert), это означает, что несколько строк данных из DataFrame будут вставлены в таблицу в рамках одного SQL-запроса, а не каждый ряд отдельно. Это позволяет значительно ускорить вставку, так как уменьшается количество запросов к базе данных.

**Что происходит при пакетной вставке:**

Пакетная вставка — это когда вместо того, чтобы делать два отдельных запроса:

```
INSERT INTO schema.tablica(resume_id, owner_id, url, url_w_contacts, vacancy_code, search_status, t_changed_dttm)
VALUES ('aaa111', 111111, 'test1', 'test_11', 10011, 'active', 'data');

#И

INSERT INTO schema.tablica(resume_id, owner_id, url, url_w_contacts, vacancy_code, search_status, t_changed_dttm)
VALUES ('aaa222', 22222, 'test2', 'test_22', 10012, 'active', 'data2');
```

Мы можем сделать один запрос, который будет вставлять сразу обе строки:

```
INSERT INTO schema.tablica(resume_id, owner_id, url, url_w_contacts, vacancy_code, search_status, t_changed_dttm)
VALUES 
('aaa111', 111111, 'test1', 'test_11', 10011, 'active', 'data'),
('aaa222', 22222, 'test2', 'test_22', 10012, 'active', 'data2');
```

Здесь мы добавляем обе строки в одном запросе, вместо того чтобы делать два отдельных запроса.

В Python с помощью библиотеки psycopg2 (для PostgreSQL) можно использовать метод executemany(), чтобы выполнить пакетную вставку. Этот метод позволяет передать сразу несколько значений для выполнения одного запроса.

`cursor.executemany(query, tuples)` — выполняет пакетную вставку, вставляя все строки из `tuples` в таблицу с помощью одного SQL-запроса. Библиотека автоматически заменяет %s в запросе на соответствующие значения из массива данных.

В результате все строки DataFrame будут вставлены одним запросом.




























