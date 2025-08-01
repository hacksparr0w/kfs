from pathlib import Path
from typing import Optional

import click

from ...base import Metadata
from ...cache import write_tag_index_cache
from ...core import import_file
from ..app import app, initialize
from ..format import print_entries


@app.command("im")
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
def im(
    ctx: click.Context,
    tags: list[str],
    name: Optional[str],
    external_file: Path
) -> None:
    console = ctx.obj["console"]
    root = ctx.obj["root"]

    tag_index = initialize(root, force=True)

    name = name if name else external_file.name
    metadata = Metadata(name=name, tags=set(tags))
    tag_index, entry = import_file(root, tag_index, external_file, metadata)

    write_tag_index_cache(root, tag_index)

    print_entries(console, [entry])
