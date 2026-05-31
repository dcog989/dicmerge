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
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        get_logger().warning("Encoding fallback to latin1 for %s", path)
        return path.read_text(encoding="latin1")
    except Exception:
        get_logger().error("Failed to read %s with utf-8 or latin1", path)
        raise
