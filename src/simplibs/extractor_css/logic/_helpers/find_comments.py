from simplibs.text import Span
# Inners
from .is_license_comment import is_license_comment
from .scan_checked import scan_checked


def find_comments(text: str, *, line_comments: bool, keep_license: bool) -> tuple[list[Span], list[Span]]:
    """Scan a stylesheet and choose the comments a step is going to cut.

    Args:
        text: The source.
        line_comments: Also treat `// ...` as a comment (SCSS and Less).
        keep_license: Leave out the comments that tools keep (`/*! ... */`, `@license`, `@preserve`).

    Returns:
        The comments to cut, and which of them need a space left behind; both empty for a file that
        looks damaged (a warning has been given).
    """

    # 1. One pass; a damaged file is left alone
    scan = scan_checked(text, line_comments=line_comments)
    if scan is None:
        return [], []

    # 2. Everything goes unless the licences are to stay
    if not keep_license:
        return list(scan.comments), list(scan.glued)

    # 3. The licences are told apart by their text
    kept = {span for span in scan.comments if is_license_comment(text[span[0]:span[1]])}
    comments = [span for span in scan.comments if span not in kept]
    glued = [span for span in scan.glued if span not in kept]

    return comments, glued


_DESIGN_NOTES = """
# find_comments — The One Place That Chooses the Comments

## Purpose
`css_comment_spans` and `strip_css_comments` answer the same question, "which
comments", and differ only in what they do with the answer. The scan, the
damage check and the licences are decided here, once.

## Spans Are Compared as They Are
A span that is kept is left out of both lists by its value, so a glued comment
that is a licence leaves the second list together with the first.

## A Damaged File
No comments are reported at all, so a step that cuts them cuts nothing and
returns the text unchanged.
"""
