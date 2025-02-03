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
