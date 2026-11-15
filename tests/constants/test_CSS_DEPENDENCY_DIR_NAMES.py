from simplibs.extractor_css.constants import CSS_DEPENDENCY_DIR_NAMES


def test_the_dependency_folders_are_the_documented_names() -> None:
    assert CSS_DEPENDENCY_DIR_NAMES == ("node_modules", "bower_components", "vendor")


def test_no_dependency_folder_is_listed_twice() -> None:
    assert len(CSS_DEPENDENCY_DIR_NAMES) == len(set(CSS_DEPENDENCY_DIR_NAMES))
