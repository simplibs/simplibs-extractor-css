import warnings

import pytest
from simplibs.extractor_css.logic._helpers import CssScan, scan_checked


def test_a_healthy_file_is_scanned_without_a_warning() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        scan = scan_checked("a /* x */ b", line_comments=False)
    assert scan == CssScan(((1, 9),), (), (), ())


def test_line_comments_are_passed_on_to_the_scanner() -> None:
    assert scan_checked("a // x\n", line_comments=True) == CssScan(((1, 6),), (), (), ())
    assert scan_checked("a // x\n", line_comments=False) == CssScan((), (), (), ())


@pytest.mark.parametrize(
    ("text", "messages"),
    [
        ("a /* x", ["a comment on line 1 is not closed; it runs to the end of the file"]),
        ('a { b: "x\n}', ["a string on line 1 is not closed"]),
        ("a{b:url(x\n)}", ["an address in url( on line 1 is not closed"]),
        (
            "'a\nb{}\n/* c",
            ["a string on line 1 is not closed", "a comment on line 3 is not closed; it runs to the end of the file"],
        ),
    ],
    ids=["comment", "string", "address", "two-problems"],
)
def test_a_damaged_file_gives_no_scan_and_one_warning_per_problem(text: str, messages: list[str]) -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        scan = scan_checked(text, line_comments=False)
    assert scan is None
    assert [str(warning.message) for warning in caught] == messages
    assert all(issubclass(warning.category, UserWarning) for warning in caught)
