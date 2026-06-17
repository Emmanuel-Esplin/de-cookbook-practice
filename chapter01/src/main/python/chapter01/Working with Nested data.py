import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter01-Nested-DataFrame")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Load DataFrame
df = (spark.read.format("json")
      .option("multiLine", "true")
      .load("data/input/Stanford Question Answering Dataset.json"))

# Explode nested data
df_exploded = (
    df.select("title",
            explode("paragraphs").alias("paragraphs"))
    .select("title",
            col('paragraphs.context').alias("context"),
            explode(col("paragraphs.qas")).alias("questions")))

# Display DataFrame
df_exploded.show()

# Get unique values with array
df_array_distinct = (
    df_exploded.select("title", "context"
                       ,col("questions.id").alias("question_id")
                       ,col("questions.question").alias("question_text")
                       ,col("questions.answers").alias("answers"))
)

# Display unique array
df_array_distinct.show()

# Dot notation with deeply nested data structures
(df_array_distinct
 .select("title", "context", "question_text",
         col("answers").getItem(0).getField("text"))
 .show())

# Nested data with Null values
(df_array_distinct
 .filter(col("answers").getItem(0).getField("text").isNotNull()).show())

# Array contains function
from pyspark.sql.functions import array_contains

df1 = spark.createDataFrame(
    [(["apple", "orange", "banana"],),
     (["grape", "kiwi", "melon"],),
     (["mango", "pineapple", "orange"],)],
    ["fruits"])
(df1.select("fruits"
            ,array_contains("fruits", "orange")
            .alias("contains_orange"))
 .show(truncate=False))

# Map key and value functions
from pyspark.sql.functions import map_keys

spark = (SparkSession.builder.appName("map_keys_example").getOrCreate())

data = [
    {"user_info": {"name": "Alice", "age": 28, "email": "alice@example.com"}},
    {"user_info": {"name": "Bob", "age": 25, "email": "bob@example.com"}},
    {"user_info": {"name": "Charlie", "age": "40", "email": "charlie@example.com"}}
]

df2 = spark.createDataFrame(data)
df2.show(truncate=False)

# Map key function
(df2.select("user_info",
            map_keys("user_info").alias("user_info_keys"),
            map_values("user_info").alias("user_info_values"))
 .show(truncate=False))

# Explode outer function
data1 = [
    {"words": ["hello", "world"]},
    {"words": ["foo", "bar", "baz"]},
    {"words": None}
]

df3 = spark.createDataFrame(data1)
(df3.select(explode_outer("words").alias("word")).show(truncate=False))

# Release the resources
spark.stop()