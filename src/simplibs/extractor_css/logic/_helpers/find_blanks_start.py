def find_blanks_start(text: str, position: int) -> int:
    """Move back over the spaces and tabs in front of a position.

    Args:
        text: The source.
        position: Where a comment starts.

    Returns:
        The offset of the first blank of the run that ends at `position`, or `position` itself.
    """

    # 1. Spaces and tabs only: a line break is never swallowed
    while position > 0 and text[position - 1] in " \t":
        position -= 1

    return position


_DESIGN_NOTES = """
# find_blanks_start — The Blanks Go With the Comment

## Purpose
`a: b; /* note */` should become `a: b;`, not `a: b; `. The blanks in front
of a comment belong to it, so the cut takes them along.

## Only Spaces and Tabs
The line break in front of a comment is not touched: removing it would pull
the next line up.
"""
