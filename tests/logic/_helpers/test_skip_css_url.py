import pytest
from simplibs.extractor_css.logic._helpers import skip_css_url


@pytest.mark.parametrize(
    ("text", "start", "expected"),
    [
        ("a.png) x", 0, (6, True)),
        ("  a.png)", 0, (8, True)),
        ("\n a.png )", 0, (9, True)),
        ("//cdn/a.png)", 0, (12, True)),
        ("a/*b*/.png)", 0, (11, True)),
        ("a\\).png)", 0, (8, True)),
        (")", 0, (1, True)),
    ],
    ids=["simple", "blanks", "break-and-blanks", "slashes", "comment-marks", "escaped-paren", "empty"],
)
def test_an_unquoted_address_ends_just_after_its_closing_parenthesis(text: str, start: int, expected: tuple[int, bool]) -> None:
    assert skip_css_url(text, start) == expected


@pytest.mark.parametrize(
    ("text", "start"),
    [('"a.png")', 0), (" 'a.png')", 0), ('\n"a.png")', 0)],
    ids=["double", "single-after-a-blank", "after-a-break"],
)
def test_a_quoted_address_is_left_to_the_string_scanner(text: str, start: int) -> None:
    assert skip_css_url(text, start) == (start, True)


@pytest.mark.parametrize(
    ("text", "start", "expected"),
    [
        ("a.png\nb)", 0, (5, False)),
        ("a.png", 0, (5, False)),
        ("  ", 0, (2, False)),
    ],
    ids=["break-ends-it", "end-of-text", "only-blanks"],
)
def test_an_address_that_is_not_closed_ends_with_its_line(text: str, start: int, expected: tuple[int, bool]) -> None:
    assert skip_css_url(text, start) == expected
