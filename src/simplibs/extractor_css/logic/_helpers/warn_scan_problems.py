# Inners
from .CssScan import CssScan
from .warn_problems import warn_problems


def warn_scan_problems(scan: CssScan) -> None:
    """Turn what the scanner noticed into warnings.

    Args:
        scan: The result of `scan_css`.
    """

    # 1. The sentences of the scan
    warn_problems(scan.problems)


_DESIGN_NOTES = """
# warn_scan_problems — The Scan Speaks

## Purpose
The scanner writes its problems into the result and does not warn itself, so
`scan_css` stays a pure function that anybody may call. This is the step
between the result and the warnings.
"""
