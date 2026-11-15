import re

import pytest
from simplibs.extractor_css.constants import CSS_TOKEN_PATTERN


def test_the_token_pattern_is_a_compiled_pattern() -> None:
    assert isinstance(CSS_TOKEN_PATTERN, re.Pattern)


@pytest.mark.parametrize(
    ("text", "tokens"),
    [
        ('"a" \'b\'', ['"', '"', "'", "'"]),
        ("/* c */", ["/*"]),
        ("url(a.png)", ["url("]),
        ("URL(a.png)", ["URL("]),
        ("x url(a)", ["url("]),
        ("(url(a))", ["url("]),
        ("data-url(a)", []),
        ("curl(a)", []),
        ("_url(a)", []),
        ("// not a token", []),
        ("a { b: c }", []),
        ("*/", []),
    ],
    ids=["quotes", "comment", "url", "upper-url", "after-blank", "after-paren", "hyphen-name", "letter-name", "underscore-name", "double-slash", "plain-code", "comment-end"],
)
def test_the_token_pattern_stops_where_something_may_begin(text: str, tokens: list[str]) -> None:
    assert [found.group() for found in CSS_TOKEN_PATTERN.finditer(text)] == tokens
