# Data Engineering Cookbook

Practical Apache Spark recipes for learning data engineering with Python, Scala, and Gradle. The repository is organized by cookbook chapter, with runnable examples kept under `examples/`.

**Repository:** [`Emmanuel-Esplin/de-cookbook-practice`](https://github.com/Emmanuel-Esplin/de-cookbook-practice)
**Project slug:** `de-cookbook-practice`

## Project Layout

| Path | Purpose |
| --- | --- |
| `chapter01/` | Foundational Spark input/output, parsing, and text-processing recipes. |
| `chapter02/` | Transformations, filtering, joins, null handling, aggregations, UDFs, and windows. |
| `chapter03/` | Delta Lake table examples. |
| `chapter*/src/main/python/` | Chapter-specific Python implementations. |
| `chapter*/src/main/scala/` | Chapter-specific Scala implementations. |
| `chapter*/src/test/scala/` | Scala tests for chapter modules. |
| `chapter*/notebooks/` | Local notebook workspace; notebook files are excluded until outputs are reviewed and sanitized. |
| `examples/chapterXX/` | Standalone, directly runnable Python recipe entry points. |
| `src/main/`, `src/test/` | Root-project source and test locations for shared code. |
| `gradle/wrapper/` | Gradle Wrapper configuration and wrapper JAR. |
| `gradlew`, `gradlew.bat` | Reproducible Gradle launchers for macOS/Linux and Windows. |
| `build.gradle` | Shared Gradle plugins, repositories, dependency versions, and Scala/Spark configuration. |
| `settings.gradle` | Root project name and included chapter modules. |
| `.gitignore` | Excludes local data, credentials, environments, notebooks, and generated files. |
| `SECURITY.md` | Security reporting and sensitive-data handling policy. |

Keep new recipes in the chapter that owns the topic. Use `examples/` for standalone entry points; link to an existing implementation instead of copying the same recipe into another location.

## Requirements

- JDK 11, matching the Gradle Java compatibility configured for this project.
- Python and PySpark for Python examples. Use the Spark version declared in `build.gradle` (currently Spark 3.4.1); some recipes need additional Spark packages such as Delta Lake or Spark XML.
- Gradle is provided by the wrapper; a separate Gradle installation is not required.

## Getting Started

```bash
git clone https://github.com/Emmanuel-Esplin/de-cookbook-practice.git
cd de-cookbook-practice
./gradlew projects
./gradlew test
```

Run a standalone Python recipe after installing its dependencies and setting `JAVA_HOME` to a local JDK 11 installation:

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
cd chapter01
python3 ../examples/chapter01/reading_csv_with_spark.py
```

Recipe-specific package requirements and input paths may vary. Review the selected script before running it and obtain any required sample data from its original, permitted source. Place local inputs under `chapter*/data/input/`; generated output belongs under `chapter*/data/output/`. These directories are intentionally not published.

## Data and Secrets

Never commit credentials, private keys, personal or financial data, local datasets, generated output, or notebooks containing cell output. The ignore rules reduce accidental additions, but do not remove files already tracked or protect secrets present in Git history. Review `SECURITY.md` and inspect the staged diff before every push. Revoke and rotate any credential that may have been committed; deleting the file is not sufficient.

## Contributing

Create a focused branch for each change, keep a recipe in one canonical location, and run the relevant Gradle task or Python example before opening a pull request. Do not add data files unless their source, license, and privacy status are clear and publication is explicitly intended.
