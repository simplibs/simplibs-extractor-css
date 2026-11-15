from typing import Final


CSS_LINE_COMMENT_SUFFIXES: Final[tuple[str, ...]] = (".scss", ".less")
"""The suffixes of the CSS preprocessors that allow `// ...` comments next to `/* ... */`."""


_DESIGN_NOTES = """
# CSS_LINE_COMMENT_SUFFIXES — SCSS and Less

## Purpose
SCSS and Less add one thing the comment scanner has to know about: a comment
that runs from `//` to the end of the line. The profiles give these suffixes
the steps with `line_comments` switched on.

## Why `.sass` Is Not Here
The indented syntax of Sass has no braces: its structure is the indentation.
Comments would still work, but the outline of selectors could not be read the
same way, so the suffix stays out until it has a scanner of its own.
"""
