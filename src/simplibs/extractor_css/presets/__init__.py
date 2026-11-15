from .CSS_LINE_CLEAN import CSS_LINE_CLEAN
from .CSS_LINE_NO_IMPORTS import CSS_LINE_NO_IMPORTS
from .CSS_LINE_OUTLINE import CSS_LINE_OUTLINE
from .CSS_PLAIN_CLEAN import CSS_PLAIN_CLEAN
from .CSS_PLAIN_NO_IMPORTS import CSS_PLAIN_NO_IMPORTS
from .CSS_PLAIN_OUTLINE import CSS_PLAIN_OUTLINE


__all__ = [
    "CSS_LINE_CLEAN",
    "CSS_LINE_NO_IMPORTS",
    "CSS_LINE_OUTLINE",
    "CSS_PLAIN_CLEAN",
    "CSS_PLAIN_NO_IMPORTS",
    "CSS_PLAIN_OUTLINE",
]


_DESIGN_NOTES = """
# simplibs.extractor_css.presets — Ready-Made Pipeline Steps

## Purpose
Chains of actions that the profiles use, built once.

    from simplibs.extractor_css.presets import CSS_PLAIN_CLEAN
    steps = CSS_PLAIN_CLEAN

## Domain Folder
`presets/` has its own `__all__` and is not re-exported from the package root.
It stands to the right of `actions` (it uses them) and to the left of `profiles`.

## Two Kinds of File
Each preset exists twice: `PLAIN` for the suffixes where only `/* ... */` is a
comment, `LINE` for those where `// ...` is one too. A step sees only the
text, so the choice is made by the profile, by suffix.

## Internal Components Registry

| Component              | Type   | Description                                                     |
| :--------------------- | :----- | :-------------------------------------------------------------- |
| `CSS_LINE_CLEAN`       | Preset | SCSS and Less without comments, whitespace tidied.              |
| `CSS_LINE_NO_IMPORTS`  | Preset | SCSS and Less rules only, compact.                              |
| `CSS_LINE_OUTLINE`     | Preset | Selectors and at-rules of SCSS and Less.                        |
| `CSS_PLAIN_CLEAN`      | Preset | Plain CSS without comments, whitespace tidied.                  |
| `CSS_PLAIN_NO_IMPORTS` | Preset | Plain CSS rules only, compact.                                  |
| `CSS_PLAIN_OUTLINE`    | Preset | Selectors and at-rules of plain CSS.                            |
"""
