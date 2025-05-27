**Проверка, что в столбце числа**

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
