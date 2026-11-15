from typing import Final
from simplibs.extractor import Profile
# Inners
from .CSS_CODE_CLEAN import CSS_CODE_CLEAN
from .CSS_CODE_NO_IMPORTS import CSS_CODE_NO_IMPORTS
from .CSS_DATA_ALL import CSS_DATA_ALL
from .CSS_OUTLINE import CSS_OUTLINE
from .CSS_SRC_CLEAN import CSS_SRC_CLEAN


CSS_PROFILES: Final[tuple[Profile, ...]] = (
    CSS_CODE_CLEAN,
    CSS_CODE_NO_IMPORTS,
    CSS_DATA_ALL,
    CSS_OUTLINE,
    CSS_SRC_CLEAN,
)
"""The profiles of the system `css`."""


_DESIGN_NOTES = """
# CSS_PROFILES — The `css` System

## Purpose
The profiles of one system in the order the listing commands show them.
"""
