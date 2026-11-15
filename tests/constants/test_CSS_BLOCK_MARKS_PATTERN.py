import re

import pytest
from simplibs.extractor_css.constants import CSS_BLOCK_MARKS_PATTERN


def test_the_block_marks_pattern_is_a_compiled_pattern() -> None:
    assert isinstance(CSS_BLOCK_MARKS_PATTERN, re.Pattern)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("a { b: c; }", ["{", ";", "}"]),
        ("a{b:c;d:e}", ["{", ";", "}"]),
        ("{{;;}}", ["{", "{", ";", ";", "}", "}"]),
        ("no marks here", []),
        ("(a) [b] <c> :, ", []),
        ("", []),
    ],
    ids=["spaced", "compact", "repeated", "no-marks", "other-brackets", "empty"],
)
def test_the_block_marks_pattern_finds_only_braces_and_semicolons(text: str, expected: list[str]) -> None:
    assert CSS_BLOCK_MARKS_PATTERN.findall(text) == expected


def test_the_block_marks_pattern_does_not_know_strings() -> None:
    # Whether a mark sits inside a string is the scanner's business, not this pattern's.
    assert CSS_BLOCK_MARKS_PATTERN.findall('content: "{;}"') == ["{", ";", "}"]
