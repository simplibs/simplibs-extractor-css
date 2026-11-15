from typing import Final
from simplibs.extractor import Profile
# Outers
from ..file_rules import CSS_BASE
from ..presets import CSS_LINE_NO_IMPORTS, CSS_PLAIN_NO_IMPORTS
# Inners
from .steps_for_css import steps_for_css


CSS_CODE_NO_IMPORTS: Final[Profile] = Profile(
    system="css",
    name="code-no-imports",
    description="Pure rules: no imports, comments or blank lines",
    include=CSS_BASE,
    steps=steps_for_css(CSS_PLAIN_NO_IMPORTS, CSS_LINE_NO_IMPORTS),
    output_name="css_code_no_imports.md",
)
"""The profile `css/code-no-imports`."""


_DESIGN_NOTES = """
# CSS_CODE_NO_IMPORTS — `css/code-no-imports`

## Purpose
The stylesheets reduced to what they style: no `@import`, `@use` or
`@forward`, no comments, no blank lines.

## Output
`css_code_no_imports.md`.
"""
