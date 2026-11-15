from ...constants import CSS_BLOCK_MARKS_PATTERN
# Inners
from .CssScan import CssScan
from .Protected import Protected
from .blank_spans import blank_spans


def build_outline(text: str, scan: CssScan, max_depth: int | None) -> tuple[list[str], list[str]]:
    """Write the headers of the blocks of a stylesheet, one line each, indented by depth.

    Args:
        text: The source.
        scan: The result of `scan_css` for `text`.
        max_depth: The number of levels to list, or `None` for all of them.

    Returns:
        The lines, and the problems found (braces that do not pair up).
    """

    # 1. Comments are blanked and strings are protected, so only real braces count
    blanked = blank_spans(text, scan.comments)
    protected = Protected(scan.literals)

    lines: list[str] = []
    depth = 0
    interpolation = 0
    stray = 0
    boundary = 0

    for mark in CSS_BLOCK_MARKS_PATTERN.finditer(blanked):
        position = mark.start()
        if protected.contains(position):
            continue
        character = mark.group()

        # 2. `#{ ... }` of SCSS is a value inside a name, not a block
        if character == "{" and position > 0 and blanked[position - 1] == "#":
            interpolation += 1
            continue
        if interpolation:
            if character == "}":
                interpolation -= 1
            continue

        # 3. A block opens: what stands since the last mark is its header
        if character == "{":
            header = " ".join(blanked[boundary:position].split())
            if header and (max_depth is None or depth < max_depth):
                lines.append("  " * depth + header)
            depth += 1

        # 4. A block closes
        elif character == "}":
            if depth:
                depth -= 1
            else:
                stray += 1

        # 5. Every mark starts a new stretch of text
        boundary = position + 1

    # 6. Braces that do not pair up
    problems: list[str] = []
    if depth:
        problems.append(f"{depth} block(s) are never closed")
    if stray:
        problems.append(f"{stray} closing brace(s) have no opening one")

    return lines, problems


_DESIGN_NOTES = """
# build_outline — The Blocks of a Stylesheet in a Few Lines

## Purpose
What a reader needs from a large stylesheet to ask the right questions:
which selectors and which at-rules (`@media`, `@keyframes`, `@mixin`) it
has, and how they are nested. The declarations are the detail.

## How
A header is whatever stands between the last `{`, `}` or `;` and the next
`{`, with comments blanked and blanks collapsed. A declaration ends in `;`, so
it never becomes a header; an at-rule without a block (`@charset`, `@include
x;`) does not either.

## Nesting
Plain CSS nests (`@media`, `@supports`, `@layer`, native nesting) and so do
SCSS and Less. Each level is indented by two spaces.

## `max_depth`
`1` lists only the top level, `2` adds one level below it, `None` lists all.

## SCSS Interpolation
`.col-#{$i} { ... }` has a brace that is not a block. A `{` right behind a `#`
is counted separately and does not become a header or a level.

## Known Limits
SCSS nested properties (`font: { family: x; }`) are listed as a block with the
header `font:`. Keyframe steps (`from`, `50%`) are listed under their
`@keyframes`; a smaller `max_depth` hides them.
"""
