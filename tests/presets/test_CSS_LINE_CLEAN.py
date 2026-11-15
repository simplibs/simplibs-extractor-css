import warnings

from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import strip_css_comments
from simplibs.extractor_css.presets import CSS_LINE_CLEAN
from simplibs.text.presets import CLEANUP_WHITESPACE

SAMPLES = [
    "// banner\n\n@use 'a';\n.a { color: red; } // c   \n\n\n\n.b { margin: 0/**/auto; }  \n",
    ".a{}\n",
    "",
]


def test_css_line_clean_contract(subtests) -> None:
    assert_action(
        subtests,
        CSS_LINE_CLEAN,
        valid_values=SAMPLES,
        expected_outputs=["@use 'a';\n.a { color: red; }\n\n.b { margin: 0 auto; }\n", ".a{}\n", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_css_line_clean_keeps_the_double_slashes_of_an_address() -> None:
    assert CSS_LINE_CLEAN("a{b:url(//x/y.png)} // z\n\n\n") == "a{b:url(//x/y.png)}\n"


def test_css_line_clean_gives_what_its_two_steps_give(stylesheet_samples: list[str]) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for text in stylesheet_samples:
            assert CSS_LINE_CLEAN(text) == CLEANUP_WHITESPACE(strip_css_comments(text, line_comments=True)), repr(text)
