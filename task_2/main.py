from datetime import datetime, date

from pyspark.sql import SparkSession, Row


# SparkSession.builder.master("local[*]").getOrCreate().stop()
spark = SparkSession.builder.master('spark://localhost:7077').appName('Spark-app-test').getOrCreate()
print(spark)
# spark = SparkSession.builder.master("sc://localhost:7077").getOrCreate()
# print("123")

df = spark.read.parquet("examples/src/main/resources/users.parquet")
(df.write.format("parquet")
    .option("parquet.bloom.filter.enabled#favorite_color", "true")
    .option("parquet.bloom.filter.expected.ndv#favorite_color", "1000000")
    .option("parquet.enable.dictionary", "true")
    .option("parquet.page.write-checksum.enabled", "false")
    .save("users_with_options.parquet"))