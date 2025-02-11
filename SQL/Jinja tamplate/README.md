# Применение jinja для фильтрации показателей

**Создаем датасет для фильтра**

Сгенерируем серию с '2025-01-01' по '2025-03-02' и далее сгрупирую по номеру месяца

```
SELECT month_number, 
       CONCAT(TO_CHAR(MIN(day), 'DD.MM.YYYY'), ' - ', TO_CHAR(MAX(day), 'DD.MM.YYYY')) as "Период", 
       CONCAT(TO_CHAR(MIN(day), 'YYYY-MM-DD'), ' - ', TO_CHAR(MAX(day), 'YYYY-MM-DD')) as "Период jinja" 
FROM(
   SELECT day, EXTRACT(month FROM day) AS month_number
   FROM generate_series('2025-01-01'::date, '2025-03-02'::date, '1 day'::interval) AS day   
      
    ) as rez
group by 1
order by 1
```

Запрос

![image](https://github.com/user-attachments/assets/72f772d0-4685-4dcd-a4f4-d0424e3a30d7)

Датасет

![image](https://github.com/user-attachments/assets/4f2c40f1-22d4-4853-9701-84055693f298)

**Создаем датасет для показателя**

Также сгенерируем датасет для показателя, получим таблицу с датами и номером дня конкретного месяца

```
SELECT day, EXTRACT(day FROM day) AS day_number
FROM generate_series('2025-01-01'::date, '2025-03-02'::date, '1 day'::interval) AS day
```
 Запрос
 
![image](https://github.com/user-attachments/assets/91a43a21-7b1e-4fe7-8c24-1ba88db372cb)

Датасет

![image](https://github.com/user-attachments/assets/156b6108-b57b-4eda-ab12-1d0208adf0bb)

Получаем два датасета, которые будем использовать для построения графика и фильтра jinja

![image](https://github.com/user-attachments/assets/25d52c65-c072-4c42-8323-96f0e04c1a38)

**Создание графика показателя**

Сделаем простой график показателя, чтобы понять как работает jinja. Будем считать сумму по столбцу ```day_number```.

По дефолту(когда никаких фильтров нет) будет браться период с '2025-01-01' по '2025-03-02' и считаться сумма, которая будет равняться 903.

Но если применить фильтр, на боковой панели superset, то будет рассчитываться сумма за тот период который в нашем фильтре, то есть по месяцам.

Для реализации этого в показатле, при настройке графика, надо прописать следующее:

```
SUM(day_number) filter (where day>=concat(right(left($$'{{ filter_values('Период jinja')[0]| default('2025-01-01')}}'$$, 12),12), '''')::date - interval '2 days 8 hours 13 minute 59 seconds'
 and day<concat(left(right($$'{{ filter_values('Период jinja')[0]| default('2025-03-02')}}'$$, 12),12), '''')::date - interval '8 hours 14 minute 59 seconds')
```

![image](https://github.com/user-attachments/assets/1905d010-7792-46f3-965a-7d0fe88048ea)

**Создание дашборда и добавление фильтров**

Создадим дашборд с графиком из предыдущего шага. Так же добавим фильтры на боковой панели superset. Фильтр строим на основе запроса, который генерирует датасет для фильтра.

![image](https://github.com/user-attachments/assets/39c8d3dc-d60c-413c-bf71-c0be66343785)

![image](https://github.com/user-attachments/assets/8abea7b8-4bc6-494f-b4cf-596a19f2a60c)

![image](https://github.com/user-attachments/assets/888aa505-02df-4f4a-8f48-c88096ca8f3e)

![image](https://github.com/user-attachments/assets/ccd1f771-003c-4c3a-b28b-1842230d2277)


**Пример работы**

В исходном состоянии когда не выбраны никакие фильтры на боковой панели суперсет, получаем следующее. Как видно, значение показателя равно 903.

![image](https://github.com/user-attachments/assets/badde948-25e3-4f4e-8a14-6d57482abe55)

Так же если посмотреть сгенерированный запрос на графике, то будет видно границы которые были заданы по дефолту '2025-01-01' по '2025-03-02':

```
SELECT SUM(day_number) filter (
                               where day>=concat(right(left($$'2025-01-01'$$, 12), 12), '''')::date - interval '2 days 8 hours 13 minute 59 seconds'
                                 and day<concat(left(right($$'2025-03-02'$$, 12), 12), '''')::date - interval '8 hours 14 minute 59 seconds') AS "Показатель"
FROM
  (SELECT day,
          EXTRACT(day
                  FROM day) AS day_number
   FROM generate_series('2025-01-01'::date, '2025-03-02'::date, '1 day'::interval) AS day) AS virtual_table
LIMIT 50000;
```

![image](https://github.com/user-attachments/assets/5a26613e-8c5f-4ef2-96c3-711dd34a54df)

Так же если провалится в редактирование графика, то в поле "Фильтры" только одна метка "day(без фильтра)"

![image](https://github.com/user-attachments/assets/fba45545-dbbb-42f2-9830-b7f43a0b1fd4)

Но если на боковой панели дашборда выбрать интервал

![image](https://github.com/user-attachments/assets/7c31b3f2-5472-4c19-b755-5bbf91e6eee2)

Сгенерированный запрос, 
```
SELECT SUM(day_number) filter (
                               where day>=concat(right(left($$'2025-01-01 - 2025-01-31'$$, 12), 12), '''')::date - interval '2 days 8 hours 13 minute 59 seconds'
                                 and day<concat(left(right($$'2025-01-01 - 2025-01-31'$$, 12), 12), '''')::date - interval '8 hours 14 minute 59 seconds') AS "Показатель"
FROM
  (SELECT day,
          EXTRACT(day
                  FROM day) AS day_number
   FROM generate_series('2025-01-01'::date, '2025-03-02'::date, '1 day'::interval) AS day) AS virtual_table
LIMIT 50000;
```

Как видно подставился интервал который выбран в боковом фильтре. В результате чего показатель расчитался для заданного интервала даты

![image](https://github.com/user-attachments/assets/b94c337f-69ee-4c30-95f1-5575d9bb13ba)

В графике применился фильтр. Видно в поле "Фильтр" в настройке графика

![image](https://github.com/user-attachments/assets/cc612f65-ba60-4f8c-90f1-8fd4bb300c1b)

Тоесть jinja тянет требуемый интервал и на основе чего применяет фильтрацию для графика. Если ничего не задано, то по дефолту возвращается дата, которая установлена в праметрах по дефолту
![image](https://github.com/user-attachments/assets/408b6d5d-f9f1-4da9-aeac-9813af9a4887)

Также можно проверить, сгенерировав запрос и посчитав сумму. Получим значение равное 465

```
WITH t1 AS(SELECT day, EXTRACT(day FROM day) AS day_number
FROM generate_series('2025-01-01'::date, '2025-03-02'::date, '1 day'::interval) AS day   
WHERE day <= '2025-01-31'::date - INTERVAL '8 hours 14 minute 59 seconds')

select sum(day_number)
From t1
```

![image](https://github.com/user-attachments/assets/77d9a306-b6be-4956-9e4e-f7d60e1a5a59)


**Пример нативного фильтра**

Есть еще один вариант фильтра, это нативный фильтр.

Строится на том же запросе. Только выносится из боковой панели фильтров на сам дашборд.

![image](https://github.com/user-attachments/assets/7bd95e97-025e-48fe-9b8c-0405718dd26b)

Чтобы добавить, выбрать "Редактировать дашборд" -> Компоненты -> Нативные фильтры

![image](https://github.com/user-attachments/assets/545de520-9fb3-4e67-8760-e3b265780682)

Перенести фильтр на дашборд, в меню нативные фильтры, добавить элент на вкладку.

![image](https://github.com/user-attachments/assets/5bd5fc40-d83c-40f6-9693-ee74e92bf132)

Настраивается так же как и обычный фильтр на боковой панели

![image](https://github.com/user-attachments/assets/708b9c1d-f2f0-419c-abf2-29e4be75f8fe)

![image](https://github.com/user-attachments/assets/52ef8e5b-6d15-4e9a-8f3a-27260aa35ca9)

![image](https://github.com/user-attachments/assets/7d739e5a-c662-482b-baa7-eb918f3db877)

Если выбрать интервал, то видно изменение на графике:

![image](https://github.com/user-attachments/assets/d00a331b-2116-408c-ac7a-c17aca8d2fce)

В редактировании графика видно что ссылается так же как и при обычном боковом фильтре

![image](https://github.com/user-attachments/assets/a9e2784d-8b0e-446f-b2de-c0f59d925d68)

![image](https://github.com/user-attachments/assets/c7aae576-8b64-4f4b-ae80-cd224b504f7c)

















