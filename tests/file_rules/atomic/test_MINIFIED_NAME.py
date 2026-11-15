from pathlib import Path

import pytest
from simplibs.extractor_css.file_rules import MINIFIED_NAME


@pytest.mark.parametrize(
    "path",
    ["app.min.css", "dir/app.min.scss", "a.b.min.css", "app.min.less", "dist/vendor.min.css"],
    ids=["css", "scss", "dotted-stem", "less", "in-a-folder"],
)
def test_a_stem_that_ends_with_dot_min_is_a_minified_file(path: str) -> None:
    assert MINIFIED_NAME.is_valid(path) is True


@pytest.mark.parametrize(
    "path",
    ["app.css", "administration.css", "app.min", "min.css", "app.minified.css", "app.css.min", "dir.min/app.css", "", None, 5],
    ids=["plain", "word-ending-in-min", "no-last-suffix", "no-dot", "longer-word", "min-as-the-suffix", "min-folder", "empty", "None", "int"],
)
def test_every_other_name_is_not(path: object) -> None:
    assert MINIFIED_NAME.is_valid(path) is False


def test_a_path_object_gives_the_same_answer() -> None:
    assert MINIFIED_NAME.is_valid(Path("dir/app.min.css")) is True
    assert MINIFIED_NAME.is_valid(Path("dir/app.css")) is False
