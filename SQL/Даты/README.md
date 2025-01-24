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
# DATE_ADD



