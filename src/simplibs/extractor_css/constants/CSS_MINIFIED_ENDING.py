from typing import Final


CSS_MINIFIED_ENDING: Final[str] = ".min"
"""What the stem of a minified stylesheet ends with (`app.min.css`)."""


_DESIGN_NOTES = """
# CSS_MINIFIED_ENDING — A File Written for the Browser, Not for the Reader

## Purpose
Used by `MINIFIED_NAME`. A minified stylesheet is one very long line: it
costs the most tokens and says the least, and the readable file it was made
from is usually next to it.

## Only the Stem
The ending is compared with the name without its last suffix, so
`app.min.css` is minified and `administration.css` is not.
"""
