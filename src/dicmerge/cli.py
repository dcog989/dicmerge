import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from dicmerge import __version__
from dicmerge.config import DEFAULT_CONFIG_PATH
from dicmerge.core import run
from dicmerge.exceptions import ConfigError, DicmergeError

console = Console()

_SHOW_CONFIG = object()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="dicmerge",
        description="Scan, merge, and write back custom user dictionaries",
    )
    parser.add_argument(
        "--write-back",
        action="store_true",
        help="Write new words back to source files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only, no files written",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"dicmerge {__version__}",
        help="Show version",
    )
    parser.add_argument(
        "--list-sources",
        action="store_true",
        help="Show discovered source files",
    )
    parser.add_argument(
        "--config",
        nargs="?",
        type=Path,
        const=_SHOW_CONFIG,
        default=None,
        metavar="CONFIG",
        help="Set path to config file",
    )

    args = parser.parse_args()

    if args.config is _SHOW_CONFIG:
        console.print(f"Config path: {DEFAULT_CONFIG_PATH}")
        return

    if args.config is not None and not args.config.exists():
        raise ConfigError(f"Config file not found: {args.config}")

    if args.list_sources:
        from dicmerge.config import load_config
        from dicmerge.scanner.discovery import discover_source_files

        try:
            config = load_config(args.config)
        except DicmergeError as e:
            console.print(f"[red]Error:[/red] {e}")
            sys.exit(e.exit_code)
        discovered = discover_source_files(config)
        table = Table(title="Discovered Sources")
        table.add_column("Source", style="cyan")
        table.add_column("Files")
        for name, files in sorted(discovered.items()):
            if files:
                table.add_row(name, "\n".join(str(f) for f in files))
            else:
                table.add_row(name, "[dim]none found[/dim]")
        console.print(table)
        return

    if args.dry_run:
        console.print("[yellow]Dry run mode — no files will be written[/yellow]")

    try:
        result = run(
            config_path=args.config,
            write_back=args.write_back,
            dry_run=args.dry_run,
        )
    except DicmergeError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(e.exit_code)

    console.print("\n[bold]Scanning:[/bold]")
    for name, count in sorted(result["source_stats"].items()):
        if count:
            console.print(f"  [green]✓[/green] {name}: {count} words")
        else:
            console.print(f"  [yellow]⚠[/yellow] {name}: not found")

    console.print(
        f"\nTotal unique words: [bold]{result['total_unique']}[/bold] "
        f"(from {result['total_raw']} raw, {result['total_filtered']} after filters)"
    )
    console.print(f"Output: {result['output_path']}")

    if result["write_back_stats"]:
        console.print("\n[bold]Write-back:[/bold]")
        for name, entries in sorted(result["write_back_stats"].items()):
            for filename, count in entries:
                console.print(f"  [green]✓[/green] {name}: {filename} → +{count} words")

    console.print("\n[green]Done.[/green]")
