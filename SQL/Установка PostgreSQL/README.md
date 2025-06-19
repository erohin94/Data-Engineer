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

**Подключение к контейнеру PostgreSQL через терминал:**

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
