from collections.abc import Iterable
from simplibs.text import Span


def blank_spans(text: str, spans: Iterable[Span]) -> str:
    """Replace the characters of some ranges with spaces, keeping every line break and every offset.

    Args:
        text: The source.
        spans: The ranges to blank (the comments of a scan).

    Returns:
        A text of the same length in which the ranges hold only spaces and line breaks.
    """

    # 1. Copy what is between the ranges, put blanks where the ranges were
    pieces: list[str] = []
    previous = 0
    for start, end in sorted(spans):
        pieces.append(text[previous:start])
        pieces.append("".join("\n" if character == "\n" else " " for character in text[start:end]))
        previous = end
    pieces.append(text[previous:])

    return "".join(pieces)


_DESIGN_NOTES = """
# blank_spans — Hide Without Moving

## Purpose
A header of a rule may have a comment inside it (`.a, /* old */ .b {`).
Cutting the comments out would shift every offset the scan reported; blanking
them leaves all offsets where they were, and the words around the comment
only need their blanks collapsed.

## Line Breaks Stay
The blanked text has the same lines as the original, so a statement that is
found in it starts at the same line in both.
"""
