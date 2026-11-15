from typing import Final
from simplibs.text.presets import CLEANUP_WHITESPACE
# Outers
from ..actions import StripCssComments


CSS_PLAIN_CLEAN: Final = (
    StripCssComments()
    >> CLEANUP_WHITESPACE
)
"""Plain CSS without comments, whitespace tidied: imports stay."""


_DESIGN_NOTES = """
# CSS_PLAIN_CLEAN — The Everyday Clean Read of `.css`

## Purpose
The steps of `css/code-clean` and `css/src-clean` for the suffixes in
`CSS_PLAIN_SUFFIXES`, built once.

## Plain
In plain CSS only `/* ... */` is a comment, so the step has `line_comments` off.
"""
