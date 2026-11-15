from simplibs.actions import create_action
# Outers
from ..logic import strip_css_comments


StripCssComments = create_action(
    strip_css_comments,
    main_param="text",
    class_name="StripCssComments",
)
"""Action wrapping `strip_css_comments` — takes the comments out of the stylesheet flowing in."""


_DESIGN_NOTES = """
# StripCssComments — Action Over `strip_css_comments`

## Purpose
The comment step as a link of a pipeline: `StripCssComments(line_comments=True, keep_license=True)`.

## Shape
Main input: `text`. Options: `line_comments` (also `// ...`, for SCSS and Less) and
`keep_license` (leave `/*! ... */`, `@license` and `@preserve` comments). Text in, text out.

## One Action, Not Two
SCSS and Less need only the option, so there is no second class for them; the
profiles build the two pipelines from the same action.
"""
