import pytest
from simplibs.extractor_css.logic._helpers import blank_spans


@pytest.mark.parametrize(
    ("text", "spans", "expected"),
    [
        ("a /* x */ b", [(2, 9)], "a" + " " * 9 + "b"),
        ("/* a\nb */", [(0, 9)], "    \n    "),
        ("ab cd", [(0, 2), (3, 5)], "     "),
        ("ab cd", [(3, 5), (0, 2)], "     "),
        ("abc", [], "abc"),
        ("abc", [(1, 1)], "abc"),
        ("", [], ""),
    ],
    ids=["one-span", "line-break-kept", "two-spans", "any-order", "no-spans", "empty-span", "empty-text"],
)
def test_the_characters_of_the_ranges_become_blanks_and_the_line_breaks_stay(text: str, spans: list[tuple[int, int]], expected: str) -> None:
    assert blank_spans(text, spans) == expected


@pytest.mark.parametrize("text", ["a /* x */ b", "x\n/* a\nb */\ny", "///"])
def test_the_text_keeps_its_length_and_its_lines(text: str) -> None:
    result = blank_spans(text, [(1, len(text) - 1)])
    assert len(result) == len(text)
    assert result.count("\n") == text.count("\n")
