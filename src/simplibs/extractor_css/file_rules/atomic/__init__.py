from .DEPENDENCY_DIRS import DEPENDENCY_DIRS
from .DOT_NAME import DOT_NAME
from .MINIFIED_NAME import MINIFIED_NAME
from .OUTPUT_DIRS import OUTPUT_DIRS
from .VCS_DIRS import VCS_DIRS


_DESIGN_NOTES = """
# atomic — The Shared Pieces of the File Rules

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component         | Type | Description                                                  |
| :---------------- | :--- | :----------------------------------------------------------- |
| `DEPENDENCY_DIRS` | Rule | A folder above the file holds stylesheets of other people.   |
| `DOT_NAME`        | Rule | The name starts with a dot.                                  |
| `MINIFIED_NAME`   | Rule | The name is `something.min` plus a suffix.                   |
| `OUTPUT_DIRS`     | Rule | A folder above the file holds generated files.               |
| `VCS_DIRS`        | Rule | A folder above the file is a version-control folder.         |

## Layering & Design
- Every piece is one rule of one idea; the `css` folder only combines them.
- The rules about folders use `AnyParentNameIs` of `simplibs-path` and `IsIn` of `simplibs-rules`.
"""
