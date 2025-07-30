from pathlib import Path


_SYSTEM_DIRECTORY_NAME = ".kfs"
_SYSTEM_ENCODING = "utf-8"


__all__ = (
    "InvalidSystemDirectory",
    "SystemError",

    "ensure_system_directory",
    "get_system_directory",
    "get_system_encoding"
)


class SystemError(Exception):
    pass


class InvalidSystemDirectory(SystemError):
    pass


def get_system_directory(root: Path) -> Path:
    return root / _SYSTEM_DIRECTORY_NAME


def get_system_encoding() -> str:
    return _SYSTEM_ENCODING


def ensure_system_directory(root: Path) -> Path:
    directory = get_system_directory(root)

    if not directory.exists():
        directory.mkdir()

    if not directory.is_dir():
        raise InvalidSystemDirectory

    return directory
