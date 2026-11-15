import warnings

from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_css.actions import CssOutline
from simplibs.extractor_css.logic import css_outline

SAMPLES = [".a { .b {} }", "", "x: y;"]


def test_css_outline_contract(subtests) -> None:
    assert_action(
        subtests,
        CssOutline(),
        valid_values=SAMPLES,
        expected_outputs=[".a\n  .b\n", "", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=CssOutline,
        invalid_init_params=[((), {"max_depth": 0}), ((), {"max_depth": -1}), ((), {"line_comments": 5})],
        verbose=False,
    )


def test_css_outline_hands_its_options_to_the_function() -> None:
    text = "// .x {\n.a { .b {} }\n// }\n"
    assert CssOutline(line_comments=True)(text) == ".a\n  .b\n"
    assert CssOutline(line_comments=True, max_depth=1)(text) == ".a\n"


def test_css_outline_gives_what_the_function_gives(stylesheet_samples: list[str]) -> None:
    plain, preprocessor, shallow = CssOutline(), CssOutline(line_comments=True), CssOutline(max_depth=1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for text in stylesheet_samples:
            assert plain(text) == css_outline(text), repr(text)
            assert preprocessor(text) == css_outline(text, line_comments=True), repr(text)
            assert shallow(text) == css_outline(text, max_depth=1), repr(text)


def test_css_outline_can_be_used_again_and_again() -> None:
    action = CssOutline()
    first = action(".a { .b {} }")
    assert action(".c {}") == ".c\n"
    assert action(".a { .b {} }") == first == ".a\n  .b\n"
