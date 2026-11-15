import warnings

import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import strip_css_comments

SAMPLES = [
    "",
    "a{b:c}",
    "/* c */\na{}\n",
    "a{} /* c */\nb{}\n",
    "a{\n  /* c */\n  b:c\n}\n",
    "a{margin:0/**/auto}",
    "a/**/.b{}",
    "/*! keep */\n/* drop */\na{}\n",
    'a{content:"/* no */"}',
    "a{background:url(//cdn/a.png)}",
]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ""),
        ("a{b:c}", "a{b:c}"),
        ("/* c */\na{}\n", "a{}\n"),
        ("a{} /* c */\nb{}\n", "a{}\nb{}\n"),
        ("a{\n  /* c */\n  b:c\n}\n", "a{\n  b:c\n}\n"),
        ("a /* x */ b", "a b"),
        ("a {/* x */ b: c}", "a { b: c}"),
        ("/* a */ /* b */\nc{}", "c{}"),
        ("a{}\n\n/* c */\n\nb{}\n", "a{}\n\n\nb{}\n"),
        ("/* a * b / c */a{}", "a{}"),
        ("/*\n * many\n * lines\n */\na{}\n", "a{}\n"),
        ("a{content:'é'} /* é */\n", "a{content:'é'}\n"),
    ],
    ids=["empty", "no-comment", "whole-line", "after-code", "indented-whole-line", "between-words", "after-a-brace", "two-in-a-row", "blank-lines-stay", "marks-inside", "many-lines", "other-alphabet"],
)
def test_the_comments_are_taken_out_of_a_stylesheet(text: str, expected: str) -> None:
    assert strip_css_comments(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("a{margin:0/**/auto}", "a{margin:0 auto}"),
        ("a/**/b{}", "a b{}"),
        ("1/**/.5", "1 .5"),
        ("a{b:1./**/5}", "a{b:1. 5}"),
        ("a{b:1/**/;}", "a{b:1;}"),
        ("a{/**/b:c}", "a{b:c}"),
        ("a:/**/b", "a:b"),
        ("a/**/.b{}", "a.b{}"),
    ],
    ids=["value-and-keyword", "two-names", "digit-and-dot", "dot-and-digit", "before-a-semicolon", "after-a-brace", "after-a-colon", "selector-dot-stays-joined"],
)
def test_a_comment_between_two_tokens_leaves_a_space_only_where_they_would_merge(text: str, expected: str) -> None:
    assert strip_css_comments(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        'a{content:"/* no */"}',
        "a{content:'/* no */'}",
        "a{background:url(//cdn.example.com/a.png)}",
        "a{background:url(/*x*/a.png)}",
        'a{background:url("/* x */a.png")}',
        'a{content:"a\\"/* no */"}',
    ],
    ids=["double-quotes", "single-quotes", "slashes-in-a-url", "comment-marks-in-a-url", "marks-in-a-quoted-url", "escaped-quote"],
)
def test_what_looks_like_a_comment_inside_a_string_or_an_address_stays(text: str) -> None:
    assert strip_css_comments(text) == text


@pytest.mark.parametrize(
    ("line_comments", "expected"),
    [(False, "a{b:c} // x\n"), (True, "a{b:c}\n")],
    ids=["plain-css", "preprocessor"],
)
def test_double_slashes_are_a_comment_only_in_a_preprocessor(line_comments: bool, expected: str) -> None:
    assert strip_css_comments("a{b:c} // x\n", line_comments=line_comments) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("// whole line\na{}\n", "a{}\n"),
        ("a{} // x\n// y\nb{}\n", "a{}\nb{}\n"),
        ("a{b:url(//cdn/a.png)} // x\n", "a{b:url(//cdn/a.png)}\n"),
        ('a{b:"//x"} // y\n', 'a{b:"//x"}\n'),
        ("a{} /* block */ // line\n", "a{}\n"),
    ],
    ids=["whole-line", "two-lines", "slashes-in-a-url", "slashes-in-a-string", "both-kinds"],
)
def test_a_preprocessor_loses_its_line_comments_but_not_its_addresses(text: str, expected: str) -> None:
    assert strip_css_comments(text, line_comments=True) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("/*! keep */\n/* drop */\na{}\n", "/*! keep */\na{}\n"),
        ("/* @license MIT */\n/* drop */\na{}\n", "/* @license MIT */\na{}\n"),
        ("/* x @preserve y */\n/* drop */\na{}\n", "/* x @preserve y */\na{}\n"),
        ("/*! one */\n/*! two */\na{}\n", "/*! one */\n/*! two */\na{}\n"),
        ("/* plain */\na{}\n", "a{}\n"),
    ],
    ids=["bang", "license-tag", "preserve-tag", "two-licences", "no-licence"],
)
def test_the_licences_stay_when_they_are_asked_to(text: str, expected: str) -> None:
    assert strip_css_comments(text, keep_license=True) == expected


def test_the_licences_go_by_default() -> None:
    assert strip_css_comments("/*! keep */\na{}\n") == "a{}\n"


def test_a_licence_in_a_preprocessor_is_judged_by_its_words() -> None:
    text = "// @license MIT\n// drop\na{}\n"
    assert strip_css_comments(text, line_comments=True, keep_license=True) == "// @license MIT\na{}\n"


@pytest.mark.parametrize("text", SAMPLES)
def test_a_second_run_changes_nothing(text: str) -> None:
    once = strip_css_comments(text)
    assert strip_css_comments(once) == once


@pytest.mark.parametrize(
    "text",
    ["a{} /* x", "a{}\n/* x\nb{}", 'a { b: "x\n}', "a{b:url(x\n)}", "a /* x */ b /* y"],
    ids=["comment", "comment-over-lines", "string", "address", "good-then-bad"],
)
def test_a_damaged_file_comes_back_unchanged_with_a_warning(text: str) -> None:
    with pytest.warns(UserWarning, match="not closed"):
        assert strip_css_comments(text) == text


def test_a_healthy_file_gives_no_warning() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        strip_css_comments("a{} /* x */ b{}\n")


@pytest.mark.parametrize("text", [5, None, b"a", ["a"], 1.5], ids=["int", "None", "bytes", "list", "float"])
def test_a_text_that_is_not_a_str_is_refused(text: object) -> None:
    with pytest.raises(ValidationError):
        strip_css_comments(text)  # type: ignore[arg-type]
