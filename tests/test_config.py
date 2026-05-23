from pathlib import Path

from dicmerge.config import _default_config, _normalise, discover_source_files, load_config


def test_default_config_structure():
    cfg = _default_config()
    assert "output" in cfg
    assert "sources" in cfg
    assert "write_back" in cfg
    assert "filters" in cfg


def test_default_config_sources():
    cfg = _default_config()
    assert "firefox" in cfg["sources"]
    assert "obsidian" in cfg["sources"]
    assert "kde_sonnet" in cfg["sources"]


def test_load_config_writes_defaults_when_missing(tmp_path: Path):
    config_path = tmp_path / "dicmerge" / "config.yaml"
    cfg = load_config(config_path)
    assert cfg["output"]["path"] == "~/dicmerge-output/combined.txt"
    assert config_path.exists()


def test_normalise_merges_partial_config():
    raw = {"output": {"sort": False}}
    cfg = _normalise(raw)
    assert cfg["output"]["sort"] is False
    assert cfg["output"]["encoding"] == "utf-8"


def test_normalise_overrides_sources():
    raw = {"sources": {"firefox": {"enabled": False}}}
    cfg = _normalise(raw)
    assert cfg["sources"]["firefox"]["enabled"] is False


def test_discover_source_files_finds_matching(tmp_path: Path):
    (tmp_path / "firefox" / "default" / "persdict.dat").parent.mkdir(parents=True)
    (tmp_path / "firefox" / "default" / "persdict.dat").write_text("foo\n", encoding="utf-8")

    cfg = _default_config()
    cfg["sources"]["firefox"]["paths"] = [str(tmp_path / "firefox/*/persdict.dat")]

    result = discover_source_files(cfg)
    assert len(result["firefox"]) == 1
    assert result["firefox"][0].name == "persdict.dat"


def test_discover_source_files_skips_disabled(tmp_path: Path):
    (tmp_path / "persdict.dat").write_text("foo\n", encoding="utf-8")

    cfg = _default_config()
    cfg["sources"]["firefox"]["paths"] = [str(tmp_path / "persdict.dat")]
    cfg["sources"]["firefox"]["enabled"] = False

    result = discover_source_files(cfg)
    assert result.get("firefox", []) == []


def test_discover_source_files_skips_backup_paths(tmp_path: Path):
    (tmp_path / "dir-backup" / "persdict.dat").parent.mkdir(parents=True)
    (tmp_path / "dir-backup" / "persdict.dat").write_text("foo\n", encoding="utf-8")

    cfg = _default_config()
    cfg["sources"]["firefox"]["paths"] = [str(tmp_path / "*/persdict.dat")]

    result = discover_source_files(cfg)
    assert result.get("firefox", []) == []


def test_discover_source_files_custom_sources(tmp_path: Path):
    (tmp_path / "my_words.txt").write_text("foo\n", encoding="utf-8")

    cfg = _default_config()
    cfg["custom_sources"] = [
        {"name": "custom", "paths": [str(tmp_path / "my_words.txt")], "enabled": True},
    ]

    result = discover_source_files(cfg)
    assert "custom" in result
    assert len(result["custom"]) == 1


def test_discover_source_files_respects_recursive(tmp_path: Path):
    (tmp_path / "a" / "b" / "words.dic").parent.mkdir(parents=True)
    (tmp_path / "a" / "b" / "words.dic").write_text("foo\n", encoding="utf-8")

    cfg = _default_config()
    cfg["sources"]["obsidian"]["paths"] = [str(tmp_path / "a/**/*.dic")]
    cfg["sources"]["obsidian"]["recursive"] = True

    result = discover_source_files(cfg)
    assert len(result["obsidian"]) == 1
