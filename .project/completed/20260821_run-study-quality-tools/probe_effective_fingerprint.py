"""THROWAWAY design probe (RUN-STUDY Item 4).

Three questions the design rests on:

  P1. Does the era stack accept a loader that returns an *effective* executable
      fingerprint instead of the sealed one? (i.e. is the whole effective-
      fingerprint plan a one-line change at the loader seam, or does something
      downstream cross-check against the seal?)
  P2. Does an existing store then refuse to reopen under a changed effective
      fingerprint? (the lineage-refusal proof's mechanism)
  P3. Re-run the item-start loader probe: how many sealed artifacts differ?

Run:  uv run python .project/active/run-study-quality-tools/probe_effective_fingerprint.py
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
E2E = REPO / "exploration" / "stellarator_e2e"
TEAX_V1 = "/home/reid/1cfe/teax-v1-era/packages/teax-simkit"
sys.path.insert(0, TEAX_V1)
sys.path.insert(0, str(E2E))

import verify_stellaris as vs  # noqa: E402

from simkit.evaluation import package_load as _pl  # noqa: E402
from simkit.evaluation.evaluator import PreparedEvaluator  # noqa: E402
from simkit.evaluation.package_load import ProvisionalPackageLoader  # noqa: E402
from simkit.study.definition import StudyDefinition  # noqa: E402
from simkit.study.identity import digest_of  # noqa: E402
from simkit.study.policy import ObjectivePolicy  # noqa: E402
from simkit.study.query import StudyQuery  # noqa: E402
from simkit.study.runner import StudyRunner  # noqa: E402
from simkit.study.store import StudyStore  # noqa: E402
from simkit.study.strategy import PreparedListStrategy  # noqa: E402

PKG = E2E / "generated"
SPEC = PKG / "pipelines" / "mfe_stellarator.yaml"
P = "stellarator_09__stellaris__"
GLUE_EDITED = {"pipelines/mfe_stellarator.yaml", "inputs/system_design.json"}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------- P3
def probe_seal() -> None:
    seal = json.loads((PKG / "contracts" / "package_contract.json").read_text())
    hashes = seal["artifact_hashes"]
    bad = [rel for rel, want in hashes.items() if sha256_file(PKG / rel) != want]
    print(f"[P3] runtime_contract_version={seal['runtime_contract_version']} "
          f"artifacts={len(hashes)} differing={len(bad)} -> {sorted(bad)}")


# ---------------------------------------------------------------- adapter shape
class ProbeAdapterLoader:
    """The promoted shape: accept exactly the documented glue edits, return the
    EFFECTIVE fingerprint, not the sealed one."""

    def __init__(self, inner: ProvisionalPackageLoader, adapter_source: bytes) -> None:
        self._inner = inner
        self._adapter_source = adapter_source
        self.identity: dict = {}

    def load(self):
        pdir = self._inner.package_dir
        seal = json.loads((pdir / "contracts" / "package_contract.json").read_text())
        version = seal.get("runtime_contract_version")
        if version not in _pl.ACCEPTED_RUNTIME_CONTRACT_VERSIONS:
            raise _pl.SealVerificationError(f"era mismatch: {version}")
        verify = _pl._load_authenticated_verifier(pdir)
        result = verify.verify_package(
            pdir, self._inner.package_name, runtime_version=version, strict=True
        )
        offenders = {(d.kind, d.path) for d in result.diagnostics}
        unexpected = offenders - {("TAMPER", p) for p in GLUE_EDITED}
        if unexpected:
            raise _pl.SealVerificationError(f"beyond documented glue: {unexpected}")

        modified = {rel: sha256_file(pdir / rel) for rel in sorted(GLUE_EDITED)}
        adapter_digest = hashlib.sha256(self._adapter_source).hexdigest()
        canon = "\n".join(
            ["effective-executable-fingerprint/v1",
             f"sealed {seal['executable_fingerprint']}"]
            + [f"modified {rel} {dig}" for rel, dig in modified.items()]
            + [f"adapter {adapter_digest}"]
        ) + "\n"
        effective = hashlib.sha256(canon.encode("utf-8")).hexdigest()
        self.identity = {
            "sealed_executable_fingerprint": seal["executable_fingerprint"],
            "allowed_modified_files": modified,
            "adapter_source_digest": adapter_digest,
            "effective_executable_fingerprint": effective,
        }
        return self._inner._load_module(), effective


def oracle_at(**overrides):
    saved = dict(vs.IN)
    vs.IN.update(overrides)
    try:
        return vs.compute()
    finally:
        vs.IN.clear()
        vs.IN.update(saved)


def proposal(R: float, a: float, availability: float) -> dict[str, float]:
    o = oracle_at(R=R, a=a, magnet_R0=R)
    sm = o["special_materials"]
    f = {
        f"{P}cas23_to_28_capital__special_materials_capital": sm,
        f"{P}cas2x_pre_contingency__special_materials_capital": sm,
        f"{P}cas23_to_28_capital__cas28_capital": 5_000_000.0,
        f"{P}cas2x_pre_contingency__cas28_capital": 5_000_000.0,
        f"{P}replacement_cost_per_event__n_mod": 1.0,
        "mfe_plant__MFE_Power_Plant__p_th": o["p_th"],
        "mfe_plant__MFE_Power_Plant__p_the": o["p_the"],
        "mfe_plant__MFE_Power_Plant__p_et": o["p_et"],
        f"{P}geom__R": R, f"{P}rb__R": R, f"{P}magnet__R0": R,
        f"{P}geom__a": a, f"{P}rb__a": a,
    }
    for k in ("cas72_calc", "fuel_calc", "lcoe_calc", "lcoe_1cfe_calc"):
        f[f"{P}{k}__availability"] = availability
    return f


def validate_proposal(raw):
    out = {}
    for k, v in raw.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return None
        out[k] = float(v)
    return out


def build_definition(prepared, proposals, study_id):
    return StudyDefinition(
        study_id=study_id,
        entry_models=prepared.entry_models,
        strategy=PreparedListStrategy(proposals),
        validate_proposal=validate_proposal,
        policy=ObjectivePolicy(objectives=(), response_roles={}),
        executable_fingerprint=prepared.fingerprint,
        model_contract_fingerprint=digest_of(
            json.loads((PKG / "contracts" / "model_contract.json").read_text())
        ),
        input_schema_version="input-v1",
        evidence_schema_version=prepared.EVIDENCE_SCHEMA_VERSION,
        study_definition_fingerprint=digest_of(
            {"proposals": [sorted(p.items()) for p in proposals]}
        ),
    )


def main() -> None:
    probe_seal()
    work = Path(tempfile.mkdtemp(prefix="item4probe-"))

    # ---- P1: run 3 points under the effective fingerprint --------------
    loader = ProbeAdapterLoader(
        ProvisionalPackageLoader(package_dir=PKG, package_name="stellarator_tea",
                                 link_root=work / "pkg_link"),
        adapter_source=b"# probe adapter source v1\n",
    )
    prepared = PreparedEvaluator(loader, SPEC)
    print(f"[P1] sealed    = {loader.identity['sealed_executable_fingerprint']}")
    print(f"[P1] effective = {prepared.fingerprint}")
    assert prepared.fingerprint != loader.identity["sealed_executable_fingerprint"]

    proposals = [proposal(12.7, 1.3, 0.85), proposal(14.0, 1.65, 0.85),
                 proposal(5.0, 1.0, 0.85)]
    db = work / "probe.db"
    definition = build_definition(prepared, proposals, "item4-probe-v1")
    store = StudyStore.create_or_open(db, definition.compatibility())
    store.acquire_lease()
    StudyRunner(store, definition, prepared).run()
    store.release_lease()
    store.close()

    cases = StudyQuery(StudyStore(db), PKG).cases()
    done = [c for c in cases if c.state == "completed"]
    print(f"[P1] {len(done)}/{len(cases)} completed")
    bl = done[0]
    lcoe = bl.outputs[f"{P}lcoe_calc__lcoe"]
    pinned = 275.264220042
    print(f"[P1] baseline LCOE={lcoe!r} rel={abs(lcoe - pinned) / pinned:.2e} "
          f"verdicts={ {k.rsplit('__', 2)[-2]: v for k, v in bl.verdicts.items()} }")
    print(f"[P1] evidence provenance fingerprint == effective: "
          f"{bl.executable_fingerprint == prepared.fingerprint}")

    # ---- P2: reopen the same store under a changed effective fingerprint
    loader2 = ProbeAdapterLoader(
        ProvisionalPackageLoader(package_dir=PKG, package_name="stellarator_tea",
                                 link_root=work / "pkg_link2"),
        adapter_source=b"# probe adapter source v2 (behaviour changed)\n",
    )
    prepared2 = PreparedEvaluator(loader2, SPEC)
    print(f"[P2] effective after adapter-source change = {prepared2.fingerprint}")
    definition2 = build_definition(prepared2, proposals, "item4-probe-v1")
    try:
        StudyStore.create_or_open(db, definition2.compatibility())
        print("[P2] FAIL — store accepted a different effective fingerprint")
    except Exception as exc:  # noqa: BLE001
        print(f"[P2] refused as designed: {type(exc).__name__}: {str(exc)[:120]}...")

    print(f"[probe] scratch: {work}")


if __name__ == "__main__":
    main()
