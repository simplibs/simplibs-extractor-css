from typing import Final
# Inners
from .CSS_LINE_COMMENT_SUFFIXES import CSS_LINE_COMMENT_SUFFIXES
from .CSS_PLAIN_SUFFIXES import CSS_PLAIN_SUFFIXES


CSS_SUFFIXES: Final[tuple[str, ...]] = CSS_PLAIN_SUFFIXES + CSS_LINE_COMMENT_SUFFIXES
"""The suffixes of every stylesheet this library reads: `.css`, `.scss`, `.less`."""


_DESIGN_NOTES = """
# CSS_SUFFIXES — What Counts as a Stylesheet

## Purpose
The file rules choose files by these suffixes. The profiles do not use the
whole tuple for their steps: they give `CSS_PLAIN_SUFFIXES` and
`CSS_LINE_COMMENT_SUFFIXES` their own step each.

## Built From the Two Halves
The tuple is made of the two smaller ones, so a suffix added to either of
them is a stylesheet at once and nobody has to remember a third place.
"""
