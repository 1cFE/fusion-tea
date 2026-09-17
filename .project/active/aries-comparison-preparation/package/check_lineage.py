"""Verify current comparison lineage and the actual indicator reader's read set.

Run from a repository checkout through .codex-test/run. This does not execute physics.
The historical integration proof is reused only if its source inputs are unchanged.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


BASE = "fe104e8d"
PACKAGE = "exploration/stellarator_e2e/generated"
INTEGRATION = "work/orchestration/goals/stellaris-reference-reconciliation/evidence/T-007_integration/integration_return.json"
SOURCE_PATHS = [
    "models", "exploration/stellarator_e2e/models", PACKAGE,
    "exploration/stellarator_e2e/verify_stellaris.py",
    "exploration/stellarator_e2e/studies/oracle_entry.py",
]


def check(root: Path) -> dict:
    sys.path.insert(0, str(root))
    from scripts.study import indicators, manifest

    prior = json.loads((root / INTEGRATION).read_text())
    assert prior["class"] == "CANDIDATE", "historical integration did not pass"
    expected = prior["candidate"]
    changed = subprocess.check_output(
        ["git", "diff", "--name-only", BASE, "--", *SOURCE_PATHS], cwd=root, text=True
    ).splitlines()
    assert not changed, f"source/package changed since reviewed integration: {changed}"
    tracked = set(subprocess.check_output(
        ["git", "ls-files", "--", "models", "exploration/stellarator_e2e/models"],
        cwd=root, text=True,
    ).splitlines())
    actual_models = {
        p.relative_to(root).as_posix()
        for base in (root / "models", root / "exploration/stellarator_e2e/models")
        for p in base.rglob("*.sysml") if p.is_file()
    }
    assert actual_models <= tracked, f"untracked model inputs: {sorted(actual_models-tracked)}"
    package = root / PACKAGE
    model_contract = json.loads((package / "contracts/model_contract.json").read_text())
    package_contract = json.loads((package / "contracts/package_contract.json").read_text())
    assert model_contract["semantic_fingerprint"] == expected["semantic_fingerprint"]
    assert package_contract["executable_fingerprint"] == expected["executable_fingerprint"]
    spec = importlib.util.spec_from_file_location("comparison_package_verify", package / "contracts/verify.py")
    verifier = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = verifier
    spec.loader.exec_module(verifier)
    seal = verifier.verify_package(package, "stellarator_tea", runtime_version="2.0.0", strict=True)
    assert seal.ok, str(seal.diagnostics)
    loaded = manifest.load(root / "exploration/stellarator_e2e/studies/manifest.json")
    manifest.assert_package_identity(loaded, package)
    fingerprint = manifest.indicator_input_fingerprint(package)
    manifest.assert_pin_matches(loaded, fingerprint)
    assert fingerprint["digest"] == expected["pin"]
    parsed = indicators.read_pipelines(package)
    read_paths = parsed.artifact_paths + [package / "contracts/model_contract.json"]
    manifest.assert_read_set_covered(read_paths, package, loaded)
    negative_checks = []
    for path in (package / "uncovered-input.json", root / "outside-package-input.json"):
        try:
            manifest.assert_read_set_covered([path], package, loaded)
        except manifest.ManifestError:
            negative_checks.append(path.name)
        else:
            raise AssertionError(f"read-set guard accepted {path}")
    graph = indicators.build_graph(parsed)
    return {
        "status": "pass",
        "source_checkpoint": subprocess.check_output(["git", "rev-parse", BASE], cwd=root, text=True).strip(),
        "entering_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip(),
        "historical_integration": INTEGRATION,
        "unchanged_source_paths": SOURCE_PATHS,
        "source_model_files": len(actual_models),
        "semantic_fingerprint": expected["semantic_fingerprint"],
        "executable_fingerprint": expected["executable_fingerprint"],
        "indicator_pin": fingerprint["digest"],
        "sealed_artifacts": len(package_contract["artifact_hashes"]),
        "read_set": [
            {"path": p.resolve().relative_to(package.resolve()).as_posix(),
             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(read_paths)
        ],
        "read_set_negative_checks": negative_checks,
        "produced_channels": len(graph.producer),
        "physical_evaluations": 0,
        "limitations": [
            "Historical ten-gate integration reused by unchanged-source and fresh seal checks, not rerun.",
            "Read-set coverage applies to this current parsed package; scripts/integrate.py itself is unchanged.",
            "Static L2/L6 limitations and sixteen prior independently unmapped native outputs remain.",
            "This proves numerical package lineage, not technology applicability or engineering qualification.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = check(args.root.resolve())
    except Exception as error:
        result = {"status": "failed", "error": f"{type(error).__name__}: {error}"}
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(result["status"])
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
