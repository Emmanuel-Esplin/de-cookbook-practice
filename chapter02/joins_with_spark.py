
# Import libraries
"""Joins with Spark

Demonstrates inner, left, right, full and cross joins, plus broadcast joins for small tables.

Usage: set `JAVA_HOME` and run with `pyspark`.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'
import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter02-joins-with-spark")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

#Create DataFrame
cards_df = (spark.read.format("csv")
            .option("header", "true")
            .option("nullValue", "null")
            .load("data/input/Credit Card/CardBase.csv"))

customers_df = (spark.read.format("csv")
                .option("header", "true")
                .option("nullValue", "null")
                .load("data/input/Credit Card/CustomerBase.csv"))

transaction_df = (spark.read.format("csv")
                  .option("header", "true")
                  .option("nullValue", "null")
                  .load("data/input/Credit Card/TransactionBase.csv"))

fraud_df = (spark.read.format("csv")
            .option("header", "true")
            .option("nullValue", "null")
            .load("data/input/Credit Card/FraudBase.csv"))

# Inner join
customer_cards_df = (
    cards_df.join(customers_df,
                  on='Cust_ID', how='inner'))
customer_cards_df.show()

# Left outer join
joined_transactions_df = (
    transaction_df.join(fraud_df,
                        on='Transaction_ID', how='left_outer'))
joined_transactions_df.show()

# Joins with complex conditions
joinExpr = (
    (customer_cards_df["Card_Number"] == joined_transactions_df["Credit_Card_ID"])
      & (joined_transactions_df["Fraud_Flag"].isNotNull()))

customer_with_fraud_df = (
    customer_cards_df.join(joined_transactions_df,
     on=joinExpr, how='inner'))
customer_with_fraud_df.show()

# Right outer join
data1 = [("Alice", "F", 25), ("Bob", "M", 30), ("Charlie", "M", 35), ("Dave", "M", 40)]
df1=spark.createDataFrame(data1, ["Name", "Gender", "Age"])

data2 = [("Charlie", "M"), ("Dave", "M"), ("Eve", "F")]
df2 = spark.createDataFrame(data2, ["Name", "Gender"])

right_join = df1.join(df2, on='Name', how='right_outer')
right_join.show()

# Full outer join
full_join = df1.join(df2, on='Name', how='outer')
full_join.show()

# Cross join
cross_join = df1.crossJoin(df2)
cross_join.show()

# Broadcast join
broadcast_join = df1.join(broadcast(df2), ["Name", "Gender"], "inner")
broadcast_join.show()

# Multiple join condition
multi_join = df1.join(df2, on=["Name", "Gender"], how="inner")
multi_join.show()

# Release the resources
spark.stop()
