import warnings

from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import strip_css_comments
from simplibs.extractor_css.presets import CSS_PLAIN_CLEAN
from simplibs.text.presets import CLEANUP_WHITESPACE

SAMPLES = [
    "/* banner */\n\n\n@import 'a.css';\n.a { color: red; } /* c */   \n\n\n\n.b { margin: 0/**/auto; }  \n\n",
    ".a{}\n",
    "",
]


def test_css_plain_clean_contract(subtests) -> None:
    assert_action(
        subtests,
        CSS_PLAIN_CLEAN,
        valid_values=SAMPLES,
        expected_outputs=["@import 'a.css';\n.a { color: red; }\n\n.b { margin: 0 auto; }\n", ".a{}\n", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_css_plain_clean_keeps_double_slashes_because_they_are_code_in_plain_css() -> None:
    assert CSS_PLAIN_CLEAN("a{b:url(//x/y.png)} // z\n\n\n") == "a{b:url(//x/y.png)} // z\n"


def test_css_plain_clean_gives_what_its_two_steps_give(stylesheet_samples: list[str]) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for text in stylesheet_samples:
            assert CSS_PLAIN_CLEAN(text) == CLEANUP_WHITESPACE(strip_css_comments(text)), repr(text)
