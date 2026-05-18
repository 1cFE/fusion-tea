"""Phase 1 tests: taxonomy extraction pipeline."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from exploration.scoring_v2.lib.schema import (
    SchemaError,
    load_schema,
    validate_features_file,
)


def test_bulk_taxonomy_produces_38_valid_files(run_cli, tmp_features_dir: Path):
    # Wipe and re-extract into the tmp dir from scratch.
    for p in tmp_features_dir.glob("*.yaml"):
        p.unlink()
    run_cli("extract.py", "--bulk-taxonomy")
    files = sorted(tmp_features_dir.glob("*.yaml"))
    assert len(files) == 38
    schema = load_schema()
    for f in files:
        validate_features_file(f, schema)


def test_single_feature_reextract_preserves_other_fields(run_cli, tmp_features_dir: Path):
    cid = "01-hts-compact-tokamak"
    snapshot = yaml.safe_load((tmp_features_dir / f"{cid}.yaml").read_text())
    # Mutate magnet_type so we can prove re-extraction overwrites it.
    snapshot["magnet_type"]["value"] = "SENTINEL"
    (tmp_features_dir / f"{cid}.yaml").write_text(yaml.safe_dump(snapshot, sort_keys=False))

    run_cli("extract.py", cid, "magnet_type")

    after = yaml.safe_load((tmp_features_dir / f"{cid}.yaml").read_text())
    assert after["magnet_type"]["value"] == "HTS (wound)"
    # Every other feature block must be untouched (value + provenance + confidence + extracted_at).
    for k, v in snapshot.items():
        if k == "magnet_type":
            continue
        assert after[k] == v, f"feature {k} changed unexpectedly"


def test_validator_catches_malformed_enum(tmp_features_dir: Path):
    target = tmp_features_dir / "01-hts-compact-tokamak.yaml"
    doc = yaml.safe_load(target.read_text())
    doc["confinement_family"]["value"] = "Garbage"
    target.write_text(yaml.safe_dump(doc, sort_keys=False))
    with pytest.raises(SchemaError) as ei:
        validate_features_file(target)
    msg = str(ei.value)
    assert "01-hts-compact-tokamak" in msg
    assert "confinement_family" in msg


def test_validator_catches_unknown_feature(tmp_features_dir: Path):
    target = tmp_features_dir / "01-hts-compact-tokamak.yaml"
    doc = yaml.safe_load(target.read_text())
    doc["mystery_feature"] = {"value": "x", "provenance": "manual", "confidence": "high"}
    target.write_text(yaml.safe_dump(doc, sort_keys=False))
    with pytest.raises(SchemaError, match="mystery_feature"):
        validate_features_file(target)


def test_dispatcher_raises_for_unimplemented_extractors():
    from exploration.scoring_v2.lib.extractors import dispatch
    for name in ("cost_model", "llm"):
        with pytest.raises(NotImplementedError, match="later slice"):
            dispatch(name)
