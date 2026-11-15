from bisect import bisect_right
from collections.abc import Iterable
from simplibs.text import Span


class Protected:
    """Places where a statement cannot begin: strings, addresses, comments.

    Args:
        spans: Ranges that do not overlap (the literals or the comments of a scan).
    """

    __slots__ = ("_spans", "_starts")

    def __init__(self, spans: Iterable[Span]) -> None:

        # 1. Sorted once, so a question costs a binary search
        self._spans = sorted(spans)
        self._starts = [start for start, _ in self._spans]

    def contains(self, position: int) -> bool:
        """Say whether an offset lies inside one of the ranges."""

        # 1. The last range that starts at or before the position is the only one that can hold it
        index = bisect_right(self._starts, position) - 1
        return index >= 0 and position < self._spans[index][1]


_DESIGN_NOTES = """
# Protected — Is This Position Inside Something

## Purpose
A `;` inside `"a;b.css"` does not end a statement, and a `{` inside
`url({x})` does not open a block. The import and outline steps ask this
object before they trust a mark.

## Why a Class
The sorted ranges and their starts are made once and used for every mark of
a file; a function would have to be given both each time.

## Ranges Must Not Overlap
The literals of a scan do not (a string and an address exclude each other),
and neither do its comments, so the last range that starts before a position
is the only candidate.
"""
