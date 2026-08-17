"""Design-search proof of life: (R, a) grid + availability sweep through the
stock teax study layer, on the committed Stellaris generated package.

What this is: the first real design-search study on the stellarator demo model
(epic Item 5, first cut). Two studies run through teax's delivered study
machinery (PreparedListStrategy -> StudyRunner -> StudyStore -> StudyQuery, no
hand-rolled sweep loops):

  A. 2D grid over the two causal geometry levers — major radius R, minor
     radius a — LCOE + all 5 viability verdicts recorded per point.
  B. 1D sweep over availability (operations lever), same recording.

Axis rule compliance (.project/active/demo-study-parameterization-policy/policy.md §2):
axes are causal design levers, declared at the SysML-attribute level and
expanded to their complete entry-key set (the AXES map below). `magnet__R0`
rides with R as a DECLARED PHYSICAL-IDENTITY TIE [AGENT]: the magnet-cost
Ampere's-law current runs on the major radius (total_kAm = G*B*R0*r_coil/mu0)
— same physical quantity, separately authored attribute, so it is recorded
here as a tie, not as mechanical fan-out of one attribute.

Era pin: current teax main refuses this package's v1.0.0 seal (fail-closed
re-vendor at CONSTRAINT-SEMANTICS Item 3). The studies therefore run against
a read-only git worktree of teax at fa0e06a — the commit that built the study
layer, the same v1 era that generated and certified this package (and the
July IFE 2,301-point study). Nothing in teax or sysml-codegen is modified.

GLUE LEDGER (everything the harness supplies that the model does not; all
inherited from the documented WI-018/WI-028/WI-029 glue, one rung added):
  g1. The two seal exceptions: `pipelines/mfe_stellarator.yaml` and
      `inputs/system_design.json` differ from their sealed hashes by exactly
      the committed glue-1 edits (BOP repoint + 3 schema fillers).
      GlueAwareLoader below verifies every OTHER sealed artifact and refuses
      anything beyond those two files.
  g2. Constant injections per proposal: cas28_capital (2 keys, 5.0 M$ costing
      constant), replacement n_mod (1.0, the declared default codegen could
      not resolve), and the 3 dead `mfe_plant__MFE_Power_Plant__p_*` schema
      fillers (nothing reads them — asserted below).
  g3. `special_materials_capital` (2 keys): CAS27 is a function of the
      radial-build blanket volume, which the package cannot wire cross-part.
      NEW RUNG, loudly: it is recomputed PER POINT from the same formula the
      oracle uses (blanket_vol x 0.50 x 9400 x 5.0), so off-baseline points
      stay self-consistent. Consequence for verification: the oracle-parity
      check verifies the package's arithmetic GIVEN this injected value; the
      CAS27 ingredient itself is glue-fed on both sides and is NOT
      independently verified.

Verification (in `verify`): the baseline grid point must reproduce the pinned
headline exactly (LCOE 275.264220042, all 5 verdicts satisfied); K random
off-baseline points are recomputed by the independent pure-Python oracle
(verify_stellaris.py) at rel < 1e-9 on named channels; verdicts are re-derived
from oracle operands against the package's bound limits; and the committed
package must be byte-untouched after every run (git-clean gate).

Run (from exploration/stellarator_e2e/):
    uv run python study/run_design_search.py run      # both studies + gates
    uv run python study/run_design_search.py verify   # oracle spot-checks
"""
from __future__ import annotations

import argparse
import csv
import functools
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
E2E = HERE.parent
TEAX_V1 = "/home/reid/1cfe/teax-v1-era/packages/teax-simkit"
sys.path.insert(0, TEAX_V1)
sys.path.insert(0, str(E2E))

import verify_stellaris as vs  # noqa: E402  (the independent oracle)

# The profile integral depends only on (alpha_n, alpha_T, T_i0) — none of the
# swept axes — so memoizing it is exact, not an approximation.
vs._profile_integral = functools.lru_cache(maxsize=None)(vs._profile_integral)

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

PACKAGE_DIR = E2E / "generated"
SPEC_PATH = PACKAGE_DIR / "pipelines" / "mfe_stellarator.yaml"
WORK = HERE / "_work"
P = "stellarator_09__stellaris__"

