from simplibs.text import Span
from ...constants import CSS_BLOCK_MARKS_PATTERN, CSS_IMPORT_PATTERN
# Inners
from .CssScan import CssScan
from .Protected import Protected
from .blank_spans import blank_spans
from .find_blanks_start import find_blanks_start


def _statement_start(text: str, at: int) -> int:
    """Where the cut of a statement begins: the line start when only blanks stand in front of it."""

    # 1. Blanks that reach back to a line break (or the start of the text) go with the statement
    start = find_blanks_start(text, at)
    if start > 0 and text[start - 1] != "\n":
        return at

    return start


def _statement_end(blanked: str, protected: Protected, at: int) -> int:
    """Where a statement ends: after its semicolon, or at the end of its line if it has none."""

    # 1. The first structural mark outside a string decides; only a semicolon ends the statement
    for mark in CSS_BLOCK_MARKS_PATTERN.finditer(blanked, at):
        if protected.contains(mark.start()):
            continue
        if mark.group() == ";":
            return mark.end()
        break

    # 2. No semicolon before a brace (or at all): the line is the statement
    newline = blanked.find("\n", at)
    return len(blanked) if newline == -1 else newline


def find_import_spans(text: str, scan: CssScan) -> list[Span]:
    """Find the import statements of a stylesheet.

    Args:
        text: The source.
        scan: The result of `scan_css` for `text`.

    Returns:
        A span for each `@import`, `@use` and `@forward` statement that begins a line.
    """

    # 1. Comments are blanked, so an `@import` in a comment is never seen
    blanked = blank_spans(text, scan.comments)
    protected = Protected(scan.literals)

    # 2. Each statement that begins in code is a span from its line start to its semicolon
    spans: list[Span] = []
    for match in CSS_IMPORT_PATTERN.finditer(blanked):
        at = match.start("at")
        if protected.contains(at):
            continue
        spans.append((_statement_start(text, at), _statement_end(blanked, protected, at)))

    return spans


_DESIGN_NOTES = """
# find_import_spans — The Statements, From the Scan

## Purpose
`remove_css_imports` cuts these ranges.

## The End of a Statement
It is the first semicolon that is not inside a string or an address, so
`@import "a;b.css";` is one statement. A statement that meets a brace first
is not terminated (a damaged file), and then the line is taken: the cut never
runs on into the rules that follow.

## The Start of a Statement
The blanks in front of it go with it when they reach back to a line break,
so the whole line can disappear. A statement behind a comment (`/* c */ @import
"a";`) is cut from the `@` on and leaves the comment alone; the comment is the
business of the comment step.
"""
