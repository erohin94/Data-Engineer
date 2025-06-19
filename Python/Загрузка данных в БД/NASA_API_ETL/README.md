## Пример Data-Engineer (ETL project)

Пример извлечения данных из открытого API NASA в виде JSON.

Преобразовании этих данных в pandas dataframe и загрузке данных в БД postgre.

После чего можно сделать визуализацию в superset с необходиммыми показателями.

## Пример скрипта для подключения к БД и извлечения данных из открытого api nasa

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
