# **Представления**

В контексте баз данных, представление (View) и материализованное представление (Materialized View) — это два типа объектов базы данных, которые используются для упрощения работы с данными. 

**1. Представление (View):**

Представление — это виртуальная таблица, которая строится на основе SQL-запроса. Оно не хранит данных, а представляет собой результат выполнения запроса каждый раз, когда вы обращаетесь к этому представлению. 
По сути, это сохранённый запрос, который позволяет работать с результатом без необходимости писать его каждый раз.

Когда вы выполняете запрос к представлению, база данных выполняет запрос, который был использован для его создания, и возвращает данные, как если бы это была обычная таблица.

Пример:

Есть таблица

```
SELECT * FROM orders ORDER BY customer_id;
```

![image](https://github.com/user-attachments/assets/359b3167-8824-4ed9-8f1d-e8442b2838bb)

Создаем представление с агрегацией.
Которое будет агрегировать данные, например, подсчитывать общее количество заказов и сумму по каждому клиенту:

```
--Создание представления
CREATE VIEW customer_order_summary AS
SELECT customer_id, 
       COUNT(order_id) AS total_orders, 
       SUM(total_amount) AS total_spent
FROM orders
GROUP BY customer_id;
```

После выполенения кода, на боковой панели в папке представление появляется таблица с значком глаза. Это и есть наше представление.

![image](https://github.com/user-attachments/assets/266e21fd-4f22-4044-8004-b754dd6f3841)

Если выполним запрос и в качестве таблицы укажем представление

```
SELECT *
FROM customer_order_summary
ORDER BY customer_id
```

Получим агрегированный результат

![image](https://github.com/user-attachments/assets/1525683b-4ab4-4e27-9c1e-0529de74a761)

Добавим еще данные в таблицу `orders`

```
INSERT INTO orders (customer_id, order_date, total_amount)
VALUES
    (7, '2025-01-07', 200.00),
    (7, '2025-01-08', 400.00);
```

```
SELECT * FROM orders order by customer_id;
```

![image](https://github.com/user-attachments/assets/8044295f-d5c6-4cd6-bd06-64661a8f6635)

Теперь обращаемся к представлению

```
SELECT *
FROM customer_order_summary
ORDER BY customer_id
```

Видим агрегированный результат

![image](https://github.com/user-attachments/assets/a3ada027-184e-4e6e-a79b-5dfa967b1a08)







