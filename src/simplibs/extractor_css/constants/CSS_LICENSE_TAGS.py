from typing import Final


CSS_LICENSE_TAGS: Final[tuple[str, ...]] = ("@license", "@preserve")
"""Words inside a comment that mark it as one to keep."""


_DESIGN_NOTES = """
# CSS_LICENSE_TAGS — The Other Way to Say "Keep This"

## Purpose
Besides the leading `!`, minifiers keep a comment that contains `@license` or
`@preserve`. The same two words keep it here.
"""
