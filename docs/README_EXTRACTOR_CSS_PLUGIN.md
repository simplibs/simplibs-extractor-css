# 🔌 `extractor_css/plugin` — The Meeting Point With the Extractor

The `plugin` package holds **one function**, `register_all`: the target of the entry point through which the extractor finds this library. `pip install simplibs-extractor-css` is the whole installation — the
entry point makes the extractor find the function, and the five profiles appear in `simplibs-extractor --list-profiles css`.

```python
from simplibs.extractor_css import register_all

register_all()      # -> ['css/code-clean', 'css/code-no-imports', 'css/data-all', 'css/outline', 'css/src-clean']
```

`register_all` is exported from the package root. The entry point lives in this library's `pyproject.toml`:

```toml
[project.entry-points."simplibs.extractor.plugins"]
css = "simplibs.extractor_css:register_all"
```

The extractor's `load_plugins()` reads the group `simplibs.extractor.plugins`, calls every function it finds **with no arguments**, and never lets one add-on stop another; nothing is imported by name. The command
`simplibs-extractor` calls `load_plugins()` for you. From Python, call it **once** before a profile is looked up by its key — `extract()` never loads add-ons on its own.

## A note on the rules of an add-on function

An add-on function is small on purpose: it takes **no required argument**, registers with `replace_existing=True` (so calling it twice changes nothing), **only registers** — no scanning, no network, no printing —
and uses only the public API of the extractor (`Profile`, `register_profile`, `register_language`).

## A note on the languages

`.scss` and `.less` get their code-fence language here. The markdown output writes the language after the opening fence so that a viewer can colour the code; without the registration the extractor would write the code
blocks of these files with no language. The names are in
[`CSS_EXTRA_LANGUAGE_BY_SUFFIX`](README_EXTRACTOR_CSS_CONSTANTS.md#suffixes); `.css` is not registered, because the extractor knows it itself.

## A note on the order

**Languages first, profiles after.** A profile that is registered is usable at once, and its output should already be fenced correctly.

---

## 🧭 Table of Contents

* [`register_all`](#register_all)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-plugin--the-meeting-point-with-the-extractor)

---

### `register_all`

Registers every profile and language of this library in the registries of the extractor, and returns the keys of the profiles. The extractor calls it, with no arguments, for every installed add-on.

**Parameters:**
* `replace_existing` (*bool*, keyword-only, default `True`): Replace a profile or a language that already has the key. The default makes the call safe to repeat.

**Returns:**
* `list[str]`: The keys of the registered profiles, in the order of [`CSS_PROFILES`](README_EXTRACTOR_CSS_PROFILES.md#css_profiles) (`"css/code-clean"`, …).

**Raises:**
* `AlreadyExistsError` (`EXTRACTOR_PROFILE_EXISTS`): A profile key is already registered and `replace_existing` is `False`.
* `ParamError`: A language suffix is already registered and `replace_existing` is `False`.

**Example usage:**
```python
from simplibs.extractor_css import register_all

register_all()                               # -> ['css/code-clean', 'css/code-no-imports', 'css/data-all', 'css/outline', 'css/src-clean']
register_all()                               # -> ['css/code-clean', 'css/code-no-imports', 'css/data-all', 'css/outline', 'css/src-clean']     twice: nothing changes
register_all(replace_existing=False)         # -> raises: the keys are taken
```

**Under the hood:**
```python
@validate_call
def register_all(*, replace_existing: bool = True) -> list[str]:

    # 1. The languages of the preprocessors, so the output fences them properly
    for suffix, language in CSS_EXTRA_LANGUAGE_BY_SUFFIX.items():
        register_language(suffix, language, replace_existing=replace_existing)

    # 2. Register each profile
    keys: list[str] = []
    for profile in CSS_PROFILES:
        registered = register_profile(profile, replace_existing=replace_existing)
        keys.append(registered.key)

    return keys
```

> 💡 Calling it from your own code is rarely needed: the command and `load_plugins()` do it. A program that only imports a profile object (`from simplibs.extractor_css.profiles import CSS_SRC_CLEAN`) needs no registration at all.

[▲ Back to top](#-table-of-contents)

---

### Errors of this package

It raises no cards of its own. `register_all` raises the cards of the **extractor's registry** when it is called with `replace_existing=False` and a key is already taken (see the errors of
[`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/)); a wrong type of the argument is a `ValidationError` from `simplibs-validate`.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-plugin--the-meeting-point-with-the-extractor)
