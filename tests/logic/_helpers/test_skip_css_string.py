import pytest
from simplibs.extractor_css.logic._helpers import skip_css_string


@pytest.mark.parametrize(
    ("text", "start", "expected"),
    [
        ('"ab" c', 0, (4, True)),
        ("'a' ", 0, (3, True)),
        ('""', 0, (2, True)),
        ('x "a" y', 2, (5, True)),
        ('"it\'s"', 0, (6, True)),
        ("'say \"x\"'", 0, (9, True)),
        ('"a\\"b" x', 0, (6, True)),
        ('"a\\\nb"', 0, (6, True)),
    ],
    ids=["double", "single", "empty", "after-text", "other-quote-inside", "double-inside-single", "escaped-quote", "escaped-break"],
)
def test_a_closed_string_ends_just_after_its_closing_quote(text: str, start: int, expected: tuple[int, bool]) -> None:
    assert skip_css_string(text, start) == expected


@pytest.mark.parametrize(
    ("text", "start", "expected"),
    [
        ('"abc\nxyz"', 0, (4, False)),
        ('"abc', 0, (4, False)),
        ('"', 0, (1, False)),
        ('"a\\', 0, (3, False)),
    ],
    ids=["break-ends-it", "end-of-text", "only-the-opening", "backslash-at-the-end"],
)
def test_a_string_that_is_not_closed_ends_with_its_line(text: str, start: int, expected: tuple[int, bool]) -> None:
    assert skip_css_string(text, start) == expected
