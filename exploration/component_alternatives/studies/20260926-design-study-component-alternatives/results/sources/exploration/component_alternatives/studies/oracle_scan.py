"""Scan declared inputs with the independent oracle before fixing a native window.

The loop visits explicit choices once. It never solves for a chosen source, ratio,
equipment rating or price. Native study execution remains the stock route's job.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.study import common, manifest, verify
from exploration.component_alternatives.studies import oracle_entry, study_route


def scan(proposals_path: Path, integration_path: Path, out_path: Path):
    if out_path.exists():
        raise ValueError("scan evidence exists; use a distinct output path")
    loaded = manifest.load(study_route.MANIFEST_PATH)
    integration = common.read_json(integration_path, "integration return")
    candidate = integration.get("candidate") or {}
    interface = study_route.interface()
    if integration.get("class") != "CANDIDATE":
        raise ValueError("scan requires a native integration candidate")
    for key, value in (("executable_fingerprint", interface["executable_fingerprint"]),
                       ("semantic_fingerprint", interface["semantic_fingerprint"]),
                       ("pin", loaded.pinned_digest)):
        if candidate.get(key) != value:
            raise ValueError(f"integration identity differs: {key}")
    common.assert_tree_clean(study_route.PACKAGE_DIR)
    manifest.assert_pin_matches(loaded, manifest.indicator_input_fingerprint(study_route.PACKAGE_DIR))
    proposals = common.read_json(proposals_path, "explicit scan choices")["cases"]
    catalog = study_route._catalog_by_constraint_id(study_route.PACKAGE_DIR)
    bindings = oracle_entry.operand_bindings()
    baseline = loaded.data["baseline"]["point"]
    rows = []
    for proposal in proposals:
        point = proposal["point"]
        if study_route.validate_proposal(point) is None:
            raise ValueError(f"incomplete proposal: {proposal['case']}")
        row = dict(proposal)
        try:
            outputs = oracle_entry.evaluate(point)
        except ValueError as exc:
            row.update(status="oracle_refusal", error=str(exc),
                       interpretation="Review this exact refusal before fixing the executable window.")
        else:
            verdicts = {cid: "satisfied" if verify.derive_verdict(
                cid, entry, bindings, point, baseline, outputs)[0] else "violated"
                for cid, entry in catalog.items()}
            # Keep all predicate identities and the relevant result/state channels.
            # The native store and verification will retain/check the full catalog.
            selected = {key: value for key, value in outputs.items() if any(
                tag in key for tag in ("__steam_ledger__", "__gas_ledger__",
                    "__primary_loop__", "__gas_boundary__", "__steam_boundary__",
                    "__water_ic1__", "__water_ic2__", "__water_pre__"))}
            row.update(status="evaluated", verdicts=verdicts, outputs=selected,
                       all_checks_satisfied=all(value == "satisfied" for value in verdicts.values()),
                       independently_calculated_channels=len(outputs))
        rows.append(row)
    result = {"kind": "independent-oracle-window-scan", "integration_candidate": candidate,
              "proposal_sha256": hashlib.sha256(proposals_path.read_bytes()).hexdigest(),
              "cases": rows}
    with out_path.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    common.assert_tree_clean(study_route.PACKAGE_DIR)
    summary = {"cases": len(rows), "evaluated": sum(r["status"] == "evaluated" for r in rows),
               "refused": sum(r["status"] == "oracle_refusal" for r in rows),
               "all_checks_satisfied": sum(r.get("all_checks_satisfied", False) for r in rows)}
    print(json.dumps(summary))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposals", type=Path, required=True)
    parser.add_argument("--integration-return", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    scan(args.proposals, args.integration_return, args.out)
