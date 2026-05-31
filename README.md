# dicmerge

Scan multiple applications for custom user dictionaries, merge them into a single wordlist, and optionally write new words back to each source.

## Install

```bash
uv pip list --outdated
uv tool install git+https://github.com/dcog989/dicmerge
# or locally
uv sync
```

## Usage

```bash
dicmerge                        # Merge and write combined wordlist
dicmerge --dry-run              # Preview only
dicmerge --write-back           # Merge + append new words to each source
dicmerge --list-sources         # Show discovered dictionary files
dicmerge --config custom.yaml   # Use alternate config
```

```bash
uv run version                  # Bump minor version
uv run version 1.0.0            # Set specific version
uv run version major            # Bump major
uv run version patch            # Bump patch
```

On first run, `~/.config/dicmerge/config.yaml` is created automatically with default settings.

## Sources

| Source | Path(s) |
|--------|---------|
| Firefox | `~/.mozilla/firefox/*/persdict.dat`, `~/.config/mozilla/firefox/*/persdict.dat` |
| Thunderbird | `~/.thunderbird/*/persdict.dat` |
| Obsidian | `~/Documents/Obsidian/*/*.dic`, `~/.config/obsidian/Custom Dictionary.txt` |
| LibreOffice | `~/.config/libreoffice/4/user/wordbook/*.dic` |
| KDE Sonnet | `~/.hunspell_*` |
| Vim/Neovim | `~/.vim/spell/*.add`, `~/.config/nvim/spell/*.add` |
| Gedit | `~/.local/share/gedit/spellcheck/words` |

Custom sources can be added in the config file under `custom_sources`.

## Output

Default: `~/dicmerge-output/combined.txt` (configurable in config).

## Write-back

`--write-back` appends words missing from each source to its dictionary file. Original files are backed up with a `.bak` suffix before modification.
