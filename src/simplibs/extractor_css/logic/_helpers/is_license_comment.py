from ...constants import CSS_LICENSE_START, CSS_LICENSE_TAGS


def is_license_comment(comment: str) -> bool:
    """Say whether a comment is one that tools keep (a licence, a banner).

    Args:
        comment: The text of the comment, with its `/*` and `*/` (blanks in front are allowed).

    Returns:
        `True` if it begins with `/*!` or contains `@license` or `@preserve`.
    """

    # 1. The marker at the start, or one of the words anywhere
    stripped = comment.lstrip()
    return stripped.startswith(CSS_LICENSE_START) or any(tag in stripped for tag in CSS_LICENSE_TAGS)


_DESIGN_NOTES = """
# is_license_comment — Who Wants to Be Kept

## Purpose
The only comments a reader of a stylesheet may not want to lose are the
licence and the banner of a library. The convention that marks them is the
one minifiers already follow.

## Line Comments
A `// @license` of SCSS is judged the same way: the test looks at the words, not
at the kind of comment.
"""
