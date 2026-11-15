import pytest
from simplibs.extractor_css.logic._helpers import needs_gap


@pytest.mark.parametrize(
    ("before", "after"),
    [
        ("a", "b"),
        ("a", "1"),
        ("1", "a"),
        ("-", "a"),
        ("a", "-"),
        ("_", "a"),
        ("é", "x"),
        ("1", "."),
        (".", "1"),
    ],
    ids=["name-name", "name-digit", "digit-name", "hyphen-name", "name-hyphen", "underscore-name", "other-alphabet", "digit-dot", "dot-digit"],
)
def test_a_space_is_left_where_the_two_sides_would_merge(before: str, after: str) -> None:
    assert needs_gap(before, after) is True


@pytest.mark.parametrize(
    ("before", "after"),
    [
        ("{", "a"),
        ("a", "{"),
        (":", "a"),
        ("a", ";"),
        (")", "a"),
        ("}", "{"),
        (" ", "a"),
        ("a", " "),
        ("a", "."),
        (".", "a"),
        ("1", ";"),
        ("/", "1"),
        ("\n", "a"),
    ],
    ids=["brace-name", "name-brace", "colon-name", "name-semicolon", "paren-name", "braces", "blank-name", "name-blank", "name-dot", "dot-name", "digit-semicolon", "slash-digit", "break-name"],
)
def test_nothing_is_left_where_the_two_sides_stay_apart(before: str, after: str) -> None:
    assert needs_gap(before, after) is False
