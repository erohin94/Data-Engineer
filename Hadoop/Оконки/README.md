# RANGE и ROWS

Таблица

```
сreate table in not exists sales (
                                  sales_id INT,
                                  sales_dt TIMESTAMP,
                                  customer_id INT,
                                  item_id INT,
                                  cnt INT,
                                  price_per_item DECIMAL(19,4)
                                  );

insert into sales values(
                        (1, '2020-01-10 10:00:00', 100, 200, 2, 30.15),
                        (2, '2020-01-11 11:00:00', 100, 311, 1, 5.00),
                        (3, '2020-01-12 14:00:00', 100, 400, 1, 50.00),
                        (4, '2020-01-12 20:00:00', 100, 311, 5, 5.00),
                        (5, '2020-01-13 10:00:00', 150, 311, 1, 5.00),
                        (6, '2020-01-13 11:00:00', 100, 315, 1, 17.00),
                        (7, '2020-01-14 10:00:00', 150, 200, 2, 30.15),
                        (8, '2020-01-14 15:00:00', 100, 380, 1, 8.00),
                        (9, '2020-01-14 18:00:00', 170, 380, 3, 8.00),
                        (10, '2020-01-15 09:30:00', 100, 311, 1, 5.00),
                        (11, '2020-01-15 12:45:00', 150, 311, 5, 5.00),
                        (12, '2020-01-15 21:30:00', 170, 200, 1, 30.15) 
                        )
```

Разница функции `SUM()` с указанием сортировки и без нее:

```
SELECT sales_id, customer_id, count, 
SUM(cnt) OVER () as total,
SUM(cnt) OVER (ORDER BY customer_id) AS cum,
SUM(cnt) OVER (ORDER BY customer_id, sales_id) AS cum_uniq
FROM sales
ORDER BY customer_id, sales_id;
```

<img width="477" height="311" alt="image" src="https://github.com/user-attachments/assets/7d9e6377-9a9a-4c34-9177-c33d3e07864b" />

Фрейм бывает 2х видов `ROWS` и `RANGE`, познакомимся сначала с `ROWS`.

Варианты ограничения фрейма:

1. Все, что до текущей строки/диапазона и само значение текущей строки
   ```
   BETWEEN UNBOUNDED PRECEDING
   BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
   ```

