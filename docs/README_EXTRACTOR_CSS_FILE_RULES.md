# 📐 `extractor_css/file_rules` — Which Files Are Worth Reading

The `file_rules` package holds **rules on the path of a file**: which files of a project are stylesheets worth reading, and which are somebody else's, generated, or
under version control. Eight rules in two groups — five *atomic* pieces of one idea each, and three *stylesheet* rules that combine them.

```python
from simplibs.extractor_css.file_rules import CSS_BASE, CSS_STRICT_EXCLUDE

CSS_BASE.is_valid("src/app.scss")                  # -> True
CSS_STRICT_EXCLUDE.is_valid("node_modules/x/a.css")   # -> True
```

Every element is a [`Rule`](https://pypi.org/project/simplibs-rules/) of `simplibs-rules`: it is asked with `is_valid(path)` (or by calling it), and rules combine with
`&` (and), `|` (or) and `~` (not). The profiles use them as `include` and `exclude`; a program can build its own selection from the same pieces.

| You want to …                                                              | Use                        |
|----------------------------------------------------------------------------|----------------------------|
| take every stylesheet that is not hidden (the default `include`)           | `CSS_BASE`                 |
| take files by their suffix alone                                           | `CSS_FILES`                |
| leave out everything that is not the project's own source (the `exclude`)  | `CSS_STRICT_EXCLUDE`       |
| judge one thing only — a dot name, a minified name, a kind of folder       | an atomic piece            |

## A note on the path inside the source

The rules judge the path **relative to the source folder**, not the whole path on the disk. A project that lies in a folder called `dist` is therefore not dropped as
"generated output": the rule sees only what is *inside* the source. That is also why the rules about folders look at the folders **above** the file and never at the
file's own name — `vendor.css` is not inside a folder called `vendor`.

## A note on the base rule that has no switches

`CSS_BASE` is `CSS_FILES & ~DOT_NAME` and nothing more. The JavaScript add-on has switches for `index.*` and `_*` files because the old code dropped both and a project
may need them back. Here nothing needs a switch: an SCSS partial such as `_variables.scss` is a perfectly ordinary source file and is always taken. **Minified files are taken
too:** a profile that gives "every file as it is" must not decide what a reader may see. The strict exclusion is the one place that leaves them out.

## A note on what the strict exclusion does not leave out

There are **no tests, no configuration files and no asset folders** in `CSS_STRICT_EXCLUDE`: a stylesheet is not tested, no tool keeps its settings in a file with a stylesheet
suffix, and `static/` is where a Django project keeps its *own* styles. What is left out is what a reader of the project's source would not want: minified files,
packages of other people, generated output and version control.

## A note on rules built once

Every rule is built **once**, when the package is imported, and shared by every profile that uses it. A rule holds no state, so one object serves any number of selections.
Each is declared `Final`.

---

## 🧭 Table of Contents

**Atomic pieces** — one idea each

* [`DOT_NAME`](#dot_name) · [`MINIFIED_NAME`](#minified_name) · [`VCS_DIRS`](#vcs_dirs) · [`DEPENDENCY_DIRS`](#dependency_dirs) · [`OUTPUT_DIRS`](#output_dirs)

**Stylesheet rules** — built from the pieces

* [`CSS_FILES`](#css_files) · [`CSS_BASE`](#css_base) · [`CSS_STRICT_EXCLUDE`](#css_strict_exclude)

**Your own selection**

* [Combining the rules](#combining-the-rules)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-file_rules--which-files-are-worth-reading)

---

### `DOT_NAME`

The file name starts with a dot (`.hidden.css`) — hidden by convention.

**Built from:** `NameIs(StartsWith("."))`.

**Example usage:**
```python
from simplibs.extractor_css.file_rules import DOT_NAME

DOT_NAME.is_valid(".hidden.css")        # -> True
DOT_NAME.is_valid("src/.x.css")         # -> True
DOT_NAME.is_valid("visible.css")        # -> False
DOT_NAME.is_valid(".cache/app.css")     # -> False     only the name is judged, not the folders
```

**Notes.** Dot files are settings and tool state, not source. Only the name of the file is judged: a visible file inside a `.cache` folder is not hidden by this rule (the strict
exclusions look at folders). Used by [`CSS_BASE`](#css_base).

**Under the hood:**
```python
DOT_NAME: Final[Rule] = NameIs(StartsWith("."))
```

[▲ Back to top](#-table-of-contents)

---

### `MINIFIED_NAME`

The file is a minified stylesheet: its name is `something.min` plus a suffix (`app.min.css`).

**Built from:** `StemIs(EndsWith(CSS_MINIFIED_ENDING))`, with [`CSS_MINIFIED_ENDING`](README_EXTRACTOR_CSS_CONSTANTS.md#marks-that-decide) = `".min"`.

**Example usage:**
```python
from simplibs.extractor_css.file_rules import MINIFIED_NAME

MINIFIED_NAME.is_valid("app.min.css")           # -> True
MINIFIED_NAME.is_valid("dist/theme.min.scss")   # -> True
MINIFIED_NAME.is_valid("admin.css")             # -> False
```

**Notes.** `StemIs` judges the name **without its last suffix**, so the check is exactly "the part before `.css` ends with `.min`" and a name such as `admin.css` can never be taken for a
minified one. A minified stylesheet is one very long line: it costs the most tokens and says the least.

**Under the hood:**
```python
MINIFIED_NAME: Final[Rule] = StemIs(EndsWith(CSS_MINIFIED_ENDING))
```

[▲ Back to top](#-table-of-contents)

---

### `VCS_DIRS`

The file lies inside a version-control folder (`.git`, `.svn`, `.hg`, `.bzr`).

**Built from:** `AnyParentNameIs(IsIn(IGNORE_VCS))`, with `IGNORE_VCS` from [`simplibs-path`](https://pypi.org/project/simplibs-path/).

**Example usage:**
```python
from simplibs.extractor_css.file_rules import VCS_DIRS

VCS_DIRS.is_valid(".git/hooks/theme.css")     # -> True
VCS_DIRS.is_valid(".github/a.css")            # -> False     `.github` is not `.git`
VCS_DIRS.is_valid("src/app.css")              # -> False
```

**Notes.** The names are not kept here: version control is the same for every language, so the library borrows the list instead of keeping its own. `IsIn` compares a folder name
**as a whole**, so a folder that only *starts* like a version-control one is not taken.

**Under the hood:**
```python
VCS_DIRS: Final[Rule] = AnyParentNameIs(IsIn(IGNORE_VCS))
```

[▲ Back to top](#-table-of-contents)

---

### `DEPENDENCY_DIRS`

The file lies inside a folder of stylesheets written by other people (`node_modules`, `bower_components`, `vendor`).

**Built from:** `AnyParentNameIs(IsIn(CSS_DEPENDENCY_DIR_NAMES))`, with the names from [`constants`](README_EXTRACTOR_CSS_CONSTANTS.md#folder-names).

**Example usage:**
```python
from simplibs.extractor_css.file_rules import DEPENDENCY_DIRS

DEPENDENCY_DIRS.is_valid("node_modules/pkg/dist/a.css")     # -> True
DEPENDENCY_DIRS.is_valid("static/vendor/bootstrap.css")     # -> True
DEPENDENCY_DIRS.is_valid("src/app.css")                     # -> False
DEPENDENCY_DIRS.is_valid("vendor.css")                      # -> False     a file name is not a folder
```

**Notes.** A framework copied into the project (`static/vendor/bootstrap/`) or installed by a package manager is thousands of lines that are not the project's own.

**Under the hood:**
```python
DEPENDENCY_DIRS: Final[Rule] = AnyParentNameIs(IsIn(CSS_DEPENDENCY_DIR_NAMES))
```

[▲ Back to top](#-table-of-contents)

---

### `OUTPUT_DIRS`

The file lies inside a folder of generated files (`dist`, `staticfiles`, `coverage`, …).

**Built from:** `AnyParentNameIs(IsIn(CSS_OUTPUT_DIR_NAMES))`, with the names from [`constants`](README_EXTRACTOR_CSS_CONSTANTS.md#folder-names).

**Example usage:**
```python
from simplibs.extractor_css.file_rules import OUTPUT_DIRS

OUTPUT_DIRS.is_valid("dist/app.css")                   # -> True
OUTPUT_DIRS.is_valid("staticfiles/admin/base.css")     # -> True
OUTPUT_DIRS.is_valid("static/site.css")                # -> False     `static/` holds the project's own styles
```

**Notes.** These folders contain stylesheets that a tool made: reading them repeats the source in another shape.

**Under the hood:**
```python
OUTPUT_DIRS: Final[Rule] = AnyParentNameIs(IsIn(CSS_OUTPUT_DIR_NAMES))
```

[▲ Back to top](#-table-of-contents)

---

### `CSS_FILES`

The file is a stylesheet: it has one of the suffixes `.css`, `.scss`, `.less`.

**Built from:** `HasSuffix(*CSS_SUFFIXES)`, with [`CSS_SUFFIXES`](README_EXTRACTOR_CSS_CONSTANTS.md#suffixes).

**Example usage:**
```python
from simplibs.extractor_css.file_rules import CSS_FILES

CSS_FILES.is_valid("src/app.css")             # -> True
CSS_FILES.is_valid("src/theme.less")          # -> True
CSS_FILES.is_valid("src/_variables.scss")     # -> True
CSS_FILES.is_valid("Dir/FOO.CSS")             # -> True      the suffix is compared case-insensitively
CSS_FILES.is_valid("README.md")               # -> False
CSS_FILES.is_valid("src/style.sass")          # -> False     the indented syntax is not read
```

**Notes.** The core of `CSS_BASE`. `HasSuffix` compares case-insensitively and takes several suffixes at once. SCSS and Less files are stylesheets in every sense that matters to a reader, so they are
taken together with plain CSS; **which steps** they get is decided by the [profiles](README_EXTRACTOR_CSS_PROFILES.md), per suffix.

**Under the hood:**
```python
CSS_FILES: Final[Rule] = HasSuffix(*CSS_SUFFIXES)
```

[▲ Back to top](#-table-of-contents)

---

### `CSS_BASE`

The default rule for stylesheets worth reading: every stylesheet that is not hidden. Every profile of this library uses it as `include`.

**Built from:** [`CSS_FILES`](#css_files) `& ~`[`DOT_NAME`](#dot_name).

**Example usage:**
```python
from simplibs.extractor_css.file_rules import CSS_BASE

CSS_BASE.is_valid("src/app.css")              # -> True
CSS_BASE.is_valid("src/_variables.scss")      # -> True      a partial is an ordinary source file
CSS_BASE.is_valid("src/.hidden.css")          # -> False     a dot name
CSS_BASE.is_valid("static/app.min.css")       # -> True      minified files are taken too
CSS_BASE.is_valid("README.md")                # -> False     not a stylesheet
```

**Notes.** There are no switches (see [the note above](#a-note-on-the-base-rule-that-has-no-switches)). Dot *folders* are not judged here — only the name of the file.

**Under the hood:**
```python
CSS_BASE: Final[Rule] = CSS_FILES & ~DOT_NAME
```

[▲ Back to top](#-table-of-contents)

---

### `CSS_STRICT_EXCLUDE`

Everything that is a stylesheet but **not the project's own source**: minified files, packages of other people, generated output, version control. The `exclude` of the profile
[`css/src-clean`](README_EXTRACTOR_CSS_PROFILES.md#css_src_clean).

**Built from:** [`MINIFIED_NAME`](#minified_name) `|` [`VCS_DIRS`](#vcs_dirs) `|` [`DEPENDENCY_DIRS`](#dependency_dirs) `|` [`OUTPUT_DIRS`](#output_dirs).

**Example usage:**
```python
from simplibs.extractor_css.file_rules import CSS_STRICT_EXCLUDE

CSS_STRICT_EXCLUDE.is_valid("static/app.min.css")         # -> True
CSS_STRICT_EXCLUDE.is_valid("node_modules/pkg/a.css")     # -> True
CSS_STRICT_EXCLUDE.is_valid("dist/a.css")                 # -> True
CSS_STRICT_EXCLUDE.is_valid(".git/x.css")                 # -> True
CSS_STRICT_EXCLUDE.is_valid("src/app.css")                # -> False
CSS_STRICT_EXCLUDE.is_valid("static/site.css")            # -> False     `static/` is the project's own
```

**Notes.** It judges nothing about the suffix: it is an `exclude`, used together with an `include` such as `CSS_BASE`. See
[the note above](#a-note-on-what-the-strict-exclusion-does-not-leave-out) for what is deliberately not in it.

**Under the hood:**
```python
CSS_STRICT_EXCLUDE: Final[Rule] = MINIFIED_NAME | VCS_DIRS | DEPENDENCY_DIRS | OUTPUT_DIRS
```

[▲ Back to top](#-table-of-contents)

---

### Combining the rules

The rules are ordinary `Rule` objects, so a selection of your own is one expression away. The profiles are built the same way, and
[a profile of your own](README_EXTRACTOR_CSS_PROFILES.md#a-profile-of-your-own) takes such an expression as its `include` or `exclude`.

**Example usage:**
```python
from simplibs.extractor_css.file_rules import CSS_BASE, CSS_STRICT_EXCLUDE, MINIFIED_NAME, DEPENDENCY_DIRS

only_minified = CSS_BASE & MINIFIED_NAME
only_minified.is_valid("a.min.css")                 # -> True
only_minified.is_valid("a.css")                     # -> False

own_source = CSS_BASE & ~CSS_STRICT_EXCLUDE         # what `css/src-clean` reads
own_source.is_valid("src/app.css")                  # -> True
own_source.is_valid("static/app.min.css")           # -> False

not_packages = CSS_BASE & ~DEPENDENCY_DIRS          # everything, only without other people's packages
not_packages.is_valid("static/vendor/a.css")        # -> False
not_packages.is_valid("static/app.min.css")         # -> True
```

[▲ Back to top](#-table-of-contents)

---

### Errors of this package

It raises no cards of its own: a rule answers `True` or `False` and builds no error. Whatever the rules of
[`simplibs-rules`](https://pypi.org/project/simplibs-rules/) and [`simplibs-path`](https://pypi.org/project/simplibs-path/) raise surfaces unchanged.

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../README.md#-file_rules--which-files-are-worth-reading)
