from simplibs.types import int_positive
from simplibs.validate import validate_call
# Inners
from ._helpers import build_outline, scan_checked, warn_problems


@validate_call
def css_outline(text: str, *, line_comments: bool = False, max_depth: int_positive | None = None) -> str:
    """Write an overview of a stylesheet: the headers of its blocks, without the declarations.

    Args:
        text: The source.
        line_comments: Also read `// ...` as a comment (SCSS and Less).
        max_depth: How many levels of nesting to list (`1` is the top level only); `None` lists all.

    Returns:
        One line for each selector or at-rule that opens a block, indented by two spaces for each
        level; an empty string for a file with no block. A file that looks damaged (a comment or a
        string that is never closed, braces that do not pair up) comes back unchanged, with a warning.

    Example:
        css_outline("@media print { .a, .b { color: red; } }")
        # '@media print\\n  .a, .b\\n'
    """

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


_DESIGN_NOTES = """
# css_outline — The Shape of a Stylesheet in a Few Lines

## Purpose
The step of the profile `css/outline`: what a stylesheet styles, without how
it does it. For handing a large project to a reader with a limited window,
the list of selectors is most of what is needed to ask the right questions.

## What Is Listed
Every block header: selectors, `@media`, `@supports`, `@keyframes`,
`@font-face`, `@layer`, and for the preprocessors `@mixin`, `@function` and
the like. Declarations and at-rules without a block (`@charset`, `@import`,
`@include x;`) are not listed.

## Written From the Text
The headers are the text of the stylesheet with comments removed and blanks
collapsed; nothing is rewritten, so `.a:not(.b) > .c` stays as it was.

## A Damaged File
The whole text is returned, as `python_outline` does for a source it cannot
parse, so the reader sees the file and the report says why it is not an
outline.
"""
