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
      )
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
