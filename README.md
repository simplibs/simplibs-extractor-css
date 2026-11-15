# 🎨 `simplibs-extractor-css`

[![PyPI](https://img.shields.io/pypi/v/simplibs-extractor-css)](https://pypi.org/project/simplibs-extractor-css/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-extractor-css/blob/main/LICENSE)
[![tests](https://github.com/simplibs/simplibs-extractor-css/actions/workflows/tests.yml/badge.svg)](https://github.com/simplibs/simplibs-extractor-css/actions)

**A stylesheet project in one document — cleaned of its comments, or reduced to a list of what it styles.**

The CSS add-on of [`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/). The extractor gathers the text files of a folder into one document and knows **no language**; this library teaches it
stylesheets — CSS, SCSS and Less: which files are worth reading, how to take **comments and imports** out of a source, how to write an **outline** of its selectors and at-rules, and five ready **profiles** that put it
together. A stylesheet is read by a small scanner that knows strings and `url()` addresses, never by a regex over the whole text — so a `/*` inside `content: "/*"` or a `//` inside an address is left alone.

```bash
pip install simplibs-extractor-css
simplibs-extractor css src-clean my_project
```

```python
from simplibs.extractor_css import strip_css_comments, css_outline

strip_css_comments('a { content: "/* kept */"; /* gone */ }\n')      # -> 'a { content: "/* kept */"; }\n'
css_outline("@media print { .a, .b { color: red; } }")               # -> '@media print\n  .a, .b\n'
```

> `pip install` is the whole installation: the library announces itself to the extractor through an entry point, so the profiles show up in `simplibs-extractor --list-profiles css` with nothing to import. The same
> steps are plain functions (`str -> str`) that you can use without the extractor at all.

---

## 🧭 The Core Philosophy

Cleaning a stylesheet with a few regular expressions works until the first file where it does not: a `/*` inside `content: "/*"`, a `//` inside `url(//cdn.example.com/a.png)` (a comment in SCSS, an address everywhere
else), `0/**/auto` that becomes the one broken value `0auto`, an `@import` inside a comment. `simplibs-extractor-css` takes those traps seriously:

* **A scanner, not a regex.** One pass that knows strings, `url(...)` addresses and comments, and jumps from one stop to the next. It is not a parser — it builds no tree — and it cannot fail: there is no syntax it refuses.
* **Plain CSS is not SCSS.** `//` is a comment only in `.scss` and `.less`. A step sees only the text, so the profile chooses the step by suffix, and a `//` in a plain `.css` file is never cut.
* **A comment is a border between two tokens.** `0/**/auto` becomes `0 auto`, not `0auto`: a space stays exactly where the two sides would merge, and nowhere else. A step cuts by position and changes nothing it did not
  find; `strip_css_comments`, run twice, returns the same text.
* **A damaged file is left as it is.** A comment or a string that is never closed, braces that do not pair up: the text comes back unchanged, with a warning, and the extractor calls the file `partial`. A step never cuts on
  a basis it does not trust.
* **Licences can stay.** With `keep_license=True` the comments that minifiers keep — `/*! ... */`, `@license`, `@preserve` — survive. Off by default: the default result has no comments at all.
* **Imports are one family.** `@import`, `@use` and `@forward` all say "this file needs that one", so one step takes all three and there is no option for the difference.
* **The project's own is its own.** The strict profile leaves out minified files, packages of other people and generated output — but `static/` stays, because it is where a Django project keeps its own styles.
* **Functions first, actions on top.** Every step is a plain function; the action is a thin wrapper of the same name, and the presets and profiles are built from the actions. The logic lives once.
* **Layers that only look left.** `constants` ← `file_rules` ← `logic` ← `actions` ← `presets` ← `profiles` ← `plugin` — every layer imports only from those before it.

```python
strip_css_comments("a { b: c; /* never closed\n")      # -> 'a { b: c; /* never closed\n'     unchanged, with a UserWarning: the comment is never closed
```

---

## 📦 Installation

```bash
pip install simplibs-extractor-css
```

Requires Python 3.11+. The package brings [`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/) with it, and the command `simplibs-extractor` is available at once. Runtime dependencies (installed automatically):
[`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/) (the profile, the registry, `by_suffix`),
[`simplibs-text`](https://pypi.org/project/simplibs-text/) (cutting the found ranges, the `Span` type, the whitespace presets),
[`simplibs-actions`](https://pypi.org/project/simplibs-actions/) (the steps as actions),
[`simplibs-path`](https://pypi.org/project/simplibs-path/) and [`simplibs-rules`](https://pypi.org/project/simplibs-rules/) (the file rules),
[`simplibs-validate`](https://pypi.org/project/simplibs-validate/) (`@validate_call` on every public function) and
[`simplibs-types`](https://pypi.org/project/simplibs-types/) (`int_positive`, the depth of the outline).

---

## 🚀 Quick Start in 60 Seconds

### Level 1: The command line

```bash
simplibs-extractor css src-clean my_project                     # the project's own stylesheets, cleaned -> my_project/css_src_clean.md
simplibs-extractor css outline my_project                       # selectors and at-rules only — the smallest overview
simplibs-extractor css code-no-imports my_project               # the rules alone
simplibs-extractor css code-clean,data-all my_project           # two profiles -> two files, one run
simplibs-extractor css data-all my_project --dry-run            # plan and report, write nothing
simplibs-extractor --list-profiles css                          # the five profiles
```

Which one? `data-all` gives the files as they are, `code-clean` takes the comments away, `src-clean` does the same and leaves out minified files, other people's packages and generated output, `code-no-imports` takes also the
imports away, and `outline` keeps only what a project styles.

### Level 2: The steps as functions

```python
from simplibs.extractor_css import strip_css_comments, remove_css_imports, css_outline, css_comment_spans

strip_css_comments("a { margin: 0/**/auto; } /* n */\n")                       # -> 'a { margin: 0 auto; }\n'
strip_css_comments("// n\na { b: c; } // t\n", line_comments=True)            # -> 'a { b: c; }\n'          SCSS and Less
strip_css_comments("/*! v1 */\n/* x */\na { b: c; }\n", keep_license=True)     # -> '/*! v1 */\na { b: c; }\n'
remove_css_imports('@import "a.css";\n@use "b";\na { c: d; }\n')                # -> 'a { c: d; }\n'
css_outline("@media print { .a, .b { color: red; } }", max_depth=1)            # -> '@media print\n'
css_comment_spans("a { b: c; } /* x */\n")                                     # -> [(11, 19)]
```

### Level 3: Actions and ready-made chains

```python
from simplibs.extractor_css.actions import CssOutline, RemoveCssImports, StripCssComments
from simplibs.extractor_css.presets import CSS_LINE_CLEAN, CSS_PLAIN_NO_IMPORTS

steps = StripCssComments() >> RemoveCssImports()
steps('@import "a.css"; /* c */\na { b: c; }\n')                                # -> 'a { b: c; }\n'

CSS_PLAIN_NO_IMPORTS('@import "a.css";\n\n/* c */\na { b: c; }\n\n\nd { e: f; }\n')    # -> 'a { b: c; }\nd { e: f; }\n'
CSS_LINE_CLEAN("// c\na { b: c; } // t\n")                                      # -> 'a { b: c; }\n'
CssOutline(max_depth=1)("@media print { .a { b: c; } }\n")                      # -> '@media print\n'
```

### Level 4: Your own profile from the parts

File rules combine with `&`, `|` and `~`; the steps are presets; a registered profile is a name for both.

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
```

---

## 🛠️ Architecture & Package Structure

```
src/simplibs/extractor_css/
├── constants/            ◄── CSS_SUFFIXES, CSS_PLAIN_SUFFIXES, folder names, licence marks, the four patterns of the scanner
├── file_rules/           ◄── Rules on the path inside the source (domain folder)
│   ├── atomic/           ◄── DOT_NAME, MINIFIED_NAME, VCS_DIRS, DEPENDENCY_DIRS, OUTPUT_DIRS
│   └── css/              ◄── CSS_FILES, CSS_BASE, CSS_STRICT_EXCLUDE
├── logic/                ◄── The steps: plain functions that read a stylesheet with a scanner
│   ├── css_comment_spans.py  strip_css_comments.py  remove_css_imports.py  css_outline.py
│   └── _helpers/         ◄── Private: the scanner (scan_css) and the small parts it is made of
├── actions/              ◄── The steps as Action classes (domain folder)
├── presets/              ◄── Ready-made chains: PLAIN and LINE of each (domain folder)
├── profiles/             ◄── The five Profile objects and CSS_PROFILES (domain folder)
├── plugin/               ◄── register_all: the target of the entry point
└── py.typed
```

The folder `_helpers/` is private: it holds the scanner and the parts it is made of, and nothing in it is a public name.

The package root exports **the steps** and `register_all`. The four domain folders have their own `__all__` and are imported through their domain — a function and an action are different kinds of thing and should stay
visibly different at the import line:

```python
from simplibs.extractor_css import strip_css_comments, css_outline, register_all   # the steps and the entry point
from simplibs.extractor_css.actions import StripCssComments                          # the steps as actions
from simplibs.extractor_css.file_rules import CSS_BASE, CSS_STRICT_EXCLUDE           # the rules
from simplibs.extractor_css.presets import CSS_PLAIN_CLEAN                           # ready-made chains
from simplibs.extractor_css.profiles import CSS_SRC_CLEAN                            # the profiles as objects
```

The fixed values are imported from `simplibs.extractor_css.constants`. The ranges the steps find are `simplibs.text.Span`; the type is taken from `simplibs-text`, not defined here.

---

## 🔧 `logic/` — The steps that read stylesheets

Plain functions: a stylesheet as a text in, a text out (one of them gives the positions of the comments). All take their options as keyword-only parameters. A file that looks damaged comes back unchanged, with a warning.

| Function             | Description / Parameters                                                                                                                     |
|----------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| `css_comment_spans`  | Finds the comments with the scanner; returns a `Span` for each, from the blanks in front to the end (`text`, keyword-only: `line_comments=False`, `keep_license=False`). |
| `strip_css_comments` | Removes the comments; a line that held only a comment disappears, a comment between two tokens leaves a space (`text`, keyword-only: `line_comments=False`, `keep_license=False`). |
| `remove_css_imports` | Removes `@import`, `@use` and `@forward`; the lines they stood on disappear (`text`, keyword-only: `line_comments=False`).                      |
| `css_outline`        | Writes the headers of the blocks, one per line, indented by depth (`text`, keyword-only: `line_comments=False`, `max_depth=None`).            |

➡️ [README_EXTRACTOR_CSS_LOGIC](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/logic/README_EXTRACTOR_CSS_LOGIC.md)

---

## ⚙️ `actions/` — Pipeline steps

Every step except `css_comment_spans` is also an `Action` of [`simplibs-actions`](https://pypi.org/project/simplibs-actions/): configured once, called with the **text** as its main input, chainable with `>>`. The options of the
function are the options of the action: `StripCssComments(line_comments=True)`. Actions are a separate domain, imported through `simplibs.extractor_css.actions`; `css_comment_spans` has no action, because it returns spans and not a text.

| Action             | Over                 | Description                                                  |
|--------------------|----------------------|--------------------------------------------------------------|
| `StripCssComments` | `strip_css_comments` | Takes the comments out of the text flowing in.               |
| `RemoveCssImports` | `remove_css_imports` | Takes `@import`, `@use` and `@forward` out.                  |
| `CssOutline`       | `css_outline`        | Turns the text into the list of its selectors and at-rules.  |

➡️ [README_EXTRACTOR_CSS_ACTIONS](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_ACTIONS.md)

---

## 🧩 `presets/` — Ready-made chains

Chains of actions, built once, that the profiles use. Each exists twice: `PLAIN` for `.css`, where only `/* ... */` is a comment, and `LINE` for `.scss` and `.less`, where `// ...` is one too.

| Preset                 | Chain                                                                                         |
|------------------------|-----------------------------------------------------------------------------------------------|
| `CSS_PLAIN_CLEAN`      | `StripCssComments() >> CLEANUP_WHITESPACE` — the imports stay.                                |
| `CSS_PLAIN_NO_IMPORTS` | `StripCssComments() >> RemoveCssImports() >> COMPACT` — the rules only.                       |
| `CSS_PLAIN_OUTLINE`    | `CssOutline()` — the selectors and at-rules.                                                  |
| `CSS_LINE_CLEAN`       | `StripCssComments(line_comments=True) >> CLEANUP_WHITESPACE` — the imports stay.              |
| `CSS_LINE_NO_IMPORTS`  | `StripCssComments(line_comments=True) >> RemoveCssImports(line_comments=True) >> COMPACT`     |
| `CSS_LINE_OUTLINE`     | `CssOutline(line_comments=True)`                                                              |

`CLEANUP_WHITESPACE` squeezes blank runs to one line, `COMPACT` removes every blank line.

➡️ [README_EXTRACTOR_CSS_PRESETS](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_PRESETS.md)

---

## 📋 `profiles/` — The five profiles

Registered in the system `css`; also importable as `Profile` objects. A profile of a kind that has steps gives `.css` the `PLAIN` preset and `.scss` and `.less` the `LINE` one.

| Profile               | Output                   | Description                                                                                   |
|-----------------------|--------------------------|-----------------------------------------------------------------------------------------------|
| `css/code-clean`      | `css_code_clean.md`      | Stylesheets without comments and extra blank lines (imports stay).                            |
| `css/code-no-imports` | `css_code_no_imports.md` | Pure rules: no imports, comments or blank lines.                                              |
| `css/data-all`        | `css_data_all.md`        | Every relevant stylesheet, as it is.                                                          |
| `css/outline`         | `css_outline.md`         | Overview of the stylesheets: selectors and at-rules without declarations.                     |
| `css/src-clean`       | `css_src_clean.md`       | Like `code-clean`, without minified files, packages of other people and generated output.     |

`CSS_PROFILES` is the tuple of all five, in the order the listings show them.

➡️ [README_EXTRACTOR_CSS_PROFILES](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_PROFILES.md)

---

## 📐 `file_rules/` — Which files are worth reading

Rules on the path **inside** the source folder: `Rule` objects of [`simplibs-rules`](https://pypi.org/project/simplibs-rules/), composable with `&`, `|` and `~`.

| Rule                 | Description                                                                                                  |
|----------------------|--------------------------------------------------------------------------------------------------------------|
| `CSS_BASE`           | The default choice: every stylesheet that is not hidden — minified files and SCSS partials included.          |
| `CSS_FILES`          | A file with a stylesheet suffix: `.css`, `.scss`, `.less`.                                                    |
| `CSS_STRICT_EXCLUDE` | What is not the project's own source: minified files, packages of other people, generated output, version control. |
| `DOT_NAME`           | The file name starts with a dot.                                                                             |
| `MINIFIED_NAME`      | The name is `something.min` plus a suffix (`app.min.css`).                                                   |
| `VCS_DIRS`           | A folder above the file is a version-control folder (`.git`, `.svn`, `.hg`, `.bzr`).                          |
| `DEPENDENCY_DIRS`    | A folder above the file holds stylesheets of other people (`node_modules`, `bower_components`, `vendor`).     |
| `OUTPUT_DIRS`        | A folder above the file holds generated files (`dist`, `staticfiles`, `coverage`, …).                         |

➡️ [README_EXTRACTOR_CSS_FILE_RULES](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_FILE_RULES.md)

---

## 🔖 `constants/` — Fixed values

Thirteen fixed values the rules, the scanner and the profiles are built from. The indented Sass syntax (`.sass`) is not among the suffixes: it has no braces, so its outline could not be read the same way.

| Constant                       | Description                                                                          |
|--------------------------------|--------------------------------------------------------------------------------------|
| `CSS_SUFFIXES`                 | `(".css", ".scss", ".less")` — every stylesheet the library reads.                   |
| `CSS_PLAIN_SUFFIXES`           | `(".css",)` — where only `/* ... */` is a comment.                                   |
| `CSS_LINE_COMMENT_SUFFIXES`    | `(".scss", ".less")` — where `// ...` is a comment too.                              |
| `CSS_EXTRA_LANGUAGE_BY_SUFFIX` | The code-fence language of `.scss` and `.less`.                                      |
| `CSS_DEPENDENCY_DIR_NAMES`     | Folders of stylesheets written by other people.                                      |
| `CSS_OUTPUT_DIR_NAMES`         | Folders of generated files and reports.                                              |
| `CSS_LICENSE_START`            | `"/*!"` — how a comment that has to survive minification begins.                     |
| `CSS_LICENSE_TAGS`             | `("@license", "@preserve")` — words that mark a comment as one to keep.              |
| `CSS_MINIFIED_ENDING`          | `".min"` — what the stem of a minified stylesheet ends with.                         |
| `CSS_TOKEN_PATTERN`            | Where the scanner stops in plain CSS: a quote, `/*`, `url(`.                         |
| `CSS_LINE_TOKEN_PATTERN`       | Where the scanner stops in SCSS and Less: the same, and `//`.                        |
| `CSS_BLOCK_MARKS_PATTERN`      | The braces and the semicolon that structure a stylesheet.                            |
| `CSS_IMPORT_PATTERN`           | The start of `@import`, `@use` and `@forward` at the beginning of a line.            |

➡️ [README_EXTRACTOR_CSS_CONSTANTS](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_CONSTANTS.md)

---

## 🔌 `plugin/` — The meeting point with the extractor

| Function       | Description / Parameters                                                                                                                                      |
|----------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `register_all` | Registers the languages of `.scss` and `.less` and the five profiles in the extractor's registries and returns the profile keys; the target of the entry point `simplibs.extractor.plugins` (keyword-only: `replace_existing=True`). |

The entry point lives in this library's `pyproject.toml`; the extractor's `load_plugins()` finds it, so nothing is imported by name. From Python, call `load_plugins()` of the extractor once before a profile is looked up.

➡️ [README_EXTRACTOR_CSS_PLUGIN](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_PLUGIN.md)

---

## ⚠️ Exceptions

The library defines no exceptions of its own, and **a stylesheet is never the cause of an error**: a file that looks damaged is a warning, not an exception. What can be raised is a structured
[`simplibs.exception`](https://pypi.org/project/simplibs-exception/) card from a library it builds on, or a `ValidationError` for a wrong argument; a caller that wants "any error of the family" catches `SimpleError`.

What is an exception and what is not:

| Situation                                                                                          | How it is reported                                                              |
|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| A step called directly on a stylesheet with a comment, a string or an address never closed          | a `UserWarning`; the text comes back unchanged (`css_comment_spans`: `[]`)       |
| `css_outline` on a stylesheet whose braces do not pair up                                          | a `UserWarning`; the text comes back unchanged                                  |
| The same inside an **extraction**                                                                  | **not raised**: the file stays in the output, marked `partial`, the warning is in the report |
| A wrong **type or value** of an argument (`text=5`, `max_depth=0`)                                 | a `ValidationError` from `simplibs-validate`                                    |
| A profile key that is taken, with `register_all(replace_existing=False)`                           | the card of the extractor's registry (`EXTRACTOR_PROFILE_EXISTS`)               |

Each helper README ends with the errors of its own package.

---

## 📚 Documentation

The detailed references — every function, rule and profile with its parameters, return value, raised errors, an example and a look under the hood:

| Reference | What it describes |
|-----------|-------------------|
| [LOGIC](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/logic/README_EXTRACTOR_CSS_LOGIC.md) | the four steps: comments, imports, the outline — and the scanner under them |
| [ACTIONS](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_ACTIONS.md) | the steps as pipeline actions |
| [PRESETS](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_PRESETS.md) | the six ready-made chains, `PLAIN` and `LINE` |
| [PROFILES](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_PROFILES.md) | the five profiles, one stylesheet through each, a profile of your own |
| [FILE_RULES](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_FILE_RULES.md) | which files are worth reading: the atomic pieces and the rules of a stylesheet project |
| [CONSTANTS](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_CONSTANTS.md) | the fixed values: suffixes, folder names, licence marks, the patterns of the scanner |
| [PLUGIN](https://github.com/simplibs/simplibs-extractor-css/blob/main/docs/README_EXTRACTOR_CSS_PLUGIN.md) | `register_all` and how the extractor finds this add-on |

---

## 🔗 Related libraries

* **[`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/)** — the extractor this library is an add-on of: the six phases, the profiles and the command.
* **[`simplibs-extractor-python`](https://pypi.org/project/simplibs-extractor-python/)** and **[`simplibs-extractor-javascript`](https://pypi.org/project/simplibs-extractor-javascript/)** — the sister add-ons for Python and for JavaScript and TypeScript projects.
* **[`simplibs-text`](https://pypi.org/project/simplibs-text/)** — `remove_spans` cuts the ranges the steps find, `Span` is their type; `CLEANUP_WHITESPACE` and `COMPACT` close the presets.
* **[`simplibs-actions`](https://pypi.org/project/simplibs-actions/)** — the `Action` the steps are wrapped in.
* **[`simplibs-path`](https://pypi.org/project/simplibs-path/)** — the path rules (`HasSuffix`, `NameIs`, `StemIs`, `AnyParentNameIs`) and `IGNORE_VCS`.
* **[`simplibs-rules`](https://pypi.org/project/simplibs-rules/)** — the `Rule` object and its building blocks (`IsIn`, `StartsWith`, `EndsWith`).
* **[`simplibs-validate`](https://pypi.org/project/simplibs-validate/)** and **[`simplibs-types`](https://pypi.org/project/simplibs-types/)** — the check of every signature, and the `int_positive` type of the outline depth.
* **[`simplibs-exception`](https://pypi.org/project/simplibs-exception/)** — the error cards raised by the libraries underneath; it comes with the extractor.

---

## ☯️ About simplibs

All libraries in the **simplibs** (Simple Libraries) ecosystem share a common
engineering philosophy:

* **Dyslexia-friendly:**
We actively minimize cognitive load. Code is atomized into small, self-contained units,
files are named directly after the logical task they perform, and explanations describe
*why* something is designed, not just *what* it is.
* **Programmer's Zen:**
Nothing should be missing, and nothing should be superfluous. We value clean execution
paths and robust, understandable code architectures over rushed, messy feature sets.
* **Defensive Style:**
We actively anticipate edge cases and failure modes so that only safe operational paths
remain. Our code is built to degrade gracefully rather than crash unexpectedly.
* **Minimalism:**
Find the most direct path to the goal in as few operational steps as possible without
taking shortcuts on safety, readability, or completeness.
* **Code as Craft:**
Code should be pleasant to look at, readable at a glance, and evoke structural harmony.
We treat software engineering as a precision trade.

---

### 🤝 Contributing & Community

This is an **open-source project** built with love and care. We strongly believe in
community collaboration and welcome any feedback, bug reports, or feature ideas!

* **Want to contribute?** Feel free to open an Issue or submit a Pull Request.
* **Want to get in touch?** If you'd like to discuss the project further, collaborate,
  or just say hello, feel free to open a GitHub Issue or start a Discussion.

---

### 📝 License

This library is released under the **MIT License**. Build great things!

---
