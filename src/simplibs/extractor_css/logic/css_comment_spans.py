from simplibs.text import Span
from simplibs.validate import validate_call
# Inners
from ._helpers import find_comments


@validate_call
def css_comment_spans(text: str, *, line_comments: bool = False, keep_license: bool = False) -> list[Span]:
    """Find the comments of a stylesheet.

    Args:
        text: The source.
        line_comments: Also treat `// ...` as a comment (SCSS and Less).
        keep_license: Leave out the comments that tools keep (`/*! ... */`, `@license`, `@preserve`).

    Returns:
        A span for each comment, from the blanks in front of it to its end; an empty list for a file
        that looks damaged (a comment or a string that is never closed), with a warning.
    """

    # 1. The comments the scanner found, licences aside if they are to stay
    comments, _ = find_comments(text, line_comments=line_comments, keep_license=keep_license)

    return comments


_DESIGN_NOTES = """
# css_comment_spans — Where the Comments Are

## Purpose
The spans of the comments, for anything that wants to look at them or cut them.
`strip_css_comments` also knows which of them need a space left behind; this
function reports every one that is to be cut.

## Never Raises
The scanner has no syntax it refuses: whatever the text is, it gets an answer.
A file that looks damaged is answered with no spans and a warning, so a step
that cuts them leaves the file as it is.
"""
