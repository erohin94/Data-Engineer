#!/bin/bash

# Метка времени для уникальности
timestamp=$(date +%Y%m%d_%H%M%S)

# Локальная папка внутри контейнера
local_dir="/tmp/letters_$timestamp"
mkdir -p "$local_dir"

# Папка в HDFS
hdfs_dir="/task_$timestamp"

# Текст для генерации
text="Всем привет, я изучаю HDFS"

# Разбиваем текст на буквы (только русские и английские)
letters=$(echo "$text" | grep -o -i "[а-яёa-z]")

# Генерация CSV-файлов
pos=0
for letter in $letters; do
    filename="$local_dir/letter_${pos}.csv"
    echo "letter,position" > "$filename"
    echo "$letter,$pos" >> "$filename"
    pos=$((pos+1))
done

echo "[OK] Сгенерировано $pos файлов в $local_dir"

# Создаем папку в HDFS
hdfs dfs -mkdir "$hdfs_dir"
echo "[OK] В HDFS создана папка $hdfs_dir"

# Загружаем все файлы в HDFS
hdfs dfs -put "$local_dir"/* "$hdfs_dir"/
echo "[OK] Папка $local_dir загружена в HDFS → $hdfs_dir"

# Проверяем содержимое
hdfs dfs -ls -R "$hdfs_dir"