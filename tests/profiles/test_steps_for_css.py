from simplibs.extractor_css.actions import StripCssComments
from simplibs.extractor_css.constants import CSS_LINE_COMMENT_SUFFIXES, CSS_PLAIN_SUFFIXES, CSS_SUFFIXES
from simplibs.extractor_css.profiles.steps_for_css import steps_for_css


def test_each_kind_of_stylesheet_gets_its_own_step() -> None:
    plain, line = StripCssComments(), StripCssComments(line_comments=True)
    steps = steps_for_css(plain, line)
    assert steps[".css"] is plain
    assert steps[".scss"] is line
    assert steps[".less"] is line


def test_the_suffixes_are_those_of_the_stylesheets_in_their_order() -> None:
    steps = steps_for_css(StripCssComments(), StripCssComments(line_comments=True))
    assert list(steps) == list(CSS_SUFFIXES) == [*CSS_PLAIN_SUFFIXES, *CSS_LINE_COMMENT_SUFFIXES]


def test_the_same_step_for_both_kinds_is_allowed() -> None:
    step = StripCssComments()
    steps = steps_for_css(step, step)
    assert set(steps) == set(CSS_SUFFIXES)
    assert all(value is step for value in steps.values())
