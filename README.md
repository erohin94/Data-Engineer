# Data-Engineer

**Запуск и настройка Postgresql и Clickhouse**

1. Для начала создадим файл docker-compose.yml. С необходимыми настройками.

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
      

  clickhouse:
    image: yandex/clickhouse-server:latest
    restart: always
    container_name: clickhouse
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - ./clickhouse_data:/var/lib/clickhouse
      


volumes:
  postgres_data:
  clickhouse_data:
```

Этот файл как раз и позволит запустить 2 контейнера: один с PostgreSQL, а другой с ClickHouse.

2. Открыть Docker Desktop.

3. Открыть CMD терминал и перейти в папку с проектом где лежит docker-compose.yml.

4. Запустить Docker Compose
Для запуска используем команду в терминале CMD:

```
docker-compose up -d
```
