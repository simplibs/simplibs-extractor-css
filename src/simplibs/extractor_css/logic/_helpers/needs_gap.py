def needs_gap(before: str, after: str) -> bool:
    """Say whether two characters would grow into one token if a comment between them disappeared.

    Args:
        before: The character in front of the comment.
        after: The character behind it.

    Returns:
        `True` if a space has to be left where the comment was.
    """

    # 1. Two name characters become one name
    if _is_name_character(before) and _is_name_character(after):
        return True

    # 2. A digit and a dot become one number
    return (before.isdigit() and after == ".") or (before == "." and after.isdigit())


def _is_name_character(character: str) -> bool:
    """A letter, a digit, an underscore or a hyphen: what a CSS name is made of."""

    # 1. `isalnum` also knows the letters of every alphabet
    return character.isalnum() or character in "_-"


_DESIGN_NOTES = """
# needs_gap — A Comment Is a Border Between Two Tokens

## Purpose
In CSS a comment separates tokens: `0/**/auto` is two values. Cut out without
a trace it becomes `0auto`, which is one broken one. A space is needed only
where the two sides would really merge.

## Only Where They Merge
A comment between a brace and a name, a colon and a name, or next to a blank
needs nothing, so the output does not fill with spaces that were never there.
`a/**/.b` stays `a.b`: CSS reads the comment as no token at all, so the
selector means the same with or without it, and a space would change it.
"""
