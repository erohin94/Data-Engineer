**`AnalysisException: Could not resolve column/field reference: 'curent_date'`**

Ошибка, которая возникает при выполнении запроса в Impala и выглядит так: `«AnalysisException:` Не удалось разрешить ссылку на столбец/поле: `current_date`.

Причина ошибки — несовместимость функции `«Current_Date»` с работой Impala. 

Решение: вместо `«Current_Date»` можно использовать `«now()»` или `«current_timestamp()»` или `«Current_Date()»` - указал скобки в python скрипте при выполнени запроса.


**`Hiveserver2Error: ParseException: Syntax error ... Encountered: DATETIME`** 

Ошибка возникает при загрузке датафрейма в БД hadoop. В датафрейме в столбце `df['standart_time_load']` строка в виде `06:30:00`.

Hive не понимает тип datetime.time (в отличие от pandas или Python), потому что Hive поддерживает свои типы данных 

`DATE (yyyy-MM-dd)` 

`TIMESTAMP (yyyy-MM-dd HH:mm:ss)`

и datetime.time — не подходит.

Если надо сохранять 06:30:00 как время, без даты — нужно: 

-либо сохранять это как строку (STRING)

-либо привести к TIMESTAMP, добавив фиктивную дату (например, 1970-01-01 06:30:00)

Решение: в DataFrame колонку со значениями типа datetime.time (например, "06:30:00"), перед загрузкой в Hive нужно привести к строковому формату.

`df['standart_time_load'] = df['standart_time_load'].astype(str)`

![image](https://github.com/user-attachments/assets/c3bf5972-aa8a-4168-b3a8-c0d487554b13)

![image](https://github.com/user-attachments/assets/96d4639a-9fcd-407f-8cdc-9a648d59db16)

Пример данных 

![image](https://github.com/user-attachments/assets/ac82e1dd-fe65-49e9-9f51-8add192fdd33)

