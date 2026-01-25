Рабочая конфигурация Airflow + PostgreSQL с использованием PostgresHook, чтобы Airflow мог выполнять SQL-запросы к базе.


docker-compose.yaml

PostgreSQL и Airflow в одном docker-compose, на одной сети

Airflow будет видеть PostgreSQL по имени сервиса postgres

Пример DAG, использующий PostgresHook

```
version: "3.8"

services:
  postgres:
    image: postgres:15
    container_name: postgres_airflow
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: 1
      POSTGRES_DB: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "test"]
      interval: 10s
      retries: 5
      start_period: 5s

  airflow-webserver:
    image: apache/airflow:2.8.1
    container_name: airflow-webserver
    depends_on:
      - postgres
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://test:1@postgres:5432/postgres
      - AIRFLOW__DATABASE__SQL_ALCHEMY_POOL_ENABLED=False
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: webserver

  airflow-init:
    image: apache/airflow:2.8.1
    depends_on:
      - postgres
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://test:1@postgres:5432/postgres
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: db init

  airflow-scheduler:
    image: apache/airflow:2.8.1
    depends_on:
      - airflow-webserver
    environment:
      - AIRFLOW__CORE__EXECUTOR=LocalExecutor
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql+psycopg2://test:1@postgres:5432/postgres
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: scheduler

volumes:
  postgres_data:
```

Запуск

`docker-compose up airflow-init`

`docker-compose up -d`

Cоздать пользователя вручную

`docker-compose run airflow-webserver airflow users create --username airflow --password airflow --firstname Air --lastname Flow --role Admin --email airflow@example.com`

После запуска открыть http://localhost:8080, логин по умолчанию:

Login: airflow
Password: airflow
