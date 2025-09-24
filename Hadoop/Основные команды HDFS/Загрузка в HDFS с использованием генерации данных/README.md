# Загрузка в HDFS с использованием генерации данных.

**Задача.**

У нас есть следующий текст - "Всем привет, я изучаю HDFS"
               
Необходимо каждую букву записать в `csv` файл и загрузить в HDFS с помощью цикла, а не руками. 
Так как загрузка на текущий момент происходит через Docker, то необходимо как-то автоматизировать этот процесс и при этом необходимо это делать в терминале. 
По итогу мы должны научиться загружать любое количество файлов, вне зависимости от их количества и размера.

**Решение**

Запускаю скрипт

<img width="867" height="512" alt="image" src="https://github.com/user-attachments/assets/43b2bab2-d903-4511-8e53-4eaf02801558" />

Папка с `csv` файлами создана вмоей локальной папке `C:\Users\erohi\Desktop\hdfs`, с помощью скрипта.

<img width="613" height="110" alt="image" src="https://github.com/user-attachments/assets/543a8692-ae19-443b-a226-399487aad425" />

С помощью команды в скрипте `f"docker cp \"{local_dir}\" {container_name}:{container_tmp}"` я скопировал файлы из локальной папки в контейнер.

Можно проверить выполнив команду в терминале `docker exec a3d9ac3c9f82 ls -la /tmp/letters_20250924_190048`. Увидим следующее

<img width="639" height="405" alt="image" src="https://github.com/user-attachments/assets/cc85e331-ef93-4cdc-9fec-ac66d665b57c" />

что подтверждает что папка скопирована в контейнер

Выполнять команду можно как из корневой папки `C:\Users\erohi>docker exec a3d9ac3c9f82 ls -la /tmp/letters_20250924_190048`, 
так и из папки с проектом `C:\Users\erohi\Desktop\hdfs>docker exec a3d9ac3c9f82 ls -la /tmp/letters_20250924_190048`. 
Результат будет одинаковый.

Посмотреть содержимое содержимое директории /tmp внутри контейнера куда добавил файлы `docker exec a3d9ac3c9f82 ls -la /tmp`

<img width="633" height="117" alt="image" src="https://github.com/user-attachments/assets/9c6ed2a5-c2aa-442b-a684-5e9658b3995e" />

Удалить файлы которые добавил в контейнер `docker exec a3d9ac3c9f82 find /tmp -type d -name "letters_*" -exec rm -rf {} +`

**Проверить наличие файлов в hdfs**

Через терминал докера `docker exec -it docker-hive-namenode-1 hdfs dfs -ls /task_20250924_190048/letters_20250924_190048`

<img width="1069" height="475" alt="image" src="https://github.com/user-attachments/assets/70b61da6-7fd1-480c-9774-c32250951b16" />

Прочитать содержимое конкретного файла `docker exec -it docker-hive-namenode-1 hdfs dfs -cat /task_20250924_190048/letters_20250924_190048/letter_0.csv`

<img width="1120" height="146" alt="image" src="https://github.com/user-attachments/assets/13adc8ee-19e0-4518-9fb7-5665905ea2bc" />

Через терминал HDFS. Переходим в терминал с HDFS `docker exec -it docker-hive-namenode-1 /bin/bash`

Вводим `hdfs dfs -ls /` - Показывает все папки в HDFS.

<img width="708" height="183" alt="image" src="https://github.com/user-attachments/assets/496f7179-dc64-4136-816b-a1563f73677d" />

Содержимое конкретной папки `hdfs dfs -ls /task_20250924_190048/letters_20250924_190048`

<img width="1053" height="434" alt="image" src="https://github.com/user-attachments/assets/7c218623-321b-453c-a389-4dccb9b47f25" />

Прочитать содержимое файла `hdfs dfs -cat /task_20250924_190048/letters_20250924_190048/letter_0.csv`

<img width="759" height="67" alt="image" src="https://github.com/user-attachments/assets/233b09db-afdb-4415-9373-b6e8b0a3668b" />

**Удаление файлов из контейнера и HDFS**

Удаляем папки из HDFS `docker exec -it docker-hive-namenode-1 hdfs dfs -rm -r -f /task_20250924_*`

`-r` — рекурсивно, чтобы удалить подпапки.

`-f`— принудительно, без подтверждений.

