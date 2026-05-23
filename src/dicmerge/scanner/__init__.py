from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.scanner.firefox import FirefoxScanner
from dicmerge.scanner.libreoffice import LibreOfficeScanner
from dicmerge.scanner.plaintext import PlainTextScanner


def _is_libreoffice(path: Path) -> bool:
    name = path.name
    if not name.endswith(".dic"):
        return False
    if not path.exists():
        return True
    try:
        first = path.read_text(encoding="utf-8").splitlines()[0].strip()
        return first == "OOoUserDict1"
    except IndexError, OSError:
        return False


def get_scanner(path: Path) -> Scanner:
    name = path.name
    if name == "persdict.dat":
        return FirefoxScanner()
    if _is_libreoffice(path):
        return LibreOfficeScanner()
    return PlainTextScanner()
