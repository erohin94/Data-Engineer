import subprocess
import pandas as pd
import re
import os
from datetime import datetime

# Имя контейнера (проверь через docker ps)
container_name = "docker-hive-namenode-1"

# Метка времени для уникальности
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Локальная папка для CSV
local_dir = fr"C:\Users\erohi\Desktop\hdfs\letters_{timestamp}"
os.makedirs(local_dir, exist_ok=True)

# Папка внутри контейнера
container_tmp = f"/tmp/letters_{timestamp}"

# Папка в HDFS
hdfs_dir = f"/task_{timestamp}"

def letters_to_hdfs(text):
    # Разбиваем текст на буквы
    letters = re.findall(r"[а-яёa-z]", text, re.IGNORECASE)

    # Генерим CSV-файлы
    for pos, letter in enumerate(letters):
        filename = f"letter_{pos}.csv"
        filepath = os.path.join(local_dir, filename)
        df = pd.DataFrame({"letter": [letter], "position": [pos]})
        df.to_csv(filepath, index=False, encoding='utf-8')

    print(f"[OK] Сгенерировано {len(letters)} файлов в {local_dir}")

    # 1. Копируем папку в контейнер
    subprocess.run(
        f"docker cp \"{local_dir}\" {container_name}:{container_tmp}",
        shell=True, check=True
    )
    print(f"[OK] Папка {local_dir} скопирована в контейнер → {container_tmp}")

    # 2. Создаём папку в HDFS
    subprocess.run(
    f"docker exec {container_name} hdfs dfs -mkdir {hdfs_dir}",
    shell=True, check=True
    )
    print(f"[OK] В HDFS создана папка {hdfs_dir}")

    # 3. Загружаем всю директорию в HDFS
    subprocess.run(
    f"docker exec {container_name} hdfs dfs -put {container_tmp} {hdfs_dir}/",
    shell=True, check=True
    )
    print(f"[OK] Папка {container_tmp} загружена в HDFS → {hdfs_dir}")

    # 4. Проверяем результат
    subprocess.run(
    f"docker exec {container_name} hdfs dfs -ls -R {hdfs_dir}",
    shell=True, check=True
    )

# Пример текста
text = "Всем привет, я изучаю HDFS"
letters_to_hdfs(text)
