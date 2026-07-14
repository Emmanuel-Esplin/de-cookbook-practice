
"""Custom UDFs in Spark

Shows how to register and use Python UDFs and pandas UDFs for custom transformations.

Usage: set `JAVA_HOME` and run with `pyspark`.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter02-Custom UDFs in Spark")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Create DataFrame
df = (spark.read.format("json")
      .option("multiLine", "true")
      .load("data/input/nobel_prizes.json"))

df_flattened = (
    df
    .withColumn("laureates", explode(col("laureates")))
    .select(col("category"),
            col("year"),
            col("overallMotivation"),
            col("laureates.id"),
            col("laureates.firstname"),
            col("laureates.surname"),
            col("laureates.share"),
            col("laureates.motivation"))
    .filter(col("laureates.firstname").isNotNull() & col("laureates.surname").isNotNull())
)

# Define Python function
def concat(first_name, last_name):
    return first_name + " " + last_name

# Register the function as a UDF
from pyspark.sql.functions import udf
concat_udf = udf(concat)

# Return UDF type
from pyspark.sql.types import StringType
concat_udf = udf(concat, StringType())

# Apply UDF
df_flattened = df_flattened.withColumn("full_name", concat_udf(df_flattened["firstname"],
                                                               df_flattened["surname"]))

df_flattened.show()

# Using UDFs in Spark SQL
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

# Define a UDF
def square_udf(x):
   return x ** 2

# Register the UDF
spark.udf.register("square", square_udf, IntegerType())

# Create a DataFrame
df = spark.createDataFrame([(1,), (2,), (3,), (4,), (5,)], ["num"])

# Use the registered UDF in a SQL query
df.createOrReplaceTempView("numbers")
result = spark.sql("SELECT num, square(num) AS square_num FROM numbers")

# Show the result
result.show()
# Release the resources
spark.stop()
