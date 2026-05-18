"""Read/write per-concept feature YAMLs, preserving non-target fields on partial update."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .schema import FEATURES_DIR


def _path(concept_id: str, features_dir: Path | str = FEATURES_DIR) -> Path:
    return Path(features_dir) / f"{concept_id}.yaml"


def read_features(concept_id: str, features_dir: Path | str = FEATURES_DIR) -> dict[str, Any]:
    p = _path(concept_id, features_dir)
    if not p.exists():
        return {}
    with open(p) as f:
        return yaml.safe_load(f) or {}


def write_features(
    concept_id: str,
    doc: dict[str, Any],
    features_dir: Path | str = FEATURES_DIR,
) -> Path:
    p = _path(concept_id, features_dir)
    p.parent.mkdir(parents=True, exist_ok=True)
    # _meta always first; remaining keys sorted for byte-stability.
    ordered: dict[str, Any] = {}
    if "_meta" in doc:
        ordered["_meta"] = doc["_meta"]
    for k in sorted(k for k in doc if k != "_meta"):
        ordered[k] = doc[k]
    with open(p, "w") as f:
        yaml.safe_dump(ordered, f, sort_keys=False, default_flow_style=False)
    return p


def update_feature(
    concept_id: str,
    feature_name: str,
    block: dict[str, Any],
    features_dir: Path | str = FEATURES_DIR,
    meta: dict[str, Any] | None = None,
) -> Path:
    """Overwrite exactly one feature block; preserve every other field."""
    doc = read_features(concept_id, features_dir)
    if meta is not None:
        doc["_meta"] = meta
    doc[feature_name] = block
    return write_features(concept_id, doc, features_dir)
