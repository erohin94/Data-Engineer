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
