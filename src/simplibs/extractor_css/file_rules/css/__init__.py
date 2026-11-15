from .CSS_BASE import CSS_BASE
from .CSS_FILES import CSS_FILES
from .CSS_STRICT_EXCLUDE import CSS_STRICT_EXCLUDE


_DESIGN_NOTES = """
# css — File Rules for Stylesheets

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component            | Type | Description                                                         |
| :------------------- | :--- | :------------------------------------------------------------------ |
| `CSS_BASE`           | Rule | The default choice of stylesheets: every one that is not hidden.    |
| `CSS_FILES`          | Rule | Files with a stylesheet suffix.                                     |
| `CSS_STRICT_EXCLUDE` | Rule | Minified files, other people's packages, generated output, VCS.     |
"""
