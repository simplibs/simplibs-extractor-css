from simplibs.extractor_css.constants import CSS_MINIFIED_ENDING


def test_a_minified_stylesheet_has_a_stem_ending_with_dot_min() -> None:
    assert CSS_MINIFIED_ENDING == ".min"
