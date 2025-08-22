- [Конкуренты Spark](#Конкуренты-Spark)

## Spark

Spark имеет способность работать в памяти, что обеспечивает значительное ускорение обработки данных. 
Это стало возможным благодаря концепции `Resilient Distributed Dataset (RDD)`, которая позволяет эффективно распределять данные и выполнять операции над ними в памяти.

## Конкуренты Spark

**Cloudera Impala:** Impala - это распределенный SQL-движок, разработанный для выполнения интерактивных запросов на основе структурированных данных, хранящихся в Apache Hadoop. 
Impala обеспечивает высокую скорость выполнения SQL-запросов и позволяет взаимодействовать с данными в реальном времени.

**Основные ядра Spark**

Apache Spark состоит из нескольких основных компонентов, которые выполняют различные функции в распределенной обработке данных. Основные ядра Apache Spark включают:

**Spark Core:** Spark Core является основным компонентом Apache Spark. 
Он предоставляет основные функциональности и API для распределенной обработки данных, включая управление памятью, планирование задач, ввод-вывод данных и взаимодействие с распределенной файловой системой.

**Spark SQL:** Spark SQL предоставляет возможности работы с данными в структурированном формате, поддерживая SQL-запросы и операции со структурами данных, такими как таблицы, представления и датасеты. 
Spark SQL обеспечивает интеграцию с различными источниками данных, включая Apache Hive, JDBC и другие.

**Spark Streaming:** Spark Streaming предоставляет возможности обработки потоковых данных в реальном времени. 
Он позволяет разрабатывать и запускать аналитические приложения для обработки непрерывных потоков данных, таких как данные из очередей сообщений, систем мониторинга и т.д.

**MLlib:** MLlib (Machine Learning Library) является библиотекой машинного обучения в Apache Spark. 
Она предоставляет набор алгоритмов и утилит для обработки данных, классификации, регрессии, кластеризации, рекомендательных систем и других задач машинного обучения.

**GraphX:** GraphX - это библиотека для работы с графами в Apache Spark. 
Она предоставляет API и инструменты для анализа и обработки графовых структур, таких как социальные сети, сети связей и другие.

**SparkR:** SparkR - это пакет для языка программирования R, который позволяет использовать возможности Apache Spark в среде R. 
Он предоставляет R-разработчикам удобный способ взаимодействия с данными и выполнения распределенных вычислений в Spark.

Каждое ядро Apache Spark предлагает свои возможности и API для обработки и анализа данных в различных сценариях. 
Вместе эти компоненты обеспечивают мощную и гибкую платформу для обработки больших объемов данных и выполнения различных задач анализа и машинного обучения.

## Создание Spark Session и сравнение со Spark Context

В Apache Spark создание `Spark Session` является более предпочтительным подходом по сравнению с использованием `Spark Context`. Вот почему:

**Spark Context** был основной входной точкой для программирования на Spark в более ранних версиях фреймворка. Он предоставлял основные функции и возможности Spark, такие как создание `RDD (Resilient Distributed Dataset)` и выполнение операций над ними. Однако, с появлением Spark 2.0 и выше, введение `Spark Session` стало рекомендованным способом работы с Spark.

**Spark Session** является более высокоуровневым интерфейсом, который объединяет функциональность `Spark Context`, `SQL Context` и `Hive Context` в одном объекте. Он предоставляет доступ к функциям `Spark Core`, `Spark SQL`, `Spark Streaming`, `MLlib` и `GraphX`. `Spark Session` позволяет разработчикам работать с различными типами данных, включая `RDD`, `DataFrames` и `Datasets`, а также выполнять запросы на языке SQL, манипулировать структурированными данными и выполнять аналитику в реальном времени.

**Преимущества Spark Session по сравнению с Spark Context:**

Удобство использования: Spark Session предоставляет более удобный и единый интерфейс для работы с различными модулями Spark. Он упрощает кодирование и повышает производительность разработки.

Поддержка различных типов данных: Spark Session поддерживает работу с RDD, DataFrames и Datasets, что обеспечивает более гибкую обработку и анализ данных в Spark.

Интеграция со сторонними инструментами: Spark Session обеспечивает интеграцию с различными инструментами и библиотеками, такими как Hive, JDBC, Parquet, Avro и другими.

Улучшенная оптимизация: Spark Session имеет лучшую оптимизацию выполнения запросов, что приводит к улучшенной производительности.

Поддержка различных источников данных: Spark Session позволяет работать с различными источниками данных, включая файловые системы (HDFS, S3 и т.д.), базы данных (MySQL, PostgreSQL и др.), Apache Kafka и другие.

В итоге, Spark Session предоставляет более современный и мощный способ работы с Apache Spark, объединяя различные модули и обеспечивая удобство использования, гибкость и лучшую производительность. Он является рекомендованным подходом для разработки на Spark, особенно начиная с версии Spark 2.0 и выше.

**Пример создания Spark Context на Python:**

```
from pyspark import SparkContext

# Создание объекта SparkContext
sc = SparkContext(appName="MySparkApp")

# Здесь можно выполнять операции с RDD

# Закрытие SparkContext
sc.stop()
```
                  
**Пример создания Spark Session на Python:**

```
from pyspark.sql import SparkSession

# Создание объекта SparkSession
spark = SparkSession.builder \
    .appName("MySparkApp") \
    .getOrCreate()

# Здесь можно выполнять операции с DataFrames
# Закрытие SparkSession
spark.stop()
```
                  
В обоих примерах мы используем PySpark для работы с Spark в языке Python.

В примере создания `Spark Context` мы импортируем модуль `SparkContext` из библиотеки `PySpark` и создаем объект `sc` с указанием имени приложения. Затем мы можем выполнять операции с `RDD`, используя `sc`. По завершении работы необходимо вызвать метод `stop()` для закрытия `Spark Context`.

В примере создания `Spark Session` мы импортируем модуль `SparkSession` и используем `builder` для настройки параметров `Spark Session`, таких как имя приложения. Затем мы вызываем метод `getOrCreate()`, который создает новую `Spark Session` или возвращает существующую, если она уже создана. После этого мы можем выполнять операции с `DataFrames`, используя `spark`. Наконец, мы вызываем метод `stop()` для закрытия `Spark Session`.

**Рассмотрим различные параметры Spark Session.**

**App Name (spark.app.name)**

- Описание: Имя Spark-приложения.
- Пример: spark = SparkSession.builder.appName("MyApp").getOrCreate()

**Master (spark.master)**

- Описание: Указывает кластерный менеджер для выполнения приложения (например, локально или в кластере).
- Пример: spark = SparkSession.builder.master("local[*]").getOrCreate()

**Spark SQL Shuffle Partitions (spark.sql.shuffle.partitions)**

- Описание: Количество разделов для операций shuffle в Spark SQL.
- Пример: spark = SparkSession.builder.config("spark.sql.shuffle.partitions", "200").getOrCreate()

**Executor Memory (spark.executor.memory)**

- Описание: Количество памяти, выделяемой каждому исполнителю.
- Пример: spark = SparkSession.builder.config("spark.executor.memory", "4g").getOrCreate()

**Driver Memory (spark.driver.memory)**

- Описание: Количество памяти, выделяемой драйверу Spark-приложения.
- Пример: spark = SparkSession.builder.config("spark.driver.memory", "2g").getOrCreate()

**Executor Cores (spark.executor.cores)**

- Описание: Количество ядер, выделяемых каждому исполнителю.
- Пример: spark = SparkSession.builder.config("spark.executor.cores", "4").getOrCreate()

**Dynamic Allocation (spark.dynamicAllocation.enabled)**

- Описание: Включает динамическое выделение исполнителей для приложения.
- Пример: spark = SparkSession.builder.config("spark.dynamicAllocation.enabled", "true").getOrCreate()

**Checkpoint Directory (spark.checkpoint.dir)**

- Описание: Указывает директорию для сохранения контрольных точек RDD.
- Пример: spark = SparkSession.builder.config("spark.checkpoint.dir", "/path/to/checkpoint/dir").getOrCreate()

**SQL Warehouse Directory (spark.sql.warehouse.dir)**

- Описание: Указывает директорию для хранения данных Spark SQL.
- Пример: spark = SparkSession.builder.config("spark.sql.warehouse.dir", "/path/to/warehouse/dir").getOrCreate()

**Hive Support (spark.sql.catalogImplementation)**

- Описание: Включает поддержку Apache Hive в Spark SQL.
- Пример: spark = SparkSession.builder.config("spark.sql.catalogImplementation", "hive").enableHiveSupport().getOrCreate()

**Пример создания Spark Session с параметрами конфигурации:**

```
from pyspark.sql import SparkSession

# Создание Spark Session с различными параметрами конфигурации
spark = SparkSession.builder \
    .appName("MyApp") \
    .master("local[*]") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.cores", "4") \
    .config("spark.dynamicAllocation.enabled", "true") \
    .config("spark.checkpoint.dir", "/path/to/checkpoint/dir") \
    .config("spark.sql.warehouse.dir", "/path/to/warehouse/dir") \
    .config("spark.sql.catalogImplementation", "hive") \
    .enableHiveSupport() \
    .getOrCreate()

# Пример использования Spark Session
df = spark.read.json("/path/to/json/file")
df.show()
```

