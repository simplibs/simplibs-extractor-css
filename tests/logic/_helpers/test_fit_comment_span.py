import pytest
from simplibs.extractor_css.logic._helpers import fit_comment_span


@pytest.mark.parametrize(
    ("text", "start", "end", "span"),
    [
        ("a /* x */ b", 2, 9, (1, 9)),
        ("a\t/* x */\tb", 2, 9, (1, 9)),
        ("/* x */ a", 0, 7, (0, 7)),
        ("a /* x */", 2, 9, (1, 9)),
        ("a {}\n/* x */\nb", 5, 12, (5, 12)),
        ("a {} /* x */\nb", 5, 12, (4, 12)),
        ("a{}  /* x */\r\nb", 5, 12, (3, 12)),
        ("a /* x", 2, 6, (1, 6)),
    ],
    ids=["blank-after", "tabs", "at-the-start", "at-the-end", "whole-line", "end-of-line", "crlf", "never-closed"],
)
def test_a_comment_followed_by_a_blank_takes_the_blanks_in_front_of_it_along(text: str, start: int, end: int, span: tuple[int, int]) -> None:
    assert fit_comment_span(text, start, end) == (span, False)


@pytest.mark.parametrize(
    ("text", "start", "end", "expected"),
    [
        ("a/* x */b", 1, 8, ((1, 8), True)),
                ("1/**/.5", 1, 5, ((1, 5), True)),
        ("0/**/auto", 1, 5, ((1, 5), True)),
        ("a{/* x */b:c}", 2, 9, ((2, 9), False)),
        ("a:/* x */b", 2, 9, ((2, 9), False)),
        ("a /* x */b", 2, 9, ((2, 9), False)),
        ("a/**/.b", 1, 5, ((1, 5), False)),
        ("a/* x */;", 1, 8, ((1, 8), False)),
        ("a /* x */;", 2, 9, ((2, 9), False)),
    ],
    ids=["name-name", "digit-dot", "digit-name", "brace-before", "colon-before", "blank-before-name-after", "selector-dot", "semicolon-after", "blank-before-semicolon-after"],
)
def test_a_comment_between_two_tokens_leaves_a_space_only_where_they_would_merge(text: str, start: int, end: int, expected: tuple) -> None:
    assert fit_comment_span(text, start, end) == expected
