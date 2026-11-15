from typing import Final
from simplibs.rules import Rule
# Outers
from ..atomic import DOT_NAME
# Inners
from .CSS_FILES import CSS_FILES


CSS_BASE: Final[Rule] = CSS_FILES & ~DOT_NAME
"""The default rule for stylesheets worth reading: every stylesheet that is not hidden."""


_DESIGN_NOTES = """
# CSS_BASE — The Default Choice of Stylesheets

## Purpose
Every CSS profile of this library uses it as `include`.

## No Switches
The JavaScript base rule has switches for `index.*` and `_*` files, because
the old code dropped both and a project may need them back. Here nothing
needs a switch: an SCSS partial such as `_variables.scss` is a perfectly
ordinary source file and is always taken.

## Minified Files
They are taken too: a profile that gives "every file as it is" must not
decide what a reader may see. The strict exclusion is the place that
leaves them out.
"""
