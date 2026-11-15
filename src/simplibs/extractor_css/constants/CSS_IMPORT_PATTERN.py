import re
from typing import Final


CSS_IMPORT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"""^[ \t]*(?P<at>@)(?:import|use|forward)(?![\w-])""",
    re.MULTILINE | re.IGNORECASE,
)
"""The start of a statement that pulls in another stylesheet, at the beginning of a line: `@import`, `@use`, `@forward`."""


_DESIGN_NOTES = """
# CSS_IMPORT_PATTERN — Where an Import Statement Begins

## Purpose
What `remove_css_imports` looks for. It finds only the beginning; where the
statement ends is decided by the scanner's knowledge of strings (an address
may contain a semicolon).

## What It Takes
`@import url("a.css") screen;` of CSS, `@import 'a', 'b';` of SCSS and
`@import (reference) "a";` of Less, and the two module statements of SCSS,
`@use` and `@forward`. All of them say "this file needs that one", which is
what a profile without imports leaves out.

## What It Leaves
A statement that is not the first thing on its line (a minified file). The
name must end there: `@use-foo` is not `@use`.

## The Group `at`
The position of the `@` itself. The match may start with blanks, but whether
it sits in a string or a comment is decided by the `@`.
"""