Проверяем, что HDFS пуст от папок: `docker exec -it docker-hive-namenode-1 hdfs dfs -ls /`

<img width="1128" height="323" alt="image" src="https://github.com/user-attachments/assets/4b366b18-5ff5-4964-8214-9f3dbba7b337" />

Удаляем временные папки внутри контейнера `docker exec -it docker-hive-namenode-1 bash -c "rm -rf /tmp/letters_*"`

Проверяем: `docker exec -it docker-hive-namenode-1 ls -l /tmp`

<img width="1016" height="259" alt="image" src="https://github.com/user-attachments/assets/769611cb-09f5-4a55-8f1e-71aaeb7d82c2" />

# Схема

Наглядная схема, как скрипт работает с файлами:

```
[Windows локальный диск]
C:\Users\erohi\Desktop\hdfs\letters_20250924_185224
      │  <- Python генерирует CSV
      │     df.to_csv(..., encoding='utf-8')
      ▼
─────────────────────────────
[Docker-контейнер: Linux FS]
/tmp/letters_20250924_185224
      │  <- docker cp копирует папку из Windows
      │
      ▼
─────────────────────────────
[HDFS: Hadoop Distributed File System]
/task_20250924_185224/letters_20250924_185224
      │  <- docker exec hdfs dfs -put загружает файлы в HDFS
      │
      ▼
      Файлы доступны в HDFS, управляются NameNode и DataNode
      Можно просматривать через:
      hdfs dfs -ls /task_20250924_185224
      hdfs dfs -cat /task_20250924_185224/letter_0.csv
```

**Пояснения:**

Windows FS — временная рабочая директория, где создаются CSV.

Docker контейнер — Linux-файловая система, через которую запускаются команды HDFS.

HDFS — распределённое хранилище Hadoop, где файлы реплицируются и управляются NameNode/DataNode.

**Важно:**

Удаление файлов в Windows не удаляет их из контейнера и HDFS.

Удаление в контейнере не удаляет их из HDFS.

Чтобы полностью очистить, нужно отдельно удалять и из контейнера, и из HDFS.

# Ошибки

При создании папки в HDFS была ошибка

```
(myenv) PS C:\Users\erohi\Desktop\task_2_hadoop> python test.py
[OK] Сгенерировано 21 файлов в C:\Users\erohi\Desktop\hdfs\letters_20250924_183206
Successfully copied 40.4kB to docker-hive-namenode-1:/tmp/letters_20250924_183206
[OK] Папка C:\Users\erohi\Desktop\hdfs\letters_20250924_183206 скопирована в контейнер → /tmp/letters_20250924_183206
mkdir: Cannot create directory /task_20250924_183206. Name node is in safe mode.
Traceback (most recent call last):
  File "C:\Users\erohi\Desktop\task_2_hadoop\test.py", line 59, in <module>
    letters_to_hdfs(text)
  File "C:\Users\erohi\Desktop\task_2_hadoop\test.py", line 44, in letters_to_hdfs
    subprocess.run(
  File "C:\Users\erohi\AppData\Local\Programs\Python\Python39\lib\subprocess.py", line 528, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command 'docker exec docker-hive-namenode-1 hdfs dfs -mkdir /task_20250924_183206' returned non-zero exit status 1.
```

![3](https://github.com/user-attachments/assets/53200e13-626a-411e-a152-32a3f1a97667)

Это значит, что `NameNode` в `safe mode` — режим «только для чтения», пока кластер проверяет блоки. 
В таком состоянии нельзя писать в HDFS (mkdir, put и т. д.).

Проверить статус:

`docker exec docker-hive-namenode-1 hdfs dfsadmin -safemode get`

Если нужно выйти из safe mode вручную:

`docker exec docker-hive-namenode-1 hdfs dfsadmin -safemode leave`

![4](https://github.com/user-attachments/assets/70888d29-39b6-4120-8250-1360837ce4f5)

После пробую запустить скрипт заново - заработало.


put: `/tmp/letters_20250924_183635/*': No such file or directory
То есть внутри контейнера папки /tmp/letters_20250924_183635 нет, хотя docker cp вроде отработал.
Причина в том, что docker cp копирует в контейнер под root (в файловую систему Linux), а hdfs dfs -put выполняется уже внутри контейнера от пользователя hdfs (или hadoop), у которого может не быть доступа/видимости к /tmp.
