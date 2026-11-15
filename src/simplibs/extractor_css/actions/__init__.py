from .CssOutline import CssOutline
from .RemoveCssImports import RemoveCssImports
from .StripCssComments import StripCssComments


__all__ = [
    "CssOutline",
    "RemoveCssImports",
    "StripCssComments",
]


_DESIGN_NOTES = """
# simplibs.extractor_css.actions — The Steps as Pipeline Actions

## Purpose
Every text step of `logic/` as an `Action` of `simplibs-actions`, so it can be
chained with `>>` and used as the `steps` of an extractor profile.

    from simplibs.extractor_css.actions import StripCssComments, RemoveCssImports
    steps = StripCssComments() >> RemoveCssImports()

## Domain Folder
`actions/` has its own `__all__` and is not re-exported from the package root:
a function and an action are different kinds of thing and stay visibly
different at the import line.

## Thin Wrappers
Each action is `create_action(function, main_param="text", ...)`.

## What Has No Action
`css_comment_spans` returns spans, not a text: it is not a link of a pipeline
that carries text.

## Internal Components Registry

| Component          | Type   | Description                            |
| :----------------- | :----- | :------------------------------------- |
| `CssOutline`       | Action | Over `css_outline`.                    |
| `RemoveCssImports` | Action | Over `remove_css_imports`.             |
| `StripCssComments` | Action | Over `strip_css_comments`.             |
"""
