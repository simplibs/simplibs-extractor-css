from simplibs.extractor.testing import assert_profile
from simplibs.extractor_css.file_rules import CSS_BASE
from simplibs.extractor_css.presets import CSS_LINE_OUTLINE, CSS_PLAIN_OUTLINE
from simplibs.extractor_css.profiles import CSS_OUTLINE


def test_css_outline_contract(subtests) -> None:
    assert_profile(
        subtests,
        CSS_OUTLINE,
        expected_key="css/outline",
        expected_output_name="css_outline.md",
        expected_description="Overview of the stylesheets: selectors and at-rules without declarations",
        included=("style.css", "src/a.scss", "styles/theme/b.less", "THEME.CSS", "node_modules/pkg/a.css", "dist/app.min.css"),
        excluded=("readme.md", "a.js", ".hidden.css", "src/.hidden.scss", "noext", "a.css.bak", "a.sass", ".css"),
        step_cases={
            ".css": [(".a { .b { c: d } }\n@media print { .e {} }\n", ".a\n  .b\n@media print\n  .e\n")],
            ".scss": [("// c\n.a { .b {} }\n", ".a\n  .b\n")],
            ".less": [("@c: red;\n.a { .b {} }\n", ".a\n  .b\n")],
        },
        unchanged_suffixes=(".txt", ".sass", ".js"),
        cover_all_suffixes=True,
        verbose=False,
    )


def test_css_outline_takes_the_base_rule_and_leaves_nothing_out() -> None:
    assert CSS_OUTLINE.include is CSS_BASE
    assert CSS_OUTLINE.exclude is None


def test_css_outline_uses_its_own_steps_for_each_kind() -> None:
    assert CSS_OUTLINE.steps[".css"] is CSS_PLAIN_OUTLINE
    assert CSS_OUTLINE.steps[".scss"] is CSS_LINE_OUTLINE
    assert CSS_OUTLINE.steps[".less"] is CSS_LINE_OUTLINE
