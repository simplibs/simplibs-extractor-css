from simplibs.extractor_css.constants import CSS_LICENSE_TAGS


def test_the_tags_that_keep_a_comment_are_license_and_preserve() -> None:
    assert CSS_LICENSE_TAGS == ("@license", "@preserve")
