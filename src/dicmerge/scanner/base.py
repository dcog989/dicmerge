from abc import ABC, abstractmethod
from pathlib import Path


class Scanner(ABC):
    extension: str = ""

    @abstractmethod
    def read(self, path: Path) -> list[str]: ...

    @abstractmethod
    def append(self, path: Path, words: list[str]) -> None: ...

    @staticmethod
    @abstractmethod
    def format_output(words: list[str]) -> str: ...
