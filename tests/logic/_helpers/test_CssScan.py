import dataclasses

import pytest
from simplibs.extractor_css.logic._helpers import CssScan


def make_scan() -> CssScan:
    return CssScan(comments=((0, 4),), glued=((0, 4),), literals=((6, 9),), problems=("a string is not closed",))


def test_a_scan_holds_what_the_scanner_found() -> None:
    scan = make_scan()
    assert scan.comments == ((0, 4),)
    assert scan.glued == ((0, 4),)
    assert scan.literals == ((6, 9),)
    assert scan.problems == ("a string is not closed",)


def test_the_fields_are_in_the_documented_order() -> None:
    assert [field.name for field in dataclasses.fields(CssScan)] == ["comments", "glued", "literals", "problems"]
    assert CssScan(((0, 1),), (), (), ()).comments == ((0, 1),)


def test_a_scan_cannot_be_changed() -> None:
    with pytest.raises(dataclasses.FrozenInstanceError):
        make_scan().comments = ()  # type: ignore[misc]


def test_a_scan_has_no_dict() -> None:
    assert not hasattr(make_scan(), "__dict__")


def test_scans_with_the_same_content_are_equal() -> None:
    assert make_scan() == make_scan()
    assert make_scan() != CssScan((), (), (), ())
