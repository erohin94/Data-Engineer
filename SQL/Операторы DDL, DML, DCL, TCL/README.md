# **🏗️ DDL – Data Definition Language (определение структуры данных) (CREATE, DROP, ALTER, TRUNCATE**

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


