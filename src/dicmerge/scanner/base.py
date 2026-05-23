from abc import ABC, abstractmethod
from pathlib import Path


class Scanner(ABC):
    @abstractmethod
    def read(self, path: Path) -> list[str]: ...

    @abstractmethod
    def append(self, path: Path, words: list[str]) -> None: ...
