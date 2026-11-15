from typing import Final
from simplibs.path.rules import AnyParentNameIs
from simplibs.rules import IsIn, Rule
# Outers
from ...constants import CSS_OUTPUT_DIR_NAMES


OUTPUT_DIRS: Final[Rule] = AnyParentNameIs(IsIn(CSS_OUTPUT_DIR_NAMES))
"""The file lies inside a folder of generated files (`dist`, `staticfiles`, `coverage`...)."""


_DESIGN_NOTES = """
# OUTPUT_DIRS — Generated Files

## Purpose
Part of the strict CSS exclusion. See `CSS_OUTPUT_DIR_NAMES`.
"""
