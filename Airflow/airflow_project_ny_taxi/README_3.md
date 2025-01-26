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

Задача пайплайна — скачать сырые данные с сайта, трансформировать их в колоночный формат Parquet и загрузить в S3. Это одна из типичных задач дата инженеров, когда необходимо что-то откуда то выгрузить, сохранить и трансформировать.

В качестве хранилища можно использовать AWS S3. Это популярный сервис для хранения файлов от компании Amazon, также S3 можно рассматривать как распределенную файловую систему. Чтобы не платить, есть альтернатива, которую можно развернуть у себя на компьютере. Сервис [Minio](https://min.io/) полностью совместимый с S3 файловый сервер, поэтому Apache Airflow будет работать с ним как с AWS S3.

**Структура пайплайна**

Пайплайн (DAG) будет состоять из следующих операторов:

```- SimpleHttpOperator``` - для проверки существования файла на сервере перед его загрузкой

```- 2 PythonOperator```:

```- download_file``` — загрузка файла с сайта и перекладывание на S3 в сжатом виде (gzip)

```to_parquet``` — оператор скачивает файл, загруженный предыдущим оператором, и трансформирует его в формат Parquet, сохраняя результат в S3.

Вот как выглядит это на диаграмме с зависимостями:

![image](https://github.com/user-attachments/assets/6b1b3b38-daa8-4378-ba64-f5a934b8aa95)

Выполнение последующего шага зависит от успешности предыдущего. 

Если необходимого файла на сервере нет (check_file), то выполнение загрузки нецелесообразно (download_file), за этим строго следит Airflow.

**Про формат Parquet**

Дата инженеру, предстоит неоднократно столкнуться с различными форматами файлов. Хранить данные открытым текстом дорого и неэффективно. Дорого потому что объём больше (а в S3 плата взымается в том числе за размер файла), а неэффективно потому что для того, чтобы найти в нём нужную информацию, его надо прочитать целиком (не говоря уже о времени передачи по сети). Умные головы за нас решили эту проблему, поэтому существует множество эффективных способов хранить и читать данные.

**Apache Parquet** — это бинарный формат колоночного хранения данных в сжатом виде (есть ряд поддерживаемых алгоритмов сжатия, включая lzo, gzip, snappy и т.д.). Идеально подходит для представления табличных данных. Parquet-файл можно представить в виде базы данных с одной таблицей. Преимущество этого формата в эффективной компрессии файла за счёт колоночного хранения (строка по сути содержит все данные одной конкретной колонки), а также в эффективном чтении. В аналитических запросах редко присутствуют выборки всех колонок сразу, обычно читают лишь часть. Если не вдаваться в детали реализации Parquet, а попробовать объяснить представление данных внутри максимально просто, то Parquet выглядит как небольшая файловая система, где значения каждой колонки лежат в отдельных файлах, а также присутствует дополнительный файл с метаданными, где хранится информация о типах колонок и их расположении. То есть чтобы получить значения заданных колонок нужно прочитать только файлы, содержащие данные этих колонок (а не всё целиком). Надеюсь у меня получилось внятно объяснить. Подробную информацию можно найти на официальном [сайте Apache Parquet](https://parquet.apache.org/). Также рекомендую взглянуть на наглядное [сравнение между Parquet и CSV в скорости обработки и стоимости](https://dzone.com/articles/how-to-be-a-hero-with-powerful-parquet-google-and).

# Скелет DAG

Ниже начальный код для будущего DAG с использованием синтаксиса TaskFlow API. По мере описания каждого оператора он будет заполняться в готовый для запуска DAG.

Как можно видеть из настроек, грузить данные мы будем за каждый месяц, начиная с 1 января 2020 года. Периодичность запуска — 1 раз в месяц.

```
from datetime import datetime

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.providers.http.operators.http import SimpleHttpOperator
from .functions import download_dataset, convert_to_parquet

default_args = {
    'owner': 'airflow',
}

@dag(default_args=default_args,
     schedule_interval='@monthly',
     start_date=datetime(2020, 1, 1),
)
def nyc_taxi_dataset_dag():

   # здесь будут таски
```

# Разбор каждого оператора из DAG по отдельности

**check_file**

Первым оператором будет ```SimpleHttpOperator``` под названием ```check_file```. ```SimpleHttpOperator``` входит в стандартный набор операторов Apache Airflow. Его задача — выполнить HTTP запрос и вернуть ответ. Мы его будем использовать для проверки существования файла перед его загрузкой.

Чтобы не скачивать весь файл целиком я предлагаю использовать метод HEAD (При использовании с данной ссылкой метод HEAD падает в ошибку, другие ссылки при этом работают. Использую метод GET все работает корректно.). Он идентичен стандартному GET с той лишь разницей, что ответ будет без тела, вернутся лишь заголовки и статус ответа.

Также ```SimpleHttpOperator``` отличный способ показать как работать с разделом ```Connections```.

При инициализации оператор принимает несколько аргументов:

```task_id``` — уникальное название оператора

```method``` — HTTP метод, использую GET

```http_conn_id``` — название ключа соединения, которое мы создадим через раздел Connections. Оператору нельзя передать полную ссылку напрямую.

```endpoint``` — URI, т.е. это всё, что есть в ссылке после указания домена. Например, если полная ссылка на данные за декабрь 2020 года ```https://data.cityofnewyork.us/resource/kxp8-n2sj.csv```, то endpoint здесь это ```/resource/kxp8-n2sj.csv``` или ```kxp8-n2sj.csv```. Он меняется в зависимости от года и месяца.

```dag``` — инстанс объекта DAG (если используется декоратор dag, то этот аргумент можно опустить).

Также у оператора есть и другие принимаемые аргументы, например, тело запроса, заголовки и даже есть возможность передать callable объект для обработки ответа в аргументе response_check. Но для нашего пайплайна это не нужно.

# Создание connection id

В работе с Apache Airflow вы неоднократно столкнётесь с Connections, т.к. система поощряет использование идентификаторов соединения вместо указания ссылки в коде. Для создания идентификатора необходимо перейти в раздел Admin → Connections и нажать на +:

![image](https://github.com/user-attachments/assets/a7dc3ff8-a2cf-4a6f-8d65-5fcb507f6de3)

На форме необходимо заполнить несколько полей:

**Conn Id:** nyc_yellow_taxi_id

**Conn Type:** HTTP

**Host:** https://data.cityofnewyork.us/

![image](https://github.com/user-attachments/assets/7aa03487-8193-45da-aa8e-2242a820918a)

В endpoint будем передавать название файла, т.к. эта часть меняется в зависимости от года и месяца.

Вот как выглядит код оператора проверки наличия файла:

```
check_file = SimpleHttpOperator(
    method='GET',
    endpoint='resource/t29m-gskq.csv',
    task_id='check_file',
    http_conn_id='nyc_yellow_taxi_id'
)
```

*Заметка```
(check_file = SimpleHttpOperator(
    method='HEAD',
    endpoint='yellow_tripdata_{{ execution_date.strftime("%Y-%m") }}.csv',
    task_id='check_file',
    http_conn_id='nyc_yellow_taxi_id'
)```
Обратите внимание на endpoint. У операторов Airflow есть т.н. template fields, куда можно передавать строку-шаблон и Airflow подставит нужные значения в зависимости от контекста. Переменная execution_date входит в набор переменных по умолчанию, доступных в контексте выполнения DAG (DagRun), она представляет из себя объект типа Pendulum из пакета pendulum, это datetime на стероидах. В качестве шаблонизатора Apache Airflow использует Jinja2. execution_date указывает на дату исполнения, это не дата на компьютере в момент выполнения DAG, а дата, рассчитанная относительно start_date и schedule interval. Пример как считается execution_date я описывал ранее.)*

**download_file**

Следующий оператор — PythonOperator с task_id download_file. Его задача загрузить файл с веб-сайта и уложить в S3 в сжатом виде (будем использовать gzip).

PythonOperator принимает объект типа callable, который будет выполнен, поэтому загрузку файла мы вынесем в отдельную функцию functions.py. Вот код этой функции:

```
def download_dataset(year_month: str):
    url = (
        f'https://data.cityofnewyork.us/resource/t29m-gskq.csv'
    )
    response = requests.get(url, stream=True)
    response.raise_for_status()

    s3 = S3Hook('aws_connection_id')

    s3_path = f's3://nyc-yellow-taxi-raw-data/t29m-gskq.csv.gz'
    bucket, key = s3.parse_s3_url(s3_path)

    with NamedTemporaryFile('w', encoding='utf-8', delete=False) as f:
        for chunk in response.iter_lines():
            f.write('{}\n'.format(chunk.decode('utf-8')))
    s3.load_file(f.name, key, bucket, replace=True, gzip=True)

    return s3_path
```

Cоздать следующую структуру папок airflow_project_ny_taxi\dags\nyc_taxi\functions.py и поместить туда код, далее в этот functions.py добавиться еще кусок кода.

Я предпочитаю выносить эту логику в отдельный модуль или даже пакет (если одного модуля недостаточно), поэтому в репозитории есть модуль functions.py.

Функция download_dataset принимает 1 аргумент, это строка вида 2020-12: год и месяц. Скачивание файла производится пакетом requests. Для работы с S3 я использую готовый Hook из Airflow — S3Hook.

Хуки это внешние интерфейсы для работы с различными сервисами: базы данных, внешние API ресурсы, распределенные хранилища типа S3, redis, memcached и т.д. Хуки являются строительными блоками операторов и берут на себя всю логику по взаимодействию с хранилищем конфигов и доступов. Используя хуки можно забыть про головную боль с хранением секретной информации в коде (например, паролей).

S3Hook даёт разработчику высокоуровневый интерфейс для работы с AWS S3, а под капотом использует библиотеку boto3. Самый главный аргумент, который нужно передать S3Hook — aws_conn_id. Соединение также необходимо создать через раздел Admin → Connections.

В коде прописан путь до S3 объекта, куда будет сохранён загружаемый файл с данными. Далее с веб-ресурса файл сохраняется во временный файл и загружается на S3 с использованием gzip=True. Функция возвращает путь до S3 объекта, которым воспользуется следующий оператор.

Демонстрацию создания бакетов и доступов в Apache Airflow смотрите в следующем параграфе.



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




Теперь проделываем шаги чтобы указать данные для доступа к этому файловому хранилищу.

Для этого переходим в уже запущенный Airflow -> Admin -> Connections нажимаем на плюсик (+ Add a new record)

Вводим параметры

![image](https://github.com/user-attachments/assets/d0fcd82e-30b5-4209-ac28-70538f64af86)

