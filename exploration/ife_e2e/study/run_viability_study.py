"""Replay the historical eta-gain heuristic comparison on the repaired IFE package.

The named net_positive verdict and generating output are recorded separately.
Only eligible prices enter the table; passing the heuristic alone is insufficient.
The stock multi-entry bridge supplies all other modeled defaults.
Use --limit N for an N-by-N smoke grid and --output-dir PATH to retain new outputs.
Historical study artifacts remain unchanged."""

from __future__ import annotations

import csv
import argparse
import json
import tempfile
from pathlib import Path

from exploration.ife_e2e.eligibility import NET_POSITIVE_ID, P, price_eligible

from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.definition import StudyDefinition
from simkit.study.identity import digest_of
from simkit.study.policy import ObjectivePolicy
from simkit.study.query import StudyQuery
from simkit.study.store import StudyStore
from simkit.study.strategy import GridStrategy

HERE = Path(__file__).parent
E2E = HERE.parent
PACKAGE_DIR = (E2E / "generated").resolve()
PACKAGE_NAME = "ife_tea"
LINK_ROOT = Path("/tmp/ife_study_pkg_link")
STORE_PATH = HERE / "_work" / "viability_study.db"
SPEC_PATH = PACKAGE_DIR / "pipelines" / "pipeline.yaml"

ETA_FIELD = "hif_plant_pkg__hif_plant__driver__efficiency"
GAIN_FIELD = "hif_plant_pkg__hif_plant__gain"
CONSTRAINT_ID = "hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b"
ETA_G_MIN = 10.0  # the retiring hand rule (sweep_ife.py:82), STRICT >

# Same domains as exploration/ife_e2e/sweep_ife.py's ETA_GRID/G_GRID (D4: one-run,
# apples-to-apples replay against the about-to-be-deleted hand rule).
ETA_GRID = [0.02 + 0.01 * i for i in range(39)]
G_GRID = [10.0 + 5.0 * i for i in range(59)]
EPS = 1e-9  # boundary window for eta*gain vs the threshold (NTH4; float grid arithmetic)


def build_definition(prepared: PreparedEvaluator) -> StudyDefinition:
    grid = [(ETA_FIELD, ETA_GRID), (GAIN_FIELD, G_GRID)]
    strategy = GridStrategy(grid)

    def validate_proposal(raw):
        canonical = {}
        for name in (ETA_FIELD, GAIN_FIELD):
            value = raw.get(name)
            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return None
            canonical[name] = float(value)
        return canonical

    policy = ObjectivePolicy(objectives=(), response_roles={})
    return StudyDefinition(
        study_id="ife-viability-acceptance",
        entry_models=prepared.entry_models,
        strategy=strategy,
        validate_proposal=validate_proposal,
        policy=policy,
        executable_fingerprint=prepared.fingerprint,
        model_contract_fingerprint=digest_of(
            json.loads((PACKAGE_DIR / "contracts" / "model_contract.json").read_text())
        ),
        input_schema_version="input-v1",
        evidence_schema_version=prepared.EVIDENCE_SCHEMA_VERSION,
        study_definition_fingerprint=digest_of({"grid": [[n, d] for n, d in grid]}),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    output = args.output_dir or Path(tempfile.mkdtemp(prefix="ife-study-"))
    output.mkdir(parents=True, exist_ok=True)
    global STORE_PATH, ETA_GRID, G_GRID
    STORE_PATH = output / "viability_study.db"
    if args.limit:
        ETA_GRID, G_GRID = ETA_GRID[:args.limit], G_GRID[:args.limit]
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    loader = ProvisionalPackageLoader(
        package_dir=PACKAGE_DIR, package_name=PACKAGE_NAME, link_root=output / "pkg"
    )
    module, _ = loader.load()
    prepared = PreparedEvaluator(loader, SPEC_PATH, expects_constraint_report=True)
    # Stock teax multi-channel bridge — the plain PreparedEvaluator is the evaluator.
    evaluator = prepared
    definition = build_definition(prepared)

    if STORE_PATH.exists():
        STORE_PATH.unlink()
    store = StudyStore.create_or_open(STORE_PATH, definition.compatibility())
    store.acquire_lease()
    from simkit.study.runner import StudyRunner

    StudyRunner(store, definition, evaluator).run()
    store.release_lease()
    store.close()

    # --- Acceptance table: old hand rule vs new generated verdict ----------
    store = StudyStore(STORE_PATH)
    # Item 8: read codegen's embedded catalog straight from the package dir's model_contract.json.
    # No standalone constraint_catalog.json, no materializer.
    query = StudyQuery(store, PACKAGE_DIR)
    cases = query.cases(constraint=CONSTRAINT_ID)
    # Query the named viability verdict; net_positive is a separate physical gate.
    if not cases:
        raise SystemExit(
            f"REGRESSION: no cases carry a verdict for {CONSTRAINT_ID!r} — the embedded catalog "
            "did not return the named viability verdict."
        )
    print(f"{len(cases)} cases carry a verdict for {CONSTRAINT_ID!r} "
          f"(of {len(ETA_GRID) * len(G_GRID)} grid points)")

    rows = []
    mismatches = 0
    boundary_rows = 0
    for case in cases:
        eta = case.inputs[ETA_FIELD]
        gain = case.inputs[GAIN_FIELD]
        eta_g = eta * gain
        old_viable = eta_g > ETA_G_MIN  # sweep_ife.py:82, strict >
        verdict = case.verdicts[CONSTRAINT_ID]  # satisfied | violated | indeterminate
        new_viable = verdict == "satisfied"
        at_boundary = abs(eta_g - ETA_G_MIN) <= EPS
        match = (old_viable == new_viable) or at_boundary
        if at_boundary:
            boundary_rows += 1
        if not match:
            mismatches += 1
        net_positive = case.verdicts.get(NET_POSITIVE_ID)
        price = case.outputs.get(P + "hawker_price__price")
        generating = case.outputs.get(P + "hawker_price__generating")
        eligible = price_eligible(price, generating, net_positive)
        rows.append({
            "eta": eta, "gain": gain, "eta_g": eta_g,
            "net_positive": net_positive, "generating": generating,
            "price_eligible": eligible,
            "hawker_price": price if eligible else None,
            "old_viable": old_viable, "new_verdict": verdict,
            "new_viable": new_viable, "at_boundary": at_boundary, "match": match,
        })

    out_csv = output / "acceptance_table.csv"
    with out_csv.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    total = len(rows)
    print(f"wrote {out_csv}: {total} rows, {mismatches} non-boundary mismatch(es), "
          f"{boundary_rows} boundary row(s) flagged")
    if mismatches:
        raise SystemExit(f"{mismatches} unexplained mismatch(es) — see {out_csv}")
    print("ACCEPTANCE: 100% agreement (modulo flagged boundary rows)")


if __name__ == "__main__":
    main()
