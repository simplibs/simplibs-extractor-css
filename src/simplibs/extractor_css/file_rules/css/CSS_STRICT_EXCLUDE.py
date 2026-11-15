from typing import Final
from simplibs.rules import Rule
# Outers
from ..atomic import DEPENDENCY_DIRS, MINIFIED_NAME, OUTPUT_DIRS, VCS_DIRS


CSS_STRICT_EXCLUDE: Final[Rule] = MINIFIED_NAME | VCS_DIRS | DEPENDENCY_DIRS | OUTPUT_DIRS
"""Everything that is a stylesheet but not the project's own source: minified files, packages of other people, generated output, version control."""


_DESIGN_NOTES = """
# CSS_STRICT_EXCLUDE — Only the Project's Own Stylesheets

## Purpose
The `exclude` of the profile `css/src-clean`.

## What Is Not Excluded
There are no tests, no configuration files and no asset folders in this
rule: a stylesheet is not tested, no tool keeps its settings in one, and
`static/` is where a Django project keeps its own styles.
"""
