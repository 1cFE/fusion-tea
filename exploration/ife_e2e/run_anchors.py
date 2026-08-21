"""WI-015 anchor checks — post-retirement harness (PIPELINE-TRUTH Item 3).

Executes the generated IFE pipeline and asserts LCOE against the verified oracle
(scripts/verify_ife_lcoe.py, which mirrors ife_lcoe.sysml line-for-line).

This is the workaround-free harness. What changed vs the WI-015 original, now that the
sysml-codegen PIPELINE-TRUTH fixes have landed and the models generate whole-plant with
zero V11 offenders:

  1. Single pass, no manual gamma recirculation. The Meier chain is closed by generated
     wiring — gamma -> lcoe.driver_cost_constant and cost_billions -> meier_capital.driver_cost
     are wired channels in the emitted YAML. Run C runs the pipeline exactly once.
  2. NO hand-written input JSONs. Run C's inputs are the GENERATED inputs/*.json exactly
     as emitted (the value-fill materializer carries the model's own cross-part literals).
  3. Meier channels are keyed off the CANONICAL driver path
     (hif_plant_pkg__hif_plant__driver__meier_cost__*). The standalone driver-instance
     workaround part is gone; the retyped-part indexing fix emits meier_cost from
     `part :>> driver`.
  4. Anchors A/B are MODULE-LEVEL checks. With driver_cost_constant a wired input (not an
     entry point), the pipeline can no longer be fed the Hawker/Realistic driver_cost=5.0
     that A/B are defined at — that is the model's own semantics. A/B call the generated
     lcoe/recirc implementations directly.
  5. A perturbed-key rerun proves the emitted JSON is genuinely CONSUMED (not shadowed by a
     baked default): move the emitted lcoe gain key 80 -> 100 and assert lcoe follows to an
     oracle-computed target (SC-B rider).

The teax T-1/T-2 router (RootModel[float]/float exit handlers) is reused verbatim — those
findings are out of the epic's scope and stay harness-side.

Run:  cd ~/1cfe/fusion-tea/exploration/ife_e2e && \
      ../pipeline_spike/.venv-exec/bin/python run_anchors.py
"""

import json
import sys
from pathlib import Path

E2E = Path(__file__).parent
REPO = E2E.parent.parent

# Oracle (pure stdlib, venv-independent): mirrors ife_lcoe.sysml line-for-line.
sys.path.insert(0, str(REPO / "scripts"))
from verify_ife_lcoe import compute_ife_lcoe  # noqa: E402

# Make the generated package importable as `ife_tea`.
pkg_dir = E2E / "pkg"
pkg_dir.mkdir(exist_ok=True)
link = pkg_dir / "ife_tea"
if not link.exists():
    link.symlink_to(E2E / "generated")
sys.path.insert(0, str(pkg_dir))

from simkit.core.pipeline import execute_pipeline  # noqa: E402
from simkit.io.output_router import (  # noqa: E402
    WriteHandler,
    create_output_router_with_json_schemas,
)

from ife_tea import CUSTOM_SCHEMA_TYPES, create_ife_tea_registry  # noqa: E402
from ife_tea.handwritten.fusion_cycle.recirculating_power_fraction_impl import (  # noqa: E402
    run_recirculating_power_fraction,
)
from ife_tea.handwritten.ife_lcoe.ife_lcoe_impl import run_ife_lcoe  # noqa: E402
from ife_tea.modules.fusion_cycle.recirculating_power_fraction import (  # noqa: E402
    Recirculating_Power_FractionInput,
)
from ife_tea.modules.ife_lcoe.ife_lcoe import IFE_LCOEInput  # noqa: E402

REL_TOL = 1e-6  # spec.md tolerance

P = "hif_plant_pkg__hif_plant__"
CH_LCOE = f"{P}lcoe_calc__lcoe"
CH_FREC = f"{P}recirc_calc__f_recirc"
CH_GAMMA = f"{P}driver__meier_cost__gamma"        # canonical driver path (instance deleted)
CH_CB = f"{P}driver__meier_cost__cost_billions"
CH_COE = f"{P}meier_coe_calc__coe_cents_kwh"
CH_CAPITAL = f"{P}meier_capital_calc__total_capital_billions"

