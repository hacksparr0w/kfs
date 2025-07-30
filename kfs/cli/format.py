from typing import Iterable

from rich.console import Console
from rich.table import Table

from ..core import Entry


__all__ = (
    "print_entries",
)


def print_entries(console: Console, entries: Iterable[Entry]) -> None:
    table = Table()

    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Tags")

    for entry in entries:
        entry_id, metadata = entry

        table.add_row(entry_id, metadata.name, ", ".join(metadata.tags))

    console.print(table)
