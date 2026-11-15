import warnings

from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_css.logic import css_outline
from simplibs.extractor_css.presets import CSS_PLAIN_OUTLINE

SAMPLES = [".a { .b { c: d } }\n@media print { .e {} }\n", "", "x: y;"]


def test_css_plain_outline_contract(subtests) -> None:
    assert_action(
        subtests,
        CSS_PLAIN_OUTLINE,
        valid_values=SAMPLES,
        expected_outputs=[".a\n  .b\n@media print\n  .e\n", "", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        deep_check=False,
        verbose=False,
    )


def test_css_plain_outline_reads_double_slashes_as_code() -> None:
    assert CSS_PLAIN_OUTLINE("// .x {\n.a {}\n// }\n") == "// .x\n  .a\n"


def test_css_plain_outline_gives_what_the_function_gives(stylesheet_samples: list[str]) -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for text in stylesheet_samples:
            assert CSS_PLAIN_OUTLINE(text) == css_outline(text), repr(text)
