import pytest
from simplibs.extractor_css.logic._helpers import line_of


@pytest.mark.parametrize(
    ("text", "offset", "line"),
    [
        ("", 0, 1),
        ("abc", 0, 1),
        ("abc", 2, 1),
        ("a\nb", 1, 1),
        ("a\nb", 2, 2),
        ("a\nb\nc", 4, 3),
        ("\n\n", 2, 3),
    ],
    ids=["empty", "first-character", "same-line", "at-the-break", "second-line", "third-line", "after-two-breaks"],
)
def test_the_line_is_one_more_than_the_breaks_in_front_of_the_offset(text: str, offset: int, line: int) -> None:
    assert line_of(text, offset) == line
