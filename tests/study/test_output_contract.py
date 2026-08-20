"""The output, manifest, and digest recipes as a fixed seam.

Covers the recipes and the strict manifest validator (Phase 1), the real manifest
against its schema and its live pin (Phase 2), and — from Phase 7 — byte
determinism, schema validation of real output, disclosure parity, and constraint
completeness.
"""

import subprocess
import sys

import pytest

from scripts.study import manifest


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
    assert "pipelines/mfe_stellarator.yaml" in files
    assert "contracts/model_contract.json" in files
    assert sum(1 for p in files if p.startswith("inputs/")) == 3
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
