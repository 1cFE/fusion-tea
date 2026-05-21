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


def test_bulk_taxonomy_produces_all_valid_files(run_cli, tmp_features_dir: Path):
    # Re-extract over the existing live snapshot, then run --bulk-derived
    # (confinement_concept reads upstream taxonomy values from disk, so it
    # must run after bulk_taxonomy). Concept count is 40 post ontology-v3
    # merge. gap_report_path (manual extractor) is required: false in
    # schema; absent values are allowed.
    run_cli("extract.py", "--bulk-taxonomy")
    run_cli("extract.py", "--bulk-derived")
    files = sorted(tmp_features_dir.glob("*.yaml"))
    assert len(files) == 40
    schema = load_schema()
    for f in files:
        validate_features_file(f, schema)


def test_v3_features_present_after_bulk_taxonomy(run_cli, tmp_features_dir: Path):
    """The 5 v3 taxonomy columns and the derived confinement_concept must
    populate for every concept after the bulk extraction sequence."""
    run_cli("extract.py", "--bulk-taxonomy")
    run_cli("extract.py", "--bulk-derived")
    v3_taxonomy_features = [
        "primary_heating",
        "blanket_config",
        "repetition_rate",
        "laser_approach",
        "non_standard_mechanism",
    ]
    for path in sorted(tmp_features_dir.glob("*.yaml")):
        doc = yaml.safe_load(path.read_text())
        for fname in v3_taxonomy_features:
            assert fname in doc, f"{path.name}: missing {fname}"
            assert doc[fname]["provenance"] == "taxonomy"
            assert doc[fname]["value"], f"{path.name}: empty {fname}"
        assert "confinement_concept" in doc, f"{path.name}: missing confinement_concept"
        assert doc["confinement_concept"]["provenance"] == "derived"


def test_retired_orphans_not_in_schema():
    """Pre-v3 orphans must be gone from the schema (P1 retirement)."""
    schema = load_schema()
    assert "tritium_breeding" not in schema
    assert "neutron_management" not in schema


@pytest.mark.parametrize("cid,expected", [
    ("01-hts-compact-tokamak",                    "Compact tokamak"),
    ("21-spherical-tokamak-hts",                  "Spherical tokamak"),
    ("29-negative-triangularity-tokamak",         "Negative triangularity tokamak"),
    ("33-state-backed-tokamak-best",              "Tokamak"),
    ("09-qi-stellarator-hts",                     "QI stellarator"),
    ("20a-type-one-stellarator",                  "Modular stellarator"),
    ("36-helical-coil-stellarator",               "Helical coil stellarator"),
    ("05-planar-coil-stellarator",                "Planar coil stellarator"),
    ("06-magnetic-mirror",                        "Mirror"),
    ("11-magnetic-mirror",                        "Mirror"),
    ("15-sheared-flow-stabilized-z-pinch",        "Z-pinch (sheared-flow)"),
    ("12-levitated-dipole",                       "Levitated dipole"),
    ("19-orbital-levitated-dipole",               "Levitated dipole (orbital)"),
    ("18-p-b11-frc",                              "FRC"),
    ("26-laser-icf-indirect-drive",               "Laser ICF (indirect drive)"),
    ("31-laser-icf-oec-architecture",             "Laser ICF (direct drive)"),
    ("17b-laser-icf-fast-ignition",               "Laser ICF (fast ignition)"),
    ("23-laser-icf-nanostructured-target",        "Laser ICF (ultrashort pulse)"),
    ("17a-laser-icf-hybrid-drive",                "Laser ICF (hybrid drive)"),
    ("03-laser-icf-liquid-jet-target",            "Laser ICF (liquid jet)"),
    ("22-projectile-icf",                         "Projectile ICF"),
    ("25-heavy-ion-beam-icf",                     "Heavy ion ICF"),
    ("02-acoustic-icf-sonofusion",                "Acoustic ICF (sonofusion)"),
    ("07-maglif",                                 "MagLIF"),
    ("14-magnetized-target-fusion-pneumatic-compression", "Magnetized target fusion"),
    ("37-magnetized-target-inertial-fusion-mtif", "Magnetized target fusion"),
    ("08-frc-w-direct-conversion",                "FRC compression (MIF)"),
    ("27-polywell",                               "Polywell"),
    ("13-electrostatic-hybrid",                   "Electrostatic hybrid"),
    ("38-particle-accelerator-driven-fusion",     "Beam-target fusion"),
    ("16-muon-catalyzed-fusion",                  "Muon-catalyzed fusion"),
    ("24-dense-plasma-focus",                     "Dense plasma focus"),
])
def test_confinement_concept_disambiguation(cid: str, expected: str):
    """The derived confinement_concept must match the downstream-spec
    controlled vocabulary for every concept (sampled across the table).

    Reads from the live features/ directory because the values are
    committed alongside this test as part of P1."""
    from exploration.scoring_v2.lib import feature_io
    doc = feature_io.read_features(cid)
    assert "confinement_concept" in doc, f"{cid}: missing confinement_concept"
    assert doc["confinement_concept"]["value"] == expected, (
        f"{cid}: confinement_concept = {doc['confinement_concept']['value']!r}, "
        f"expected {expected!r}"
    )


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
    # cost_model lands in slice 2; only llm remains unimplemented.
    with pytest.raises(NotImplementedError, match="later slice"):
        dispatch("llm")
