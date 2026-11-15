from typing import Final
from simplibs.text.presets import CLEANUP_WHITESPACE
# Outers
from ..actions import StripCssComments


CSS_LINE_CLEAN: Final = (
    StripCssComments(line_comments=True)
    >> CLEANUP_WHITESPACE
)
"""SCSS and Less without comments (`//` included), whitespace tidied: imports stay."""


_DESIGN_NOTES = """
# CSS_LINE_CLEAN — The Everyday Clean Read of `.scss` and `.less`

## Purpose
The same as `CSS_PLAIN_CLEAN` for the suffixes in `CSS_LINE_COMMENT_SUFFIXES`,
where `// ...` is a comment too.
"""
