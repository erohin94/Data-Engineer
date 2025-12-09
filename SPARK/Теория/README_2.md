## PySpark Shell

**PySpark Shell** - это интерактивная оболочка для Apache Spark с использованием языка Python. Возможность писать код прям в терминале.

**Плюсы:** 1. Не нужно каждый раз запускать spark-session. 2. Код можно запускать построчно. 3. Spark Shell предоставляет запуск без UI - интерфейса компилятора. То есть только командная строка. 4. Явно в логах "раскатывается" UI интерфейс самого Spark, где можно посмотреть как выполняется джоба.

**Минусы:** 1. Изменить уже запущенный код невозможно. Только копировать - редактировать - еще раз запускать. Как в принципе и в любой командной строке. 2. Нет никаких инструментов отладки.

Запустить PySpark Shell очень просто. Необходимо ввести в терминале команду `pyspark`

Если все хорошо, то увидим следующую картинку:

<img width="1147" height="382" alt="image" src="https://github.com/user-attachments/assets/073b378c-3548-4492-8750-a7a1181cfd43" />

И далее пишем код:

<img width="623" height="336" alt="image" src="https://github.com/user-attachments/assets/31145825-ba83-498d-a8f0-bad21c034918" />

## Spark UI

<img width="802" height="265" alt="image" src="https://github.com/user-attachments/assets/9b404aa4-2bbb-46a3-8463-0e40fc90b094" />


**Jobs** - это целое приложение.

Spark Job создается всякий раз, когда на `DataFrame` или `RDD` (Resilient Distributed Dataset) вызывается действие (`action`) или преобразование. Примеры действий включают `collect()`, `count()`, `saveAsTextFile()`, `show()`.

В свою очередь `Job` состоит еще из нескольких этапов, а именно - `Stages` и `Tasks`.

**Stage:** Работа (`job`) разбивается на несколько этапов (`stages`). Каждый этап представляет собой последовательность операций, которые могут быть выполнены без необходимости передавать данные по сети.

**Task:** Каждый этап разбивается на задачи (`tasks`), которые выполняются на отдельных разделах данных (`partitions`). Задачи выполняются параллельно на рабочих узлах (`workers`) кластера.

**Раздел (`partitions`)** - это часть данных, которая обрабатывается одной задачей (`task`) в Spark. Каждая `RDD` (Resilient Distributed Dataset) и `DataFrame` состоит из нескольких разделов.

Чаще всего Spark сам решает на сколько разделов ему поделить данные, но можно указать явно.

`df = spark.read.csv("path/to/file.csv", header=True, inferSchema=True, numPartitions=10)`

Когда джоба началась, видно сколько длилась, сколько было `stage` и сколько `tasks`.

<img width="1023" height="126" alt="image" src="https://github.com/user-attachments/assets/eb71f7d3-3602-43c3-a1db-88044dfab39d" />

Нажав на синий текст, можно увидеть выполнение программы внутри.

<img width="258" height="713" alt="image" src="https://github.com/user-attachments/assets/fb7f7da3-1843-4514-a689-a8249812ebfe" />

Если нажать на любой из синих квадратиков можно получить полную информацию о выполнении.

<img width="392" height="685" alt="image" src="https://github.com/user-attachments/assets/b5ff408c-3916-49fc-973c-8fd2cc6a9129" />

## Catalyst Optimizer 

**Catalyst Optimizer** — это встроенный механизм оптимизации запросов в Apache Spark, используемый для обработки и оптимизации запросов SQL и DataFrame. Catalyst Optimizer является одной из ключевых частей Spark SQL и отвечает за создание, оптимизацию и выполнение логического и физического планов запросов.
