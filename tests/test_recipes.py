"""Static checks that every recipe follows the repository conventions."""

import ast
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RECIPES = sorted(
    p for p in ROOT.glob("chapter*/src/main/python/chapter*/*.py") if p.name != "__init__.py"
)


def test_recipes_found():
    assert RECIPES, "no recipes found under chapter*/src/main/python/chapter*/"


@pytest.mark.parametrize("recipe", RECIPES, ids=lambda p: str(p.relative_to(ROOT)))
class TestRecipe:
    def test_lives_in_its_chapter_package(self, recipe):
        chapter_module = recipe.relative_to(ROOT).parts[0]
        assert recipe.parent.name == chapter_module

    def test_snake_case_filename(self, recipe):
        assert re.fullmatch(r"[a-z0-9_]+\.py", recipe.name)

    def test_has_module_docstring(self, recipe):
        assert ast.get_docstring(ast.parse(recipe.read_text()))

    def test_stops_spark_session(self, recipe):
        assert "spark.stop()" in recipe.read_text()

    def test_no_machine_specific_settings(self, recipe):
        source = recipe.read_text()
        assert "JAVA_HOME'] =" not in source and 'JAVA_HOME"] =' not in source
        assert not re.search(r"['\"](/Users/|/home/|[A-Za-z]:\\\\)", source)

    def test_no_star_imports(self, recipe):
        tree = ast.parse(recipe.read_text())
        star = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and any(a.name == "*" for a in n.names)]
        assert not star
