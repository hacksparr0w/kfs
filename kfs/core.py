import shutil
import uuid

from pathlib import Path
from typing import Iterator, Optional

from pydantic import BaseModel, ValidationError

from . import git


__all__ = (
    "Entry",
    "Metadata",
    "Query",

    "filter_entries",
    "generate_carrier_file_name",
    "get_carrier_file",
    "get_metadata_file",
    "import_file",
    "list_entries",
    "list_metadata_files"
)


DEFAULT_ENCODING = "utf-8"
METADATA_FILE_SUFFIX = ".meta"


class Metadata(BaseModel):
    name: str
    tags: list[str]


type Entry = tuple[Path, Metadata]


class Query(BaseModel):
    name: Optional[str]
    tags: list[str]


def generate_carrier_file_name() -> str:
    return str(uuid.uuid4())


def get_carrier_file(metadata_file: Path) -> Path:
    return metadata_file.with_suffix("")


def get_metadata_file(carrier_file: Path) -> Path:
    return carrier_file.with_suffix(METADATA_FILE_SUFFIX)


def list_metadata_files(root: Path) -> Iterator[Path]:
    return (x for x in root.iterdir() if x.suffix == METADATA_FILE_SUFFIX)


def list_entries(root: Path) -> Iterator[Entry]:
    for metadata_file in list_metadata_files(root):
        try:
            metadata = Metadata.model_validate_json(
                metadata_file.read_text(
                    encoding=DEFAULT_ENCODING
                )
            )
        except ValidationError:
            continue

        carrier_file = get_carrier_file(metadata_file)

        if not carrier_file.exists():
            continue

        yield (carrier_file, metadata)


def filter_entries(query: Query, entries: Iterator[Entry]) -> Iterator[Entry]:
    def check_tags(metadata: Metadata) -> bool:
        for x in query.tags:
            if x not in metadata.tags:
                return False

        return True

    for entry in entries:
        carrier_file, metadata = entry

        if query.name is not None:
            if metadata.name != query.name:
                continue

        if not check_tags(metadata):
            continue

        yield entry


def import_file(root: Path, external_file: Path, metadata: Metadata) -> Entry:
    carrier_file = root / generate_carrier_file_name()
    metadata_file = get_metadata_file(carrier_file)

    shutil.copy(external_file, carrier_file)
    metadata_file.write_text(
        metadata.model_dump_json(
            indent=2
        ),
        encoding=DEFAULT_ENCODING
    )

    if git.is_repository(cwd=root) and git.check_author(cwd=root):
        git.add(str(carrier_file.name), cwd=root)
        git.add(str(metadata_file.name), cwd=root)
        git.commit(f"add '{metadata.name}'", cwd=root)

    return (carrier_file, metadata)
