from pathlib import Path

import pytest
from simplibs.extractor_css.file_rules import OUTPUT_DIRS


@pytest.mark.parametrize(
    "path",
    [
        "build/a.css",
        "dist/a.css",
        "out/a.css",
        ".next/static/a.css",
        ".nuxt/a.css",
        "staticfiles/admin/a.css",
        "coverage/lcov-report/base.css",
        "htmlcov/style.css",
        "storybook-static/a.css",
        "src/dist/a.css",
    ],
    ids=["build", "dist", "out", "next", "nuxt", "django-collectstatic", "coverage", "htmlcov", "storybook", "deeper"],
)
def test_a_file_inside_a_folder_of_generated_files_is_recognized(path: str) -> None:
    assert OUTPUT_DIRS.is_valid(path) is True


@pytest.mark.parametrize(
    "path",
    ["a.css", "static/a.css", "src/a.css", "dist.css", "distribution/a.css", "builds/a.css", "dist", "x/dist", "", None, 5],
    ids=["no-folder", "django-source-folder", "own-folder", "file-named-like-it", "longer-name", "plural", "the-name-itself", "the-name-itself-in-a-folder", "empty", "None", "int"],
)
def test_every_other_file_is_not(path: object) -> None:
    assert OUTPUT_DIRS.is_valid(path) is False


def test_a_path_object_gives_the_same_answer() -> None:
    assert OUTPUT_DIRS.is_valid(Path("dist/a.css")) is True
    assert OUTPUT_DIRS.is_valid(Path("static/a.css")) is False
