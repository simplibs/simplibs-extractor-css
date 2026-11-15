from typing import Final
from simplibs.text.presets import COMPACT
# Outers
from ..actions import RemoveCssImports, StripCssComments


CSS_LINE_NO_IMPORTS: Final = (
    StripCssComments(line_comments=True)
    >> RemoveCssImports(line_comments=True)
    >> COMPACT
)
"""SCSS and Less reduced to their rules: no comments, no imports (`@use` and `@forward` included), no blank lines."""


_DESIGN_NOTES = """
# CSS_LINE_NO_IMPORTS — The Rules and Nothing Else, for Preprocessors

## Purpose
The steps of `css/code-no-imports` for `.scss` and `.less`.

## Both Steps Know `//`
The import step needs `line_comments` too: without it a `// @import "x";`
would look like a statement that has been left in the code.
"""
