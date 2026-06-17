import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'
# Import libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, row_number, lead, lag, count, avg

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter02-Window functions using spark")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Create DataFrame
df = (spark.read
      .format("csv")
      .option("header", "true")
      .option("nullValue", "null")
      .option("dateFormat", "LLLL d, y")
      .load("data/input/netflix_titles.csv"))

# Filter out null from country and date added
df = df.filter(col("country").isNotNull() & col("date_added").isNotNull())

# Define Window function
from pyspark.sql.window import Window
window_spec = Window.partitionBy("country").orderBy("date_added")

# Use row_number window function
#Assign row numbers with each partition
result = df.withColumn("row_number", row_number().over(window_spec))
result.select("title", "country", "date_added", "row_number").show()

# Use the lead and lag window functions
# Add lead column
df = df.withColumn("lead_date_added", lead("date_added").over(window_spec))

# Add lag column
df = df.withColumn("lag_date_added", lag("date_added").over(window_spec))

df.select("title", "country", "date_added", "lead_date_added", "lag_date_added").show(3)

# Nested window functions
from pyspark.sql.functions import sum, lead
from pyspark.sql.window import Window

window_spec = Window.partitionBy("country").orderBy("release_year")
df = df.withColumn("running_total", count("show_id").over(window_spec))

df = df.withColumn("next_running_total", lead("running_total").over(window_spec))

df = df.withColumn("diff", df["next_running_total"] - df["running_total"])
(df.filter(df.next_running_total.isNotNull()).select("show_id", "country", "release_year", "running_total", "next_running_total", "diff").show())

# Window frames
data = [(1, 10), (2, 15), (3, 20), (4, 25), (5, 30)]
df = spark.createDataFrame(data, ["id", "value"])

windowSpec = Window.orderBy("id").rowsBetween(-2, 0)
df = df.withColumn("rolling_avg", avg(df["value"]).over(windowSpec))

df.show()


# Release the resources
spark.stop()