# Pinned codegen emits the default pipeline filename `pipeline.yaml` (was `ife_hif.yaml`
# in the pre-epic package); migrated for Item 13 compose (test-infra only).
PIPELINE = E2E / "generated/pipelines/pipeline.yaml"
INPUTS_DIR = E2E / "generated/inputs"
GAIN_LCOE_KEY = f"{P}lcoe_calc__gain"   # the emitted per-consumer lcoe gain key

# --- Anchor parameter sets (Hawker's 14 + 2 fixed constants) ---------------
HAWKER_DEFAULTS = dict(
    availability=0.70, blanket_energy_multiple=1.2, discount_rate=0.08,
    driver_cost_constant=5.0, driver_efficiency=0.10, driver_energy=10.0e6,
    driver_lifetime_shots=5.0e7, frequency=0.2, gain=500.0,
    om_cost_constant=30.0, plant_cost_constant=3000.0,
    target_cost_constant=10.0, thermal_efficiency=0.40,
    yield_cost_constant=5.0e6,
)
REALISTIC_HIF = dict(
    HAWKER_DEFAULTS,
    availability=0.85, driver_efficiency=0.25, driver_energy=5.0e6,
    driver_lifetime_shots=1.0e9, frequency=5.0, gain=100.0,
    discount_rate=0.05, target_cost_constant=0.50,
)
# Osiris (hif_plant.sysml bindings); driver_cost_constant comes from generated wiring.
OSIRIS = dict(
    availability=0.90, blanket_energy_multiple=1.15, discount_rate=0.08,
    driver_efficiency=0.35, driver_energy=14.286e6,
    driver_lifetime_shots=6.0e9, frequency=3.5, gain=80.0,
    om_cost_constant=65.0, plant_cost_constant=2000.0,
    target_cost_constant=10.0, thermal_efficiency=0.43,
    yield_cost_constant=5.0e6,
)

failures: list = []


