from simplibs.extractor_css.constants import CSS_EXTRA_LANGUAGE_BY_SUFFIX, CSS_LINE_COMMENT_SUFFIXES


def test_the_fence_languages_are_the_documented_pairs() -> None:
    assert CSS_EXTRA_LANGUAGE_BY_SUFFIX == {".scss": "scss", ".less": "less"}


def test_plain_css_is_not_listed_because_the_extractor_knows_it() -> None:
    assert ".css" not in CSS_EXTRA_LANGUAGE_BY_SUFFIX


def test_every_preprocessor_suffix_has_a_fence_language() -> None:
    assert set(CSS_EXTRA_LANGUAGE_BY_SUFFIX) == set(CSS_LINE_COMMENT_SUFFIXES)
