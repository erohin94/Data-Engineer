# Типы даты/времени

```time``` - время суток (без даты)

```timestamp``` - дата и время

```interval``` - временной интервал

```date``` - дата (без времени суток)

Стандарт SQL требует, чтобы тип timestamp подразумевал timestamp without time zone (время без часового пояса), и PostgreSQL следует этому. Для краткости timestamp with time zone можно записать как timestamptz; это расширение PostgreSQL.

# EXTRACT извлечение даты и времени

Функция EXTRACT в PostgreSQL используется для извлечения различных компонентов даты и времени (например, года, месяца, дня, часа и т.д.) из значения типа timestamp, date, time и других типов данных.

```
-- Извлечение года из даты
SELECT EXTRACT(YEAR FROM '2025-01-24'::date) AS year;

 year
------
 2025
```

```
-- Извлечение месяца из timestamp
SELECT EXTRACT(MONTH FROM '2025-01-24 15:30:00'::timestamp) AS month;

 month
------
     1
```

```
-- Извлечение дня недели (цифровое представление)
SELECT EXTRACT(DOW FROM '2025-01-24'::date) AS day_of_week;

 day_of_week
-------------
           5
```

```
--Использование EXTRACT для извлечения продолжительности
SELECT EXTRACT(DAY FROM '2025-01-24'::date - '2025-01-01'::date) AS days_diff;

 days_diff
-----------
        23
```


# Текущие дата и время

Для получения только текущей даты:

```
SELECT CURRENT_DATE;
```
Для получения только текущего времени (без даты):

```
SELECT CURRENT_TIME;
```

Для получения текущей даты и времени (включая час, минуту и секунду):

```
SELECT NOW();
```

# DATE_TRUNC

В PostgreSQL функция date_trunc используется для округления временных значений (типов данных timestamp, timestamptz, date) до указанного интервала. Она удаляет часть времени, оставляя только данные с точностью до выбранного уровня. Например, можно округлить дату до месяца, года, часа и так далее.

```
DATE_TRUNC('interval', date_or_timestamp)

где:

'interval' — это строка, указывающая на уровень округления. Например, 'minute', 'hour', 'day', 'month', 'year'.

date_or_timestamp — это значение даты или временной метки, которое нужно округлить.
```

```
-- Округление до дня
SELECT date_trunc('day', '2025-01-24 14:45:30'::timestamp);
--------------
2025-01-24 00:00:00
```

```
-- Округление до месяца
SELECT date_trunc('month', '2025-01-24 14:45:30'::timestamp);
--------------
2025-01-01 00:00:00
```

# DATE_ADD

В PostgreSQL нет функции с именем DATE ADD, как, например, в MySQL, но аналогичный функционал можно выполнить с помощью оператора + или функции interval.

```
SELECT '2025-01-24'::date + 5;
------------------
2025-01-29
```

```
SELECT '2025-01-24'::date + INTERVAL '1 month';
-----------------
2025-02-24
```

# Получить текущий месяц

```SELECT EXTRACT(MONTH FROM CURRENT_DATE) AS current_month;```

или 

```SELECT DATE_PART('month', CURRENT_DATE) AS current_month;```

# Получить интервал времени

```
SELECT
  EXTRACT(epoch FROM ('2025-01-27 18:00:00'::timestamp - '2025-01-27 14:30:00'::timestamp)) / 3600 AS hours,
  (EXTRACT(epoch FROM ('2025-01-27 18:00:00'::timestamp - '2025-01-27 14:30:00'::timestamp)) / 60) % 60 AS minutes;

 hours | minutes
-------+---------
     3 |      30
```

