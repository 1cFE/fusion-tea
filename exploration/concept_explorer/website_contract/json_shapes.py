"""JSON shapes: flatten response bodies to "path -> set of kinds" (design Architecture).

Paths: the root is `.`; record fields are `.a.b`; arrays add `[]` and maps add `{*}` to
the segment they follow (`.concepts[]`, `.params{*}`). Standard library only.
"""

from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Callable, Collection, Iterable, Iterator
from typing import Any

KINDS = ("object", "array", "string", "number", "boolean", "null", "absent", "empty")
VACANT = frozenset({"null", "absent", "empty"})  # kinds that carry no value
# Characters a record key or concept ID can't hold, because they'd break a path or token.
PATH_BREAKERS = re.compile(r"[\s.\[\]{}]")


def flatten(bodies: Iterable[Any], map_paths: Collection[str]) -> dict[str, set[str]]:
    """Path -> the kinds seen there, unioned over `bodies`, array elements and map values.

    Objects at `map_paths` are maps: their values share one `{*}` path, and an empty map
    is `empty`. Every other object is a record, whose fields get their own paths. A field
    is `absent` where an object at its record path lacks it; a path under a parent never
    observed as an object is not observed at all. A record key that can't be written as a
    path segment is skipped with everything under it (`unwritable_keys` lists them).
    """
    kinds: dict[str, set[str]] = defaultdict(set)
    objects_seen: dict[str, int] = defaultdict(int)
    fields_seen: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for body in bodies:
        for path, value in _nodes(body, ".", map_paths):
            is_map = path in map_paths
            kinds[path].add(_kind(value, is_map))
            if isinstance(value, dict) and not is_map:
                objects_seen[path] += 1
                for key in filter(_is_path_segment, value):
                    fields_seen[path][key] += 1
    for path, seen in objects_seen.items():
        for key, count in fields_seen[path].items():
            if count < seen:
                kinds[field_path(path, key)].add("absent")
    return dict(kinds)


def strings_at(
    bodies: Iterable[Any], map_paths: Collection[str], wanted: Callable[[str], bool]
) -> set[str]:
    """Every string value at a path `wanted` accepts."""
    return {
        value
        for body in bodies
        for path, value in _nodes(body, ".", map_paths)
        if isinstance(value, str) and wanted(path)
    }


def unwritable_keys(bodies: Iterable[Any], map_paths: Collection[str]) -> list[tuple[str, str]]:
    """(record path, key) for each record key that can't be written as a path segment, sorted.

    The contract can't hold such a key, so a check skips it as new; a recording refuses it.
    """
    return sorted(
        {
            (path, key)
            for body in bodies
            for path, value in _nodes(body, ".", map_paths)
            if isinstance(value, dict) and path not in map_paths
            for key in value
            if not _is_path_segment(key)
        }
    )


def _is_path_segment(key: str) -> bool:
    """Whether a record key can be written as a path segment."""
    return not PATH_BREAKERS.search(key)


def field_path(path: str, key: str) -> str:
    """The path of record field `key` under `path`; fails on a key a path can't hold."""
    if not _is_path_segment(key):
        raise ValueError(
            f"record key {key!r} under {path} can't be written as a path; "
            "a data-driven key like this most likely means a map was classified as a record"
        )
    return f".{key}" if path == "." else f"{path}.{key}"


def _nodes(value: Any, path: str, map_paths: Collection[str]) -> Iterator[tuple[str, Any]]:
    """Every (path, value) in `value`, depth first, starting with `value` itself."""
    yield path, value
    if isinstance(value, dict):
        if path in map_paths:
            children = ((path + "{*}", child) for child in value.values())
        else:
            children = (
                (field_path(path, key), child)
                for key, child in value.items()
                if _is_path_segment(key)
            )
    elif isinstance(value, list):
        children = ((path + "[]", child) for child in value)
    else:
        return
    for child_path, child in children:
        yield from _nodes(child, child_path, map_paths)


def _kind(value: Any, is_map: bool) -> str:
    if isinstance(value, dict):
        return "empty" if is_map and not value else "object"
    if isinstance(value, list):
        return "array" if value else "empty"
    if isinstance(value, bool):  # before int: bool is an int subclass
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if value is None:
        return "null"
    raise TypeError(f"not a JSON value: {value!r}")
