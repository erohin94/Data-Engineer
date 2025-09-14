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
SELECT LENGTH('Было интересно и информативно!!!')
```

<img width="411" height="200" alt="image" src="https://github.com/user-attachments/assets/8d83cb00-4eb0-41f9-b091-705eddd621bb" />

