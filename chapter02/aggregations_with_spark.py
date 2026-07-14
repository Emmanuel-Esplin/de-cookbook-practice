
"""Aggregations with Spark

Demonstrates groupBy, agg, rollups, cubes and approximate aggregation techniques.

Usage: set `JAVA_HOME` and run with `pyspark`.
"""
import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, max, count, min, approx_count_distinct
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter02-Aggregations")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Create DataFrame
df = (spark.read.format("csv")
     .option("header", "true")
      .option("nullValue", "null")
      .option("dateFormat", "LLLL d, y")
      .load("data/input/netflix_titles.csv"))

# Group data by column | Perform aggregations
grouped_df = df.groupBy("country")

# Count the number of rows in each group | Perform aggregations or transformations
count_df = grouped_df.count()
count_df.show()

# Apply custom aggregation using max
max_release_df = grouped_df.agg(max(col("date_added")))
max_release_df.show()

# Multi aggregations
release_date_group_df = (
    df.groupBy("country")
    .agg(
        count("show_id").alias("NumberOfReleases"),
        max("date_added").alias("LastReleaseDate"),
        min("date_added").alias("FirstReleaseDate"),
    )
)
release_date_group_df.show(3)

# Pivot tables
pivot_table = df.groupBy("country").pivot("type").agg(count("show_id"))
pivot_table.show()

# Approximate aggregations
# Define Schema
schema = StructType([
    StructField("Id", IntegerType(), True),
    StructField("ProductId", StringType(), True),
    StructField("UserId", StringType(), True),
    StructField("ProfileName", StringType(), True),
    StructField("HelpfulnessNumerator", StringType(), True),
    StructField("HelpfulnessDenominator", StringType(), True),
    StructField("Score", IntegerType(), True),
    StructField("Time", StringType(), True),
    StructField("Summary", StringType(), True),
    StructField("Text", StringType(), True)
])

review_df = (spark.read.format("csv")
             .option("header", "true")
             .schema(schema)
             .load("data/input/Reviews.csv"))

# Approximate quantile calculation
quantiles = review_df.approxQuantile("Score", [0.25, 0.5, 0.75], 0.1)
print("Approximate Quantiles:", quantiles)

# Approximate distinct count calculation
approx_distinct_count = review_df.select(
    approx_count_distinct("ProductId", rsd=0.1).alias("approx_distinct_count")
)
approx_distinct_count.show()

# Release the resources
spark.stop()
