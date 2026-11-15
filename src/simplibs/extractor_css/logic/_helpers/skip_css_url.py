def skip_css_url(text: str, start: int) -> tuple[int, bool]:
    """Find where an unquoted `url(...)` address ends.

    Args:
        text: The source.
        start: The offset just after the `url(`.

    Returns:
        The offset just after the closing parenthesis and `True`. For an address in quotes the
        function consumes nothing (`start` and `True`): the string scanner takes it. For an address
        that is not closed, the end of its line and `False`.
    """

    # 1. Blanks are allowed between the parenthesis and the address
    position = start
    length = len(text)
    while position < length and text[position] in " \t\r\n":
        position += 1

    # 2. A quoted address is a string like any other
    if position < length and text[position] in "'\"":
        return start, True

    # 3. An unquoted one runs to the closing parenthesis; a backslash takes the next character
    while position < length:
        character = text[position]
        if character == "\\":
            position += 2
        elif character == ")":
            return position + 1, True
        elif character == "\n":
            return position, False
        else:
            position += 1

    return length, False


_DESIGN_NOTES = """
# skip_css_url — An Address Is Not Code

## Purpose
`url(data:image/png;base64,AA//BB)` and `url(//cdn.example.com/a.css)` hold
`//` and sometimes `/*`; neither starts a comment. The address is skipped as
a whole.

## Quoted Addresses
`url("a//b")` needs nothing special: the quote is found next by the scanner
and read as a string.

## An Address That Is Not Closed
Unquoted, it cannot contain a line break, so it ends at its line and is
reported.
"""
