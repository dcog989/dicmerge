# AGENTS.md

## Project: dicmerge

Python script to scan, merge, and optionally write back custom user dictionaries from multiple Linux applications.

## Dev Environment

Linux CachyOS / KDE Plasma 6 + Firefox, Zed code editor, fish shell with Ghostty + Fresh editor. yay and bun package managers.

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

```sh
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

### File System Access

- Allowed: `/home/bubba/Projects/dicmerge/`
- Disallowed:

---

## General Guidelines

### Code Changes

- For non-trivial work, propose an approach and confirm before implementing.
- Keep modifications minimal and scoped; prefer incremental improvements over rewrites. Ask before architectural changes.
- Use explicit types and named constants (no magic numbers).
- Return explicit error types; do not suppress exceptions.
- Follow standard repository linting and formatting configs.
- Decompose files over 400 lines if they mix concerns.
- Use clear naming over comments; reserve comments for complex workarounds or non-obvious issues — why, not what.
- Never run git mutations (commit, push, reset, rebase, amend) unless explicitly instructed.
- Do not create documentation files unless explicitly requested.

### Verification

- Do not run test, lint, format, or type-check commands; the user builds, tests, and lints manually.
- Run them only when the user explicitly asks.

### Author Environment

- CachyOS, KDE Plasma 6, Wayland, Btrfs.
- fish shell, Ghostty terminal, Fresh TUI editor, yay package manager, bun npm manager, Firefox, and Zed code editor.

### Testing

- Do not create test files for trivial changes, or for behavior that is not reliably unit-testable in the test environment (e.g. UI layout/click mapping). Prefer no new files; only add a test when the logic is genuinely testable and worth guarding.

### Definition of Done

- Logic fully implemented.
- Existing docs updated if public interfaces changed.
- When required by the `Verification` rules, run the corresponding `Workflow` command.
- On completion of an update or fix, print a concise conventional commit message in a fenced code block.

### Communication Style

- Provide concise, actionable responses.
- Ask clarifying questions when requirements are ambiguous.
- Flag potential risks or edge cases proactively.
- Do not pretend to understand how the user feels.
- Never editorialise your answer. No "to be honest", "honestly", hedging, disclaimers, or meta-commentary — just answer.
