from .cli.app import app
from .cli.command.im import im as _ # noqa: F401, F811
from .cli.command.ls import ls as _ # noqa: F401, F811
from .cli.command.tags import tags as _ # noqa: F401, F811


def main() -> None:
    app()


if __name__ == "__main__":
    main()
