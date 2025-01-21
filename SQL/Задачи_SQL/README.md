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







