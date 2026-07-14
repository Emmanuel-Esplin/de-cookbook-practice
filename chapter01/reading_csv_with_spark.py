"""Reading CSV with Spark

Example Spark recipe demonstrating several ways to read CSV files:
- infer schema
- provide explicit schema
- handle nulls, empty values and custom date formats

Usage: ensure `pyspark` is available and `JAVA_HOME` is set, then run with Python.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

from pyspark.sql import SparkSession

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter01-ReadCSV")
         .master("local[*]")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Reading CSV data with an inferred schema
df = (spark.read.format("csv")
      .option("header", "true")
      .load('data/input/netflix_titles.csv'))

# Display sa,ple data in the DataFrame
df.show()

# Print schema of DataFrame
df.printSchema()

# Read CSV data with an Explicit schema

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

# Define Schema
schema = StructType([
    StructField("show_id", StringType(), True),
    StructField("type", StringType(), True),
    StructField("title", StringType(), True),
    StructField("director", StringType(), True),
    StructField("cast", StringType(), True),
    StructField("country", StringType(), True),
    StructField("date_added", DateType(), True),
    StructField("release_year", IntegerType(), True),
    StructField("rating", StringType(), True),
    StructField("duration", StringType(), True),
    StructField("listed_in", StringType(), True),
    StructField("description", StringType(), True),])

# Read CSV into DataFrame
df2 = (spark.read.format("csv")
      .option("header", "true")
      .schema(schema)
      .load('data/input/netflix_titles.csv'))

# Display DataFrame content
df2.show()

# Read CSV into DataFrame
df3 = (spark.read.format("csv")
       .option("header", "true")
       .option("nullValue", "null")
       .option("escapeQuotes","true")
       .schema(schema)
       .load('data/input/netflix_titles.csv'))

# Display first 5 rows of DataFrame
df3.show(5)

# Read CSV into DataFrame
df4 = (spark.read.format("csv")
       .option("header", "true")
       .option("nullValue", "null")
       .option("emptyValues","")
       .schema(schema)
       .load('data/input/netflix_titles.csv'))

# Display first 5 rows of DataFrame
df4.show(5)

# Read CSV into DataFrame
df5 = (spark.read.format("csv")
       .option("header", "true")
       .option("nullValue", "null")
       .option("dateFormat","LLLL d, y")
       .schema(schema)
       .load('data/input/netflix_titles.csv'))

# Display rows of DataFrame
df5.show()

# ── End of recipe ──

# Release the resources
spark.stop()
