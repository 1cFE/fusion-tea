"""The output, manifest, and digest recipes as a fixed seam.

Covers the recipes and the strict manifest validator (Phase 1), the real manifest
against its schema and its live pin (Phase 2), and — from Phase 7 — byte
determinism, schema validation of real output, disclosure parity, and constraint
completeness.
"""

import hashlib
import json
import re
import subprocess
import sys

import jsonschema
import pytest

from scripts.study import manifest
from tests.study.conftest import DATA_DIR, REAL_MANIFEST, REAL_PACKAGE, run_tool, run_tool_raw


def test_fingerprint_recipe_is_stable_and_path_sorted(real_package_path):
    a = manifest.indicator_input_fingerprint(real_package_path)
    b = manifest.indicator_input_fingerprint(real_package_path)
    assert a["recipe"] == "indicator-input-fingerprint/v1"
    assert a == b
    paths = [f["path"] for f in a["files"]]
    assert paths == sorted(paths)
    assert not any(p.endswith("__init__.py") for p in paths)  # M1


def test_fingerprint_read_set_is_the_three_legs(real_package_path):
    files = [f["path"] for f in manifest.indicator_input_fingerprint(real_package_path)["files"]]
    assert "pipelines/pipeline.yaml" in files
    assert "contracts/model_contract.json" in files
    assert sum(1 for p in files if p.startswith("inputs/")) == 5  # one per generated input group
    assert all(
        p.startswith(("pipelines/", "inputs/")) or p == "contracts/model_contract.json"
        for p in files
    )


def test_fingerprint_is_independent_of_working_directory(real_package_path, tmp_path):
    """The recipe hashes package-relative paths, so where the tool runs cannot change it."""
    runs = [
        subprocess.run(
            [sys.executable, str(real_package_path.parents[3] / "scripts/study/indicators.py"),
             "--package", str(real_package_path), "--print-fingerprint"],
            capture_output=True, text=True, cwd=str(cwd), check=True,
        ).stdout
        for cwd in (real_package_path.parents[3], tmp_path)
    ]
    assert runs[0] == runs[1]
    assert manifest.indicator_input_fingerprint(real_package_path)["digest"] in runs[0]


def test_manifest_validator_raises_on_unknown_key(minimal_manifest_dict):
    minimal_manifest_dict["surprise"] = 1
    with pytest.raises(manifest.ManifestError) as e:
        manifest.validate(minimal_manifest_dict)
    assert "surprise" in str(e.value)


def test_minimal_manifest_validates(minimal_manifest_dict):
    assert manifest.validate(minimal_manifest_dict) is minimal_manifest_dict


@pytest.mark.parametrize(
    "path,expect",
    [
        (("package", "name"), "manifest.package.name"),
        (("fingerprints", "indicator_inputs", "digest"), "indicator_inputs.digest"),
        (("baseline", "headline", "value"), "baseline.headline.value"),
        (("oracle", "callable"), "manifest.oracle.callable"),
    ],
)
def test_manifest_validator_locates_a_missing_required_key(minimal_manifest_dict, path, expect):
    block = minimal_manifest_dict
    for step in path[:-1]:
        block = block[step]
    del block[path[-1]]
    with pytest.raises(manifest.ManifestError) as e:
        manifest.validate(minimal_manifest_dict)
    assert expect in str(e.value)


def test_manifest_validator_rejects_a_malformed_baseline(minimal_manifest_dict):
    minimal_manifest_dict["baseline"]["headline"]["value"] = "two dollars"
    with pytest.raises(manifest.ManifestError) as e:
        manifest.validate(minimal_manifest_dict)
    assert "baseline.headline.value" in str(e.value)


def test_manifest_validator_rejects_duplicate_objective_names(minimal_manifest_dict):
    entry = dict(minimal_manifest_dict["objective_catalog"][0])
    entry["channel"] = entry["channel"] + "_other"
    minimal_manifest_dict["objective_catalog"].append(entry)
    with pytest.raises(manifest.ManifestError) as e:
        manifest.validate(minimal_manifest_dict)
    assert "duplicate objective name" in str(e.value)


def test_manifest_validator_rejects_an_unknown_oracle_kind(minimal_manifest_dict):
    minimal_manifest_dict["oracle"] = {"kind": "cli", "argv": ["run"]}
    with pytest.raises(manifest.ManifestError) as e:
        manifest.validate(minimal_manifest_dict)
    assert "unknown kind" in str(e.value)