# --- Axis declarations: SysML attribute -> complete entry-key expansion -----
AXES = {
    "R": [f"{P}geom__R", f"{P}rb__R"],
    "a": [f"{P}geom__a", f"{P}rb__a"],
    "availability": [
        f"{P}cas72_calc__availability",
        f"{P}fuel_calc__availability",
        f"{P}lcoe_calc__availability",
        f"{P}lcoe_1cfe_calc__availability",
    ],
}
# Declared physical-identity tie [AGENT], not mechanical fan-out (see docstring).
R_TIE = f"{P}magnet__R0"

BASELINE = {"R": 12.7, "a": 1.3, "availability": 0.85}
PINNED_LCOE = 275.264220042  # the WI-029 executed headline
# Geometric validity: the plasma plus the held-fixed radial-build stack
# (vacuum 0.10 + firstwall 0.05 + blanket 0.80 + reflector 0.20 + ht_shield
# 0.20 + structure 0.15 + gap1 0.10 + vessel 0.10 + coil 0.30 + gap2 0.10 +
# lt_shield 0.15 = 2.25 m) must fit inside the major radius or the torus
# self-intersects. Derived bound from held-fixed inputs, not a design screen.
BUILD_STACK_M = 2.25

# Study windows — [AGENT] exploration windows chosen by oracle pre-scan so the
# constraint boundaries sit in-frame. NOT sourced design bounds, and the runs
# therefore do not test policy §7 H1 (the window is engineered).
R_VALUES = [round(4.0 + 0.5 * i, 2) for i in range(33)]      # 4.0 .. 20.0 m
A_VALUES = [round(0.80 + 0.05 * i, 2) for i in range(29)]    # 0.80 .. 2.20 m
AVAIL_VALUES = [round(0.50 + 0.025 * i, 3) for i in range(19)]  # 0.50 .. 0.95

# Recorded-channel limitation (era evidence layer): only single-field float
# channels land in the study store's `outputs`. The power-balance channels
# (pb__p_net, pb__q_eng, ...) are fields of one multi-field model and are NOT
# recorded — p_net/q_eng reach the record only through their verdicts
# (net_positive's predicate is exactly p_net > 0). Export what is recorded.
CHANNELS = {
    "lcoe": f"{P}lcoe_calc__lcoe",
    "wall_load": f"{P}wall_load_calc__wall_load",
    "p_fus": f"{P}fusion__p_fus",
    "plasma_volume": f"{P}geom__V",
    "total_capital": f"{P}total_capital__total_capital",
    "magnet_capital": f"{P}magnet_cost__capital_cost",
    "overnight_capital": f"{P}overnight_capital__overnight_capital",
    "lcoe_1cfe": f"{P}lcoe_1cfe_calc__lcoe",
}


def oracle_at(**overrides):
    """The independent oracle at a swept point (module IN saved/restored)."""
    saved = dict(vs.IN)
    vs.IN.update(overrides)
    try:
        return vs.compute()
    finally:
        vs.IN.clear()
        vs.IN.update(saved)


# --- Glue rung g1: precisely-scoped seal exception --------------------------
GLUE_EDITED = {"pipelines/mfe_stellarator.yaml", "inputs/system_design.json"}


class GlueAwareLoader:
    """ProvisionalPackageLoader accepting EXACTLY the documented glue edits.

    Runs the era's full verification (version gate, authenticated verifier,
    per-file hashes) and accepts only if every diagnostic is a TAMPER on one
    of the two glue-edited files. Any other diagnostic still refuses.
    """

    def __init__(self, inner: ProvisionalPackageLoader) -> None:
        self._inner = inner

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
        return self._inner._load_module(), seal["executable_fingerprint"]


# --- Glue rungs g2/g3: fields the bridge has no generated default for -------
def glue_fields(R: float, a: float) -> dict[str, float]:
    o = oracle_at(R=R, a=a, magnet_R0=R)
    special = o["special_materials"]  # g3: per-point, = blanket_vol*0.5*9400*5
    return {
        f"{P}cas23_to_28_capital__special_materials_capital": special,
        f"{P}cas2x_pre_contingency__special_materials_capital": special,
        f"{P}cas23_to_28_capital__cas28_capital": 5_000_000.0,
        f"{P}cas2x_pre_contingency__cas28_capital": 5_000_000.0,
        f"{P}replacement_cost_per_event__n_mod": 1.0,
        # dead schema fillers (asserted dead in preflight_checks)
        "mfe_plant__MFE_Power_Plant__p_th": o["p_th"],
        "mfe_plant__MFE_Power_Plant__p_the": o["p_the"],
        "mfe_plant__MFE_Power_Plant__p_et": o["p_et"],
    }