def check(label: str, actual: float, expected: float) -> None:
    ok = abs(actual - expected) <= REL_TOL * max(abs(actual), abs(expected), 1e-30)
    print(f"  {label:38s} actual={actual:18.8f} expected={expected:18.8f}  "
          f"{'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(label)


def run_pipeline() -> dict:
    """Execute the generated pipeline once (T-1/T-2 router kept) and return channels."""
    # CONSTRAINT-EXEC W1: the whole-plant package now carries a constraint module
    # (ConstraintEvaluation/ConstraintReport ExitPoint outputs) that didn't exist when
    # this router was first wired to just "RootModel[float]" — every custom type needs
    # a registered write handler (PipelineValidator requires one per ExitPoint type).
    schema_names = dict.fromkeys(["RootModel[float]"] + [t.__name__ for t in CUSTOM_SCHEMA_TYPES])
    router = create_output_router_with_json_schemas(list(schema_names))
    router.register_handler(
        "float",
        WriteHandler(fn=lambda value, path: Path(path).write_text(json.dumps(value)),
                     extension=".json"),
    )
    result = execute_pipeline(
        PIPELINE,
        output_dir=E2E / "outputs" / "osiris",
        registry=create_ife_tea_registry(),
        output_router=router,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    # CONSTRAINT-EXEC W1: ExitPoint now also carries constraint evidence
    # (ConstraintEvaluation/ConstraintReport), which isn't a scalar the anchor
    # checks compare against — only numeric channels are collected here.
    return {
        chan: (float(val.root) if hasattr(val, "root") else float(val))
        for chan, val in result.outputs.items()
        if hasattr(val, "root") or isinstance(val, (int, float))
    }


def _inputs_file_for(key: str) -> Path:
    """Return the emitted inputs/*.json that carries `key` (raises if absent)."""
    for jf in sorted(INPUTS_DIR.glob("*.json")):
        if key in json.loads(jf.read_text()):
            return jf
    raise KeyError(f"emitted inputs carry no key {key!r}")


def module_level(tag: str, params: dict) -> None:
    print(f"=== {tag} (module-level: generated impls called directly) ===")
    exp = compute_ife_lcoe(**params)
    lcoe = run_ife_lcoe(IFE_LCOEInput(
        construction_years=5.0, operational_years=40.0, **params))
    f_recirc = run_recirculating_power_fraction(Recirculating_Power_FractionInput(
        eta=params["driver_efficiency"], gain=params["gain"],
        blanket_multiplier=params["blanket_energy_multiple"],
        thermal_efficiency=params["thermal_efficiency"]))
    check("LCOE $/MWh", lcoe, exp["lcoe_per_MWh"])
    check("f_recirc", f_recirc, exp["recirculating_fraction"])


def main() -> None:
    # --- Anchors A and B: module level ------------------------------------
    module_level("Run A: Hawker defaults", HAWKER_DEFAULTS)
    module_level("Run B: realistic HIF", REALISTIC_HIF)

    # --- Anchor C: full pipeline, generated wiring, single pass -----------
    print("=== Run C: Osiris plant point — ONE pass, generated wiring, "
          "generated inputs ===")

    # Meier chain hand-math (per hif_economics.sysml).
    cb = (0.32 + 0.088 * 5.0) * (1.25 + 0.05 * 1.0) * (1.0 + 0.0088 * (3.5 - 5.0))
    gamma = cb * 1e9 / (5.0e6 / 0.35)
    reactor = 0.66 * (2.054 / 1.67) ** 0.49 * (0.72 * 1.0 + 0.28)
    capital = 1.83 * (reactor + cb + 0.1)
    coe = (0.113 * capital) / (0.0876 * 0.90 * 1.0)
    exp_c = compute_ife_lcoe(**{**OSIRIS, "driver_cost_constant": gamma})

    out = run_pipeline()
    check("Meier driver cost $B (wired)", out[CH_CB], cb)
    check("Meier gamma $/J (wired)", out[CH_GAMMA], gamma)
    check("Meier capital $B (wired)", out[CH_CAPITAL], capital)
    check("Meier COE c/kWh", out[CH_COE], coe)
    check("LCOE $/MWh (gamma via wiring)", out[CH_LCOE], exp_c["lcoe_per_MWh"])
    check("f_recirc", out[CH_FREC], exp_c["recirculating_fraction"])

    # --- Perturbed-key rerun: prove the emitted JSON is CONSUMED -----------
    # Move the emitted lcoe gain key 80 -> 100 in place, rerun, assert lcoe follows to the
    # oracle-computed target (gamma unaffected by gain), then restore the file byte-for-byte.
    print("=== Run C': perturbed gain 80 -> 100 (proves JSON is consumed) ===")
    gain_file = _inputs_file_for(GAIN_LCOE_KEY)
    original = gain_file.read_text()
    try:
        data = json.loads(original)
        data[GAIN_LCOE_KEY] = 100.0
        gain_file.write_text(json.dumps(data, indent=2))
        exp_cp = compute_ife_lcoe(**{**OSIRIS, "gain": 100.0, "driver_cost_constant": gamma})
        out_p = run_pipeline()
        check("LCOE $/MWh (gain=100, moved)", out_p[CH_LCOE], exp_cp["lcoe_per_MWh"])
    finally:
        gain_file.write_text(original)

    print()
    print(f"Anchor C LCOE: ${out[CH_LCOE]:.2f}/MWh (WI-015: $270.12, SV-013)")
    print(f"Osiris Meier COE: {out[CH_COE]:.3f} c/kWh (WI-015: 4.735)")
    if failures:
        raise SystemExit(f"{len(failures)} anchor check(s) FAILED: {failures}")
    print("ALL ANCHOR CHECKS PASSED (rel tol 1e-6) — run C wired, single pass, JSON consumed")


if __name__ == "__main__":
    main()
