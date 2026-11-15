from pathlib import Path

import pytest
from simplibs.extractor_css.file_rules import VCS_DIRS


@pytest.mark.parametrize(
    "path",
    [".git/x.css", "a/.svn/x.css", ".hg/x.css", ".bzr/x.css", ".git/hooks/deep/x.css"],
    ids=["git", "svn-in-a-folder", "hg", "bzr", "deep"],
)
def test_a_file_inside_a_version_control_folder_is_recognized(path: str) -> None:
    assert VCS_DIRS.is_valid(path) is True


@pytest.mark.parametrize(
    "path",
    ["a.css", ".github/x.css", ".gitignore", "git/x.css", "x/.git", ".gitlab/a.css", "", None, 5],
    ids=["no-folder", "github-folder", "dot-file", "no-dot", "the-name-itself", "gitlab-folder", "empty", "None", "int"],
)
def test_every_other_file_is_not(path: object) -> None:
    assert VCS_DIRS.is_valid(path) is False


def test_a_path_object_gives_the_same_answer() -> None:
    assert VCS_DIRS.is_valid(Path(".git/x.css")) is True
    assert VCS_DIRS.is_valid(Path("src/x.css")) is False
