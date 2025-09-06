# Установка HDFS через Docker

**Склонировать проект:**

`git clone https://github.com/big-data-europe/docker-hive.git`

![image](https://github.com/user-attachments/assets/68d67b3e-174d-4693-af64-0cef1fbbab1c)

(Либо использовать мою папку с проектом, тоже самое: [https://github.com/erohin94/Data-Engineer/tree/main/Hadoop/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0/docker-hive](ссылка))

Проект имеет следующую структуру 

<img width="622" height="278" alt="image" src="https://github.com/user-attachments/assets/a4a5a93d-0e54-4fdb-8951-b5b3f3af9735" />


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
