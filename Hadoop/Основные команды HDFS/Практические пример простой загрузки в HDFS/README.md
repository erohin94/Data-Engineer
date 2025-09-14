## Простая загрузка в HDFS.

Необходимо

1. Создать директорию в HDFS.

2. Добавить 5 файлов в HDFS. 

3. Подсчитать количество файлов и занимаемое пространство.

4. Поставить квоту на 5 файлов для этой директории.


**1.Создание директории в HDFS.**

Открываем терминал и вводим команды

```
cd C:\Users\erohi\Desktop\hdfs\docker-hive

docker-compose up -d 

docker exec -it docker-hive-namenode-1 /bin/bash

hdfs dfs -mkdir /task1
```

<img width="1150" height="496" alt="image" src="https://github.com/user-attachments/assets/1abd9c8a-004d-43e1-bb15-3dc8509aef8d" />


**2.Добавдение 5 файлов в HDFS.**

Т.к HDFS у нас располагается в Docker, то алгоритм создания  и добавления файлов будет выглядеть следующим образом:

-Создать файл локально (на своем рабочем компьютере)

<img width="655" height="185" alt="image" src="https://github.com/user-attachments/assets/2d93ae09-45d0-42b4-8f17-c4f58d5f5b07" />

-Перенести его в файловую систему докера (ничего перезапускать не нужно будет)

Открыть еще один терминал и ввести команду:

Сначала перейти в папку с проектом `cd C:\Users\erohi\Desktop\hdfs`

Посмотерть контейнеры: `docker ps`

<img width="1730" height="202" alt="image" src="https://github.com/user-attachments/assets/1c09a8ae-4c44-4255-9770-a84a4e59c8f9" />

Ввести команду: `docker cp file1.txt 67baa2e87e1c:/tmp/file1.txt`

<img width="610" height="35" alt="image" src="https://github.com/user-attachments/assets/98349be7-8cb1-4579-b798-35c6304a3564" />

Откуда я взял 67baa2e87e1c? Это нейм нода Hadoop.

-Перенести из файловой системы докера в HDFS

Вернемся в другой терминал в котором открыт HDFS.

Вводим следующую команду. Команда put копирует файл или директорию из локальной файловой системы в HDFS.

`hdfs dfs -put /tmp/file1.txt /task1/file1.txt`

Проверим, а действительно ли файл оказался в HDFS:

`hdfs dfs -ls /task1/`

<img width="631" height="82" alt="image" src="https://github.com/user-attachments/assets/c7444666-71bf-4ec5-a3bf-e5c080b335a8" />

Размер не нулевой, это уже радует. Как посмотреть содержимое файла?

Используем `cat` и указываем тот файл, который хотели бы посмотреть.

`hdfs dfs -cat /task1/file1.txt`

<img width="436" height="32" alt="image" src="https://github.com/user-attachments/assets/df6b61cb-b9fa-4aaa-a29f-4eae9a73bde5" />

Для остальных файлов проделываем тоже самое

<img width="632" height="210" alt="image" src="https://github.com/user-attachments/assets/25edf059-68f0-4deb-b90b-35ab54b250f1" />

<img width="702" height="196" alt="image" src="https://github.com/user-attachments/assets/1f0e74d0-a800-4ec2-bf0b-a794beca97e9" />

<img width="438" height="129" alt="image" src="https://github.com/user-attachments/assets/640d4c2c-de62-4b34-91a1-38dae2760ae4" />

**3.Подсчет количества файлов и занимаемое пространство.**

Посчитаем размер для нашей папки task1.

Создадим скрипт `sh` в VsCode, назовем его `calculate_hdfs_directory_size.sh` и наполним его кодом:

```
#!/bin/bash

HDFS_DIRECTORY="/task1"

DIRECTORY_SIZE=$(hdfs dfs -du -s $HDFS_DIRECTORY | awk '{print $1}')

HUMAN_READABLE_SIZE=$(hdfs dfs -du -s -h $HDFS_DIRECTORY | awk '{print $1}')

FILE_COUNT=$(hdfs dfs -ls $HDFS_DIRECTORY | grep '^-' | wc -l)

# Вывод результата
echo "Размер директории $HDFS_DIRECTORY: $DIRECTORY_SIZE байт"
echo "Человекочитаемый размер директории $HDFS_DIRECTORY: $HUMAN_READABLE_SIZE"
echo "Количество файлов в директории $HDFS_DIRECTORY: $FILE_COUNT"
```

