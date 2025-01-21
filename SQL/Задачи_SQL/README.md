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

♦️ ROW_NUMBER() будет генерировать уникальный порядковый номер (ранг) для каждой строки, даже если одна или несколько строк имеют одинаковое значение. Т. е. нумеровать по-порядку.

♦️ RANK() присвоит одинаковый номер для строки, которая содержит то же значение, и пропустит следующий номер.

♦️ DENSE_RANK() будет присваивать одинаковый номер для строки, которая содержит то же значение, но уже без пропуска следующего номера.

Для понимания, рассмотрим работу функций на конкретном примере (см. рисунок). У нас есть used_id – уникальный идентификатор пользователя, и amount – сумма заказа. 

```ROW_NUMBER``` отражает порядковый номер, тут все понятно. 

```RANK строки``` 2-4 имеют одинаковый ранг (2), а 5 – уже 5. Это связано с тем, что каждая дублирующаяся строка приводила к пропуску следующего по порядку ранга. 

```DENSE_RANK``` этот пропуск не происходил, поэтому у строки 5 стоит значение ранга – 3.









