from simplibs.text import Span
# Inners
from .find_blanks_start import find_blanks_start
from .needs_gap import needs_gap


def fit_comment_span(text: str, start: int, end: int) -> tuple[Span, bool]:
    """Decide what to cut for a block comment, and whether a space must stay behind.

    Args:
        text: The source.
        start: The offset of the `/*`.
        end: The offset just after the `*/` (or the end of the text).

    Returns:
        The span to cut, and whether it is glued (a space has to be left in its place).
    """

    # 1. What stands next to the comment; the edges of the text count as line breaks
    before = text[start - 1] if start > 0 else "\n"
    after = text[end] if end < len(text) else "\n"

    # 2. A comment followed by a blank or a line break takes the blanks in front of it along
    if after in " \t\r\n":
        return (find_blanks_start(text, start), end), False

    # 3. Otherwise only the comment goes, and a space stays if the neighbours would merge
    return (start, end), needs_gap(before, after)


_DESIGN_NOTES = """
# fit_comment_span — The Cut of One Block Comment

## Purpose
Three cases, one function: a comment at the end of a line (the blanks in
front of it go too), a comment between two tokens (a space stays) and a
comment next to a brace or a colon (nothing needs to stay).

## Why the Blanks Only in the First Case
Taking the blanks in front of `/* c */b` would glue `a` and `b` in
`a /* c */b`. The blanks are taken only when something blank follows, so the
text on the line keeps exactly one separation.
"""
