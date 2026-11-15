from typing import Final
# Outers
from ..actions import CssOutline


CSS_LINE_OUTLINE: Final = CssOutline(line_comments=True)
"""The list of selectors and at-rules of an SCSS or Less file."""


_DESIGN_NOTES = """
# CSS_LINE_OUTLINE — What an `.scss` or `.less` File Styles

## Purpose
The step of `css/outline` for `.scss` and `.less`, where a brace inside a
`// ...` comment is not a block.
"""
