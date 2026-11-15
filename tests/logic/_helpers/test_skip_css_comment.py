import pytest
from simplibs.extractor_css.logic._helpers import skip_css_comment


@pytest.mark.parametrize(
    ("text", "start", "expected"),
    [
        ("/* x */ y", 0, (7, True)),
        ("a /* x */ b", 2, (9, True)),
        ("/**/", 0, (4, True)),
        ("/* a\nb */", 0, (9, True)),
        ("/*/ x */", 0, (8, True)),
        ("/* a */ b */", 0, (7, True)),
    ],
    ids=["simple", "after-text", "empty", "multiline", "slash-after-opening", "first-close-wins"],
)
def test_a_closed_comment_ends_just_after_its_first_closing_mark(text: str, start: int, expected: tuple[int, bool]) -> None:
    assert skip_css_comment(text, start) == expected


@pytest.mark.parametrize(
    ("text", "start", "expected"),
    [
        ("a /* x", 2, (6, False)),
        ("/*", 0, (2, False)),
        ("/* a\nb", 0, (6, False)),
    ],
    ids=["text-after-the-opening", "only-the-opening", "multiline"],
)
def test_a_comment_that_is_never_closed_runs_to_the_end_of_the_text(text: str, start: int, expected: tuple[int, bool]) -> None:
    assert skip_css_comment(text, start) == expected