# ------------------------------------------------------- the real manifest (Phase 2)


def test_real_manifest_validates(real_manifest_path, load_schema):
    data = json.loads(real_manifest_path.read_bytes())
    manifest.validate(data)  # hand-rolled, strict
    jsonschema.validate(data, load_schema("study_package_manifest.v1"))


def test_real_manifest_pin_matches_live_package(real_package_path, real_manifest_path):
    pinned = json.loads(real_manifest_path.read_bytes())["fingerprints"]["indicator_inputs"]
    computed = manifest.indicator_input_fingerprint(real_package_path)
    assert pinned["digest"] == computed["digest"]
    assert pinned["files"] == [f["path"] for f in computed["files"]]


def test_real_manifest_names_the_live_package(real_package_path, real_manifest_path):
    loaded = manifest.load(real_manifest_path)
    manifest.assert_package_identity(loaded, real_package_path)


def test_real_manifest_holds_no_per_study_choices(real_manifest_path):
    """The manifest is the package catalog. Axes, windows, and selected objectives
    are per-study choices and belong to the study definition and the record."""
    data = json.loads(real_manifest_path.read_bytes())
    assert set(data) == {
        "schema_version",
        "package",
        "fingerprints",
        "objective_catalog",
        "ties",
        "baseline",
        "oracle",
    }


def test_manifest_load_reports_the_digest_of_its_own_bytes(real_manifest_path):
    loaded = manifest.load(real_manifest_path)
    assert loaded.digest == hashlib.sha256(real_manifest_path.read_bytes()).hexdigest()


def test_tool_source_digest_recomputes(repo_root):
    """M5: the digest is over an explicitly named file list, under its own recipe id."""
    computed = manifest.tool_source_digest()
    assert computed["recipe"] == "tool-source-digest/v1"
    lines = ["tool-source-digest/v1"] + [
        f"{rel} {hashlib.sha256((repo_root / rel).read_bytes()).hexdigest()}"
        for rel in sorted(manifest.TOOL_SOURCE_FILES)
    ]
    expected = hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()
    assert computed["digest"] == expected
    assert any(p.startswith("scripts/study/schemas/") for p in manifest.TOOL_SOURCE_FILES)


def test_schema_files_carry_the_two_load_bearing_descriptions(load_schema):
    """N1 and S1: facts a record reader would otherwise assume wrong."""
    schema = load_schema("indicators.v1")
    exec_fp = schema["properties"]["package"]["properties"]["recorded_executable_fingerprint"]
    assert "OUTSIDE the digested set" in exec_fp["description"]
    subset = schema["properties"]["axis_declaration"]["properties"]["subset"]
    assert "whole declaration" in subset["description"]


@pytest.mark.parametrize(
    "stem", ["indicators.v1", "study_package_manifest.v1", "axis_declaration.v1"]
)
def test_schemas_are_closed(stem, load_schema):
    """additionalProperties: false throughout — the citable contract is exact."""
    schema = load_schema(stem)

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") == "object" and "additionalProperties" not in node:
                raise AssertionError(f"{stem}: open object at {node.get('title', node)}")
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(schema)


# --------------------------------------------- the output as a fixed seam (Phase 7)


def _report(cwd=None):
    return run_tool(REAL_PACKAGE, REAL_MANIFEST, DATA_DIR / "axes.known_answers.json", cwd=cwd)


def _report_text(cwd=None):
    rc, out, err = run_tool_raw(
        REAL_PACKAGE, REAL_MANIFEST, DATA_DIR / "axes.known_answers.json", cwd=cwd
    )
    assert rc == 0, err
    return out


def test_byte_determinism_across_working_directories(repo_root, tmp_path):
    """Invariant 2 / M4. Item 2 snapshots this document's digest into every record,
    so identical facts must produce identical bytes wherever the agent ran."""
    a = _report_text(cwd=repo_root)
    b = _report_text(cwd=tmp_path)
    assert a == b
    assert "/home/" not in a
    assert not re.search(r'"/', a)  # no absolute path anywhere in the document


def test_two_runs_from_the_same_directory_are_byte_identical(repo_root):
    assert _report_text(cwd=repo_root) == _report_text(cwd=repo_root)


