import glob
from pathlib import Path
from typing import Any

import yaml

from dicmerge.exceptions import ConfigError
from dicmerge.util import expand_paths

DEFAULT_CONFIG_PATH = Path("~/.config/dicmerge/config.yaml").expanduser()


def load_config(path: Path | None = None) -> dict[str, Any]:
    config_path = path or DEFAULT_CONFIG_PATH

    if not config_path.exists():
        default = _default_config()
        _write_config(config_path, default)
        return default

    try:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise ConfigError(f"Failed to parse config: {e}") from e

    if not isinstance(raw, dict):
        msg = f"Config must be a mapping, got {type(raw).__name__}"
        raise ConfigError(msg)

    return _normalise(raw)


def _default_config() -> dict[str, Any]:
    return {
        "output": {
            "path": "~/dicmerge-output/combined.txt",
            "create_hunspell_dic": True,
            "encoding": "utf-8",
            "sort": True,
        },
        "sources": {
            "firefox": {
                "enabled": True,
                "paths": [
                    "~/.mozilla/firefox/*/persdict.dat",
                    "~/.config/mozilla/firefox/*/persdict.dat",
                    "~/.var/app/org.mozilla.firefox/.mozilla/firefox/*/persdict.dat",
                ],
            },
            "obsidian": {
                "enabled": True,
                "paths": [
                    "~/Documents/Obsidian/*/*.dic",
                    "~/.config/obsidian/Custom Dictionary.txt",
                ],
                "recursive": True,
            },
            "libreoffice": {
                "enabled": True,
                "paths": ["~/.config/libreoffice/4/user/wordbook/*.dic"],
            },
            "kde_sonnet": {
                "enabled": True,
                "paths": ["~/.hunspell_*"],
            },
            "thunderbird": {
                "enabled": True,
                "paths": ["~/.thunderbird/*/persdict.dat"],
            },
            "vim": {
                "enabled": True,
                "paths": [
                    "~/.vim/spell/*.add",
                    "~/.config/nvim/spell/*.add",
                ],
            },
            "gedit": {
                "enabled": True,
                "paths": ["~/.local/share/gedit/spellcheck/words"],
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


def _write_config(path: Path, config: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(config, default_flow_style=False), encoding="utf-8")


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


_BACKUP_MARKERS = {"-backup", "-back-ovfs"}


def _is_backup(path: Path) -> bool:
    return any(part.endswith(m) for part in path.parts for m in _BACKUP_MARKERS)


def discover_source_files(config: dict[str, Any]) -> dict[str, list[Path]]:
    discovered: dict[str, list[Path]] = {}

    for name, source in config["sources"].items():
        if not source.get("enabled", True):
            continue
        recursive = source.get("recursive", False)
        files: list[Path] = []
        for pattern in expand_paths(source["paths"]):
            matches = glob.glob(str(pattern), recursive=recursive)
            files.extend(sorted(Path(m) for m in matches if not _is_backup(Path(m))))
        discovered[name] = sorted(set(files))

    custom = config.get("custom_sources", [])
    for entry in custom:
        if not entry.get("enabled", False):
            continue
        custom_files: list[Path] = []
        for pattern in expand_paths(entry["paths"]):
            matches = glob.glob(str(pattern))
            custom_files.extend(sorted(Path(m) for m in matches))
        discovered[entry["name"]] = sorted(set(custom_files))

    return discovered
