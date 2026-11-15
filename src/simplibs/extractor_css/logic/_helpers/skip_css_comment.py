def skip_css_comment(text: str, start: int) -> tuple[int, bool]:
    """Find where a block comment ends.

    Args:
        text: The source.
        start: The offset of the opening `/*`.

    Returns:
        The offset just after the `*/` and `True`; for a comment that is never closed, the end of
        the text and `False`.
    """

    # 1. The search starts behind the `/*`, so `/*/` does not close itself
    close = text.find("*/", start + 2)
    if close == -1:
        return len(text), False

    return close + 2, True


_DESIGN_NOTES = """
# skip_css_comment — A Comment Ends at `*/`

## Purpose
The one rule of a CSS block comment: it ends at the first `*/`. There are no
nested comments and no escapes.

## An Unclosed Comment
By the specification, and so for every browser, it runs to the end of the
file. The scanner does the same and reports it: a stylesheet cut in half is
usually a damaged file, and the reader should hear about it.
"""
