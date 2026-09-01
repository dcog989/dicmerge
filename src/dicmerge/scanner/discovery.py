import glob
from pathlib import Path
from typing import Any

from dicmerge.util import expand_paths

_BACKUP_MARKERS = {"-backup", "-back-ovfs"}


def _is_backup(path: Path) -> bool:
    if any(part.endswith(m) for part in path.parts for m in _BACKUP_MARKERS):
        return True
    return path.suffix == ".bak"


def _discover_paths(patterns: list[str], *, recursive: bool) -> list[Path]:
    files: list[Path] = []
    for pattern in expand_paths(patterns):
        matches = glob.glob(str(pattern), recursive=recursive)
        files.extend(p for p in (Path(m) for m in matches) if not _is_backup(p))
    return sorted(set(files))


def discover_source_files(config: dict[str, Any]) -> dict[str, list[Path]]:
    discovered: dict[str, list[Path]] = {}

    for name, source in config["sources"].items():
        if not source.get("enabled", True):
            continue
        discovered[name] = _discover_paths(source["paths"], recursive=source.get("recursive", False))

    for entry in config.get("custom_sources", []):
        if not entry.get("enabled", False):
            continue
        discovered[entry["name"]] = _discover_paths(entry["paths"], recursive=False)

    return discovered
