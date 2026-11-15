from .css_comment_spans import css_comment_spans
from .css_outline import css_outline
from .remove_css_imports import remove_css_imports
from .strip_css_comments import strip_css_comments


_DESIGN_NOTES = """
# logic — The Steps That Read Stylesheets

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component            | Type     | Description                                                     |
| :------------------- | :------- | :-------------------------------------------------------------- |
| `css_comment_spans`  | Function | The spans of the comments (by the scanner).                     |
| `css_outline`        | Function | The headers of the blocks, indented by depth.                   |
| `remove_css_imports` | Function | Removes `@import`, `@use` and `@forward`.                       |
| `strip_css_comments` | Function | Removes the comments.                                           |
| `_helpers`           | Private  | The scanner and the parts it is made of.                        |

## Layering & Design
- A stylesheet is read by a scanner that knows strings and addresses; it is not a parser and cannot fail.
- A file that looks damaged is left as it is and reported by a warning, so the extractor calls it `partial`.
- Each step is a function of a text and returns a text; the `Action` wrappers come in `actions`.
- The steps import only `constants`; the ranges they find are `simplibs.text.Span`.
"""
