# dicmerge

Scan multiple applications for custom user dictionaries, merge them into a single wordlist, and optionally write new words back to each source.

## Install

```sh
uv tool install git+https://github.com/dcog989/dicmerge
```

## Usage

```sh
dicmerge                      # Merge and write ~/dicmerge-output/combined.txt
dicmerge --dry-run            # Preview only, no files written
dicmerge --write-back         # Overwrite each source with the merged wordlist
dicmerge --list-sources       # Show discovered dictionary files
dicmerge --version            # Show version
dicmerge --config custom.yaml # Use an alternate config file
```

On first run, `~/.config/dicmerge/config.yaml` is created automatically with default settings.

## Sources

| Source      | Path(s) |
|-------------|---------|
| Firefox     | `~/.mozilla/firefox/*/persdict.dat`, `~/.config/mozilla/firefox/*/persdict.dat`, `~/.var/app/org.mozilla.firefox/.mozilla/firefox/*/persdict.dat` |
| Thunderbird | `~/.thunderbird/*/persdict.dat` |
| Obsidian    | `~/Documents/Obsidian/*/*.dic`, `~/.config/obsidian/Custom Dictionary.txt` |
| LibreOffice | `~/.config/libreoffice/4/user/wordbook/*.dic` |
| KDE Sonnet  | `~/.hunspell_<LANG>` (falls back to `~/.hunspell_*`) |
| Vim/Neovim  | `~/.vim/spell/*.add`, `~/.config/nvim/spell/*.add` |
| Gedit       | `~/.local/share/gedit/spellcheck/words` |

Custom sources can be added under `custom_sources` in the config file.

## Output

Written to `~/dicmerge-output/combined.txt` (configurable under `output`): one word per line, deduplicated case-insensitively, sorted, UTF-8.

## Write-back

`--write-back` overwrites each source dictionary with the merged wordlist. Each original file is backed up with a `.bak` suffix before it is modified.

---

## Development

```sh
uv sync                  # Create/refresh the dev environment
uv run dicmerge          # Run from source
uv run ruff format .     # Format
uv run pytest            # Test
uv clean                 # clean build artifacts
```

## Releasing

Versions are managed by Cocogitto from conventional commits. `cog bump` updates `pyproject.toml` and `__init__.py`, appends to `CHANGELOG.md`, and tags the release.

```sh
cog bump --auto             # Auto-detect from commit types (feat=minor, fix=patch)
cog bump --version 1.0.0    # Set a specific version
cog bump --dry-run --auto   # Preview the next version without tagging
```

## License

[MIT License](LICENSE).
