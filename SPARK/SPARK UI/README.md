## Запуск SPARK UI 

Если SPARK установлен локально. Смотри [установку](https://github.com/erohin94/Data-Engineer/tree/main/SPARK/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0)

Убедится, что установлен Spark и Java:

`spark-shell --version`

`java -version`

<img width="645" height="327" alt="image" src="https://github.com/user-attachments/assets/3546af64-852e-4cfc-8795-dd7f63038e07" />

Вводим в терминале `spark-shell`

<img width="1165" height="338" alt="image" src="https://github.com/user-attachments/assets/31b0a4e1-79de-4391-8ae0-b1c22d88224c" />

И переходим по адресу `http://localhost:4040` - если спарк установлен локально.

Откроется UI интерфейс Spark

<img width="647" height="212" alt="image" src="https://github.com/user-attachments/assets/59b5464c-cdff-4147-88d7-138db60c63f9" />

Не закрывать spark-shell (окно CMD), пока смотрю UI — как только завершить сессию, UI исчезнет.

Так же UI интерфейс можно открыть, запустив любое Spark-приложение, например на Python:

```
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestApp") \
    .master("local[*]") \
    .getOrCreate()

df = spark.range(1000000)
df.selectExpr("sum(id)").show()
input("Spark запущен. Перейди в http://localhost:4040 и нажми Enter, чтобы завершить...")
```

<img width="1009" height="510" alt="image" src="https://github.com/user-attachments/assets/56d88f52-40bc-4512-87d1-2d7c5657eb6a" />

Как только нажму Enter, UI отключится.

Так же если не будет последней строки с `input(.....`, то UI так же не откроется, так как когда Python-скрипт завершается — Spark останавливается, и UI автоматически гаснет.
В моем примере: `df.selectExpr("sum(id)").show()` скрипт завершается сразу после выполнения, и SparkSession закрывается. И я просто не успеваю открыть UI.

