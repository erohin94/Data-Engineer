## **docker exec**

**docker exec**

- Это команда Docker, а не HDFS.

- Она позволяет зайти внутрь контейнера или выполнить команду внутри контейнера.

- Формат: `docker exec -it <container_name> <команда>`

**Примеры:**

`docker exec -it docker-hive-namenode-1 bash` - Откроет интерактивный bash в контейнере namenode.

`docker exec -it docker-hive-namenode-1 ls /tmp/data` - Выполнит команду `ls /tmp/data` внутри контейнера и покажет список файлов.

## **hdfs dfs**

**hdfs dfs**

- Это команда уже для работы с HDFS.

- Она позволяет создавать папки, загружать файлы, просматривать содержимое HDFS, а не локальной файловой системы контейнера.

**Примеры:**

`hdfs dfs -mkdir /backup` - Создает папку `/backup` в HDFS.

`hdfs dfs -put /tmp/data/file3.txt /backup/` - Копирует файл из локальной файловой системы контейнера (`/tmp/data/file3.txt`) в HDFS (`/backup/`).

`hdfs dfs -ls /backup` - Смотрим, что лежит в папке `/backup` в HDFS.

<img width="555" height="151" alt="image" src="https://github.com/user-attachments/assets/02d65b74-a64f-4084-bfcf-f7c39aa4f9cc" />

<img width="618" height="87" alt="image" src="https://github.com/user-attachments/assets/b057e854-79a7-4164-9374-218092fc77db" />

## **Как они работают вместе**

**`docker exec`** позволяет зайти в контейнер и запустить там команды.

**`hdfs dfs`** запускается уже внутри контейнера и управляет файлами HDFS.

**То есть пример:**

`docker exec -it docker-hive-namenode-1 hdfs dfs -ls /backup``

**`docker exec`** → запускает команду внутри контейнера **`docker-hive-namenode-1`**

**`hdfs dfs -ls /backup`** → это сама команда, которая обращается к HDFS

Простая аналогия: Docker — это дом, контейнер — это комната в доме. docker exec — вы входите в комнату и делаете что-то. HDFS — шкаф внутри комнаты. hdfs dfs — команда, которая работает только с этим шкафом.

Тоесть с hdfs я могу работать с помощью двух терминалов, через терминал докера в контейнере и непосрественно через терминал hdfs.

**Выделил желтым пример того как посмотреть папки в локальной файловой системы контейнера докер и как посмотреть папки в самом hdfs.**

<img width="1044" height="278" alt="image" src="https://github.com/user-attachments/assets/2a27e510-e2ea-469f-bccc-d0bed58c1166" />
