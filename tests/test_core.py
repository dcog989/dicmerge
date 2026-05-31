from pathlib import Path

import yaml

from dicmerge.core import _apply_filters, run
from dicmerge.exceptions import NoSourcesError


def test_apply_filters_min_length():
    words = ["a", "ab", "abc"]
    result = _apply_filters(words, {"min_length": 2})
    assert result == ["ab", "abc"]


def test_apply_filters_max_length():
    words = ["a", "ab", "abc", "abcd"]
    result = _apply_filters(words, {"min_length": 1, "max_length": 3})
    assert result == ["a", "ab", "abc"]


def test_apply_filters_numbers_not_allowed():
    words = ["foo", "bar123", "baz"]
    result = _apply_filters(words, {"allow_numbers": False})
    assert result == ["foo", "baz"]


def test_apply_filters_numbers_allowed():
    words = ["foo", "bar123", "baz"]
    result = _apply_filters(words, {"allow_numbers": True})
    assert result == ["foo", "bar123", "baz"]


def test_apply_filters_exclude_pattern():
    words = ["foo", "bar", "baz123", "qux"]
    result = _apply_filters(
        words,
        {"exclude_patterns": [r"\d"]},
    )
    assert result == ["foo", "bar", "qux"]


def test_apply_filters_combined():
    words = ["a", "foo", "bar123", "toolongword", "baz", "42"]
    result = _apply_filters(
        words,
        {
            "min_length": 2,
            "max_length": 5,
            "allow_numbers": False,
            "exclude_patterns": [],
        },
    )
    assert result == ["foo", "baz"]


def _make_config(tmp_path: Path) -> tuple[Path, Path, Path]:
    src = tmp_path / "sources"
    out = tmp_path / "output"

    cfg = {
        "output": {
            "path": str(out / "combined.txt"),
            "sort": False,
            "encoding": "utf-8",
        },
        "sources": {
            "firefox": {
                "enabled": True,
                "paths": [str(src / "firefox/*/persdict.dat")],
            },
            "obsidian": {"enabled": False, "paths": []},
            "libreoffice": {"enabled": False, "paths": []},
            "kde_sonnet": {"enabled": False, "paths": []},
            "thunderbird": {"enabled": False, "paths": []},
            "vim": {"enabled": False, "paths": []},
            "gedit": {"enabled": False, "paths": []},
        },
        "custom_sources": [],
        "write_back": {
            "enabled": False,
            "create_backup": True,
            "backup_suffix": ".bak",
        },
        "filters": {
            "min_length": 1,
            "max_length": 100,
            "allow_numbers": True,
            "exclude_patterns": [],
        },
    }
    config_path = tmp_path / "config.yaml"
    config_path.write_text(yaml.dump(cfg), encoding="utf-8")
    return config_path, src, out


def test_run_basic(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)
    d = src / "firefox" / "default"
    d.mkdir(parents=True)
    (d / "persdict.dat").write_text("foo\nbar\nbaz\n", encoding="utf-8")

    result = run(config_path=config_path)

    assert result["source_stats"]["firefox"] == 3
    assert result["total_unique"] == 3
    assert (out / "combined.txt").exists()
    assert (out / "combined.txt").read_text(encoding="utf-8") == "foo\nbar\nbaz\n"


def test_run_merges_multiple_sources(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)
    (src / "firefox" / "default").mkdir(parents=True)
    (src / "firefox" / "default" / "persdict.dat").write_text("foo\nbar\n", encoding="utf-8")

    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    cfg["sources"]["libreoffice"] = {
        "enabled": True,
        "paths": [str(src / "libreoffice/*.dic")],
    }
    config_path.write_text(yaml.dump(cfg), encoding="utf-8")
    (src / "libreoffice").mkdir(parents=True)
    (src / "libreoffice" / "custom.dic").write_text(
        "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \nbar\nbaz\n",
        encoding="utf-8",
    )

    result = run(config_path=config_path)

    assert result["source_stats"]["firefox"] == 2
    assert result["source_stats"]["libreoffice"] == 2
    assert result["total_unique"] == 3


def test_run_deduplicates(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)
    d = src / "firefox" / "default"
    d.mkdir(parents=True)
    (d / "persdict.dat").write_text("foo\nbar\nfoo\nBAR\n", encoding="utf-8")

    result = run(config_path=config_path)

    assert result["total_unique"] == 2
    assert result["total_raw"] == 4


