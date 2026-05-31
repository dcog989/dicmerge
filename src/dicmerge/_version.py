import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PYPROJECT = PROJECT_ROOT / "pyproject.toml"
INIT = PROJECT_ROOT / "src" / "dicmerge" / "__init__.py"


def read_version() -> str:
    match = re.search(r'^version\s*=\s*"([^"]+)"', PYPROJECT.read_text(encoding="utf-8"), re.M)
    if not match:
        sys.exit("Could not find version in pyproject.toml")
    return match.group(1)


def parse_version(text: str) -> tuple[int, int, int]:
    parts = text.split(".")
    if len(parts) != 3:
        sys.exit(f"Invalid version format: {text!r}")
    a, b, c = (int(p) for p in parts)
    return a, b, c


def write_pyproject(version: str) -> None:
    content = PYPROJECT.read_text(encoding="utf-8")
    updated = re.sub(
        r'^(version\s*=\s*)"([^"]+)"',
        lambda m: f'{m.group(1)}"{version}"',
        content,
        count=1,
        flags=re.M,
    )
    PYPROJECT.write_text(updated, encoding="utf-8")


def write_init(version: str) -> None:
    content = INIT.read_text(encoding="utf-8")
    updated = re.sub(
        r'__version__\s*=\s*"[^"]+"',
        f'__version__ = "{version}"',
        content,
    )
    INIT.write_text(updated, encoding="utf-8")


def bump_version(current: str, part: str) -> str:
    major, minor, patch = parse_version(current)
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    sys.exit(f"Unknown bump type: {part!r}. Use major, minor, or patch.")


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else "minor"

    current = read_version()

    if raw in ("major", "minor", "patch"):
        new_version = bump_version(current, raw)
    else:
        parse_version(raw)
        new_version = raw

    write_pyproject(new_version)
    write_init(new_version)

    print(f"{current} → {new_version}")


if __name__ == "__main__":
    main()
