import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter01-XMLData")
         .config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.17.0")
         .master("local[*]")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Read XML file into DataFrame
df = (spark.read.format("com.databricks.spark.xml")
      .option("rowTag", "row")
      .load("data/input/nobel_prizes.xml"))

# Display DataFrame
df.show()

# Access data from DataFrame
df.select("category", "year").show()

# Access data in nested XML
(df.select("category", "year"
          , col("laureates").getItem(0).id).show())

# Flatten nested structures
df_flattened = (
    df
    .withColumn("laureates",explode(col("laureates")))
    .select(col("category"),
            col("year"),
            col("overallMotivation"),
            col("laureates.id"),
            col("laureates.firstname"),
            col("laureates.surname"),
            col("laureates.share"),
            col("laureates.motivation"))
)

df_flattened.show(truncate=False)

# Use Schema to enforce data types
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType(
    [StructField("category", StringType(), True),
     StructField("laureates", ArrayType(StructType(
         [StructField("firstname", StringType(), True),
          StructField("id", StringType(), True),
          StructField("motivation", StringType(), True),
          StructField("share", StringType(), True),
          StructField("surname", StringType(), True)]),
    True), True),
     StructField("overallMotivation", StringType(), True),
     StructField("year", IntegerType(), True)])

# Read XML file into DataFrame
df_with_schema = (spark.read.format("com.databricks.spark.xml")
                  .schema(schema)
                  .option("rowTag", "row")
                  .load("data/input/nobel_prizes.xml"))

# Display schema
df_with_schema.show()

# Release the resources
spark.stop()