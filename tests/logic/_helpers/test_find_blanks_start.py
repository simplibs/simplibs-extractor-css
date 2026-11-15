import pytest
from simplibs.extractor_css.logic._helpers import find_blanks_start


@pytest.mark.parametrize(
    ("text", "position", "expected"),
    [
        ("a  b", 3, 1),
        ("a\t\tb", 3, 1),
        ("a \t b", 4, 1),
        ("  x", 2, 0),
        ("x", 0, 0),
        ("ab", 1, 1),
        ("a\n  b", 4, 2),
        ("a\r\n  b", 5, 3),
    ],
    ids=["spaces", "tabs", "mixed", "to-the-start", "at-the-start", "no-blanks", "stops-at-a-break", "stops-at-a-crlf"],
)
def test_the_run_of_spaces_and_tabs_in_front_of_a_position_is_walked_back(text: str, position: int, expected: int) -> None:
    assert find_blanks_start(text, position) == expected
