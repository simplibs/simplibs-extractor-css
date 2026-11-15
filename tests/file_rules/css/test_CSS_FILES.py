from pathlib import Path

import pytest
from simplibs.extractor_css.file_rules import CSS_FILES


@pytest.mark.parametrize(
    "path",
    ["a.css", "a.scss", "a.less", "dir/a.css", "A.CSS", "a.Scss", "a.b.css", ".hidden.css", "node_modules/p/a.css"],
    ids=["css", "scss", "less", "in-a-folder", "upper-case", "mixed-case", "dotted-name", "hidden", "dependency"],
)
def test_a_name_with_a_stylesheet_suffix_is_a_stylesheet(path: str) -> None:
    assert CSS_FILES.is_valid(path) is True


@pytest.mark.parametrize(
    "path",
    ["a.sass", "a.js", "a.txt", "a.css.bak", "a", "css", ".css", "a.cssx", "scss/a", "", None, 5, b"a.css"],
    ids=["sass", "javascript", "text", "backup", "no-suffix", "bare-word", "bare-suffix", "longer-suffix", "folder-named-like-a-suffix", "empty", "None", "int", "bytes"],
)
def test_every_other_name_is_not(path: object) -> None:
    assert CSS_FILES.is_valid(path) is False


def test_the_rule_says_which_suffixes_it_takes() -> None:
    assert CSS_FILES.describe() == "suffix one of '.css', '.scss', '.less'"


def test_a_path_object_gives_the_same_answer() -> None:
    assert CSS_FILES.is_valid(Path("src/a.scss")) is True
    assert CSS_FILES.is_valid(Path("src/a.js")) is False
