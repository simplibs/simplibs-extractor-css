import warnings
from collections.abc import Iterable


def warn_problems(problems: Iterable[str]) -> None:
    """Turn sentences about a damaged file into warnings.

    Args:
        problems: What looked wrong, one sentence each.
    """

    # 1. One warning for each, in the order of the file
    for problem in problems:
        warnings.warn(problem, UserWarning, stacklevel=2)


_DESIGN_NOTES = """
# warn_problems — A File That Is Not Quite Right Is Not an Error

## Purpose
A step is a plain function of a text and knows nothing about the extractor.
`warnings.warn` is the one channel it can use without importing anything. The
extractor collects the warnings of a file, calls the file `partial` and writes
the sentence into the report, while the file stays in the output.

## Why `UserWarning`
It is the category the extractor listens to. A `DeprecationWarning` from some
library inside a step says something about the code, not about the file.

## Outside the Extractor
Called on its own, the step gives the usual Python warning on the error
stream, once for each place.
"""
