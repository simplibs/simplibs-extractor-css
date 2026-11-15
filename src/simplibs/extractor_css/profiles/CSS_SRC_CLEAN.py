from typing import Final
from simplibs.extractor import Profile
# Outers
from ..file_rules import CSS_BASE, CSS_STRICT_EXCLUDE
from ..presets import CSS_LINE_CLEAN, CSS_PLAIN_CLEAN
# Inners
from .steps_for_css import steps_for_css


CSS_SRC_CLEAN: Final[Profile] = Profile(
    system="css",
    name="src-clean",
    description="Like code-clean, without minified files, packages of other people and generated output",
    include=CSS_BASE,
    exclude=CSS_STRICT_EXCLUDE,
    steps=steps_for_css(CSS_PLAIN_CLEAN, CSS_LINE_CLEAN),
    output_name="css_src_clean.md",
)
"""The profile `css/src-clean`."""


_DESIGN_NOTES = """
# CSS_SRC_CLEAN — `css/src-clean`

## Purpose
Only the project's own stylesheets, cleaned: no `*.min.css`, no
`node_modules` or `vendor`, no `dist`, `staticfiles` or coverage reports.

## Output
`css_src_clean.md`.
"""
