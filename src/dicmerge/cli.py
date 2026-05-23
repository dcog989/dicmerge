import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from dicmerge.core import run

console = Console()


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
        "--config",
        type=Path,
        default=None,
        help="Path to config file",
    )
    parser.add_argument(
        "--list-sources",
        action="store_true",
        help="Show discovered source files and exit",
    )

    args = parser.parse_args()

    if args.list_sources:
        from dicmerge.config import discover_source_files, load_config

        config = load_config(args.config)
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

    result = run(
        config_path=args.config,
        write_back=args.write_back,
        dry_run=args.dry_run,
    )

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
        for name, count in sorted(result["write_back_stats"].items()):
            console.print(f"  [green]✓[/green] {name}: +{count} words")

    console.print("\n[green]Done.[/green]")
