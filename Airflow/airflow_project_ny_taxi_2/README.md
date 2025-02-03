# Описание проекта
В этом репозитории немного изменю проект который делал [тут](https://github.com/erohin94/Data-Engineer/tree/main/Airflow/airflow_project_ny_taxi) поэтому установку всех зависимостей, 
настройку подключений и тд беру из первого проекта. 

Проект представляет собой систему на базе Apache Airflow, которая выполняет несколько задач обработки данных, включая загрузку файлов с веб-ресурса, их сжатие в формат GZIP и загрузку в хранилище S3, а затем преобразование этих данных в формат Parquet.

Проект будет модифицирован следующим образом:

*1.Загрузка файла с веб-ресурса и сжатие в GZIP:*

Используется оператор ```PythonOperator``` для загрузки файла с веб-сайта. Загруженный файл будет сохраняться в сжатом формате GZIP. Для реализации сжатия файла используется библиотека gzip.

*2.Функция загрузки:*

Так как ```PythonOperator``` принимает объект типа callable, который будет выполнен, функция для загрузки файла будет вынесена в отдельный модуль ```functions.py```, что улучшит структуру проекта и обеспечит повторное использование кода. В этой функции будет происходить скачивание файла с веб-ресурса, его сжатие в GZIP и загрузка в S3. Функция будет возвращать путь до S3-объекта, который будет использован в следующем операторе для дальнейшей обработки.

*3.Трансформация в формат Parquet:*

После того как файл будет загружен в S3, следующий оператор PythonOperator скачает сжатый GZIP файл с S3. Этот файл будет преобразован в формат Parquet с помощью библиотеки pandas и pyarrow.
Результат (Parquet файл) будет сохранен обратно в S3.

**Структура проекта**

Проект будет состоять из нескольких файлов:

*DAG файл (например, airflow_dag.py):*

Здесь будет прописана основная логика для Airflow: задачи, зависимости между ними, а также настройка DAG.

*Модуль функций (functions.py):*

В нем будет находиться основная логика для загрузки файла, сжатия в GZIP и загрузки на S3, а также преобразования файла в формат Parquet.

# Про формат Parquet

Хранение данных в открытом текстовом формате, таком как CSV, может быть неэффективным по нескольким причинам.

*1. Высокие затраты на хранение:*

Открытые текстовые файлы, такие как CSV, занимают много места на диске, особенно если данные включают большое количество строк и столбцов.
В хранилищах данных, таких как Amazon S3, стоимость хранения зависит от объема данных. Чем больше размер файла, тем дороже его хранение.

*2. Неэффективность при чтении и передаче:*

В открытых текстовых файлах данные представлены построчно, что означает, что чтобы извлечь данные из одной колонки, вам нужно прочитать весь файл целиком.
Это также увеличивает время передачи данных по сети. Например, если вы хотите получить информацию из одного столбца, вам все равно нужно будет загружать весь файл, даже если вам не нужны другие столбцы.
Чтобы решить эти проблемы, используются эффективные форматы для хранения и обработки данных, такие как Apache Parquet.

**Что такое Parquet?**

Apache Parquet — это бинарный формат для хранения данных, который использует колоночное хранение. Это означает, что данные в файле Parquet хранятся по колонкам, а не по строкам, как в обычных CSV или текстовых файлах.

*Почему Parquet эффективен?*

Компрессия данных:

Parquet использует сжатие данных. Формат поддерживает несколько алгоритмов сжатия, таких как gzip, snappy, lzo и другие, что позволяет значительно уменьшить объем файлов по сравнению с текстовыми файлами.
Благодаря колоночному хранению данные могут быть сжаты более эффективно, особенно если колонки содержат повторяющиеся или однотипные значения.

Эффективное чтение данных:

При колоночном хранении данных, при запросах к файлам, часто требуется прочитать только некоторые колонки, а не весь файл. Это ускоряет время работы с данными.
Например, если ваш запрос требует только информации из нескольких столбцов, то в случае с Parquet будет достаточно прочитать только те колонки, которые нужны, а не загружать весь файл целиком.
Это значительно уменьшает время выполнения запросов, особенно когда работа идет с большими объемами данных.

*Как устроен формат Parquet?*

Можно представить Parquet как нечто похожее на файловую систему с несколькими уровнями:

Данные хранятся по колонкам. Каждая колонка записана в отдельном блоке данных, и для каждой колонки хранится метаинформация о типах данных и расположении значений.

В Parquet также есть метаданные, которые содержат информацию о структуре данных, типах столбцов и их расположении. Эти метаданные помогают быстрее обрабатывать данные, так как можно сразу понять, какие колонки в файле содержат нужную информацию.

Файлы Parquet не хранят все данные подряд (как это делает обычный текстовый файл), а используют более эффективные способы хранения и индексирования, что снижает затраты на поиск нужных данных.

Если не вдаваться в детали реализации Parquet, а попробовать объяснить представление данных внутри максимально просто, то Parquet выглядит как небольшая файловая система, где значения каждой колонки лежат в отдельных файлах, а также присутствует дополнительный файл с метаданными, где хранится информация о типах колонок и их расположении. То есть чтобы получить значения заданных колонок нужно прочитать только файлы, содержащие данные этих колонок (а не всё целиком).

**Преимущества использования Parquet**

*Меньше пространства для хранения:*

Паркетные файлы занимают гораздо меньше места на диске, чем текстовые файлы, за счет сжатия данных и эффективного представления информации.

*Быстрее выполняются аналитические запросы:*

Поскольку вы можете читать только нужные колонки, работа с большими объемами данных становится значительно быстрее.
Например, при использовании Parquet с инструментами аналитики, такими как Apache Spark, AWS Athena или Presto, запросы могут выполняться быстрее, чем при работе с CSV или текстовыми файлами.

*Совместимость с инструментами Big Data:*

Parquet является стандартом для хранения данных в экосистемах Big Data, таких как Apache Hive, Apache Spark, Apache Drill, AWS Glue и других.
Он идеально подходит для аналитических и машинных приложений, где необходимо работать с огромными объемами данных.

**Пример использования:**

Предположим, у вас есть большой CSV-файл с данными о такси в Нью-Йорке. Если этот файл будет сохранен в формате CSV, то его будет тяжело обрабатывать, особенно если вам нужно выполнить запросы, которые используют только одну или несколько колонок, например, только дату или количество поездок.

Если же этот файл преобразовать в Parquet, запросы, например, для поиска всех поездок по определенной дате, будут выполняться гораздо быстрее. Почему? Потому что вам не нужно читать все данные, вы будете читать только данные для нужной колонки (например, для даты), что существенно экономит время и ресурсы.

**Заключение**

Apache Parquet — это мощный и эффективный формат для хранения и обработки данных, который позволяет сжать данные, ускорить выполнение аналитических запросов и снизить затраты на хранение. Он идеально подходит для работы с большими объемами табличных данных и активно используется в аналитических платформах и Big Data экосистемах.

# Код

**functions.py**
```
import requests
import gzip
import io
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

def download_and_compress_file(url):
    """
    Загружает CSV-файл и сжимает его в формат gzip.
    """
    response = requests.get(url)
    response.raise_for_status()  # Проверка запроса

    # Сжимаем файл в gzip
    compressed_file = io.BytesIO()
    with gzip.GzipFile(fileobj=compressed_file, mode='wb') as f:
        f.write(response.content)
    
    compressed_file.seek(0)
    return compressed_file

def convert_gzip_to_parquet(compressed_file):
    """
    Преобразует GZIP сжатый файл в формат Parquet.
    compressed_file — это объект BytesIO, содержащий сжатые данные.
    """
    # Шаг 1: Чтение CSV из сжатого GZIP файла
    with gzip.GzipFile(fileobj=compressed_file, mode='rb') as f:
        df = pd.read_csv(f)

    # Шаг 2: Преобразуем DataFrame в формат Parquet
    parquet_buffer = io.BytesIO()  # Буфер для сохранения Parquet в памяти

    # Преобразуем Pandas DataFrame в формат Parquet с использованием pyarrow
    table = pa.Table.from_pandas(df)  # Преобразуем DataFrame в Table
    pq.write_table(table, parquet_buffer)  # Записываем в буфер в формате Parquet

    parquet_buffer.seek(0)  # Перемещаем указатель в начало буфера для дальнейшего использования

    return parquet_buffer

def upload_to_minio(aws_conn_id, bucket_name, file_key, file_content):
    """
    Загружает файл в указанный бакет в MinIO.
    """
    aws_hook = S3Hook(aws_conn_id=aws_conn_id)  # Получаем подключение через S3Hook
    s3_client = aws_hook.get_conn()  # Получаем клиента boto3 для работы с S3 через Airflow

    try:
        # Загружаем данные в MinIO
        s3_client.put_object(Bucket=bucket_name, Key=file_key, Body=file_content)
        print(f"Файл {file_key} успешно загружен в бакет {bucket_name}.")
    except Exception as e:
        print(f"Ошибка при загрузке в MinIO: {e}")
```

**DAG**

![image](https://github.com/user-attachments/assets/6a4a0292-f842-4852-b202-7c0b1d51104c)

```
from datetime import datetime
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from functions import download_and_compress_file, convert_gzip_to_parquet, upload_to_minio

# Определение дефолтных параметров DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 24),
    'retries': 1,
}

dag = DAG(
    'upload_compressed_and_parquet_file_to_minio',
    default_args=default_args,
    description='DAG для проверки и загрузки сжатого CSV и Parquet файлов в MinIO',
    schedule_interval=None,  # Можно настроить на регулярный запуск
    catchup=False,
)

# Задача 1: Использование SimpleHttpOperator для проверки наличия файла
check_file_task = SimpleHttpOperator(
    task_id='check_file_exists_task',
    method='GET',
    http_conn_id='nyc_yellow_taxi_id',  # Настроить в UI Airflow Admin-Connections поле Connection id
    endpoint='/resource/kxp8-n2sj.csv',
    headers={"Accept": "application/json"},
    response_check=lambda response: response.status_code == 200,  # Проверка ответа
    dag=dag,
)

# Задача 2: Загрузка GZIP файла в MinIO
def upload_gzip_task_function(**kwargs):
    url = 'https://data.cityofnewyork.us/resource/kxp8-n2sj.csv'
    
    # Скачиваем и сжимаем файл
    compressed_file = download_and_compress_file(url)
    
    # Загружаем сжатый файл в бакет nyc-yellow-taxi-raw-data
    upload_to_minio(
        aws_conn_id='aws_connection',
        bucket_name='nyc-yellow-taxi-raw-data',
        file_key='nyc_taxi_data.csv.gz',
        file_content=compressed_file
    )

upload_gzip_task = PythonOperator(
    task_id='upload_gzip_to_minio_task',
    python_callable=upload_gzip_task_function,
    provide_context=True,  # Передаем контекст в функцию (необходимо для использования kwargs)
    dag=dag,
)

# Задача 3: Загрузка Parquet файла в MinIO
def upload_parquet_task_function(**kwargs):
    url = 'https://data.cityofnewyork.us/resource/kxp8-n2sj.csv'
    
    # Скачиваем и сжимаем файл
    compressed_file = download_and_compress_file(url)
    
    # Преобразуем сжатый файл в формат Parquet
    parquet_file = convert_gzip_to_parquet(compressed_file)
    
    # Загружаем Parquet файл в бакет nyc-yellow-taxi-parquet-data
    upload_to_minio(
        aws_conn_id='aws_connection',
        bucket_name='nyc-yellow-taxi-parquet-data',
        file_key='nyc_taxi_data.parquet',
        file_content=parquet_file
    )

upload_parquet_task = PythonOperator(
    task_id='upload_parquet_to_minio_task',
    python_callable=upload_parquet_task_function,
    provide_context=True,  # Передаем контекст в функцию (необходимо для использования kwargs)
    dag=dag,
)

# Зависимости: сначала проверяем файл, затем загружаем его в два разных бакета
check_file_task >> [upload_gzip_task, upload_parquet_task]
```

Увидим в MINIO

![image](https://github.com/user-attachments/assets/9663a29a-0e89-4ede-bda5-0276803d0ce1)

![image](https://github.com/user-attachments/assets/79778a4b-474b-4554-965b-6fd6deafc229)

![image](https://github.com/user-attachments/assets/d0ce0834-ad71-4558-a278-a74f2222e6d9)




