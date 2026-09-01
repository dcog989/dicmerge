from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.util import read_text_with_fallback

_LO_HEADER = "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \n"


class LibreOfficeScanner(Scanner):
    extension = ".dic"
    skip_header = len(_LO_HEADER.splitlines())

    @classmethod
    def matches(cls, path: Path) -> bool:
        if not path.name.endswith(".dic"):
            return False
        if not path.exists():
            return True
        try:
            first = read_text_with_fallback(path).splitlines()[0].strip()
            return first == "OOoUserDict1"
        except IndexError, OSError:
            return False

    @staticmethod
    def format_output(words: list[str]) -> str:
        return _LO_HEADER + "\n".join(words) + "\n"
