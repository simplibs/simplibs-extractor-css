from pathlib import Path

import pytest
from simplibs.extractor_css.file_rules import DOT_NAME


@pytest.mark.parametrize(
    "path",
    [".hidden.css", ".css", ".gitignore", "src/.hidden.scss", "a/b/.x", "/abs/.hidden.less"],
    ids=["hidden-stylesheet", "bare-suffix", "dot-file", "in-a-folder", "deeper", "absolute"],
)
def test_a_name_that_starts_with_a_dot_is_taken(path: str) -> None:
    assert DOT_NAME.is_valid(path) is True


@pytest.mark.parametrize(
    "path",
    ["a.css", "src/a.css", "dir.x/a.css", "a.b.", "", "src/.git/a.css", None, 5, b".a"],
    ids=["plain", "in-a-folder", "dot-in-a-folder-name", "dot-at-the-end", "empty", "dot-folder-above", "None", "int", "bytes"],
)
def test_any_other_name_is_left_alone(path: object) -> None:
    assert DOT_NAME.is_valid(path) is False


def test_only_the_final_name_counts_and_a_path_object_gives_the_same_answer() -> None:
    assert DOT_NAME.is_valid(Path("src/.hidden.css")) is True
    assert DOT_NAME.is_valid(Path(".dir/a.css")) is False
