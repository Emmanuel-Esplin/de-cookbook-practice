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

spark.sql("DROP TABLE IF EXISTS default.netflix_titles")

# Create a Delta table
spark.sql("""CREATE TABLE default.netflix_titles (
    show_id STRING,
    type STRING,
    title STRING,
    director STRING,
    cast STRING,
    country STRING,
    date_added STRING,
    release_date STRING,
    rating STRING,
    duration STRING,
    listed_in STRING,
    description STRING
) USING DELTA LOCATION 'data/delta_lake/netflix_titles';""")

# Load CSV
df = (spark.read
      .format("csv")
      .option("header", "true")
      .load("data/input/netflix_titles.csv"))

df.printSchema()

# Write to Delta
df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("default.netflix_titles")

# Query the table
spark.sql("SELECT * FROM default.netflix_titles LIMIT 3").show()


# Release the resources
spark.stop()