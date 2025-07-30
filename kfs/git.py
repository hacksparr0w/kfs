import subprocess

from pathlib import Path
from typing import Optional


__all__ = (
    "GitError",
    "InvalidRepositoryError",
    "NotInstalledError",

    "add",
    "check_author",
    "commit",
    "get_configuration",
    "is_repository",
    "run",
    "status"
)


class GitError(Exception):
    pass


class InvalidRepositoryError(GitError):
    pass


class NotInstalledError(GitError):
    pass


def run(
    *args: str,
    cwd: Optional[Path] = None
) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            ["git", *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd
        )
    except FileNotFoundError:
        raise NotInstalledError


def get_configuration(name: str, cwd: Optional[Path] = None) -> str:
    result = run("config", "--get", name, cwd=cwd)

    return result.stdout.decode()


def check_author(cwd: Optional[Path] = None) -> bool:
    return bool(get_configuration("user.name", cwd=cwd)) and \
        bool(get_configuration("user.email", cwd=cwd))


def status(cwd: Optional[Path] = None) -> None:
    result = run("status", cwd=cwd)

    if result.returncode != 0:
        raise InvalidRepositoryError


def is_repository(cwd: Optional[Path] = None) -> bool:
    try:
        status(cwd=cwd)
    except InvalidRepositoryError:
        return False

    return True


def commit(message: str, cwd: Optional[Path] = None) -> None:
    run("commit", "-m", message, cwd=cwd)


def add(specifier: str, cwd: Optional[Path] = None) -> None:
    run("add", specifier, cwd=cwd)