def proposal_for(R: float, a: float, availability: float) -> dict[str, float]:
    fields = dict(glue_fields(R, a))
    for key in AXES["R"]:
        fields[key] = R
    fields[R_TIE] = R
    for key in AXES["a"]:
        fields[key] = a
    for key in AXES["availability"]:
        fields[key] = availability
    return fields


def preflight_checks() -> None:
    """Name-based expansion completeness + dead-filler assertions.

    Honesty note: the completeness check is NAME-based (keys sharing the
    attribute's suffix). It cannot find semantic duplicates under different
    names — magnet__R0 is declared by hand above; known held-fixed semantic
    duplicates: pb__p_input / heating_cost__p_ecrh (both 50 MW installed
    heating), the two ash_frac precisions.
    """
    all_keys: set[str] = set()
    for f in (PACKAGE_DIR / "inputs").glob("*.json"):
        all_keys |= set(json.loads(f.read_text()))
    for attr, declared in AXES.items():
        found = {k for k in all_keys if k.endswith(f"__{attr}")}
        if found != set(declared):
            raise SystemExit(f"expansion mismatch for {attr}: {found ^ set(declared)}")
    r0_keys = {k for k in all_keys if k.endswith("__R0")}
    if r0_keys != {R_TIE}:
        raise SystemExit(f"unexpected R0 keys: {r0_keys}")
    # The 3 p_* schema fillers must be dead: nothing in the executed spec may
    # read them as mfe_plant_params-sourced inputs (glue-1 repointed them).
    # Broad pattern deliberately: a resurrection wired from ANY channel
    # (system_design included) must trip this, since glue feeds these fillers
    # per-point from the oracle — a live consumer would be undisclosed
    # both-sides circularity.
    spec_text = SPEC_PATH.read_text()
    if "MFE_Power_Plant__p_" in spec_text:
        raise SystemExit("schema fillers are LIVE in the pipeline spec — stale-input hazard")
    print("[preflight] expansion sets complete (name-based); schema fillers dead")


def assert_package_untouched() -> None:
    out = subprocess.run(
        ["git", "status", "--porcelain", str(PACKAGE_DIR)],
        capture_output=True, text=True, cwd=E2E,
    ).stdout.strip()
    if out:
        raise SystemExit(f"committed package was MUTATED:\n{out}")
    print("[gate] committed package byte-untouched (git clean)")


def validate_proposal(raw):
    out = {}
    for k, v in raw.items():
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            return None
        out[k] = float(v)
    return out


def run_study(study_id: str, proposals: list[dict[str, float]], db: Path):
    loader = GlueAwareLoader(ProvisionalPackageLoader(
        package_dir=PACKAGE_DIR, package_name="stellarator_tea",
        link_root=WORK / "pkg_link",
    ))
    prepared = PreparedEvaluator(loader, SPEC_PATH)
    definition = StudyDefinition(
        study_id=study_id,
        entry_models=prepared.entry_models,
        strategy=PreparedListStrategy(proposals),
        validate_proposal=validate_proposal,
        policy=ObjectivePolicy(objectives=(), response_roles={}),
        executable_fingerprint=prepared.fingerprint,
        model_contract_fingerprint=digest_of(
            json.loads((PACKAGE_DIR / "contracts" / "model_contract.json").read_text())
        ),
        input_schema_version="input-v1",
        evidence_schema_version=prepared.EVIDENCE_SCHEMA_VERSION,
        study_definition_fingerprint=digest_of(
            {"proposals": [sorted(p.items()) for p in proposals]}
        ),
    )
    if db.exists():
        db.unlink()
    store = StudyStore.create_or_open(db, definition.compatibility())
    store.acquire_lease()
    StudyRunner(store, definition, prepared).run()
    store.release_lease()
    store.close()
    return StudyQuery(StudyStore(db), PACKAGE_DIR).cases()


