import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError

# Подключение через boto3 к MinIO
s3 = boto3.client('s3', 
                  endpoint_url='http://127.0.0.1:9000',  # Адрес MinIO
                  aws_access_key_id='minioadmin', 
                  aws_secret_access_key='minioadmin', 
                  region_name='us-east-1')

try:
    # Открытие файла на локальном диске и загрузка в MinIO
    file_path = "C:/Users/erohi/Desktop/airflow_project_ny_taxi/test.txt"  # Путь к файлу на вашем компьютере
    with open(file_path, 'rb') as file:
        response = s3.put_object(Bucket='nyc-yellow-taxi-raw-data', 
                                 Key='example.txt', 
                                 Body=file)
    
    print(f"Файл {file_path} успешно загружен в бакет.")
    
except (NoCredentialsError, EndpointConnectionError) as e:
    print(f"Ошибка: {e}")
