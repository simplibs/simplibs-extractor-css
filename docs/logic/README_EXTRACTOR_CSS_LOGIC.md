# 🔧 `extractor_css/logic` — The Steps That Read Stylesheets

The `logic` package holds **the steps**: plain functions that read a stylesheet — CSS, SCSS or Less — and take something out of it or reduce it to an overview. Four of them: the
comments, the imports, the outline, and the positions of the comments.

```python
from simplibs.extractor_css import strip_css_comments, css_outline

strip_css_comments("a { b: c; } /* note */\n")                # -> 'a { b: c; }\n'
css_outline("@media print { .a, .b { color: red; } }")        # -> '@media print\n  .a, .b\n'
```

Every function takes the **text first** and returns a **new text** (`css_comment_spans` returns the positions instead). Every one is checked by `@validate_call`, takes its options
as keyword-only parameters, and **never raises on a stylesheet**: a file that looks damaged comes back unchanged, with a warning (see [the note below](#a-note-on-a-damaged-file)).
The functions are exported from the package root; the [actions](../README_EXTRACTOR_CSS_ACTIONS.md) that wrap them are a domain of their own.

| You want to …                                              | Use                  |
|------------------------------------------------------------|----------------------|
| cut the comments out                                       | `strip_css_comments` |
| know where the comments are, without cutting them          | `css_comment_spans`  |
| take out `@import`, `@use` and `@forward`                  | `remove_css_imports` |
| see what a stylesheet styles, in a few lines               | `css_outline`        |

## A note on `line_comments`

In plain CSS the characters `//` mean nothing, so they must never be cut; in SCSS and Less they start a comment that runs to the end of the line. A step is given **the text only** and
cannot tell the two apart, so it has the option `line_comments`, off by default. It is the profile that knows the suffix: it gives `.css` a step with the option off, and `.scss` and
`.less` a step with it on ([profiles](../README_EXTRACTOR_CSS_PROFILES.md)). Called on your own, you decide.

## A note on the scanner

Every step starts with the same single pass, `scan_css`. It is **a scanner, not a parser**: it builds no tree and follows only what decides where a comment begins — quotes, `url(`, `/*`
and, for the preprocessors, `//`. That is why a `/*` in `content: "/*"` or a `//` in `url(//cdn.example.com/a.css)` is never taken for a comment, and why the scanner cannot fail: there is no
syntax it refuses. It does not walk character by character either; it asks a pattern for the next stop and **jumps** there, because a stylesheet is mostly code and code holds
nothing the scanner cares about.

<details>
<summary>🔍 Under the hood — the main loop of the scanner</summary>

```python
def scan_css(text: str, *, line_comments: bool = False) -> CssScan:

    # 1. State: where the next stop is looked for, and what has been found
    pattern = CSS_LINE_TOKEN_PATTERN if line_comments else CSS_TOKEN_PATTERN
    length = len(text)
    position = 0
    comments: list[tuple[int, int]] = []
    glued: list[tuple[int, int]] = []
    literals: list[tuple[int, int]] = []
    problems: list[str] = []

    while True:

        # 2. Jump to the next place where something may begin; the code in between is not looked at
        found = pattern.search(text, position)
        if found is None:
            break
        start = found.start()
        token = found.group()

        # 3. A quoted string
        if token in ("'", '"'):
            end, closed = skip_css_string(text, start)
            literals.append((start, end))
            if not closed:
                problems.append(f"a string on line {line_of(text, start)} is not closed")
            position = end

        # 4. A block comment
        elif token == "/*":
            end, closed = skip_css_comment(text, start)
            if not closed:
                problems.append(
                    f"a comment on line {line_of(text, start)} is not closed; it runs to the end of the file"
                )
            span, is_glued = fit_comment_span(text, start, end)
            comments.append(span)
            if is_glued:
                glued.append(span)
            position = end

        # 5. A line comment (SCSS and Less only: the pattern finds it only then)
        elif token == "//":
            newline = text.find("\n", start)
            end = length if newline == -1 else newline
            comments.append((find_blanks_start(text, start), end))
            position = end

        # 6. An unquoted address behind `url(`
        else:
            end, closed = skip_css_url(text, found.end())
            if end > found.end():
                literals.append((found.end(), end))
            if not closed:
                problems.append(f"an address in url( on line {line_of(text, start)} is not closed")
            position = end

    return CssScan(tuple(comments), tuple(glued), tuple(literals), tuple(problems))
```

The result, `CssScan`, is a frozen record of four things found together: the **comments**, the **glued** comments (those that need a space left in their place), the **literals** (strings and
addresses, the places a statement cannot begin in) and the **problems**. The patterns are in [`constants`](../README_EXTRACTOR_CSS_CONSTANTS.md#patterns-of-the-scanner).

</details>

**Known limits.**

* SCSS interpolation `#{ ... }` is not understood by the scanner: a quote inside it that is not closed there makes the file look damaged.
* A `//` that follows a value in SCSS (`a: b//c`) is a comment, as the SCSS compiler reads it.
* CSS inside a `<style>` element of an HTML page is not read here: a caller that finds it passes **only that CSS** as the text.

## A note on a damaged file

The scanner never refuses a text, but it **notices** what looks wrong: a comment that is never closed (it would run to the end of the file), a string or an `url(` address that is never closed, and —
for the outline — braces that do not pair up. A step does not trust such a file. It returns **the text unchanged**, with a `UserWarning` for each place, and `css_comment_spans` returns
**no spans**. Inside an extraction the extractor collects the warnings of a file, marks it `partial` and writes the sentence into the report, while the file stays in the output.

*Why not go on.* A comment that is never closed would swallow the rest of the file, and a string that is never closed would hide a comment behind it. Cutting on such a basis loses text silently;
leaving the file alone loses nothing. `warnings.warn` is the one channel a plain function has without importing anything; called on its own, the step gives the usual Python warning, once for each place.

---

## 🧭 Table of Contents

* [`css_comment_spans`](#css_comment_spans)
* [`strip_css_comments`](#strip_css_comments)
* [`remove_css_imports`](#remove_css_imports)
* [`css_outline`](#css_outline)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logic--the-steps-that-read-stylesheets)

---

### `css_comment_spans`

Finds the comments of a stylesheet and reports **where they are**, for anything that wants to look at them or cut them in its own way.

**Parameters:**
* `text` (*str*): The source.
* `line_comments` (*bool*, keyword-only, default `False`): Also treat `// ...` as a comment (SCSS and Less).
* `keep_license` (*bool*, keyword-only, default `False`): Leave out of the answer the comments that tools keep (`/*! ... */`, `@license`, `@preserve`).

**Returns:**
* `list[Span]`: A [`Span`](https://pypi.org/project/simplibs-text/) `(start, end)` for each comment, half-open like a slice, **from the blanks in front of it to its end**. An empty list for a file that looks damaged,
  with a warning.

**Raises:**
* Nothing of its own: a wrong type of an argument is a `ValidationError` from `simplibs-validate`.

**Example usage:**
```python
from simplibs.extractor_css import css_comment_spans

css_comment_spans("a { b: c; } /* x */\n")                                    # -> [(11, 19)]     the blank in front goes with it
css_comment_spans("/*! keep */ a { b: c; } /* x */\n", keep_license=True)     # -> [(23, 31)]     the licence is not reported
css_comment_spans("a { b: c; /* open\n")                                      # -> []             damaged: a warning, no spans
```

**Every span, not only those that leave a space.** `strip_css_comments` also knows which comments need a space left behind (`0/**/auto`); this function reports every comment that is to be cut,
and nothing about spaces. It has **no action**: it returns spans, not a text, so it is not a link of a pipeline that carries text.

**Under the hood:**
```python
@validate_call
def css_comment_spans(text: str, *, line_comments: bool = False, keep_license: bool = False) -> list[Span]:

    # 1. The comments the scanner found, licences aside if they are to stay
    comments, _ = find_comments(text, line_comments=line_comments, keep_license=keep_license)

    return comments
```

`find_comments` is the one place that chooses the comments, so this function and `strip_css_comments` answer the same question the same way and differ only in what they do with the answer.

> 💡 A span that is a licence and is kept is left out **by its value**, so a glued comment that is a licence also leaves the list of comments that need a space.

[▲ Back to top](#-table-of-contents)

---

### `strip_css_comments`

Removes the comments of a stylesheet; strings and addresses are untouched.

**Parameters:**
* `text` (*str*): The source.
* `line_comments` (*bool*, keyword-only, default `False`): Also remove `// ...` comments (SCSS and Less).
* `keep_license` (*bool*, keyword-only, default `False`): Keep the comments that tools keep (`/*! ... */`, `@license`, `@preserve`).

**Returns:**
* `str`: The text without comments. A line that held only a comment disappears; a comment between two tokens leaves a space (`0/**/auto` is `0 auto`). A file that looks damaged comes
  back unchanged, with a warning.

**Raises:**
* Nothing of its own: a wrong type of an argument is a `ValidationError`.

**Example usage:**
```python
from simplibs.extractor_css import strip_css_comments

strip_css_comments("a { color: red; /* note */ }\n")                          # -> 'a { color: red; }\n'
strip_css_comments("/* header */\na { b: c; }\n")                             # -> 'a { b: c; }\n'       the line that held only a comment is gone
strip_css_comments("a { margin: 0/**/auto; }\n")                              # -> 'a { margin: 0 auto; }\n'
strip_css_comments('a::after { content: "/* kept */"; }\n')                   # -> 'a::after { content: "/* kept */"; }\n'
strip_css_comments("// note\na { b: c; } // tail\n", line_comments=True)     # -> 'a { b: c; }\n'
strip_css_comments("// note\na { b: c; }\n")                                  # -> '// note\na { b: c; }\n'     in plain CSS `//` is no comment
strip_css_comments("/*! v1 */\n/* x */\na { b: c; }\n", keep_license=True)    # -> '/*! v1 */\na { b: c; }\n'
strip_css_comments("a { b: c; /* never closed\n")                             # -> 'a { b: c; /* never closed\n'     unchanged, with a UserWarning
```

**A comment is a border between two tokens.** In CSS a comment separates tokens: `0/**/auto` is two values. Cut out without a trace it becomes `0auto`, which is one broken one. A space is left only where
the two sides would really **merge** — two name characters, or a digit and a dot. Next to a blank, a brace or a colon nothing needs to stay, so the output does not fill with spaces that were never there.
The blanks in front of a comment go with it only when something blank follows; taking them in `a /* c */b` would glue `a` and `b`.

**Idempotent.** A second run finds nothing and returns the very same text.

**Why `keep_license` is off by default.** The default result has no comments at all. The one comment a reader may not want to lose is the licence or the banner of a library, and the convention that marks
it is the one minifiers follow; a profile that wants it asks for it.

**Under the hood:**
```python
@validate_call
def strip_css_comments(text: str, *, line_comments: bool = False, keep_license: bool = False) -> str:

    # 1. Which comments go, and which of them must leave a space
    comments, glued = find_comments(text, line_comments=line_comments, keep_license=keep_license)

    # 2. Cut them
    return remove_with_gaps(text, comments, glued)
```

<details>
<summary>🔍 Under the hood — where a space stays</summary>

```python
def fit_comment_span(text: str, start: int, end: int) -> tuple[Span, bool]:

    # 1. What stands next to the comment; the edges of the text count as line breaks
    before = text[start - 1] if start > 0 else "\n"
    after = text[end] if end < len(text) else "\n"

    # 2. A comment followed by a blank or a line break takes the blanks in front of it along
    if after in " \t\r\n":
        return (find_blanks_start(text, start), end), False

    # 3. Otherwise only the comment goes, and a space stays if the neighbours would merge
    return (start, end), needs_gap(before, after)


def needs_gap(before: str, after: str) -> bool:

    # 1. Two name characters become one name
    if _is_name_character(before) and _is_name_character(after):
        return True

    # 2. A digit and a dot become one number
    return (before.isdigit() and after == ".") or (before == "." and after.isdigit())
```

`remove_with_gaps` puts the space in first and cuts the span after, so [`remove_spans`](https://pypi.org/project/simplibs-text/) of `simplibs-text` does both jobs with one primitive.

</details>

> 💡 `a/**/.b` becomes `a.b`, with no space: CSS reads the comment as no token at all, so the selector means the same with or without it, and a space would change it.

[▲ Back to top](#-table-of-contents)

---

### `remove_css_imports`

Removes the statements that pull in other stylesheets: `@import`, `@use` and `@forward`.

**Parameters:**
* `text` (*str*): The source.
* `line_comments` (*bool*, keyword-only, default `False`): Also read `// ...` as a comment (SCSS and Less), so an `@import` inside one is left alone.

**Returns:**
* `str`: The text without those statements; the lines they stood on disappear. A file that looks damaged comes back unchanged, with a warning.

**Raises:**
* Nothing of its own: a wrong type of an argument is a `ValidationError`.

**Example usage:**
```python
from simplibs.extractor_css import remove_css_imports

remove_css_imports('@import "a.css";\n@use "b";\n@forward "c";\na { c: d; }\n')       # -> 'a { c: d; }\n'
remove_css_imports('@import url("a;b.css");\na { c: d; }\n')                          # -> 'a { c: d; }\n'       the `;` in the address does not end the statement
remove_css_imports('/* @import "x"; */\na { c: d; }\n')                               # -> '/* @import "x"; */\na { c: d; }\n'     an import in a comment is not a statement
remove_css_imports('// @import "x";\n@import "y";\na { c: d; }\n', line_comments=True)   # -> '// @import "x";\na { c: d; }\n'
remove_css_imports('@import "a.css; \na { c: d; }\n')                                 # -> '@import "a.css; \na { c: d; }\n'     unchanged, with a UserWarning
```

**`@use` and `@forward` too.** They are the module statements of SCSS and mean the same as an import: *this file needs that one*. A profile without imports leaves them out as well, and there is no option for the
difference: nobody asks for `@import` to go and `@use` to stay.

**By the scan, not by a line pattern.** Where a statement **begins** is found by [`CSS_IMPORT_PATTERN`](../README_EXTRACTOR_CSS_CONSTANTS.md#patterns-of-the-scanner); where it **ends** is found by walking to the first
semicolon that is not inside a string or an address. That is why `@import url("a;b.css");` is one statement and why an import inside a comment is never cut. A statement that meets a brace before any semicolon is
not terminated (a damaged file), and then the line is taken: the cut never runs on into the rules that follow.

**It needs no order.** Comments are known to the scan, so the step gives the same result before or after `strip_css_comments`. The [presets](../README_EXTRACTOR_CSS_PRESETS.md#a-note-on-the-order-of-the-steps) put the comments
first all the same, because an import followed by a comment on the same line is a *whole line* only once the comment is gone.

**Under the hood:**
```python
@validate_call
def remove_css_imports(text: str, *, line_comments: bool = False) -> str:

    # 1. Read the file; a damaged one is left as it is
    scan = scan_checked(text, line_comments=line_comments)
    if scan is None:
        return text

    # 2. Each statement that begins a line in code is a range; cut them
    return remove_spans(text, find_import_spans(text, scan))
```

<details>
<summary>🔍 Under the hood — the ranges of the statements</summary>

```python
def find_import_spans(text: str, scan: CssScan) -> list[Span]:

    # 1. Comments are blanked, so an `@import` in a comment is never seen
    blanked = blank_spans(text, scan.comments)
    protected = Protected(scan.literals)

    # 2. Each statement that begins in code is a span from its line start to its semicolon
    spans: list[Span] = []
    for match in CSS_IMPORT_PATTERN.finditer(blanked):
        at = match.start("at")
        if protected.contains(at):
            continue
        spans.append((_statement_start(text, at), _statement_end(blanked, protected, at)))

    return spans


def _statement_end(blanked: str, protected: Protected, at: int) -> int:

    # 1. The first structural mark outside a string decides; only a semicolon ends the statement
    for mark in CSS_BLOCK_MARKS_PATTERN.finditer(blanked, at):
        if protected.contains(mark.start()):
            continue
        if mark.group() == ";":
            return mark.end()
        break

    # 2. No semicolon before a brace (or at all): the line is the statement
    newline = blanked.find("\n", at)
    return len(blanked) if newline == -1 else newline
```

</details>

> 💡 A statement that is **not the first thing on its line** (a minified file) is not found, and the name must end where the pattern ends: `@use-foo` is not `@use`.

[▲ Back to top](#-table-of-contents)

---

### `css_outline`

Writes an overview of a stylesheet: **the headers of its blocks, without the declarations** — what it styles, without how.

**Parameters:**
* `text` (*str*): The source.
* `line_comments` (*bool*, keyword-only, default `False`): Also read `// ...` as a comment (SCSS and Less).
* `max_depth` (*int_positive | None*, keyword-only, default `None`): How many levels of nesting to list (`1` is the top level only); `None` lists all. `int_positive` is a type of
  [`simplibs-types`](https://pypi.org/project/simplibs-types/): a whole number greater than zero.

**Returns:**
* `str`: One line for each selector or at-rule that opens a block, indented by **two spaces for each level**; an empty string for a file with no block. A file that looks damaged — a comment or a string that is
  never closed, braces that do not pair up — comes back **unchanged**, with a warning.

**Raises:**
* Nothing of its own: a wrong type or value of an argument (`text=5`, `max_depth=0`) is a `ValidationError`.

**Example usage:**
```python
from simplibs.extractor_css import css_outline

css_outline("@media print { .a, .b { color: red; } }")                         # -> '@media print\n  .a, .b\n'
css_outline("@media print { .a, .b { color: red; } }", max_depth=1)            # -> '@media print\n'
css_outline('@charset "utf-8";\n.a { b: c; }\n.b:not(.c) > .d { e: f; }\n')    # -> '.a\n.b:not(.c) > .d\n'          `@charset` has no block
css_outline("@keyframes spin { from { a: b; } to { a: c; } }")                 # -> '@keyframes spin\n  from\n  to\n'
css_outline(".nav {\n  // note {\n  &:hover { color: red; }\n}\n", line_comments=True)    # -> '.nav\n  &:hover\n'     a brace in a comment is no block
css_outline(".col-#{$i} { width: 1px; }\n@mixin m { a: b; }\n@include m;\n", line_comments=True)   # -> '.col-#{$i}\n@mixin m\n'
css_outline("")                                                                # -> ''
css_outline("a { b: c;\n")                                                     # -> 'a { b: c;\n'          unchanged, with a UserWarning
```

**What is listed.** Every block header: selectors, `@media`, `@supports`, `@keyframes`, `@font-face`, `@layer`, and for the preprocessors `@mixin`, `@function` and the like. **Declarations** and at-rules **without a block**
(`@charset`, `@import`, `@include x;`) are not listed.

**Written from the text.** A header is whatever stands between the last `{`, `}` or `;` and the next `{`, with comments removed and blanks collapsed. Nothing is rewritten, so `.a:not(.b) > .c` stays as it was.

**Nesting.** Plain CSS nests (`@media`, `@supports`, `@layer`, native nesting) and so do SCSS and Less; each level is indented by two spaces. Keyframe steps (`from`, `50%`) are listed under their `@keyframes`, and a smaller
`max_depth` hides them.

**Why the whole text comes back for a damaged file.** The reader then sees the file, and the report says why it is not an outline — the same choice `python_outline` of the Python add-on makes for a source it cannot parse. Braces that
do not pair up mean the nesting cannot be trusted.

**Under the hood:**
```python
@validate_call
def css_outline(text: str, *, line_comments: bool = False, max_depth: int_positive | None = None) -> str:

    # 1. Read the file; a damaged one is left as it is
    scan = scan_checked(text, line_comments=line_comments)
    if scan is None:
        return text

    # 2. The headers of the blocks
    lines, problems = build_outline(text, scan, max_depth)

    # 3. Braces that do not pair up mean the nesting cannot be trusted
    if problems:
        warn_problems(problems)
        return text

    return "\n".join(lines) + "\n" if lines else ""
```

<details>
<summary>🔍 Under the hood — the walk over the braces</summary>

```python
def build_outline(text: str, scan: CssScan, max_depth: int | None) -> tuple[list[str], list[str]]:

    # 1. Comments are blanked and strings are protected, so only real braces count
    blanked = blank_spans(text, scan.comments)
    protected = Protected(scan.literals)

    lines: list[str] = []
    depth = 0
    interpolation = 0
    stray = 0
    boundary = 0

    for mark in CSS_BLOCK_MARKS_PATTERN.finditer(blanked):
        position = mark.start()
        if protected.contains(position):
            continue
        character = mark.group()

        # 2. `#{ ... }` of SCSS is a value inside a name, not a block
        if character == "{" and position > 0 and blanked[position - 1] == "#":
            interpolation += 1
            continue
        if interpolation:
            if character == "}":
                interpolation -= 1
            continue

        # 3. A block opens: what stands since the last mark is its header
        if character == "{":
            header = " ".join(blanked[boundary:position].split())
            if header and (max_depth is None or depth < max_depth):
                lines.append("  " * depth + header)
            depth += 1

        # 4. A block closes
        elif character == "}":
            if depth:
                depth -= 1
            else:
                stray += 1

        # 5. Every mark starts a new stretch of text
        boundary = position + 1

    # 6. Braces that do not pair up
    problems: list[str] = []
    if depth:
        problems.append(f"{depth} block(s) are never closed")
    if stray:
        problems.append(f"{stray} closing brace(s) have no opening one")

    return lines, problems
```

</details>

> 💡 SCSS nested properties (`font: { family: x; }`) are listed as a block with the header `font:`.

[▲ Back to top](#-table-of-contents)

---

### Errors of this package

It raises no cards of its own, and **a stylesheet is never the cause of an error**: a file that looks damaged is a warning, not an exception. The one thing that raises is a wrong **type or value** of an
argument — `text=5`, `max_depth=0` — which is a `ValidationError` from [`simplibs-validate`](https://pypi.org/project/simplibs-validate/).

| Situation                                                           | How it is reported                                                              |
|---------------------------------------------------------------------|---------------------------------------------------------------------------------|
| A stylesheet with a comment, a string or an address never closed    | a `UserWarning` for each place; the text comes back unchanged (`css_comment_spans`: `[]`) |
| `css_outline` and braces that do not pair up                        | a `UserWarning`; the text comes back unchanged                                  |
| The same inside an extraction                                       | the file stays in the output, marked `partial`, the warning is in the report    |
| A wrong type or value of an argument                                | a `ValidationError`                                                             |

[▲ Back to top](#-table-of-contents)

---

[⬅️ Back to main README](../../README.md#-logic--the-steps-that-read-stylesheets)
