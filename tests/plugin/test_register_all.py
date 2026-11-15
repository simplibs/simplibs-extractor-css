from importlib.metadata import entry_points

import pytest
from simplibs.exception import AlreadyExistsError, ParamError
from simplibs.extractor import Profile, get_profile, register_language, register_profile
from simplibs.extractor.registry._helpers import LANGUAGE_REGISTRY, PROFILE_REGISTRY
from simplibs.extractor_css.constants import CSS_EXTRA_LANGUAGE_BY_SUFFIX
from simplibs.extractor_css.file_rules import CSS_BASE
from simplibs.extractor_css.plugin import register_all
from simplibs.extractor_css.profiles import CSS_CODE_CLEAN, CSS_PROFILES

KEYS = ["css/code-clean", "css/code-no-imports", "css/data-all", "css/outline", "css/src-clean"]


@pytest.fixture(autouse=True)
def isolated_registries():
    """Start every test with the registries as they were, minus what this add-on brings, and put them back afterwards."""
    profiles, languages = dict(PROFILE_REGISTRY), dict(LANGUAGE_REGISTRY)
    for key in KEYS:
        PROFILE_REGISTRY.pop(key, None)
    for suffix in CSS_EXTRA_LANGUAGE_BY_SUFFIX:
        LANGUAGE_REGISTRY.pop(suffix, None)
    try:
        yield
    finally:
        PROFILE_REGISTRY.clear()
        PROFILE_REGISTRY.update(profiles)
        LANGUAGE_REGISTRY.clear()
        LANGUAGE_REGISTRY.update(languages)


def a_profile_that_takes_the_key(name: str) -> Profile:
    return Profile(system="css", name=name, description="someone else's profile", include=CSS_BASE)


def test_register_all_returns_the_keys_of_the_profiles_in_their_order() -> None:
    assert register_all() == KEYS


def test_every_profile_can_be_got_from_the_extractor_afterwards() -> None:
    register_all()
    for profile in CSS_PROFILES:
        assert get_profile(profile.key) == profile


def test_the_languages_that_the_extractor_does_not_know_are_registered() -> None:
    register_all()
    assert LANGUAGE_REGISTRY[".scss"] == "scss"
    assert LANGUAGE_REGISTRY[".less"] == "less"


def test_the_language_of_plain_css_is_left_as_it_was() -> None:
    before = LANGUAGE_REGISTRY.get(".css")
    register_all()
    assert LANGUAGE_REGISTRY.get(".css") == before


def test_calling_it_twice_changes_nothing() -> None:
    first_keys = register_all()
    profiles, languages = dict(PROFILE_REGISTRY), dict(LANGUAGE_REGISTRY)
    assert register_all() == first_keys
    assert dict(PROFILE_REGISTRY) == profiles
    assert dict(LANGUAGE_REGISTRY) == languages


def test_a_profile_with_the_same_key_is_replaced_by_default() -> None:
    register_profile(a_profile_that_takes_the_key("code-clean"))
    register_all()
    assert get_profile("css/code-clean") == CSS_CODE_CLEAN


def test_a_language_with_the_same_suffix_is_replaced_by_default() -> None:
    register_language(".scss", "other")
    register_all()
    assert LANGUAGE_REGISTRY[".scss"] == "scss"


def test_a_taken_profile_key_is_refused_when_replacing_is_off() -> None:
    register_profile(a_profile_that_takes_the_key("code-clean"))
    with pytest.raises(AlreadyExistsError) as caught:
        register_all(replace_existing=False)
    assert caught.value.error_name == "EXTRACTOR_PROFILE_EXISTS"


def test_a_taken_language_suffix_is_refused_when_replacing_is_off() -> None:
    register_language(".scss", "other")
    with pytest.raises(ParamError) as caught:
        register_all(replace_existing=False)
    assert caught.value.error_name == "EXTRACTOR_CONFIG_INVALID"


def test_with_nothing_taken_replacing_off_registers_everything() -> None:
    assert register_all(replace_existing=False) == KEYS


def test_the_entry_point_of_the_package_leads_to_register_all() -> None:
    found = [point for point in entry_points(group="simplibs.extractor.plugins") if point.name == "css"]
    if not found:
        pytest.skip("simplibs-extractor-css is not installed here (pip install -e .), so its entry point is not visible.")
    assert found[0].value == "simplibs.extractor_css:register_all"
    assert found[0].load() is register_all
