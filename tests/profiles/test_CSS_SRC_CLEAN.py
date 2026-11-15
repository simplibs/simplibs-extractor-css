from simplibs.extractor.testing import assert_profile
from simplibs.extractor_css.file_rules import CSS_BASE, CSS_STRICT_EXCLUDE
from simplibs.extractor_css.presets import CSS_LINE_CLEAN, CSS_PLAIN_CLEAN
from simplibs.extractor_css.profiles import CSS_SRC_CLEAN


def test_css_src_clean_contract(subtests) -> None:
    assert_profile(
        subtests,
        CSS_SRC_CLEAN,
        expected_key="css/src-clean",
        expected_output_name="css_src_clean.md",
        expected_description="Like code-clean, without minified files, packages of other people and generated output",
        included=("style.css", "src/a.scss", "styles/b.less", "THEME.CSS", "static/site.css", "static/css/main.css"),
        excluded=(
            "app.min.css",
            "src/theme.min.scss",
            "node_modules/pkg/a.css",
            "static/vendor/bootstrap/a.css",
            "dist/a.css",
            "build/a.css",
            "staticfiles/admin/a.css",
            ".next/static/a.css",
            "coverage/lcov-report/base.css",
            ".git/hooks/x.css",
            "readme.md",
            ".hidden.css",
        ),
        step_cases={
            ".css": [("/* c */\n.a{b:c} // keep\n\n\n.d{}\n", ".a{b:c} // keep\n\n.d{}\n")],
            ".scss": [("// c\n.a{b:c} // gone\n\n\n.d{}\n", ".a{b:c}\n\n.d{}\n")],
            ".less": [("@import 'a';\n// c\n.a{}\n", "@import 'a';\n.a{}\n")],
        },
        unchanged_suffixes=(".txt", ".sass", ".js"),
        cover_all_suffixes=True,
        verbose=False,
    )


def test_css_src_clean_takes_the_base_rule_and_leaves_out_the_strict_one() -> None:
    assert CSS_SRC_CLEAN.include is CSS_BASE
    assert CSS_SRC_CLEAN.exclude is CSS_STRICT_EXCLUDE


def test_css_src_clean_cleans_like_code_clean() -> None:
    assert CSS_SRC_CLEAN.steps[".css"] is CSS_PLAIN_CLEAN
    assert CSS_SRC_CLEAN.steps[".scss"] is CSS_LINE_CLEAN
    assert CSS_SRC_CLEAN.steps[".less"] is CSS_LINE_CLEAN
