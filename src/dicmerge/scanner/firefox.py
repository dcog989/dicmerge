from pathlib import Path

from dicmerge.scanner.plaintext import PlainTextScanner


class FirefoxScanner(PlainTextScanner):
    extension = ".dat"

    @classmethod
    def matches(cls, path: Path) -> bool:
        return path.name == "persdict.dat"
