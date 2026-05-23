from pathlib import Path

from dicmerge.config import _default_config, _normalise, load_config


def test_default_config_structure():
    cfg = _default_config()
    assert "output" in cfg
    assert "sources" in cfg
    assert "write_back" in cfg
    assert "filters" in cfg


def test_default_config_sources():
    cfg = _default_config()
    assert "firefox" in cfg["sources"]
    assert "zed" in cfg["sources"]
    assert "kate" in cfg["sources"]


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
