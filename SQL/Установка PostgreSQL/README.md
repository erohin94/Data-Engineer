## Установка PostgreSQL

1. Создать файл docker-compose.yaml. С необходимыми настройками.

```
services:
  my_postgres:
    image: postgres:15
    restart: always
    container_name: my_postgres_db
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: 1
      POSTGRES_DB: postgres
    ports:
      - "5423:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    extra_hosts:
      - "host.docker.internal:host-gateway"
      

volumes:
  postgres_data:
```

3. Открыть Docker Desktop.

4. Открыть CMD терминал и перейти в папку с проектом где лежит docker-compose.yaml.

5. Запустить Docker Compose
Для запуска используем команду в терминале CMD:

```
docker-compose up -d
```

![image](https://github.com/user-attachments/assets/9a359dbe-0907-4568-89b8-e362ad6139cd)

## Подключение к контейнеру PostgreSQL через терминал:

Чтобы подключиться к PostgreSQL внутри контейнера, выполнить следующую команду:

`docker exec -it postgres psql -U test -d postgres`

![image](https://github.com/user-attachments/assets/9d0bce95-20e6-4899-bd15-5b36e9f77b38)

Теперь можно создавать таблицы, писать запросы прямо втерминале.

![image](https://github.com/user-attachments/assets/6e6c0baf-b529-4239-b8ea-d00d32fb0bb3)

Проверка созданной таблицы

```
\dt
```

Проверка структуры таблицы

```
\d launches
```

Чтобы выйти из сессии PostgreSQL, выполнить команду:

```
\q
```

## Подключение к БД с помощью python

```
import psycopg2
from psycopg2 import sql

# Параметры подключения
dbname = 'postgres'
user = 'test'
password = '1'
host = 'localhost'  # Это может быть '127.0.0.1', если localhost не работает
port = '5432'

try:
    # Установить подключение
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    
    # Создать курсор
    cursor = connection.cursor()
    
    # Пример запроса (получение данных из таблицы users)
    cursor.execute("SELECT * FROM users;")
    
    # Получить все строки
    rows = cursor.fetchall()
    
    print("Таблица users:")
    for row in rows:
        print(f"id: {row[0]}, name: {row[1]}, email: {row[2]}")
    
    # Пример запроса (вставка новой записи)
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s);", ("David", "david@example.com"))
    connection.commit()  # Подтверждаем изменения
    
    print("Новая запись добавлена в таблицу users.")

    # Закрыть курсор
    cursor.close()
    
except Exception as e:
    print(f"Ошибка при подключении или выполнении запроса: {e}")
    
finally:
    # Закрыть соединение
    if connection:
        connection.close()
```

Выполнив код увидим что все работает.

![image](https://github.com/user-attachments/assets/5e118d18-0b34-4eb8-971d-25f870ff97b0)

Структура папок

![image](https://github.com/user-attachments/assets/5a3b8d40-8aab-4065-a894-38aa1659a85f)

## Дополнительные шаги (при необходимости):

Проверка контейнера: Если нужно убедиться, что контейнер работает и слушает порт:

```
docker ps
```

Проверка логов контейнера: Если что-то пошло не так, можно просмотреть логи контейнера PostgreSQL:

```
docker logs postgres
```

## Подключение через DBeaver

![image](https://github.com/user-attachments/assets/78d24903-bd61-4a67-82ac-a51d693641bb)

Увидим созданную ранее в контейнере БД postgre и тестовые данные которыми наполнили.

![image](https://github.com/user-attachments/assets/69a221a3-3e6b-4708-9bdb-ce976636ab68)
