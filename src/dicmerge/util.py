from pathlib import Path


def expand_paths(patterns: list[str]) -> list[Path]:
    result: list[Path] = []
    for pattern in patterns:
        expanded = Path(pattern).expanduser()
        result.append(expanded)
    return result
