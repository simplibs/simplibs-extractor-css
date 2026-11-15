from simplibs.actions import Action
from simplibs.extractor import by_suffix
# Outers
from ..constants import CSS_LINE_COMMENT_SUFFIXES, CSS_PLAIN_SUFFIXES


def steps_for_css(plain: Action, line: Action) -> dict[str, Action]:
    """Give each kind of stylesheet its own step.

    Args:
        plain: The step for the suffixes where only `/* ... */` is a comment.
        line: The step for the suffixes where `// ...` is a comment too.

    Returns:
        A mapping `suffix -> step`, the form of `Profile.steps` that chooses by file type.
    """

    # 1. `by_suffix` for each half, the two mappings side by side
    return {
        **by_suffix(plain, CSS_PLAIN_SUFFIXES),
        **by_suffix(line, CSS_LINE_COMMENT_SUFFIXES),
    }


_DESIGN_NOTES = """
# steps_for_css — One Step for Each Kind of Stylesheet

## Purpose
Four of the five profiles pick a step by the kind of file. The two halves of
the suffixes do not overlap, so merging the mappings never loses a step.

## Not Exported
A tool of the profiles' own: it is not in `__all__` of the folder.
"""
