## Что такое DuckDB?

**DuckDB** — встраиваемая аналитическая база данных, которую подключают как обычную Python-библиотеку.
Работает в процессе Python (без отдельного сервера).

**1) In-memory база (в памяти)**

```
import duckdb
con = duckdb.connect()
```

Создаёт временную базу в RAM. Не сохраняется на диск — все данные исчезают после `con.close()`. Отлично для временных вычислений и ETL промежуточных таблиц.

**2) Файловая база (на диске)**

`con = duckdb.connect("my_data.duckdb")`

Создаёт или открывает файл `my_data.duckdb`. Все таблицы сохраняются между сессиями. Можно открыть файл в DBeaver или другой SQL IDE.

Пример:

```
import duckdb

# подключаемся к файлу базы
con = duckdb.connect("my_data.duckdb")

# создаём таблицу
con.execute("CREATE TABLE test AS SELECT 1 AS id, 'abc' AS name")

# читаем таблицу в pandas DataFrame
df = con.execute("SELECT * FROM test").df()
print(df)

con.close()
```

Если выполнить этот код, результат будет такой:

```
id name
1  abc
``

Это DataFrame из одной строки и двух колонок, которую мы создали в таблице `test`.

После закрытия соединения (`con.close()`) файл `my_data.duckdb` сохраняет эту таблицу на диск, и её можно открыть снова в другой сессии или в DBeaver.
