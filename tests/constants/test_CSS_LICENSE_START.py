from simplibs.extractor_css.constants import CSS_LICENSE_START


def test_a_comment_that_survives_minification_begins_with_a_bang() -> None:
    assert CSS_LICENSE_START == "/*!"
