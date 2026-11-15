import warnings

import pytest
from simplibs.extractor_css.logic._helpers import find_comments


def comments_of(text: str, **options: bool) -> tuple[list, list]:
    return find_comments(text, **{"line_comments": False, "keep_license": False, **options})


@pytest.mark.parametrize(
    ("text", "comments", "glued"),
    [
        ("", [], []),
        ("a { b: c }", [], []),
        ("a /* x */ b", [(1, 9)], []),
        ("a/**/b", [(1, 5)], [(1, 5)]),
        ("/* a */ b /* c */", [(0, 7), (9, 17)], []),
        ("/*! keep */ /* drop */", [(0, 11), (11, 22)], []),
    ],
    ids=["empty", "no-comment", "one-comment", "glued-comment", "two-comments", "licence-is-cut-by-default"],
)
def test_every_comment_is_chosen_for_cutting_by_default(text: str, comments: list, glued: list) -> None:
    assert comments_of(text) == (comments, glued)


@pytest.mark.parametrize(
    ("text", "comments"),
    [
        ("/*! keep */\n/* drop */\n", [(12, 22)]),
        ("/* @license MIT */\n/* drop */\n", [(19, 29)]),
        ("/* x @preserve y */\n/* drop */\n", [(20, 30)]),
        ("/*! a */ /*! b */", []),
    ],
    ids=["bang", "license-tag", "preserve-tag", "only-licences"],
)
def test_the_licences_are_left_out_when_they_are_to_stay(text: str, comments: list) -> None:
    assert comments_of(text, keep_license=True) == (comments, [])


def test_a_kept_licence_is_taken_out_of_the_glued_ones_too() -> None:
    assert comments_of("a/*! l */b/* c */d", keep_license=True) == ([(10, 17)], [(10, 17)])
    assert comments_of("a/*! l */b/* c */d") == ([(1, 9), (10, 17)], [(1, 9), (10, 17)])


def test_line_comments_are_chosen_only_when_asked_for() -> None:
    assert comments_of("a // x\n") == ([], [])
    assert comments_of("a // x\n", line_comments=True) == ([(1, 6)], [])


def test_a_line_comment_with_a_licence_tag_is_kept_like_a_block_comment() -> None:
    assert comments_of("// @license MIT\n// drop\n", line_comments=True, keep_license=True) == ([(16, 23)], [])


@pytest.mark.parametrize("text", ["a /* x", 'a { b: "x\n}', "a{b:url(x\n)}"])
def test_a_damaged_file_gives_nothing_to_cut_and_a_warning(text: str) -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        assert comments_of(text) == ([], [])
    assert len(caught) == 1
