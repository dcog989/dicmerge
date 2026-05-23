import logging
from pathlib import Path

LOG_DIR = Path("~/.local/share/dicmerge").expanduser()


def _setup_logger() -> logging.Logger:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("dicmerge")
    logger.setLevel(logging.DEBUG)
    path = LOG_DIR / "debug.log"
    fh = logging.FileHandler(str(path), encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(fh)
    return logger


_logger: logging.Logger | None = None


def get_logger() -> logging.Logger:
    global _logger
    if _logger is None:
        _logger = _setup_logger()
    return _logger
