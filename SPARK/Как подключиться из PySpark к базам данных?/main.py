from pyspark.sql import SparkSession
import os 
os.environ["PYSPARK_PYTHON"] = r'C:/Users/erohi/AppData/Local/Programs/Python/Python311/python.exe'
os.environ["PYSPARK_DRIVER_PYTHON"] = r'C:/Users/erohi/AppData/Local/Programs/Python/Python311/python.exe'


spark = SparkSession.builder.appName("PySpark PostgreSQL Connection").config("spark.jars", "postgresql-42.2.23.jar").getOrCreate()

url = "jdbc:postgresql://localhost:5432/mydatabase"
properties = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}

data = [
    ("Alice", "Engineer", 75000, "2021-06-15"),
    ("Bob", "Manager", 90000, "2020-05-01"),
    ("Charlie", "HR", 60000, "2019-04-12"),
    ("Diana", "Sales", 50000, "2018-01-25")
]
columns = ["name", "position", "salary", "hire_date"]

df = spark.createDataFrame(data, columns)
df.show()

filtered_df = df.filter(df.salary >= 60000)
filtered_df.show()

url = "jdbc:postgresql://localhost:5432/mydatabase"
properties = {
    "user": "myuser",
    "password": "mypassword",
    "driver": "org.postgresql.Driver"
}

filtered_df.write.jdbc(
    url=url,
    table="high_salary_employees",
    mode="overwrite",  # "overwrite" - если таблица уже существует, она будет перезаписана
    properties=properties
)

df.write.mode("error").jdbc(url=url, table="my_table", properties=properties)

print("Данные успешно записаны в таблицу high_salary_employees")

spark.stop()


