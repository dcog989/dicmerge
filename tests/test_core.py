from dicmerge.core import _apply_filters


def test_apply_filters_min_length():
    words = ["a", "ab", "abc"]
    result = _apply_filters(words, {"min_length": 2})
    assert result == ["ab", "abc"]


def test_apply_filters_max_length():
    words = ["a", "ab", "abc", "abcd"]
    result = _apply_filters(words, {"min_length": 1, "max_length": 3})
    assert result == ["a", "ab", "abc"]


def test_apply_filters_numbers_not_allowed():
    words = ["foo", "bar123", "baz"]
    result = _apply_filters(words, {"allow_numbers": False})
    assert result == ["foo", "baz"]


def test_apply_filters_numbers_allowed():
    words = ["foo", "bar123", "baz"]
    result = _apply_filters(words, {"allow_numbers": True})
    assert result == ["foo", "bar123", "baz"]


def test_apply_filters_exclude_pattern():
    words = ["foo", "bar", "baz123", "qux"]
    result = _apply_filters(
        words,
        {"exclude_patterns": [r"\d"]},
    )
    assert result == ["foo", "bar", "qux"]


def test_apply_filters_combined():
    words = ["a", "foo", "bar123", "toolongword", "baz", "42"]
    result = _apply_filters(
        words,
        {
            "min_length": 2,
            "max_length": 5,
            "allow_numbers": False,
            "exclude_patterns": [],
        },
    )
    assert result == ["foo", "baz"]
