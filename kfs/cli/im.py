from pathlib import Path

import click

from ..core import Metadata, import_file
from .cli import cli


__all__ = (
    "im",
)


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
    root = ctx.obj["root"]
    name = name if name else external_file.name
    metadata = Metadata(name=name, tags=tags)
    entry = import_file(root, external_file, metadata)

    print(entry)
