**AnalysisException: Could not resolve column/field reference: 'curent_date'**

Ошибка, которая возникает при выполнении запроса в Impala и выглядит так: «AnalysisException: Не удалось разрешить ссылку на столбец/поле: „current_date“».

Причина ошибки — несовместимость функции «Current_Date» с работой Impala. 

Решение: вместо «Current_Date» можно использовать «now()» или «current_timestamp()» или «Current_Date()» - указал скобки в python скрипте при выполнени запроса.
