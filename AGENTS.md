# AGENTS.md

## Project: dicmerge

Python script to scan, merge, and optionally write back custom user dictionaries from multiple Linux applications.

## Dev Environment

Linux CachyOS, Limine boot loader, KDE Plasma 6, Wayland, Btrfs. Firefox, Kate text editor, Zed code editor, fish shell with Ghostty + Fresh editor. paru and bun package managers. All software is updated as of today.

### Tech Stack

| Tool | Version |
|------|---------|
| Python | 3.14 |
| Package manager | uv |
| Build backend | hatchling |
| Linter + formatter | ruff |
| Type checker | mypy |
| Test framework | pytest |
| Git hooks | lefthook |

### Dependencies

- **Runtime**: PyYAML, Rich
- **Stdlib**: `pathlib`, `glob`, `re`, `argparse`, `shutil`, `logging`, `tempfile`
- **Dev**: ruff, mypy, pytest

### Key Files

| Path | Purpose |
|------|---------|
| `/usr/local/bin/dicmerge` | Main script |
| `~/.config/dicmerge/config.yaml` | User configuration |
| `~/dicmerge-output/combined.txt` | Merged output |
| `~/.local/share/dicmerge/debug.log` | Debug log |

### Core Behaviors

- Scan enabled sources from config (Firefox, Obsidian, LibreOffice, KDE Sonnet, Thunderbird, Vim, Gedit)
- Deduplicate case-insensitively (first occurrence wins)
- Output plain text, one word per line, UTF-8
- Write-back appends missing words only, creates `.bak` backup first
- Manual execution only, no daemon or scheduler

### Command Line

```bash
dicmerge                      # Write to combined.txt
dicmerge --write-back         # Write new words back to sources
dicmerge --dry-run            # Preview only
dicmerge --list-sources       # Show discovered paths
```

### Exit Codes

0=Success, 1=Generic error, 2=Config error, 3=No sources, 4=Write-back failed, 5=Output unwritable

### Development Priorities

1. Core scanner + plain text handler
2. Firefox, Obsidian, LibreOffice
3. Obsidian, LibreOffice
4. KDE Sonnet discovery
5. Write-back with backup
6. Custom source support

### Constraints

- No binary dictionary support (skip `.rws`)
- No concurrency handling (manual execution only)
- Linux only, CachyOS/Arch paths assumed

### Coding Principles

- Use current coding standards and patterns (Svelte 5 runes, modern TS)
- KISS, Occam's razor, DRY, YAGNI
- Optimize for actual and perceived performance
- Self-documenting code via clear naming
- Comments only for workarounds/complex logic - do NOT add comments as running dev commentary.
- No magic numbers
- Split files of 400+ lines in to separate distinct functions
- **Do NOT create docs files** (summary, reference, testing, etc.) unless explicitly requested

### File System Access

#### Allowed Directories

- `/home/bubba/Projects/dicmerge/`

#### Disallowed

- `.context/`, `.assets/`, `node_modules/`, `.repomix/`
- `repomix.config.json`, `bun.lock`, `.repomixignore`
