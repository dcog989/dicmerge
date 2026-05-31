from pathlib import Path

from dicmerge.scanner.base import Scanner
from dicmerge.util import read_text_with_fallback


class PlainTextScanner(Scanner):
    extension = ".txt"

    @staticmethod
    def format_output(words: list[str]) -> str:
        return "\n".join(words) + "\n"

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
