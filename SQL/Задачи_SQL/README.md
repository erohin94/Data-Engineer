# Задача 1

**Есть таблица с покупками Purchase(client_id, date)
Нужно достать дату первой покупки для каждого клиента**

1-й способ

```
SELECT client_id, MIN(date) 
FROM Purchase
GROUP BY client_id
```

2-й способ с помощью оконки

```
SELECT client_id, date
FROM (
      SELECT client_id, date,
      ROW_NUMBER() OVER(PARTITION BY client_id ORDER BY date) AS rn
      FROM Purchase
      ) t1
WHERE rn =1
```

# Задача 2

**Есть таблица с открытиями приложения Open(client_id, datetime)
Нужно достать информацию о последнем открытии приложения для каждого клиента**

Не совсем лаконичное решение

```
SELECT client_id, datetime
FROM Open o
INNER JOIN (
            SELECT client_id, MAX(datetime) AS max_datetime
            FROM Open
            GROUP BY client_id  
            ) t1
ON o.client_id = t1.client_id AND o.datetime = t1.max_datetime
```

# Задача 3

**Есть таблица с информацией о городах City(city, population)
Нужно достать топ - 5 городов по численности населения. В случае наличия городов с одинаковой численностью населения все равно выводить только топ 5 городов**

1-й способ

```
SELECT city, population,
FROM (
      SELECT city, population,
      ROW_NUMBER OVER(ORDER BY population DESC) AS rn
      FROM City) t1
WHERE rn <= 5
```

2-й способ

```
SELECT city, MAX(population) as population
FROM City
ORDER BY population DESC
LIMIT 5
```

# Задача 4

**Чем отличаются SQL функции ROW_NUMBER, RANK и DENSE_RANK?**

![image](https://github.com/user-attachments/assets/1158be16-78ce-4958-a7f1-8d2e22b1bc3e)

Все три функции используются для нумерации строк результата запроса.

♦️ ```ROW_NUMBER()``` будет генерировать уникальный порядковый номер (ранг) для каждой строки, даже если одна или несколько строк имеют одинаковое значение. Т. е. нумеровать по-порядку.

♦️ ```RANK()``` присвоит одинаковый номер для строки, которая содержит то же значение, и пропустит следующий номер.

♦️ ```DENSE_RANK()``` будет присваивать одинаковый номер для строки, которая содержит то же значение, но уже без пропуска следующего номера.

Для понимания, рассмотрим работу функций на конкретном примере (см. рисунок). У нас есть used_id – уникальный идентификатор пользователя, и amount – сумма заказа. 

```ROW_NUMBER``` отражает порядковый номер, тут все понятно. 

```RANK строки``` 2-4 имеют одинаковый ранг (2), а 5 – уже 5. Это связано с тем, что каждая дублирующаяся строка приводила к пропуску следующего по порядку ранга. 

```DENSE_RANK``` этот пропуск не происходил, поэтому у строки 5 стоит значение ранга – 3.

# Задача 5

**Напишите 2 SQL запроса для поиска значений среднего и медианы по сумме продажи. Сумму транзакции округляем до целой части. Нельзя использовать стандартные функции среднего и медианы в SQL. Можно использовать только агрегатные функции SUM и COUNT. Схема данных: Orders (id, sale_amount, user_id, datetime). sale_amount записывается в центах.**

```
--Среднее
SELECT ROUND(SUM(sale_amount)/COUNT(sale_amount), 0) AS srednee
FROM Orders

--Медиана если количество продаж нечетное
SELECT sale_amount AS median
FROM Orders
ORDER BY sale_amount OFFSET (SELECT COUNT(*) FROM Orders) / 2
LIMIT 1 
```

Общий вариант для медианы

```
WITH ordered_sales AS (SELECT sale_amount,
                       ROW_NUMBER() OVER (ORDER BY sale_amount) AS rn,
                       COUNT(*) OVER () AS total_count
                       FROM Orders)
SELECT 
CASE 
WHEN total_count % 2 = 1 THEN (SELECT sale_amount FROM ordered_sales WHERE rn = (total_count + 1) / 2) -- Если количество строк нечетное, возвращаем средний элемент
ELSE (SELECT (sale_amount + next_sale_amount) / 2 FROM (SELECT sale_amount, LEAD(sale_amount) OVER (ORDER BY rn) AS next_sale_amount FROM ordered_sales
                                                           WHERE rn IN (total_count / 2, total_count / 2 + 1) AS median_values) -- Если количество строк четное, усредняем два центральных элемента
END AS median_sale_amount;
```

Про OFFSET

```
SELECT * FROM users
LIMIT 10 OFFSET 20;
```
Этот запрос извлекает 10 записей, начиная с 21-й записи (так как индексы начинаются с 0, офсет 20 означает, что мы начинаем с 21-й строки).

# Задача 6

**Есть таблица transact с транзакциями клиентов, начиная с 2021 года. В ней столбцы:** 

**id_client - id клиента** 

**tran_time - время транзакции**

**id_tran - id транзакции**

**sum_tran - сумма транзакции**

**1. Посчитать траты каждого клиента за последние 30 дней от текущего числа;**

**2. Для топ-100 наиболее платежеспособных клиентов за всю историю покупок посчитать траты помесячно.**

--1
SELECT id_client, SUM(sum_tran)
FROM transact
WHERE  tran_time > CURRENT_DATE() - INTERVAL '30 DAY'
GROUP BY id_client

--2
WITH t1 AS (SELECT DATE_TRUNC()
FROM transact)

SELECT SUM(sum_tran)
FROM transact
GROUP BY id_client, 
LIMIT 100


