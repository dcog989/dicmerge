import re
import shutil
from pathlib import Path
from typing import Any

from dicmerge.config import discover_source_files, load_config
from dicmerge.dedup import deduplicate, missing_words
from dicmerge.exceptions import NoSourcesError, OutputError, WriteBackError
from dicmerge.log import get_logger
from dicmerge.output import write_words
from dicmerge.scanner import get_scanner
from dicmerge.scanner.base import Scanner
from dicmerge.scanner.plaintext import PlainTextScanner


def run(
    *,
    config_path: Path | None = None,
    write_back: bool = False,
    dry_run: bool = False,
) -> dict[str, Any]:
    config = load_config(config_path)
    discovered = discover_source_files(config)

    total_sources = sum(len(files) for files in discovered.values())
    if total_sources == 0:
        raise NoSourcesError("No enabled source files found")

    stats: dict[str, int] = {}
    all_words: list[str] = []
    per_file_words: dict[Path, list[str]] = {}
    used_scanner_types: set[type[Scanner]] = set()

    for name, files in discovered.items():
        total = 0
        for path in files:
            if path.suffix == ".rws":
                get_logger().warning("%s: %s: skipping binary format (.rws)", name, path.name)
                continue
            scanner = get_scanner(path)
            used_scanner_types.add(type(scanner))
            try:
                words = scanner.read(path)
                per_file_words[path] = words
                all_words.extend(words)
                total += len(words)
            except Exception as e:
                get_logger().warning("Failed to scan %s: %s", path, e)
        stats[name] = total

    filtered = _apply_filters(all_words, config["filters"])
    unique = deduplicate(filtered)

    if config["output"]["sort"]:
        unique = sorted(unique, key=str.casefold)

    output_path = Path(config["output"]["path"]).expanduser()

    if not dry_run:
        try:
            write_words(output_path, unique)
            written_extensions = {output_path.suffix}
            for scanner_cls in used_scanner_types:
                if scanner_cls is PlainTextScanner:
                    continue
                ext = scanner_cls.extension
                if ext in written_extensions:
                    continue
                written_extensions.add(ext)
                fmt_path = output_path.with_suffix(ext)
                fmt_path.write_text(scanner_cls.format_output(unique), encoding="utf-8")
        except (OSError, PermissionError) as e:
            raise OutputError(f"Cannot write output to {output_path}: {e}") from e

    write_back_stats: dict[str, list[tuple[str, int]]] = {}

    if write_back:
        for name, files in discovered.items():
            for path in files:
                if path.suffix == ".rws":
                    get_logger().warning(
                        "%s: %s: skipping write-back for binary format (.rws)",
                        name,
                        path.name,
                    )
                    continue
                existing = per_file_words.get(path)
                if existing is None:
                    try:
                        existing = get_scanner(path).read(path)
                    except Exception as e:
                        get_logger().warning("Failed to re-read %s for write-back: %s", path, e)
                        continue
                new = missing_words(unique, existing)
                if not new:
                    continue
                if not dry_run:
                    scanner = get_scanner(path)
                    if config["write_back"]["create_backup"]:
                        backup = path.with_suffix(
                            path.suffix + config["write_back"]["backup_suffix"]
                        )
                        if not backup.exists():
                            shutil.copy2(path, backup)
                    try:
                        scanner.append(path, new)
                    except (OSError, PermissionError) as e:
                        raise WriteBackError(f"Cannot write back to {path}: {e}") from e
                write_back_stats.setdefault(name, []).append((path.name, len(new)))

    return {
        "source_stats": stats,
        "total_raw": len(all_words),
        "total_filtered": len(filtered),
        "total_unique": len(unique),
        "write_back_stats": write_back_stats,
        "output_path": str(output_path),
    }


def _apply_filters(words: list[str], filters: dict[str, Any]) -> list[str]:
    min_len = filters.get("min_length", 2)
    max_len = filters.get("max_length", 64)
    allow_numbers = filters.get("allow_numbers", False)
    exclude_patterns = filters.get("exclude_patterns", [])

    compiled = [re.compile(p) for p in exclude_patterns]

    result: list[str] = []
    for w in words:
        if len(w) < min_len or len(w) > max_len:
            continue
        if not allow_numbers and any(c.isdigit() for c in w):
            continue
        if any(p.search(w) for p in compiled):
            continue
        result.append(w)
    return result
