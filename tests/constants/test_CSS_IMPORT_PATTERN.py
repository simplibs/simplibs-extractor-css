import re

import pytest
from simplibs.extractor_css.constants import CSS_IMPORT_PATTERN


@pytest.mark.parametrize(
    ("text", "at"),
    [
        ('@import "a";', 0),
        ("@import url(a.css) screen;", 0),
        ('@import (reference) "a";', 0),
        ('@use "a";', 0),
        ('@forward "a";', 0),
        ("  @import 'a';", 2),
        ("\t@import 'a';", 1),
        ('@IMPORT "a";', 0),
        ('@Use "a";', 0),
        ('x;\n@import "a";', 3),
    ],
    ids=["import", "import-url", "less-option", "use", "forward", "spaces", "tab", "upper-import", "mixed-use", "second-line"],
)
def test_the_import_pattern_finds_the_at_sign_of_a_statement_that_begins_a_line(text: str, at: int) -> None:
    found = CSS_IMPORT_PATTERN.search(text)
    assert found is not None
    assert found.start("at") == at


@pytest.mark.parametrize(
    "text",
    [
        '@use-foo "a";',
        '@import-once "a";',
        '@imported "a";',
        '@uses "a";',
        '.a{} @import "a";',
        '@charset "utf-8";',
        "@media print {",
        "/* @import 'a'; */",
        "import 'a';",
        "",
    ],
    ids=["use-foo", "import-once", "imported", "uses", "mid-line", "charset", "media", "in-a-comment-line", "no-at-sign", "empty"],
)
def test_the_import_pattern_leaves_everything_else_alone(text: str) -> None:
    assert CSS_IMPORT_PATTERN.search(text) is None


def test_the_match_may_start_with_blanks_but_the_group_is_the_at_sign() -> None:
    found = CSS_IMPORT_PATTERN.search("  @import 'a';")
    assert found is not None
    assert found.start() == 0
    assert found.start("at") == 2


def test_the_import_pattern_finds_a_statement_on_every_line() -> None:
    text = '@import "a";\n  @use "b";\n.c{}\n@forward "d";\n'
    assert [found.start("at") for found in CSS_IMPORT_PATTERN.finditer(text)] == [0, 15, 30]


def test_the_import_pattern_ignores_case_and_works_per_line() -> None:
    assert CSS_IMPORT_PATTERN.flags & re.IGNORECASE
    assert CSS_IMPORT_PATTERN.flags & re.MULTILINE
