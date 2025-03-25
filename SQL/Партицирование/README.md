# **Партицирование**

Создание партиций таблиц в различных СУБД (например, PostgreSQL) позволяет эффективно управлять большими объёмами данных. 
Это достигается путём разделения таблицы на несколько частей (партиций), каждая из которых хранит определённую часть данных. 

**1.Создание основной таблицы (партиционированной):**

Для создания партиционированной таблицы нужно указать, что она будет использовать партиционирование по диапазону значений (например, по дате).

Так же важный момент, если указали PRIMARY KEY, например для поля order_id, то партицированный столбец также должен быть первичным ключом, иначе будет ошибка.
Ошибка с первичным ключом возникает, потому что для партиционированных таблиц PostgreSQL требует, чтобы первичный ключ был составным, включая поле, 
по которому осуществляется партиционирование (в нашем случае — order_date). Это нужно для того, чтобы гарантировать уникальность строк в рамках каждой партиции.

*Пример ошибки:*

```
CREATE TABLE orders_2 (
    order_id SERIAL PRIMARY KEY, --Первичный ключ
    order_date DATE,
    amount DECIMAL(10, 2)
) PARTITION BY RANGE (order_date);
```

![image](https://github.com/user-attachments/assets/10266fc0-bff4-42a2-85d8-9a72a5769053)

Правильный вариант:

```
--1.Создание таблицы с PRIMARY KEY, включающим order_date
-- Создаем таблицу заказов с партиционированием по дате
CREATE TABLE orders (
    order_id SERIAL,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id, order_date)  -- Включаем order_date в PRIMARY key, если не включить, то будет ошибка
) PARTITION BY RANGE (order_date);
```

После того как основная таблица создана, вы можете создавать партиции для неё, указав диапазоны значений для каждой партиции.

```
--2.Добавление партиций для каждого месяца
-- Партиция для заказов в январе 2025 года
CREATE TABLE orders_jan_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');

-- Партиция для заказов в феврале 2025 года
CREATE TABLE orders_feb_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');

-- Партиция для заказов в марте 2025 года
CREATE TABLE orders_mar_2025 PARTITION OF orders
    FOR VALUES FROM ('2025-03-01') TO ('2025-04-01');
```

Добавление тестовых данных

```
--3.Вставка тестовых данных
-- Вставляем данные для января 2025 года
INSERT INTO orders (customer_id, order_date, total_amount)
VALUES
    (1, '2025-01-05', 150.00),
    (2, '2025-01-15', 200.50),
    (3, '2025-01-20', 99.99);

-- Вставляем данные для февраля 2025 года
INSERT INTO orders (customer_id, order_date, total_amount)
VALUES
    (4, '2025-02-05', 250.00),
    (5, '2025-02-10', 350.75);

-- Вставляем данные для марта 2025 года
INSERT INTO orders (customer_id, order_date, total_amount)
VALUES
    (6, '2025-03-01', 450.00);
```

Выводим результат

```
--4.Запросы для работы с партициями
-- Запрос всех заказов
SELECT * FROM orders;

-- Запрос заказов только за февраль 2025 года
SELECT * FROM orders WHERE order_date BETWEEN '2025-02-01' AND '2025-02-28';
```

![image](https://github.com/user-attachments/assets/5363885d-61f7-4cbe-b966-e1dd64a1c722)

Сами партиции

![image](https://github.com/user-attachments/assets/a946e2d6-9345-49dc-9af0-ed7fa6a9226a)



