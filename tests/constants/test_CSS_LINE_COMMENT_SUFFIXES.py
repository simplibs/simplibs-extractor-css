from simplibs.extractor_css.constants import CSS_LINE_COMMENT_SUFFIXES


def test_the_preprocessors_with_line_comments_are_scss_and_less() -> None:
    assert CSS_LINE_COMMENT_SUFFIXES == (".scss", ".less")


def test_sass_is_left_out_until_it_has_a_scanner_of_its_own() -> None:
    assert ".sass" not in CSS_LINE_COMMENT_SUFFIXES


def test_plain_css_has_no_line_comments() -> None:
    assert ".css" not in CSS_LINE_COMMENT_SUFFIXES
