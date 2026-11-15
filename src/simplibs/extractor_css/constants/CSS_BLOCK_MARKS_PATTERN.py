import re
from typing import Final


CSS_BLOCK_MARKS_PATTERN: Final[re.Pattern[str]] = re.compile(r"[{};]")
"""The three characters that structure a stylesheet: an opening brace, a closing brace and a semicolon."""


_DESIGN_NOTES = """
# CSS_BLOCK_MARKS_PATTERN — The Skeleton of a Stylesheet

## Purpose
A rule ends at `}`, a block opens at `{`, a declaration or an at-rule without
a block ends at `;`. The outline and the end of an import statement are found
by walking these three and nothing else.

## Not Here
Whether a mark sits inside a string or an address is not this pattern's
business: the steps skip the marks the scanner has put in a literal.
"""
