from typing import Final
from simplibs.text.presets import COMPACT
# Outers
from ..actions import RemoveCssImports, StripCssComments


CSS_PLAIN_NO_IMPORTS: Final = (
    StripCssComments()
    >> RemoveCssImports()
    >> COMPACT
)
"""Plain CSS reduced to its rules: no comments, no imports, no blank lines."""


_DESIGN_NOTES = """
# CSS_PLAIN_NO_IMPORTS — The Rules and Nothing Else

## Purpose
The steps of `css/code-no-imports` for `.css`.

## Order
Comments go first: an import followed by a comment on the same line is only
a whole line once the comment is gone.
"""
