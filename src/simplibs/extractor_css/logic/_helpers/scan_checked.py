# Inners
from .CssScan import CssScan
from .scan_css import scan_css
from .warn_scan_problems import warn_scan_problems


def scan_checked(text: str, *, line_comments: bool) -> CssScan | None:
    """Scan a stylesheet and say so when it cannot be trusted.

    Args:
        text: The source.
        line_comments: Also treat `// ...` as a comment (SCSS and Less).

    Returns:
        The scan; `None` if the scanner noticed damage (a warning has been given for each problem).
    """

    # 1. One pass
    scan = scan_css(text, line_comments=line_comments)

    # 2. A file with damage is not read any further: the step leaves it as it is
    if scan.problems:
        warn_scan_problems(scan)
        return None

    return scan


_DESIGN_NOTES = """
# scan_checked — Trust the Scan Only if It Found Nothing Wrong

## Purpose
Every step starts the same way: scan, and if the file looks damaged, give up
on it. The extractor's contract for such a file is that the step returns the
text unchanged and warns; the file then stays in the output as `partial`.
This is the one place where that is decided for the whole library.

## Why Not Go On
A comment that is never closed would swallow the rest of the file, and a
string that is never closed would hide a comment behind it. Cutting on such
a basis loses text silently; leaving the file alone loses nothing.
"""
