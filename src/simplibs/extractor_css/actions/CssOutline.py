from simplibs.actions import create_action
# Outers
from ..logic import css_outline


CssOutline = create_action(
    css_outline,
    main_param="text",
    class_name="CssOutline",
)
"""Action wrapping `css_outline` — turns the stylesheet flowing in into the list of its selectors and at-rules."""


_DESIGN_NOTES = """
# CssOutline — Action Over `css_outline`

## Purpose
The overview step as a link of a pipeline: `CssOutline(max_depth=2)`.

## Shape
Main input: `text`. Options: `line_comments` (read `// ...` as a comment) and
`max_depth` (how many levels of nesting to list; all by default). Text in,
text out (one header per line, indented by depth).
"""
