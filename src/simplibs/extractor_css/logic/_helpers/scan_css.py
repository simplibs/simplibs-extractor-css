# Outers
from ...constants import CSS_LINE_TOKEN_PATTERN, CSS_TOKEN_PATTERN
# Inners
from .CssScan import CssScan
from .find_blanks_start import find_blanks_start
from .fit_comment_span import fit_comment_span
from .line_of import line_of
from .skip_css_comment import skip_css_comment
from .skip_css_string import skip_css_string
from .skip_css_url import skip_css_url


def scan_css(text: str, *, line_comments: bool = False) -> CssScan:
    """Read a stylesheet once and find its comments and literals.

    Args:
        text: The source.
        line_comments: Also treat `// ...` as a comment (SCSS and Less).

    Returns:
        The comments, the comments that need a space left behind, the strings and addresses, and
        the problems that were noticed.
    """

    # 1. State: where the next stop is looked for, and what has been found
    pattern = CSS_LINE_TOKEN_PATTERN if line_comments else CSS_TOKEN_PATTERN
    length = len(text)
    position = 0
    comments: list[tuple[int, int]] = []
    glued: list[tuple[int, int]] = []
    literals: list[tuple[int, int]] = []
    problems: list[str] = []

    while True:

        # 2. Jump to the next place where something may begin; the code in between is not looked at
        found = pattern.search(text, position)
        if found is None:
            break
        start = found.start()
        token = found.group()

        # 3. A quoted string
        if token in ("'", '"'):
            end, closed = skip_css_string(text, start)
            literals.append((start, end))
            if not closed:
                problems.append(f"a string on line {line_of(text, start)} is not closed")
            position = end

        # 4. A block comment
        elif token == "/*":
            end, closed = skip_css_comment(text, start)
            if not closed:
                problems.append(
                    f"a comment on line {line_of(text, start)} is not closed; it runs to the end of the file"
                )
            span, is_glued = fit_comment_span(text, start, end)
            comments.append(span)
            if is_glued:
                glued.append(span)
            position = end

        # 5. A line comment (SCSS and Less only: the pattern finds it only then)
        elif token == "//":
            newline = text.find("\n", start)
            end = length if newline == -1 else newline
            comments.append((find_blanks_start(text, start), end))
            position = end

        # 6. An unquoted address behind `url(`
        else:
            end, closed = skip_css_url(text, found.end())
            if end > found.end():
                literals.append((found.end(), end))
            if not closed:
                problems.append(f"an address in url( on line {line_of(text, start)} is not closed")
            position = end

    return CssScan(tuple(comments), tuple(glued), tuple(literals), tuple(problems))


_DESIGN_NOTES = """
# scan_css — A Scanner, Not a Regex Over the Whole Text

## Purpose
Everything the CSS steps need to know about a source comes from this one
pass: it knows strings and addresses, so a `/*` in `content: "/*"` or a `//`
in `url(//cdn.example.com/a.css)` is never taken for a comment.

## Not a Parser
It builds no tree. It follows only what decides where a comment begins:
quotes, `url(`, `/*` and, for the preprocessors, `//`. That is why it cannot
fail: there is no syntax it refuses.

## It Jumps
A stylesheet is mostly code, and code holds nothing the scanner cares about.
It asks the pattern for the next stop and jumps there instead of walking
character by character.

## Plain CSS and `//`
In a `.css` file `//` is not a comment, so the plain pattern does not even
look for it. With `line_comments=True` (SCSS, Less) it does.

## Problems
A comment that is never closed runs to the end of the file, and a string that
is never closed ends at its line, exactly as a browser reads them. Both are
written down in `problems`, and the steps do not trust a file that has any:
they leave it as it is and warn (see `scan_checked`).

## Known Limits
* SCSS interpolation `#{ ... }` is not understood: a quote inside it that is
  not closed there makes the scan report a damaged string.
* A `//` that follows a value in SCSS (`a: b//c`) is a comment, as the SCSS
  compiler reads it.
* CSS inside a `<style>` element of HTML is the business of the HTML library:
  it hands the content of the element to the steps of this one.
"""
