from typing import Final


CSS_OUTPUT_DIR_NAMES: Final[tuple[str, ...]] = (
    "build",
    "dist",
    "out",
    ".next",
    ".nuxt",
    "staticfiles",
    "coverage",
    "htmlcov",
    "storybook-static",
)
"""Names of folders that hold generated files, stylesheets of build tools and reports included."""


_DESIGN_NOTES = """
# CSS_OUTPUT_DIR_NAMES — Generated, Not Written

## Purpose
The names behind `OUTPUT_DIRS`. These folders contain stylesheets that a
tool made: reading them repeats the source in another shape.

## `staticfiles`
The target of Django's `collectstatic`. It copies the stylesheets of every
installed app into one folder, the admin's included, so everything in it is
either a second copy of the project's own files or somebody else's code.

## `coverage`, `htmlcov`, `storybook-static`
Test-coverage reports and a built Storybook come with stylesheets of their
own (`base.css`, `style.css`).

## `static` Is Not Here
In a Django project `static/` is where the source stylesheets live. In a
React project the JavaScript add-on treats it as an asset folder, but for
stylesheets that would hide the project's own files.

## `.next` and `.nuxt`
They start with a dot, but the base rule only leaves out dot FILES, so
without these names the compiled stylesheets inside would be read as source.
"""
