from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.util import read_text_with_fallback


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
