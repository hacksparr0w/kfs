from pathlib import Path

import click

from rich.console import Console

from ..base import TagIndex, Metadata, build_tag_index
from ..core import (
    Query,
    filter_entries,
    import_file,
    list_entries
)

from ..cache import (
    get_tag_index_cache_file,
    read_tag_index_cache,
    write_tag_index_cache
)

from ..system import ensure_system_directory
from .format import print_entries, print_tag_index


def _initialize(root: Path) -> TagIndex:
    ensure_system_directory(root)

    tag_index_cache_file = get_tag_index_cache_file(root)
    tag_index: TagIndex

    if not tag_index_cache_file.exists():
        entries = list_entries(root)
        tag_index = build_tag_index(entries)
        write_tag_index_cache(root, tag_index)
    else:
        tag_index = read_tag_index_cache(root)

    return tag_index


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

    tag_index = _initialize(root)

    name = name if name else external_file.name
    metadata = Metadata(name=name, tags=set(tags))
    tag_index, entry = import_file(root, tag_index, external_file, metadata)

    write_tag_index_cache(root, tag_index)

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


@cli.command("tags")
@click.pass_context
def tags(ctx):
    console = ctx.obj["console"]
    root = ctx.obj["root"]

    tag_index_cache_file = get_tag_index_cache_file(root)

    if not tag_index_cache_file.exists():
        return

    tag_index = read_tag_index_cache(root)

    if not tag_index:
        return

    print_tag_index(console, tag_index)
