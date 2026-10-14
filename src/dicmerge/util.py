from pathlib import Path

from dicmerge.log import get_logger


def expand_paths(patterns: list[str]) -> list[Path]:
    result: list[Path] = []
    for pattern in patterns:
        expanded = Path(pattern).expanduser()
        result.append(expanded)
    return result


def read_text_with_fallback(path: Path) -> str:
    try:
        raw = path.read_bytes()
    except OSError:
        get_logger().error("Failed to read %s", path)
        raise
    if b"\x00" in raw:
        raise ValueError(f"{path} is not plain text (contains NUL bytes)")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        get_logger().warning("Encoding fallback to latin1 for %s", path)
        return raw.decode("latin1")
