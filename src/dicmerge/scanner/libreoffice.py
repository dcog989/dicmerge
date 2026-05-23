from pathlib import Path

from dicmerge.scanner.base import Scanner


class LibreOfficeScanner(Scanner):
    def read(self, path: Path) -> list[str]:
        lines = path.read_text(encoding="utf-8").splitlines()
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
        with path.open("a", encoding="utf-8") as f:
            for word in words:
                f.write(f"{word}\n")
