from typing import Final


CSS_EXTRA_LANGUAGE_BY_SUFFIX: Final[dict[str, str]] = {
    ".scss": "scss",
    ".less": "less",
}
"""The code-fence language of the suffixes the extractor does not know on its own."""


_DESIGN_NOTES = """
# CSS_EXTRA_LANGUAGE_BY_SUFFIX — Names for the Fence

## Purpose
The markdown output writes the language after the opening fence, so a viewer
can colour the code. The extractor knows `.css` itself; `.scss` and `.less`
are what this add-on brings, and `register_all` tells the extractor about them.

## Only What Is Missing
`.css` is not listed: registering it again would change nothing.
"""
