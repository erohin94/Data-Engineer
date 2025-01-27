# Переменные

Переменные (Variables): Переменные в Airflow представляют собой ключ-значение пары, которые могут быть использованы для хранения конфигурационных данных и параметров, доступных в рабочем процессе. Некоторые примеры использования переменных могут включать настройки подключения к базе данных, настройки авторизации и другие параметры, которые могут меняться в зависимости от окружения выполнения. Переменные можно определить и настроить через веб-интерфейс Airflow или использовать API для программного управления ими. Для доступа к переменным в коде задачи вы можете использовать объект Variable модуля airflow.models.

В Apache Airflow переменные можно создать через веб-интерфейс Airflow или с использованием API. Вот примеры создания переменных с использованием обоих подходов:

**1. Создание переменных через веб-интерфейс Airflow:**

Перейти в веб-интерфейс Airflow (доступен по адресу http://localhost:8080).

В меню выберать «Admin» и затем «Variables».

Нажать кнопку «Create» или «Add Variable».

Ввести имя переменной (Key) и значение переменной (Value).

Нажать кнопку «Save» или «Add».

**2. Создание переменных с использованием API:** 

Также можно использовать API для программного создания переменных. [Вот пример](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/Variables%2C%20Connections%2C%20and%20XCom/main_variables.py) использования API Python для создания переменной.

В моем конфиге airflow указано ```AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session'``` это значит что используется несколько методов аутентификации, а именно:

1.Basic Authentication (через заголовки Authorization с логином и паролем).
   
Если используется Basic Auth, нужно будет передавать логин и пароль в заголовке каждого запроса.

2.Session-based Authentication (через сессии, вероятно, используя куки для аутентификации после первоначальной авторизации).

Если используется Session-based Authentication, это значит, что необходимо сначала получить сессионный токен, а затем использовать его для выполнения API-запросов.

После выполнения кода, в интерфесе airflow увидим:

![image](https://github.com/user-attachments/assets/18942d4b-b3d8-45fc-9b17-96d467ced70c)

И если перейти через браузер по адресу http://127.0.0.1:8080/api/v1/variables.

![image](https://github.com/user-attachments/assets/30211898-cad8-40c2-afff-bf0ade86a165)

В этом примере мы отправляем POST-запрос на URL /api/v1/variables с указанием имени переменной (Key) и ее значения (Value) в формате JSON. Если ответ имеет код состояния 200, значит переменная была успешно создана.

Когда переменная создана, вы можете использовать ее в коде ваших задач с помощью объекта Variable модуля airflow.models. Вот пример использования переменной в коде - в этом примере мы получаем значение переменной с помощью Variable.get() и выводим его в задаче с помощью функции my_task().:

```from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime

def my_task():
    my_variable = Variable.get("my_variable")
    print(my_variable)

with DAG('my_dag', schedule_interval='@daily', start_date=datetime(2024, 1, 1)) as dag:
    task = PythonOperator(task_id='my_task', python_callable=my_task)```
```

# Подключения

Подключения (Connections): Подключения в Airflow представляют собой параметры, необходимые для установки связи с внешними источниками данных, такими как базы данных, сервисы облачных провайдеров, API и другие ресурсы. Эти параметры, такие как хост, порт, имя пользователя, пароль и другие, могут быть настроены и управляются в веб-интерфейсе Airflow или через API. Подключения в Airflow могут быть использованы в коде задач для установки соединения с внешними источниками данных. Для доступа к подключениям в коде задачи вы можете использовать объект Connection модуля airflow.hooks.base.
В Apache Airflow подключения можно создавать как через веб-интерфейс Airflow, так и с использованием API. Вот примеры создания подключений с использованием обоих подходов:

**1 Создание подключений через веб-интерфейс Airflow:**

Перейдите в веб-интерфейс Airflow ( доступен по адресу http://localhost:8080).

В меню выберите «Admin» и затем «Connections».

Нажмите кнопку «Create» или «Add Connection».

Заполните поля для подключения, такие как Conn Id (идентификатор подключения), Conn Type (тип подключения), Host, Port, Login, Password и другие, в зависимости от типа подключения.

Нажмите кнопку «Save» или «Add».

**2 Создание подключений с использованием API:**

Также можно использовать API для программного создания подключений. Вот пример использования API Python для создания подключения к базе данных PostgreSQL:

```
import requests

# URL для создания подключения
url = 'http://localhost:8080/api/v1/connections'

# Параметры запроса
headers = {'Content-Type': 'application/json'}
data = {
    'conn_id': 'my_postgres_conn',
    'conn_type': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'login': 'my_user',
    'password': 'my_password',
    'schema': 'my_schema'
}

# Отправка POST-запроса для создания подключения
response = requests.post(url, headers=headers, json=data)

# Проверка статуса ответа
if response.status_code == 200:
    print('Подключение успешно создано')
else:
    print('Ошибка при создании подключения:', response.status_code)
```

В этом примере отправляем POST-запрос на URL /api/v1/connections с указанием параметров подключения в формате JSON. Если ответ имеет код состояния 200, значит подключение было успешно создано.

Когда подключение создано, можно использовать его в коде задач с помощью объекта Connection модуля airflow.hooks.base. Вот пример использования подключения в коде:

```
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.base_hook import BaseHook
from datetime import datetime

def my_task():
    my_conn = BaseHook.get_connection("my_postgres_conn")
    print(f"Host: {my_conn.host}")
    print(f"Login: {my_conn.login}")

with DAG('my_dag', schedule_interval='@daily', start_date=datetime(2024, 1, 1)) as dag:
    task = PythonOperator(task_id='my_task', python_callable=my_task)
```

В этом примере получаем подключение с помощью BaseHook.get_connection() и выводим некоторые параметры подключения в задаче с помощью функции my_task(). 

Как выглядят переменные и подключения и как можно автоматизировать их добавление c помощью DAG.

Variables и connections по сути своей пары "ключ-значение". Получается что мы сможем сохранить их в соответствующем файле, это JSON.

Примера, есть ситуация когда необходимо в процессе выполнения DAG использовать подключение к базе данных PostgreSQL. Для этого создаем файл connections.json в таком виде:

```
{
  "conn1": {
    "conn_type": "postgres",
    "description": "Подключение к базе данных",
    "login": "postgres",
    "password": "password",
    "host": "host.docker.internal",
    "port": 5430,
    "schema": "test",
    "extra": "{}"
 }
}
```

А также в процессе задачи требуется использовать какие-то значения, которые не хорошо писать прям в коде (API ключи, какие-то параметры, подключения те же именовать). Для этого создадим файл variables.json в таком виде:

```
{
    "base_url": "https://www.тут-нужная-вам-ссылка.co/query",
    "conn_name": "conn1",
    "function": "TIME_SERIES_INTRADAY",
    "interval": "15min",
    "symbol_apple": "AAPL",
    "apikey": "----------",
    "outputsize": "full"
    
}
```

Теперь создадим DAG который назовем init, который будет добавлять наши переменные и подключения в Airflow автоматически, при помощи bash-оператора:

```
from datetime import datetime, timedelta, date
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

# аргументы дага по умолчанию
default_args = {
    "owner": "user",
    "retries": 0,
    "start_date": datetime.today()
}

# функция добавления переменных в airflow

with DAG(dag_id="01_init",description = 'Прикручиваем connections и variables', default_args=default_args, schedule_interval='@once', catchup=False) as dag:

    start = EmptyOperator(task_id='start')

    with TaskGroup("01_init", tooltip="Добавление connections") as init_tg:

        # ****************** добавление переменных ***********************

        set_variables = BashOperator(
            task_id = 'set_variables',
            bash_command='airflow variables import /opt/airflow/dags/variables.json'
        )

        # ****************** добавление connecions ***********************

        set_connections = BashOperator(
            task_id='set_connections',
            bash_command='airflow connections import /opt/airflow/dags/connections.json'
        )

    end = EmptyOperator(task_id='end')

    start >> init_tg >> end
```

# XComs (Cross-Communication)

XComs, или механизм кросс-коммуникации, позволяет задачам в Airflow обмениваться сообщениями или данными между собой. Каждая задача может "вытолкнуть" сообщение в XCom с помощью метода xcom_push, и другие задачи могут "вытянуть" это сообщение с помощью метода xcom_pull.

Это особенно полезно в сценариях, где результат выполнения одной задачи требуется для начала выполнения другой. Например, задача, которая обрабатывает данные, может передать результаты другой задаче, которая использует эти данные для обновления базы данных или отправки уведомлений.

XComs хранятся в базе данных Airflow, что делает этот механизм надежным и эффективным для управления данными между задачами.

```
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def push_data(**context):
    context['ti'].xcom_push(key='my_data', value='Hello, Airflow!')

def process_data(**context):
    my_data = context['ti'].xcom_pull(key='my_data')
    print(my_data)

with DAG('xcom_example_dag', schedule_interval='@daily', start_date=datetime(2024, 1, 1)) as dag:
    push_task = PythonOperator(
        task_id='push_task',
        python_callable=push_data,
        provide_context=True
    )

    process_task = PythonOperator(
        task_id='process_task',
        python_callable=process_data,
        provide_context=True
    )

    push_task >> process_task
```

В этом примере у две задачи: push_task и process_task.

В задаче push_task определяем функцию push_data(), которая отправляет данные 'Hello, Airflow!' в XCom с помощью метода xcom_push(). Мы используем аргумент **context, чтобы получить доступ к контексту выполнения задачи, и вызываем context['ti'].xcom_push() для отправки данных в XCom. Мы указываем ключ 'my_data' и значение 'Hello, Airflow!'.

В задаче process_task мы определяем функцию process_data(), которая получает данные из XCom с помощью метода xcom_pull(). Мы снова используем аргумент **context, чтобы получить доступ к контексту выполнения задачи, и вызываем context['ti'].xcom_pull() с ключом 'my_data', чтобы получить данные из XCom. Затем мы просто выводим полученные данные.

Затем мы связываем задачи push_task и process_task с помощью оператора >>, чтобы определить порядок их выполнения.

При выполнении этого DAG задача push_task сначала отправляет данные в XCom, а затем задача process_task получает эти данные из XCom и выводит их.
