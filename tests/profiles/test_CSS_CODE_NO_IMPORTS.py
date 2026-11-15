from simplibs.extractor.testing import assert_profile
from simplibs.extractor_css.file_rules import CSS_BASE
from simplibs.extractor_css.presets import CSS_LINE_NO_IMPORTS, CSS_PLAIN_NO_IMPORTS
from simplibs.extractor_css.profiles import CSS_CODE_NO_IMPORTS


def test_css_code_no_imports_contract(subtests) -> None:
    assert_profile(
        subtests,
        CSS_CODE_NO_IMPORTS,
        expected_key="css/code-no-imports",
        expected_output_name="css_code_no_imports.md",
        expected_description="Pure rules: no imports, comments or blank lines",
        included=("style.css", "src/a.scss", "styles/theme/b.less", "THEME.CSS", "node_modules/pkg/a.css", "dist/app.min.css"),
        excluded=("readme.md", "a.js", ".hidden.css", "src/.hidden.scss", "noext", "a.css.bak", "a.sass", ".css"),
        step_cases={
            ".css": [("@import 'a.css';\n/* c */\n.a{}\n\n.b{}\n", ".a{}\n.b{}\n")],
            ".scss": [("@use 'a';\n// c\n.a{}\n", ".a{}\n")],
            ".less": [("@import (reference) 'a';\n.a{}\n", ".a{}\n")],
        },
        unchanged_suffixes=(".txt", ".sass", ".js"),
        cover_all_suffixes=True,
        verbose=False,
    )


def test_css_code_no_imports_takes_the_base_rule_and_leaves_nothing_out() -> None:
    assert CSS_CODE_NO_IMPORTS.include is CSS_BASE
    assert CSS_CODE_NO_IMPORTS.exclude is None


def test_css_code_no_imports_uses_its_own_steps_for_each_kind() -> None:
    assert CSS_CODE_NO_IMPORTS.steps[".css"] is CSS_PLAIN_NO_IMPORTS
    assert CSS_CODE_NO_IMPORTS.steps[".scss"] is CSS_LINE_NO_IMPORTS
    assert CSS_CODE_NO_IMPORTS.steps[".less"] is CSS_LINE_NO_IMPORTS
