from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.scanner.firefox import FirefoxScanner
from dicmerge.scanner.plaintext import PlainTextScanner


def get_scanner(path: Path) -> Scanner:
    name = path.name
    if name == "persdict.dat":
        return FirefoxScanner()
    return PlainTextScanner()
