from pathlib import Path
from typing import Literal, Optional, overload

import click

from rich.console import Console

from ..base import TagIndex, build_tag_index
from ..cache import (
    get_tag_index_cache_file,
    read_tag_index_cache,
    write_tag_index_cache
)

from ..core import list_entries
from ..system import ensure_system_directory


@overload
def initialize(root: Path, *, force: Literal[False]) -> Optional[TagIndex]:
    ...


@overload
def initialize(root: Path, *, force: Literal[True]) -> TagIndex: ...


def initialize(root: Path, *, force: bool) -> Optional[TagIndex]:
    if force:
        ensure_system_directory(root)

    tag_index_cache_file = get_tag_index_cache_file(root)
    tag_index: TagIndex

    if not tag_index_cache_file.exists():
        if not force:
            return None

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
def app(ctx: click.Context, root: Path) -> None:
    ctx.ensure_object(dict)
    ctx.obj["console"] = Console()
    ctx.obj["root"] = root
