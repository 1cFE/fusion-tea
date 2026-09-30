"""Step 10 (full): compare every recorded non-constant channel of every stored case with the independent oracle and
re-derive every constraint verdict from the oracle's own operands through the package's predicate IR.

Tolerance (contract r3 section 8): a channel agrees when relative deviation < 1e-9 or absolute error < 1e-9 per unit.
Nonfinite values must agree exactly (same NaN-ness or same signed infinity). Any disagreement is recorded, not
adjusted. Constant formula channels are excluded and listed.

    .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" exec python <record>/verify_all.py'
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

RECORD = Path(__file__).resolve().parent
sys.path.insert(0, str(RECORD))
import oracle_entry  # noqa: E402
from scripts.study import common, verify  # noqa: E402
from scripts.study import manifest as manifest_mod  # noqa: E402

REL, ABS = 1e-9, 1e-9


def agree(native: float, independent: float) -> tuple[bool, float, float]:
    if not (math.isfinite(native) and math.isfinite(independent)):
        same = (math.isnan(native) and math.isnan(independent)) or (native == independent)
        return same, (0.0 if same else math.inf), (0.0 if same else math.inf)
    rel = common.relative_deviation(native, independent)
    err = abs(native - independent)
    return (rel < REL or err < ABS), rel, err


def main():
    cases = json.loads((RECORD / "results" / "cases.json").read_text())["cases"]
    catalog = json.loads((RECORD / "results" / "constraint_catalog.json").read_text())
    manifest = json.loads((RECORD / "manifest.json").read_text())
    bindings = oracle_entry.operand_bindings()
    constants = oracle_entry.constant_channels()
    package_inputs = verify.package_input_values(manifest_mod.repo_root() / manifest["package"]["path"])
    channels_checked = None
    worst = {"rel": (0.0, None, None), "abs": (0.0, None, None)}
    disagreements, mismatches, unique_seen = [], [], set()
    per_channel_worst = {}
    verdict_counts = Counter()
    for case in cases:
        if case["candidate_id"] in unique_seen:
            continue  # aliases share one stored evaluation; verified once per stored point
        unique_seen.add(case["candidate_id"])
        independent = oracle_entry.evaluate(case["inputs"])
        wanted = sorted(set(case["outputs"]) - set(constants))
        if channels_checked is None:
            channels_checked = wanted
        elif channels_checked != wanted:
            raise RuntimeError("channel set differs between cases")
        missing = [c for c in wanted if c not in independent]
        if missing:
            raise RuntimeError(f"oracle returned no value for {missing[:3]}")
        for channel in wanted:
            ok, rel, err = agree(case["outputs"][channel], independent[channel])
            pcw = per_channel_worst.setdefault(channel, {"rel": 0.0, "abs": 0.0})
            pcw["rel"] = max(pcw["rel"], rel if math.isfinite(rel) else 0.0)
            pcw["abs"] = max(pcw["abs"], err if math.isfinite(err) else 0.0)
            if math.isfinite(rel) and rel > worst["rel"][0]:
                worst["rel"] = (rel, case["case_id"], channel)
            if math.isfinite(err) and err > worst["abs"][0]:
                worst["abs"] = (err, case["case_id"], channel)
            if not ok:
                disagreements.append({"case_id": case["case_id"], "candidate_id": case["candidate_id"], "channel": channel,
                                      "native": case["outputs"][channel], "oracle": independent[channel],
                                      "relative_deviation": rel, "absolute_error": err})
        for constraint_id, recorded in case["verdicts"].items():
            entry = catalog[constraint_id]
            satisfied, resolved = verify.derive_verdict(constraint_id, entry, bindings, case["inputs"], package_inputs, independent)
            expected = "satisfied" if satisfied else "violated"
            verdict_counts[(entry["owner_instance_path"].split("__")[-1], entry["source_local_identity"], recorded)] += 1
            if recorded != expected:
                mismatches.append({"case_id": case["case_id"], "constraint_id": constraint_id,
                                   "source_local_identity": entry["source_local_identity"],
                                   "recorded": recorded, "rederived": expected})
    document = {
        "kind": "full-channel-oracle-verification/v1",
        "record": RECORD.name,
        "oracle": {"adapter": "oracle_entry.py (record-local name mapping)",
                   "source": "exploration/magnet_materials/oracle.py",
                   "source_sha256": hashlib.sha256((RECORD.parents[1] / "oracle.py").read_bytes()).hexdigest(),
                   "adapter_sha256": hashlib.sha256((RECORD / "oracle_entry.py").read_bytes()).hexdigest(),
                   "operand_bindings_digest": verify.bindings_digest(bindings)},
        "tolerance": {"relative": REL, "absolute_per_unit": ABS,
                      "rule": "agree when rel < 1e-9 or abs < 1e-9 (contract r3 section 8); nonfinite must match exactly"},
        "stored_points_verified": len(unique_seen), "declared_cases_covered": len(cases),
        "channels_checked": len(channels_checked), "channels_checked_list": channels_checked,
        "constant_channels_excluded": constants,
        "constraints_rederived": sorted(catalog),
        "verdicts_rederived": True,
        "worst_relative_deviation": {"value": worst["rel"][0], "case_id": worst["rel"][1], "channel": worst["rel"][2]},
        "worst_absolute_error": {"value": worst["abs"][0], "case_id": worst["abs"][1], "channel": worst["abs"][2]},
        "per_channel_worst": per_channel_worst,
        "verdict_counts": [{"material": m, "source_local_identity": s, "status": st, "count": n}
                           for (m, s, st), n in sorted(verdict_counts.items())],
        "disagreements": disagreements, "verdict_mismatches": mismatches,
        "outcome": "pass" if not disagreements and not mismatches else "fail",
    }
    common.write_document(document, RECORD / "results" / "verification_full.json")
    print(json.dumps({k: v for k, v in document.items() if k not in ("channels_checked_list", "per_channel_worst", "disagreements", "verdict_mismatches", "verdict_counts", "constraints_rederived")}, indent=1))
    print("disagreements", len(disagreements), "verdict mismatches", len(mismatches))
    return 0 if document["outcome"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
