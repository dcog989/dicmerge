from pathlib import Path
from typing import Any

import yaml

from dicmerge.util import expand_paths

DEFAULT_CONFIG_PATH = Path("~/.config/dicmerge/config.yaml").expanduser()


def load_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or DEFAULT_CONFIG_PATH

    if not config_path.exists():
        return _default_config()

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"Config must be a mapping, got {type(raw).__name__}"
        raise ValueError(msg)

    return _normalise(raw)


def _default_config() -> dict[str, Any]:
    return {
        "output": {
            "path": "~/.local/share/dicmerge/combined.txt",
            "create_hunspell_dic": True,
            "encoding": "utf-8",
            "sort": True,
        },
        "sources": {
            "firefox": {
                "enabled": True,
                "paths": [
                    "~/.mozilla/firefox/*/persdict.dat",
                    "~/.var/app/org.mozilla.firefox/.mozilla/firefox/*/persdict.dat",
                ],
            },
            "obsidian": {
                "enabled": True,
                "paths": [
                    "~/Documents/Obsidian/*/*.dic",
                    "~/.config/obsidian/custom-dict.txt",
                ],
                "recursive": True,
            },
            "zed": {
                "enabled": True,
                "paths": ["~/.config/zed/dictionary.txt"],
            },
            "libreoffice": {
                "enabled": True,
                "paths": ["~/.config/libreoffice/4/user/wordbook/*.dic"],
            },
            "kate": {
                "enabled": True,
                "paths": [
                    "~/.local/share/kate/dictionary.txt",
                    "~/.config/kate/spellcheck/*.txt",
                ],
            },
            "kde_sonnet": {
                "enabled": True,
                "paths": ["~/.config/enchant/hunspell/*.dic"],
            },
        },
        "custom_sources": [
            {"name": "custom", "paths": ["~/my_words.txt"], "enabled": False},
        ],
        "write_back": {
            "enabled": False,
            "create_backup": True,
            "backup_suffix": ".bak",
        },
        "filters": {
            "min_length": 2,
            "max_length": 64,
            "allow_numbers": False,
            "exclude_patterns": ["^[0-9]+$"],
        },
    }


def _normalise(raw: dict[str, Any]) -> dict[str, Any]:
    config = _default_config()

    if "output" in raw:
        config["output"].update(raw["output"])
    if "sources" in raw:
        config["sources"].update(raw["sources"])
    if "custom_sources" in raw:
        config["custom_sources"] = raw["custom_sources"]
    if "write_back" in raw:
        config["write_back"].update(raw["write_back"])
    if "filters" in raw:
        config["filters"].update(raw["filters"])

    return config


def discover_source_files(config: dict[str, Any]) -> dict[str, list[Path]]:
    discovered: dict[str, list[Path]] = {}

    for name, source in config["sources"].items():
        if not source.get("enabled", True):
            continue
        recursive = source.get("recursive", False)
        files: list[Path] = []
        for pattern in expand_paths(source["paths"]):
            if recursive:
                files.extend(sorted(pattern.rglob("*")))
            else:
                files.extend(sorted(pattern.glob("*")))
        discovered[name] = sorted(set(files))

    custom = config.get("custom_sources", [])
    for entry in custom:
        if not entry.get("enabled", False):
            continue
        files = []
        for pattern in expand_paths(entry["paths"]):
            files.extend(sorted(Path(pattern).parent.glob(Path(pattern).name)))
        discovered[entry["name"]] = sorted(set(files))

    return discovered
