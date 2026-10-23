# Data Engineering Cookbook

Practical Apache Spark recipes for learning data engineering with Python, Scala, and Gradle. The repository is organized by cookbook chapter; each chapter is a Gradle module whose PySpark recipes live in a Python package of the same name.

**Repository:** [`Emmanuel-Esplin/de-cookbook-practice`](https://github.com/Emmanuel-Esplin/de-cookbook-practice)
**Project slug:** `de-cookbook-practice`

## Project Layout

| Path | Purpose |
| --- | --- |
| `chapter01/` | Data ingestion and extraction: CSV, JSON, Parquet, XML, text, nested data, writing data. |
| `chapter02/` | Transformations, filtering, joins, null handling, aggregations, UDFs, and window functions. |
| `chapter03/` | Delta Lake tables. |
| `chapterXX/src/main/python/chapterXX/` | The chapter's PySpark recipes, one runnable script per recipe. |
| `chapterXX/src/main/scala/`, `chapterXX/src/test/scala/` | Scala recipes and ScalaTest suites (compiled by Gradle). |
| `chapterXX/data/input/`, `chapterXX/data/output/` | Local datasets and generated output. Not published. |
| `chapterXX/notebooks/` | Local notebook workspace. Not published until outputs are reviewed and sanitized. |
| `tests/` | Pytest checks for recipe conventions and the Spark/Delta environment. |
| `build.gradle` | Shared Scala/Spark/Delta versions for all chapter modules. |
| `settings.gradle` | Included chapter modules. |
| `requirements.txt`, `requirements-dev.txt` | Pinned Python runtime and development dependencies. |
| `pyproject.toml` | Ruff and pytest configuration. |

Each recipe has exactly one canonical location: the package of the chapter that owns the topic. Name files in `snake_case`.

## Requirements

- JDK 11, matching the Gradle Java compatibility configured for this project.
- Python 3.9-3.11 (3.12 works with the `setuptools` shim in `requirements.txt`). PySpark and Delta Lake are pinned to the versions in `build.gradle` (Spark 3.4.1, Delta 2.4.0).
- Gradle is provided by the wrapper; a separate Gradle installation is not required.

## Getting Started

```bash
git clone https://github.com/Emmanuel-Esplin/de-cookbook-practice.git
cd de-cookbook-practice
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
export JAVA_HOME=$(/usr/libexec/java_home -v 11)   # macOS; point JAVA_HOME at any JDK 11 elsewhere
```

Recipes read `data/input/...` and write `data/output/...` relative to the working directory, so run them from inside their chapter:

```bash
cd chapter01
python src/main/python/chapter01/reading_csv_with_spark.py
```

Obtain sample data from its original, permitted source and place it under `chapterXX/data/input/`. The XML recipe downloads `com.databricks:spark-xml` at startup, and Delta recipes use `delta-spark`.

## Checks

```bash
ruff check .                                   # lint
pytest                                         # all Python tests
pytest tests/test_recipes.py -k reading_csv    # checks for a single recipe
./gradlew build                                # compile and test Scala modules
```

CI runs the same checks on every push to `master` and on pull requests.

## Data and Secrets

Never commit credentials, private keys, personal or financial data, local datasets, generated output, or notebooks containing cell output. The ignore rules reduce accidental additions, but do not remove files already tracked or protect secrets present in Git history. Review `SECURITY.md` and inspect the staged diff before every push. Revoke and rotate any credential that may have been committed; deleting the file is not sufficient.

## Contributing

Create a focused branch for each change and use [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `refactor:`, `docs:`, `build:`, `test:`, `chore:`). Keep a recipe in one canonical location, and make sure `ruff check .`, `pytest`, and the recipe itself pass before opening a pull request. Do not add data files unless their source, license, and privacy status are clear and publication is explicitly intended.
