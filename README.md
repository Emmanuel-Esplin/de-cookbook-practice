# De-Cookbook Practice

This repository contains Spark recipes and examples used for learning data engineering concepts.

## Structure Overview

- `chapter01/`, `chapter02/`, `chapter03/`: chapter-specific examples, notebooks, and data folders.
- Each chapter contains `src/main/python` with example scripts demonstrating Spark operations.
- **`examples/`**: Consolidated and cleaned copies of all chapter scripts with normalized filenames (no spaces, snake_case naming).

## What Changed

- Added this `README.md` with a concise repo overview and run notes.
- Added module-level docstrings to chapter Python examples to improve readability and discoverability.
- **Created `examples/` folder** with cleaned filenames for all chapter scripts:
  - `examples/chapter01/`: 12 Python scripts (e.g., `reading_csv_with_spark.py`, `parsing_xml_with_spark_v2.py`)
  - `examples/chapter02/`: 7 Python scripts (e.g., `window_functions_with_spark.py`, `joins_with_spark.py`)
  - `examples/chapter03/`: 2 Python scripts (e.g., `delta_lake_table.py`, `reading_delta_table.py`)

## Run Notes

- Most scripts expect `PySpark` (and for chapter03, `delta-spark`) plus a Java 11+ runtime.
- Set `JAVA_HOME` before running:
  ```bash
  export JAVA_HOME=/path/to/jdk
  python3 examples/chapter01/reading_csv_with_spark.py
  ```

## Using the Examples

All example scripts are self-contained and include:
- A docstring at the top explaining what the script demonstrates.
- `os.environ['JAVA_HOME']` set to a default Java installation path (adjust as needed).
- `pyspark.sql.SparkSession` configuration for local execution.

Run any script directly:
```bash
cd /path/to/de-cookbook-practice
python3 examples/chapter02/window_functions_with_spark.py
```

## Suggested Next Steps

- Add `requirements.txt` with `pyspark` and optional packages (`delta-spark`, `spark-xml`).
- Create `CONTRIBUTING.md` with setup and contribution guidelines.
- Run linting or type checks on Python scripts.
