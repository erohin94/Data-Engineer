# Установка MINIO

Бесплатная с открытым исходным кодом система. Это распределенное файловое хранилище. Можно установить на компьютер. Полностью совместима с Amazon S3.

[Ссылка на скачивание](https://min.io/open-source/download?platform=windows) 

[Дока с установкой](https://min.io/docs/minio/windows/index.html)

Чтобы запустить minio необходимо выполнить инструкции:

![image](https://github.com/user-attachments/assets/35c0b57b-4dd7-4f76-b995-f9b170730326)

1. Создаем папку ```mkdir fs```:

![image](https://github.com/user-attachments/assets/5210efad-e85c-4c84-9fa6-abb077593ef9)

Эта папка будет выступать файловой системой для сервиса minio

2. Установить сервер MinIO

Загрузите исполняемый файл MinIO по следующему [URL-адресу](https://dl.min.io/server/minio/release/windows-amd64/minio.exe).

Сохранить в папку fs:

![image](https://github.com/user-attachments/assets/9d20c722-d0aa-48c8-a7bb-a2acb3b0b8cf)


Следующий шаг включает инструкции по запуску исполняемого файла. 

Вы не можете запустить исполняемый файл из Проводника или двойным щелчком по файлу. Вместо этого вы вызываете исполняемый файл для запуска сервера.

3. Запустите minio server

В PowerShell или командной строке перейдите к местоположению исполняемого файла или добавьте путь к ```minio.exe``` файлу в систему ```$PATH```.

Используйте эту команду для запуска локального экземпляра MinIO в ```C:\minio``` папке. Вы можете заменить ```C:\minio``` на другой диск или путь к папке на локальном компьютере.

![image](https://github.com/user-attachments/assets/78cd3343-0935-41a1-a5a7-b00783d4b025)

```minio.exe server C:\Users\erohi\Desktop\fs --console-address ":9001"```

Процесс выводит свой вывод на системную консоль, примерно так:minio server

![image](https://github.com/user-attachments/assets/c9a8ad9a-e696-4cc8-bcf8-27fa47a7c8a2)

Процесс привязан к текущему окну PowerShell или командной строки. Закрытие окна останавливает сервер и завершает процесс.

4. Подключите ваш браузер к серверу MinIO

Чтобы получить доступ к консоли MinIO, зайдите в браузер (например, Microsoft Edge) и перейдите по адресу http://127.0.0.1:9001 или одному из адресов консоли, указанных в выводе команды. Например, в примере вывода указаны два возможных адреса для подключения к консоли.minio serverConsole: http://192.0.2.10:9001 http://127.0.0.1:9001

Пока порт 9000 используется для подключения к API, MinIO автоматически перенаправляет доступ браузера к консоли MinIO.

Войдите в консоль с учетными данными пользователя RootUserи RootPass, отображаемыми в выводе. По умолчанию они равны .minioadmin | minioadmin

![image](https://github.com/user-attachments/assets/cf841deb-dd85-4a0a-a1d1-f14e62d950bc)

По итогу получаем

![image](https://github.com/user-attachments/assets/a450783e-a9bd-4e85-8ab8-89419ea4f829)

**Тест**

Попробуем загрузить что нибудь.

Создаем бакет

![image](https://github.com/user-attachments/assets/e3a7459e-d8a6-4d0f-8599-95ca3adc4fb2)

![image](https://github.com/user-attachments/assets/3491654a-350d-4eab-aaed-62db82fc3f6d)

![image](https://github.com/user-attachments/assets/e4639fa8-552c-4b65-8c06-424cbdf741d3)

Бакета сделали два, один для сырых данных, второй для данных в формате parquet.

И тестовый для проверки работоспособности

![image](https://github.com/user-attachments/assets/c713a632-4d82-4ee5-be04-88afde36d05e)

Кликаем на бакет и нажимаем иконку Browse Bucket

![image](https://github.com/user-attachments/assets/e392ecfa-cbe7-4e94-b745-52eca3a97942)

![image](https://github.com/user-attachments/assets/84aa32d8-083c-40b9-8338-868249af9dd6)

И загружаем лого Airflow

![image](https://github.com/user-attachments/assets/fa9cced5-6f32-4f66-b9cf-d3f1b111e86c)

Убедимся что все работает и загружено. Открываем новый терминал.

Переходим в директорию

![image](https://github.com/user-attachments/assets/95173b47-948b-4392-b41f-349b2bcb681a)

Вводим команды и видим 

![image](https://github.com/user-attachments/assets/30d4968d-1f81-4d88-b6dd-b9643d31d67e)

# Тест подключения к MINIO

Создадим тестовый файл test.py

![image](https://github.com/user-attachments/assets/a43a9553-28a9-4fef-8dd9-9a39d63c2e54)

Установить библиотеку ```pip install boto3``` 

В test.py прописать код

```
import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError

# Подключение через boto3 к MinIO
s3 = boto3.client('s3', 
                  endpoint_url='http://127.0.0.1:9000',  # Адрес MinIO. Был порт 9001, падал в ошибку. Заменил на 9000
                  aws_access_key_id='minioadmin', 
                  aws_secret_access_key='minioadmin', 
                  region_name='us-east-1')

try:
    # Попробуем получить список бакетов
    response = s3.list_buckets()
    print("Buckets:", response['Buckets'])
except (NoCredentialsError, EndpointConnectionError) as e:
    print(f"Error: {e}")
```
Получу следующее

![image](https://github.com/user-attachments/assets/8f453234-d4a0-4e87-825d-a8514c0cedbe)

*Тест 2*

Создать текстовый файл и попробовать загрузить в MINIO
```
import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError

# Подключение через boto3 к MinIO
s3 = boto3.client('s3', 
                  endpoint_url='http://127.0.0.1:9000',  # Адрес MinIO
                  aws_access_key_id='minioadmin', 
                  aws_secret_access_key='minioadmin', 
                  region_name='us-east-1')

try:
    # Открыть файл
    file_path = "C:/Users/erohi/Desktop/airflow_project_ny_taxi/test.txt"  # Путь
    with open(file_path, 'rb') as file:
        response = s3.put_object(Bucket='nyc-yellow-taxi-raw-data', 
                                 Key='example.txt', 
                                 Body=file)
    
    print(f"Файл {file_path} успешно загружен в бакет.")
    
except (NoCredentialsError, EndpointConnectionError) as e:
    print(f"Ошибка: {e}")
```

Увижу 

![image](https://github.com/user-attachments/assets/e7dbbafb-0768-4791-9131-ae5e367bbc5f)

В MINIO если зайти в бакеты то будет видно загруженый файл

![image](https://github.com/user-attachments/assets/fa3752fe-4a24-4b4e-afaf-e6cbf1334dff)
