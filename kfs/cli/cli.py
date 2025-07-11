from pathlib import Path

import click


__all__ = (
    "cli",
)


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
    ctx.obj["root"] = root
