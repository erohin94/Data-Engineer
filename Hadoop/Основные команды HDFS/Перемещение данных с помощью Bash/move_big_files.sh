#!/bin/bash

# Папка с исходными файлами
SOURCE_DIR="/tmp/data"

# Папка backup в HDFS
HDFS_BACKUP_DIR="/backup"

# Создаем директорию backup в HDFS, если ее нет
hdfs dfs -mkdir -p $HDFS_BACKUP_DIR

# Проходим по всем файлам в SOURCE_DIR
for file in $SOURCE_DIR/*; do
    # Получаем размер файла в Мб
    size=$(du -m "$file" | cut -f1)

    # Если размер больше 100 Мб — копируем в HDFS backup
    if [ "$size" -gt 100 ]; then
        echo "Переносим $file размером $size Мб в $HDFS_BACKUP_DIR"
        hdfs dfs -put -f "$file" $HDFS_BACKUP_DIR/
    fi
done