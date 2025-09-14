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


-Перенести из файловой системы докера в HDFS
