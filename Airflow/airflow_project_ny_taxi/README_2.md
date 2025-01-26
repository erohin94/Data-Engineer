# New York taxi data pipline

[Инстукция](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/README.md) по установке Airflow

Создать структуру папок

![image](https://github.com/user-attachments/assets/6ec7a984-41a1-463d-8f0a-d8bd2a305db3)

Открыть docker desktop и в терминале ввести команды:

```cd Desktop\airflow_project_ny_taxi``` - перейти в папку с проектом

```docker-compose up airflow-init``` - инициализация Airflow

```docker-compose up -d``` - запуск Airflow

Чтобы увидеть интерфейс Airflow открыть браузер и перейдите по адресу http://127.0.0.1:8080/

Ввести airflow два раза

Использую датасет, содержащий поездки на такси по городу Нью-Йорк. Данные открыто лежат на [сайте](https://opendata.cityofnewyork.us/).

В качестве хранилища можно использовать AWS S3. Это популярный сервис для хранения файлов от компании Amazon, также S3 можно рассматривать как распределенную файловую систему. Чтобы не платить, есть альтернатива, которую можно развернуть у себя на компьютере. Сервис [Minio](https://min.io/) полностью совместимый с S3 файловый сервер, поэтому Apache Airflow будет работать с ним как с AWS S3.

**Структура пайплайна**

Пайплайн (DAG) будет состоять из следующих операторов:

```- SimpleHttpOperator``` - для проверки существования файла на сервере перед его загрузкой

```- PythonOperator``` - загрузка файла с сайта и перекладывание на S3 в виде csv

Вот как выглядит это на диаграмме с зависимостями:

![image](https://github.com/user-attachments/assets/d8fe0e62-8805-4fbf-8cef-be894c78d8cc)

Выполнение последующего шага зависит от успешности предыдущего. 

Если необходимого файла на сервере нет (check_file_task), то выполнение загрузки нецелесообразно (upload_task), за этим строго следит Airflow.

# Установка S3Hook

Для подключения к S3 надо импортировать класс S3Hook

```from airflow.providers.amazon.aws.hooks.s3 import S3Hook```

S3Hook — это класс, который используется для взаимодействия с Amazon S3 (облачное хранилище данных от Amazon). С помощью S3Hook можно загружать файлы в S3, скачивать их, проверять наличие объектов и другие операции с данными в облаке.

S3Hook упрощает работу с S3 в контексте задач в Airflow.

Так как Airflow работает в контейнерах Docker, нужно будет установить необходимую библиотеку внутри Docker-контейнера, используемого для проекта. Для этого есть несколько вариантов. 

Буду устанавливать через ```.env``` файл:

У меня сейчас в ```docker-compose.yaml``` файле следующее 

![image](https://github.com/user-attachments/assets/f3307d37-115d-402d-855f-1f4491c75432)

Это означает, что переменная ```_PIP_ADDITIONAL_REQUIREMENTS``` может быть установлена через окружение или .env файл, но по умолчанию она не содержит значений.

В папке проекта где лежит ```docker-compose.yaml``` создать еще один файл ```.env```

Открыть ```.env``` в VScode и прописать в нем ```_PIP_ADDITIONAL_REQUIREMENTS=apache-airflow-providers-amazon```

Далее

Перезапустить контейнер с помощью Docker Compose

Перейти в папку с проектом Airflow, где находится файл docker-compose.yml.

Чтобы перезапустить контейнеры Airflow, используйте следующую команду:

```docker-compose down``` — завершает и удаляет все контейнеры, созданные с помощью docker-compose.

```docker-compose up -d``` — пересоздает и запускает контейнеры в фоновом режиме (-d — detached mode).

![image](https://github.com/user-attachments/assets/99345757-0944-4947-92ff-d80e332a9007)

После этого Airflow будет перезапущен, и изменения в конфигурации будут учтены.

**Проверка**

Чтобы проверить, установлен ли пакет apache-airflow-providers-amazon в контейнере Airflow в Docker.

1. Узнайте имя контейнера

Если вы не уверены, как называется контейнер, в котором работает Airflow, используйте команду:

```docker ps```

Это выведет список всех работающих контейнеров. Найдите контейнер, который связан с Airflow (например, airflow-webserver, airflow-scheduler, или airflow-init).

2. Войдите в контейнер
   
Теперь нужно войти в контейнер с Airflow. Используйте команду docker exec:

```docker exec -it <container_name> /bin/bash```

Замените <container_name> на имя контейнера, например airflow-webserver или любой другой контейнер, в котором работает Airflow.

Пример:

```docker exec -it airflow-webserver /bin/bash```

3. Проверьте установку пакета
   
После того как вы вошли в контейнер, выполните команду для проверки установленного пакета:

```pip show apache-airflow-providers-amazon```

Если пакет установлен, вы увидите информацию о нем, как в обычной среде Python, например:

![image](https://github.com/user-attachments/assets/29a519cd-50ad-4f7c-a2a8-c302884a858f)

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

# Настройка подключений в интерфейсе Airflow

В UI Airflow перейти в Admin-Connections нажать плюсик и добавить подключение 

![image](https://github.com/user-attachments/assets/fda9fa97-6e44-4299-aff8-c167dab10ea7)

**Здесь будет ссылка на test_dag**

Подключение для AWS

![image](https://github.com/user-attachments/assets/ab71e553-27b9-4b8b-a92f-57f24700e6f3)



# Заметки

Была ошибка, при загрузке файла в S3 с помощью Airflow.

При этом если загружать в S3 с помощью тестовых скриптов (Тесты которые выше при установке MINIO)  вручную, то все работает.

Проблема была в следующем:

Airflow развернут в Docker, а MinIO работает на  локальном компьютере (развернут локально), из за этого проблема с подключением между контейнерами Airflow и MinIO, потому что контейнер Airflow не видит 127.0.0.1 localhost. 

Нужно использовать IP адрес хоста или специальный Docker-сетевой адрес для доступа из контейнера Airflow к MinIO.  Короче надо вот так endpoint_url='http://host.docker.internal:9000', а уменя было вот так endpoint_url='http://127.0.0.1:9000'
