from .atomic import (
    DEPENDENCY_DIRS,
    DOT_NAME,
    MINIFIED_NAME,
    OUTPUT_DIRS,
    VCS_DIRS,
)
from .css import (
    CSS_BASE,
    CSS_FILES,
    CSS_STRICT_EXCLUDE,
)


__all__ = [
    # atomic
    "DEPENDENCY_DIRS",
    "DOT_NAME",
    "MINIFIED_NAME",
    "OUTPUT_DIRS",
    "VCS_DIRS",
    # css
    "CSS_BASE",
    "CSS_FILES",
    "CSS_STRICT_EXCLUDE",
]


_DESIGN_NOTES = """
# simplibs.extractor_css.file_rules — Which Files Are Worth Reading

## Purpose
Rules on the path of a file, relative to the source folder. The profiles use
them as `include` and `exclude`; they compose with `&`, `|` and `~`, so a
program can build its own selection from them:

    from simplibs.extractor_css.file_rules import CSS_BASE, MINIFIED_NAME
    only_minified = CSS_BASE & MINIFIED_NAME

## Domain Folder
`file_rules/` has its own `__all__` and is not re-exported from the package root.

## Internal Components Registry

| Component | Type    | Description                                                      |
| :-------- | :------ | :--------------------------------------------------------------- |
| `atomic`  | Package | The shared pieces: dot names, minified names, the folder rules.  |
| `css`     | Package | Rules for stylesheets.                                           |

## Layering & Design
- `atomic` ← `css`.
- Every rule is built once, when the package is imported.
- A rule about the folders above a file is `AnyParentNameIs` of `simplibs-path`; a set of names is `IsIn` of `simplibs-rules`.
"""
