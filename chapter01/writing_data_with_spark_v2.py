"""Writing data with Spark (v2)

Examples showing various write options: formats, compression, partitioning and repartition/coalesce.

Usage: set `JAVA_HOME` and run with `pyspark` available.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

from pyspark.sql import SparkSession

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter01-write-data")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Read CSV file
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

df = (spark.read.format("csv")
      .option("header", "true")
      .option("nullValue", "null")
      .option("dateFormat", "LLLL d, y")
      .load("data/input/netflix_titles.csv"))

# Write the CSV date
(df.write.format("csv")
 .option("header", "true")
 .mode("overwrite")
 .option("delimiter", ";")
 .save("data/output/data_lake/netflix_csv_data"))

# Write the DataFrame to JSON
(df.write.format("json")
 .mode("overwrite")
 .save("data/output/data_lake/netflix_json_data"))

# Write DataFrame to Parquet
(df.write.format("parquet")
 .mode("overwrite")
 .save("data/output/data_lake/netflix_parquet_data"))

# Write compressed data
(df.write.format("csv")
 .mode("overwrite")
 .option("header", "true")
 .option("delimiter", ";")
 .option("codec", "org.apache.hadoop.io.compress.GzipCodec")
 .save("data/output/data_lake/netflix_csv_data.gz"))

# Specifying the number of partitions
(df.repartition(4)
 .write.format("csv")
 .mode("overwrite")
 .option("header", "true")
 .option("delimiter", ";")
 .save("data/output/data_lake/netflix_csv_data_repartition"))

# Use coalesce to reduce the number of partitions
(df.coalesce(1)
 .write.format("csv")
 .mode("overwrite")
 .option("header", "true")
 .option("delimiter", ";")
 .save("data/output/data_lake/netflix_csv_data_coalesce"))

# Use partitionBy to write partitions based on column
# partition the CSV data by the 'release_year' column
(df.write.format("csv")
 .option("header", "true")
 .option("delimiter", ";")
 .mode("overwrite")
 .partitionBy('release_year')
 .save("data/output/data_lake/netflix_csv_data_partitioned"))

# Release the resources
spark.stop()
