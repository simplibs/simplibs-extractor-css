from pathlib import Path

import pytest
from simplibs.extractor_css.file_rules import (
    CSS_STRICT_EXCLUDE,
    DEPENDENCY_DIRS,
    MINIFIED_NAME,
    OUTPUT_DIRS,
    VCS_DIRS,
)

PATHS = [
    "a.css",
    "app.min.css",
    "src/theme.min.scss",
    "node_modules/p/a.css",
    "static/vendor/x/a.css",
    "dist/a.css",
    ".next/a.css",
    "staticfiles/a.css",
    ".git/x.css",
    "coverage/a.css",
    "static/site.css",
    "src/a.scss",
    "administration.css",
]


@pytest.mark.parametrize(
    "path",
    [
        "app.min.css",
        "src/theme.min.scss",
        "node_modules/p/a.css",
        "static/vendor/x/a.css",
        "bower_components/a.css",
        "dist/a.css",
        "build/a.less",
        ".next/static/a.css",
        ".nuxt/a.css",
        "staticfiles/admin/a.css",
        "coverage/lcov-report/base.css",
        "storybook-static/a.css",
        ".git/hooks/x.css",
        ".svn/x.css",
    ],
    ids=["minified", "minified-scss", "node-modules", "django-vendor", "bower", "dist", "build", "next", "nuxt", "collectstatic", "coverage", "storybook", "git", "svn"],
)
def test_everything_that_is_not_the_projects_own_source_is_left_out(path: str) -> None:
    assert CSS_STRICT_EXCLUDE.is_valid(path) is True


@pytest.mark.parametrize(
    "path",
    ["a.css", "src/a.scss", "styles/a.less", "static/site.css", "administration.css", "static/css/main.css", "", None, 5],
    ids=["plain", "scss", "less", "django-source-folder", "word-ending-in-min", "nested-source-folder", "empty", "None", "int"],
)
def test_the_projects_own_source_is_kept(path: object) -> None:
    assert CSS_STRICT_EXCLUDE.is_valid(path) is False


@pytest.mark.parametrize("path", PATHS)
def test_the_rule_is_the_union_of_the_four_atomic_ones(path: str) -> None:
    expected = any(rule.is_valid(path) for rule in (MINIFIED_NAME, VCS_DIRS, DEPENDENCY_DIRS, OUTPUT_DIRS))
    assert CSS_STRICT_EXCLUDE.is_valid(path) is expected


def test_a_path_object_gives_the_same_answer() -> None:
    assert CSS_STRICT_EXCLUDE.is_valid(Path("dist/a.css")) is True
    assert CSS_STRICT_EXCLUDE.is_valid(Path("src/a.css")) is False
