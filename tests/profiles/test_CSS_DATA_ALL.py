from simplibs.extractor.testing import assert_profile
from simplibs.extractor_css.file_rules import CSS_BASE
from simplibs.extractor_css.profiles import CSS_DATA_ALL


def test_css_data_all_contract(subtests) -> None:
    assert_profile(
        subtests,
        CSS_DATA_ALL,
        expected_key="css/data-all",
        expected_output_name="css_data_all.md",
        expected_description="Every relevant stylesheet, as it is",
        included=("style.css", "src/a.scss", "styles/theme/b.less", "THEME.CSS", "node_modules/pkg/a.css", "dist/app.min.css"),
        excluded=("readme.md", "a.js", ".hidden.css", "src/.hidden.scss", "noext", "a.css.bak", "a.sass", ".css"),
        unchanged_suffixes=(".css", ".scss", ".less", ".txt"),
        verbose=False,
    )


def test_css_data_all_takes_the_base_rule_and_changes_no_text() -> None:
    assert CSS_DATA_ALL.include is CSS_BASE
    assert CSS_DATA_ALL.exclude is None
    assert CSS_DATA_ALL.steps is None
