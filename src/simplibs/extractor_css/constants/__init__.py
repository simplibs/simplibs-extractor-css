from .CSS_BLOCK_MARKS_PATTERN import CSS_BLOCK_MARKS_PATTERN
from .CSS_DEPENDENCY_DIR_NAMES import CSS_DEPENDENCY_DIR_NAMES
from .CSS_EXTRA_LANGUAGE_BY_SUFFIX import CSS_EXTRA_LANGUAGE_BY_SUFFIX
from .CSS_IMPORT_PATTERN import CSS_IMPORT_PATTERN
from .CSS_LICENSE_START import CSS_LICENSE_START
from .CSS_LICENSE_TAGS import CSS_LICENSE_TAGS
from .CSS_LINE_COMMENT_SUFFIXES import CSS_LINE_COMMENT_SUFFIXES
from .CSS_LINE_TOKEN_PATTERN import CSS_LINE_TOKEN_PATTERN
from .CSS_MINIFIED_ENDING import CSS_MINIFIED_ENDING
from .CSS_OUTPUT_DIR_NAMES import CSS_OUTPUT_DIR_NAMES
from .CSS_PLAIN_SUFFIXES import CSS_PLAIN_SUFFIXES
from .CSS_SUFFIXES import CSS_SUFFIXES
from .CSS_TOKEN_PATTERN import CSS_TOKEN_PATTERN


_DESIGN_NOTES = """
# constants — Fixed Values of simplibs-extractor-css

Plain imports, no `__all__` (the package root decides what is public).

## Internal Components Registry

| Component                      | Type     | Description                                                 |
| :----------------------------- | :------- | :---------------------------------------------------------- |
| `CSS_BLOCK_MARKS_PATTERN`      | Pattern  | The braces and the semicolon that structure a stylesheet.   |
| `CSS_DEPENDENCY_DIR_NAMES`     | Constant | Folders of stylesheets written by other people.             |
| `CSS_EXTRA_LANGUAGE_BY_SUFFIX` | Constant | The fence language of `.scss` and `.less`.                  |
| `CSS_IMPORT_PATTERN`           | Pattern  | The start of `@import`, `@use` and `@forward`.              |
| `CSS_LICENSE_START`            | Constant | How a comment that has to survive minification begins.      |
| `CSS_LICENSE_TAGS`             | Constant | Words that mark a comment as one to keep.                   |
| `CSS_LINE_COMMENT_SUFFIXES`    | Constant | Suffixes of preprocessors with `//` comments.               |
| `CSS_LINE_TOKEN_PATTERN`       | Pattern  | Where the scanner stops in SCSS and Less.                   |
| `CSS_MINIFIED_ENDING`          | Constant | What the stem of a minified stylesheet ends with.           |
| `CSS_OUTPUT_DIR_NAMES`         | Constant | Folders of generated files and reports.                     |
| `CSS_PLAIN_SUFFIXES`           | Constant | Suffixes of plain CSS.                                      |
| `CSS_SUFFIXES`                 | Constant | Suffixes of every stylesheet the library reads.             |
| `CSS_TOKEN_PATTERN`            | Pattern  | Where the scanner stops in plain CSS.                       |

## Layering & Design
- Every value is a tuple, a plain string, a small dict or a compiled pattern: the rules and the steps are built from them.
- The names of version-control folders are not here: they come from `IGNORE_VCS` of `simplibs-path`.
- There is no list of configuration names: no tool keeps its settings in a file with a stylesheet suffix.
"""
