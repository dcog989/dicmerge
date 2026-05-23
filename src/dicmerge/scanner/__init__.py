from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.scanner.firefox import FirefoxScanner
from dicmerge.scanner.libreoffice import LibreOfficeScanner
from dicmerge.scanner.plaintext import PlainTextScanner
from dicmerge.util import read_text_with_fallback


def _is_libreoffice(path: Path) -> bool:
    name = path.name
    if not name.endswith(".dic"):
        return False
    if not path.exists():
        return True
    try:
        first = read_text_with_fallback(path).splitlines()[0].strip()
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
