import click

from ..app import app, initialize
from ..format import print_tag_index


@app.command("tags")
@click.pass_context
def tags(ctx) -> None:
    console = ctx.obj["console"]
    root = ctx.obj["root"]

    tag_index = initialize(root, force=False)

    if not tag_index:
        return

    print_tag_index(console, tag_index)
