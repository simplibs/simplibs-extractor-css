from typing import Final
from simplibs.extractor import Profile
# Outers
from ..file_rules import CSS_BASE
from ..presets import CSS_LINE_CLEAN, CSS_PLAIN_CLEAN
# Inners
from .steps_for_css import steps_for_css


CSS_CODE_CLEAN: Final[Profile] = Profile(
    system="css",
    name="code-clean",
    description="Stylesheets without comments and extra blank lines (imports stay)",
    include=CSS_BASE,
    steps=steps_for_css(CSS_PLAIN_CLEAN, CSS_LINE_CLEAN),
    output_name="css_code_clean.md",
)
"""The profile `css/code-clean`."""


_DESIGN_NOTES = """
# CSS_CODE_CLEAN — `css/code-clean`

## Purpose
Every stylesheet of the project with the comments taken out, as it is
otherwise: the everyday way to give a stylesheet to a reader.

## Output
`css_code_clean.md`. `.css` gets the step for plain CSS, `.scss` and `.less`
the step that also knows `//`.
"""
