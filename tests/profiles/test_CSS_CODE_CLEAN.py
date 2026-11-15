from simplibs.extractor.testing import assert_profile
from simplibs.extractor_css.file_rules import CSS_BASE
from simplibs.extractor_css.presets import CSS_LINE_CLEAN, CSS_PLAIN_CLEAN
from simplibs.extractor_css.profiles import CSS_CODE_CLEAN


def test_css_code_clean_contract(subtests) -> None:
    assert_profile(
        subtests,
        CSS_CODE_CLEAN,
        expected_key="css/code-clean",
        expected_output_name="css_code_clean.md",
        expected_description="Stylesheets without comments and extra blank lines (imports stay)",
        included=("style.css", "src/a.scss", "styles/theme/b.less", "THEME.CSS", "node_modules/pkg/a.css", "dist/app.min.css"),
        excluded=("readme.md", "a.js", ".hidden.css", "src/.hidden.scss", "noext", "a.css.bak", "a.sass", ".css"),
        step_cases={
            ".css": [("/* c */\n.a{b:c} // keep\n\n\n.d{}\n", ".a{b:c} // keep\n\n.d{}\n")],
            ".scss": [("// c\n.a{b:c} // gone\n\n\n.d{}\n", ".a{b:c}\n\n.d{}\n")],
            ".less": [("@import 'a';\n// c\n.a{}\n", "@import 'a';\n.a{}\n")],
        },
        unchanged_suffixes=(".txt", ".sass", ".js"),
        cover_all_suffixes=True,
        verbose=False,
    )


def test_css_code_clean_takes_the_base_rule_and_leaves_nothing_out() -> None:
    assert CSS_CODE_CLEAN.include is CSS_BASE
    assert CSS_CODE_CLEAN.exclude is None


def test_css_code_clean_cleans_plain_css_and_preprocessors_with_their_own_step() -> None:
    assert CSS_CODE_CLEAN.steps[".css"] is CSS_PLAIN_CLEAN
    assert CSS_CODE_CLEAN.steps[".scss"] is CSS_LINE_CLEAN
    assert CSS_CODE_CLEAN.steps[".less"] is CSS_LINE_CLEAN
