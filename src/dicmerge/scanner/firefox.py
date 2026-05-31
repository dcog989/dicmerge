from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.util import ensure_trailing_newline, read_text_with_fallback


class FirefoxScanner(Scanner):
    extension = ".dat"

    @staticmethod
    def format_output(words: list[str]) -> str:
        return "\n".join(words) + "\n"

    def read(self, path: Path) -> list[str]:
        words: list[str] = []
        for line in read_text_with_fallback(path).splitlines():
            word = line.strip()
            if word:
                words.append(word)
        return words

    def append(self, path: Path, words: list[str]) -> None:
        ensure_trailing_newline(path)
        with path.open("a", encoding="utf-8") as f:
            for word in words:
                f.write(f"{word}\n")
