# Big data

Большие данные нельзя хранить в традиционных хранилищах и нельзя обрабатывать стандартными инструментами.

Потому что хранение будет неоптимизированным, а взятие информации будет занимать очень много времени, что для бизнеса недопустимо. 

Именно поэтому начали создавать специальный софт для хранения, обработки, загрузки и выгрузки больших данных.

---------------------------------------

**1. Распределенные файловые системы:**

**Hadoop Distributed File System (HDFS):**

Это распределенная файловая система, которая является основой платформы Hadoop. HDFS позволяет хранить большие объемы данных, распределяя их по кластерам серверов. Данные разбиваются на блоки, которые хранятся на разных узлах кластера, обеспечивая отказоустойчивость и высокую доступность.

**Amazon S3 (Simple Storage Service):**

Облачное хранилище, используется для хранения больших данных. S3 предлагает высокую масштабируемость, надежность и доступность, что делает его популярным выбором для хранения неструктурированных и полуструктурированных данных.

**Google Cloud Storage, Microsoft Azure Blob Storage:**

Подобные сервисы облачного хранения от Google и Microsoft предлагают аналогичные возможности для хранения больших объемов данных в облаке с высокой доступностью и безопасностью.

---------------------------------------

**2. NoSQL базы данных:**

**Apache Cassandra:**

Распределенная NoSQL база данных, которая позволяет хранить и управлять большими объемами данных на нескольких серверах. Cassandra хорошо подходит для работы с большими данными благодаря своей масштабируемости и высокой доступности.

**MongoDB:**

Документно-ориентированная база данных, которая позволяет хранить данные в формате BSON (расширение JSON). MongoDB хорошо справляется с большими объемами данных и обеспечивает гибкость в работе с полуструктурированными и неструктурированными данными.

**HBase:**

NoSQL база данных, построенная поверх HDFS, которая обеспечивает быструю запись и чтение данных, что делает её подходящей для работы с большими данными в реальном времени.

---------------------------------------

**3. И в отдельную группу вынесены еще 2 способа хранения данных, поскольку они не раскатываются образом по типу скачал-установил. Их дополнительно нужно настраивать, при чем не быстро.**

**Data Lake:**

Data Lake — это централизованное хранилище, в котором можно хранить структурированные, полуструктурированные и неструктурированные данные в их исходном виде. 

Data Lake поддерживает хранение данных любого типа и позволяет организациям собирать и обрабатывать данные из множества источников.

**Хранилища данных (Data Warehouses):**

Эти хранилища данных позволяют эффективно хранить и обрабатывать структурированные данные, а также выполнять сложные аналитические запросы над большими объемами данных. 

# Обработка больших данных

**1. Распределенные вычисления:**

**Apache Hadoop:**

Платформа для распределенной обработки больших данных, которая включает в себя HDFS и MapReduce. MapReduce позволяет разбивать задачи на небольшие подзадачи, которые выполняются параллельно на разных узлах кластера, а затем собираются в единый результат. 

**Apache Spark:**

Платформа для распределенных вычислений, которая обеспечивает более быструю обработку данных по сравнению с Hadoop благодаря использованию in-memory вычислений (и не только). Spark поддерживает разнообразные задачи: от обработки потоков данных (Streaming) до машинного обучения (MLlib).

---------------------------------------

**2. Потоковая обработка данных:**

**Apache Kafka:**

Платформа для обработки потоков данных в реальном времени, которая позволяет обрабатывать большие объемы данных, поступающих с высокой скоростью. Kafka используется для сбора, хранения и обработки потоков данных, таких как события IoT или логи сервера. Но на самом деле обработку именно самих данных кафка не делает. Она их перенаправляет.

**Apache Flink, Apache Storm:**

Инструменты для потоковой обработки данных, которые обеспечивают низкую задержку и возможность обработки данных в реальном времени. Flink и Storm используются для задач, требующих мгновенного отклика на поступающие данные. Они являются аналогами Kafka.

---------------------------------------

**3. Инструменты для анализа данных:**

**Hive:**

Инструмент, работающий поверх Hadoop, который позволяет выполнять SQL-подобные запросы к данным, хранящимся в HDFS. Hive упрощает анализ больших данных, предоставляя интерфейс, знакомый пользователям SQL.

**Presto:**

Движок для выполнения SQL-запросов по распределённым данным, который обеспечивает высокую производительность и возможность работы с данными, хранящимися в разных системах (HDFS, S3, реляционные базы данных).

---------------------------------------

**4. Облачные платформы для обработки больших данных:**

**Google Cloud BigQuery:**

Инструмент для обработки больших данных, который позволяет выполнять SQL-запросы по большим наборам данных, хранящимся в облаке. BigQuery обеспечивает высокую производительность и масштабируемость, позволяя обрабатывать петабайты данных за считанные секунды.

**Amazon EMR (Elastic MapReduce):**

Облачная платформа от Amazon для обработки больших данных, основанная на Apache Hadoop и Apache Spark. EMR позволяет быстро разворачивать кластеры и обрабатывать большие объемы данных в облаке.

**Microsoft Azure Synapse Analytics:**

Облачная аналитическая платформа, которая объединяет хранение данных и их обработку, обеспечивая возможность работы с большими данными с использованием SQL и Spark.

Конечно, большие данные можно обрабатывать Python-ом, пандасом и так далее. Но сколько времени потребуется? А время - это самый главный ресурс!

