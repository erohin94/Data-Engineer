import requests
from requests.auth import HTTPBasicAuth

# URL для создания переменной
url = 'http://127.0.0.1:8080/api/v1/variables'

# Параметры запроса
headers = {'Content-Type': 'application/json'}
data = {
    'key': 'my_variable',
    'value': 'my_value'
}

#Используется Basic Auth, нужно будет передавать логин и пароль в заголовке каждого запроса.

username = 'airflow'
password = 'airflow'

# Отправка POST-запроса для создания переменной
response = requests.post(url, headers=headers, json=data, auth=HTTPBasicAuth(username, password))

# Проверка статуса ответа
if response.status_code == 200:
    print('Переменная успешно создана')
else:
    print('Ошибка при создании переменной:', response.status_code)
