from typing import Final


CSS_DEPENDENCY_DIR_NAMES: Final[tuple[str, ...]] = ("node_modules", "bower_components", "vendor")
"""Names of folders that hold stylesheets written by other people."""


_DESIGN_NOTES = """
# CSS_DEPENDENCY_DIR_NAMES — Other People's Stylesheets

## Purpose
The names behind `DEPENDENCY_DIRS`. A framework copied into the project
(`static/vendor/bootstrap/`) or installed by a package manager is thousands
of lines that are not the project's own.

## `vendor`
In a Django project the third-party stylesheets usually live in
`static/vendor/`, so the name is worth more here than it would be in a
language whose `vendor` folder holds only code.

## Own List
Each add-on decides for its own language what counts as dependencies; the
library does not borrow the list of the JavaScript add-on.
"""
