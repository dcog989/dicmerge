from dicmerge.dedup import deduplicate, missing_words


def test_deduplicate_removes_duplicates():
    words = ["foo", "bar", "foo", "baz", "bar"]
    assert deduplicate(words) == ["foo", "bar", "baz"]


def test_deduplicate_case_insensitive():
    words = ["Foo", "foo", "FOO"]
    assert deduplicate(words) == ["Foo"]


def test_deduplicate_preserves_first_occurrence():
    words = ["Foo", "bar", "foo"]
    assert deduplicate(words) == ["Foo", "bar"]


def test_deduplicate_empty():
    assert deduplicate([]) == []


def test_deduplicate_no_duplicates():
    words = ["alpha", "beta", "gamma"]
    assert deduplicate(words) == ["alpha", "beta", "gamma"]


def test_missing_words_returns_not_in_existing():
    all_w = ["foo", "bar", "baz"]
    existing = ["bar"]
    assert missing_words(all_w, existing) == ["foo", "baz"]


def test_missing_words_case_insensitive():
    all_w = ["Foo", "Bar"]
    existing = ["foo"]
    assert missing_words(all_w, existing) == ["Bar"]


def test_missing_words_all_present():
    all_w = ["foo", "bar"]
    existing = ["foo", "bar"]
    assert missing_words(all_w, existing) == []


def test_missing_words_empty_existing():
    all_w = ["foo", "bar"]
    existing: list[str] = []
    assert missing_words(all_w, existing) == ["foo", "bar"]
