from .CssScan import CssScan
from .Protected import Protected
from .blank_spans import blank_spans
from .build_outline import build_outline
from .find_blanks_start import find_blanks_start
from .find_comments import find_comments
from .find_import_spans import find_import_spans
from .fit_comment_span import fit_comment_span
from .is_license_comment import is_license_comment
from .line_of import line_of
from .needs_gap import needs_gap
from .remove_with_gaps import remove_with_gaps
from .scan_checked import scan_checked
from .scan_css import scan_css
from .skip_css_comment import skip_css_comment
from .skip_css_string import skip_css_string
from .skip_css_url import skip_css_url
from .warn_problems import warn_problems
from .warn_scan_problems import warn_scan_problems


_DESIGN_NOTES = """
# _helpers — The Scanner and Its Parts

Private. Plain imports, no `__all__`.

## Internal Components Registry

| Component             | Type     | Description                                                          |
| :-------------------- | :------- | :------------------------------------------------------------------- |
| `CssScan`             | Class    | Comments, glued comments, literals and problems found in one pass.   |
| `Protected`           | Class    | Answers whether a position lies inside a string, an address or a comment. |
| `blank_spans`         | Function | Replaces ranges with blanks, keeping every offset.                   |
| `build_outline`       | Function | The headers of the blocks, indented by depth.                        |
| `find_blanks_start`   | Function | Moves back over the blanks in front of a comment.                    |
| `find_comments`       | Function | Scans and chooses the comments a step cuts.                          |
| `find_import_spans`   | Function | The ranges of the import statements.                                 |
| `fit_comment_span`    | Function | The cut of one block comment, and whether a space must stay.         |
| `is_license_comment`  | Function | Is this a comment that tools keep?                                   |
| `line_of`             | Function | The line of an offset.                                               |
| `needs_gap`           | Function | Would two characters merge into one token?                           |
| `remove_with_gaps`    | Function | Removes spans, leaving a space where one was marked.                 |
| `scan_checked`        | Function | Scans; gives `None` and warns when the file looks damaged.           |
| `scan_css`            | Function | One pass over a source: comments, literals, problems.                |
| `skip_css_comment`    | Function | The end of a block comment.                                          |
| `skip_css_string`     | Function | The end of a quoted string.                                          |
| `skip_css_url`        | Function | The end of an unquoted `url(...)` address.                           |
| `warn_problems`       | Function | Turns sentences about a damaged file into warnings.                  |
| `warn_scan_problems`  | Function | Turns the problems of a scan into warnings.                          |
"""
