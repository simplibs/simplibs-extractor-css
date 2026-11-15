import warnings

from simplibs.actions.testing import assert_action
from simplibs.exception import ValidationError
from simplibs.extractor_css.actions import RemoveCssImports
from simplibs.extractor_css.logic import remove_css_imports

SAMPLES = ['@import "a";\n.a{}\n', ".a{}\n", ""]


def test_remove_css_imports_contract(subtests) -> None:
    assert_action(
        subtests,
        RemoveCssImports(),
        valid_values=SAMPLES,
        expected_outputs=[".a{}\n", ".a{}\n", ""],
        invalid_values=[5, None, b"x"],
        expected_exception_type=ValidationError,
        expected_input_type=str,
        expected_output_type=str,
        action_class=RemoveCssImports,
        invalid_init_params=[((), {"line_comments": 5}), ((), {"line_comments": None})],
        verbose=False,
    )


def test_remove_css_imports_hands_its_option_to_the_function() -> None:
    text = '// @import "a";\n@use "b";\n.a{}\n'
    assert RemoveCssImports(line_comments=True)(text) == '// @import "a";\n.a{}\n'


def test_remove_css_imports_gives_what_the_function_gives(stylesheet_samples: list[str]) -> None:
    plain, preprocessor = RemoveCssImports(), RemoveCssImports(line_comments=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for text in stylesheet_samples:
            assert plain(text) == remove_css_imports(text), repr(text)
            assert preprocessor(text) == remove_css_imports(text, line_comments=True), repr(text)


def test_remove_css_imports_can_be_used_again_and_again() -> None:
    action = RemoveCssImports()
    first = action('@import "a";\n.a{}\n')
    assert action('@use "b";\n.b{}\n') == ".b{}\n"
    assert action('@import "a";\n.a{}\n') == first == ".a{}\n"
