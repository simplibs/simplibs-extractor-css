def line_of(text: str, offset: int) -> int:
    """Say on which line an offset lies.

    Args:
        text: The source.
        offset: A position in it.

    Returns:
        The line number, counted from 1.
    """

    # 1. One more than the number of line breaks in front of the offset
    return text.count("\n", 0, offset) + 1


_DESIGN_NOTES = """
# line_of — Where Was That

## Purpose
A warning that says "a string is not closed" is useless without the line.
The count is made only when there is a problem to report, so a healthy file
never pays for it.
"""
