"""Item 8 phase-3 gate: prove the canonical embedded-catalog seam end-to-end on the real,
license-regenerated IFE package (`generated/`, catalog_schema_version 2.0.0).

Scope (labelled honestly): this is a *representative* study run — one real evaluation of the
whole-plant package through teax's `StudyRunner`/store, then a `StudyQuery` that reads codegen's
embedded catalog straight from `contracts/model_contract.json` (no standalone
`constraint_catalog.json`, no materializer). It proves exactly what Item 8 delivers: the catalog
seam (`load_model_contract` + embedded-catalog `StudyQuery`) and the def→usage FK join. The full
2,301-point (eta, gain) acceptance sweep is Item 13's bar, not this phase's.

Multi-channel wiring is Item 9's stock `CandidateBridge` (zero/one/many channels), which this
proof now uses directly: `StudyDefinition` carries the complete `entry_models` map and the plain
`PreparedEvaluator` is the evaluator — no consumer wrapper. The candidate (the ife_plant_params
template values) routes to its channel; the other two channels keep their modeled defaults.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.definition import StudyDefinition
from simkit.study.identity import digest_of
from simkit.study.model_contract import load_model_contract
from simkit.study.policy import ObjectivePolicy
from simkit.study.query import StudyQuery
from simkit.study.runner import StudyRunner
from simkit.study.store import StudyStore
from simkit.study.strategy import PreparedListStrategy

HERE = Path(__file__).parent
E2E = HERE.parent
PACKAGE_DIR = (E2E / "generated").resolve()
PACKAGE_NAME = "ife_tea"
LINK_ROOT = Path("/tmp/ife_seam_pkg_link")
STORE_PATH = HERE / "_work" / "catalog_seam.db"
SPEC_PATH = PACKAGE_DIR / "pipelines" / "pipeline.yaml"
INPUTS = PACKAGE_DIR / "inputs"

CONSTRAINT_ID = "hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b"


def _clean_build_artifacts() -> None:
    """Remove stale `.pytest_cache` dirs left inside the sealed package tree (audit N1).

    The package's own pytest run drops `generated/tests/.pytest_cache/`, an EXTRA file the
    Item-7 seal verifier rejects (`SealVerificationError`) before this proof can load the
    package. A reproducer must start from a clean tree, so sweep them first.
    """
    for cache in PACKAGE_DIR.rglob(".pytest_cache"):
        if cache.is_dir():
            shutil.rmtree(cache, ignore_errors=True)


def main() -> None:
    _clean_build_artifacts()
    STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if STORE_PATH.exists():
        STORE_PATH.unlink()

    loader = ProvisionalPackageLoader(
        package_dir=PACKAGE_DIR, package_name=PACKAGE_NAME, link_root=LINK_ROOT
    )
    loader.load()
    prepared = PreparedEvaluator(loader, SPEC_PATH)
    # Stock Item-9 multi-channel bridge: plain PreparedEvaluator, no consumer wrapper.
    evaluator = prepared

    # One representative candidate: the ife_plant_params template values themselves.
    # The stock bridge routes them to their channel; the other two channels default.
    candidate = json.loads((INPUTS / "ife_plant_params.json").read_text())

    definition = StudyDefinition(
        study_id="ife-catalog-seam-proof",
        entry_models=prepared.entry_models,
        strategy=PreparedListStrategy([candidate]),
        validate_proposal=lambda raw: dict(raw),
        policy=ObjectivePolicy(objectives=(), response_roles={}),
        executable_fingerprint=prepared.fingerprint,
        # Item 8: bind the real semantic_fingerprint, read via the embedded-catalog seam.
        model_contract_fingerprint=load_model_contract(PACKAGE_DIR).semantic_fingerprint,
        input_schema_version="input-v1",
        evidence_schema_version=prepared.EVIDENCE_SCHEMA_VERSION,
        study_definition_fingerprint=digest_of({"proof": "catalog-seam"}),
    )

    store = StudyStore.create_or_open(STORE_PATH, definition.compatibility())
    store.acquire_lease()
    StudyRunner(store, definition, evaluator).run()
    store.release_lease()
    store.close()

    # --- The Item-8 catalog seam: query reads the embedded catalog from the package dir. ---
    store = StudyStore(STORE_PATH)
    query = StudyQuery(store, PACKAGE_DIR)
    cases = query.cases(constraint=CONSTRAINT_ID)
    if not cases:
        raise SystemExit(
            f"REGRESSION: no case carries a verdict for {CONSTRAINT_ID!r} — the embedded catalog "
            "has zero eligible entries where exactly one was expected (B4)."
        )
    view = cases[0].catalog[CONSTRAINT_ID]
    verdict = cases[0].verdicts[CONSTRAINT_ID]
    store.close()

    print("=== Item 8 catalog-seam proof (representative run; full sweep is Item 13) ===")
    print(f"schema_version : {load_model_contract(PACKAGE_DIR).catalog_schema_version}")
    print(f"eligible entries carrying a verdict for the viability constraint: {len(cases)}")
    print(f"constraint_id  : {view.constraint_id}")
    print(f"source_form    : {view.source_form}")
    print(f"owner_qn       : {view.owner_qn}")
    print(f"definition_qn  : {view.definition_qn}   <- Item-8 def->usage join, read from the entry")
    print(f"verdict        : {verdict}")
    assert view.source_form == "definition_typed"
    assert view.definition_qn == "fusion_cycle::'Viability Threshold'"
    print("PASS: embedded catalog consumed directly; def->usage join present; >=1 eligible entry.")


if __name__ == "__main__":
    main()
