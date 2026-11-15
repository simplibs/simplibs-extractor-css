from .CSS_CODE_CLEAN import CSS_CODE_CLEAN
from .CSS_CODE_NO_IMPORTS import CSS_CODE_NO_IMPORTS
from .CSS_DATA_ALL import CSS_DATA_ALL
from .CSS_OUTLINE import CSS_OUTLINE
from .CSS_PROFILES import CSS_PROFILES
from .CSS_SRC_CLEAN import CSS_SRC_CLEAN


__all__ = [
    "CSS_CODE_CLEAN",
    "CSS_CODE_NO_IMPORTS",
    "CSS_DATA_ALL",
    "CSS_OUTLINE",
    "CSS_PROFILES",
    "CSS_SRC_CLEAN",
]


_DESIGN_NOTES = """
# simplibs.extractor_css.profiles — The Profiles Themselves

## Purpose
The five profiles as `Profile` objects of the extractor. Registering them is
the job of `register_all`; having them as objects lets a program use one
directly or build its own on top of it.

    from simplibs.extractor_css.profiles import CSS_SRC_CLEAN
    from dataclasses import replace
    mine = replace(CSS_SRC_CLEAN, name="mine", output_name="mine.md")

## Domain Folder
`profiles/` has its own `__all__` and is not re-exported from the package root.

## Internal Components Registry

| Component             | Type    | Description                                                        |
| :-------------------- | :------ | :----------------------------------------------------------------- |
| `CSS_CODE_CLEAN`      | Profile | `css/code-clean`: comments removed.                                |
| `CSS_CODE_NO_IMPORTS` | Profile | `css/code-no-imports`: the rules only.                             |
| `CSS_DATA_ALL`        | Profile | `css/data-all`: every file as it is.                               |
| `CSS_OUTLINE`         | Profile | `css/outline`: selectors and at-rules without declarations.        |
| `CSS_PROFILES`        | Tuple   | All five profiles, in the order the listings show them.            |
| `CSS_SRC_CLEAN`       | Profile | `css/src-clean`: the project's own stylesheets, cleaned.           |
| `steps_for_css`       | Module  | Private: gives each kind of stylesheet its own step.               |

## Layering & Design
- `by_suffix` (one step for a family of file types) is a tool of `simplibs-extractor`.
- The profiles with a step choose it twice, once for `.css` and once for `.scss` and `.less`.
"""
