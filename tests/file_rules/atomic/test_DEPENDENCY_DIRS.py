from pathlib import Path

import pytest
from simplibs.extractor_css.file_rules import DEPENDENCY_DIRS


@pytest.mark.parametrize(
    "path",
    [
        "node_modules/a.css",
        "x/node_modules/y/a.css",
        "bower_components/a.css",
        "vendor/a.css",
        "static/vendor/bootstrap/a.css",
        "node_modules/deep/er/a.css",
    ],
    ids=["node-modules", "in-the-middle", "bower", "vendor", "django-static-vendor", "deep"],
)
def test_a_file_inside_a_folder_of_other_peoples_stylesheets_is_recognized(path: str) -> None:
    assert DEPENDENCY_DIRS.is_valid(path) is True


@pytest.mark.parametrize(
    "path",
    ["a.css", "src/a.css", "my_node_modules/a.css", "vendors/a.css", "node_modules", "x/node_modules", "", None, 5],
    ids=["no-folder", "own-folder", "longer-name", "plural", "the-name-itself", "the-name-itself-in-a-folder", "empty", "None", "int"],
)
def test_every_other_file_is_not(path: object) -> None:
    assert DEPENDENCY_DIRS.is_valid(path) is False


def test_a_path_object_gives_the_same_answer() -> None:
    assert DEPENDENCY_DIRS.is_valid(Path("vendor/a.css")) is True
    assert DEPENDENCY_DIRS.is_valid(Path("src/a.css")) is False
