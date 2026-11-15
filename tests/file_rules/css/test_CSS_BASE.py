from pathlib import Path

import pytest
from simplibs.extractor_css.file_rules import CSS_BASE


@pytest.mark.parametrize(
    "path",
    ["a.css", "src/a.scss", "dir/theme/b.less", "THEME.CSS", "node_modules/p/a.css", "dist/app.min.css", ".github/a.css", "static/vendor/a.css"],
    ids=["css", "scss", "less", "upper-case", "dependency", "minified", "dot-folder", "vendor"],
)
def test_every_stylesheet_that_is_not_hidden_is_taken(path: str) -> None:
    assert CSS_BASE.is_valid(path) is True


@pytest.mark.parametrize(
    "path",
    [".hidden.css", "src/.hidden.scss", ".css", "a.js", "readme.md", "a.sass", "noext", "", None, 5],
    ids=["hidden", "hidden-in-a-folder", "bare-suffix", "javascript", "markdown", "sass", "no-suffix", "empty", "None", "int"],
)
def test_a_hidden_file_and_anything_that_is_not_a_stylesheet_is_left_out(path: object) -> None:
    assert CSS_BASE.is_valid(path) is False


def test_the_base_rule_does_not_leave_out_minified_or_generated_files() -> None:
    # That is the job of CSS_STRICT_EXCLUDE; the base rule takes them.
    assert CSS_BASE.is_valid("app.min.css") is True
    assert CSS_BASE.is_valid("dist/a.css") is True


def test_a_path_object_gives_the_same_answer() -> None:
    assert CSS_BASE.is_valid(Path("src/a.scss")) is True
    assert CSS_BASE.is_valid(Path("src/.a.scss")) is False
