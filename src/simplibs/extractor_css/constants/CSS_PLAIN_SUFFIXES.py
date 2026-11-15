from typing import Final


CSS_PLAIN_SUFFIXES: Final[tuple[str, ...]] = (".css",)
"""The suffixes of plain CSS files, where only `/* ... */` is a comment."""


_DESIGN_NOTES = """
# CSS_PLAIN_SUFFIXES — Where `//` Is Not a Comment

## Purpose
The profiles choose the steps of a file by its suffix (the extractor gives a
step the text only, never the path). A plain `.css` file is read with block
comments only: in CSS the characters `//` have no meaning of their own, so
the scanner must never cut them away.

## The Other Half
The preprocessor suffixes, where `//` does start a comment, are in
`CSS_LINE_COMMENT_SUFFIXES`.
"""
