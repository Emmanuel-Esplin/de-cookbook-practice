"""Processing text data with Spark

Example showing how to read and process text files using Spark transformations.

Usage: set `JAVA_HOME` and run using Python with `pyspark`.
"""

import os
os.environ['JAVA_HOME'] = '/Users/emmanuel/Library/Java/JavaVirtualMachines/temurin-11.0.30/Contents/Home'

import setuptools
import distutils

from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Create a SparkSession object
spark = (SparkSession.builder
         .appName("chapter01-text-processing")
         .master("local[*]")
         .config("spark.executor.memory", "512m")
         .getOrCreate())

spark.sparkContext.setLogLevel("WARN")

# Load data into DataFrame
df = (spark.read.format("csv")
      .option("header", "true")
      .option("multiLine", "true")
      .load("data/input/Reviews.csv"))

# Explore DataFrame
df.show(10, truncate=False)

# Apply regular expression to remove all non-alphabetic characters
df_clean = (df
            .withColumn("Text", regexp_replace("Text", "[^a-zA-Z ]", ""))
            .withColumn("Text", regexp_replace("Text", " +", " ")))

df_clean.show()

df_with_words = (df_clean.withColumn("words", split(df_clean.Text, "\\\\s+")))
df_with_words.show()

from pyspark.ml.feature import Tokenizer
# Tokenize the text data
tokenizer = Tokenizer(inputCol='Text', outputCol='words')
df_with_words = tokenizer.transform(df_clean)
df_with_words.show()

# Remove stop words
from pyspark.ml.feature import StopWordsRemover

remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
df_stop_words_removed = remover.transform(df_with_words)
df_stop_words_removed.show()

# Compute the word frequency
df_exploded = (df_stop_words_removed
               .select(explode(df_stop_words_removed.filtered_words).alias("word")))
word_count = (df_exploded
              .groupBy("word")
              .count()
              .orderBy("count", ascending=False))
word_count.show(n=100)

# Convert text data into numerical Machine Learning (ML)
from pyspark.ml.feature import CountVectorizer

# Convert the text data into numerical features
vectorizer = CountVectorizer(inputCol="filtered_words", outputCol="features")
vectorizer_data = vectorizer.fit(df_stop_words_removed).transform(df_stop_words_removed)
vectorizer_data.show(10, truncate=False)

# Save the procesed data
(vectorizer_data.repartition(1)
 .write.mode("overwrite")
 .json("data/output/data_lake/reviews_vectorized.json"))

# Using the regexp_extract function
from pyspark.sql.functions import regexp_extract

# Extract all the starting with "q"
df_q_words = (vectorizer_data
              .withColumn("q_words", regexp_extract("text", "\\\\bq\\\\w*", 0)))
df_q_words.show()

# Using the rlike function
# Check if the text data contains the word "good"
df_good_word = (vectorizer_data
                .withColumn("contains_good", expr("text rlike 'quick'")))
df_good_word.show()

# Customizing stop words
custom_stopwords = ["/><br", "-", "/>I", "/>The"]
stop_words_remover = StopWordsRemover(inputCol="words", outputCol="filtered_words", stopWords=custom_stopwords)
df_stop_words_removed = stop_words_remover.transform(df_with_words)
df_stop_words_removed.show()

# Release the resources
spark.stop()
