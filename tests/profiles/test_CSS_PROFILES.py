from simplibs.extractor_css.profiles import (
    CSS_CODE_CLEAN,
    CSS_CODE_NO_IMPORTS,
    CSS_DATA_ALL,
    CSS_OUTLINE,
    CSS_PROFILES,
    CSS_SRC_CLEAN,
)


def test_the_add_on_has_the_five_documented_profiles_in_their_order() -> None:
    assert CSS_PROFILES == (CSS_CODE_CLEAN, CSS_CODE_NO_IMPORTS, CSS_DATA_ALL, CSS_OUTLINE, CSS_SRC_CLEAN)


def test_the_keys_are_the_documented_ones() -> None:
    assert [profile.key for profile in CSS_PROFILES] == [
        "css/code-clean",
        "css/code-no-imports",
        "css/data-all",
        "css/outline",
        "css/src-clean",
    ]


def test_every_profile_belongs_to_the_css_system() -> None:
    assert {profile.system for profile in CSS_PROFILES} == {"css"}


def test_no_key_and_no_output_name_is_used_twice() -> None:
    assert len({profile.key for profile in CSS_PROFILES}) == len(CSS_PROFILES)
    assert len({profile.output_name for profile in CSS_PROFILES}) == len(CSS_PROFILES)


def test_a_collection_of_profiles_is_a_tuple() -> None:
    assert isinstance(CSS_PROFILES, tuple)
