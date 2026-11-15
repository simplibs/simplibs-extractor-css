import warnings

import pytest
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import remove_css_imports, strip_css_comments


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ('@import "a.css";\n.a{}\n', ".a{}\n"),
        ("@import url(a.css) screen;\n.a{}\n", ".a{}\n"),
        ("@import 'a', 'b';\n.a{}\n", ".a{}\n"),
        ('@import (reference) "a";\n.a{}\n', ".a{}\n"),
        ('@use "a";\n.a{}\n', ".a{}\n"),
        ('@forward "a";\n.a{}\n', ".a{}\n"),
        ('@use "a";\n@forward "b";\n@import "c";\n.a{}\n', ".a{}\n"),
        ('@IMPORT "a";\n.a{}\n', ".a{}\n"),
        ('  @import "a";\n.a{}\n', ".a{}\n"),
        ('@charset "utf-8";\n@import "a";\n.a{}\n', '@charset "utf-8";\n.a{}\n'),
        ('.a{}\n@import "b";\n.c{}\n', ".a{}\n.c{}\n"),
        ('@import url("a;b.css");\n.c{}\n', ".c{}\n"),
        ('@import "a"\n.b{}\n', ".b{}\n"),
        ('@import "a";\n\n.a{}\n', "\n.a{}\n"),
        ('@import "a";', ""),
        ("", ""),
    ],
    ids=["import", "import-with-a-media", "import-list", "less-option", "use", "forward", "all-three", "upper-case", "indented", "charset-stays", "between-rules", "semicolon-in-a-string", "no-semicolon", "blank-line-stays", "only-an-import", "empty"],
)
def test_the_statements_that_pull_in_other_stylesheets_are_taken_out(text: str, expected: str) -> None:
    assert remove_css_imports(text) == expected


@pytest.mark.parametrize(
    "text",
    [
        '/* @import "a"; */\n.a{}\n',
        '/*\n@import "a";\n*/\n.a{}\n',
        '.a{} @import "b";\n',
        '@use-foo "a";\n.a{}\n',
        '@import-once "a";\n.a{}\n',
        'a{content:"x\\\n@import y;"}\n',
        '// @import "a";\n.a{}\n',
        ".a{}\n",
    ],
    ids=["in-a-comment", "in-a-multiline-comment", "mid-line", "longer-name", "other-name", "in-a-string", "double-slashes", "no-import"],
)
def test_what_is_not_a_statement_in_code_stays(text: str) -> None:
    assert remove_css_imports(text) == text


def test_an_import_in_a_line_comment_stays_in_a_preprocessor_too() -> None:
    text = '// @import "a";\n@import "b";\n.a{}\n'
    assert remove_css_imports(text, line_comments=True) == "// @import \"a\";\n.a{}\n"


def test_the_option_does_not_change_a_stylesheet_without_double_slashes() -> None:
    text = '@use "a";\n.a{}\n'
    assert remove_css_imports(text, line_comments=True) == remove_css_imports(text) == ".a{}\n"


def test_a_comment_in_front_of_a_statement_stays() -> None:
    assert remove_css_imports('/* c */ @import "a";\n.b{}\n') == "/* c */ \n.b{}\n"


@pytest.mark.parametrize(
    "text",
    [
        '/* about */\n@import "a";\n.a{ /* x */ }\n',
        '@use "a"; /* c */\n.a{}\n',
        '@import "a";\n/* c */ @import "b";\n.a{}\n',
    ],
    ids=["comment-around", "comment-after", "comment-in-front-of-a-second"],
)
def test_the_order_of_this_step_and_the_comment_step_does_not_matter(text: str) -> None:
    assert strip_css_comments(remove_css_imports(text)) == remove_css_imports(strip_css_comments(text))


@pytest.mark.parametrize(
    "text",
    ['@import "a";\n.a{}\n', '@use "a";\n@forward "b";\n.a{}\n', ".a{}\n", ""],
)
def test_a_second_run_changes_nothing(text: str) -> None:
    once = remove_css_imports(text)
    assert remove_css_imports(once) == once


@pytest.mark.parametrize(
    "text",
    ['@import "a";\n/* x', '@import "a";\n.a { content: "x\n}', '@import "a";\n.a{b:url(x\n)}'],
    ids=["comment", "string", "address"],
)
def test_a_damaged_file_comes_back_unchanged_with_a_warning(text: str) -> None:
    with pytest.warns(UserWarning, match="not closed"):
        assert remove_css_imports(text) == text


def test_a_healthy_file_gives_no_warning() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        remove_css_imports('@import "a";\n.a{}\n')


@pytest.mark.parametrize("text", [5, None, b"a", ["a"], 1.5], ids=["int", "None", "bytes", "list", "float"])
def test_a_text_that_is_not_a_str_is_refused(text: object) -> None:
    with pytest.raises(ValidationError):
        remove_css_imports(text)  # type: ignore[arg-type]
