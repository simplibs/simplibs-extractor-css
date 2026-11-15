# 🧩 `extractor_css/presets` — Ready-Made Chains

The `presets` package holds **chains of actions, built once**, that the profiles use as their steps. Where a step of [`logic`](logic/README_EXTRACTOR_CSS_LOGIC.md) is a *function* you call on a text, a preset is an
*object* you drop into a pipeline. Six presets: three jobs — clean, take the imports away, outline — each in two kinds, `PLAIN` and `LINE`.

```python
from simplibs.extractor_css.presets import CSS_PLAIN_CLEAN, CSS_LINE_CLEAN

CSS_PLAIN_CLEAN("/* c */\na { b: c; }   \n\n\n\nd { e: f; }\n")        # -> 'a { b: c; }\n\nd { e: f; }\n'
CSS_LINE_CLEAN("// c\na { b: c; } // t\n")                             # -> 'a { b: c; }\n'
```

Presets are **not** exported from `simplibs.extractor_css` itself — they are a domain of their own, imported through `simplibs.extractor_css.presets`, which defines `__all__`. They stand to the right of
[`actions`](README_EXTRACTOR_CSS_ACTIONS.md) (a preset is built **from actions**) and to the left of the [`profiles`](README_EXTRACTOR_CSS_PROFILES.md) that use them. Every preset takes a stylesheet as text and returns a text.

| You want …                                              | for `.css`              | for `.scss` and `.less`  |
|---------------------------------------------------------|-------------------------|--------------------------|
| the comments out, whitespace tidied (imports stay)      | `CSS_PLAIN_CLEAN`       | `CSS_LINE_CLEAN`         |
| the rules only: no imports, comments or blank lines     | `CSS_PLAIN_NO_IMPORTS`  | `CSS_LINE_NO_IMPORTS`    |
| the selectors and at-rules only                         | `CSS_PLAIN_OUTLINE`     | `CSS_LINE_OUTLINE`       |

## A note on `PLAIN` and `LINE`

Each preset exists **twice**. `PLAIN` is for the suffixes where only `/* ... */` is a comment (`CSS_PLAIN_SUFFIXES`), `LINE` for those where `// ...` is one too (`CSS_LINE_COMMENT_SUFFIXES`). A step sees only the text, never the path, so the
choice is made by the profile, by suffix. Using the wrong one is not harmless: a `PLAIN` preset on SCSS leaves its `//` comments in, and a `LINE` preset on plain CSS would cut a `//` that means nothing there.

```python
CSS_PLAIN_CLEAN("a { b: c; } // not a comment in css\n")        # -> 'a { b: c; } // not a comment in css\n'
CSS_LINE_CLEAN("a { b: c; } // a comment in scss\n")            # -> 'a { b: c; }\n'
```

## A note on the order of the steps

In the presets that remove imports the **comments go first**: an import followed by a comment on the same line is a *whole line* only once the comment is gone. The import step itself gives the same result either way, because
the scanner knows what a comment is; the order is for the lines left behind.

## A note on sharing one object

A preset is created **once**, at import, and used wherever it is needed. That is safe because an action holds only its options and no state between calls, so the same object can serve any number of pipelines. Each is declared `Final`.

## A note on a preset that is a single action

`CSS_PLAIN_OUTLINE` and `CSS_LINE_OUTLINE` are one action each, and they are presets all the same: the profile picks its steps by the kind of file, and each kind has one **name**.

---

## 🧭 Table of Contents

