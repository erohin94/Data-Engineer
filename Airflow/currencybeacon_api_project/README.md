

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

