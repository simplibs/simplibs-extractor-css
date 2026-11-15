from typing import Final
from simplibs.extractor import Profile
# Outers
from ..file_rules import CSS_BASE


CSS_DATA_ALL: Final[Profile] = Profile(
    system="css",
    name="data-all",
    description="Every relevant stylesheet, as it is",
    include=CSS_BASE,
    output_name="css_data_all.md",
)
"""The profile `css/data-all`."""


_DESIGN_NOTES = """
# CSS_DATA_ALL — `css/data-all`

## Purpose
The files selected by `CSS_BASE`, untouched: comments, imports and minified
files included.

## Output
`css_data_all.md`.
"""
