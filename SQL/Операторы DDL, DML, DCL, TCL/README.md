# **🏗️ DDL – Data Definition Language (определение структуры данных) (CREATE, DROP, ALTER, TRUNCATE**

**Операции для определения структуры объектов базы данных: схем, таблиц, индексов, типов и пр.**

📁 `CREATE SCHEMA` – создание схемы. Схема — это логическое объединение объектов (удобно для организации данных).

📦 `CREATE TABLE` – создание таблицы. Создание таблицы с типами данных и ограничениями.

🛠️ `ALTER TABLE` – изменение таблицы (структуры). Добавить/удалить столбец, изменить тип.

🧹 `TRUNCATE TABLE` – быстрая очистка. Полностью удаляет данные без возможности отката.

❌ `DROP TABLE / DROP SCHEMA` - Удаляет таблицу/схему навсегда.

После создания схемы и таблицы получаем следующую структуру:

![image](https://github.com/user-attachments/assets/feea2b1c-9bd4-4cf7-9e0c-7b0e49ac1ba1)

Добавить столбец:

![image](https://github.com/user-attachments/assets/5b58b79d-0a1d-4d9c-b9b8-414e003bed8d)

Удалили столбец и изменили тип данных (столбца amount TYPE FLOAT):

![image](https://github.com/user-attachments/assets/f0134336-5a2e-4d30-9f91-eb8453f5a160)

