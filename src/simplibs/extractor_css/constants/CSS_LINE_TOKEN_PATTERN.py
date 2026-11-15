import re
from typing import Final


CSS_LINE_TOKEN_PATTERN: Final[re.Pattern[str]] = re.compile(r"""['"]|/\*|//|(?<![\w-])url\(""", re.IGNORECASE)
"""What the scanner stops at in SCSS and Less: the same as `CSS_TOKEN_PATTERN`, and the start of a `//` comment."""


_DESIGN_NOTES = """
# CSS_LINE_TOKEN_PATTERN — The Same, With `//`

## Purpose
SCSS and Less have a second kind of comment that runs to the end of the line.
It is a separate pattern and not a switch inside the first one, so a plain
`.css` file can never have its `//` cut by mistake.

## Order
Strings and `url(` are found before a `//` that lies after them in the same
line, so `url(//cdn.example.com/a.png)` is skipped as an address and is not
read as a comment.
"""
