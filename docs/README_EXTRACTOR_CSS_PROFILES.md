# 📋 `extractor_css/profiles` — The Five Profiles

The `profiles` package holds the **five profiles** of the system `css` as `Profile` objects of [`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/). A profile says *which files* of a
project to read (`include`, `exclude`) and *what to do with the text* of each (`steps`), and gives the document its name. Registering them in the extractor is the job of
[`register_all`](README_EXTRACTOR_CSS_PLUGIN.md#register_all); having them as objects lets a program use one directly or build its own on top of it.

```python
from simplibs.extractor_css.profiles import CSS_SRC_CLEAN, CSS_PROFILES

CSS_SRC_CLEAN.key                          # -> 'css/src-clean'
[profile.name for profile in CSS_PROFILES]    # -> ['code-clean', 'code-no-imports', 'data-all', 'outline', 'src-clean']
```

The profiles are **not** exported from `simplibs.extractor_css` itself — they are a domain of their own, imported through `simplibs.extractor_css.profiles`, which defines `__all__`. They stand at the very top of the layers
(`constants` ← `file_rules` ← `logic` ← `actions` ← `presets` ← `profiles`), because a profile is built from rules and from presets. From the command line a profile is used by its key:
`simplibs-extractor css src-clean my_project`.

| You want …                                                                                  | Use                    |
|---------------------------------------------------------------------------------------------|------------------------|
| every stylesheet **as it is**, minified files and comments included                          | `css/data-all`         |
| the comments taken away, the imports kept — the everyday way to give a stylesheet to a reader | `css/code-clean`       |
| **only the project's own** stylesheets, cleaned: no minified files, packages or build output  | `css/src-clean`        |
| the rules alone: no imports, comments or blank lines                                          | `css/code-no-imports`  |
| a list of what a project styles, a fraction of the size                                       | `css/outline`          |

## The five at a glance

| Profile                  | Output                      | Include     | Exclude              | Steps (`.css` / `.scss`, `.less`)                  |
|--------------------------|-----------------------------|-------------|----------------------|----------------------------------------------------|
| `css/code-clean`         | `css_code_clean.md`         | `CSS_BASE`  | —                    | `CSS_PLAIN_CLEAN` / `CSS_LINE_CLEAN`               |
| `css/code-no-imports`    | `css_code_no_imports.md`    | `CSS_BASE`  | —                    | `CSS_PLAIN_NO_IMPORTS` / `CSS_LINE_NO_IMPORTS`     |
| `css/data-all`           | `css_data_all.md`           | `CSS_BASE`  | —                    | none: every file as it is                          |
| `css/outline`            | `css_outline.md`            | `CSS_BASE`  | —                    | `CSS_PLAIN_OUTLINE` / `CSS_LINE_OUTLINE`           |
| `css/src-clean`          | `css_src_clean.md`          | `CSS_BASE`  | `CSS_STRICT_EXCLUDE` | `CSS_PLAIN_CLEAN` / `CSS_LINE_CLEAN`               |

`CSS_PROFILES` is the tuple of all five, in the order the listings show them (alphabetical by name).

## A note on choosing the steps by suffix

A step is given the text only, never the path, and a plain `.css` file must never have its `//` cut while an `.scss` file must. So the four profiles that have steps choose them **by suffix**: one preset for `.css`
(`PLAIN`), one for `.scss` and `.less` (`LINE`). The mapping is `suffix -> step`, the form of `Profile.steps` that chooses by file type. The two halves of the suffixes do not overlap, so merging the mappings never loses a step.
`css/data-all` has no steps at all.

<details>
<summary>🔍 Under the hood — the private helper that builds the mapping</summary>

```python
def steps_for_css(plain: Action, line: Action) -> dict[str, Action]:

    # 1. `by_suffix` for each half, the two mappings side by side
    return {
        **by_suffix(plain, CSS_PLAIN_SUFFIXES),
        **by_suffix(line, CSS_LINE_COMMENT_SUFFIXES),
    }
```

`steps_for_css` is a tool of the profiles' own and is not exported; `by_suffix` is a tool of `simplibs-extractor`.

</details>

## A note on what a profile never decides

A profile is **data**: files in, steps on the text, a name out. It reads nothing and writes nothing; the extractor does that. A profile also never judges a reader's wishes — `css/data-all` hands over minified files and
comments because "every file as it is" must not decide what a reader may see.

---

## 🧭 Table of Contents

* [`CSS_CODE_CLEAN`](#css_code_clean)
* [`CSS_CODE_NO_IMPORTS`](#css_code_no_imports)
* [`CSS_DATA_ALL`](#css_data_all)
* [`CSS_OUTLINE`](#css_outline)
* [`CSS_SRC_CLEAN`](#css_src_clean)
* [`CSS_PROFILES`](#css_profiles)
* [One stylesheet through each profile](#one-stylesheet-through-each-profile)
* [A profile of your own](#a-profile-of-your-own)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-profiles--the-five-profiles)

---

### `CSS_CODE_CLEAN`

The profile **`css/code-clean`**: every stylesheet of the project with the comments taken out, as it is otherwise — the **imports stay**. The everyday way to give a stylesheet to a reader.

**Type:**
* `Final[Profile]`: `system="css"`, `name="code-clean"`, output `css_code_clean.md`.

**Example usage:**
```bash
simplibs-extractor css code-clean my_project         # -> my_project/css_code_clean.md
```

`.css` gets the step for plain CSS, `.scss` and `.less` the step that also knows `//`.

**Under the hood:**
```python
CSS_CODE_CLEAN: Final[Profile] = Profile(
    system="css",
    name="code-clean",
    description="Stylesheets without comments and extra blank lines (imports stay)",
    include=CSS_BASE,
    steps=steps_for_css(CSS_PLAIN_CLEAN, CSS_LINE_CLEAN),
    output_name="css_code_clean.md",
)
```

[▲ Back to top](#-table-of-contents)

---

### `CSS_CODE_NO_IMPORTS`

The profile **`css/code-no-imports`**: the stylesheets reduced to what they style — no `@import`, `@use` or `@forward`, no comments, no blank lines.

**Type:**
* `Final[Profile]`: `system="css"`, `name="code-no-imports"`, output `css_code_no_imports.md`.

**Example usage:**
```bash
simplibs-extractor css code-no-imports my_project    # -> my_project/css_code_no_imports.md
```

**Under the hood:**
```python
CSS_CODE_NO_IMPORTS: Final[Profile] = Profile(
    system="css",
    name="code-no-imports",
    description="Pure rules: no imports, comments or blank lines",
    include=CSS_BASE,
    steps=steps_for_css(CSS_PLAIN_NO_IMPORTS, CSS_LINE_NO_IMPORTS),
    output_name="css_code_no_imports.md",
)
```

> 💡 What a stylesheet needs from other files is the part of its text that says least about the stylesheet itself — but a document without imports no longer says where a name comes from. The profile is built for a reader, not for a compiler.

[▲ Back to top](#-table-of-contents)

---

### `CSS_DATA_ALL`

The profile **`css/data-all`**: the files selected by `CSS_BASE`, **untouched** — comments, imports and minified files included.

**Type:**
* `Final[Profile]`: `system="css"`, `name="data-all"`, output `css_data_all.md`; it has **no steps**.

**Example usage:**
```bash
simplibs-extractor css data-all my_project           # -> my_project/css_data_all.md
```

**Under the hood:**
```python
CSS_DATA_ALL: Final[Profile] = Profile(
    system="css",
    name="data-all",
    description="Every relevant stylesheet, as it is",
    include=CSS_BASE,
    output_name="css_data_all.md",
)
```

[▲ Back to top](#-table-of-contents)

---

### `CSS_OUTLINE`

The profile **`css/outline`**: what a project styles, in a fraction of the size. For a reader with a limited window the list of selectors is most of what is needed to ask the right questions.

**Type:**
* `Final[Profile]`: `system="css"`, `name="outline"`, output `css_outline.md`.

**Example usage:**
```bash
simplibs-extractor css outline my_project            # -> my_project/css_outline.md
```

Each file is a list of headers, one per line, indented by the depth of its block. A file with no block gives an empty section.

**Under the hood:**
```python
CSS_OUTLINE: Final[Profile] = Profile(
    system="css",
    name="outline",
    description="Overview of the stylesheets: selectors and at-rules without declarations",
    include=CSS_BASE,
    steps=steps_for_css(CSS_PLAIN_OUTLINE, CSS_LINE_OUTLINE),
    output_name="css_outline.md",
)
```

[▲ Back to top](#-table-of-contents)

---

### `CSS_SRC_CLEAN`

The profile **`css/src-clean`**: like [`css/code-clean`](#css_code_clean), but only **the project's own stylesheets** — no `*.min.css`, no `node_modules` or `vendor`, no `dist`, `staticfiles` or coverage reports.

**Type:**
* `Final[Profile]`: `system="css"`, `name="src-clean"`, output `css_src_clean.md`; `exclude` is [`CSS_STRICT_EXCLUDE`](README_EXTRACTOR_CSS_FILE_RULES.md#css_strict_exclude).

**Example usage:**
```bash
simplibs-extractor css src-clean my_project          # -> my_project/css_src_clean.md
```

**Under the hood:**
```python
CSS_SRC_CLEAN: Final[Profile] = Profile(
    system="css",
    name="src-clean",
    description="Like code-clean, without minified files, packages of other people and generated output",
    include=CSS_BASE,
    exclude=CSS_STRICT_EXCLUDE,
    steps=steps_for_css(CSS_PLAIN_CLEAN, CSS_LINE_CLEAN),
    output_name="css_src_clean.md",
)
```

[▲ Back to top](#-table-of-contents)

---

### `CSS_PROFILES`

The profiles of the system `css`, in the order the listing commands show them.

**Type:**
* `Final[tuple[Profile, ...]]`: the five profiles above.

**Example usage:**
```python
from simplibs.extractor_css.profiles import CSS_PROFILES

len(CSS_PROFILES)                                     # -> 5
[profile.output_name for profile in CSS_PROFILES]     # -> ['css_code_clean.md', 'css_code_no_imports.md', 'css_data_all.md', 'css_outline.md', 'css_src_clean.md']
```

**Under the hood:**
```python
CSS_PROFILES: Final[tuple[Profile, ...]] = (
    CSS_CODE_CLEAN,
    CSS_CODE_NO_IMPORTS,
    CSS_DATA_ALL,
    CSS_OUTLINE,
    CSS_SRC_CLEAN,
)
```

[▲ Back to top](#-table-of-contents)

---

### One stylesheet through each profile

The steps of a profile are in `Profile.steps`, a mapping of suffix to step, so one file can be run through each by hand — which is what the extractor does for every file it takes.

**Example usage:**
```python
from simplibs.extractor_css.profiles import CSS_CODE_CLEAN, CSS_CODE_NO_IMPORTS, CSS_OUTLINE

source = '@import "base.css";\n/* layout */\n.card { color: red; } /* tail */\n@media print { .card { color: black; } }\n'

CSS_CODE_CLEAN.steps[".css"](source)        # -> '@import "base.css";\n.card { color: red; }\n@media print { .card { color: black; } }\n'
CSS_CODE_NO_IMPORTS.steps[".css"](source)   # -> '.card { color: red; }\n@media print { .card { color: black; } }\n'
CSS_OUTLINE.steps[".css"](source)           # -> '.card\n@media print\n  .card\n'
```

The same with a file that has `//` comments, which only the steps of `.scss` and `.less` know:

```python
scss = '// layout\n@use "base";\n.card { color: red; // tail\n  &:hover { color: blue; } }\n'

CSS_CODE_CLEAN.steps[".scss"](scss)         # -> '@use "base";\n.card { color: red;\n  &:hover { color: blue; } }\n'
CSS_CODE_NO_IMPORTS.steps[".scss"](scss)    # -> '.card { color: red;\n  &:hover { color: blue; } }\n'
CSS_OUTLINE.steps[".scss"](scss)            # -> '.card\n  &:hover\n'
```

`css/data-all` has no steps, and `css/src-clean` runs the same steps as `css/code-clean` — it differs only in the files it takes.

[▲ Back to top](#-table-of-contents)

---

### A profile of your own

A profile is an ordinary `Profile` of the extractor, so one of your own is made from the same parts: the [file rules](README_EXTRACTOR_CSS_FILE_RULES.md) combine with `&`, `|` and `~`, the steps are the
[presets](README_EXTRACTOR_CSS_PRESETS.md), and `by_suffix` gives each kind of file its own.

```python
from simplibs.extractor import Profile, by_suffix, extract, register_profile
from simplibs.extractor_css.constants import CSS_LINE_COMMENT_SUFFIXES, CSS_PLAIN_SUFFIXES
from simplibs.extractor_css.file_rules import CSS_BASE, MINIFIED_NAME
from simplibs.extractor_css.presets import CSS_LINE_OUTLINE, CSS_PLAIN_OUTLINE

register_profile(Profile(
    system="css", name="own-outline",
    description="The outline of the stylesheets, minified files left out",
    include=CSS_BASE,
    exclude=MINIFIED_NAME,
    steps={**by_suffix(CSS_PLAIN_OUTLINE, CSS_PLAIN_SUFFIXES), **by_suffix(CSS_LINE_OUTLINE, CSS_LINE_COMMENT_SUFFIXES)},
    output_name="css_own_outline.md",
))

extract(source="my_project", profile="css/own-outline")
```

A changed copy of a profile of this library is one `dataclasses.replace` away:

```python
from dataclasses import replace
from simplibs.extractor_css.profiles import CSS_SRC_CLEAN

mine = replace(CSS_SRC_CLEAN, name="mine", output_name="mine.md")
mine.key                                   # -> 'css/mine'
```

> 💡 From Python, call `load_plugins()` of the extractor once before a profile of this library is looked up by its key; `extract()` never loads add-ons on its own. A profile object you import needs no loading.

[▲ Back to top](#-table-of-contents)

---

### Errors of this package

It raises no cards of its own: the profiles are built when the package is imported, and a `Profile` that is built wrongly would fail there, in the extractor's own check. A profile key that is already registered is
the card of the extractor's registry, raised by [`register_all`](README_EXTRACTOR_CSS_PLUGIN.md#errors-of-this-package).

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-profiles--the-five-profiles)
