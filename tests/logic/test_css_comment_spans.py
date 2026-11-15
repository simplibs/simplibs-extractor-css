import warnings

import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import css_comment_spans


@pytest.mark.parametrize(
    ("text", "spans"),
    [
        ("", []),
        ("a { b: c }", []),
        ("a /* x */ b", [(1, 9)]),
        ("a/**/b", [(1, 5)]),
        ("/* a */ b /* c */", [(0, 7), (9, 17)]),
        ('a { content: "/* no */" }', []),
        ("a { background: url(//cdn/a.png) }", []),
        ("a { background: url(/*x*/a.png) }", []),
    ],
    ids=["empty", "no-comment", "one", "glued-one-is-reported-too", "two", "in-a-string", "slashes-in-a-url", "comment-marks-in-a-url"],
)
def test_the_spans_of_the_comments_are_reported_from_the_blanks_in_front_of_them(text: str, spans: list[tuple[int, int]]) -> None:
    assert css_comment_spans(text) == spans


def test_a_span_is_the_text_of_the_comment_with_the_blanks_in_front() -> None:
    text = "a{} /* x */\nb{}\n"
    [(start, end)] = css_comment_spans(text)
    assert text[start:end] == " /* x */"


@pytest.mark.parametrize(
    ("text", "keep_license", "spans"),
    [
        ("/*! l */ /* c */", False, [(0, 8), (8, 16)]),
        ("/*! l */ /* c */", True, [(8, 16)]),
        ("/* @license x */\n/* c */\n", True, [(17, 24)]),
        ("/* @preserve */\n/* c */\n", True, [(16, 23)]),
        ("/*! only */", True, []),
    ],
    ids=["licence-listed-by-default", "bang-kept", "license-tag-kept", "preserve-tag-kept", "only-a-licence"],
)
def test_the_licences_are_left_out_only_when_asked_for(text: str, keep_license: bool, spans: list[tuple[int, int]]) -> None:
    assert css_comment_spans(text, keep_license=keep_license) == spans


@pytest.mark.parametrize(
    ("line_comments", "spans"),
    [(False, []), (True, [(1, 6)])],
    ids=["plain-css", "preprocessor"],
)
def test_line_comments_are_spans_only_in_a_preprocessor(line_comments: bool, spans: list[tuple[int, int]]) -> None:
    assert css_comment_spans("a // x\nb", line_comments=line_comments) == spans


@pytest.mark.parametrize("text", ["a /* x", 'a { b: "x\n}', "a{b:url(x\n)}"], ids=["comment", "string", "address"])
def test_a_damaged_file_has_no_spans_and_gives_a_warning(text: str) -> None:
    with pytest.warns(UserWarning, match="not closed"):
        assert css_comment_spans(text) == []


@pytest.mark.parametrize(
    "text",
    ["", "/*", "*/", '"', "'", "url(", "//", "{{{", "}}}", "\x00", "a\r\nb /* c", "/*/", "\\", "😀 /* 😀 */"],
)
def test_whatever_the_text_is_it_gets_a_list_and_no_exception(text: str) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert isinstance(css_comment_spans(text, line_comments=True), list)
        assert isinstance(css_comment_spans(text), list)


@pytest.mark.parametrize("text", [5, None, b"a", ["a"], 1.5], ids=["int", "None", "bytes", "list", "float"])
def test_a_text_that_is_not_a_str_is_refused(text: object) -> None:
    with pytest.raises(ValidationError):
        css_comment_spans(text)  # type: ignore[arg-type]
