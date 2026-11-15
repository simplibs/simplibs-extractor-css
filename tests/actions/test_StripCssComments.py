import warnings

from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_css.actions import StripCssComments
from simplibs.extractor_css.logic import strip_css_comments

SAMPLES = ["a{} /* c */\nb{}\n", "plain{}", ""]


def test_strip_css_comments_contract(subtests) -> None:
    assert_action(
        subtests,
        StripCssComments(),
        valid_values=SAMPLES,
        expected_outputs=["a{}\nb{}\n", "plain{}", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=StripCssComments,
        invalid_init_params=[((), {"line_comments": 5}), ((), {"keep_license": None})],
        verbose=False,
    )


def test_strip_css_comments_hands_its_options_to_the_function() -> None:
    assert StripCssComments(line_comments=True)("a{} // x\n") == "a{}\n"
    assert StripCssComments()("a{} // x\n") == "a{} // x\n"
    assert StripCssComments(keep_license=True)("/*! l */\n/* c */\na{}\n") == "/*! l */\na{}\n"
    assert StripCssComments()("/*! l */\n/* c */\na{}\n") == "a{}\n"


def test_strip_css_comments_gives_what_the_function_gives(stylesheet_samples: list[str]) -> None:
    plain, preprocessor, keeping = StripCssComments(), StripCssComments(line_comments=True), StripCssComments(keep_license=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for text in stylesheet_samples:
            assert plain(text) == strip_css_comments(text), repr(text)
            assert preprocessor(text) == strip_css_comments(text, line_comments=True), repr(text)
            assert keeping(text) == strip_css_comments(text, keep_license=True), repr(text)


def test_strip_css_comments_can_be_used_again_and_again() -> None:
    action = StripCssComments()
    first = action("a{} /* c */\nb{}\n")
    assert action("x{} /* d */\ny{}\n") == "x{}\ny{}\n"
    assert action("a{} /* c */\nb{}\n") == first == "a{}\nb{}\n"