def test_the_real_output_validates_against_its_schema(load_schema):
    jsonschema.validate(_report(), load_schema("indicators.v1"))


def test_the_axis_declaration_validates_against_its_schema(load_schema):
    declaration = json.loads((DATA_DIR / "axes.known_answers.json").read_text())
    jsonschema.validate(declaration, load_schema("axis_declaration.v1"))


def test_not_derivable_is_byte_equal(load_schema):
    """Invariant 7 / D5: a group excerpted into a per-axis framing section still
    carries the disclosure."""
    doc = _report()
    document_block = json.dumps(doc["not_derivable"], sort_keys=True)
    assert len(doc["not_derivable"]["statements"]) == 3
    for group in doc["groups"]:
        assert json.dumps(group["not_derivable"], sort_keys=True) == document_block


def test_constraint_completeness(real_package_path):
    """Invariant 5 / S4: both halves. Every catalog constraint appears exactly once
    in bounds and exactly once across reachable + unreachable."""
    contract = json.loads(
        (real_package_path / "contracts" / "model_contract.json").read_text()
    )
    catalog_ids = sorted(
        e["constraint_id"] for e in contract["constraint_catalog"]["concrete_entries"]
    )
    for group in _report()["groups"]:
        assert sorted(c["constraint_id"] for c in group["bounds"]) == catalog_ids
        partition = group["constraints_reachable"] + group["constraints_unreachable"]
        assert sorted(c["constraint_id"] for c in partition) == catalog_ids


def test_bounds_is_authoritative_and_axis_varying():
    """S2: the two partition lists are bounds filtered on 'any operand reached'."""
    doc = _report()
    for group in doc["groups"]:
        reachable = [c for c in group["bounds"] if any(o["reached"] for o in c["operands"])]
        assert reachable == group["constraints_reachable"]
        unreachable = [
            c for c in group["bounds"] if not any(o["reached"] for o in c["operands"])
        ]
        assert unreachable == group["constraints_unreachable"]
    by_axis = {g["axis"]: g["bounds"] for g in doc["groups"]}
    assert by_axis["R"] != by_axis["beta"]  # bounds vary per axis, not a constant block


def test_lists_are_sorted_by_a_stated_key():
    """D4: deterministic order, no set-iteration leaking through."""
    doc = _report()
    assert [g["axis"] for g in doc["groups"]] == sorted(g["axis"] for g in doc["groups"])
    assert [o["name"] for o in doc["objective_catalog"]] == sorted(
        o["name"] for o in doc["objective_catalog"]
    )
    for group in doc["groups"]:
        for key in ("bounds", "constraints_reachable", "constraints_unreachable"):
            ids = [c["constraint_id"] for c in group[key]]
            assert ids == sorted(ids)
        assert [k["key"] for k in group["declared_keys"]] == sorted(
            k["key"] for k in group["declared_keys"]
        )
        for key in ("objectives_reachable", "objectives_unreachable", "sibling_candidates"):
            assert group[key] == sorted(group[key])


def test_the_report_carries_its_tool_source_digest():
    """M5: emitted as {recipe, digest, files}, never a bare hash. The files list
    carries per-file digests so a record's tool revision names what it covered
    (Item 4 coordination, orchestrator 2026-08-20)."""
    tool = _report()["tool"]
    assert tool["path"] == "scripts/study/indicators.py"
    assert tool["source_digest"] == manifest.tool_source_digest()
    assert set(tool["source_digest"]) == {"recipe", "digest", "files"}
    assert all(set(f) == {"path", "sha256"} for f in tool["source_digest"]["files"])


def test_the_report_carries_the_three_package_fingerprints(real_package_path):
    package = _report()["package"]
    assert package["semantic_fingerprint"] == manifest.read_semantic_fingerprint(
        real_package_path
    )
    assert package["recorded_executable_fingerprint"] == manifest.read_executable_fingerprint(
        real_package_path
    )
    assert package["indicator_input_fingerprint"] == manifest.indicator_input_fingerprint(
        real_package_path
    )


def test_the_report_carries_no_timestamp():
    """A generation time would break the digest stability the record depends on;
    the record supplies the time."""
    text = _report_text()
    assert "timestamp" not in text
    assert "generated_at" not in text
