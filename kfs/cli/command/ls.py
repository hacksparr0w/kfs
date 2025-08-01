from typing import Optional

import click

from ...core import (
    Query,
    filter_entries,
    list_entries
)

from ..app import app
from ..format import print_entries


@app.command("ls")
@click.option("--tag", "tags", multiple=True)
@click.option("--name")
@click.pass_context
def ls(ctx: click.Context, tags: list[str], name: Optional[str]) -> None:
    console = ctx.obj["console"]
    root = ctx.obj["root"]

    query = Query(name=name, tags=set(tags))
    entries = list_entries(root)
    entries = filter_entries(query, entries)
    entries = list(entries)

    if entries:
        print_entries(console, entries)
