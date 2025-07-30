import uuid

from typing import Iterator

from pydantic import BaseModel


__all__ = (
    "Entry",
    "EntryId",
    "Metadata",
    "Tag",
    "TagIndex",
    "Tags",

    "add_to_tag_index",
    "build_tag_index",
    "copy_tag_index",
    "generate_entry_id"
)


type EntryId = str
type Entry = tuple[EntryId, Metadata]
type Tag = str
type Tags = set[Tag]
type TagIndex = dict[Tag, set[EntryId]]


class Metadata(BaseModel):
    name: str
    tags: Tags


def generate_entry_id() -> EntryId:
    return str(uuid.uuid4())


def add_to_tag_index(index: TagIndex, entry_id: EntryId, tags: Tags) -> None:
    for tag in tags:
        index.setdefault(tag, set()).add(entry_id)


def build_tag_index(entries: Iterator[Entry]) -> TagIndex:
    index = {}

    for entry_id, metadata in entries:
        add_to_tag_index(index, entry_id, metadata.tags)

    return index


def copy_tag_index(index: TagIndex) -> TagIndex:
    return {k: v.copy() for k, v in index.items()}
