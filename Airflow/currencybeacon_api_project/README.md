Попробую написать свой Operator и Hook.

Они будут нужны для взаимодействия с внешним API сервисом, хранящим курсы валют. Также буду использовать PostgreOperator для укладки полученных данных в таблицу, которую также будет создавать отдельным таском.

# **Про Hook**

В Airflow, **hook** — это объект, который используется для установления подключения и взаимодействия с внешними системами, такими как базы данных, облачные хранилища, API и другие сервисы. Хуки предоставляют интерфейсы для выполнения операций с этими системами, абстрагируя детали подключения и взаимодействия. Они помогают упростить доступ к данным и поддерживать безопасность, так как многие параметры подключения можно задать в одном месте.

**Примеры хуков в Airflow:**

`PostgresHook`: Используется для подключения и выполнения операций с базами данных PostgreSQL. Например, вы можете подключаться к базе данных, выполнять SQL-запросы и управлять транзакциями.

`HttpHook`: Используется для взаимодействия с внешними API через HTTP-запросы.

`S3Hook`: Используется для взаимодействия с хранилищем S3 в AWS. Вы можете загружать и скачивать файлы, создавать бакеты и другие операции.

**Как работают хуки:**

**Соединение:** Хуки получают данные подключения (логин, пароль, хост, порт и т.д.) из настроек соединений Airflow (в Admin -> Connections), для доступа к базам данных, API или другим системам.

**Методы:** Каждый хук предоставляет набор методов для выполнения операций с внешними системами, например, get_conn(), run() и другие. Например, для взаимодействия с базой данных можно использовать методы для выполнения SQL-запросов, загрузки данных и т.д.

**Повторное использование:** Хуки позволяют создавать общие логики взаимодействия с внешними системами, которые можно повторно использовать в различных тасках.

# **Описание проекта**

DAG будет выглядеть следующим образом:

**Здесь будет картинка------------------------------------------------------------**

В пайплайне 3 таска:

`create_table`, отвечает за создание таблицы в базе данных PostgreSQL

`get_rate`, собственный Operator для работы с API сервиса курсов валют

`insert_rate`, укладывает полученный курс в таблицу, созданную в таске create_table

# **create_table**

Первый таск из пайплайна отвечает за создание таблицы, если её нет. В качестве базы данных используется PostgreSQL, можно поднять новый docker-образ базы:

