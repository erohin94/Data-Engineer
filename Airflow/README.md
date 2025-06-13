# **Установка**

Дока https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Установить и запустить Airflow можно разными способами,но для удобства буду использовать docker compose из официальной документации Airflow.

Для развертывания Apache Airflow с использованием docker compose, нужно выполнить несколько подготовительных шагов, включая настройку папок, скачивание и конфигурирование файла docker-compose.yaml, а также инициализацию и запуск Airflow. Так вкратце выглядит путь, который предстоит пройти.

**Шаг 1: Подготовка структуры папок**

- Создать  главную папку для проекта `Airflow`. Например, `airflow_project`
- Внутри этой папки создать три подпапки: `dags`, `logs`, и `plugins`

**Шаг 2:  Скачивание docker-compose.yaml**

Необходимо скачать файл `docker-compose.yaml` с официального сайта Apache Airflow по ссылке :
https://airflow.apache.org/docs/apache-airflow/2.9.2/docker-compose.yaml и поместить его в папку `airflow_project`.

Копируем весь текст из этой ссылки и вставлем в блокнот который создали в папке.
Меняем расширение у блокнота c txt на yaml. Получаем файл `docker-compose.yaml`

Должно получиться вот так:

![image](https://github.com/user-attachments/assets/294896ad-6630-41f3-97e5-e9f4b063ad84)

Теперь открываем этот файл и находим 62 строку. Меняем в ней значение параметра с 'true' на 'false' и нажимаем кнопку Сохранить:

![image](https://github.com/user-attachments/assets/1902507f-b1fc-465c-9405-a3e7358209f9)

Этот параметр отвечает за загрузку разных примеров DAG при запуске Airflow. Это несомненно полезно, но только когда видишь Airflow не в первый раз. Всегда можно включить этот параметр и посмотреть на те примеры, которые сделали сами создатели Airflow.

**Шаг 3: Инициализация Airflow**
- Открываем Docker Desctop
- Заходим в папку  `airflow_project` кликаем правой кнопкой мыши и выбираем пункт меню Открыть в терминале и в открывшемся терминале выполняем команду:

Linux:

`sudo docker-compose up airflow-init`

Windows (выполняем в PowerShell либо Git Bash):

`docker-compose up airflow-init`

Это необходимо для инициализации, а так же, как пишут в официальной документации, "чтобы запустить миграцию базы данных и создать первую учетную запись пользователя".

- Дождаться окончания процесса инициализации, который настроит служебную базу данных и создаст необходимые таблицы.(В качестве служебных БД в Airflow используется PostgreSQL и не только - это будет видно в процессе выполнения команды).

Успешное завершение выглядит так:

![image](https://github.com/user-attachments/assets/2a579f1d-aa96-4669-94cb-3c5fcedf7749)

**Шаг 4: Запуск Airflow**

- После успешной инициализации запуститьь Airflow выполнив в терминале команду:

Linux:

`sudo docker-compose up -d `

Windows:

`docker-compose up -d`

Подождать, пока все сервисы будут запущены.

Чтобы увидеть интерфейс Airflow открыть браузер и перейти по адресу http://127.0.0.1:8080/

Если все прошло по плану, то появится окно для ввода имени пользователя и пароля. Вводим в оба окошка airflow и подтверждаем. Перед нами открывается основное окно инструмента:

![image](https://github.com/user-attachments/assets/aa337c6c-7bbe-4483-89f6-bf1bf83ef6d0)

На этом установка закончена - переходим к использованию!

Дополнительно, для тех кто все установил Docker Desktop, обращаю внимание на то, как выглядит запущенный compose в Docker Desktop. Можно увидеть все запущенные контейнеры, описанные в файле:

![image](https://github.com/user-attachments/assets/76328688-c846-48b1-ab0d-e19b9b8da55f)

# **Заметки**

**Как подключится к PostgreSQL через Ui Airflow?**

Была проблема с подключением через UI Airflow(Admin-Connections) к бд PostgreSQL.

В .yaml файле для airflow не был указан порт для postgresql (База для логов).

В результате чего я не мог подключится к БД из dbvear и ui airflow

*Так как:*

-Внутри контейнера PostgreSQL всегда работает на стандартном порту 5432 (если не изменено в конфигурации).

-На хосте (Мой компьютер) порт не проброшен (нет ports: в конфигурации).

`Host (хост)`: postgres (имя сервиса в docker-compose.yml)

`Port (порт)`: 5432 (стандартный порт внутри контейнера)

В .yaml для Airflow прописал порты и заработало

![1](https://github.com/user-attachments/assets/b8032d18-2b3e-42bc-a6f7-ebe0f05865aa)

В conection прописал следующее

![2](https://github.com/user-attachments/assets/64e435a7-b7a9-4a41-9e78-70432eb0a2f6)

dbvear

![image](https://github.com/user-attachments/assets/9d447bfe-4f90-480c-aa53-eb3358fbdc6c)

-------------------------------------------------------------------------

**Не мог так же подключится к БД postgre которая создана в другом .yml файле из UI Airflow. Даг падал в ошибку**

Есть [.yml](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/docker-compose.yml) файл с PostgreSQL и [.yaml](https://github.com/erohin94/Data-Engineer/blob/main/Airflow/docker-compose.yaml) файл с Airflow

Пример струткуры папок:

```
DE/                     
├── Programs_installation/
│   ├── ClickHouse
│         └── ..............
│   ├── Postgre          
│         └── docker-compose.yml #Докер файл с PostgreSQL
│
├── Airflow_project/
│   ├── dags
│   ├── logs
│   ├── plugins
│         └── docker-compose.yaml #Докер файл с Airflow
```

Была так же проблема с подключением из UI Airflow

Причины и решение:

1. Разные сети Docker
   
По умолчанию каждый docker-compose создаёт свою собственную сеть. Контейнеры из разных файлов не видят друг друга.

Решение:

Создать общую сеть в обоих файлах. В обоих docker-compose файлах добавить:

```
networks:
  default:
    name: my_shared_network
    external: true
```

2. Использовать host.docker.internal (для Mac/Windows):

В конфиге my_postgres добавить:

```
extra_hosts:
  - "host.docker.internal:host-gateway"
```

Тогда в Airflow UI Connections указать Host: host.docker.internal, Port: 5423

Пошел по второму пути, как в пункте 2. 

Пример настроек в UI Airflow

![3](https://github.com/user-attachments/assets/2c82fc68-5c84-446f-9982-9ce6f6bb5a73)

.yml файл с PostgreSQL, так же внимание проброшенные порты

![4](https://github.com/user-attachments/assets/6103acc3-beb5-464c-94eb-84c5800b7eee)

-------------------------------------------------------------------------

**Про хост и порт**

Что такое host и port в Docker

*Хост (host)* — это "машина", на которой работает сервис:

-localhost — мой ПК (host-машина).

-container_name или имя сервиса из docker-compose.yml — внутри Docker-сети.

*Порт (port)* — номер канала, по которому клиент подключается к сервису.

Например:

5432 — стандартный порт PostgreSQL.

8080 — часто используется для веб-интерфейсов.

-------------------------------------------------------------------------

*Как работают хост и порт в Docker на локальном компьютере*

Когда запускаем PostgreSQL (или любой другой сервис) в Docker, важно понимать три уровня адресации:

1.Внутри контейнера 

Сервис (например, PostgreSQL) всегда работает на своём стандартном порту (5432 для Postgres).

Хост внутри контейнера: localhost (но только для этого контейнера).

2.В сети Docker (между контейнерами) (несколько сервисов в yaml фале)

Контейнеры могут общаться по имени сервиса (из docker-compose.yml) или имени контейнера.

Пример: если есть сервис my_postgres, другие контейнеры могут подключиться к нему по адресу:

```
Host: my_postgres  
Port: 5432
Docker автоматически резолвит имена через внутренний DNS.
```

3.На локальном компьютере (host-машине)

Чтобы подключиться к контейнеру с моего ПК (не из Docker), нужно:

Пробросить порт через ports: в docker-compose.yml.

Использовать localhost (или 127.0.0.1) и внешний порт.

Примеры из конфигов

```
1. Для логов Airflow (первый контейнер)
yaml
services:
  postgres:
    image: postgres:13
    ports:
      - "5432:5432"  # Проброс порта: хост_порт_пк:контейнер_порт

Подключение из другого контейнера (если несколько сервисов в .yaml файле):
postgres:5432

Подключение с локального ПК:
localhost:5432
```

```
2. Для моей БД (второй контейнер)
yaml
services:
  my_postgres:
    image: postgres:15
    ports:
      - "5423:5432"  # Внутри контейнера — 5432, снаружи — 5423

Подключение из другого контейнера (если несколько сервисов в .yaml файле):
my_postgres:5432

Подключение с локального ПК:
localhost:5423
```

# **Пример 1**

.yaml файл с Airflow в котором есть служебная БД Postgres для логов.

![image](https://github.com/user-attachments/assets/f3b7d3ed-2444-41f9-802c-9d9e2d2dbd82)

Когда подключаюсь с наружи с моего ПК к контейнеру то прописываю следующие настройки.

```
ports:
      - "5432:5432"  # Снаружи (localhost) — 5432, внутри контейнера — 5432
```

Тоесть 5432 (слева-снаружи) это номер канала, по которому клиент (в данном случае мой ПК - приложение dbvear - (Хост - localhost)) подключается к сервису.

![image](https://github.com/user-attachments/assets/92323751-4881-47a4-9561-b44f3efc43f1)

------------------------------------

Когда подключаюсь в сети Docker (между контейнерами) (несколько сервисов в yaml фале), тоесть Airflow к сервису Postgre то прописываю следующие настройки.

Обращаюсь по имени сервиса `postgres`.

![image](https://github.com/user-attachments/assets/3657d438-8432-43c5-8d82-5299d63248b1)

# **Пример 2**

Подключение к контейнеру с моего ПК (не из Docker)

![image](https://github.com/user-attachments/assets/2ba4f65a-41e2-42f0-918d-ef5fd7b55e7e)

В настройках прописываю

```
ports:
      - "5423:5432"  # Снаружи (localhost) — 5423, внутри контейнера — 5432
```

Тоесть 5423 это номер канала, по которому клиент (в данном случае мой ПК - приложение dbvear) подключается к сервису. А там его ждёт PostgreSQL.

DBeaver стучится в localhost:5423. Docker получает этот запрос и перенаправляет его внутрь контейнера на порт 5432,
где работает PostgreSQL и слушает подключения.

![image](https://github.com/user-attachments/assets/1cfb17d2-ed48-49e5-a2ad-bb946f24fd94)

Подключение к контейнеру из другого контейнера, указал сеть по которой подключаюсь

![image](https://github.com/user-attachments/assets/1f823e4a-14ab-46f5-9867-a3b61fe8b33e)





