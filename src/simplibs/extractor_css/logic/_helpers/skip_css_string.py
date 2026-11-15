def skip_css_string(text: str, start: int) -> tuple[int, bool]:
    """Find where a quoted string ends.

    Args:
        text: The source.
        start: The offset of the opening quote (`'` or `"`).

    Returns:
        The offset just after the closing quote and `True`; for a string that is not closed, the end
        of its line (or of the text) and `False`.
    """

    # 1. Walk to the matching quote; a backslash takes the next character with it
    quote = text[start]
    position = start + 1
    length = len(text)
    while position < length:
        character = text[position]
        if character == "\\":
            position += 2
        elif character == quote:
            return position + 1, True
        elif character == "\n":
            return position, False
        else:
            position += 1

    return length, False


_DESIGN_NOTES = """
# skip_css_string — A String Ends at Its Quote or at Its Line

## Purpose
A `/*` or `//` inside a string is text, not a comment
(`content: "/* not a comment */"`). The scanner skips the whole string.

## An Unclosed String
In CSS a line break that is not escaped ends a string that has no closing
quote. The scanner does the same, so the damage stays on that one line, and it
reports the line.

## Escapes
A backslash takes the next character, so `"a\\"b"` is one string and a
backslash at the end of a line continues the string on the next one.
"""
