from pathlib import Path

from dicmerge.scanner.base import Scanner


class FirefoxScanner(Scanner):
    def read(self, path: Path) -> list[str]:
        words: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            word = line.strip()
            if word:
                words.append(word)
        return words

    def append(self, path: Path, words: list[str]) -> None:
        with path.open("a", encoding="utf-8") as f:
            for word in words:
                f.write(f"{word}\n")