def short_verdicts(case) -> dict[str, str]:
    return {cid.rsplit("__", 2)[-2]: v for cid, v in case.verdicts.items()}


def export_csv(cases, axes: list[str], path: Path) -> None:
    rows = []
    for c in cases:
        row = {ax: c.inputs[AXES[ax][0]] for ax in axes}
        for name, ch in CHANNELS.items():
            row[name] = c.outputs.get(ch)
        verdicts = short_verdicts(c)
        row.update(verdicts)
        row["feasible"] = all(v == "satisfied" for v in verdicts.values())
        rows.append(row)
    rows.sort(key=lambda r: tuple(r[ax] for ax in axes))
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"[export] {path.name}: {len(rows)} rows")


def cmd_run() -> None:
    WORK.mkdir(exist_ok=True)
    preflight_checks()

    # Study A: (R, a) grid, geometric-validity-excluded, baseline appended.
    grid, excluded = [], 0
    for R in R_VALUES:
        for a in A_VALUES:
            if R > a + BUILD_STACK_M:
                grid.append(proposal_for(R, a, BASELINE["availability"]))
            else:
                excluded += 1  # self-intersecting torus — not a design
    grid.append(proposal_for(**BASELINE))
    print(f"[study A] {len(grid)} proposals ({excluded} geometrically invalid "
          f"points excluded by R > a + {BUILD_STACK_M}); baseline appended")
    cases_a = run_study("stellarator-design-search-ra-v1", grid, WORK / "design_search_R_a.db")
    completed = [c for c in cases_a if c.state == "completed"]
    print(f"[study A] {len(completed)}/{len(cases_a)} cases completed")
    export_csv(completed, ["R", "a"], HERE / "design_search_R_a.csv")

    # Study B: availability sweep at baseline geometry.
    sweep = [proposal_for(BASELINE["R"], BASELINE["a"], av) for av in AVAIL_VALUES]
    cases_b = run_study("stellarator-availability-sweep-v1", sweep, WORK / "availability_sweep.db")
    completed_b = [c for c in cases_b if c.state == "completed"]
    print(f"[study B] {len(completed_b)}/{len(cases_b)} cases completed")
    export_csv(completed_b, ["availability"], HERE / "availability_sweep.csv")

    # Gates.
    baseline_cases = [
        c for c in cases_a
        if c.inputs[AXES["R"][0]] == BASELINE["R"] and c.inputs[AXES["a"][0]] == BASELINE["a"]
    ]
    assert baseline_cases, "baseline point missing from study A"
    bl = baseline_cases[0]
    lcoe = bl.outputs[CHANNELS["lcoe"]]
    assert abs(lcoe - PINNED_LCOE) / PINNED_LCOE < 1e-9, f"baseline LCOE {lcoe}"
    assert all(v == "satisfied" for v in bl.verdicts.values()), short_verdicts(bl)
    print(f"[gate] baseline reproduces pinned headline: LCOE {lcoe:.9f}, 5/5 satisfied")
    assert_package_untouched()


