import pytest
from simplibs.extractor_css.logic._helpers import CssScan, scan_css


@pytest.mark.parametrize(
    ("text", "comments", "glued", "literals"),
    [
        ("", (), (), ()),
        ("a { b: c }", (), (), ()),
        ("a /* x */ b", ((1, 9),), (), ()),
        ("a/* x */b", ((1, 8),), ((1, 8),), ()),
        ('a { content: "x" }', (), (), ((13, 16),)),
        ("a { b: 'x' }", (), (), ((7, 10),)),
        ("a { b: url(a.png) }", (), (), ((11, 17),)),
        ('a { b: url("a.png") }', (), (), ((11, 18),)),
        ('/* a */ "/* b */" /* c */', ((0, 7), (17, 25)), (), ((8, 17),)),
        ('a { content: "/* no */" }', (), (), ((13, 23),)),
        ("a { b: url(//cdn.example.com/a.png) }", (), (), ((11, 35),)),
    ],
    ids=["empty", "plain-code", "comment", "glued-comment", "double-quoted", "single-quoted", "unquoted-url", "quoted-url", "comment-string-comment", "marks-in-a-string", "slashes-in-a-url"],
)
def test_plain_css_has_comments_and_literals(text: str, comments: tuple, glued: tuple, literals: tuple) -> None:
    assert scan_css(text) == CssScan(comments, glued, literals, ())


@pytest.mark.parametrize(
    ("text", "comments", "literals"),
    [
        ("// x\nb", ((0, 4),), ()),
        ("a // x\nb", ((1, 6),), ()),
        ("a // x", ((1, 6),), ()),
        ("a // /* not a block */\nb", ((1, 22),), ()),
        ("a{b:url(//cdn/a.png)} // x\n", ((21, 26),), ((8, 20),)),
        ('a{b:"//x"} // y\n', ((10, 15),), ((4, 9),)),
    ],
    ids=["whole-line", "after-code", "at-the-end", "block-marks-inside", "slashes-in-a-url", "slashes-in-a-string"],
)
def test_line_comments_are_read_only_when_they_are_asked_for(text: str, comments: tuple, literals: tuple) -> None:
    scan = scan_css(text, line_comments=True)
    assert scan.comments == comments
    assert scan.literals == literals
    assert scan.glued == ()
    assert scan.problems == ()


@pytest.mark.parametrize("text", ["// x\nb", "a // x\nb", "a{b:c} // x"])
def test_double_slashes_are_code_in_plain_css(text: str) -> None:
    assert scan_css(text) == CssScan((), (), (), ())


def test_the_block_comment_is_cut_with_its_blanks_only_when_a_blank_follows() -> None:
    assert scan_css("a /* x */b").comments == ((2, 9),)
    assert scan_css("a /* x */ b").comments == ((1, 9),)


@pytest.mark.parametrize(
    ("text", "comments", "literals", "problems"),
    [
        ("a /* x", ((1, 6),), (), ("a comment on line 1 is not closed; it runs to the end of the file",)),
        ("a{}\n/* x", ((4, 8),), (), ("a comment on line 2 is not closed; it runs to the end of the file",)),
        ('a { b: "x\n}', (), ((7, 9),), ("a string on line 1 is not closed",)),
        ("a{b:url(x\n)}", (), ((8, 9),), ("an address in url( on line 1 is not closed",)),
        (
            "'a\nb{}\n/* c",
            ((7, 11),),
            ((0, 2),),
            ("a string on line 1 is not closed", "a comment on line 3 is not closed; it runs to the end of the file"),
        ),
    ],
    ids=["comment", "comment-on-line-two", "string", "address", "string-then-comment"],
)
def test_damage_is_reported_in_the_order_of_the_file(text: str, comments: tuple, literals: tuple, problems: tuple) -> None:
    scan = scan_css(text)
    assert scan.comments == comments
    assert scan.literals == literals
    assert scan.problems == problems


def test_a_name_that_only_ends_in_url_is_not_an_address() -> None:
    assert scan_css("a { data-url(x): y }").literals == ()
    assert scan_css("a { curl(x): y }").literals == ()


def test_the_keyword_url_is_found_in_any_case() -> None:
    assert scan_css("a { b: URL(x.png) }").literals == ((11, 17),)
