from simplibs.text import remove_spans
from simplibs.validate import validate_call
# Inners
from ._helpers import find_import_spans, scan_checked


@validate_call
def remove_css_imports(text: str, *, line_comments: bool = False) -> str:
    """Remove the statements that pull in other stylesheets: `@import`, `@use` and `@forward`.

    Args:
        text: The source.
        line_comments: Also read `// ...` as a comment (SCSS and Less), so an `@import` in one is left alone.

    Returns:
        The text without those statements; the lines they stood on disappear. A file that looks damaged
        (a comment or a string that is never closed) comes back unchanged, with a warning.
    """

    # 1. Read the file; a damaged one is left as it is
    scan = scan_checked(text, line_comments=line_comments)
    if scan is None:
        return text

    # 2. Each statement that begins a line in code is a range; cut them
    return remove_spans(text, find_import_spans(text, scan))


_DESIGN_NOTES = """
# remove_css_imports — The Logic Without Its Dependencies

## Purpose
A step of the profile `css/code-no-imports`: what a stylesheet needs from
other files is the part of its text that says least about the stylesheet
itself.

## `@use` and `@forward`
They are the module statements of SCSS and mean the same as an import:
"this file needs that one". A profile without imports leaves them out too,
and there is no option for the difference: nobody asks for `@import` to go
and `@use` to stay.

## By the Scan, Not by a Line Pattern
Where a statement begins is found by a pattern; where it ends is found
by walking to the first semicolon that is not inside a string or an address.
That is why `@import url("a;b.css");` is one statement, and why an import
inside a comment is never cut.

## Needs No Order
Comments are known to the scan, so the step gives the same result before or
after `strip_css_comments`.
"""
