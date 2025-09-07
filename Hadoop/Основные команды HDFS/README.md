# Содержание 

-[Команды](#Команды)

-[Как запускать bash скрипты](#Как-запускать-bash-скрипты)

-[Добавление дата нод](#Добавление-дата-нод)

-[Загрузка большого файла в 3 датаноды](#Загрузка-большого-файла-в-3-датаноды)

-[Заметки](#Заметки)

## Команды 

Другие команды, как провалится в котейнер смотри тут [ссылка](https://github.com/erohin94/Data-Engineer/tree/main/Hadoop/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0)

`hdfs dfs` может применяться только в HDFS, а команды `hadoop fs` — это универсальная команда файловой системы. Она может работать как с HDFS, так и с другими файловыми системами, поддерживаемыми Hadoop (например, локальной файловой системой или S3).

**Команды**

Создать папки:

`hdfs dfs -mkdir /test1`

![image](https://github.com/user-attachments/assets/c9a40bb5-173a-4e9d-adbc-ec530c246df1)

Посмотреть что создали:

`hdfs dfs -ls /`

![image](https://github.com/user-attachments/assets/7daa56e9-f9e6-4fdb-8ede-6203ab1e152a)

Команды в HDFS предназначены для выполнения одной операции за один раз (например, ls, put, get). Эти команды подключаются к HDFS, выполняют операцию и завершаются. 

В HDFS нет команды, аналогичной touch в локальных файловых системах, для создания пустого файла. В HDFS нельзя просто создать пустой файл, как это делается с помощью touch в Unix-подобных системах. HDFS ориентирован на хранение больших объемов данных, и концепция пустых файлов не так важна для распределенной файловой системы.

Но, поскольку HDFS у нас располагается в Docker, то алгоритм будет выглядеть следующим образом:

-Создать файл локально (на своем рабочем компьютере)

-Перенести его в файловую систему докера (ничего перезапускать не нужно будет)

-Перенести из файловой системы докера в HDFS

Создадим рандомный файл в файловой системе и заполним его любой информацией. Сделать это очень просто и можно использовать UI. В моем случае это будет VsCode.

![image](https://github.com/user-attachments/assets/e3e07f48-19b1-4bfb-9e0b-13ce2062073b)

Открыть еще один терминал и ввести команду (В первом терминале запущен HDFS):

Сначала перейти в папку с проектом `cd Desktop\hdfs`

Посмотерть контейнеры: `docker ps`

Ввести команду: `docker cp localfile.txt ed770a67d0c6:/tmp/localfile.txt`

Откуда я взял ed770a67d0c6? Это нейм нода Hadoop.

![image](https://github.com/user-attachments/assets/f3c5b102-56e0-481a-8a1c-f9007ad4bcef)

Вернемся в другой терминал в котором открыт HDFS. 

Вводим следующую команду. Команда `put` копирует файл или директорию из локальной файловой системы в HDFS. Она похожа на команду `cp` в Unix-подобных системах, но работает между локальной файловой системой и HDFS.

`hdfs dfs -put /tmp/localfile.txt /test1/localfile.txt`

![image](https://github.com/user-attachments/assets/c2774927-8a55-41d0-8806-518b917cbfe4)

Проверим, а действительно ли файл оказался в HDFS:

`hdfs dfs -ls /test1/`

![image](https://github.com/user-attachments/assets/34f9e0c1-2691-4f7d-9b4a-8065fa6d20c6)

Размер не нулевой, это уже радует. Как посмотреть содержимое файла? 

Используем cat и указываем тот файл, который хотели бы посмотреть.

`hdfs dfs -cat /test1/localfile.txt`

![image](https://github.com/user-attachments/assets/625ae5b9-310b-4c53-bb27-b7d47fafc75a)

*Чтобы не вбивать команды в ручную а копировать и вставлять в терминал, использовать сочетание клавиш CTRL+SHIFT+V*

Ровно также, как и в Linux файл можно перемещать и копировать. Например введем следующую команду.

Чтобы выйти из строки `Тестовый текст для HDFSroot@ed770a67d0c6:/#` Нажать ENTER и вводить команды ниже:

`hdfs dfs -cp /test1/localfile.txt /test1/localfile_copy.txt`

`hdfs dfs -ls /test1/`

![image](https://github.com/user-attachments/assets/279875dc-822a-4b0c-88bf-4900728975c3)

Ровно также будут работать и `mv`, как с точки зрения перемещения, так и с точки зрения переименовывания. Видим, что благодаря примеру, ниже файл поменял свое название.

`hdfs dfs -mv /test1/localfile.txt /test1/localfile_renamed.txt`

`hdfs dfs -ls /test1/`

![image](https://github.com/user-attachments/assets/3e264e26-8839-4ecb-b8a1-f9a8d5907faf)

Аналогично Linux будет работать и команда `rm`: 

`hdfs dfs -rm /test1/localfile_copy.txt`

![image](https://github.com/user-attachments/assets/9bceac92-b86e-43a7-a550-d9e7f14ba43d)

![image](https://github.com/user-attachments/assets/723a212d-d9ca-48d0-b102-5b12394248b5)

Но... Что с репликами? Познакомимся с очень важной командой в HDFS - `stat`. Команда `hdfs dfs -stat` в HDFS используется для получения информации о файле или директории. Выглядит вот так в общем случае:

`hdfs dfs -stat [формат] [путь_к_файлу]`

`%b` — размер файла в байтах.

`%y` — время последней модификации файла (формат даты).

`%n` — имя файла.

`%o` — права доступа к файлу (в формате rwx).

`%r` — количество реплик файла.

`%u` — владелец файла.

`%g` — группа файла.

Ставятся в формате, как в примере ниже. В данном случае у нас 3 реплики файла (такая конфигурация), а также пользователь - root.

`hdfs dfs -stat "%r %u" /test1/localfile_renamed.txt`

![image](https://github.com/user-attachments/assets/70313c51-7193-4cfa-bfe6-b06a5a250722)

Можно ли изменять количество реплик? Можно. Но не нужно. Потому что HDFS неспроста называют отказоустойчивой. Ведь благодаря фактору репликации мы можем делать копии файла. Но, поскольку команда такая есть - мы на нее смотрим:

`hdfs dfs -setrep 1 /test1/localfile_renamed.txt`

`hdfs dfs -stat "%r %u" /test1/localfile_renamed.txt`

![image](https://github.com/user-attachments/assets/9b81b9e8-5f3e-4b65-9bec-bf7f80f5ced6)

Команда `hdfs dfsadmin -report` в HDFS используется для получения отчёта о состоянии распределённой файловой системы Hadoop (HDFS). Она выводит информацию о всём кластере HDFS, включая статистику использования пространства, состояние DataNode, а также метаданные о блоках и репликации.

![image](https://github.com/user-attachments/assets/b650486c-b164-4aa3-9663-e8b3a6e75f45)

Cверху вниз пояснение.

`Configured Capacity` — общая ёмкость всех DataNode, доступная в HDFS (сумма всех дисковых пространств).

`Present Capacity` — доступная ёмкость HDFS с учетом зарезервированного пространства.

`DFS Remaining` — оставшееся свободное пространство на всех DataNode.

`DFS Used` — пространство, которое используется для хранения данных в HDFS.

`DFS Used%` — процент использования пространства в HDFS.

`Under replicated blocks` — количество блоков, у которых недостаточно реплик.

`Blocks with corrupt replicas` — количество блоков с повреждёнными репликами.

`Missing blocks` — количество блоков, которые отсутствуют в кластере (потерянные данные).

`Live datanodes` — количество активных (доступных) DataNode.

`Dead datanodes` — количество DataNode, которые не в сети или не отвечают.

`Name и Hostname` — IP-адрес и имя хоста DataNode.

`Decommission Status` — статус DataNode (например, Normal или Decommissioned, если DataNode выведен из эксплуатации).

`Configured Capacity, DFS Used, DFS Remaining` — ёмкость, используемое и оставшееся пространство на DataNode.

`DFS Used%, DFS Remaining%` — процентное использование и оставшееся пространство.

`Last contact` — время последнего контакта с DataNode.

Итого файлы подкладывать научились, реплики менять тоже научились. Но, вот правда не узнали где они все таки лежат. Для этого используем следующую команду:

`hdfs fsck /test1/localfile_renamed.txt -files -blocks -locations`

Но, поскольку у нас одна реплика, то вывод будет следующий.

![image](https://github.com/user-attachments/assets/63197ff7-31a0-40a4-b695-0cd4d2d17633)

Изменим репликацию этого файла на 3 и снова повторим эту команду.

`hdfs dfs -setrep 3 /test1/localfile_renamed.txt`

`hdfs fsck /test1/localfile_renamed.txt -files -blocks -locations`

![image](https://github.com/user-attachments/assets/d6c885d2-3b71-466e-a2dc-83b125323af8)

И все равно мы видим, что в колонке missing replicas у нас 2 блока. Почему? По правилам в ЛУЧШЕМ случае у нас должно быть сколько блоков, столько дата нод. Конечно, мы не можем разместить 3 реплики на одной дата ноде. Но, что если файл 256 Гб весит, а одна реплика 128 Мб? Все просто - меняется конфигурация при загрузке файла в HDFS, но это уже совсем другая история :)


## Как запускать bash скрипты

Посчитаем размер для нашей папки test1.

Создадим скрипт `sh` в `VsCode`, назовем его `calculate_hdfs_directory_size.sh` и наполним его кодом:

```
#!/bin/bash

HDFS_DIRECTORY="/test1"

DIRECTORY_SIZE=$(hdfs dfs -du -s $HDFS_DIRECTORY | awk '{print $1}')

HUMAN_READABLE_SIZE=$(hdfs dfs -du -s -h $HDFS_DIRECTORY | awk '{print $1}')

# Вывод результата
echo "Размер директории $HDFS_DIRECTORY: $DIRECTORY_SIZE байт"
echo "Человекочитаемый размер директории $HDFS_DIRECTORY: $HUMAN_READABLE_SIZE"
```
<img width="1309" height="427" alt="image" src="https://github.com/user-attachments/assets/3f7fd1a0-b4c2-4e1c-8c59-09023a88d4e6" />

Открываем отдельный терминал, в другом запущен докер.

<img width="1778" height="237" alt="image" src="https://github.com/user-attachments/assets/fae64f51-10f4-48b2-a970-f6f1ed4bfa94" />

Далее мы перенесем этот скрипт в Docker.

`docker cp calculate_hdfs_directory_size.sh 393bcc0012d8:/tmp/calculate_hdfs_directory_size.sh`

<img width="1084" height="38" alt="image" src="https://github.com/user-attachments/assets/9a1a05cf-30ce-4347-b140-0f26f1cf75ea" />

Стоит ли его перекидывать в HDFS? Нет. Проверим его наличие в Docker.

`docker exec -it 393bcc0012d8 ls /tmp/calculate_hdfs_directory_size.sh`

<img width="950" height="113" alt="image" src="https://github.com/user-attachments/assets/ebfeada2-9f18-40e8-b1e2-a022f3c7f40c" />

А далее остается сделать его исполняемым и запустить.

`docker exec -it 393bcc0012d8 chmod +x /tmp/calculate_hdfs_directory_size.sh`

<img width="951" height="90" alt="image" src="https://github.com/user-attachments/assets/8c7cef8d-fde7-4463-82a7-3ceeddc60103" />

И наконец, запустить скрипт

`docker exec -it 393bcc0012d8 /tmp/calculate_hdfs_directory_size.sh`

<img width="983" height="122" alt="image" src="https://github.com/user-attachments/assets/5e7a5b20-6efb-48bd-a80e-9e7687c1bc46" />

## Добавление дата нод

А что если...мы создадим еще дата нод? Чтобы посмотреть на то, как происходит репликация... Для этого изменим конфиг docker-compose на следующий

```
version: "3"

services:
  namenode:
    image: bde2020/hadoop-namenode:2.0.0-hadoop2.7.4-java8
    volumes:
      - namenode:/hadoop/dfs/name
    environment:
      - CLUSTER_NAME=test
    env_file:
      - ./hadoop-hive.env
    ports:
      - "50070:50070"

  datanode1:
    image: bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8
    volumes:
      - datanode1:/hadoop/dfs/data
    env_file:
      - ./hadoop-hive.env
    environment:
      SERVICE_PRECONDITION: "namenode:50070"
    ports:
      - "50075:50075"

  datanode2:
    image: bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8
    volumes:
      - datanode2:/hadoop/dfs/data
    env_file:
      - ./hadoop-hive.env
    environment:
      SERVICE_PRECONDITION: "namenode:50070"
    ports:
      - "50076:50075" # Порт изменен для уникальности

  datanode3:
    image: bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8
    volumes:
      - datanode3:/hadoop/dfs/data
    env_file:
      - ./hadoop-hive.env
    environment:
      SERVICE_PRECONDITION: "namenode:50070"
    ports:
      - "50077:50075" # Порт изменен для уникальности

  hive-server:
    image: bde2020/hive:2.3.2-postgresql-metastore
    env_file:
      - ./hadoop-hive.env
    environment:
      HIVE_CORE_CONF_javax_jdo_option_ConnectionURL: "jdbc:postgresql://hive-metastore/metastore"
      SERVICE_PRECONDITION: "hive-metastore:9083"
    ports:
      - "10000:10000"

  hive-metastore:
    image: bde2020/hive:2.3.2-postgresql-metastore
    env_file:
      - ./hadoop-hive.env
    command: /opt/hive/bin/hive --service metastore
    environment:
      SERVICE_PRECONDITION: "namenode:50070 datanode1:50075 datanode2:50075 datanode3:50075 hive-metastore-postgresql:5432"
    ports:
      - "9083:9083"

  hive-metastore-postgresql:
    image: bde2020/hive-metastore-postgresql:2.3.0

  presto-coordinator:
    image: shawnzhu/prestodb:0.181
    ports:
      - "8080:8080"

volumes:
  namenode:
  datanode1:
  datanode2:
  datanode3:
```
После того как изменил докер файл, выполняю команды

Пересобрать конфигурацию. Если контейнеры уже были запущены: `docker compose down`

Поднять новые сервисы: `docker compose up -d`

--------------------------------------------

*Были проблемы с перезапуском контейнера, клнфликт портов. Сделал `docker stop 26886381c2cb`, `docker rm 26886381c2cb`, `docker compose down` и `docker compose up -d`.*

--------------------------------------------
Запустим с такой конфигурацией. Помните, что у нас остались другие файлы, пока мы практиковались? Их можно удалять. Так как HDFS не умеет переносить на свежие датаноды реплики уже загруженного файла. Даже если мы сделаем команду 

`hdfs dfs -setrep 3 /test1/localfile_renamed.txt`

Не заработает! Проверим, введя команду

`hdfs fsck /test1/localfile_renamed.txt -files -blocks -locations`

<img width="1072" height="747" alt="Снимок экрана 2024-11-14 в 02 58 08" src="https://github.com/user-attachments/assets/c52dc326-f864-4900-834f-2c51b9882a24" />

Видим, что блоки потеряны (MISSING BLOCKS). Поэтому дропнем этот файл и закинем еще один (который на самом деле никуда не девался, он по прежнему находится в Docker, если Вы внимательно читали это руководство).

Итак, мы дропаем старый файл. Подкладываем с докера новый файл.

`hdfs dfs -put /tmp/localfile.txt /test1/localfile.txt`

--------------------------------------------

*Если не ищет файл*

1.Скопировать файл с хоста в контейнер. Сначала скопируй с хост-машины в контейнер namenode(в другом терминале где не запущен hdfs): `docker cp localfile.txt docker-hive-namenode-1:/tmp/localfile.txt`

<img width="871" height="43" alt="image" src="https://github.com/user-attachments/assets/febe4cf1-5d40-45c1-8a14-f897064ffec2" />

2.Затем уже в контейнере: `hdfs dfs -put /tmp/localfile.txt /test1/localfile.txt`

<img width="600" height="34" alt="image" src="https://github.com/user-attachments/assets/5b1a8a18-b5fc-4416-a605-2a9545912c42" />

--------------------------------------------

А далее смотрим где это все размазано

`hdfs fsck /test1/localfile.txt -files -blocks -locations`

Видим, что размазано по следующим датанодам 

[DatanodeInfoWithStorage[172.21.0.2:50010,DS-90c878d9-459e-44a4-ba94-07602152c7ab,DISK], 
DatanodeInfoWithStorage[172.21.0.5:50010,DS-a13fcb7a-d8d7-404b-9310-c56761ad1653,DISK], 
DatanodeInfoWithStorage[172.21.0.7:50010,DS-a079bc3c-0c2b-457f-bbed-e89814501837,DISK]]

Видим размер блока - len=39 и количество реплик repl=3

<img width="1890" height="459" alt="image" src="https://github.com/user-attachments/assets/75e843ed-8fef-4598-a21d-8dbfcbbc62f8" />

А теперь попробуем изменить фактор репликации на 2. И посмотреть сможет ли он убрать копию файла с какой-то дата ноды.

`hdfs dfs -setrep 2 /test1/localfile.txt`

<img width="512" height="74" alt="image" src="https://github.com/user-attachments/assets/e834cbe6-4d35-4e1f-ac03-fe78804a04c6" />

А теперь посмотрим на то, что происходит с датанодами - `hdfs fsck /test1/localfile.txt -files -blocks -locations`

<img width="1891" height="464" alt="image" src="https://github.com/user-attachments/assets/37a25cae-2e18-4594-a33e-5d23dfb7da25" />

Видим, что датанод у нас 3, а фактор репликации - 2. Поэтому 2 файла (которые в текущем случае являются не кусочками, а файлами) записывают на 2 дата ноды.

## Загрузка большого файла в 3 датаноды

Рассмотрим загрузку большого файла в 3 датаноды, чтобы понять, как происходит запись файла. Для этого возьмем датасет с яндекс диска - https://disk.yandex.ru/d/l4GbAIMPAUmClg

Сколько весит? Почти 3 Гб. Это минимально допустимый для больших данных размер.

Как всегда, добавим его в докер. Логично, что загрузка может занять некоторое время.

Файл расположен в следующем месте, соответственно надо перейти в папку где лежит файл и оттуда выполнять комнды.

<img width="636" height="148" alt="image" src="https://github.com/user-attachments/assets/4822d8e0-7862-49b1-9ec4-18d0e9e6fa10" />

Вводим команду `docker cp synthetic_fraud_data.csv 67baa2e87e1c:/tmp/synthetic_fraud_data.csv`

Ниже пример команд, если выполнять их не из той дирректории, указать не правильно нейм ноду и корректный запуск команды

<img width="1770" height="946" alt="image" src="https://github.com/user-attachments/assets/fff61f4e-a983-45d0-bd76-d341594c4b45" />

А далее перенесем внутрь HDFS. Запускать в терминале, где работате hdfs.

`hdfs dfs -put /tmp/synthetic_fraud_data.csv /test1/synthetic_fraud_data.csv`

<img width="776" height="19" alt="image" src="https://github.com/user-attachments/assets/a0e6515c-d765-4d98-92a2-23a842abfed8" />

*Разбор по частям: `hdfs dfs` — запускает утилиту работы с HDFS. `-put` — копирует файл из локальной файловой системы в HDFS. `/tmp/synthetic_fraud_data.csv` — путь к файлу на локальной машине (или внутри контейнера, если вы выполняете команду там). `/test1/synthetic_fraud_data.csv` — путь в HDFS, куда будет загружен файл.*

Итак, команда - `hdfs dfs -ls /test1/synthetic_fraud_data.csv`. Покажет нам размер. Проверим сначала его.

<img width="773" height="54" alt="image" src="https://github.com/user-attachments/assets/f5d99720-80b9-4118-94c5-823ef0e8f4a6" />

Видим размер в байтах, что соответствует заявленному размеру.

<img width="616" height="74" alt="image" src="https://github.com/user-attachments/assets/02957369-e83e-4759-9081-2717de5450fe" />

------------------------------

## Заметки

**1. Обьяснение команды `hdfs fsck /test1/localfile.txt -files -blocks -locations`**

**Что такое hdfs fsck** `fsck (file system check)` в HDFS — это утилита для проверки состояния файлов и блоков в файловой системе. Она не чинит файловую систему, а просто показывает диагностику (в отличие от fsck в Linux).

**Аргументы:**

`/test1/localfile.txt` → путь к конкретному файлу, который проверяем.

`files` → выводит список файлов, их размер и принадлежность блокам.

`blocks` → показывает, из каких блоков состоит файл, их ID и длину.

`locations` → дополнительно выводит список DataNode, где физически лежат копии каждого блока.

**2. Где вводить команду `cp` внутри hdfs или снаружи**

Когда перед `cp` пишем докер `docker cp` - то выполняется на твоём хосте (т.е. в терминале, где установлен Docker), а не внутри контейнера и не внутри HDFS.

Когда перед `cp` пишем hdfs dfs `hdfs dfs -cp` - то выполняется копирование файлов внутри самого HDFS. Это копия файла/директории внутри HDFS (аналог cp в Linux).

| Откуда                | Куда                   | Команда / Метод | Где выполняется         | Что делает                                                                                 | Пример                                                                              |
| --------------------- | ---------------------- | --------------- | ----------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| **Хост**              | **Контейнер**          | `docker cp`     | На хосте (терминал)     | Копирует файл с хоста внутрь контейнера или обратно                                        | `docker cp localfile.txt docker-hive-namenode-1:/tmp/localfile.txt`                 |
| **Контейнер**         | **Хост**               | `docker cp`     | На хосте (терминал)     | Копирует файл из контейнера на хост                                                        | `docker cp docker-hive-namenode-1:/tmp/localfile.txt ./localfile.txt`               |
| **Внутри контейнера** | **HDFS**               | `hdfs dfs -put` | В контейнере (namenode) | Загружает файл из файловой системы контейнера в HDFS                                       | `hdfs dfs -put /tmp/localfile.txt /test1/`                                          |
| **HDFS**              | **HDFS**               | `hdfs dfs -cp`  | В контейнере (namenode) | Копирует файл внутри HDFS (между директориями или создаёт дубликат)                        | `hdfs dfs -cp /test1/localfile.txt /test1/localfile_copy.txt`                       |
| **HDFS**              | **Хост / контейнер**   | `hdfs dfs -get` | В контейнере (namenode) | Копирует файл из HDFS в файловую систему контейнера/хоста                                  | `hdfs dfs -get /test1/localfile.txt /tmp/`                                          |
| **Хост / контейнер**  | **HDFS**               | `hdfs dfs -put` | В контейнере (namenode) | Загружает файл с хоста/контейнера в HDFS                                                   | `hdfs dfs -put /tmp/localfile.txt /test1/`                                          |
| **HDFS**              | **HDFS**               | `hdfs dfs -mv`  | В контейнере (namenode) | Перемещает или переименовывает файл внутри HDFS                                            | `hdfs dfs -mv /test1/file1.txt /test1/file_renamed.txt`                             |
| **Хост**              | **Контейнер с volume** | Через volume    | На хосте + контейнер    | Любой файл в примонтированной директории хоста автоматически виден в контейнере и наоборот | volume: `./data:/data` → файл `./data/file.csv` виден в контейнере `/data/file.csv` |


------------------------------
