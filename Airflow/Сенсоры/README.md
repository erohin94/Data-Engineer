# Сенсоры

Сенсоры это разновидность операторов, чья задача реагировать на какое-либо событие и в зависимости от результата продолжать цепочку выполнения тасков или "засыпать" для повторной проверки через X секунд. Например, ожидается появление файла в источнике (S3-бакет, FTP-сервер и т.д.). Если файл на месте, то можно продолжить цепочку задач — скачать, преобразовать, загрузить в другое место. Если файла ещё нет, то сенсор повторит проверку через заданное время (в секундах).

В Apache Airflow существует ряд готовых сенсоров на все случаи жизни:

```PythonSensor``` — выполняет функцию, переданную в python_callable, и в случае, если она возвращает True продолжает цепочку дальше.

```DateTimeSensor``` — ждёт наступления заданной даты и времени

```S3KeySensor``` — ждёт появления S3-объекта по переданному пути

```FileSensor``` — проверяет появился ли файл или директория с файлом по заданному пути

```HttpSensor``` — делает запрос на заданный URL, повторяет его пока удалённый хост не вернёт успешный запрос (статусы 2xx)

Применить сенсоры в работе с датасетом поездок на такси очень просто. Можно заменить ```SimpleHttpOperator``` на ```HttpSensor``` с минимальными модификациями. Во-первых, будет происходить точно такая же проверка наличия файла перед его загрузкой. Во-вторых, в случае если файла нет на сервере, то таск не будет падать, а будет автоматически перезапускаться через заданный интервал для повторной проверки.

Например на сайте нет данных за 2021 год хотя прошло 2 полных месяца (январь и февраль), датасеты появляются с задержкой в несколько месяцев. Поэтому реализация через сенсор имеет большой плюс — не нужно самостоятельно следить когда данные появятся на сайте и перезапускать DAG для конкретного месяца. Датасет будет загружен автоматически как только данные станут доступны на сайте.

**HttpSensor**

```HttpSensor``` очень похож на ```SimpleHttpOperator``` с той лишь разницей, что умеет повторять запросы в случае, если критерий успеха не был удовлетворен. Критерием успеха является HTTP-код ответа. Если сервер вернул статус 200 (включая все 2xx статусы), то цепочка продолжится дальше, а если ответ был 404, то запрос повторится через заданный интервал. Также можно передать ```callable```-объект в аргумент ```response_check```, чтобы провести дополнительную проверку и задать свой критерий успеха.

```
from airflow.providers.http.sensors.http import HttpSensor

check_if_exists = HttpSensor(
    method='HEAD',
    endpoint='yellow_tripdata_{{ execution_date.strftime("%Y-%m") }}.csv',
    http_conn_id='nyc_yellow_taxi_id',
    task_id='check_if_exists',
    poke_interval=60 * 60,  # каждый час
    mode='poke',
)
```

Помимо знакомых уже параметров method, endpoint, http_conn_id, два новых:

```poke_interval``` — интервал ожидания между повторными проверками в секундах

```mode``` — режим проверок, по умолчанию равен poke.

**Режимы mode**

Начиная с Apache Airflow 1.10.2 у сенсоров появился аргумент mode через который задаётся режим их работы. Сейчас есть 2 основных режима:

```poke```

```reschedule```

Также есть ```smart sensor```, который нужно активировать через ```airflow.cfg```.

Что же выбрать между ```poke``` и ```reschedule```? 

Если сенсор работает в режиме ```poke```, то воркер, исполняющий его, всегда находится в режиме работы и не может исполнять другие задачи (между ```poke_interval``` у него выполняется ```sleep```). 

Не рекомендуется использовать этот режим, если у вас большой интервал ожидания между периодическими проверками. Используйте ```poke```, если требуется часто делать проверку (до 1 минуты), для всего что дольше — ```reschedule```. В режиме ```reschedule``` воркер освобождается, и сенсор помечается для повторного перезапуска через ```poke_interval``` (в случае, если критерий успеха не был достигнут и нужен перезапуск).

# DAG

Реализация DAGа на сенсоре. Необходимо заменить ```SimpleHttpOperator``` на ```HttpSensor``` и добавить 2 дополнительных аргумента: ```mode``` и ```poke_interval```. Делать проверку чаще 1 раза в сутки нет мысла, но можно делать реже. Я для простоты указал интервал раз в 24 часа в секундах (60 * 60 * 24).

```
import datetime as dt

from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import get_current_context
from airflow.providers.http.sensors.http import HttpSensor

from nyc_taxi.functions import download_dataset, convert_to_parquet

default_args = {
    'owner': 'airflow',
}

with DAG(
    start_date=dt.datetime(2021, 1, 1),
    dag_id='nyc_taxi_2021_dag',
    schedule_interval='@monthly',
    default_args=default_args,
) as dag:

    check_if_exists = HttpSensor(
        method='HEAD',
        endpoint='yellow_tripdata_{{ execution_date.strftime("%Y-%m") }}.csv',
        http_conn_id='nyc_yellow_taxi_id',
        task_id='check_if_exists',
        poke_interval=60 * 60 * 24,  # раз в 24 часа
        mode='reschedule',
    )

    @task
    def download_file():
        context = get_current_context()
        return download_dataset(context['execution_date'].strftime('%Y-%m'))

    @task
    def to_parquet(file_path: str):
        context = get_current_context()
        return convert_to_parquet(context['execution_date'].strftime('%Y-%m'), file_path)

    file_path = download_file()
    parquet_file_path = to_parquet(file_path)

    check_if_exists >> file_path >> parquet_file_path
```

