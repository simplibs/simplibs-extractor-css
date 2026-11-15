from typing import Final
from simplibs.path.rules import StemIs
from simplibs.rules import EndsWith, Rule
# Outers
from ...constants import CSS_MINIFIED_ENDING


MINIFIED_NAME: Final[Rule] = StemIs(EndsWith(CSS_MINIFIED_ENDING))
"""The file is a minified stylesheet: its name is `something.min` plus a suffix (`app.min.css`)."""


_DESIGN_NOTES = """
# MINIFIED_NAME — The Compressed Twin

## Purpose
Part of the strict CSS exclusion. See `CSS_MINIFIED_ENDING`.

## Why `StemIs`
`StemIs` judges the name without its last suffix, so the check is exactly
"the part before `.css` ends with `.min`" and a name such as `admin.css` can
never be taken for a minified one.
"""
