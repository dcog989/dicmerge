from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.util import read_text_with_fallback


class FirefoxScanner(Scanner):
    def read(self, path: Path) -> list[str]:
        words: list[str] = []
        for line in read_text_with_fallback(path).splitlines():
            word = line.strip()
            if word:
                words.append(word)
        return words

    def append(self, path: Path, words: list[str]) -> None:
        with path.open("a", encoding="utf-8") as f:
            for word in words:
                f.write(f"{word}\n")
