from dataclasses import dataclass
from simplibs.text import Span


@dataclass(frozen=True, slots=True)
class CssScan:
    """What the scanner found in a stylesheet.

    Attributes:
        comments: The spans of every comment, with the blanks in front of it where they can go.
        glued: The comments (a subset of `comments`) whose removal would join two names or two
            numbers; a space has to be left in their place.
        literals: The spans of every string and every unquoted `url(...)` address.
        problems: What looked damaged, one sentence each (a comment or a string that is not closed).
    """

    comments: tuple[Span, ...]
    glued: tuple[Span, ...]
    literals: tuple[Span, ...]
    problems: tuple[str, ...]


_DESIGN_NOTES = """
# CssScan — The Result of One Pass

## Purpose
The scanner reads a stylesheet once and answers four questions together:
where the comments are, which of them need a space in their place, where the
literals are (the places a statement cannot begin in) and whether anything
looked damaged.

## Why a Frozen Record
The four lists belong together and are not changed after the scan.

## `problems`
The scanner never refuses a text. What it notices on the way (a comment that
is never closed) it writes down, and the steps turn it into a warning, so the
extractor can call the file `partial` instead of saying nothing.
"""
