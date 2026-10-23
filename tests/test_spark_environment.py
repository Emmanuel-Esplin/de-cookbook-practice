"""Smoke test that the pinned PySpark and Delta Lake versions work together."""

import pytest

pytest.importorskip("pyspark")
pytest.importorskip("delta")

from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


@pytest.fixture(scope="module")
def spark():
    builder = (SparkSession.builder
               .appName("tests-spark-environment")
               .master("local[1]")
               .config("spark.ui.enabled", "false")
               .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
               .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
    session = configure_spark_with_delta_pip(builder).getOrCreate()
    yield session
    session.stop()


def test_delta_round_trip(spark, tmp_path):
    path = str(tmp_path / "delta_table")
    spark.range(5).write.format("delta").save(path)

    assert spark.read.format("delta").load(path).count() == 5
