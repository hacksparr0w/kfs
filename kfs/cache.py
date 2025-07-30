from pathlib import Path

from .core import TagIndex
from .system import get_system_directory, get_system_encoding

from pydantic import TypeAdapter


_TAG_INDEX_CACHE_FILE_NAME = "tags.json"


__all__ = (
    "get_tag_index_cache_file",
    "read_tag_index_cache",
    "write_tag_index_cache"
)


def get_tag_index_cache_file(root: Path) -> Path:
    return get_system_directory(root) / _TAG_INDEX_CACHE_FILE_NAME


def read_tag_index_cache(root: Path) -> TagIndex:
    data = get_tag_index_cache_file(root).read_text(
        encoding=get_system_encoding()
    )

    return TypeAdapter(TagIndex).validate_json(data)


def write_tag_index_cache(root: Path, index: TagIndex) -> None:
    data = TypeAdapter(TagIndex).dump_json(index)

    get_tag_index_cache_file(root).write_bytes(data)
