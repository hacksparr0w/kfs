import click

from ..core import Query, list_entries, filter_entries
from .cli import cli


__all__ = (
    "ls",
)


@cli.command("ls")
@click.option("--tag", "tags", multiple=True)
@click.option("--name")
@click.pass_context
def ls(ctx, tags, name):
    root = ctx.obj["root"]
    query = Query(name=name, tags=tags)
    entries = list_entries(root)
    entries = filter_entries(query, entries)
    entries = list(entries)

    print(entries)
