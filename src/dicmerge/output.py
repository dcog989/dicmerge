import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile


def write_words(path: Path, words: list[str], encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding=encoding,
            dir=path.parent,
            prefix=".dicmerge_",
            delete=False,
        ) as tmp:
            tmp_path = Path(tmp.name)
            for word in words:
                tmp.write(f"{word}\n")
            tmp.flush()
        if tmp_path is None:
            raise RuntimeError("temporary file was not created")
        shutil.move(tmp_path, path)
    except Exception:
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)
        raise
