# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-11-15

The first release: the CSS add-on of [`simplibs-extractor`](https://pypi.org/project/simplibs-extractor/).
It reads CSS, SCSS and Less with a scanner that knows strings, `url()` addresses and comments, and gives the extractor five ready profiles for them.

### ✨ Added

#### Steps — plain functions, text in, text out

* `css_comment_spans(text, *, line_comments=False, keep_license=False)` — finds the comments with the scanner and returns them as `Span`s (from the blanks in front of a comment to its end); a `/*` inside a string or inside a `url(...)` address is never a comment; `//` is a comment only with `line_comments=True`; a stylesheet that looks damaged gives an empty list and a warning
* `strip_css_comments(text, *, line_comments=False, keep_license=False)` — removes every comment; a line that held only a comment disappears, `a { b: c; } /* note */` loses the note, and a comment between two tokens leaves one space where they would merge (`0/**/auto` → `0 auto`); with `keep_license=True` the comments that tools keep (`/*! … */`, `@license`, `@preserve`) stay
* `remove_css_imports(text, *, line_comments=False)` — removes `@import`, `@use` and `@forward` statements, and the lines they stood on; the end of a statement is the first semicolon outside a string or an address, so `@import url("a;b.css");` is one statement; an import inside a comment is left alone
* `css_outline(text, *, line_comments=False, max_depth=None)` — writes the headers of the blocks (selectors and at-rules, without the declarations), one per line, indented by two spaces for each level of nesting; `max_depth` limits the levels; a `{` inside a comment or a string is not a block, and SCSS interpolation `#{ … }` is not a block either

#### The scanner

* One pass over the stylesheet that knows quoted strings, unquoted `url(...)` addresses and comments, and jumps from one stop to the next instead of walking every character. It is not a parser: it builds no tree and there is no syntax it refuses
* `//` is read as a comment only for SCSS and Less; in plain CSS it is left alone, so `url(//cdn.example.com/a.png)` and a stray `//` are never cut
* A comment that is never closed, a string that is never closed and an address that is never closed are noticed; the steps then return the text **unchanged** and warn (a `UserWarning` for each place), because cutting on such a basis would lose text silently. `css_outline` does the same for braces that do not pair up

#### Actions — the steps as links of a pipeline

* `StripCssComments`, `RemoveCssImports`, `CssOutline` — one `Action` over each step that returns a text, made with `create_action`; the options of the function are the options of the action. `css_comment_spans` has no action: it returns spans, not a text. Imported from `simplibs.extractor_css.actions`

#### Presets — ready-made chains

* `PLAIN` presets for `.css`, where only `/* … */` is a comment, and `LINE` presets for `.scss` and `.less`, where `// …` is a comment too:
  * `CSS_PLAIN_CLEAN`, `CSS_LINE_CLEAN` — comments out, whitespace tidied; the imports stay
  * `CSS_PLAIN_NO_IMPORTS`, `CSS_LINE_NO_IMPORTS` — comments and imports out, no blank lines; the rules and nothing else
  * `CSS_PLAIN_OUTLINE`, `CSS_LINE_OUTLINE` — the selectors and at-rules only
* Imported from `simplibs.extractor_css.presets`

#### Profiles — registered in the system `css`

* `css/code-clean` — `css_code_clean.md`
* `css/code-no-imports` — `css_code_no_imports.md`
* `css/data-all` — `css_data_all.md`, every relevant stylesheet as it is
* `css/outline` — `css_outline.md`, what a project styles, in a fraction of the size
* `css/src-clean` — `css_src_clean.md`, like `code-clean`, with the strict exclusion (no minified files, no packages of other people, no generated output)
* `CSS_PROFILES` — the five profile objects in the order the listings show them
* The steps of a profile are chosen by the suffix of the file: the `PLAIN` preset for `.css`, the `LINE` preset for `.scss` and `.less`
* Imported from `simplibs.extractor_css.profiles`

#### File rules — judge the path inside the source

* `CSS_FILES`, `CSS_BASE` — stylesheets (`.css`, `.scss`, `.less`) that are not hidden; minified files and SCSS partials (`_variables.scss`) are taken, and the base rule has no switches
* `CSS_STRICT_EXCLUDE` — minified files, packages of other people, generated output and version control together; `static/` is deliberately **not** left out, because that is where a web project keeps its own styles
* Atomic pieces: `DOT_NAME`, `MINIFIED_NAME`, `VCS_DIRS`, `DEPENDENCY_DIRS`, `OUTPUT_DIRS`
* Imported from `simplibs.extractor_css.file_rules`

#### Constants and the add-on

* Suffixes: `CSS_SUFFIXES`, `CSS_PLAIN_SUFFIXES`, `CSS_LINE_COMMENT_SUFFIXES`, `CSS_EXTRA_LANGUAGE_BY_SUFFIX`
* Names: `CSS_DEPENDENCY_DIR_NAMES`, `CSS_OUTPUT_DIR_NAMES`, `CSS_MINIFIED_ENDING`
* Licence marks: `CSS_LICENSE_START`, `CSS_LICENSE_TAGS`
* Patterns of the scanner: `CSS_TOKEN_PATTERN`, `CSS_LINE_TOKEN_PATTERN`, `CSS_BLOCK_MARKS_PATTERN`, `CSS_IMPORT_PATTERN`
* `register_all(*, replace_existing=True)` — registers the code-fence languages of `.scss` and `.less` and the five profiles; the target of the entry point `simplibs.extractor.plugins`, so `pip install` is the whole installation

#### Exceptions

* The library defines no exceptions of its own, and **a stylesheet is never the cause of an error**: a file that looks damaged is a warning, not an exception. A step returns the text as it got it and warns; the extractor reports the file as `partial`, and the file stays in the output
* A text that is not a `str`, or a `max_depth` that is not a positive number, is refused by `@validate_call` with its `ValidationError`
* `register_all(replace_existing=False)` raises the cards of the extractor's registry when a profile key or a language suffix is already taken

#### Typing

* `py.typed` marker — the package ships its type information

#### Package Layout

* `simplibs.extractor_css` exports the four steps and `register_all`; the actions, presets, profiles and file rules are imported from their own folders (`actions`, `presets`, `profiles`, `file_rules`), each of which declares its own `__all__`, and the constants from `constants`
* Layers that only look left: `constants` ← `file_rules` ← `logic` ← `actions` ← `presets` ← `profiles` ← `plugin`
* The scanner and the parts it is made of are private (`logic/_helpers/`)
* The add-on uses `simplibs.extractor` only through its public names (`Profile`, `register_profile`, `register_language`, `by_suffix`)
* Importing the package registers nothing; the extractor calls `register_all` through the entry point

#### Dependencies

* `simplibs-extractor>=0.2.0` — `Profile`, `register_profile`, `register_language` and `by_suffix`, and the file status `partial`; all of them first appear in 0.2.0
* `simplibs-text` — `remove_spans`, `Span`, `CLEANUP_WHITESPACE` and `COMPACT`
* `simplibs-actions` — `create_action`: the steps as pipeline actions
* `simplibs-path` — `IGNORE_VCS` and the path rules (`HasSuffix`, `NameIs`, `StemIs`, `AnyParentNameIs`)
* `simplibs-rules` — `Rule`, `IsIn`, `StartsWith` and `EndsWith`
* `simplibs-validate` — `@validate_call` on every public function
* `simplibs-types` — `int_positive`, the depth of the outline

### 📚 Documentation

* Main `README.md` with a quick start in four levels, the package structure, a quick reference of every layer, the table of what is an exception and what is not, and an index of the detailed references
* Detailed references in `docs/`: `README_EXTRACTOR_CSS_ACTIONS`, `_CONSTANTS`, `_FILE_RULES`, `_PLUGIN`, `_PRESETS`, `_PROFILES`, and under `docs/logic/` `README_EXTRACTOR_CSS_LOGIC`

---

## Legend

* 🔄 **Changed** — modifications to existing functionality
* ✨ **Added** — new features and components
* 🐛 **Fixed** — bug fixes
* 📋 **Improved** — enhancements to existing features
* ⚠️ **Deprecated** — deprecated functionality (not used yet in this project)
* 🗑️ **Removed** — removed functionality (not used yet in this project)
