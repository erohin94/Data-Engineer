# **В postgresql**

Предположим есть датафрейм

```
import pandas as pd

resumes_id_list_all = [['aaa111', 111111, 'test1', 'test_11', 10011, 'active', 'data'],  
                       ['aaa222', 22222, 'test2', 'test_22', 10012, 'active', 'data2']]

df_resumes_list = pd.DataFrame(resumes_id_list_all, columns=['resume_id', 'owner_id', 'url', 'url_w_contacts', 'vacancy_code', 'search_status', 't_changed_dttm']).drop_duplicates()
```

![image](https://github.com/user-attachments/assets/6d9a74e0-9b2a-4427-b8a5-975ca8e1ff52)

```
#Получаем список кортежей
#Кортеж (tuple) — неизменяемый тип данных. my_tuple = (1, 2, 3)
#Множество (set) — изменяемый тип данных. my_set = {1, 2, 3}

df = df_resumes_list
tuples = list(set([tuple(x) for x in df.to_numpy()]))
tuples

-----------------------------------------------
[('aaa222', 22222, 'test2', 'test_22', 10012, 'active', 'data2'),
 ('aaa111', 111111, 'test1', 'test_11', 10011, 'active', 'data')]
```

