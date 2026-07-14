"""Reading JSON with Spark (v2)

Alternative JSON reading examples, flattening nested JSON and extracting fields.

Usage: set `JAVA_HOME` and run with `pyspark` available.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter01-ReadJSON")
         .master("local[*]")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Load JSON dato into DataFrame
df = (spark.read.format("json")
      .option("multiline","true")
      .load("data/input/nobel_prizes.json"))

# View DataFrame Schema
df.printSchema()

# View the DataFrame
df.show()

# Flatten nested structures in JSON
df_flattened = (df
    .withColumn("laureates",explode(col("laureates")))
    .select(col("category"),
            col("year"),
            col("overallMotivation"),
            col("laureates.id"),
            col("laureates.firstname"),
            col("laureates.surname"),
            col("laureates.share"),
            col("laureates.motivation")
            )
    )

# Display Flattened JSON
df_flattened.show(truncate=False)

# Use Schema to enforce data types
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

json_schema = StructType([
    StructField('category', StringType(), True),
    StructField('laureates', ArrayType(StructType(
        [StructField('firstname', StringType(), True),
         StructField('id', StringType(), True),
         StructField('motivation', StructType(), True),
         StructField('share', StringType(), True),
         StructField('surname', StringType(), True),
         ]), True), True),
    StructField('overallMotivation', StringType(), True),
    StructField('year', IntegerType(), True),])

json_df_with_schema = (
    spark.read.format("json")
    .schema(json_schema)
    .option("multiline","true")
    .option("mode", "PERMISSIVE")
    .option("columnNameOfCorruptRecord", "corrupt_record")
    .load("data/input/nobel_prizes.json"))

# Get JSON Object and Tuple functions
from pyspark.sql.functions import get_json_object
from pyspark.sql.types import StringType

# Create DataFrame with JSON sting
df1 = spark.createDataFrame([
    (1, '{"name": "Alice", "age": 25}'),
    (2, '{"name": "Bob", "age": 25}')
], ["id", "json_data"])

# Extract the "name" field from JSON string
name_df = df1.select(get_json_object("json_data", "$.name").alias("name"))

# Cast the extract value to a string
name_str_df = name_df.withColumn("name_str", name_df["name"].cast(StringType()))

# Display DataFrame
name_str_df.show()

from pyspark.sql.functions import json_tuple

# create a DataFrame with JSON string
df2 = spark.createDataFrame([
    (1, '{"name": "Alice", "age": 25}'),
    (2, '{"name": "Bob", "age": 25}')
], ["id", "json_data"])

# Extract the "name" and "age" fields from the JSON string
name_age_df = df2.select(json_tuple("json_data", "name", "age").alias("name", "age"))

# Display DataFrame
name_age_df.show()

# Flatten and Collect list functions
from pyspark.sql.functions import flatten, collect_list

# Create a DataFrame with an array of columns
df3 = spark.createDataFrame([
    (1, [[1, 2], [3, 4], [5, 6]]),
    (2, [[7, 8], [9, 10], [11, 12]])
], ["id", "data"])

# Use collect_list() function to group by specified column
collect_df = df3.select(collect_list("data").alias("data"))
collect_df.show(truncate=False)

# Use flatten function to merge all the elements
flattened_df = collect_df.select(flatten("data").alias("merged_data"))
flattened_df.show(truncate=False)

# Use flatten function with a nested array
from pyspark.sql.functions import explode, flatten, collect_list

# Create a DataFrame with nested array column
df4 = spark.createDataFrame([
    (1, [[[1, 2], [3, 4], [5, 6], [7, 8]]]),
    (2, [[[9, 10], [11, 12], [13, 14], [15, 16]]])
], ["id", "data"])

# Explode the outermost array to flatten the structure
exploded_df = df4.select(col("id"),explode("data").alias("inner_data"))

# Use collect_list to group all the inner arrays together
grouped_df = exploded_df.groupBy("id").agg(collect_list("inner_data").alias("merged_data"))

# Use flatten to merge all the elements of the inner arrays
flattened_df1 = grouped_df.select(flatten("merged_data").alias("final_data"))

flattened_df1.show(truncate=False)

# Release the resources
spark.stop()
