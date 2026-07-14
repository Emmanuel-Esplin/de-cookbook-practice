"""Filtering data with Spark

Examples showing predicate filtering, SQL expressions and performance considerations for filtering.

Usage: set `JAVA_HOME` and run with `pyspark`.
"""
import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'
# Import libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import transform, col, concat, lit

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter02-Filtering Data with Spark")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

df = (spark.read.format("csv")
      .option("header", "true")
      .option("nullValue", "null")
      .option("dateFormat", "LLLL, d, y")
      .load("data/input/netflix_titles.csv"))

# Filter the DataFrame
filtered_df = df.filter(col("release_year") > 2000)
filtered_df.printSchema()
filtered_df.show()

# Combine multiple conditions
filtered_df = (
    df.filter(
    (col("country") == "United States")
    & (col("release_year") > 2000)))
filtered_df.show()

# Filter based on a list of values
filtered_df = (
    df.filter(
        col("country")
        .isin(["United States", "United Kingdom", "India"])
    )
)
filtered_df.show()

# Filtering on string
filtered_df = df.filter(col("listed_in").like("%Crime%"))
# Display the filtered DataFrame
filtered_df.show()

# Filter the DataFrame based on a regular expression
filtered_df = df.filter(col("listed_in").rlike("(Crime|Thrillers)"))
# Display the filtered DataFrame
filtered_df.show()

# Filtering on data ranges

# Filter the DataFrame based on a date range
filtered_df = df.filter((col("date_added") >= "2021-02-01") &
                        (col("date_added") <= "2021-03-01"))
# Display the filtered DataFrame
filtered_df.show()

# Filter the DataFrame based on a date range
filtered_df = df.filter((col("date_added").between("2021-02-01", "2021-03-01")))
# Display the filtered DataFrame
filtered_df.show()

# Filtering on arrays

from pyspark.sql.functions import array_contains, col

# Read parquet file into a DataFrame
df_recipes = (spark.read
              .format("parquet")
              .load("data/input/recipes.parquet"))
# Filter the DataFrame based on a value in the array column
filtered_df = df_recipes.filter(array_contains(col("RecipeIngredientParts"), "apple"))

# Display the filtered DataFrame
filtered_df.show()

# Filter on map columns

from pyspark.sql.functions import col, explode

# Read JSON file into a DataFrame
df_nobel_prizes = (spark.read
                   .format("json")
                   .option("multiLine", "true")
                   .load("data/input/nobel_prizes.json"))

df_nobel_prizes_exploded = (
    df_nobel_prizes
    .withColumn("laureates",explode(col("laureates")))
    .select(col("category"),
            col("year"),
