import pytest
from simplibs.extractor_css.logic._helpers import Protected


@pytest.mark.parametrize(
    ("position", "expected"),
    [
        (0, False),
        (1, False),
        (2, True),
        (4, True),
        (5, False),
        (7, False),
        (10, True),
        (11, True),
        (12, False),
        (99, False),
    ],
    ids=["before-all", "just-before", "first-start", "inside", "first-end-is-open", "between", "second-start", "second-last", "second-end-is-open", "far-after"],
)
def test_a_position_is_protected_inside_a_range_and_the_end_is_not_part_of_it(position: int, expected: bool) -> None:
    assert Protected([(2, 5), (10, 12)]).contains(position) is expected


def test_ranges_may_come_in_any_order() -> None:
    protected = Protected([(10, 12), (2, 5)])
    assert protected.contains(3) is True
    assert protected.contains(11) is True
    assert protected.contains(7) is False


def test_nothing_is_protected_without_ranges() -> None:
    assert Protected([]).contains(0) is False


def test_ranges_can_come_from_any_iterable() -> None:
    assert Protected(iter([(0, 3)])).contains(2) is True


def test_a_protected_object_has_no_dict() -> None:
    assert not hasattr(Protected([]), "__dict__")
