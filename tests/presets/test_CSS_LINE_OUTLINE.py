import warnings

from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import css_outline
from simplibs.extractor_css.presets import CSS_LINE_OUTLINE

SAMPLES = ["// c\n.a { .b {} }\n", "", "@c: red;"]


def test_css_line_outline_contract(subtests) -> None:
    assert_action(
        subtests,
        CSS_LINE_OUTLINE,
        valid_values=SAMPLES,
        expected_outputs=[".a\n  .b\n", "", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_css_line_outline_does_not_see_a_block_inside_a_line_comment() -> None:
    assert CSS_LINE_OUTLINE("// .x {\n.a {}\n// }\n") == ".a\n"


def test_css_line_outline_gives_what_the_function_gives(stylesheet_samples: list[str]) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for text in stylesheet_samples:
            assert CSS_LINE_OUTLINE(text) == css_outline(text, line_comments=True), repr(text)
