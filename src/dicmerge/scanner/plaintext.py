from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.util import read_text_with_fallback


class PlainTextScanner(Scanner):
    def read(self, path: Path) -> list[str]:
        words: list[str] = []
        for lineno, line in enumerate(read_text_with_fallback(path).splitlines(), 1):
            word = line.strip()
            if not word:
                continue
            if lineno == 1 and word.isdigit():
                continue
            words.append(word)
        return words

    def append(self, path: Path, words: list[str]) -> None:
        with path.open("a", encoding="utf-8") as f:
            for word in words:
                f.write(f"{word}\n")
