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
