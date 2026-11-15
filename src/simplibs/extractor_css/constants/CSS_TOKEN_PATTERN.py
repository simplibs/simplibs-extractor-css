import re
from typing import Final


CSS_TOKEN_PATTERN: Final[re.Pattern[str]] = re.compile(r"""['"]|/\*|(?<![\w-])url\(""", re.IGNORECASE)
"""What the scanner stops at in plain CSS: a quote, the start of a block comment, or `url(`."""


_DESIGN_NOTES = """
# CSS_TOKEN_PATTERN — Where Something Interesting Begins

## Purpose
The scanner does not look at every character. It asks this pattern for the
next place where a string, a comment or an unquoted address may begin, and
jumps there. Everything in between is plain code.

## `url(`
An unquoted address may contain `//` and `/*` (`url(//cdn.example.com/a.css)`),
and neither is a comment. The pattern finds `url(` so the scanner can skip the
address as a whole. The lookbehind keeps names such as `data-url(` or `curl(`
from being taken for it.

## Case
CSS keywords do not care about case, so `URL(` is found too.
"""
