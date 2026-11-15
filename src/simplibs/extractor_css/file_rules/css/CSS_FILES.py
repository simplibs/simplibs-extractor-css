from typing import Final
from simplibs.path.rules import HasSuffix
from simplibs.rules import Rule
# Outers
from ...constants import CSS_SUFFIXES


CSS_FILES: Final[Rule] = HasSuffix(*CSS_SUFFIXES)
"""The file is a stylesheet (`.css .scss .less`)."""


_DESIGN_NOTES = """
# CSS_FILES — By Suffix Alone

## Purpose
The core of `CSS_BASE`. HasSuffix compares case-insensitively and takes
several suffixes at once.

## Preprocessor Files
SCSS and Less files are stylesheets in every sense that matters to a reader,
so they are taken together with plain CSS. Which steps they get is decided by
the profiles, per suffix.
"""
