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
