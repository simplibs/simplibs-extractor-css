from simplibs.validate import validate_call
# Inners
from ._helpers import find_comments, remove_with_gaps


@validate_call
def strip_css_comments(text: str, *, line_comments: bool = False, keep_license: bool = False) -> str:
    """Remove the comments of a stylesheet.

    Args:
        text: The source.
        line_comments: Also remove `// ...` comments (SCSS and Less).
        keep_license: Keep the comments that tools keep (`/*! ... */`, `@license`, `@preserve`).

    Returns:
        The text without comments. A line that held only a comment disappears, and a comment between
        two tokens leaves a space (`0/**/auto` is `0 auto`). A file that looks damaged (a comment or
        a string that is never closed) comes back unchanged, with a warning.
    """

    # 1. Which comments go, and which of them must leave a space
    comments, glued = find_comments(text, line_comments=line_comments, keep_license=keep_license)

    # 2. Cut them
    return remove_with_gaps(text, comments, glued)


_DESIGN_NOTES = """
# strip_css_comments — The Comments Out, The Strings Untouched

## Purpose
A step of the profiles `css/code-clean`, `css/code-no-imports` and
`css/src-clean`.

## Options
`line_comments` is for SCSS and Less: the profiles give those suffixes a step
with it on, and a plain `.css` file a step with it off, because the step sees
only the text and cannot tell them apart itself. `keep_license` is off by
default, so the default result has no comments at all.

## A Damaged File
It is returned as it is, and the warning makes the extractor call the file
`partial`. The step never cuts on a basis it does not trust.

## Idempotent
A second run finds nothing and returns the very same text.

## Known Limits
See `scan_css`: SCSS interpolation with an unclosed quote makes the file look
damaged.
"""
