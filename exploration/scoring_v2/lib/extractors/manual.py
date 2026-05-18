"""Manual extractor: noop. The value is whatever already lives on disk."""
from __future__ import annotations

from typing import Any

from .. import feature_io


def extract(
    concept_id: str, feature_name: str, schema_entry: dict[str, Any]
) -> tuple[Any, str, str]:
    doc = feature_io.read_features(concept_id)
    block = doc.get(feature_name)
    if not isinstance(block, dict) or "value" not in block:
        raise ValueError(
            f"manual extractor: {concept_id}.{feature_name} has no on-disk value; "
            f"edit features/{concept_id}.yaml first"
        )
    confidence = block.get("confidence", "medium")
    return block["value"], "manual", confidence
