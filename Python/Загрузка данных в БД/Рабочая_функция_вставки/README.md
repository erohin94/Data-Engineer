# **Тестовый скрипт для загрузки данных в БД postgreSQL**

Скрипт для загрузки данных в postgreSQL. Данные получены из HH API в виде JSON и сохранены в `.csv` файл в исходном виде и распарсенном.

В файле `main_test.py` вызываются все основные функции.

В файле `create_table.py` запросы для создания таблиц, которые вызываются в `main_test.py` циклом.

В файле `insert_in_postgresql.py` две функции для выполнения запросов `sql_query_execute()` и вставки данных в БД `insert_into_hadoop()`.

После запуска в БД появляются две таблицы

![image](https://github.com/user-attachments/assets/af58896a-3dbb-48d0-9f7c-6007c978a2f6)

**Заметки:**

Важно при загрузке соблюдать типы колонок в БД и типы колонок в датафрейме который грузим, иначе будут ошибки.

Соблюдать экранирование символов, разные БД ведут себя по разному.

Привести значения в DataFrame к стандартным типам Python. Перед тем как передавать данные в `execute_values`, нужно преобразовать все значения в стандартные типы Python, такие как `int`, `float`, `str`, `datetime`, которые поддерживаются psycopg2. 

Когда создаёшь DataFrame, pandas под капотом использует `NumPy` для хранения данных. И чтобы эффективно обрабатывать большие массивы чисел, он применяет типы вроде `np.float64`, `np.int64`, `np.object_` и т.п. — это просто NumPy-аналог стандартных типов Python (`float`, `int` и т.д.), но с большей производительностью и поддержкой векторных операций.

Некоторые библиотеки для работы с базами данных (например, `sqlite3`, `psycopg2`, `sqlalchemy`) не всегда автоматически приводят `np.float64` к стандартному `float`, и возникает ошибка.

Сделал с помощью `df = df.astype(object)` перед тем как добавлять данные в БД.

Дата фрейм надо привести к виду, тоесть достать колонки и строки со значениями:

```
INSERT INTO users (id, name, email) VALUES (2, 'Пётр Смирнов', 'petr@example.com'), (3, 'Ольга Соколова', 'olga@example.com');
```

**SQL запросы**

```
DROP TABLE IF EXISTS sbxm_hr.rda_hh_application_resume_erohin

DROP TABLE IF EXISTS sbxm_hr.rda_hh_full_resume_erohin

select * from sbxm_hr.rda_hh_application_resume_erohin 

select * from sbxm_hr.rda_hh_full_resume_erohin
```



