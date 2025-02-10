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


```
--1
SELECT id_client, SUM(sum_tran)
FROM transact
WHERE  tran_time > CURRENT_DATE() - INTERVAL '30 DAY'
GROUP BY id_client
```

```
--2
-- Нашли топ 100 клиентов
WITH client_totals AS (SELECT id_client, SUM(sum_tran) AS total_spent
                       FROM transact
                       GROUP BY id_client
                       ORDER BY total_spent DESC
                       LIMIT 100)

SELECT t.id_client, EXTRACT(YEAR FROM t.tran_time) AS year, EXTRACT(MONTH FROM t.tran_time) AS month, SUM(t.sum_tran) AS monthly_spent
FROM transact t
JOIN client_totals c
ON t.id_client = c.id_client
GROUP BY t.id_client, EXTRACT(YEAR FROM t.tran_time), EXTRACT(MONTH FROM t.tran_time)
ORDER BY t.id_client, year, month;
```

# Задача 7

**Дана таблица с логом выполнения операторами задач в CRM системе. Необходимо вывести среднее время выполнения задач с status ‘failed’, созданных в текущем месяце**
```
create table crm_tasks_log (
    task_id int,
    operator_id int,
    status varchar, -- есть 4 статуса ‘failed’, 'success', 'open', 'in progress'
    created_at timestamp, -- время создания задачи
    started_at timestamp, -- время старта задачи
    closed_at timestamp -- время завершения задачи
);
```

```
SELECT AVG(EXTRACT(EPOCH FROM (closed_at - started_at)) / 3600) AS avg_hours
FROM crm_tasks_log
WHERE EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
  AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
  AND status = 'failed'
  AND closed_at IS NOT NULL;
```

# Задача 8

**Дан sql запрос, написанный аналитиком. Необходимо определить неоптимальности в запросе и предложить как их избежать. В запросе джойнятся две таблицы: таблица фактов events c ключом `event_id`, таблица-справочник источников трафика с ключом `referer_str`**

```
select *
from (select distinct e.event_id, e.user_id, e.category_id, e.location_id, s.source_name, s.medium_name, s.campaign_name,
             row_number() over(partition by e.event_id, e.user_id, e.category_id, e.location_id, s.source_name, s.medium_name, s.campaign_name) as rnk
      from events e 
      left join traffic_source s
      on e.referer_str = s.referer_str
      where e.event_date = current_date() - 1
      group by 1,2,3,4,5,6,7) t 
where rnk = 1
```

# Задача 9

**Есть две таблицы:**

**Таблица "employees":**

```
employee_id    department_id    dep salary  
1                   1               50000    
2                   2               60000   
3                   1               55000    
4                   2               52000 
```

**Таблица "departments":**

```
department_id    department_name
1                Sales
2                Marketing
```

**Необходимо вывести топ 3 самых высоких зарплат по каждому департаменту**

```
WITH t1 AS (SELECT d.department_name AS department_name, e.dep_salary AS dep_salary,
ROW_NUMBER() OVER(PARTITION BY d.department_name ORDER BY e.dep_salary DESC) AS rn
FROM employees e
JOIN departments d
ON e.department_id=d.department_id)

SELECT department_name, dep_salary, rn
FROM t1
WHERE rn <=3
```
# Задача 10

```
Orders:
- order_date datetime NOT NULL
- user_id int NOT NULL
- order_id int NOT NULL    
 
Goods:
- order_id int NOT NULL
- model int NOT NULL
- cat_1 varchar(50) NOT NULL
- price int NOT NULL
- quantity int NOT NULL

Значения в cat_1:
- Одежда
- Обувь
- Косметика
- Товары для дома
- Игрушки
```