* [`CSS_PLAIN_CLEAN`](#css_plain_clean)
* [`CSS_PLAIN_NO_IMPORTS`](#css_plain_no_imports)
* [`CSS_PLAIN_OUTLINE`](#css_plain_outline)
* [`CSS_LINE_CLEAN`](#css_line_clean)
* [`CSS_LINE_NO_IMPORTS`](#css_line_no_imports)
* [`CSS_LINE_OUTLINE`](#css_line_outline)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-presets--ready-made-chains)

---

### `CSS_PLAIN_CLEAN`

Plain CSS without comments, whitespace tidied: **the imports stay**. The everyday clean read of `.css`, and the step of `css/code-clean` and `css/src-clean` for that suffix.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**
```python
from simplibs.extractor_css.presets import CSS_PLAIN_CLEAN

CSS_PLAIN_CLEAN("/* c */\n@import 'a.css';\na { b: c; }   \n\n\n\nd { e: f; }\n")     # -> "@import 'a.css';\na { b: c; }\n\nd { e: f; }\n"
```

<details>
<summary>🔍 Under the hood</summary>

```python
CSS_PLAIN_CLEAN: Final = (
    StripCssComments()
    >> CLEANUP_WHITESPACE
)
```

In plain CSS only `/* ... */` is a comment, so the step has `line_comments` off. `CLEANUP_WHITESPACE` of [`simplibs-text`](https://pypi.org/project/simplibs-text/) leaves at most one blank line in a row.

</details>

[▲ Back to top](#-table-of-contents)

---

### `CSS_PLAIN_NO_IMPORTS`

Plain CSS reduced to its rules: no comments, no imports, no blank lines. The step of `css/code-no-imports` for `.css`.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**
```python
from simplibs.extractor_css.presets import CSS_PLAIN_NO_IMPORTS

CSS_PLAIN_NO_IMPORTS('@import "a.css"; /* c */\n\na { b: c; }\n\n\nd { e: f; }\n')     # -> 'a { b: c; }\nd { e: f; }\n'
```

<details>
<summary>🔍 Under the hood</summary>

```python
CSS_PLAIN_NO_IMPORTS: Final = (
    StripCssComments()
    >> RemoveCssImports()
    >> COMPACT
)
```

`COMPACT` of `simplibs-text` removes every blank line (and the trailing spaces), so the rules end up one after another.

</details>

[▲ Back to top](#-table-of-contents)

---

### `CSS_PLAIN_OUTLINE`

The list of selectors and at-rules of a plain CSS file. The step of `css/outline` for `.css`.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**
```python
from simplibs.extractor_css.presets import CSS_PLAIN_OUTLINE

CSS_PLAIN_OUTLINE("a { b: c; }\n@media print { d { e: f; } }\n")     # -> 'a\n@media print\n  d\n'
```

<details>
<summary>🔍 Under the hood</summary>

```python
CSS_PLAIN_OUTLINE: Final = CssOutline()
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `CSS_LINE_CLEAN`

SCSS and Less without comments (`//` included), whitespace tidied: **the imports stay**. The same as [`CSS_PLAIN_CLEAN`](#css_plain_clean) for the suffixes where `// ...` is a comment too.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**
```python
from simplibs.extractor_css.presets import CSS_LINE_CLEAN

CSS_LINE_CLEAN("// c\na { b: c; } // t\n\n\n\nd { e: f; }\n")     # -> 'a { b: c; }\n\nd { e: f; }\n'
```

<details>
<summary>🔍 Under the hood</summary>

```python
CSS_LINE_CLEAN: Final = (
    StripCssComments(line_comments=True)
    >> CLEANUP_WHITESPACE
)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `CSS_LINE_NO_IMPORTS`

SCSS and Less reduced to their rules: no comments, no imports (`@use` and `@forward` included), no blank lines. The step of `css/code-no-imports` for `.scss` and `.less`.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**
```python
from simplibs.extractor_css.presets import CSS_LINE_NO_IMPORTS

CSS_LINE_NO_IMPORTS('// c\n@use "a";\n\na { b: c; } // t\n')     # -> 'a { b: c; }\n'
```

<details>
<summary>🔍 Under the hood</summary>

```python
CSS_LINE_NO_IMPORTS: Final = (
    StripCssComments(line_comments=True)
    >> RemoveCssImports(line_comments=True)
    >> COMPACT
)
```

**Both steps know `//`.** The import step needs `line_comments` too: without it a `// @import "x";` would look like a statement that has been left in the code.

</details>

[▲ Back to top](#-table-of-contents)

---

### `CSS_LINE_OUTLINE`

The list of selectors and at-rules of an SCSS or Less file, where a brace inside a `// ...` comment is not a block. The step of `css/outline` for `.scss` and `.less`.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**
```python
from simplibs.extractor_css.presets import CSS_LINE_OUTLINE

CSS_LINE_OUTLINE(".a {\n  // x {\n  .b { c: d; }\n}\n")     # -> '.a\n  .b\n'
```

<details>
<summary>🔍 Under the hood</summary>

```python
CSS_LINE_OUTLINE: Final = CssOutline(line_comments=True)
```

</details>

[▲ Back to top](#-table-of-contents)

---

### Errors of this package

This package raises **no cards of its own** and takes no options: a preset accepts any text. An argument that is not a `str` is a `ValidationError` from the action that receives it, and a stylesheet that looks damaged
is a warning, not an error (see [the errors of `logic`](logic/README_EXTRACTOR_CSS_LOGIC.md#errors-of-this-package)).

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-presets--ready-made-chains)