2. Текущая строка/диапазон и все, что после нее
   ```
   BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
   ````
   
3. С конкретным указазнием сколько строк до и после включать (не поддерживается для `RANGE`)
   ```
   BETWEEN N Preceding AND N Following
   BETWEEN CURRENT ROW AND N Following
   BETWEEN N Preceding AND CURRENT ROW
   ```

Фрейм в действии.
Открываем оконку на текущую строку и все предыдущие, для функции `SUM` как видите это совпадает с сортировкой `ASC`

```
SELECT sales_id, customer_id, cnt, 
SUM(cnt) OVER (ORDER BY customer_id, sales_id) AS cum_uniq,
SUM(cnt) OVER (ORDER BY customer_id, sales_id ROWS UNBOUNDED PRECEDING) AS current_and_all_before,
SUM(cnt) OVER (ORDER BY customer_id, sales_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS current_and_all_before2
FROM sales
ORDER BY customer_id, sales_id;
```

<img width="655" height="321" alt="image" src="https://github.com/user-attachments/assets/3d87464a-b221-4759-9c12-6ed51e9cc317" />


```
SELECT sales_id, customer_id, cnt, 
SUM(cnt) OVER (ORDER BY customer_id, sales_id) AS cum_uniq,
SUM(cnt) OVER (ORDER BY customer_id, sales_id ROWS UNBOUNDED PRECEDING) AS current_and_all_before,
SUM(cnt) OVER (ORDER BY customer_id, sales_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS current_and_all_before2
FROM sales
ORDER BY cnt;
```

<img width="580" height="309" alt="image" src="https://github.com/user-attachments/assets/a3ea1200-004c-4cb8-bdfe-cdb1656900ee" />

Функционал фрейма, когда мы включаем все последующие строки.

```
SELECT sales_id, customer_id, cnt, 
SUM(cnt) OVER (ORDER BY customer_id, sales_id ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS current_and_all_frame,
SUM(cnt) OVER (ORDER BY customer_id DESC, sales_id DESC) AS current_and_all_order_desc
FROM sales
ORDER BY customer_id, sales_id;
```

<img width="573" height="318" alt="image" src="https://github.com/user-attachments/assets/3ed7f95f-b7d2-4696-a74c-59f191a04fbc" />

Вариант, когда мы указываем конкретное количество строк, которые должны войти во фрейм.

```
SELECT sales_id, customer_id, cnt, 
SUM(cnt) OVER (ORDER BY customer_id, sales_id ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS before_and_current,
cnt,
SUM(cnt) OVER (ORDER BY customer_id, sales_id ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS current_and_1_next,
cnt,
SUM(cnt) OVER (ORDER BY customer_id, sales_id ROWS BETWEEN 2 PRECEDING AND 2 FOLLOWING) AS before2_and_2_next
FROM sales
ORDER BY customer_id, sales_id;
```

<img width="726" height="276" alt="image" src="https://github.com/user-attachments/assets/eed9f8c0-bc26-4e1d-8234-f26f1bf0f300" />

**Разница ROWS и RANGE**

Разница заключается в том, что `ROWS` оперирует строкой, а `RANGE` диапазоном.

Давайте посмотрим на картинке.

<img width="684" height="757" alt="image" src="https://github.com/user-attachments/assets/726f6a87-8f5e-4b68-9a7b-811bf76bd3d6" />

Теперь, если мы внимательно посмотрим, то станет очевидно, что диапазоном называются строки с одинаковым значением параметра сортировки.

Как уже было сказано выше `ROWS` ограничивается именно строкой, в то время как `RANGE` захватывает весь диапазон совпадающих значений, которые у вас указаны в `ORDER BY` оконной функции.

```
SELECT sales_id, customer_id, cnt, 
SUM(cnt) OVER (ORDER BY customer_id) AS cum_uniq,
cnt,
SUM(cnt) OVER (ORDER BY customer_id ROWS UNBOUNDED PRECEDING) AS current_and_all_before,
customer_id,
cnt,
SUM(cnt) OVER (ORDER BY customer_id RANGE UNBOUNDED PRECEDING) AS current_and_all_before2
FROM sales
ORDER BY 2, sales_id;
```

<img width="722" height="238" alt="image" src="https://github.com/user-attachments/assets/4e9f4651-9624-4d39-86f7-546475ece6a1" />

`ROWS` — всегда оперирует конкретной строкой, даже если сортировка не уникальна, а вот `RANGE` как раз объединяет в диапазоны периоды, с совпадающими значениями полей сортировки. 
В этом смысле функциональность очень похожа на поведение функции `SUM()` с сортировкой по неуникальному полю. Посмотрим еще один пример.

```
SELECT sales_id, customer_id, price_per_item, cnt, 
SUM(cnt) OVER (ORDER BY customer_id, price_per_item) AS cum_uniq,
cnt,
SUM(cnt) OVER (ORDER BY customer_id, price_per_item ROWS UNBOUNDED PRECEDING) AS current_and_all_before,
customer_id,
cnt,
SUM(cnt) OVER (ORDER BY customer_id, price_per_item RANGE UNBOUNDED PRECEDING) AS current_and_all_before2
FROM sales
ORDER BY 2, price_per_item;
```

<img width="742" height="220" alt="image" src="https://github.com/user-attachments/assets/f22b4fdf-8960-4ce7-97d6-a9d3113fd2d5" />

Тут уже 2 поля и `range` определяется диапазоном с совпадающими значениями по обоим полям

И вариант когда мы включаем в расчет все последующие строки от текущей, который в случае с функцией `SUM` совпадает со значением, которое можно получить, воспользовавшись обратной сортировкой:

```
SELECT sales_id, customer_id, price_per_item, cnt, 
SUM(cnt) OVER (ORDER BY customer_id DESC, price_per_item DESC) AS cum_uniq,
cnt,
SUM(cnt) OVER (ORDER BY customer_id, price_per_item ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS current_and_all_before,
customer_id,
cnt,
SUM(cnt) OVER (ORDER BY customer_id, price_per_item RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) AS current_and_all_before2
FROM sales
ORDER BY 2, price_per_item, sales_id desc;
```

<img width="737" height="217" alt="image" src="https://github.com/user-attachments/assets/2e614092-d1f1-4f8f-a858-ed442c3fd5c3" />


Как видно RANGE опять же захватывает весь диапазон совпадающих пар.






















