import pytest
from simplibs.extractor_css.logic._helpers import remove_with_gaps


@pytest.mark.parametrize(
    ("text", "spans", "gaps", "expected"),
    [
        ("a/**/b", [(1, 5)], [(1, 5)], "a b"),
        ("a/**/b", [(1, 5)], [], "ab"),
        ("a/**/b/**/c", [(1, 5), (6, 10)], [(1, 5), (6, 10)], "a b c"),
        ("a/**/b/**/c", [(1, 5), (6, 10)], [(6, 10)], "ab c"),
        ("a/**/b/**/c", [(6, 10), (1, 5)], [(1, 5)], "a bc"),
        ("x\n/**/\ny", [(2, 6)], [], "x\ny"),
        ("abc", [], [], "abc"),
        ("", [], [], ""),
    ],
    ids=["one-gap", "no-gap", "two-gaps", "second-gap-only", "spans-in-any-order", "emptied-line-goes", "no-spans", "empty-text"],
)
def test_the_spans_are_cut_and_a_marked_span_leaves_one_space(text: str, spans: list, gaps: list, expected: str) -> None:
    assert remove_with_gaps(text, spans, gaps) == expected


def test_a_line_that_held_only_a_removed_span_disappears_even_when_other_spans_leave_gaps() -> None:
    assert remove_with_gaps("a/**/b\n/**/\nc", [(1, 5), (7, 11)], [(1, 5)]) == "a b\nc"
