from typing import Final
# Outers
from ..actions import CssOutline


CSS_PLAIN_OUTLINE: Final = CssOutline()
"""The list of selectors and at-rules of a plain CSS file."""


_DESIGN_NOTES = """
# CSS_PLAIN_OUTLINE — What a `.css` File Styles

## Purpose
The step of `css/outline` for `.css`. It is a single action, and it is a
preset all the same: the profile picks its steps by the kind of file, and
each kind has one name.
"""
