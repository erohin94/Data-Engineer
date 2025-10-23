## Проверка, что в столбце числа

```
SELECT cast('sfaf' as int) AS col_1, cast('12323' as int) AS col_2
```

![image](https://github.com/user-attachments/assets/5a090ce5-0cfb-4afa-a70e-fa5ff0c8725b) 

Если в столбец `priority` будет введена строка, например `1556Abc`, то `CAST(priority as int) ` даст `NULL`. 

И такие строки где тип данных не число мы исключаем, применяя фильтрацию `WHERE CAST(priority as int) IS NOT NULL`. 

```
SELECT * 
FROM dm_es.view_model
WHERE CAST(priority as int) IS NOT NULL
```

## Проверка заполняемости полей

После того как собрал витрину `table_mart`, можно проверить расчитанные атрибуты в результирующей таблице на заполняемость полей.
С помощью SQL запроса ниже. Где `table_mart` - это итоговая витрина. А `atr_1, atr_2, atr_3` атрибуты, которые считал на основе источников, согласно БТ.
После чего соединил их в одну таблицу `table_mart` по идентификатору `pid_id` и отчетному месяцу `report_dt`

```
SELECT
      COUNT(atr_1)/COUNT(*) AS atr_1
      COUNT(atr_2)/COUNT(*) AS atr_2
      COUNT(atr_3)/COUNT(*) AS atr_3
FROM table_mart
GROUP BY report_dt
ORDER BY report_dt
```

<img width="514" height="649" alt="image" src="https://github.com/user-attachments/assets/ac232544-66d2-4ca6-afac-7bb623fef741" />

Если для каких то месяцев будут пропуски, то следует проверить либо сам расчет, либо источник (на основе которого был произведен расчет) на полноту данных.

## Проверка длины строки - подсчет символов

```
SELECT
LENGTH('Было интересно и информативно!!!') AS leng,
LENGTH(REGEXP_REPLACE('Было интересно и информативно!!!', '.', 'X')) AS leng_reg_rep,
REGEXP_REPLACE('Было интересно и информативно!!!', '.', 'X') AS reg_rep;
```

<img width="706" height="249" alt="image" src="https://github.com/user-attachments/assets/80ed8785-2e18-4549-9070-338805ccf24c" />

При подсчете количества символов с помощью `LENGTH` заметил, что не корректно считает (из за кодировки), поэтому сделал подсчет с помощью `REGEXP_REPLACE`

Функция `REGEXP_REPLACE('Было интересно и информативно!!!', '.', 'X')` делает следующее:

`. (точка)` в регулярных выражениях означает "любой один символ"

`REGEXP_REPLACE` ищет ВСЕ совпадения с шаблоном в строке

Заменяет каждый найденный символ на букву `'X'`

## Узнать размер таблицы в Impala

`SHOW TABLE STATS database_name.table_name`

<img width="1111" height="50" alt="image" src="https://github.com/user-attachments/assets/7b82aaf1-abb3-406f-a55e-0f7ac98c0e48" />

Не забыть сделать `COMPUTE STATS database_name.table_name` перед сбором статистики

## Кейс расчета атрибута для витрины

Надо расчитать атрибут `interact_week_cnt` для витрины.

`interact_week_cnt` - Количество рабочих недель (неделя - временной отрезок с понедельника по воскресенье), когда между сотрудниками происходило взаимодействие (встреча, звонок, лайк), за последний месяц. Для зачета календарного месяца необходимо наличие хотя бы одного любого взаимодействия (встреча звонок лайк).

Первичный расчет витрины начинается с `2023-09-08`. Далее обновление будет происходить каждую неделю инкрементом, без удаления старых данных в витрине.

Сложность возникла в том что надо определять данные за последний месяц, который определяется как 4 отчетных периода(недели) с учетом текущего. Тоесть расчет витрины 26.10.2025, то расчет делаем за 26.10.2025 минус 4 недели.

Описание:

Есть пара `user_id` (Пользователь) и `object_id` (Обьект с кем взаимодействует пользователь) между которыми происходит взаимодействие, 
`report_dt` - отчетная неделя (Последний день недели).

И есть взаимодействия  `cnt_interactions_calls`, `cnt_interactions_meet`, `cnt_interactions_like` по звонкам встречам и лайкам. 

**Таблица t1**  
```
user_id    object_id    report_dt      cnt_interactions_calls   cnt_interactions_meet   cnt_interactions_like                 
77240      95419         2024-01-14   0                                  1                                  0
77240      95419         2024-01-21   0                                  1                                  0
77240      95419         2024-01-28   0                                  1                                  0
77240      95419         2024-02-04   0                                  1                                  0
77240      95419         2024-02-11   0                                  1                                  0
.............................................................................................................................
77240      95419         2025-03-02   0                                  1                                  0
```

**Алгоритм получения атрибута**

Количество отчетных периодов по полю `report_dt` за последний месяц (4 отчетных периода с учетом текущего), когда в витрине присутсвовала пара `user_id` - `object-id`.
Присутсвие я определил с помощью флага.

**Решение**

Использовал `ROWS BETWEEN 3 PRECEDING AND CURRENT ROW`

```
WITH t2 AS (SELECT user_id, 
                   object_id, 
                   report_dt,
                   (cnt_interactions_calls + cnt_interactions_meet + cnt_interactions_like) AS sum_all_nteractions
            FROM t1),
t3 AS (SELECT user_id, 
              object_id, 
              report_dt,
              sum_all_nteractions
              /* Задаю флаг, если за отчетную неделю были какие то взаимодйсвия то ставлю флаг 1 */
              CASE WHEN  sum_all_nteractions > 0 THEN 1 ELSE 0 END AS flg
      FROM t2)
SELECT 
    user_id,
    object_id,
    report_dt,
    -- Количество недель с взаимодействием за последние 4 недели (включая текущую)
    SUM(has_interaction) OVER (PARTITION BY user_id, object_id ORDER BY report_dt ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS interact_week_cnt
FROM t3
ORDER BY user_id, object_id, report_dt;
 ```     

Примеры промежуточных результатов

t1

<img width="847" height="227" alt="image" src="https://github.com/user-attachments/assets/be3f3fd8-c8fe-4824-8d05-c9b883a39b6f" />

t2

<img width="506" height="235" alt="image" src="https://github.com/user-attachments/assets/6e42768d-c404-47fd-8087-67d96db00a87" />

t3

<img width="418" height="231" alt="image" src="https://github.com/user-attachments/assets/b6399172-6389-448a-a778-28745d3e0f57" />

Итог

<img width="565" height="248" alt="image" src="https://github.com/user-attachments/assets/7b450120-6cff-4fe2-82db-f1bec76d38b4" />

