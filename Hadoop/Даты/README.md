`NOW()` — возвращает текущую дату и время

------------------------------------------------

`CURRENT_DATE()` — возвращает текущую дату

------------------------------------------------

`TRUNC(date_value, 'единица_времени')` — функция для усечения даты до определённого уровня точности, например: до начала дня, месяца, года и т.д.

| Параметр       | Значение `TRUNC(...)`  | Пример результата (если вход — `2025-05-27 14:35`) |
| -------------- | ---------------------- | -------------------------------------------------- |
| `'dd'` (день)  | Начало текущего дня    | `2025-05-27 00:00:00`                              |
| `'mm'` (месяц) | Начало текущего месяца | `2025-05-01 00:00:00`                              |
| `'yyyy'` (год) | Начало текущего года   | `2025-01-01 00:00:00`                              |

------------------------------------------------

`DATE_SUB(date, INTERVAL number unit)` - используется для вычитания интервала (дней, месяцев, лет и т.д.) из даты.

| Единица   | Назначение |
| --------- | ---------- |
| `SECOND`  | Секунды    |
| `MINUTE`  | Минуты     |
| `HOUR`    | Часы       |
| `DAY`     | Дни        |
| `MONTH`   | Месяцы     |
| `YEAR`    | Годы       |
| `WEEK`    | Недели     |
| `QUARTER` | Кварталы   |

```
SELECT DATE_SUB('2025-05-27', INTERVAL 10 DAY);
-- Результат: '2025-05-17'
```

------------------------------------------------

`LAST_DAY(date)` - возвращает последний день месяца для указанной даты.

```
SELECT LAST_DAY('2025-05-10');
-- Результат: '2025-05-31'
```

------------------------------------------------

`DATE_ADD(date, INTERVAL number unit)` - используется для прибавления интервала (дней, месяцев, лет и т.д.) к дате.

| Единица   | Значение |
| --------- | -------- |
| `SECOND`  | Секунды  |
| `MINUTE`  | Минуты   |
| `HOUR`    | Часы     |
| `DAY`     | Дни      |
| `MONTH`   | Месяцы   |
| `YEAR`    | Годы     |
| `WEEK`    | Недели   |
| `QUARTER` | Кварталы |

```
SELECT DATE_ADD('2025-05-27', INTERVAL 2 MONTH);
-- Результат: '2025-07-27'
```

**Примеры**

Сегодня `SELECT NOW()`

![image](https://github.com/user-attachments/assets/69195f25-db0c-434b-a7eb-9727c3aa41dc)

```
SELECT LAST_DAY(DATE_SUB(TRUNC(NOW(), 'mm'), 1)) --Возвращает последний день месяца для указанной даты
```
![image](https://github.com/user-attachments/assets/73ed2308-8792-4f59-b3b2-bc74f5f8221e)

```
SELECT DATE_SUB(TRUNC(DATE_ADD(TRUNC(NOW(), 'mm'), INTERVAL 0 MONTH), 'mm'), 150)
```
![image](https://github.com/user-attachments/assets/40af4aa8-9296-460a-8bb1-a647810a75cb)

```
SELECT TRUNC(NOW(), 'dd') --Округление до дня
```
![image](https://github.com/user-attachments/assets/ff819622-b148-4dda-b940-d38b2d47b9c1)

```
SELECT DATE_ADD(TRUNC(NOW(), 'dd'), INTERVAL 1 MONTH) -- Добавляет интервал 1 месяцев к сегодня
```
![image](https://github.com/user-attachments/assets/c00a915e-19f3-4735-9ca9-e0d995c95898)

```
SELECT TRUNC(DATE_ADD(TRUNC(NOW(), 'dd'), INTERVAL 1 MONTH), 'mm') --Округление до дня, добавление интервала 1 месяцев, округления до начала месяца
```
![image](https://github.com/user-attachments/assets/8d9c21ce-7931-43ee-ab96-80d3ef0a714a)

```
SELECT DATE_SUB(TRUNC(DATE_ADD(TRUNC(NOW(), 'mm'), INTERVAL 1 MONTH), 'mm'), 150) --Округление до месяца, добавление интервала 1 месяцев, округления до начала месяца, начало месяца минус 150 дней
```
![image](https://github.com/user-attachments/assets/6822b7f4-a0fd-40d5-9ced-d48bf18447c2)

```
SELECT DATE_SUB(TRUNC(NOW(), 'dd'), 150) --Разница, сегодня (от 00:00:00 часов) минус 150 дней
```
![image](https://github.com/user-attachments/assets/2a059793-301e-4c1f-8ca0-b880d413970c)
