from .logic import (
    css_comment_spans,
    css_outline,
    remove_css_imports,
    strip_css_comments,
)
from .plugin import register_all


__all__ = [
    # steps
    "css_comment_spans",
    "css_outline",
    "remove_css_imports",
    "strip_css_comments",
    # add-on of the extractor
    "register_all",
]


_DESIGN_NOTES = """
# simplibs-extractor-css — Package Root

## Purpose
The add-on that teaches `simplibs-extractor` about stylesheets (CSS, SCSS and
Less): file rules for such projects, the steps that clean the source
(comments, imports) or reduce it to an overview, and five ready profiles.
Install it and the profiles are there:

    simplibs-extractor css src-clean my_project

## What the Root Exports
The steps as plain functions (`str -> str`, except the spans) and `register_all`
(the target of the entry point `simplibs.extractor.plugins`):

    from simplibs.extractor_css import strip_css_comments, css_outline

## What the Root Deliberately Does NOT Export
Four domain folders with their own `__all__`, imported through their domain:

    from simplibs.extractor_css.actions import StripCssComments
    from simplibs.extractor_css.file_rules import CSS_BASE
    from simplibs.extractor_css.presets import CSS_PLAIN_CLEAN
    from simplibs.extractor_css.profiles import CSS_SRC_CLEAN

and the internals: `_helpers/` inside `logic`.

## Spans
The steps find ranges of characters as `simplibs.text.Span`. The type is not
defined here, it is taken from `simplibs-text`.

## Layering
`constants` ← `file_rules` ← `logic` ← `actions` ← `presets` ← `profiles` ← `plugin`.
Each layer imports only from the layers on its left; the root imports from the ones it exports.

## `__all__`
Defined here and in the domain folders (`actions`, `file_rules`, `presets`,
`profiles`) only; the layers inside them use plain imports.
"""
