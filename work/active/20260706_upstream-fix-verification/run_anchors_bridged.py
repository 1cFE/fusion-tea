"""WI-015 anchor verification against the BRIDGED package (upstream-findings epic).

Differences from exploration/ife_e2e/run_anchors.py (the WI-015 harness):

1. NO two-pass gamma feedback. The epic's Item 10 wired gamma -> lcoe.driver_cost_constant
   and cost_billions -> meier_capital.driver_cost at graph level; this harness runs the
   pipeline ONCE and lets generated wiring close the Meier chain.
2. Runs A and B are MODULE-LEVEL checks (direct calls of the generated lcoe/recirc
   implementations). Under correct wiring, lcoe.driver_cost_constant is a wired input,
   not an entry point, so the pipeline can no longer be fed the Hawker/Realistic
   driver_cost_constant values (5.0) that anchors A/B are defined at. That is the model's
   own semantics (hif_plant binds driver.cost_per_joule = meier_cost.gamma); the old
   harness could only feed those values because the wiring was missing.
3. Run C's inputs come from the GENERATED input JSONs as emitted (bridge-filled with the
   model's own cross-part literals) — nothing is written before execution.

The teax T-1/T-2 router workaround (RootModel[float]/float exit handlers) is reused
verbatim — those findings are out of the epic's scope and expected to remain.

Run:  cd ~/1cfe/fusion-tea/exploration/ife_e2e && \
      ../pipeline_spike/.venv-exec/bin/python \
      ~/1cfe/fusion-tea/work/active/20260706_upstream-fix-verification/run_anchors_bridged.py
"""

import json
import sys
from pathlib import Path

E2E = Path.home() / "1cfe/fusion-tea/exploration/ife_e2e"
REPO = E2E.parent.parent
OUTDIR = E2E / "outputs_bridged"

sys.path.insert(0, str(REPO / "scripts"))
from verify_ife_lcoe import compute_ife_lcoe  # noqa: E402

sys.path.insert(0, str(E2E / "pkg_bridged"))

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

REL_TOL = 1e-6

P = "hif_plant_pkg__hif_plant__"
CH_LCOE = f"{P}lcoe_calc__lcoe"
CH_FREC = f"{P}recirc_calc__f_recirc"
CH_GAMMA = f"{P}driver__meier_cost__gamma"          # retyped-driver instance (Item 10 wiring)
CH_CB = f"{P}driver__meier_cost__cost_billions"
CH_COE = f"{P}meier_coe_calc__coe_cents_kwh"
CH_CAPITAL = f"{P}meier_capital_calc__total_capital_billions"

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

    # Meier chain hand-math (per hif_economics.sysml), as in run_anchors.py
    cb = (0.32 + 0.088 * 5.0) * (1.25 + 0.05 * 1.0) * (1.0 + 0.0088 * (3.5 - 5.0))
    gamma = cb * 1e9 / (5.0e6 / 0.35)
    reactor = 0.66 * (2.054 / 1.67) ** 0.49 * (0.72 * 1.0 + 0.28)
    capital = 1.83 * (reactor + cb + 0.1)
    coe = (0.113 * capital) / (0.0876 * 0.90 * 1.0)
    exp_c = compute_ife_lcoe(**{**OSIRIS, "driver_cost_constant": gamma})

    router = create_output_router_with_json_schemas(["RootModel[float]"])
    router.register_handler(
        "float",
        WriteHandler(fn=lambda value, path: Path(path).write_text(json.dumps(value)),
                     extension=".json"),
    )
    result = execute_pipeline(
        E2E / "generated_bridged/pipelines/ife_hif.yaml",
        output_dir=OUTDIR / "osiris",
        registry=create_ife_tea_registry(),
        output_router=router,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    out = {}
    for chan, val in result.outputs.items():
        out[chan] = float(val.root) if hasattr(val, "root") else float(val)

    check("Meier driver cost $B (wired)", out[CH_CB], cb)
    check("Meier gamma $/J (wired)", out[CH_GAMMA], gamma)
    check("Meier capital $B (wired)", out[CH_CAPITAL], capital)
    check("Meier COE c/kWh", out[CH_COE], coe)
    check("LCOE $/MWh (gamma via wiring)", out[CH_LCOE], exp_c["lcoe_per_MWh"])
    check("f_recirc", out[CH_FREC], exp_c["recirculating_fraction"])

    print()
    print(f"Anchor C LCOE: ${out[CH_LCOE]:.2f}/MWh (WI-015: $270.12, SV-013)")
    print(f"Osiris Meier COE: {out[CH_COE]:.3f} c/kWh (WI-015: 4.735)")
    if failures:
        raise SystemExit(f"{len(failures)} anchor check(s) FAILED: {failures}")
    print("ALL ANCHOR CHECKS PASSED (rel tol 1e-6) — run C wired, single pass")


if __name__ == "__main__":
    main()