**Вывести количество заказов и "товаров нужной категории в заказе" за 2021 год в категориях «Одежда» и за 2022 год в категории «Обувь» (Итоговый вид: 2 строки. Поля: год, количество товаров, количество заказов)**
```
SELECT EXTRACT(YEAR FROM o.order_date) AS year, SUM(g.quantity) AS total_goods, COUNT(DISTINCT o.order_id) AS total_orders
FROM Orders o
JOIN Goods g 
ON o.order_id = g.order_id
WHERE(EXTRACT(YEAR FROM o.order_date) = 2021 AND g.cat_1 = 'Одежда') OR (EXTRACT(YEAR FROM o.order_date) = 2022 AND g.cat_1 = 'Обувь')
GROUP BY year
ORDER BY year;
```

*Важно: несмотря на то, что в соответствии с порядком выполнения операторов блок SELECT выполняется после блока GROUP BY, в данном случае PostgreSQL позволяет нам немного отойти от правил и упростить процесс написания запроса. Однако такой «синтаксический сахар» есть не в каждой СУБД, поэтому при работе с другими инструментами будьте аккуратны — в общем случае рекомендуется дублировать расчётное поле в блоке GROUP BY и не использовать в нём алиасы колонок из SELECT.*

# Задача 11 (ClickHouse)

**Перечислить через запятую, в порядке убывания, в какие годы топ-5 издателей по продажам за всё время превышали продажи Global_Sales всех остальных более чем на 60. Формат ответа: Годы через запятую в порядке убывания.**

```
CREATE TABLE video_game_sales (
    Rank UInt32,
    Name String,
    Platform String,
    Year String,
    Genre String,
    Publisher String,
    NA_Sales Float32,
    EU_Sales Float32,
    JP_Sales Float32,
    Other_Sales Float32,
    Global_Sales Float32
) ENGINE = Log
```

```
INSERT INTO video_game_sales SELECT * FROM url('https://raw.githubusercontent.com/dmitrii12334/clickhouse/main/vgsale', CSVWithNames, 'Rank UInt32,
    Name String,
    Platform String,
    Year String,
    Genre String,
    Publisher String,
    NA_Sales Float32,
    EU_Sales Float32,
    JP_Sales Float32,
    Other_Sales Float32,
    Global_Sales Float32')
```

Пример таблицы

