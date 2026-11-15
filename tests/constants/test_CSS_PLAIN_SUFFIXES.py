from simplibs.extractor_css.constants import CSS_PLAIN_SUFFIXES


def test_plain_css_is_the_only_suffix_where_double_slashes_are_not_a_comment() -> None:
    assert CSS_PLAIN_SUFFIXES == (".css",)
