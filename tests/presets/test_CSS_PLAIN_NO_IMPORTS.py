import warnings

from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import remove_css_imports, strip_css_comments
from simplibs.extractor_css.presets import CSS_PLAIN_NO_IMPORTS
from simplibs.text.presets import COMPACT

SAMPLES = [
    "/* banner */\n\n\n@import 'a.css';\n.a { color: red; } /* c */   \n\n\n\n.b { margin: 0/**/auto; }  \n\n",
    ".a{}\n",
    "",
]


def test_css_plain_no_imports_contract(subtests) -> None:
    assert_action(
        subtests,
        CSS_PLAIN_NO_IMPORTS,
        valid_values=SAMPLES,
        expected_outputs=[".a { color: red; }\n.b { margin: 0 auto; }\n", ".a{}\n", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_css_plain_no_imports_leaves_no_blank_line_at_all() -> None:
    assert CSS_PLAIN_NO_IMPORTS("@import 'a';\n\n.a{}\n\n\n.b{}\n") == ".a{}\n.b{}\n"


def test_css_plain_no_imports_gives_what_its_three_steps_give(stylesheet_samples: list[str]) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for text in stylesheet_samples:
            assert CSS_PLAIN_NO_IMPORTS(text) == COMPACT(remove_css_imports(strip_css_comments(text))), repr(text)
