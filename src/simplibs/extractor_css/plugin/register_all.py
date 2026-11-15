from simplibs.extractor import register_language, register_profile
from simplibs.validate import validate_call
# Outers
from ..constants import CSS_EXTRA_LANGUAGE_BY_SUFFIX
from ..profiles import CSS_PROFILES


@validate_call
def register_all(*, replace_existing: bool = True) -> list[str]:
    """Register every profile and language of this library in the registries of the extractor.

    The extractor calls it, with no arguments, for every installed add-on
    (entry-point group `simplibs.extractor.plugins`).

    Args:
        replace_existing: Replace a profile or a language that already has the key (the default, so calling it twice changes nothing).

    Returns:
        The keys of the registered profiles (`"css/code-clean"`...).

    Raises:
        StateError: A profile key is taken and `replace_existing` is `False`.
        ParamError: A language suffix is taken and `replace_existing` is `False`.
    """

    # 1. The languages of the preprocessors, so the output fences them properly
    for suffix, language in CSS_EXTRA_LANGUAGE_BY_SUFFIX.items():
        register_language(suffix, language, replace_existing=replace_existing)

    # 2. Register each profile
    keys: list[str] = []
    for profile in CSS_PROFILES:
        registered = register_profile(profile, replace_existing=replace_existing)
        keys.append(registered.key)

    return keys


_DESIGN_NOTES = """
# register_all — What the Entry Point Calls

## Purpose
`pip install simplibs-extractor-css` is the whole installation: the entry
point `css = "simplibs.extractor_css:register_all"` makes the extractor find
this function, and the five profiles appear in `--list-systems`.

## The Rules of an Add-On Function
It takes no required argument, registers with `replace_existing=True`, only
registers (no scanning, no network, no printing) and uses only the public API
of the extractor (`Profile`, `register_profile`, `register_language`).

## Languages
`.scss` and `.less` get their fence language here. Without it the extractor
would write their code blocks with no language and a viewer would not colour
them.

## Order
Languages first: a profile that is registered is usable at once, and its
output should already be fenced correctly.
"""
