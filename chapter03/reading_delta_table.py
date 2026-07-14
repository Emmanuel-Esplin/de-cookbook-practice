"""Reading Delta Lake tables

Examples for reading Delta table versions, showing history and time travel queries.

Usage: requires `delta-spark` and `pyspark` with `JAVA_HOME` set.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'
# Import libraries
from delta import configure_spark_with_delta_pip, DeltaTable
from pyspark.sql import SparkSession

# Create a SparkSession object
builder = (SparkSession.builder
           .appName("chapter03-delta-table")
           .master("local[*]")
           .config("spark.executor.memory", "512m")
           .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
           .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark.sparkContext.setLogLevel("WARN")




# Release the resources
spark.stop()
