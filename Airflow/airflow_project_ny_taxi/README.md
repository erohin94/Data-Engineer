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

**Про датасет**

Использую датасет, содержащий поездки на такси по городу Нью-Йорк. Данные открыто лежат на [сайте](https://opendata.cityofnewyork.us/).

В качестве хранилища можно использовать AWS S3. Это популярный сервис для хранения файлов от компании Amazon, также S3 можно рассматривать как распределенную файловую систему. Чтобы не платить, есть альтернатива, которую можно развернуть у себя на компьютере. Сервис [Minio](https://min.io/) полностью совместимый с S3 файловый сервер, поэтому Apache Airflow будет работать с ним как с AWS S3.

**Структура пайплайна**

Пайплайн (DAG) будет состоять из следующих операторов:

```- SimpleHttpOperator``` - для проверки существования файла на сервере перед его загрузкой

```- PythonOperator``` - загрузка файла с сайта и перекладывание на S3 в виде csv

Вот как выглядит это на диаграмме с зависимостями:

![image](https://github.com/user-attachments/assets/fc45caf9-db53-4703-963b-95126080ea60)

Выполнение последующего шага зависит от успешности предыдущего. 

Если необходимого файла на сервере нет (check_file_task), то выполнение загрузки нецелесообразно (upload_task), за этим строго следит Airflow.



# Настройка подключений в интерфейсе Airflow

В UI Airflow перейти в Admin-Connections нажать плюсик и добавить подключение 

![image](https://github.com/user-attachments/assets/fda9fa97-6e44-4299-aff8-c167dab10ea7)

В форме необходимо заполнить несколько полей:

**Conn Id**: ```nyc_yellow_taxi_id```

**Conn Type:** ```HTTP```

**Host:** ```https://data.cityofnewyork.us```

Код оператора из будущего DAG отдельно:

```
check_file_task = SimpleHttpOperator(
    task_id='check_file_exists_task_2',
    method='GET',  # Используем метод для проверки доступности ресурса
    http_conn_id='nyc_yellow_taxi_id',  # Настроить в UI Airflow Admin-Connections поле Connection id
    endpoint='/resource/kxp8-n2sj.csv',  # Путь файла
    headers={"Accept": "application/json"},  # Заголовки запроса
    response_check=lambda response: response.status_code == 200,  # Проверка ответа
    dag=dag,
)
```

```SimpleHttpOperator``` его задача — выполнить HTTP запрос и вернуть ответ. Используем для проверки существования файла перед его загрузкой. Также ```SimpleHttpOperator``` отличный способ показать как работать с разделом Connections.

При инициализации оператор принимает несколько аргументов:

```task_id``` — уникальное название оператора.

```method``` — HTTP метод, использую GET.

```http_conn_id``` — название ключа соединения, создали через раздел Connections. Оператору нельзя передать полную ссылку напрямую.

```endpoint``` — URI, т.е. это всё, что есть в ссылке после указания домена. 

Например, если полная ссылка на данные ```https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2020-12.csv```, то endpoint здесь это ```/trip+data/yellow_tripdata_2020-12.csv или yellow_tripdata_2020-12.csv```. 
Он меняется в зависимости от года и месяца.

```headers``` - это словарь, который передается в запрос, чтобы указать дополнительные параметры или информацию. В моем случае этот заголовок сообщает серверу, что клиент (в данном случае Airflow) ожидает получить данные в формате JSON. То есть, сервер должен возвращать ответ в формате JSON, если это возможно.

```response_check``` - это функция, которая используется для проверки ответа от сервера. Задача будет успешной только в том случае, если HTTP-ответ от сервера имеет код состояния 200, что означает успешное выполнение запроса.

```dag``` — инстанс объекта DAG (если используется декоратор dag, то этот аргумент можно опустить).

**Подключение для AWS.**

Можно в ```AWS Access Key ID``` и ```AWS Secret Access Key``` ввести ```minioadmin```. 

В Extra 
```
{
  "endpoint_url": "http://host.docker.internal:9000",
  "region_name": "us-east-1"
}
```

![image](https://github.com/user-attachments/assets/d9f02bd1-5bce-4e6f-b653-deb88f6eced3)

А можно в интерфейсе MINIO создать секретные ключи

![image](https://github.com/user-attachments/assets/4b47f37a-dc6d-4432-9b9f-e09ceb7126d3)

![image](https://github.com/user-attachments/assets/843f2b64-c03d-4874-b3d8-c0d920cd6171)

Копируем и вставляем их в UI Airflow так же в ```AWS Access Key ID``` и ```AWS Secret Access Key``` вместо ```minioadmin```.

![image](https://github.com/user-attachments/assets/ff8f42a5-46b9-40e7-a71d-8e4913b2adf2)


![image](https://github.com/user-attachments/assets/ab71e553-27b9-4b8b-a92f-57f24700e6f3)

# DAG

В папке проекта dags создать DAG

[Ссыдка на даг 2](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/airflow_project_ny_taxi/dags/test_dag_2.py) - используется S3Hook от Airflow для взаимодействия с MinIO (или S3). S3Hook предоставляет более абстрактированный интерфейс для работы с хранилищем, что упрощает подключение и работу с сервисами AWS, используя настройки, указанные в UI Airflow. В этом случае все настройки подключения (например, ключи доступа и другие параметры) не указываются в коде.

Хуки это внешние интерфейсы для работы с различными сервисами: базы данных, внешние API ресурсы, распределенные хранилища типа S3, redis, memcached и т.д. Хуки являются строительными блоками операторов и берут на себя всю логику по взаимодействию с хранилищем конфигов и доступов. Используя хуки можно забыть про головную боль с хранением секретной информации в коде (например, паролей).

S3Hook даёт разработчику высокоуровневый интерфейс для работы с AWS S3, а под капотом использует библиотеку boto3. Самый главный аргумент, который нужно передать S3Hook — aws_conn_id. Соединение также необходимо создать через раздел Admin → Connections.

[Ссыдка на даг](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/airflow_project_ny_taxi/dags/test_dag.py) - подключение и работа с MinIO осуществляются через библиотеку boto3 напрямую в коде. Мы создаем объект клиента S3 вручную и используем его для загрузки файла. В этом случае явно указываются параметры подключения, такие как endpoint_url, aws_access_key_id, aws_secret_access_key и другие параметры в коде. Это означает, что настройки подключения (например, ключи доступа) жестко прописаны в самом коде.


# Заметка - ошибка при загрузке файла в S3

Была ошибка, при загрузке файла в S3 с помощью Airflow.

При этом если загружать в S3 с помощью тестовых скриптов (Тесты которые выше при установке MINIO)  вручную, то все работает.

Проблема была в следующем:

Airflow развернут в Docker, а MinIO работает на  локальном компьютере (развернут локально), из за этого проблема с подключением между контейнерами Airflow и MinIO, потому что контейнер Airflow не видит 127.0.0.1 localhost. 

Нужно использовать IP адрес хоста или специальный Docker-сетевой адрес для доступа из контейнера Airflow к MinIO.  Короче надо вот так endpoint_url='http://host.docker.internal:9000', а уменя было вот так endpoint_url='http://127.0.0.1:9000'

```
def upload_to_minio():
    s3 = boto3.client('s3', 
                      endpoint_url='http://host.docker.internal:9000',  # Адрес MinIO
                      aws_access_key_id='ANV9JuSM47gsMx8BtBqf', 
                      aws_secret_access_key='Y3O0qw1fV3cP1dzDXIDASAUx2vnaRFm28lDr3RYs', 
                      region_name='us-east-1')
```

[Ссыдка на даг](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/airflow_project_ny_taxi/dags/test_dag.py) 

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