<img width="693" height="297" alt="image" src="https://github.com/user-attachments/assets/2e542552-a69b-43fa-88c9-013a1ee3fe6f" />

Открываем отдельный терминал и переходим в папку с файлом .sh.

<img width="360" height="22" alt="image" src="https://github.com/user-attachments/assets/6a0a363c-ca17-4d20-8d2a-8f3365b7b054" />

Далее мы перенесем этот скрипт в Docker.

`docker cp calculate_hdfs_directory_size.sh 67baa2e87e1c:/tmp/calculate_hdfs_directory_size.sh`

<img width="1082" height="36" alt="image" src="https://github.com/user-attachments/assets/060b8629-1f64-4541-b528-786b9fd99abb" />

Стоит ли его перекидывать в HDFS? Нет. Проверим его наличие в Docker.

`docker exec -it 67baa2e87e1c ls /tmp/calculate_hdfs_directory_size.sh`

<img width="943" height="135" alt="image" src="https://github.com/user-attachments/assets/bc2da986-3010-4d85-82a1-232dc6d648c7" />

А далее остается сделать его исполняемым и запустить.

`docker exec -it 67baa2e87e1c chmod +x /tmp/calculate_hdfs_directory_size.sh`

<img width="946" height="121" alt="image" src="https://github.com/user-attachments/assets/3e3a59cc-a300-4017-b896-89d2b3075f7f" />

И наконец, запустить скрипт

`docker exec -it 67baa2e87e1c /tmp/calculate_hdfs_directory_size.sh`

<img width="939" height="164" alt="image" src="https://github.com/user-attachments/assets/504fef5b-6c24-49af-8498-337852538696" />

**4.Поставить квоту на 5 файлов для этой директории.**

Переходим в терминал с HDFS

Ввожу команду `hdfs dfsadmin -setQuota 5 /task1` - Поставить квоту на 5 файлов для директории /task1.

`hdfs dfs -count -q /task1` - Проверить квоту.

<img width="942" height="66" alt="image" src="https://github.com/user-attachments/assets/44504043-ab8a-4509-a6c7-a68f8383c103" />

```
Колонки означают:

QUOTA = 5 → стоит квота на количество файлов/директорий = 5.

REMAINING_QUOTA = -1 → это значит, что квота уже достигнута (больше файлов создавать нельзя).

SPACE_QUOTA = none → квота по размеру не задана.

REMAINING_SPACE_QUOTA = inf → ограничений по объёму нет.

DIR_COUNT = 1 → в /task1 есть 1 директория (сама /task1).

FILE_COUNT = 5 → внутри лежит 5 файлов.

CONTENT_SIZE = 135 → общий размер файлов в байтах.

PATHNAME = /task1 → путь до директории.
```

Удалить квоту (снять ограничение) - `hdfs dfsadmin -clrQuota /task1`

<img width="919" height="51" alt="image" src="https://github.com/user-attachments/assets/ab4eb376-19ad-491d-abc4-2badfb433812" />

Если попытаешься загрузить больше 5 файлов, HDFS выдаст ошибку: `QuotaExceededException: The NameSpace quota (directories and files) of directory /task1 is exceeded`

## В HDFS на директорию можно ставить квоты – ограничения. Есть два типа:

**1. Quota (по количеству файлов и папок)**

- ограничивает, сколько объектов (файлов + подкаталогов) можно создать внутри директории.

- если квота достигнута, новые файлы/каталоги создать уже нельзя.

Например:

`hdfs dfsadmin -setQuota 5 /task1`

Это значит, что в каталоге /task1 можно хранить не более 5 файлов или папок.

**2. Space Quota (по размеру данных)**

- ограничивает суммарный объём данных (байты) в директории.

- пример: `hdfs dfsadmin -setSpaceQuota 1g /task1`

Это значит, что в каталоге можно хранить до 1 ГБ данных.


