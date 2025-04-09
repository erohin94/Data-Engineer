# **🏗️ 1. DDL – Data Definition Language (определение структуры данных) (CREATE, DROP, ALTER, TRUNCATE)**

**Операции для определения структуры объектов базы данных: схем, таблиц, индексов, типов и пр.**

📁 `CREATE SCHEMA` – создание схемы. Схема — это логическое объединение объектов (удобно для организации данных).

📦 `CREATE TABLE` – создание таблицы. Создание таблицы с типами данных и ограничениями.

🛠️ `ALTER TABLE` – изменение таблицы (структуры). Добавить/удалить столбец, изменить тип.

🧹 `TRUNCATE TABLE` – быстрая очистка таблицы. Полностью удаляет данные без возможности отката.

❌ `DROP TABLE / DROP SCHEMA` - Удаляет таблицу/схему навсегда.

После создания схемы и таблицы получаем следующую структуру:

![image](https://github.com/user-attachments/assets/feea2b1c-9bd4-4cf7-9e0c-7b0e49ac1ba1)

Добавить столбец:

![image](https://github.com/user-attachments/assets/5b58b79d-0a1d-4d9c-b9b8-414e003bed8d)

Удалили столбец и изменили тип данных (столбца amount TYPE FLOAT):

![image](https://github.com/user-attachments/assets/f0134336-5a2e-4d30-9f91-eb8453f5a160)

```
CREATE SCHEMA sales_data;

CREATE TABLE sales_data.transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    amount DECIMAL(10, 2) CHECK (amount > 0)
);

ALTER TABLE sales_data.transactions ADD COLUMN payment_method VARCHAR(20);
ALTER TABLE sales_data.transactions DROP COLUMN payment_method;
ALTER TABLE sales_data.transactions ALTER COLUMN amount TYPE FLOAT;

TRUNCATE TABLE sales_data.transactions;

DROP TABLE sales_data.transactions;
DROP SCHEMA sales_data;

DROP SCHEMA sales_data CASCADE; --Использовать команду CASCADE аккуратно

select * from sales_data.transactions
```
**Команда `EXISTS`** в SQL используется как логическая проверка — чтобы определить, существует ли результат запроса или объект (например, таблица). Она особенно полезна в WHERE и IF выражениях, а также при условном создании или удалении объектов.

✅ EXISTS — в запросах (для данных)

```
--Проверить, есть ли покупки у клиента
--Вернёт имена только тех клиентов, у которых есть хотя бы одна транзакция.
--EXISTS возвращает TRUE, если подзапрос вернул хотя бы одну строку.
--SELECT 1 — можно писать что угодно, данные не возвращаются, важен факт наличия строк.
SELECT name
FROM customers c
WHERE EXISTS (
    SELECT 1
    FROM transactions t
    WHERE t.customer_id = c.customer_id
);
```

🏗️ IF EXISTS / IF NOT EXISTS — для структур

Эти конструкции применяются с `CREATE` и `DROP`, чтобы избежать ошибок, если объект уже существует или не существует.

```
---Создать таблицу, если её ещё нет
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT
);

--Удалить таблицу, только если она существует
DROP TABLE IF EXISTS users;

--Проверка существования схемы, таблицы, колонки (PostgreSQL)
--Вернёт true или false — в зависимости от того, есть ли таблица public.users
SELECT EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_schema = 'public'
      AND table_name = 'users'
);
```

**🔍 Важно!!! Что делает DROP SCHEMA sales_data CASCADE;?**

Удаляет схему sales_data

Автоматически удаляет все таблицы, представления, последовательности, функции и другие объекты, которые находятся в этой схеме

Удаление без дополнительных подтверждений — если что-то связано, оно тоже будет удалено

Без `CASCADE`, удалить схему если в ней есть таблица не получится. Сначала надо будет удалить таблицу, потом схему, иначе будет ошибка:

![image](https://github.com/user-attachments/assets/0bec841d-ecb1-45d8-8731-1fefd76ba6e3)

Аналогично работает и в других случаях:

```
DROP TABLE customers CASCADE;
-- Удалит таблицу и ВСЕ внешние ключи, представления, которые на неё ссылаются
```

`CASCADE` — опасная команда в продуктивных БД, потому что она может удалить всё, что связано, без возможности восстановления (если нет бэкапа).

# **📝 2. DML – Data Manipulation Language (Операции над содержимым таблиц) (SELECT, INSERT, UPDATE, DELETE)**

Операции для вставки, изменения, удаления и чтения данных.

Операции над содержимым таблиц:

`SELECT` — выбрать данные

`INSERT` — вставить строку

`UPDATE` — обновить строку

`DELETE` — удалить строку

```
INSERT INTO sales_data.transactions (customer_id, product_id, transaction_date, amount)
VALUES (101, 5, '2024-01-15', 150.75);

--Множественная вставка:
INSERT INTO sales_data.transactions (customer_id, product_id, transaction_date, amount)
VALUES 
(102, 3, '2024-01-16', 99.99),
(103, 2, '2024-01-17', 249.00);

UPDATE sales_data.transactions
SET amount = 200.00
WHERE transaction_id = 1;

DELETE FROM sales_data.transactions
WHERE transaction_date < '2024-01-16';

SELECT * FROM sales_data.transactions;
SELECT customer_id, SUM(amount) AS total_spent
FROM sales_data.transactions
GROUP BY customer_id;

SELECT * FROM sales_data.transactions
```

# **🔐 3. DCL – Data Control Language (управление доступом) (GRANT, REVOKE)**

Контроль прав доступа. Управляют правами доступа к объектам базы данных: таблицам, схемам, представлениям, функциям и т. д.

**🔐 GRANT — предоставить права**

📌 Синтаксис:

```
GRANT привилегии
ON объект
TO пользователь [WITH GRANT OPTION];
```

🔹 Примеры:

1. Дать пользователю analyst_user права только на чтение таблицы:

```
GRANT SELECT ON sales_data.transactions TO analyst_user;
```

2. Дать полные права на таблицу:

```
GRANT SELECT, INSERT, UPDATE, DELETE ON sales_data.transactions TO data_engineer;
```

3. Дать право создавать таблицы в схеме:

```
GRANT CREATE ON SCHEMA sales_data TO junior_dev;
```

4. С правом передачи прав (WITH GRANT OPTION):

```
GRANT SELECT ON sales_data.transactions TO team_lead WITH GRANT OPTION;
```

Теперь team_lead может давать другим пользователям доступ к таблице.

**🛑 REVOKE — отозвать права**

📌 Синтаксис:

```
REVOKE привилегии
ON объект
FROM пользователь;
```

🔹 Примеры:

1. Убрать права на вставку:

```
REVOKE INSERT ON sales_data.transactions FROM analyst_user;
```

2. Полностью убрать все права:

```
REVOKE ALL ON sales_data.transactions FROM data_engineer;
```

3. Отозвать только право делиться правами:

```
REVOKE GRANT OPTION FOR SELECT ON sales_data.transactions FROM team_lead;
```

🧠 Полезно знать

В PostgreSQL пользователи и роли — одно и то же (ROLE)

Есть системные роли (postgres, pg_read_all_data, pg_write_all_data)

Права можно выдавать не только пользователям, но и группам ролей

📋 Таблица распространённых привилегий:

```
Объект	        Привилегии
TABLE	        SELECT, INSERT, UPDATE, DELETE, REFERENCES
SCHEMA	        USAGE, CREATE
DATABASE	    CONNECT, CREATE, TEMP
FUNCTION	    EXECUTE
```

**Как посмотреть текущие права доступа (привилегии) к таблицам, схемам и другим объектам в PostgreSQL — через системные представления и SQL-запросы.**

🔎 1. Посмотреть права на таблицу

```
SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_name = 'transactions'
  AND table_schema = 'sales_data';
```

🔍 Покажет:

- кто (grantee) имеет доступ

- какие привилегии (SELECT, INSERT, и т.д.)

test - это пользователь

![image](https://github.com/user-attachments/assets/bb78723c-f974-46b7-b52c-747dca176468)

![image](https://github.com/user-attachments/assets/c1f06b4c-a9b7-466a-9fc4-9cb7358fa8f2)

🔎 2. Права по всем таблицам в схеме

```
SELECT table_schema, table_name, grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'sales_data';
```

📋 Это удобно, если хочешь посмотреть все доступы по своей схеме.

🔎 3. Права на схему

```
SELECT grantee, privilege_type
FROM information_schema.role_usage_grants
WHERE object_type = 'SCHEMA'
  AND object_name = 'sales_data';
```

🔎 4. Права на функции

```
SELECT grantee, specific_name, privilege_type
FROM information_schema.role_routine_grants
WHERE routine_schema = 'public';
```

🔎 5. Права на уровне базы данных (например, подключение)

```
SELECT datacl
FROM pg_database
WHERE datname = 'your_database_name';
```

💡 datacl — это массив текстов с правами (user=CTc/postgres, например CONNECT, TEMP, CREATE).

🔎 6. Права по ролям

```
SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin
FROM pg_roles;
```
📌 Показывает:

-суперпользователь?

-может ли создавать другие роли?

-может ли логиниться?

# **🔄 4. TCL – Transaction Control Language (управление транзакциями)**

Операции контроля транзакций:

`BEGIN / START TRANSACTION` — начало транзакции

`COMMIT` — зафиксировать изменения

`ROLLBACK` — откатить транзакцию

`SAVEPOINT` — установить точку сохранения

`RELEASE SAVEPOINT` — удалить точку сохранения

`SET TRANSACTION` — установить параметры транзакции

Транзакция — это группа операций, которая выполняется целиком или не выполняется вовсе.
Она обеспечивает целостность данных в случае сбоев, ошибок или откатов.

Для управления транзакциями (важно в ETL, особенно при загрузке данных).

🧾 BEGIN, COMMIT, ROLLBACK

🔹 1. BEGIN / START TRANSACTION

Открывает новую транзакцию. Все последующие операции будут частью этой транзакции, пока не будет выполнена COMMIT или ROLLBACK.
```
BEGIN;
-- или
START TRANSACTION;
```

🔹 2. COMMIT

Фиксирует изменения, сделанные в рамках транзакции — сохраняет их навсегда в БД.

```
COMMIT;
```

🔹 3. ROLLBACK

Отменяет все изменения, сделанные после BEGIN, и возвращает БД к предыдущему стабильному состоянию.

```
ROLLBACK;
```
💡 Пример: ручное управление транзакцией

```
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE user_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE user_id = 2;

-- если всё прошло успешно
COMMIT;

-- если произошла ошибка
ROLLBACK;
```

🧠 Когда использовать?

```
Ситуация	                                Почему
Обновление нескольких таблиц	            Чтобы не оставить данные в несогласованном состоянии
Массовые изменения данных	                Можно отменить, если что-то пошло не так
Вставка данных из ETL-пайплайнов	        Гарантия целостности при загрузке
Финансовые и бухгалтерские операции	        Обязательна целостность
```

🔐 Автоматическая vs ручная транзакция

По умолчанию в PostgreSQL каждый запрос — это отдельная транзакция (автоматическая фиксация).

Но ты можешь начать транзакцию вручную и контролировать её полностью.

📋 Дополнительно

Команда	                                Назначение
SAVEPOINT	                            Создание точки отката внутри транзакции
ROLLBACK TO	                            Откат к указанной точке
SET TRANSACTION	                        Задание уровня изоляции транзакции


🧷 SAVEPOINT и ROLLBACK TO

🎯 Зачем нужен SAVEPOINT?

Создаёт «чекпоинт» внутри транзакции

Можно откатиться до него с помощью ROLLBACK TO

Позволяет продолжить выполнение остальных операций

```
BEGIN;

-- шаг 1: всё хорошо
INSERT INTO products (id, name, price) VALUES (101, 'Product A', 9.99);

-- сохраняем точку
SAVEPOINT before_discount;

-- шаг 2: возможно, ошибочный
UPDATE products SET price = price / 0 WHERE id = 101; -- деление на 0 вызовет ошибку

-- если ошибка, откатим только этот шаг
ROLLBACK TO SAVEPOINT before_discount;

-- продолжим выполнение
UPDATE products SET price = price * 0.9 WHERE id = 101;

COMMIT;
```

📌 Что произойдёт:

1.Добавим продукт

2.Сделаем ошибку (/0) → сработает ROLLBACK TO

3.Вместо этого применим скидку 10%

4.Все изменения (вставка + скидка) сохранятся при COMMIT

🧰 Полезно в ETL-сценариях

Представим, ты загружаешь данные из файла построчно:

```
BEGIN;

-- строка 1
SAVEPOINT row1;
INSERT INTO clients VALUES (...);

-- строка 2
SAVEPOINT row2;
-- что-то пошло не так
ROLLBACK TO row2;

-- строка 3
SAVEPOINT row3;
INSERT INTO clients VALUES (...);

COMMIT;
```

📊 В результате:

строка 1 и строка 3 загружены

строка 2 — пропущена (но остальное не пострадало)








