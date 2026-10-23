# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A learning cookbook of Apache Spark recipes organized by chapter (ch01 ingestion/IO, ch02 transformations, ch03 Delta Lake). The real content is standalone PySpark scripts. The Gradle/Scala build is scaffolding for future Scala recipes; there are no Scala sources or tests yet.

## Commands

```bash
pip install -r requirements-dev.txt            # pinned pyspark/delta-spark + pytest/ruff
export JAVA_HOME=$(/usr/libexec/java_home -v 11)

ruff check .                                   # lint (config in pyproject.toml)
pytest                                         # all tests
pytest tests/test_recipes.py -k joins          # checks for one recipe
pytest tests/test_spark_environment.py         # Spark + Delta smoke test (needs JDK 11)
./gradlew build                                # compile Scala modules
./gradlew :chapter01:test                      # one module's ScalaTest suite

# Run a recipe: must be run from inside its chapter dir
cd chapter01 && python src/main/python/chapter01/reading_csv_with_spark.py
```

CI (`.github/workflows/ci.yml`) runs ruff, pytest (Python 3.11, JDK 11) and `./gradlew build`.

## Architecture and conventions

- **One canonical copy per recipe** at `chapterXX/src/main/python/chapterXX/<snake_case>.py`. Do not reintroduce duplicate or `_v2` copies; edit the recipe in place. `tests/test_recipes.py` enforces location, snake_case names, a module docstring, `spark.stop()` at the end, no star imports, and no machine-specific paths or `JAVA_HOME` assignments.
- **Recipe style is notebook-like**: a top-level script that builds a `SparkSession` (`local[*]`, `setLogLevel("WARN")`), then runs commented steps, importing what each step needs next to it (E402 is ignored for this reason). Use explicit `pyspark.sql.functions` imports.
- **Relative data paths.** Scripts read `data/input/...` and write `data/output/...` (Delta: `data/delta_lake/...`) relative to the working directory, hence running from `chapterXX/`. `chapter*/data/` and notebooks are gitignored; datasets are not in the repo.
- **Extra Spark packages.** XML recipes fetch `com.databricks:spark-xml_2.12:0.17.0` via `spark.jars.packages`. Delta recipes use `configure_spark_with_delta_pip` plus the Delta SQL extension/catalog configs.
- **Versions must stay aligned**: `pyspark`/`delta-spark` in `requirements.txt` match `sparkVersion`/`deltaVersion` in root `build.gradle` (Spark 3.4.1, Delta 2.4.0, Scala 2.12). PySpark 3.4 needs `numpy<2` for `pyspark.ml` and the `setuptools` distutils shim on Python 3.12.
- **Gradle.** Root `build.gradle` applies the `scala` plugin to all subprojects and centralizes versions; Java source dirs are disabled in subprojects. To add a chapter, uncomment it in `settings.gradle`, add `chapterXX/build.gradle`, and create the `chapterXX` Python package.

## Git

Use Conventional Commits (`feat:`, `fix:`, `refactor:`, `build:`, `test:`, `ci:`, `docs:`, `chore:`), and work on a branch rather than committing to `master` directly. Never commit datasets, generated output, `*.ipynb`, credentials, or local paths (see `SECURITY.md`).
