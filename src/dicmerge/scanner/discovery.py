import glob
from pathlib import Path
from typing import Any


def _is_backup(path: Path) -> bool:
    parent = path.parent.name.casefold()
    if parent.endswith("-backup") or "-backup-crashrecovery-" in parent:
        return True
    return path.suffix == ".bak"


def _discover_paths(patterns: list[str], *, recursive: bool) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        matches = glob.glob(str(Path(pattern).expanduser()), recursive=recursive)
        files.extend(p for p in (Path(m) for m in matches) if p.is_file() and not _is_backup(p))
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
