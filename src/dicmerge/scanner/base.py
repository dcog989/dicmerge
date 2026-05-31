from abc import ABC, abstractmethod
from pathlib import Path


class Scanner(ABC):
    extension: str = ""

    @abstractmethod
    def read(self, path: Path) -> list[str]: ...

    @staticmethod
    @abstractmethod
    def format_output(words: list[str]) -> str: ...
