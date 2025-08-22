# Установка HDFS через Docker

**Склонировать проект:**

`git clone https://github.com/big-data-europe/docker-hive.git`

![image](https://github.com/user-attachments/assets/68d67b3e-174d-4693-af64-0cef1fbbab1c)

**Перейти в папку с проектом:**

`cd docker-hive`

![image](https://github.com/user-attachments/assets/ff6600cd-4d78-4bd7-a6b3-9156505b13aa)

**Запустить Docker образ:**

`docker-compose up -d`

После успешного запуска, получим сообщение:

![image](https://github.com/user-attachments/assets/5de27163-1df4-4d8e-9e03-2b804689e7e3)

Далее необходимо залезть в контейнер и поработать с hdfs.

Посмотрим список процессов командой `docker ps`:

![image](https://github.com/user-attachments/assets/1b790337-9029-4fe2-8264-12087cba8a60)

Далее ищем контейнер с названием docker-hive-namenode-1. Вводим следующую команду, чтобы туда провалиться:

`docker exec -it docker-hive-namenode-1 /bin/bash`

![image](https://github.com/user-attachments/assets/dea99366-f130-49ef-a1b5-a6769a1f8427)

![image](https://github.com/user-attachments/assets/dfe55daf-d23c-45a7-9fe3-1cb1968eaf8f)

Теперь мы в HDFS. Чтобы проверить это, вводим команду:

`hadoop version`

![image](https://github.com/user-attachments/assets/a4152183-b6c0-478e-bb95-2a043d0867b1)

Так же если ввести команду:

`hdfs dfsadmin -report`

Увидим:

![image](https://github.com/user-attachments/assets/086259dd-5a27-4f5e-a82c-6302f59b3c35)

Команда `hdfs dfsadmin -report` используется в Hadoop для получения сводной информации о состоянии кластера HDFS (Hadoop Distributed File System). Она позволяет администраторам системы видеть статистику и состояние файловой системы.

# Команды 

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

Configured Capacity — общая ёмкость всех DataNode, доступная в HDFS (сумма всех дисковых пространств).

Present Capacity — доступная ёмкость HDFS с учетом зарезервированного пространства.

DFS Remaining — оставшееся свободное пространство на всех DataNode.

DFS Used — пространство, которое используется для хранения данных в HDFS.

DFS Used% — процент использования пространства в HDFS.

Under replicated blocks — количество блоков, у которых недостаточно реплик.

Blocks with corrupt replicas — количество блоков с повреждёнными репликами.

Missing blocks — количество блоков, которые отсутствуют в кластере (потерянные данные).

Live datanodes — количество активных (доступных) DataNode.

Dead datanodes — количество DataNode, которые не в сети или не отвечают.

Name и Hostname — IP-адрес и имя хоста DataNode.

Decommission Status — статус DataNode (например, Normal или Decommissioned, если DataNode выведен из эксплуатации).

Configured Capacity, DFS Used, DFS Remaining — ёмкость, используемое и оставшееся пространство на DataNode.

DFS Used%, DFS Remaining% — процентное использование и оставшееся пространство.

Last contact — время последнего контакта с DataNode.

Итого файлы подкладывать научились, реплики менять тоже научились. Но, вот правда не узнали где они все таки лежат. Для этого используем следующую команду:

`hdfs fsck /test1/localfile_renamed.txt -files -blocks -locations`

Но, поскольку у нас одна реплика, то вывод будет следующий.

![image](https://github.com/user-attachments/assets/63197ff7-31a0-40a4-b695-0cd4d2d17633)

Изменим репликацию этого файла на 3 и снова повторим эту команду.

`hdfs dfs -setrep 3 /test1/localfile_renamed.txt`

`hdfs fsck /test1/localfile_renamed.txt -files -blocks -locations`

![image](https://github.com/user-attachments/assets/d6c885d2-3b71-466e-a2dc-83b125323af8)

И все равно мы видим, что в колонке missing replicas у нас 2 блока. Почему? По правилам в ЛУЧШЕМ случае у нас должно быть сколько блоков, столько дата нод. Конечно, мы не можем разместить 3 реплики на одной дата ноде. Но, что если файл 256 Гб весит, а одна реплика 128 Мб? Все просто - меняется конфигурация при загрузке файла в HDFS, но это уже совсем другая история :)
