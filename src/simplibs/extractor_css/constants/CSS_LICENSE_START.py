from typing import Final


CSS_LICENSE_START: Final[str] = "/*!"
"""How a comment that has to survive minification begins."""


_DESIGN_NOTES = """
# CSS_LICENSE_START — The Comment That Tools Keep

## Purpose
By a long-standing convention a block comment starting with `/*!` is the one
that minifiers keep: a licence, a version banner, a copyright line. With
`keep_license` the step keeps it too.
"""
