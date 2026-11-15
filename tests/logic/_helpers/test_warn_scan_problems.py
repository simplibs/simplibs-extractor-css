import warnings

from simplibs.extractor_css.logic._helpers import CssScan, warn_scan_problems


def test_the_problems_of_a_scan_become_warnings() -> None:
    scan = CssScan(comments=((0, 4),), glued=(), literals=(), problems=("a string is not closed", "a comment is not closed"))
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warn_scan_problems(scan)
    assert [str(warning.message) for warning in caught] == ["a string is not closed", "a comment is not closed"]
    assert all(warning.category is UserWarning for warning in caught)


def test_a_scan_without_problems_gives_no_warning() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        warn_scan_problems(CssScan((), (), (), ()))
