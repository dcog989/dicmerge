def deduplicate(words: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for word in words:
        key = word.casefold()
        if key not in seen:
            seen.add(key)
            result.append(word)
    return result


def missing_words(all_words: list[str], existing: list[str]) -> list[str]:
    existing_lower = {w.casefold() for w in existing}
    return [w for w in all_words if w.casefold() not in existing_lower]
