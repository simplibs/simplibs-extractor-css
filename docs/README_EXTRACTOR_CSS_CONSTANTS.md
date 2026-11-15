# 🔖 `extractor_css/constants` — Fixed Values

The `constants` package holds **the fixed values** that the file rules, the scanner and the profiles are built from: the suffixes of
stylesheets, the names of folders that hold other people's or generated files, the marks that make a comment worth keeping, and the four
compiled patterns the scanner stops at. Thirteen values in four groups, each a tuple, a string, a small dict or a compiled pattern.

```python
from simplibs.extractor_css.constants import CSS_SUFFIXES, CSS_LICENSE_TAGS

CSS_SUFFIXES                  # -> ('.css', '.scss', '.less')
CSS_LICENSE_TAGS              # -> ('@license', '@preserve')
```

Every value is declared `Final`, so a type checker stops an accidental reassignment. Nothing here is a function: the values are the *data*,
and the rules and steps that use them live in the layers to the right ([`file_rules`](README_EXTRACTOR_CSS_FILE_RULES.md),
[`logic`](logic/README_EXTRACTOR_CSS_LOGIC.md)).

## A note on the two halves of the suffixes

The profiles choose the steps of a file **by its suffix**, because a step is given the text only, never the path. In plain `.css` the characters `//`
mean nothing, so they must never be cut; in `.scss` and `.less` they start a comment. That is why the suffixes are two tuples — `CSS_PLAIN_SUFFIXES`
and `CSS_LINE_COMMENT_SUFFIXES` — and `CSS_SUFFIXES` is only the two joined: a suffix added to either of them is a stylesheet at once, and nobody
has to remember a third place. The indented Sass syntax (`.sass`) is not here: it has no braces, so its outline could not be read the same way.

## A note on folder names

