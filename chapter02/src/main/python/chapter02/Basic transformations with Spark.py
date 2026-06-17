import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'
# Import libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import transform, col, concat, lit

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter02-basic-transformations")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Read file
df = (spark.read.format("json")
      .option("multiline","true")
      .load("data/input/nobel_prizes.json"))

# Apply transform function to Numbers column
df_transformed = (
    df.select("category",
              "overallMotivation",
              "year",
              "laureates",
              transform(col("laureates"), lambda x: concat(x.firstname,lit(" "), x.surname))
              .alias("laureates_full_name"))
)

df_transformed.show()

# Drop duplicates from DataFrame
df_deduped = df.dropDuplicates(["category", "overallMotivation", "year"])
df_deduped.show()

# Sort DataFram by applying the orderBy function
df_sorted = df.orderBy("year")
df_sorted.show()

# Sort by year in descending order, then by category in ascending order
df_sorted = df.orderBy(["year", "category"], ascending=[False, True])
df_sorted.show()

# Sort by Age in ascending order, then by Name in descending order
df_sorted = df.sort(["year", "category"], ascending=[False, True])
df_sorted.show()

# Rename columns
df_renamed = df.withColumnRenamed("category", "Topic")
df_renamed.show()

# Use select function rename multiple columns
df_renamed = (
    df.selectExpr("category as Topic", "year as Year", "overallMotivation as Motivation"))
df_renamed.show(5)

# Release the resources
spark.stop()