def test_run_sorts_output(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)
    d = src / "firefox" / "default"
    d.mkdir(parents=True)
    (d / "persdict.dat").write_text("gamma\nAlpha\nbeta\n", encoding="utf-8")

    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    cfg["output"]["sort"] = True
    config_path.write_text(yaml.dump(cfg), encoding="utf-8")

    result = run(config_path=config_path)

    assert result["total_unique"] == 3
    assert (out / "combined.txt").read_text(encoding="utf-8") == "Alpha\nbeta\ngamma\n"


def test_run_dry_run_does_not_write(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)
    d = src / "firefox" / "default"
    d.mkdir(parents=True)
    (d / "persdict.dat").write_text("foo\nbar\n", encoding="utf-8")

    result = run(config_path=config_path, dry_run=True)

    assert result["total_unique"] == 2
    assert not (out / "combined.txt").exists()


def test_run_no_sources_raises_error(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    cfg["sources"]["firefox"]["paths"] = [str(src / "nonexistent/*.dat")]
    config_path.write_text(yaml.dump(cfg), encoding="utf-8")

    import pytest

    with pytest.raises(NoSourcesError):
        run(config_path=config_path)


def test_run_write_back_appends_new_words(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)

    firefox_dir = src / "firefox" / "default"
    firefox_dir.mkdir(parents=True)
    ff_file = firefox_dir / "persdict.dat"
    ff_file.write_text("foo\n", encoding="utf-8")

    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    cfg["sources"]["libreoffice"] = {
        "enabled": True,
        "paths": [str(src / "libreoffice/*.dic")],
    }
    cfg["write_back"]["create_backup"] = False
    config_path.write_text(yaml.dump(cfg), encoding="utf-8")

    lo_dir = src / "libreoffice"
    lo_dir.mkdir(parents=True)
    lo_file = lo_dir / "custom.dic"
    lo_file.write_text(
        "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \nbar\nbaz\n",
        encoding="utf-8",
    )

    result = run(config_path=config_path, write_back=True)

    assert result["write_back_stats"]["firefox"] == [("persdict.dat", 2)]
    assert result["write_back_stats"]["libreoffice"] == [("custom.dic", 1)]
    assert ff_file.read_text(encoding="utf-8") == "foo\nbar\nbaz\n"
    assert lo_file.read_text(encoding="utf-8") == (
        "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \nbar\nbaz\nfoo\n"
    )


def test_run_write_back_creates_backup(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)

    firefox_dir = src / "firefox" / "default"
    firefox_dir.mkdir(parents=True)
    ff_file = firefox_dir / "persdict.dat"
    ff_file.write_text("foo\n", encoding="utf-8")

    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    cfg["sources"]["libreoffice"] = {
        "enabled": True,
        "paths": [str(src / "libreoffice/*.dic")],
    }
    cfg["write_back"]["create_backup"] = True
    config_path.write_text(yaml.dump(cfg), encoding="utf-8")

    lo_dir = src / "libreoffice"
    lo_dir.mkdir(parents=True)
    lo_file = lo_dir / "custom.dic"
    lo_file.write_text(
        "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \nbar\n",
        encoding="utf-8",
    )

    run(config_path=config_path, write_back=True)

    assert (firefox_dir / "persdict.dat.bak").exists()
    assert (lo_dir / "custom.dic.bak").exists()
    assert (firefox_dir / "persdict.dat.bak").read_text(encoding="utf-8") == "foo\n"


def test_run_writes_discovered_formats(tmp_path: Path):
    config_path, src, out = _make_config(tmp_path)

    firefox_dir = src / "firefox" / "default"
    firefox_dir.mkdir(parents=True)
    (firefox_dir / "persdict.dat").write_text("foo\nbar\n", encoding="utf-8")

    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    cfg["sources"]["libreoffice"] = {
        "enabled": True,
        "paths": [str(src / "libreoffice/*.dic")],
    }
    config_path.write_text(yaml.dump(cfg), encoding="utf-8")

    lo_dir = src / "libreoffice"
    lo_dir.mkdir(parents=True)
    (lo_dir / "custom.dic").write_text(
        "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \nbaz\n",
        encoding="utf-8",
    )

    run(config_path=config_path)

    assert (out / "combined.txt").read_text(encoding="utf-8") == "foo\nbar\nbaz\n"
    assert (out / "combined.dat").exists()
    assert (out / "combined.dat").read_text(encoding="utf-8") == "foo\nbar\nbaz\n"
    assert (out / "combined.dic").exists()
    assert (out / "combined.dic").read_text(encoding="utf-8") == (
        "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \nfoo\nbar\nbaz\n"
    )
