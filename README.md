# Data-Engineer (ETL project)

Инструкция по настройке Postgresql, Clickhouse, Superset. 

А так же пример извлечения данных из открытого API NASA в виде JSON.

Преобразовании этих данных в pandas dataframe и загрузке данных в БД postgre.

После чего можно сделать визуализацию в superset с необходиммыми показателями.

**Запуск и настройка Postgresql и Clickhouse**

1. Для начала создадим файл docker-compose.yml. С необходимыми настройками.

```
services:
  postgres:
    image: postgres:15
    restart: always
    container_name: postgres
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: 1
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
      

  clickhouse:
    image: yandex/clickhouse-server:latest
    restart: always
    container_name: clickhouse
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - ./clickhouse_data:/var/lib/clickhouse
      


volumes:
  postgres_data:
  clickhouse_data:
```

Этот файл как раз и позволит запустить 2 контейнера: один с PostgreSQL, а другой с ClickHouse.

2. Открыть Docker Desktop.

3. Открыть CMD терминал и перейти в папку с проектом где лежит docker-compose.yml.

4. Запустить Docker Compose
Для запуска используем команду в терминале CMD:

```
docker-compose up -d
```

![image](https://github.com/user-attachments/assets/9a359dbe-0907-4568-89b8-e362ad6139cd)

**Подключение к контейнеру PostgreSQL через терминал:**

Чтобы подключиться к PostgreSQL внутри контейнера, выполнить следующую команду:

`docker exec -it postgres psql -U test -d postgres`

![image](https://github.com/user-attachments/assets/9d0bce95-20e6-4899-bd15-5b36e9f77b38)

Теперь можно создавать таблицы, писать запросы прямо втерминале.

![image](https://github.com/user-attachments/assets/6e6c0baf-b529-4239-b8ea-d00d32fb0bb3)

Проверка созданной таблицы

```
\dt
```

Проверка структуры таблицы

```
\d launches
```

Чтобы выйти из сессии PostgreSQL, выполнить команду:

```
\q
```

**Подключение к БД с помощью python**

```
import psycopg2
from psycopg2 import sql

# Параметры подключения
dbname = 'postgres'
user = 'test'
password = '1'
host = 'localhost'  # Это может быть '127.0.0.1', если localhost не работает
port = '5432'

try:
    # Установить подключение
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    # Создать курсор
    cursor = connection.cursor()
    
    # Пример запроса (получение данных из таблицы users)
    cursor.execute("SELECT * FROM users;")
    
    # Получить все строки
    rows = cursor.fetchall()
    
    print("Таблица users:")
    for row in rows:
        print(f"id: {row[0]}, name: {row[1]}, email: {row[2]}")
    
    # Пример запроса (вставка новой записи)
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s);", ("David", "david@example.com"))
    connection.commit()  # Подтверждаем изменения
    
    print("Новая запись добавлена в таблицу users.")

    # Закрыть курсор
    cursor.close()
    
except Exception as e:
    print(f"Ошибка при подключении или выполнении запроса: {e}")
    
finally:
    # Закрыть соединение
    if connection:
        connection.close()
```

Выполнив код увидим что все работает.

![image](https://github.com/user-attachments/assets/5e118d18-0b34-4eb8-971d-25f870ff97b0)

Структура папок

![image](https://github.com/user-attachments/assets/5a3b8d40-8aab-4065-a894-38aa1659a85f)

**Дополнительные шаги (при необходимости):**

Проверка контейнера: Если нужно убедиться, что контейнер работает и слушает порт:

```
docker ps
```

Проверка логов контейнера: Если что-то пошло не так, можно просмотреть логи контейнера PostgreSQL:

```
docker logs postgres
```

**Подключение через DBeaver**

![image](https://github.com/user-attachments/assets/78d24903-bd61-4a67-82ac-a51d693641bb)

Увидим созданную ранее в контейнере БД postgre и тестовые данные которыми наполнили.

![image](https://github.com/user-attachments/assets/69a221a3-3e6b-4708-9bdb-ce976636ab68)

**Пример скрипта для подключения к БД и извлечения данных из открытого api nasa**

```
import requests
import pandas as pd
import json
from pandas import json_normalize
from sqlalchemy import create_engine
url = f"https://eonet.gsfc.nasa.gov/api/v3/events"

response = requests.get(url)
data = response.json()


df_geometry	 = pd.json_normalize(data['events'], record_path = 'geometry',
                       meta = ['id', 'title', 'description', 'link', 'closed'],
                       meta_prefix = 'events_',
                       errors='ignore')

df_sources	 = pd.json_normalize(data['events'], record_path = 'sources',
                       meta = ['id'],
                       meta_prefix = 'events_',
                       errors='ignore')

df_categories	 = pd.json_normalize(data['events'], record_path = 'categories',
                       meta = ['id'],
                       meta_prefix = 'events_',
                       errors='ignore')

merge_df = pd.merge(df_geometry, df_categories, on='events_id', how='left')

result = pd.merge(merge_df, df_sources, on='events_id', how='left')

result = result.rename(columns={'magnitudeValue': 'geometry_magnitudeValue', 
                                'magnitudeUnit': 'geometry_magnitudeUnit',
                                'date': 'geometry_date',
                                'type': 'geometry_type',
                                'coordinates': 'geometry_coordinates',
                                'id_x': 'categories_id', 
                                'title': 'categories_title',
                                'id_y': 'sources_id', 
                                'url': 'sources_url'})


# Параметры подключения
dbname = 'postgres' # Имя базы данных
user = 'test' # Имя пользователя
password = '1' # Пароль
host = 'localhost'  # Адрес хоста
port = '5432' # Порт (по умолчанию для PostgreSQL)

# Строка подключения для SQLAlchemy
connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(connection_string)

# Загрузка DataFrame в таблицу PostgreSQL
result.to_sql('eonet_nasa_api', engine, if_exists='replace', index=False)

# if_exists='replace' — если таблица существует, она будет заменена
# Если хотим добавлять данные без удаления таблицы, использовать if_exists='append'
```

Результат в DBeaver

![image](https://github.com/user-attachments/assets/59167769-4c5f-466a-af43-29e8bf7940f6)

![image](https://github.com/user-attachments/assets/89e23543-a8b7-4852-a66c-cf388d113adc)

# **Установка superset**

Создать папку, например superset на раб столе.

Открыть эту папку в cmd терминале.

Далее вводим команды в cmd.

Клонируем проект из github
`git clone https://github.com/apache/superset.git`
 
Переходим в директорию
`cd superset`

![image](https://github.com/user-attachments/assets/d931b628-bcb0-4731-b12e-8e542936ef1a)

Переключаемся на ветку релиза 2.1.0
`git checkout 2.1.0`
 
Проверяем статус (что переключились на правильный тег)
`git status`

Вводим команду чтобы открылся vscode `code .`

![image](https://github.com/user-attachments/assets/9fa38c3b-2d07-4c4c-bc5d-b8253353fb5f)

Открываем в vscode файл `docker-compose-non-dev.yml` меняем версию образа, который нужно использовать при развертывании. Делается это в 17 строке, вместо  `x-superset-image: &superset-image apache/superset:${TAG:-latest-dev}` пишем `x-superset-image: &superset-image apache/superset:2.1.0`

Открываем Docker Desctop

Запускаем установку (запустится скачивание образов с hub.docker.com). Вводим команду в cmd терминале `docker-compose -f docker-compose-non-dev.yml up`

По заверншении установки вводим в браузере `http://localhost:8088`

По умолчанию логин и пароль для входа: admin/admin.

Получаем superset

![image](https://github.com/user-attachments/assets/8fcab786-c7a9-4d72-a5b6-3b0d63619ec8)

Подключчаем развернутую в docker БД postgre к superset.

В HOST указываем host.docker.internal

Поскольку используем Superset в док-контейнере, не можем использовать ни 127.0.0.1, ни локальный хост, поскольку они разрешаются в контейнер, а не в хост.

![image](https://github.com/user-attachments/assets/2c6fa41d-b8a6-46ad-94b3-2bca7ca35cf8)

Если сделать запрос, видим что подключились к тестовой БД

![image](https://github.com/user-attachments/assets/8242190c-1fe7-419b-8b89-601019bce022)





