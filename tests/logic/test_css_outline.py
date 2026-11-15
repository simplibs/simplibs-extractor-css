import warnings

import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import css_outline


def test_the_documented_example() -> None:
    assert css_outline("@media print { .a, .b { color: red; } }") == "@media print\n  .a, .b\n"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (".a {}", ".a\n"),
        (".a { b: c }", ".a\n"),
        (".a { b: c } .d { e: f }", ".a\n.d\n"),
        (".a { .b { c: d } }\n.e {}\n", ".a\n  .b\n.e\n"),
        ("@media print { .a, .b { color: red; } }", "@media print\n  .a, .b\n"),
        ("@font-face { font-family: x }", "@font-face\n"),
        ("@keyframes spin { from { a: b } to { a: c } }", "@keyframes spin\n  from\n  to\n"),
        ("@layer base { .a {} }", "@layer base\n  .a\n"),
        ("@mixin box($x) { .a { b: $x } }", "@mixin box($x)\n  .a\n"),
        (".a:not(.b) > .c ~ .d + .e {}", ".a:not(.b) > .c ~ .d + .e\n"),
        (".a\n,\n.b { c: d }", ".a , .b\n"),
        ("/* c */ .a /* d */ , .b {}", ".a , .b\n"),
        ("@charset \"x\";\n@import 'a';\n.a {}", ".a\n"),
        (".a { @include box; b: c }", ".a\n"),
        (".a-#{$x} { b: c }", ".a-#{$x}\n"),
        ('a[title="{"] { b: c }', 'a[title="{"]\n'),
    ],
    ids=["empty-block", "declarations-are-not-listed", "two-rules", "nested", "media", "font-face", "keyframes", "layer", "mixin", "selector-is-kept-as-it-was", "header-over-lines", "comments-are-dropped", "at-rules-without-a-block", "include-is-not-listed", "interpolation", "brace-in-a-string"],
)
def test_one_line_is_written_for_each_header_that_opens_a_block(text: str, expected: str) -> None:
    assert css_outline(text) == expected


@pytest.mark.parametrize("text", ["", "   \n", "@import 'a';", "a: b;", "/* c */"], ids=["empty", "blanks", "only-an-import", "only-a-declaration", "only-a-comment"])
def test_a_file_with_no_block_gives_an_empty_string(text: str) -> None:
    assert css_outline(text) == ""


@pytest.mark.parametrize(
    ("max_depth", "expected"),
    [
        (None, ".a\n  .b\n    .c\n.d\n"),
        (1, ".a\n.d\n"),
        (2, ".a\n  .b\n.d\n"),
        (3, ".a\n  .b\n    .c\n.d\n"),
        (50, ".a\n  .b\n    .c\n.d\n"),
    ],
    ids=["all", "top-level-only", "two-levels", "three-levels", "more-than-there-is"],
)
def test_the_depth_limit_cuts_off_the_deeper_headers(max_depth: int | None, expected: str) -> None:
    assert css_outline(".a { .b { .c { e: f } } } .d {}", max_depth=max_depth) == expected


@pytest.mark.parametrize("max_depth", [0, -1, -50], ids=["zero", "minus-one", "minus-fifty"])
def test_a_depth_that_is_not_positive_is_refused(max_depth: int) -> None:
    with pytest.raises(ValidationError):
        css_outline(".a {}", max_depth=max_depth)


@pytest.mark.parametrize(
    ("line_comments", "expected"),
    [(True, ".a\n"), (False, "// .x\n  .a\n")],
    ids=["preprocessor", "plain-css"],
)
def test_a_double_slash_hides_a_block_only_in_a_preprocessor(line_comments: bool, expected: str) -> None:
    # In plain CSS the `//` is code, so `// .x` is read as the header of the first block.
    text = "// .x {\n.a {}\n// }\n"
    assert css_outline(text, line_comments=line_comments) == expected


@pytest.mark.parametrize(
    "text",
    [".a {", ".a { .b {", ".a {} }", "} .a {}", ".a {} /* x", '.a { content: "x\n}'],
    ids=["one-open", "two-open", "stray-brace", "stray-brace-first", "comment", "string"],
)
def test_a_damaged_file_comes_back_unchanged_with_a_warning(text: str) -> None:
    with pytest.warns(UserWarning):
        assert css_outline(text) == text


@pytest.mark.parametrize(
    ("text", "message"),
    [(".a {", "1 block(s) are never closed"), (".a {} }", "1 closing brace(s) have no opening one")],
    ids=["open", "stray"],
)
def test_the_warning_says_what_is_wrong_with_the_braces(text: str, message: str) -> None:
    with pytest.warns(UserWarning, match=message.replace("(", r"\(").replace(")", r"\)")):
        css_outline(text)


def test_a_healthy_file_gives_no_warning() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        css_outline(".a { b: c }")


@pytest.mark.parametrize("text", [5, None, b"a", ["a"], 1.5], ids=["int", "None", "bytes", "list", "float"])
def test_a_text_that_is_not_a_str_is_refused(text: object) -> None:
    with pytest.raises(ValidationError):
        css_outline(text)  # type: ignore[arg-type]
