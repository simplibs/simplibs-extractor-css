from simplibs.actions import create_action
# Outers
from ..logic import remove_css_imports


RemoveCssImports = create_action(
    remove_css_imports,
    main_param="text",
    class_name="RemoveCssImports",
)
"""Action wrapping `remove_css_imports` — takes `@import`, `@use` and `@forward` out of the stylesheet flowing in."""


_DESIGN_NOTES = """
# RemoveCssImports — Action Over `remove_css_imports`

## Purpose
The import step as a link of a pipeline: `RemoveCssImports(line_comments=True)`.

## Shape
Main input: `text`. Option: `line_comments` (read `// ...` as a comment, for
SCSS and Less). Text in, text out.
"""
