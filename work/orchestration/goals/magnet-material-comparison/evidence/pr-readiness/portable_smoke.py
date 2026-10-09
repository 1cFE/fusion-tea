"""Replay four sealed supplied designs without machine-local study inputs/stores.

Reuses the sealed executor and full-channel verifier. Only the case-data provider
is replaced by the explicitly hashed four-case fixture; identity gates are intact.
"""

import hashlib
import json
import multiprocessing as mp
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
RECORD = ROOT / "exploration/stellarator_materials/studies/20260930-magnet-material-plant-map"
FIXTURE_SHA = "3f928da333892c68c5b2290e6db3a1878409208dbd8dff068324bc97a6201e76"


def main():
    raw = (HERE / "portable-smoke-fixture.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == FIXTURE_SHA
    fixture = json.loads(raw)
    assert (
        hashlib.sha256((RECORD / "snapshot.json").read_bytes()).hexdigest()
        == fixture["sources"]["snapshot_sha256"]
    )
    snapshot = json.loads((RECORD / "snapshot.json").read_text())
    source_checks = {}
    source_blocks = [t["source_digest"] for t in snapshot["tools"]]
    source_blocks += [
        a["manifest"]["content_used"]["oracle"]["source_digest"] for a in snapshot["arms"]
    ]
    for block in source_blocks:
        for source in block["files"]:
            path = ROOT / source["path"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"], path
            source_checks[source["path"]] = source["sha256"]
    for case in fixture["cases"] + fixture["supporting_cases"]:
        assert (
            hashlib.sha256(
                json.dumps(case, sort_keys=True, separators=(",", ":")).encode()
            ).hexdigest()
            == fixture["case_hashes"][case["case_id"]]
        )
    sys.path.insert(0, str(RECORD))
    import execute_study as execution
    import record_common as rc
    import verify_all as verification

    # Explicit portable data injection. Neither ignored case list nor oracle scan
    # is read; a fresh results root owns every generated file.
    rc.load_cases = lambda check=True: {"cases": fixture["cases"]}
    root = Path(tempfile.mkdtemp(prefix="magnet-portable-smoke-"))
    rc.CASES = root / "deliberately-absent-cases.json"
    rc.RESULTS = root
    assert not rc.CASES.exists() and not (root / "oracle_scan.json").exists()
    for unit in rc.MATERIALS:
        execution.execute(
            unit,
            ROOT
            / "work/orchestration/goals/magnet-material-comparison/evidence"
            / f"integration-r3-{unit}/integration_return.json",
            out_root=root,
        )
    declared = {c["case_id"]: c for c in fixture["cases"]}
    by_id = {c["case_id"]: c for c in fixture["cases"] + fixture["supporting_cases"]}
    scan = {c["case_id"]: c for c in fixture["scan_rows"]}
    units = {}
    with mp.get_context("fork").Pool(2) as pool:
        for unit in rc.MATERIALS:
            units[unit], _ = verification.verify_unit(unit, pool, root, scan, declared, by_id)
    failed = any(
        u[k]
        for u in units.values()
        for k in (
            "disagreements",
            "verdict_mismatches",
            "refusal_mismatches",
            "status_mismatches_against_scan",
        )
    )
    receipt = {
        "scope": "four-case portable regression; no full replay claim",
        "fixture_sha256": FIXTURE_SHA,
        "source_snapshot_sha256": fixture["sources"]["snapshot_sha256"],
        "results_root": str(root),
        "sealed_source_hashes_checked": source_checks,
        "ignored_case_list_and_scan_used": False,
        "case_count": sum(u["cases"] for u in units.values()),
        "scalar_comparisons": sum(u["channel_comparisons"] for u in units.values()),
        "tolerance": {"relative": verification.REL, "absolute_per_unit": verification.ABS},
        "units": units,
        "outcome": "fail" if failed else "pass",
    }
    rc.write_json(receipt, root / "portable-smoke-receipt.json")
    assert not failed, root
    print(
        json.dumps(
            {k: v for k, v in receipt.items() if k not in ("units", "sealed_source_hashes_checked")}
        )
    )


if __name__ == "__main__":
    main()
