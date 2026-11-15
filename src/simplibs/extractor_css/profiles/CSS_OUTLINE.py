from typing import Final
from simplibs.extractor import Profile
# Outers
from ..file_rules import CSS_BASE
from ..presets import CSS_LINE_OUTLINE, CSS_PLAIN_OUTLINE
# Inners
from .steps_for_css import steps_for_css


CSS_OUTLINE: Final[Profile] = Profile(
    system="css",
    name="outline",
    description="Overview of the stylesheets: selectors and at-rules without declarations",
    include=CSS_BASE,
    steps=steps_for_css(CSS_PLAIN_OUTLINE, CSS_LINE_OUTLINE),
    output_name="css_outline.md",
)
"""The profile `css/outline`."""


_DESIGN_NOTES = """
# CSS_OUTLINE — `css/outline`

## Purpose
What a project styles, in a fraction of the size. For a reader with a limited
window the list of selectors is most of what is needed to ask the right
questions.

## Output
`css_outline.md`; each file is a list of headers, one per line, indented by
the depth of its block. A file with no block gives an empty section.
"""
