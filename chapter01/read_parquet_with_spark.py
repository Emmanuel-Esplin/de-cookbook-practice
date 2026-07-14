"""Read Parquet with Spark

Example showing reading Parquet files and working with schema-on-read.

Usage: requires `pyspark` and `JAVA_HOME`.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

from pyspark.sql import SparkSession

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter01-ReadParquet")
         .master("local[*]")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Load Parquet data
df = (spark.read.format("parquet")
      .load("data/input/recipes.parquet"))

# View schema of DataFrame
df.printSchema()

# Display data in DataFrame
df.show()

# Reading partitioned data
df_partitioned = (spark.read.format("parquet")
                  .load("data/input/recipes.parquet"))
df_partitioned.printSchema()

df_partitioned1 = (spark.read.format("parquet")
                   .load("data/input/partitioned_recipes/DatePublished=2020-01*"))
df_partitioned1.printSchema()

# Schema merging
df_merge_schema = (spark.read.format("parquet")
                   .option("mergeSchema", "true")
                   .load("data/input/partitioned_recipes"))
df_merge_schema.printSchema()

# Release the resources
spark.stop()