![image](https://github.com/user-attachments/assets/978cde00-6be3-461a-b113-fcd71ec87626)

Результат 

```
--В CTE находим ТОП 5 издателей по продажам за все время
WITH t1 AS (SELECT Publisher
FROM sandbox.video_game_sales_es
GROUP BY Publisher
ORDER BY SUM(Global_Sales) DESC
LIMIT 5),

--Считаем продажи по годам для топ 5 издателей и продажи по годам для всех всех издателей кроме топ 5
t2 AS (SELECT Year,
        SUM(Global_Sales) FILTER (WHERE Publisher IN (SELECT Publisher FROM t1)) AS prodazhi_top5,
        SUM(Global_Sales) FILTER (WHERE Publisher NOT IN (SELECT Publisher FROM t1)) AS prodazhi_vse_krome_top5
FROM sandbox.video_game_sales_es
GROUP BY Year)

SELECT arrayStringConcat(groupArray(Year), ',') as "Результат"
FROM
    (
    SELECT Year, prodazhi_top5, prodazhi_vse_krome_top5, prodazhi_top5 - prodazhi_vse_krome_top5 AS delta
    FROM t2
    WHERE prodazhi_top5 - prodazhi_vse_krome_top5 > 60
    ORDER BY Year DESC
    )
```

![image](https://github.com/user-attachments/assets/82e8d0f6-fe58-421f-af08-7ed21e48b43f)

**Пример с использованием OFFSET**

```
WITH top5 AS (SELECT Publisher, SUM(Global_Sales) AS first_5_sales
                          FROM sandbox.video_game_sales_es 
                          GROUP BY Publisher 
                          ORDER BY SUM(Global_Sales) DESC
                          LIMIT 5),
not_top5 AS (SELECT Publisher, SUM(Global_Sales) AS not_5_sales
                       FROM sandbox.video_game_sales_es 
                       GROUP BY Publisher 
                       ORDER BY SUM(Global_Sales) desc
                       OFFSET 5)

SELECT arrayStringConcat(groupArray("Год"), ',') as "Результат"
FROM( 
SELECT Year "Год",
            SUM(Global_Sales) filter (WHERE Publisher IN (SELECT Publisher FROM top5)) AS "Суммарная прибыль топ 5",
            SUM(Global_Sales) filter (WHERE Publisher IN (SELECT Publisher FROM not_top5)) "Суммарная прибыль всех >5",
            SUM(Global_Sales) filter (WHERE Publisher IN (SELECT Publisher FROM top5))-SUM(Global_Sales) filter (WHERE Publisher IN (SELECT Publisher FROM not_top5)) AS delta
FROM sandbox.video_game_sales_es 
GROUP BY Year
HAVING delta>60
ORDER BY Year DESC) AS rez
```

# Задача 12 (ClickHouse)

**Задача — реализовать столбец rank, который назначает порядок числу из числового столбца. Решить через CROSS JOIN и GROUP BY. Пользоваться массивами или оконными функциями в данном задании нельзя. Требуется, чтобы ранг (rank) назначался в порядке от большего к меньшему (то есть наибольшее значение получает ранг 1, следующее — ранг 2 и так далее)**

```
CREATE TABLE cross_join
(
    user UInt64,
    value UInt64
)
ENGINE = Log
```

```
INSERT INTO cross_join (*) VALUES (50, 136),  (16, 188),  (42, 190),  (92, 106),  (61, 173),  (96, 192),  (30, 182),  (71, 179),  (48, 160),  (31, 103),  (74, 178),  (27, 102),  (77, 105),  (62, 120),  (84, 177),  (49, 164),  (70, 184),  (46, 145),  (17, 100),  (39, 114),  (55, 121),  (87, 123),  (68, 119),  (58, 115),  (85, 122),  (69, 148),  (75, 175),  (18, 101),  (22, 158),  (43, 104),  (0, 162),  (97, 163),  (6, 131),  (78, 128),  (59, 159),  (37, 156),  (40, 107),  (2, 194),  (11, 134),  (8, 189),  (83, 187),  (7, 197),  (64, 111),  (1, 117),  (79, 161),  (21, 110),  (76, 109),  (60, 170),  (57, 191),  (54, 108),  (13, 139),  (80, 125),  (35, 129),  (82, 171),  (89, 153),  (66, 174),  (95, 135),  (41, 193),  (15, 141),  (81, 127),  (24, 181),  (36, 146),  (34, 142),  (67, 143),  (53, 140),  (93, 113),  (44, 149),  (26, 198),  (19, 138),  (63, 147),  (32, 186),  (88, 180),  (20, 172),  (29, 151),  (5, 169),  (73, 124),  (25, 185),  (72, 183),  (3, 154),  (14, 118),  (9, 133),  (52, 112),  (45, 199),  (4, 132),  (98, 144),  (38, 152),  (10, 157),  (65, 165),  (90, 176),  (47, 137),  (12, 116),  (28, 168),  (33, 130),  (94, 167),  (23, 166),  (56, 196),  (99, 195),  (51, 150),  (86, 126),  (91, 155)
```

Результат

```
SELECT sum(rank * value) AS result
FROM (
        SELECT c1.user, c1.value, COUNT(*) AS rank
        FROM cross_join c1
        CROSS JOIN cross_join c2
        WHERE c1.value <= c2.value
        GROUP BY c1.user, c1.value
    )
```

Объяснение:
`CROSS JOIN`: Мы соединяем таблицу cross_join саму с собой. Это позволяет сравнить каждое значение с каждым другим значением.

`WHERE c1.value <= c2.value: Фильтруем результаты, оставляя только те пары, где значение из c1 меньше или равно значению из c2. Основной кусок, благодаря которуму отсекутся все записи которые больше данного числа. После чего с помощью группировки посчитается количество - тоесть ранг.

`GROUP BY c1.user, c1.value`: Группируем результаты по пользователю и значению, чтобы подсчитать количество строк, удовлетворяющих условию.

`COUNT(*) AS rank`: Подсчитываем количество строк в каждой группе, что и будет рангом.

`sum(rank * value)`: Вычисляем сумму произведений ранга на значение.



























