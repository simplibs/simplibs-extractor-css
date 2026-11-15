from simplibs.extractor_css.constants import CSS_OUTPUT_DIR_NAMES


def test_the_output_folders_are_the_documented_names() -> None:
    assert CSS_OUTPUT_DIR_NAMES == (
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


def test_the_dot_folders_of_the_frameworks_are_listed_by_name() -> None:
    # The base rule leaves out only dot FILES, so these names are what keeps the compiled stylesheets out.
    assert ".next" in CSS_OUTPUT_DIR_NAMES
    assert ".nuxt" in CSS_OUTPUT_DIR_NAMES


def test_static_is_not_an_output_folder_because_django_keeps_its_source_there() -> None:
    assert "static" not in CSS_OUTPUT_DIR_NAMES


def test_no_output_folder_is_listed_twice() -> None:
    assert len(CSS_OUTPUT_DIR_NAMES) == len(set(CSS_OUTPUT_DIR_NAMES))
