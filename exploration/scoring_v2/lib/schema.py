"""Hand-rolled schema validator for scoring_v2 feature files."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema.yaml"
FEATURES_DIR = ROOT / "features"

_VALID_EXTRACTORS = {"taxonomy", "manual", "cost_model", "derived", "llm"}


class SchemaError(ValueError):
    pass


def load_schema(path: Path | str = SCHEMA_PATH) -> dict[str, dict[str, Any]]:
    with open(path) as f:
        schema = yaml.safe_load(f)
    for name, entry in schema.items():
        if entry.get("extractor") not in _VALID_EXTRACTORS:
            raise SchemaError(
                f"{path}: {name}.extractor: must be one of {sorted(_VALID_EXTRACTORS)}"
            )
        if entry.get("type") == "enum" and not entry.get("values"):
            raise SchemaError(f"{path}: {name}: enum type requires non-empty values list")
    return schema


def validate_features_file(path: Path | str, schema: dict[str, dict[str, Any]] | None = None) -> None:
    """Validate one features/{concept_id}.yaml against the schema. Raises SchemaError on first violation."""
    path = Path(path)
    if schema is None:
        schema = load_schema()
    with open(path) as f:
        doc = yaml.safe_load(f)
    if not isinstance(doc, dict):
        raise SchemaError(f"{path.name}: file must be a YAML mapping at top level")

    meta = doc.get("_meta")
    if not isinstance(meta, dict) or not meta.get("concept_id") or not meta.get("name"):
        raise SchemaError(f"{path.name}: _meta block must contain concept_id and name")

    for feat_name, entry in schema.items():
        if feat_name not in doc:
            if entry.get("required"):
                raise SchemaError(f"{path.name}: {feat_name}: required feature missing")
            continue
        block = doc[feat_name]
        if not isinstance(block, dict) or "value" not in block:
            raise SchemaError(f"{path.name}: {feat_name}: must be a mapping with a 'value' key")
        value = block["value"]
        if entry["type"] == "enum":
            if value not in entry["values"]:
                raise SchemaError(
                    f"{path.name}: {feat_name}.value: {value!r} not in enum "
                    f"{entry['values']}"
                )
        elif entry["type"] == "string":
            if not isinstance(value, str):
                raise SchemaError(
                    f"{path.name}: {feat_name}.value: expected string, got {type(value).__name__}"
                )
        elif entry["type"] == "float":
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                raise SchemaError(
                    f"{path.name}: {feat_name}.value: expected float, got {type(value).__name__}"
                )
        elif entry["type"] == "int":
            if not isinstance(value, int) or isinstance(value, bool):
                raise SchemaError(
                    f"{path.name}: {feat_name}.value: expected int, got {type(value).__name__}"
                )
        else:
            raise SchemaError(f"{path.name}: {feat_name}: unknown type {entry['type']!r}")

        if "provenance" not in block:
            raise SchemaError(f"{path.name}: {feat_name}.provenance: missing")
        if "confidence" not in block:
            raise SchemaError(f"{path.name}: {feat_name}.confidence: missing")
        if block["confidence"] not in ("low", "medium", "high"):
            raise SchemaError(
                f"{path.name}: {feat_name}.confidence: must be low|medium|high"
            )

    # Reject unknown top-level keys (other than _meta and per-axis
    # `{axis}_diagnostics` blocks) to prevent silent typos. Diagnostic
    # blocks are populated by the per-axis scripts (e.g.
    # populate_modularity_diagnostics.py) and have arbitrary mapping
    # shape; they are not subject to feature-style validation.
    for key in doc:
        if key == "_meta":
            continue
        if key.endswith("_diagnostics"):
            if not isinstance(doc[key], dict):
                raise SchemaError(
                    f"{path.name}: {key}: must be a mapping"
                )
            continue
        if key not in schema:
            raise SchemaError(f"{path.name}: unknown feature {key!r} (not declared in schema)")


def validate_all(features_dir: Path | str = FEATURES_DIR) -> int:
    """Validate every feature file. Returns count validated."""
    schema = load_schema()
    files = sorted(Path(features_dir).glob("*.yaml"))
    for f in files:
        validate_features_file(f, schema)
    return len(files)
