from typing import Final
from simplibs.path.rules import AnyParentNameIs
from simplibs.rules import IsIn, Rule
# Outers
from ...constants import CSS_DEPENDENCY_DIR_NAMES


DEPENDENCY_DIRS: Final[Rule] = AnyParentNameIs(IsIn(CSS_DEPENDENCY_DIR_NAMES))
"""The file lies inside a folder of stylesheets written by other people (`node_modules`, `vendor`)."""


_DESIGN_NOTES = """
# DEPENDENCY_DIRS — Other People's Stylesheets

## Purpose
Part of the strict CSS exclusion. See `CSS_DEPENDENCY_DIR_NAMES`.
"""
