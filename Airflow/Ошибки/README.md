# Заметка - ошибка при загрузке файла в S3

Была ошибка, при загрузке файла в S3 с помощью Airflow.

При этом если загружать в S3 с помощью тестовых скриптов (Тесты которые при установке MINIO) вручную, то все работает.

Проблема была в следующем:

Airflow развернут в Docker, а MinIO работает на  локальном компьютере (развернут локально), из за этого проблема с подключением между контейнерами Airflow и MinIO, потому что контейнер Airflow не видит `127.0.0.1 localhost`. 

Нужно использовать IP адрес хоста или специальный Docker-сетевой адрес для доступа из контейнера Airflow к MinIO.  Короче надо вот так `endpoint_url='http://host.docker.internal:9000'`, а уменя было вот так `endpoint_url='http://127.0.0.1:9000'`

```
def upload_to_minio():
    s3 = boto3.client('s3', 
                      endpoint_url='http://host.docker.internal:9000',  # Адрес MinIO
                      aws_access_key_id='ANV9JuSM47gsMx8BtBqf', 
                      aws_secret_access_key='Y3O0qw1fV3cP1dzDXIDASAUx2vnaRFm28lDr3RYs', 
                      region_name='us-east-1')
```

# Заметка - проверка установки S3Hook

Для подключения к S3 надо импортировать класс S3Hook

```from airflow.providers.amazon.aws.hooks.s3 import S3Hook```

S3Hook — это класс, который используется для взаимодействия с Amazon S3 (облачное хранилище данных от Amazon). С помощью S3Hook можно загружать файлы в S3, скачивать их, проверять наличие объектов и другие операции с данными в облаке.

S3Hook упрощает работу с S3 в контексте задач в Airflow.

Чтобы проверить, установлен ли пакет apache-airflow-providers-amazon в контейнере Airflow в Docker.

1. Узнать имя контейнера

Если не понятно, как называется контейнер, в котором работает Airflow, ввести команду:

```docker ps```

Это выведет список всех работающих контейнеров. Найти контейнер, который связан с Airflow (например, airflow-webserver, airflow-scheduler, или airflow-init).

2. Войти в контейнер
   
Теперь нужно войти в контейнер с Airflow. Использовать команду docker exec:

```docker exec -it <container_name> /bin/bash```

Заменить <container_name> на имя контейнера, например airflow-webserver или любой другой контейнер, в котором работает Airflow.

Пример:

```docker exec -it airflow-webserver /bin/bash```

3. Проверить установку пакета
   
После того как вошли в контейнер, выполнить команду для проверки установленного пакета:

```pip show apache-airflow-providers-amazon```

Если пакет установлен, увидим информацию о нем, как в обычной среде Python, например:

![image](https://github.com/user-attachments/assets/29a519cd-50ad-4f7c-a2a8-c302884a858f)

# Заметка - проверить какие библиотеке установлены в контейнере

Чтобы проверить, какие библиотеки установлены в Docker контейнере, можно использовать несколько способов. Рассмотрим основные:

```docker ps``` - все работающие контейнеры

```docker exec -it <container_id_or_name> /bin/bash``` - войти в контейнер

```pip list``` - после того как оказался внутри контейнера, использую pip для вывода списка установленных библиотек

```docker exec <container_id_or_name> pip list``` - если не хочешь входить в контейнер, можно использовать команду docker exec напрямую из терминала

В официальном образе Apache Airflow, который можно скачать с Docker Hub, уже предустановлены многие библиотеки Python, которые часто используются в задачах Airflow (requests, pandas, numpy, boto3 и тд).

# Заметка - установка доп библиотек если ее нет в стандартном образе Airflow

Если нужно добавить дополнительные библиотеки, которые не входят в официальный образ, можно использовать переменную окружения _PIP_ADDITIONAL_REQUIREMENTS (находится в файле docker-compose.yaml). 

![image](https://github.com/user-attachments/assets/f3307d37-115d-402d-855f-1f4491c75432)

Пример как добавить доп библиотеки:

В папке проекта где лежит ```docker-compose.yaml``` создать еще один файл ```.env```. Пример [ссылка на .env файл](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/airflow_project_ny_taxi/.env)

Открыть ```.env``` в VScode и прописать в нем ```_PIP_ADDITIONAL_REQUIREMENTS=apache-airflow-providers-amazon```

Далее перезапустить контейнер с помощью Docker Compose

Перейти в папку с проектом Airflow, где находится файл docker-compose.yml.

Чтобы перезапустить контейнеры Airflow, используйте следующую команду:

```docker-compose down``` — завершает и удаляет все контейнеры, созданные с помощью docker-compose.

```docker-compose up -d``` — пересоздает и запускает контейнеры в фоновом режиме (-d — detached mode).

![image](https://github.com/user-attachments/assets/99345757-0944-4947-92ff-d80e332a9007)
