import shutil
import uuid

from pathlib import Path
from typing import Iterator, Optional

from pydantic import BaseModel, ValidationError

from . import git


__all__ = (
    "Entry",
    "EntryId",
    "Metadata",
    "Query",

    "filter_entries",
    "generate_entry_id",
    "get_carrier_file",
    "get_entry_id_from_metadata_file",
    "get_metadata_file",
    "import_file",
    "list_entries",
    "list_metadata_files"
)


DEFAULT_ENCODING = "utf-8"
METADATA_FILE_SUFFIX = ".meta"


type EntryId = str


class Metadata(BaseModel):
    name: str
    tags: list[str]


type Entry = tuple[EntryId, Metadata]


class Query(BaseModel):
    name: Optional[str]
    tags: list[str]


def generate_entry_id() -> EntryId:
    return str(uuid.uuid4())


def get_carrier_file(root: Path, entry_id: EntryId) -> Path:
    return root / entry_id


def get_metadata_file(root: Path, entry_id: EntryId) -> Path:
    return (root / entry_id).with_suffix(METADATA_FILE_SUFFIX)


def get_entry_id_from_metadata_file(metadata_file: Path) -> EntryId:
    return metadata_file.stem


def list_metadata_files(root: Path) -> Iterator[Path]:
    return (
        x for x in root.iterdir()
        if tuple(x.suffixes) == (METADATA_FILE_SUFFIX,)
    )


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

        entry_id = get_entry_id_from_metadata_file(metadata_file)
        carrier_file = get_carrier_file(root, entry_id)

        if not carrier_file.exists():
            continue

        yield (entry_id, metadata)


def filter_entries(query: Query, entries: Iterator[Entry]) -> Iterator[Entry]:
    def check_tags(metadata: Metadata) -> bool:
        for x in query.tags:
            if x not in metadata.tags:
                return False

        return True

    for entry in entries:
        entry_id, metadata = entry

        if query.name is not None:
            if metadata.name != query.name:
                continue

        if not check_tags(metadata):
            continue

        yield entry


def import_file(root: Path, external_file: Path, metadata: Metadata) -> Entry:
    entry_id = generate_entry_id()
    carrier_file = get_carrier_file(root, entry_id)
    metadata_file = get_metadata_file(root, entry_id)

    shutil.copy(external_file, carrier_file)
    metadata_file.write_text(
        metadata.model_dump_json(
            indent=2
        ),
        encoding=DEFAULT_ENCODING
    )

    try:
        if git.is_repository(cwd=root) and git.check_author(cwd=root):
            git.add(str(carrier_file.relative_to(root)), cwd=root)
            git.add(str(metadata_file.relative_to(root)), cwd=root)
            git.commit(f"add '{metadata.name}'", cwd=root)
    except git.NotInstalledError:
        pass

    return (entry_id, metadata)
