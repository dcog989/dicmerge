from pathlib import Path

from dicmerge.scanner.firefox import FirefoxScanner
from dicmerge.scanner.plaintext import PlainTextScanner


def test_plaintext_read(tmp_path: Path):
    f = tmp_path / "dict.txt"
    f.write_text("foo\nbar\nbaz\n", encoding="utf-8")
    scanner = PlainTextScanner()
    assert scanner.read(f) == ["foo", "bar", "baz"]


def test_plaintext_read_strips_whitespace(tmp_path: Path):
    f = tmp_path / "dict.txt"
    f.write_text("  foo  \n\tbar\t\n", encoding="utf-8")
    scanner = PlainTextScanner()
    assert scanner.read(f) == ["foo", "bar"]


def test_plaintext_read_skips_empty_lines(tmp_path: Path):
    f = tmp_path / "dict.txt"
    f.write_text("foo\n\n\nbar\n", encoding="utf-8")
    scanner = PlainTextScanner()
    assert scanner.read(f) == ["foo", "bar"]


def test_plaintext_read_skips_first_line_if_digits(tmp_path: Path):
    f = tmp_path / "dict.txt"
    f.write_text("12345\nfoo\nbar\n", encoding="utf-8")
    scanner = PlainTextScanner()
    assert scanner.read(f) == ["foo", "bar"]


def test_plaintext_read_keeps_non_digit_first_line(tmp_path: Path):
    f = tmp_path / "dict.txt"
    f.write_text("foo\nbar\nbaz\n", encoding="utf-8")
    scanner = PlainTextScanner()
    assert scanner.read(f) == ["foo", "bar", "baz"]


def test_plaintext_append(tmp_path: Path):
    f = tmp_path / "dict.txt"
    f.write_text("foo\n", encoding="utf-8")
    scanner = PlainTextScanner()
    scanner.append(f, ["bar", "baz"])
    assert f.read_text(encoding="utf-8") == "foo\nbar\nbaz\n"


def test_firefox_read(tmp_path: Path):
    f = tmp_path / "persdict.dat"
    f.write_text("foo\nbar\nbaz\n", encoding="utf-8")
    scanner = FirefoxScanner()
    assert scanner.read(f) == ["foo", "bar", "baz"]


def test_firefox_does_not_skip_digit_line(tmp_path: Path):
    f = tmp_path / "persdict.dat"
    f.write_text("12345\nfoo\n", encoding="utf-8")
    scanner = FirefoxScanner()
    assert scanner.read(f) == ["12345", "foo"]


def test_firefox_append(tmp_path: Path):
    f = tmp_path / "persdict.dat"
    f.write_text("foo\n", encoding="utf-8")
    scanner = FirefoxScanner()
    scanner.append(f, ["bar", "baz"])
    assert f.read_text(encoding="utf-8") == "foo\nbar\nbaz\n"
