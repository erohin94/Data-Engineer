import requests
import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
from datetime import datetime

# Функция для загрузки файла в MinIO
def upload_to_minio():
    s3 = boto3.client('s3', 
                      endpoint_url='http://host.docker.internal:9000',  # Адрес MinIO
                      aws_access_key_id='ANV9JuSM47gsMx8BtBqf', 
                      aws_secret_access_key='Y3O0qw1fV3cP1dzDXIDASAUx2vnaRFm28lDr3RYs', 
                      region_name='us-east-1')

    try:
        # Загрузка CSV-файла
        url = 'https://data.cityofnewyork.us/resource/kxp8-n2sj.csv'
        response = requests.get(url)
        response.raise_for_status()  # Проверка запроса

        # Загрузка файла в MinIO
        file_content = response.content  # Получаем бинарные данные файла
        file_key = 'nyc_taxi_data.csv'  # Уникальное имя для файла в MinIO
        
        # Загружаем данные в MinIO
        s3.put_object(Bucket='nyc-yellow-taxi-raw-data', # Название бакета в MinIO
                      Key=file_key, 
                      Body=file_content)

        print(f"Файл {file_key} успешно загружен в бакет MinIO.")
    
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при скачивании файла: {e}")
    except (NoCredentialsError, EndpointConnectionError) as e:
        print(f"Ошибка при загрузке в MinIO: {e}")


# Определение дефолтных параметров DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 24),
    'retries': 1,
}

dag = DAG(
    'upload_file_to_minio_with_http_check',
    default_args=default_args,
    description='DAG для проверки и загрузки CSV-файла в MinIO',
    schedule_interval=None,  # Можно настроить на регулярный запуск
    catchup=False,
)

# Задача 1: Использование SimpleHttpOperator для проверки наличия файла
check_file_task = SimpleHttpOperator(
    task_id='check_file_exists_task',
    method='GET',  # Используем метод для проверки доступности ресурса
    http_conn_id='nyc_yellow_taxi_id',  # Настроить в UI Airflow Admin-Connections поле Connection id
    endpoint='/resource/kxp8-n2sj.csv',  # Путь файла
    headers={"Accept": "application/json"},  # Заголовки запроса
    response_check=lambda response: response.status_code == 200,  # Проверка ответа
    dag=dag,
)

# Задача 2: Загрузка файла в MinIO (если файл доступен)
upload_task = PythonOperator(
    task_id='upload_to_minio_task',
    python_callable=upload_to_minio,
    dag=dag,
)

# Зависимости: сначала проверяем файл, затем загружаем его в MinIO
check_file_task >> upload_task