def cmd_verify(k: int = 12, seed: int = 20260816) -> None:
    """Oracle spot-checks on K random committed rows from each study CSV."""
    rng = random.Random(seed)
    # Bound inputs the verdict re-derivation reads (from the committed inputs).
    sd = json.loads((PACKAGE_DIR / "inputs" / "system_design.json").read_text())
    sp = json.loads((PACKAGE_DIR / "inputs" / "stellarator_plant_params.json").read_text())
    recirc_threshold = sd[f"{P}recirc_ok__afc3be66f0a3421b__threshold"]
    wall_limit = sp[f"{P}wall_load_limit"]
    beta_ok = sp[f"{P}beta"] <= sp[f"{P}beta_limit"]
    tbr_ok = sp[f"{P}tbr"] >= sp[f"{P}tbr_floor"]

    checks = [("design_search_R_a.csv", lambda r: dict(
                  R=float(r["R"]), a=float(r["a"]), magnet_R0=float(r["R"]))),
              ("availability_sweep.csv", lambda r: dict(availability=float(r["availability"])))]
    worst = 0.0
    for csv_name, to_overrides in checks:
        rows = list(csv.DictReader((HERE / csv_name).open()))
        # Stratified: guarantee at least one row per observed verdict
        # combination (a plain random sample can miss the 32-row recirc
        # stratum entirely), then fill the rest randomly.
        strata: dict[tuple, list] = {}
        for r in rows:
            key = tuple(r[v] for v in ("net_positive", "recirc_ok", "wall_load_ok",
                                       "beta_ok", "tbr_ok"))
            strata.setdefault(key, []).append(r)
        sample = [rng.choice(members) for members in strata.values()]
        rest = [r for r in rows if r not in sample]
        sample += rng.sample(rest, min(max(0, k - len(sample)), len(rest)))
        for r in sample:
            o = oracle_at(**to_overrides(r))
            for name, okey in [("lcoe", "lcoe"), ("p_fus", "p_fus"), ("magnet_capital", "magnet"),
                               ("total_capital", "total_capital"), ("wall_load", "wall_load")]:
                got, exp = float(r[name]), o[okey]
                rd = abs(got - exp) / max(abs(exp), 1e-30)
                worst = max(worst, rd)
                assert rd < 1e-9, f"{csv_name} {name} at {to_overrides(r)}: {got} vs {exp} ({rd:.2e})"
            expect = {
                "beta_ok": beta_ok,
                "tbr_ok": tbr_ok,
                "net_positive": o["p_net"] > 0.0,
                "recirc_ok": o["rec_frac"] <= recirc_threshold,
                "wall_load_ok": o["wall_load"] <= wall_limit,
            }
            for vname, want in expect.items():
                got_v = r[vname] == "satisfied"
                assert got_v == want, f"{csv_name} verdict {vname} at {to_overrides(r)}: " \
                                      f"package={r[vname]} oracle-derived={want}"
        print(f"[verify] {csv_name}: {len(sample)} sampled rows, channels rel<1e-9, "
              f"verdicts match oracle re-derivation")
    print(f"[verify] worst channel rel dev: {worst:.2e}")
    print("[verify] NOTE: the glue-fed inputs (CAS27 special_materials per point, "
          "cas28 constant, n_mod) are identical by construction on both sides "
          "and are not independently verified by this check.")
    assert_package_untouched()
    (HERE / "verification_summary.json").write_text(json.dumps({
        "sampled_rows_per_study": k, "seed": seed, "worst_channel_rel_dev": worst,
        "sampling": "stratified by verdict combination, remainder random",
        "channels_checked": ["lcoe", "p_fus", "magnet_capital", "total_capital", "wall_load"],
        "tolerance": 1e-9, "verdicts_rederived": True, "package_git_clean": True,
        "glue_note": "glue-fed inputs (CAS27 per-point, cas28, n_mod) identical by "
                     "construction on both sides; not independently verified",
    }, indent=2))
    print(f"[verify] wrote verification_summary.json")


def cmd_export() -> None:
    """Re-export CSVs from existing study stores (no re-run), with gates."""
    for db, axes, csv_name in [
        (WORK / "design_search_R_a.db", ["R", "a"], "design_search_R_a.csv"),
        (WORK / "availability_sweep.db", ["availability"], "availability_sweep.csv"),
    ]:
        cases = StudyQuery(StudyStore(db), PACKAGE_DIR).cases()
        completed = [c for c in cases if c.state == "completed"]
        print(f"[export] {db.name}: {len(completed)}/{len(cases)} completed")
        export_csv(completed, axes, HERE / csv_name)
        if "R" in axes:
            bl = [c for c in completed
                  if c.inputs[AXES["R"][0]] == BASELINE["R"]
                  and c.inputs[AXES["a"][0]] == BASELINE["a"]]
            lcoe = bl[0].outputs[CHANNELS["lcoe"]]
            assert abs(lcoe - PINNED_LCOE) / PINNED_LCOE < 1e-9, lcoe
            print(f"[gate] baseline reproduces pinned headline: LCOE {lcoe:.9f}")
    assert_package_untouched()


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["run", "verify", "export"])
    args = ap.parse_args()
    {"run": cmd_run, "verify": cmd_verify, "export": cmd_export}[args.command]()
