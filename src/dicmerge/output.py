import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile


def write_words(path: Path, words: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=".dicmerge_",
        delete=False,
    )
    try:
        for word in words:
            tmp.write(f"{word}\n")
        tmp.flush()
        tmp.close()
        tmp_path = Path(tmp.name)
        shutil.move(tmp_path, path)
    except Exception:
        Path(tmp.name).unlink(missing_ok=True)
        raise
