from typing import Iterable

from rich.console import Console
from rich.table import Table

from ..base import Entry, TagIndex


__all__ = (
    "print_entries",
    "print_tag_index"
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


def print_tag_index(console: Console, index: TagIndex) -> None:
    table = Table()

    table.add_column("Tag")
    table.add_column("Frequency")

    frequencies = [(k, len(v)) for k, v in index.items()]
    frequencies.sort(key=lambda x: x[1], reverse=True)

    for tag, frequency in frequencies:
        table.add_row(tag, str(frequency))

    console.print(table)
