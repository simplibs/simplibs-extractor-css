from simplibs.extractor_css.constants import CSS_LINE_COMMENT_SUFFIXES, CSS_PLAIN_SUFFIXES, CSS_SUFFIXES


def test_the_stylesheet_suffixes_are_css_scss_and_less() -> None:
    assert CSS_SUFFIXES == (".css", ".scss", ".less")


def test_the_suffixes_are_made_of_the_two_halves() -> None:
    assert CSS_SUFFIXES == CSS_PLAIN_SUFFIXES + CSS_LINE_COMMENT_SUFFIXES


def test_no_suffix_belongs_to_both_halves() -> None:
    assert set(CSS_PLAIN_SUFFIXES).isdisjoint(CSS_LINE_COMMENT_SUFFIXES)


def test_every_suffix_is_lowercase_and_starts_with_a_dot() -> None:
    assert all(suffix.startswith(".") and suffix == suffix.lower() for suffix in CSS_SUFFIXES)
