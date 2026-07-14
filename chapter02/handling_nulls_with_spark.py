"""Handling nulls with Spark

Examples showing `dropna`, `fillna`, and SQL expressions to handle missing values.

Usage: set `JAVA_HOME` and run with `pyspark`.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'
# Import libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, when

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter02-Handling-Nulls with Spark")
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
)

# Drop Null values
# Dropping rows with null values
df_dropna = df_flattened.dropna()

# Displaying the DataFrame after dropping null values
df_dropna.show()

# Fill null values
# Filling null values with a specific value
df_fillna = df_flattened.fillna("N/A")

# Displaying the DataFrame after filling null values
df_fillna.show()

# Replace null values based on conditions
df_replace = (
    df_flattened.withColumn("category", when(col("category").isNull(),
                                        "").otherwise(col("category")))
    .withColumn("overallMotivation", when(col("overallMotivation").isNull(),
                                     "").otherwise(col("overallMotivation")))
    .withColumn("firstname", when(col("firstname").isNull(),
                             "").otherwise(col("firstname")))
    .withColumn("surname", when(col("surname").isNull(),
                            "").otherwise(col("surname")))
    .withColumn("year", when(col("year").isNull(),
                        9999).otherwise(col("year")))
)

# Displaying the DataFrame after replacing null values
df_replace.show()

# Handling null values in UDF
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Sample DataFrame with null values
data = [("john", 25), ("Alice", None), ("Bob", 30)]
df = spark.createDataFrame(data, ["name", "age"])

# Define a UDF to handle null values
def process_name(name):
    if name is None:
        return "Unknown"
    else:
        return name.upper()

# Register the UDF
process_name_udf = udf(process_name, StringType())

# Apply the UDF to the DataFrame
df_with_processed_names = df.withColumn("processedName", process_name_udf(df["name"]))
df_with_processed_names.show()

# Handling null values in machine learning pipelines
from pyspark.sql import SparkSession
from pyspark.ml.feature import Imputer

# Create a sample DataFrame with missing Values
data2 = [
    (1, 2.0),
