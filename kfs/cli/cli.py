from pathlib import Path

import click

from rich.console import Console

from ..core import Metadata, Query, filter_entries, import_file, list_entries
from .format import print_entries


@click.group()
@click.option(
    "--root",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        path_type=Path
    ),
    default=Path.cwd()
)
@click.pass_context
def cli(ctx, root):
    ctx.ensure_object(dict)
    ctx.obj["console"] = Console()
    ctx.obj["root"] = root


@cli.command("im")
@click.option("--tag", "tags", multiple=True)
@click.option("--name")
@click.argument(
    "external_file",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        path_type=Path
    )
)
@click.pass_context
def im(ctx, tags, name, external_file):
    console = ctx.obj["console"]
    root = ctx.obj["root"]
    name = name if name else external_file.name
    metadata = Metadata(name=name, tags=tags)
    entry = import_file(root, external_file, metadata)

    print_entries(console, [entry])


@cli.command("ls")
@click.option("--tag", "tags", multiple=True)
@click.option("--name")
@click.pass_context
def ls(ctx, tags, name):
    console = ctx.obj["console"]
    root = ctx.obj["root"]
    query = Query(name=name, tags=tags)
    entries = list_entries(root)
    entries = filter_entries(query, entries)
    entries = list(entries)

    if entries:
        print_entries(console, entries)
