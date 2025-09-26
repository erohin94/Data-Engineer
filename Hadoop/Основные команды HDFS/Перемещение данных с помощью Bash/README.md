## Задание. Перемещение данных с помощью Bash.

Необходимо достать любые текстовые файлы, половина из которых будет весить больше 100 Мб. Минимальное количество файлов - 5. 
Загрузить их в какую-нибудь папку (это можно сделать руками, не через Bash).

Первый файл - 40 Мб

Второй файл - 95 Мб

Третий файл - 105 Мб

Четвертый файл - 146 Мб

Пятый файл - 930 Мб

Необходимо написать Bash скрипт, который будет запускаться в HDFS и будет делать следующие действия - 

Создаст директорию backup

Перенесет туда все файлы из Вашей папки, чьи размеры будут более 100 Мб.

## Решение

**Создам тестовые файлы в ручную, в терминале ввожу команды**

```
# 40 MB
fsutil file createnew file1.txt 41943040
# 95 MB
fsutil file createnew file2.txt 99614720
# 105 MB
fsutil file createnew file3.txt 110100480
# 146 MB
fsutil file createnew file4.txt 153092096
# 930 MB
fsutil file createnew file5.txt 974848000
```

<img width="590" height="40" alt="image" src="https://github.com/user-attachments/assets/8bfeb178-a151-401d-a8b1-1b8e04562a91" />

**Скопировать их в контейнер Docker:**

`docker cp C:\Users\erohi\Desktop\hdfs\data docker-hive-namenode-1:/tmp/data`

`docker exec -it docker-hive-namenode-1 ls -lh /tmp/data` - проверить что скопировались

<img width="1014" height="259" alt="image" src="https://github.com/user-attachments/assets/c1ae34d6-1278-4f4c-9d7c-5dea65f41718" />

**Скрипт для перемещения больших файлов**

Создаём файл ` move_big_files.sh` локально в папке `C:\Users\erohi\Desktop\hdfs\docker-hive`

**Скопировать скрипт в контейнер:**

`docker cp move_big_files.sh docker-hive-namenode-1:/tmp/move_big_files.sh`

<img width="913" height="38" alt="image" src="https://github.com/user-attachments/assets/99d61792-00d8-4ac7-b57c-d5e6732cef8f" />

**Сделать его исполняемым:**

`docker exec -it docker-hive-namenode-1 bash -c "chmod +x /tmp/move_big_files.sh"`

**Запустить скрипт:**

`docker exec -it docker-hive-namenode-1 bash -c "/tmp/move_big_files.sh"`

<img width="1011" height="166" alt="image" src="https://github.com/user-attachments/assets/8e2f1e85-c1bf-4ef1-bb8f-ba8cc85a8289" />

**Проверка результата**

`docker exec -it docker-hive-namenode-1 hdfs dfs -ls /backup`

<img width="1019" height="181" alt="image" src="https://github.com/user-attachments/assets/9af9a9ad-7ab1-4220-b3b5-936f1061a001" />

Проверка в терминале hdfs 

`docker exec -it docker-hive-namenode-1 /bin/bash`

` hdfs dfs -ls /`

`hdfs dfs -ls /backup`

<img width="727" height="68" alt="image" src="https://github.com/user-attachments/assets/9697c243-796b-44fd-a84d-b8648474ebdf" />

<img width="629" height="101" alt="image" src="https://github.com/user-attachments/assets/10c5bd24-9faa-47ef-aaa3-9f7428529d19" />
