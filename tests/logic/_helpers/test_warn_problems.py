import warnings

from simplibs.extractor_css.logic._helpers import warn_problems


def test_every_problem_becomes_one_user_warning_in_order() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warn_problems(["first problem", "second problem"])
    assert [str(warning.message) for warning in caught] == ["first problem", "second problem"]
    assert [warning.category for warning in caught] == [UserWarning, UserWarning]


def test_no_problems_give_no_warning() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        warn_problems([])


def test_any_iterable_of_problems_is_accepted() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warn_problems(problem for problem in ("only one",))
    assert [str(warning.message) for warning in caught] == ["only one"]
