# dicmerge

Scan multiple applications for custom user dictionaries, merge them into a single wordlist, and optionally write new words back to each source.

## Install

```sh
uv pip list --outdated                       # check outdated
uv tree --outdated                           # check outdated in tree
uv sync --upgrade                            # bump all deps
uv lock --upgrade-package <name> && uv sync  # bump one package
uv run ruff format .                         # auto-format

uv tool install git+https://github.com/dcog989/dicmerge
uv sync
```

```sh
cog bump --auto             # Auto-detect bump from commit types (feat=minor, fix=patch)
cog bump --minor            # Explicit minor bump
cog bump --patch            # Explicit patch bump
cog bump --version 1.0.0    # Set a specific version
cog bump --dry-run --auto   # Preview the next version without tagging
```

Versions are managed by cocogitto from conventional commits. `cog bump` updates
`pyproject.toml` and `__init__.py`, appends to `CHANGELOG.md`, and tags the release.

## Usage

```sh
# from the project root
uv run dicmerge                      # Merge and write combined wordlist
uv run dicmerge --dry-run            # Preview only
uv run dicmerge --write-back         # Overwrite each source with the merged wordlist
uv run dicmerge --list-sources       # Show discovered dictionary files
uv run dicmerge --config custom.yaml # Use alternate config
```

On first run, `~/.config/dicmerge/config.yaml` is created automatically with default settings.

## Sources

| Source         | Path(s) |
|----------------|---------|
| Firefox        | `~/.mozilla/firefox/*/persdict.dat`, `~/.config/mozilla/firefox/*/persdict.dat`, `~/.var/app/org.mozilla.firefox/.mozilla/firefox/*/persdict.dat` |
| Thunderbird    | `~/.thunderbird/*/persdict.dat` |
| Obsidian       | `~/Documents/Obsidian/*/*.dic`, `~/.config/obsidian/Custom Dictionary.txt` |
| LibreOffice    | `~/.config/libreoffice/4/user/wordbook/*.dic` |
| KDE Sonnet     | `~/.hunspell_*` |
| Vim/Neovim     | `~/.vim/spell/*.add`, `~/.config/nvim/spell/*.add` |
| Gedit          | `~/.local/share/gedit/spellcheck/words` |

Custom sources can be added in the config file under `custom_sources`.

## Output

Default: `~/dicmerge-output/combined.txt` (configurable in config).

## Write-back

`--write-back` overwrites each source dictionary with the merged wordlist. Original files are backed up with a `.bak` suffix before modification.

Write-back also requires `write_back.enabled: true` in the config (the default); set it to `false` to disable write-back even when `--write-back` is passed.
