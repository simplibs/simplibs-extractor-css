import re

import pytest
from simplibs.extractor_css.constants import CSS_LINE_TOKEN_PATTERN, CSS_TOKEN_PATTERN


def test_the_line_token_pattern_is_a_compiled_pattern() -> None:
    assert isinstance(CSS_LINE_TOKEN_PATTERN, re.Pattern)


@pytest.mark.parametrize(
    ("text", "tokens"),
    [
        ("// a comment", ["//"]),
        ('a // b /* c */ "d"', ["//", "/*", '"', '"']),
        ("url(//cdn.example.com/a.png)", ["url(", "//"]),
        ("a { b: c }", []),
        ("data-url(a) curl(b)", []),
        ("URL(a)", ["URL("]),
    ],
    ids=["line-comment", "all-kinds", "url-then-slashes", "plain-code", "lookbehind", "upper-url"],
)
def test_the_line_token_pattern_stops_where_something_may_begin(text: str, tokens: list[str]) -> None:
    assert [found.group() for found in CSS_LINE_TOKEN_PATTERN.finditer(text)] == tokens


def test_only_the_line_pattern_knows_double_slashes() -> None:
    # A plain `.css` file must never have its `//` cut by mistake.
    assert CSS_TOKEN_PATTERN.search("// x") is None
    assert CSS_LINE_TOKEN_PATTERN.search("// x") is not None