[Ссылка для настройки PostgreSQL через Docker](https://github.com/erohin94/Data-Engineer/tree/main)

[Ссылка для настройки Airflow через Docker](https://github.com/erohin94/Data-Engineer/tree/main/Airflow)

В интерфейсе Airflow, в Admin → Connections необходимо обновить соединение postgres_default как показано на скрине:

![image](https://github.com/user-attachments/assets/51a5ea93-17a0-4e36-a9f7-28a06e909eaf)

Для подключения, передал в Admin → Connections следующие параметры из `docker-compose.yml` файла:

```
services:
  postgres:
    image: postgres:15
    restart: always
    container_name: postgres
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: 1
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
      

volumes:
  postgres_data:
```

где:

`Connection Id` : `postgres_default` (или любое другое имя для идентификации подключения)

`Connection Type` : `Postgres`

`Host` : `postgres` (это имя контейнера PostgreSQL, указанное в docker-compose.yml)

`Database` : postgres` (имя базы данных, как указано в переменной среды POSTGRES_DB)

`Login` : `test` (имя пользователя, указанное в переменной среды POSTGRES_USER)

`Password` : `1` (пароль, указанный в переменной среды POSTGRES_PASSWORD)

`Port` : `5432` (порт PostgreSQL)

Это соединение используется по умолчанию для всех Postgres операторов, безусловно можно создать новое и явно указывать его ID при создании оператора.

Для работы с Postgres в Apache Airflow есть `PostgresOperator`. Под капотом он использует библиотеку `psycopg2` для работы с базой. Именно его мы будем использовать в двух из трёх наших операторах:

`create_table`
`insert_rate`

`PostgresOperator` может принимать запрос строкой либо читать его из файла. Буду сспользовать второй вариант, т.к. он делает код более читабельным без смешивания SQL и Python. Пример оператора с запросом строкой:

```
sql_task = PostgresOperator(
    task_id='sql_task_id',
    postgres_conn_id='postgres_default',
    sql='SELECT foo FROM bar;',
)
```

Через указание пути до SQL файла:

```
sql_task = PostgresOperator(
    task_id='sql_task_id',
    postgres_conn_id='postgres_default',
    sql='sql/select_query.sql',
)
```

Выбираю второй вариант, поэтому необходимо подготовить SQL запрос создания таблицы и сохранить его в файл create_table.sql:

```
CREATE TABLE IF NOT EXISTS currency_exchange_rates (
    base VARCHAR(3) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    rate NUMERIC(12, 3) NOT NULL,
    date DATE NOT NULL,
    UNIQUE (base, currency, date)
);
```

При каждом запуске DAG будет выполняться таск `create_table`, поэтому в SQL выражении есть конструкция `IF NOT EXISTS`, которая означает, что таблица должна быть создана ТОЛЬКО, если её нет. То есть при повторном выполнении этого таска Postgres проигнорирует этот запрос, т.к. таблица уже будет существовать.

Таблица `currency_exchange_rates`:

`base` — хранится код базовой валюты

`currency` — хранится код конвертируемой валюты

`rate` — обменный курс между `currency` и `base`, т.е. стоимость `base` в `currency`

`date` — дата

Свойство `UNIQUE` по трём столбцам необходимо, чтобы делать вставку через `UPSERT` (опишу далее). Если по какой-то причине таск с одной и той же датой будет запущен несколько раз нужно не допустить дублирования.

Итак, всё готово для создания первого оператора:

```
create_table = PostgresOperator(
    task_id='create_table_task',
    sql='sql/create_table.sql',
    postgres_conn_id='postgres_default',
)
```

Путь SQL файла необходимо указывать относительно директории, где лежит сам DAG. В данном случае папка sql лежит в одной директории с кодом DAGа. Аргумент `postgres_conn_id` можно не указывать, т.к. по умолчанию он будет равен `postgres_default`, но я предпочитаю явно это делать.

# **get_rate**

Для таска `get_rate` напишем свой кастомный оператор, который будет тянуть данные из внешнего API. В качестве сервиса использую [currencybeacon](https://currencybeacon.com/).

Для работы с сервисом необходимо зарегистрироваться и получить API ключ. Ключ будет доступен сразу же после авторизации на сайте:

![Снимок](https://github.com/user-attachments/assets/533d9738-92a6-4ad4-ab60-e4159553cc1d)

`Operator` и `Hook` для работы с сервисом напишем позже, сейчас рассмотрим последний таск в нашем пайплайне — `insert_rate`.

# **insert_rate**

Для таска `insert_rate` также будем использовать `PostgresOperator`. Его задача — добавить запись о курсе валют в базу данных после успешного выполнения предыдущего таска `get_rate`.

Вставка данных будет происходить через `UPSERT`. Нередко бывают сбои и чтобы не допустить дублирования данных все таски в Airflow должны быть идемпотентными. 

В случае с таском `insert_rate` при обнаружении дубля по 3-м колонкам: `base`, `currency` и `date`, произойдёт обновление колонки `rate` вместо добавления ещё одной. Пример SQL запроса:

```
INSERT INTO
    currency_exchange_rates
VALUES ('USD', 'KZT', 420.55, '2020-01-01')
ON CONFLICT (base, currency, date) DO
    UPDATE
        SET rate = excluded.rate;
```

Если в таблице `currency_exchange_rates` уже будет запись обменного курса `USD/KZT` за 1 января, то у этой строчки будет обновлена колонка `rate` на значение `420.55`. Выражение `excluded.rate` ссылается на значение обменного курса, предложенного для вставки (новое значение).

Код оператора:

```
insert_rate = PostgresOperator(
    task_id='insert_rate',
    postgres_conn_id='postgres_default',
    sql='sql/insert_rate.sql',
    params={
        'base_currency': 'USD',
        'currency': 'KZT',
    }
)
```

Обратите внимание на аргумент `params`, он позволяет передавать значения в SQL-шаблон. Конкретно в этом случае значения у нас статичные, но в конце модуля будет пример с созданием динамических тасков, где это актуально. Параметры в шаблоне доступны через переменную `params`. К ним можно обратиться так:

```
{{ params.base_currency }} 
{{ params.currency }} 
```

А теперь давайте взглянем как выглядит файл с SQL запросом:

Код SQL шаблона:

```
INSERT INTO
    currency_exchange_rates
VALUES ('{{ params.base_currency }}', '{{ params.currency }}', {{ ti.xcom_pull(task_ids="get_rate") }}, '{{ execution_date.strftime("%Y-%m-%d") }}')
ON CONFLICT (base, currency, date) DO
    UPDATE
        SET rate = excluded.rate;
```

Переменная `execution_date` знакома, с `params` тоже всё понятно.

А что по поводу выражения?

```
{{ ti.xcom_pull(task_ids="get_rate") }}
```
Переменная `ti` также как и `execution_date` доступна в контексте выполнения DAG и ссылается на инстанс текущего таска (PostgresOperator), инстанс также доступен под названием `task_instance`.

# **Создание своего Hook**

Hook это классы для работы с внешними сервисами, их можно считать своего рода кирпичиками на которых строятся операторы. Операторы, которые взаимодействуют со сторонними системами, делают это через свои хуки. Например, `PostgresOperator` использует `PostgresHook` для запросов в базу, а для работы с `S3` мы уже использовали `S3Hook`.

Почему стоит писать свой Hook? Почему бы весь код работы с сервисом не написать в кастомном `Operator` классе?

Две основные, причины:

1.Разделение ответственности или `Single Responsibility Principle`

2.Работа с доступами в Airflow

Чтобы реализовать свой хук-класс необходимо наследоваться от базового класса `BaseHook`. У этого класса есть методы для работы с хранилищем доступов (метод `get_connection`). Ему нужно передать ваш `connection_id` и он вернёт все настройки по нему.

Для получения курсов валют мы будем использовать сервис `Currencybeacon`, `endpoint` на который будем слать запросы: https://api.currencybeacon.com/v1/historical

[Документация](https://currencybeacon.com/api-documentation)

Он принимает несколько параметров:

`base` — базовая валюта

`symbols` — список валют в которых выражается стоимость базовой валюты

`date` — дата обменного курса

Также ко всем API запросам необходимо дополнительно передавать параметр `api_key` с ключом доступа. Ключ мы как обычно будем хранить в базе данных Airflow и получать его по названию `connection_id`.

Для отправки запросов к API используем библиотеку `requests`.

Для начала необходимо создать соединение в Admin → Connection, название cur_scoop_conn_id:

В password передал API ключ

![image](https://github.com/user-attachments/assets/16233245-91ba-43bc-9442-8b4466e82ad5)

Код хука:

```
import requests
from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook

class CurrencyScoopHook(BaseHook):

    def __init__(self, currency_conn_id: str):
        super().__init__()
        self.conn_id = currency_conn_id

    def get_rate(self, date, base_currency: str, currency: str):
        url = 'https://api.currencybeacon.com/v1/historical'
        params = {
            'base': base_currency.upper(),
            'symbols': currency.upper(),
            'api_key': self._get_api_key(),
            'date': str(date),
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()['response']['rates'][currency]

    def _get_api_key(self):
        conn = self.get_connection(self.conn_id)
        if not conn.password:
            raise AirflowException('Missing API key (password) in connection settings')
        return conn.password
```

Единственный параметр, который принимает класс `CurrencyScoopHook` при инициализации — `currency_conn_id`. У класса есть 1 публичный метод — `get_rate`, он возвращает стоимость `base_currency` в валюте currency на момент даты `date`.

# **Создание своего оператора**

Чтобы создать свой оператор необходимо наследоваться от базового класса `BaseOperator`:

```
from airflow.models.baseoperator import BaseOperator

class CurrencyScoopOperator(BaseOperator):
    pass
```

Все стандартные операторы Airflow учитывают параметры DAG в котором они вызываются. Ранее я уже писал о том, что настройки в `default_args`, передаваемые инстансу DAG, наследуется всеми операторами. Чтобы сохранить такое поведение, необходимо метод `__init__` оператора обернуть в декоратор `apply_defaults`:

```
from airflow.utils.decorators import apply_defaults
from airflow.models.baseoperator import BaseOperator

class CurrencyScoopOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            base_currency: str,
            currency: str,
            conn_id: str = 'currency_scoop_conn_id',
            **kwargs) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.base_currency = base_currency
        self.currency = currency
```

Оператор дополнительно будет принимать 3 аргумента:

`base_currency` — базовый код валюты

`currency` — валюта в которой отражается стоимость базовой

`conn_id`— ключ к настройкам доступа

Логику работы оператора необходимо описать в методе `execute`, который принимает всего 1 аргумент — контекст.

Полный код оператора:

```
from typing import Any

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from .hook import CurrencyScoopHook

class CurrencyScoopOperator(BaseOperator):

    @apply_defaults
    def __init__(
            self,
            base_currency: str,
            currency: str,
            conn_id: str = 'currency_scoop_conn_id',
            **kwargs) -> None:
        super().__init__(**kwargs)
        self.conn_id = conn_id
        self.base_currency = base_currency
        self.currency = currency

    def execute(self, context: Any):
        api = CurrencyScoopHook(self.conn_id)
        return api.get_rate(context['execution_date'].date(), self.base_currency, self.currency)
```

Контекст нам нужен для получения даты выполнения DAGа. В методе `execute` мы создаём инстанс нашего `Hook` и вызываем метод получения курса валюты. Напомню, что если метод `execute` у оператора возвращает значение, оно автоматически записывается в `XCom`.

# **Сборка DAG**

Теперь у нас есть всё, чтобы сделать полноценный DAG для ежедневной загрузки курсов валют в базу. Убедится, что вы прописали соединение (postgres_default) в Admin → Connections и ваша база данных доступна.

Код DAGа:

```
from datetime import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from .operator import CurrencyScoopOperator

with DAG(
        dag_id='exchange_rate_usd_kzt_dag',
        start_date=datetime(2021, 3, 1),
        schedule_interval='@daily',
) as dag:

    create_table = PostgresOperator(
        task_id='create_table_task',
        sql='sql/create_table.sql',
        postgres_conn_id='postgres_default',
    )

    get_rate = CurrencyScoopOperator(
        task_id='get_rate',
        base_currency='USD',
        currency='KZT',
        conn_id='cur_scoop_conn_id',
        dag=dag,
        do_xcom_push=True,
    )

    insert_rate = PostgresOperator(
        task_id='insert_rate',
        postgres_conn_id='postgres_default',
        sql='sql/insert_rate.sql',
        params={
            'base_currency': 'USD',
            'currency': 'KZT',
        }
    )

    create_table >> get_rate >> insert_rate
```
А теперь взглянем на это в действии.

