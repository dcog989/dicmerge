import os
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


def ensure_trailing_newline(path: Path) -> None:
    if path.exists() and path.stat().st_size > 0:
        with path.open("rb") as f:
            f.seek(-1, os.SEEK_END)
            if f.read(1) != b"\n":
                with path.open("a", encoding="utf-8") as fw:
                    fw.write("\n")
