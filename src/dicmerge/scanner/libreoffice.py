from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.util import ensure_trailing_newline, read_text_with_fallback

_LO_HEADER = "OOoUserDict1\nlang: en-US\ntype: positive\nreplacement: \n"


class LibreOfficeScanner(Scanner):
    extension = ".dic"

    @staticmethod
    def format_output(words: list[str]) -> str:
        return _LO_HEADER + "\n".join(words) + "\n"

    def read(self, path: Path) -> list[str]:
        lines = read_text_with_fallback(path).splitlines()
        words: list[str] = []
        for lineno, line in enumerate(lines, 1):
            word = line.strip()
            if not word:
                continue
            if lineno <= 4:
                continue
            words.append(word)
        return words

    def append(self, path: Path, words: list[str]) -> None:
        ensure_trailing_newline(path)
        with path.open("a", encoding="utf-8") as f:
            for word in words:
                f.write(f"{word}\n")
