import pytest
from simplibs.extractor_css.logic._helpers import find_import_spans, scan_css


def cut_out(text: str) -> list[str]:
    return [text[start:end] for start, end in find_import_spans(text, scan_css(text))]


@pytest.mark.parametrize(
    ("text", "statements"),
    [
        ('@import "a";\n.b{}', ['@import "a";']),
        ("@import url(a.css) screen;\n.b{}", ["@import url(a.css) screen;"]),
        ("@import 'a', 'b';\n.c{}", ["@import 'a', 'b';"]),
        ('@import (reference) "a";\n.b{}', ['@import (reference) "a";']),
        ('@use "a";\n@forward "b";\n.c{}', ['@use "a";', '@forward "b";']),
        ('  @import "a";\n.b{}', ['  @import "a";']),
        ('.a{}\n@import "b";\n.c{}', ['@import "b";']),
        ('@IMPORT "a";\n.b{}', ['@IMPORT "a";']),
        ('@import url("a;b.css");\n.c{}', ['@import url("a;b.css");']),
        ('@import "a"\n.b{}', ['@import "a"']),
        ('@import "a"', ['@import "a"']),
        ('@import "a" {\n.b{}', ['@import "a" {']),
    ],
    ids=["quoted", "url-with-media", "list", "less-option", "use-and-forward", "indented", "after-a-rule", "upper-case", "semicolon-in-a-string", "no-semicolon", "no-semicolon-at-the-end", "brace-ends-by-the-line"],
)
def test_a_statement_runs_from_its_line_start_to_its_semicolon(text: str, statements: list[str]) -> None:
    assert cut_out(text) == statements


@pytest.mark.parametrize(
    "text",
    [
        '/* @import "a"; */\n.b{}',
        '/*\n@import "a";\n*/\n.b{}',
        '.a{} @import "b";\n',
        '@use-foo "a";\n',
        '@charset "utf-8";\n.a{}',
        'a{content:"\\\n@import x;"}',
        "",
        ".a{}",
    ],
    ids=["comment", "comment-over-lines", "mid-line", "longer-name", "other-at-rule", "string-over-lines", "empty", "no-statement"],
)
def test_nothing_is_cut_where_a_statement_cannot_begin(text: str) -> None:
    assert cut_out(text) == []


def test_a_comment_in_front_of_a_statement_stays_out_of_the_cut() -> None:
    assert cut_out('/* c */ @import "a";\n.b{}') == ['@import "a";']


def test_the_cut_starts_at_the_line_start_only_when_blanks_alone_stand_in_front() -> None:
    text = '  @import "a";\n'
    assert find_import_spans(text, scan_css(text)) == [(0, 14)]
    text = '/* c */ @import "a";\n'
    assert find_import_spans(text, scan_css(text)) == [(8, 20)]
