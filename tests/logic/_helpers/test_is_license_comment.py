import pytest
from simplibs.extractor_css.logic._helpers import is_license_comment


@pytest.mark.parametrize(
    "comment",
    [
        "/*! keep */",
        "/*!*/",
        "   /*! keep */",
        "\t/*! keep */",
        "/* @license MIT */",
        "/* uses @preserve here */",
        "/*\n * @license\n */",
        "// @license MIT",
    ],
    ids=["bang", "bare-bang", "blanks-in-front", "tab-in-front", "license-tag", "preserve-tag", "tag-on-another-line", "line-comment-with-a-tag"],
)
def test_a_comment_that_tools_keep_is_recognized(comment: str) -> None:
    assert is_license_comment(comment) is True


@pytest.mark.parametrize(
    "comment",
    [
        "/* plain */",
        "/* ! not at the start */",
        "/* a ! b */",
        "/**/",
        "/* license */",
        "/* preserve */",
        "// plain",
    ],
    ids=["plain", "bang-after-a-blank", "bang-inside", "empty", "word-without-at", "other-word-without-at", "line-comment"],
)
def test_every_other_comment_is_not(comment: str) -> None:
    assert is_license_comment(comment) is False
