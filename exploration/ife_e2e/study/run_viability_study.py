"""W4 acceptance: run the (eta, gain) viability grid through teax's study layer
against the sealed, regenerated fusion-tea IFE package, and build the
comparison table against sweep_ife.py's retiring hand rule.

Multi-entry via the stock bridge (Lifecycle Item 9): this package's whole-plant
`EntryPoint` (`pipelines/pipeline.yaml`) emits THREE channels (`hif_plant_params`,
`ife_plant_params`, `system_design`), and the swept fields live in *different*
channels — eta (`driver__efficiency`) in `ife_plant_params`, gain in
`hif_plant_params`. Stock teax handles this directly: `StudyDefinition` carries the
complete `entry_models` map (`PreparedEvaluator.entry_models`), and
`simkit.study.bridge.CandidateBridge` routes each swept field to its owning channel and
builds a complete typed model per channel (unselected fields keep their modeled defaults).
No consumer wrapper — the former `MultiChannelEvaluator` (which hardcoded the pre-Item-8
four-channel decomposition) is deleted; the plain `PreparedEvaluator` is the evaluator.

Run:  uv run python exploration/ife_e2e/study/run_viability_study.py
(fusion-tea's own venv; PYTHONPATH must carry teax's teax-simkit package — see wrapper
 shell invocation in the sibling `run.sh`.)
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

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
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    loader = ProvisionalPackageLoader(
        package_dir=PACKAGE_DIR, package_name=PACKAGE_NAME, link_root=LINK_ROOT
    )
    module, _ = loader.load()
    prepared = PreparedEvaluator(loader, SPEC_PATH)
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
    # Phase-3 gate: the IFE package carries exactly one eligible entry (B4, thin margin). Zero
    # cases means the viability constraint stopped being eligible — a regression, not an empty pass.
    if not cases:
        raise SystemExit(
            f"REGRESSION: no cases carry a verdict for {CONSTRAINT_ID!r} — the embedded catalog "
            "has zero eligible entries where exactly one was expected (B4)."
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
        rows.append({
            "eta": eta, "gain": gain, "eta_g": eta_g,
            "old_viable": old_viable, "new_verdict": verdict,
            "new_viable": new_viable, "at_boundary": at_boundary, "match": match,
        })

    out_csv = HERE / "acceptance_table.csv"
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