Each add-on decides for its own language what counts as other people's code or generated output; this library does not borrow the lists of the
JavaScript add-on. Two names are chosen with the stylesheets of a web project in mind: **`vendor`** is in the dependency list (in a Django
project the third-party styles live in `static/vendor/`), and **`static`** is *not* in the output list (that is where such a project keeps its own
styles). The names of version-control folders are not here at all: they come from `IGNORE_VCS` of
[`simplibs-path`](https://pypi.org/project/simplibs-path/), because version control is the same for every language.

---

## 🧭 Table of Contents

* [Suffixes](#suffixes)
* [Folder names](#folder-names)
* [Marks that decide](#marks-that-decide)
* [Patterns of the scanner](#patterns-of-the-scanner)
* [Quick reference — all 13](#quick-reference--all-13)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-constants--fixed-values)

---

### Suffixes

Four values that say which files are stylesheets and how each kind is read. `CSS_SUFFIXES` is built from the two halves.

| Name                           | Value                              | Used for                                                       |
|--------------------------------|------------------------------------|----------------------------------------------------------------|
| `CSS_PLAIN_SUFFIXES`           | `(".css",)`                        | files where only `/* ... */` is a comment                      |
| `CSS_LINE_COMMENT_SUFFIXES`    | `(".scss", ".less")`               | preprocessors where `// ...` is a comment too                  |
| `CSS_SUFFIXES`                 | `(".css", ".scss", ".less")`       | every stylesheet the library reads (`CSS_FILES`)               |
| `CSS_EXTRA_LANGUAGE_BY_SUFFIX` | `{".scss": "scss", ".less": "less"}` | the code-fence language of the suffixes the extractor does not know |

**Example usage:**
```python
from simplibs.extractor_css.constants import CSS_PLAIN_SUFFIXES, CSS_LINE_COMMENT_SUFFIXES, CSS_SUFFIXES, CSS_EXTRA_LANGUAGE_BY_SUFFIX

CSS_SUFFIXES == CSS_PLAIN_SUFFIXES + CSS_LINE_COMMENT_SUFFIXES     # -> True
CSS_EXTRA_LANGUAGE_BY_SUFFIX[".scss"]                              # -> 'scss'
".css" in CSS_EXTRA_LANGUAGE_BY_SUFFIX                             # -> False     the extractor knows `.css` itself
```

**Under the hood:**
```python
CSS_PLAIN_SUFFIXES: Final[tuple[str, ...]] = (".css",)
CSS_LINE_COMMENT_SUFFIXES: Final[tuple[str, ...]] = (".scss", ".less")
CSS_SUFFIXES: Final[tuple[str, ...]] = CSS_PLAIN_SUFFIXES + CSS_LINE_COMMENT_SUFFIXES
CSS_EXTRA_LANGUAGE_BY_SUFFIX: Final[dict[str, str]] = {
    ".scss": "scss",
    ".less": "less",
}
```

> 💡 `CSS_EXTRA_LANGUAGE_BY_SUFFIX` lists only what is missing: the markdown output writes the language after the opening fence so a viewer can colour
> the code, and [`register_all`](README_EXTRACTOR_CSS_PLUGIN.md#register_all) tells the extractor about `.scss` and `.less`. `.css` is not listed, because
> registering it again would change nothing.

[▲ Back to top](#-table-of-contents)

---

### Folder names

Two tuples of folder names, the names behind `DEPENDENCY_DIRS` and `OUTPUT_DIRS` of the [file rules](README_EXTRACTOR_CSS_FILE_RULES.md).

| Name                       | Value                                                                                                  | Folders that hold                                      |
|----------------------------|--------------------------------------------------------------------------------------------------------|--------------------------------------------------------|
| `CSS_DEPENDENCY_DIR_NAMES` | `"node_modules"`, `"bower_components"`, `"vendor"`                                                     | stylesheets written by other people                    |
| `CSS_OUTPUT_DIR_NAMES`     | `"build"`, `"dist"`, `"out"`, `".next"`, `".nuxt"`, `"staticfiles"`, `"coverage"`, `"htmlcov"`, `"storybook-static"` | generated files, build output and reports included |

**Example usage:**
```python
from simplibs.extractor_css.constants import CSS_DEPENDENCY_DIR_NAMES, CSS_OUTPUT_DIR_NAMES

"vendor" in CSS_DEPENDENCY_DIR_NAMES      # -> True
"static" in CSS_OUTPUT_DIR_NAMES          # -> False     `static/` is where a project keeps its own styles
"staticfiles" in CSS_OUTPUT_DIR_NAMES     # -> True      the target of Django's `collectstatic`
```

**Under the hood:**
```python
CSS_DEPENDENCY_DIR_NAMES: Final[tuple[str, ...]] = ("node_modules", "bower_components", "vendor")

CSS_OUTPUT_DIR_NAMES: Final[tuple[str, ...]] = (
    "build",
    "dist",
    "out",
    ".next",
    ".nuxt",
    "staticfiles",
    "coverage",
    "htmlcov",
    "storybook-static",
)
```

**Why these names.** `staticfiles` is where `collectstatic` copies the stylesheets of every installed app, the admin's included, so everything in it is either a second
copy of the project's own files or somebody else's code. `coverage`, `htmlcov` and `storybook-static` come with stylesheets of their own (`base.css`,
`style.css`). `.next` and `.nuxt` start with a dot, but [`CSS_BASE`](README_EXTRACTOR_CSS_FILE_RULES.md#css_base) leaves out only dot *files*, so without these two names the compiled
stylesheets inside would be read as source.

[▲ Back to top](#-table-of-contents)

---

### Marks that decide

Three small values that answer two questions: *is this comment one that tools keep?* and *is this file minified?*

| Name                  | Value                       | Meaning                                                                         |
|-----------------------|-----------------------------|---------------------------------------------------------------------------------|
| `CSS_LICENSE_START`   | `"/*!"`                     | how a comment that has to survive minification begins                           |
| `CSS_LICENSE_TAGS`    | `("@license", "@preserve")` | words anywhere inside a comment that mark it as one to keep                     |
| `CSS_MINIFIED_ENDING` | `".min"`                    | what the stem of a minified stylesheet ends with (`app.min.css`)                |

**Example usage:**
```python
from simplibs.extractor_css.constants import CSS_LICENSE_START, CSS_LICENSE_TAGS, CSS_MINIFIED_ENDING

CSS_LICENSE_START                          # -> '/*!'
"@preserve" in CSS_LICENSE_TAGS            # -> True
"app.min".endswith(CSS_MINIFIED_ENDING)    # -> True      the stem of `app.min.css`
"administration".endswith(CSS_MINIFIED_ENDING)   # -> False
```

**Under the hood:**
```python
CSS_LICENSE_START: Final[str] = "/*!"
CSS_LICENSE_TAGS: Final[tuple[str, ...]] = ("@license", "@preserve")
CSS_MINIFIED_ENDING: Final[str] = ".min"
```

**Why they are the minifiers' convention.** A licence or a version banner is the one comment a reader of a stylesheet may not want to lose, and the
convention that marks it is the one minifiers already follow: a leading `!`, or one of the two words. With `keep_license=True`
[`strip_css_comments`](logic/README_EXTRACTOR_CSS_LOGIC.md#strip_css_comments) keeps such a comment too. A minified stylesheet is one very long line: it
costs the most tokens and says the least, and the readable file it was made from is usually next to it.

> 💡 The ending is compared with the name **without its last suffix**, so `app.min.css` is minified and `administration.css` is not.

[▲ Back to top](#-table-of-contents)

---

### Patterns of the scanner

Four compiled patterns. Three of them tell the scanner or a step *where to look*; the fourth finds the start of an import.

| Name                      | Matches                                                                       | Flags                    | Used by                       |
|---------------------------|-------------------------------------------------------------------------------|--------------------------|-------------------------------|
| `CSS_TOKEN_PATTERN`       | a quote, `/*`, or `url(` — where something interesting begins in plain CSS    | `IGNORECASE`             | the scanner, for `.css`       |
| `CSS_LINE_TOKEN_PATTERN`  | the same, and `//` — where it begins in SCSS and Less                         | `IGNORECASE`             | the scanner, for `.scss`, `.less` |
| `CSS_BLOCK_MARKS_PATTERN` | one of the three characters `{`, `}` and `;` that structure a stylesheet      | none                     | the outline, the end of an import |
| `CSS_IMPORT_PATTERN`      | `@import`, `@use` or `@forward` at the start of a line (group `at` is the `@`) | `MULTILINE`, `IGNORECASE` | `remove_css_imports`          |

**Example usage:**
```python
from simplibs.extractor_css.constants import CSS_TOKEN_PATTERN, CSS_LINE_TOKEN_PATTERN, CSS_BLOCK_MARKS_PATTERN, CSS_IMPORT_PATTERN

sample = 'a{b:url(x) "s" /* c */ // d}'
CSS_TOKEN_PATTERN.findall(sample)                                  # -> ['url(', '"', '"', '/*']
CSS_LINE_TOKEN_PATTERN.findall(sample)                             # -> ['url(', '"', '"', '/*', '//']      the same, and `//`
CSS_BLOCK_MARKS_PATTERN.findall("a { b: c; }")                     # -> ['{', ';', '}']
[m.start("at") for m in CSS_IMPORT_PATTERN.finditer('@import "a";\n  @use "b";\n@use-foo;\nx @import "c";\n')]   # -> [0, 15]
```

**Under the hood:**
```python
CSS_TOKEN_PATTERN: Final[re.Pattern[str]] = re.compile(r"""['"]|/\*|(?<![\w-])url\(""", re.IGNORECASE)
CSS_LINE_TOKEN_PATTERN: Final[re.Pattern[str]] = re.compile(r"""['"]|/\*|//|(?<![\w-])url\(""", re.IGNORECASE)
CSS_BLOCK_MARKS_PATTERN: Final[re.Pattern[str]] = re.compile(r"[{};]")

CSS_IMPORT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""^[ \t]*(?P<at>@)(?:import|use|forward)(?![\w-])""",
    re.MULTILINE | re.IGNORECASE,
)
```

**Why a separate pattern for `//`.** SCSS and Less have a second kind of comment that runs to the end of the line. It is a separate pattern and not a switch inside the first
one, so a plain `.css` file can never have its `//` cut by mistake. In both patterns strings and `url(` are found **before** a `//` that lies after them in the same line, so
`url(//cdn.example.com/a.png)` is skipped as an address and is not read as a comment.

**Why `url(` is a token at all.** An unquoted address may contain `//` and `/*`, and neither is a comment. The lookbehind keeps names such as `data-url(` or `curl(` from being taken for it,
and the flag makes `URL(` match too, because CSS keywords do not care about case.

**What the patterns do not decide.** `CSS_BLOCK_MARKS_PATTERN` does not know whether a mark sits inside a string or an address: the steps skip the marks the scanner has put in a literal.
`CSS_IMPORT_PATTERN` finds only where a statement **begins**, and only at the start of a line (a statement behind other code, as in a minified file, is not found). Where it ends is decided
by walking to the first semicolon outside a string. The name must end there: `@use-foo` is not `@use`.

[▲ Back to top](#-table-of-contents)

---

### Quick reference — all 13

| Group                    | Count | Members                                                                                                       |
|--------------------------|-------|---------------------------------------------------------------------------------------------------------------|
| Suffixes                 | 4     | `CSS_PLAIN_SUFFIXES`, `CSS_LINE_COMMENT_SUFFIXES`, `CSS_SUFFIXES`, `CSS_EXTRA_LANGUAGE_BY_SUFFIX`             |
| Folder names             | 2     | `CSS_DEPENDENCY_DIR_NAMES`, `CSS_OUTPUT_DIR_NAMES`                                                            |
| Marks that decide        | 3     | `CSS_LICENSE_START`, `CSS_LICENSE_TAGS`, `CSS_MINIFIED_ENDING`                                                |
| Patterns of the scanner  | 4     | `CSS_TOKEN_PATTERN`, `CSS_LINE_TOKEN_PATTERN`, `CSS_BLOCK_MARKS_PATTERN`, `CSS_IMPORT_PATTERN`                |

[▲ Back to top](#-table-of-contents)

---

### Errors of this package

It raises no cards of its own: the package holds values and no function, so there is nothing that can fail.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-constants--fixed-values)
