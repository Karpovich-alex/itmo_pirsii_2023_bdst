from pyspark.sql import SparkSession
import pyspark
import pandas as pd
from datetime import datetime, date

import os

os.environ["HADOOP_HOME"] = 'C:\\Hadoop\\'

conf = pyspark.SparkConf().setAppName('Spark-app-new-data').setMaster('spark://localhost:7077')
conf.set("spark.driver.port", "20002")
conf.set("spark.driver.host", "172.25.16.1")
conf.set("spark.driver.bindAddress", "0.0.0.0")
conf.set("spark.home", "0.0.0.0")
conf.set("spark.sql.execution.arrow.pyspark.enabled", True)
sc = pyspark.SparkContext(conf=conf)
spark = SparkSession.builder.getOrCreate()

pandas_df = pd.read_csv(r"C:\Users\Karpo\PycharmProjects\itmo_pirsii_2023_bdst\task_2\test_data\test.csv")
pandas_df = pandas_df.head(100)
# pandas_df = pd.DataFrame({
#     'a': [1, 2, 3],
#     'b': [2., 3., 4.],
#     'c': ['string1', 'string2', 'string3'],
#     'd': [date(2000, 1, 1), date(2000, 2, 1), date(2000, 3, 1)],
#     'e': [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 2, 12, 0), datetime(2000, 1, 3, 12, 0)]
# })

df = spark.createDataFrame(pandas_df)


parquet_path = "file:///opt/spark-data/parquet/text_file.parquet"
df.coalesce(1).write.parquet(parquet_path, mode="overwrite")

# df.write.parquet("file:///C:/Users/Karpo/PycharmProjects/itmo_pirsii_2023_bdst/task_2/saved", mode="overwrite")
# df.write.parquet("file:///172.25.16.1/C:/Users/Karpo/PycharmProjects/itmo_pirsii_2023_bdst/task_2/saved/test.parquet")
# df.write.parquet("/opt/spark-data/test", mode="overwrite")
# df.write.orc("/opt/spark-data/test_orc", mode="overwrite")

print(spark.read.parquet(parquet_path).show())
# print(spark.read.parquet('hdfs://localhost:54310/df.orc').show())



# df = spark.read.parquet("examples/src/main/resources/users.parquet")
# (df.write.format("parquet")
#     .option("parquet.bloom.filter.enabled#favorite_color", "true")
#     .option("parquet.bloom.filter.expected.ndv#favorite_color", "1000000")
#     .option("parquet.enable.dictionary", "true")
#     .option("parquet.page.write-checksum.enabled", "false")
#     .save("users_with_options.parquet"))