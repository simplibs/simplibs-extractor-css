import importlib
from pathlib import Path

import pytest

PACKAGE_NAME = "extractor_css"

package = importlib.import_module(f"simplibs.{PACKAGE_NAME}")

EXPECTED: set[str] = {
    # Steps
    "css_comment_spans", "css_outline", "remove_css_imports", "strip_css_comments",
    # Add-on of the extractor
    "register_all",
}

SUBPACKAGES: set[str] = {"actions", "constants", "file_rules", "logic", "plugin", "presets", "profiles"}

CALLABLES: tuple[str, ...] = ("css_comment_spans", "css_outline", "remove_css_imports", "strip_css_comments", "register_all")
CLASSES: tuple[str, ...] = ()

# The sub-packages that have an `__all__` of their own, written out by hand.
DOMAINS: dict[str, set[str]] = {
    "actions": {"CssOutline", "RemoveCssImports", "StripCssComments"},
    "file_rules": {"DEPENDENCY_DIRS", "DOT_NAME", "MINIFIED_NAME", "OUTPUT_DIRS", "VCS_DIRS", "CSS_BASE", "CSS_FILES", "CSS_STRICT_EXCLUDE"},
    "presets": {"CSS_LINE_CLEAN", "CSS_LINE_NO_IMPORTS", "CSS_LINE_OUTLINE", "CSS_PLAIN_CLEAN", "CSS_PLAIN_NO_IMPORTS", "CSS_PLAIN_OUTLINE"},
    "profiles": {"CSS_CODE_CLEAN", "CSS_CODE_NO_IMPORTS", "CSS_DATA_ALL", "CSS_OUTLINE", "CSS_PROFILES", "CSS_SRC_CLEAN"},
}


def test_the_public_names_are_exactly_the_agreed_ones() -> None:
    assert set(package.__all__) == EXPECTED


def test_no_name_is_listed_twice() -> None:
    assert len(package.__all__) == len(set(package.__all__))


@pytest.mark.parametrize("name", sorted(EXPECTED))
def test_every_public_name_exists(name: str) -> None:
    assert hasattr(package, name)


def test_a_star_import_brings_exactly_the_public_names() -> None:
    namespace: dict = {}
    exec(f"from simplibs.{PACKAGE_NAME} import *", namespace)
    namespace.pop("__builtins__")
    assert set(namespace) == EXPECTED


def test_nothing_else_is_public() -> None:
    # Besides the public names, the package shows only its own sub-packages.
    public = {name for name in dir(package) if not name.startswith("_")}
    assert public - set(package.__all__) <= SUBPACKAGES


@pytest.mark.parametrize("name", CALLABLES)
def test_the_functions_are_callable(name: str) -> None:
    assert callable(getattr(package, name))


def test_the_steps_are_the_very_functions_of_the_logic_package() -> None:
    logic = importlib.import_module(f"simplibs.{PACKAGE_NAME}.logic")
    for name in ("css_comment_spans", "css_outline", "remove_css_imports", "strip_css_comments"):
        assert getattr(package, name) is getattr(logic, name), name


def test_register_all_is_the_very_function_of_the_plugin_package() -> None:
    plugin = importlib.import_module(f"simplibs.{PACKAGE_NAME}.plugin")
    assert package.register_all is plugin.register_all


@pytest.mark.parametrize("domain", sorted(DOMAINS))
def test_a_sub_package_lists_exactly_its_agreed_names(domain: str) -> None:
    module = importlib.import_module(f"simplibs.{PACKAGE_NAME}.{domain}")
    assert set(module.__all__) == DOMAINS[domain]
    assert len(module.__all__) == len(set(module.__all__))
    assert all(hasattr(module, name) for name in module.__all__)


def test_the_package_is_marked_as_typed() -> None:
    assert (Path(package.__file__).parent / "py.typed").is_file()
