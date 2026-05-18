"""Extractor dispatcher.

Each extractor implements:
    extract(concept_id: str, feature_name: str, schema_entry: dict) -> (value, provenance, confidence)
"""
from __future__ import annotations

from typing import Any, Callable, Tuple

from . import taxonomy as _taxonomy
from . import manual as _manual

Result = Tuple[Any, str, str]
ExtractorFn = Callable[[str, str, dict], Result]

_IMPLEMENTED: dict[str, ExtractorFn] = {
    "taxonomy": _taxonomy.extract,
    "manual": _manual.extract,
}


def dispatch(name: str) -> ExtractorFn:
    if name in _IMPLEMENTED:
        return _IMPLEMENTED[name]
    if name in ("cost_model", "llm"):
        raise NotImplementedError(
            f"extractor {name!r} will be implemented in a later slice"
        )
    raise ValueError(f"unknown extractor: {name!r}")
