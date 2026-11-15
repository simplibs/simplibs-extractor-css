import pytest
from simplibs.extractor_css.logic._helpers import build_outline, scan_css


def outline_of(text: str, max_depth: int | None = None, line_comments: bool = False) -> tuple[list[str], list[str]]:
    return build_outline(text, scan_css(text, line_comments=line_comments), max_depth)


@pytest.mark.parametrize(
    ("text", "lines"),
    [
        (".a {}", [".a"]),
        (".a { b: c }", [".a"]),
        (".a { b: c } .d { e: f }", [".a", ".d"]),
        (".a { .b { c: d } } .e {}", [".a", "  .b", ".e"]),
        ("@media print { .a, .b { color: red; } }", ["@media print", "  .a, .b"]),
        (".a\n,\n.b { c: d }", [".a , .b"]),
        ("@charset \"x\";\n.a {}", [".a"]),
        ("@import 'a';\n@include x;\n.a {}", [".a"]),
        ("/* c */ .a /* d */ , .b {}", [".a , .b"]),
        (".a { /* .hidden { } */ b: c }", [".a"]),
        ('a[title="{"] { b: c }', ['a[title="{"]']),
        (".a-#{$x} { b: c }", [".a-#{$x}"]),
        (".a { b: #{$x}; c: d }", [".a"]),
        ("", []),
        ("@import 'a';", []),
        (".a { b: c }\n", [".a"]),
    ],
    ids=["empty-block", "declarations-are-not-listed", "two-rules", "nested", "media-with-a-rule", "header-over-lines", "at-rule-without-a-block", "imports-and-includes", "comments-in-a-header", "braces-in-a-comment", "brace-in-a-string", "interpolation-in-a-name", "interpolation-in-a-value", "empty-text", "no-block-at-all", "trailing-break"],
)
def test_the_headers_of_the_blocks_are_listed_by_depth(text: str, lines: list[str]) -> None:
    assert outline_of(text) == (lines, [])


@pytest.mark.parametrize(
    ("max_depth", "lines"),
    [
        (None, [".a", "  .b", "    .c", ".d"]),
        (1, [".a", ".d"]),
        (2, [".a", "  .b", ".d"]),
        (3, [".a", "  .b", "    .c", ".d"]),
        (99, [".a", "  .b", "    .c", ".d"]),
    ],
    ids=["all", "top-level-only", "two-levels", "three-levels", "more-than-there-is"],
)
def test_the_depth_limit_cuts_off_the_deeper_headers(max_depth: int | None, lines: list[str]) -> None:
    assert outline_of(".a { .b { .c { e: f } } } .d {}", max_depth=max_depth) == (lines, [])


def test_the_blocks_below_the_limit_still_count_for_the_pairing() -> None:
    assert outline_of(".a { .b { .c { e: f } } } .d {}", max_depth=1)[1] == []


@pytest.mark.parametrize(
    ("text", "problems"),
    [
        (".a {", ["1 block(s) are never closed"]),
        (".a { .b {", ["2 block(s) are never closed"]),
        (".a {} }", ["1 closing brace(s) have no opening one"]),
        ("} }", ["2 closing brace(s) have no opening one"]),
        ("} .a {", ["1 block(s) are never closed", "1 closing brace(s) have no opening one"]),
    ],
    ids=["one-open", "two-open", "one-stray", "two-stray", "both"],
)
def test_braces_that_do_not_pair_up_are_reported(text: str, problems: list[str]) -> None:
    assert outline_of(text)[1] == problems


def test_a_stray_closing_brace_does_not_push_the_depth_below_zero() -> None:
    assert outline_of("} .a {}") == ([".a"], ["1 closing brace(s) have no opening one"])


def test_line_comments_are_blanked_only_when_they_are_read() -> None:
    text = "// .x {\n.a {}"
    assert outline_of(text, line_comments=True) == ([".a"], [])
    assert outline_of(text, line_comments=False)[1] == ["1 block(s) are never closed"]


@pytest.mark.parametrize(
    ("text", "lines"),
    [
        (".a-#{$x;y} { b: c }", [".a-#{$x;y}"]),
        (".a-#{$x, $y} { b: c }", [".a-#{$x, $y}"]),
        (".a-#{$x;} .b { c: d }", [".a-#{$x;} .b"]),
    ],
    ids=["semicolon-inside", "comma-inside", "semicolon-then-more-header"],
)
def test_a_mark_inside_an_interpolation_does_not_split_the_header(text: str, lines: list[str]) -> None:
    assert outline_of(text) == (lines, [])
