"""WI-015 anchor checks: execute the generated IFE pipeline through the teax
executor at three known-good points and assert LCOE against the verified
oracle (scripts/verify_ife_lcoe.py, which mirrors ife_lcoe.sysml line-for-line).

Anchors (spec.md):
  A. Hawker 14-parameter defaults          -> $252.30/MWh
  B. Realistic HIF point (f=5, eta=0.25)   -> $68.69/MWh
  C. Osiris hif_plant point (SV-013)       -> $270.12/MWh (~$270)
     + Meier COE cross-output (~5 c/kWh) and gamma from Meier Eq. 5.

Known wiring gap (codegen finding, WI-015 findings.md): the model binds
driver.cost_per_joule = meier_cost.gamma, but cross-part references drop to
unresolved entry points, so gamma -> lcoe.driver_cost_constant and
cost_billions -> meier_capital.driver_cost are NOT wired in the YAML.
The harness closes the chain: run A produces gamma/cost_billions (driver
inputs are at the Osiris point), which run C feeds back as inputs.

Run:  ../pipeline_spike/.venv-exec/bin/python run_anchors.py
"""

import json
import sys
from pathlib import Path

E2E = Path(__file__).parent
REPO = E2E.parent.parent

# Import the oracle (pure stdlib, venv-independent)
sys.path.insert(0, str(REPO / "scripts"))
from verify_ife_lcoe import compute_ife_lcoe  # noqa: E402

# Make the generated package importable as `ife_tea`
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

REL_TOL = 1e-6  # spec.md tolerance

L = "hif_plant_pkg__hif_plant__lcoe_calc__"
R = "hif_plant_pkg__hif_plant__recirc_calc__"
D = "hif_driver__hif_driver_instance__meier_cost__"
P = "hif_plant_pkg__hif_plant__"

CH_LCOE = f"{P}lcoe_calc__lcoe"
CH_FREC = f"{P}recirc_calc__f_recirc"
CH_GAMMA = f"{D}gamma"
CH_CB = f"{D}cost_billions"
CH_COE = f"{P}meier_coe_calc__coe_cents_kwh"

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
# Osiris (hif_plant.sysml bindings); driver_cost_constant filled from run A's gamma
OSIRIS = dict(
    availability=0.90, blanket_energy_multiple=1.15, discount_rate=0.08,
    driver_cost_constant=None, driver_efficiency=0.35, driver_energy=14.286e6,
    driver_lifetime_shots=6.0e9, frequency=3.5, gain=80.0,
    om_cost_constant=65.0, plant_cost_constant=2000.0,
    target_cost_constant=10.0, thermal_efficiency=0.43,
    yield_cost_constant=5.0e6,
)
# Osiris driver point (hif_plant.sysml / hif_driver.sysml)
DRIVER_INPUTS = dict(beam_energy_mj=5.0, driver_efficiency=0.35,
                     num_chambers=1.0, rep_rate=3.5)


def write_inputs(params: dict, driver_cost_billions: float = 0.0) -> None:
    ife = {f"{L}{k}": v for k, v in params.items()}
    ife[f"{L}construction_years"] = 5.0
    ife[f"{L}operational_years"] = 40.0
    ife[f"{R}eta"] = params["driver_efficiency"]
    ife[f"{R}gain"] = params["gain"]
    ife[f"{R}blanket_multiplier"] = params["blanket_energy_multiple"]
    ife[f"{R}thermal_efficiency"] = params["thermal_efficiency"]
    (E2E / "generated/inputs/ife_plant_params.json").write_text(json.dumps(ife, indent=2))

    drv = {f"{D}{k}": v for k, v in DRIVER_INPUTS.items()}
    (E2E / "generated/inputs/hif_driver_params.json").write_text(json.dumps(drv, indent=2))

    plant = {
        f"{P}meier_reactor_cost_calc__thermal_power_gw": 2.054,
        f"{P}meier_reactor_cost_calc__num_units": 1.0,
        f"{P}meier_capital_calc__driver_cost": driver_cost_billions,
        f"{P}meier_capital_calc__target_factory_cost": 0.1,
        f"{P}meier_coe_calc__availability": params["availability"],
        f"{P}meier_coe_calc__net_electric_power_gw": 1.0,
    }
    (E2E / "generated/inputs/hif_plant_params.json").write_text(json.dumps(plant, indent=2))


def run(tag: str) -> dict:
    router = create_output_router_with_json_schemas(["RootModel[float]"])
    router.register_handler(
        "float",
        WriteHandler(fn=lambda value, path: Path(path).write_text(json.dumps(value)),
                     extension=".json"),
    )
    result = execute_pipeline(
        E2E / "generated/pipelines/ife_hif.yaml",
        output_dir=E2E / "outputs" / tag,
        registry=create_ife_tea_registry(),
        output_router=router,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    out = {}
    for chan, val in result.outputs.items():
        out[chan] = float(val.root) if hasattr(val, "root") else float(val)
    return out


def check(label: str, actual: float, expected: float, failures: list) -> None:
    ok = abs(actual - expected) <= REL_TOL * max(abs(actual), abs(expected), 1e-30)
    print(f"  {label:34s} executed={actual:16.6f} expected={expected:16.6f}  "
          f"{'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(label)


def main() -> None:
    failures: list = []

    # Expected values from the oracle
    exp_a = compute_ife_lcoe(**HAWKER_DEFAULTS)
    exp_b = compute_ife_lcoe(**REALISTIC_HIF)

    # Meier chain expectations (hand math per hif_economics.sysml)
    cb = (0.32 + 0.088 * 5.0) * (1.25 + 0.05 * 1.0) * (1.0 + 0.0088 * (3.5 - 5.0))
    gamma = cb * 1e9 / (5.0e6 / 0.35)
    reactor = 0.66 * (2.054 / 1.67) ** 0.49 * (0.72 * 1.0 + 0.28)
    capital = 1.83 * (reactor + cb + 0.1)
    coe = (0.113 * capital) / (0.0876 * 0.90 * 1.0)

    exp_c = compute_ife_lcoe(**{**OSIRIS, "driver_cost_constant": gamma})

    print("=== Run A: Hawker defaults (driver module at Osiris point) ===")
    write_inputs(HAWKER_DEFAULTS)
    out_a = run("hawker_defaults")
    check("LCOE $/MWh", out_a[CH_LCOE], exp_a["lcoe_per_MWh"], failures)
    check("f_recirc", out_a[CH_FREC], exp_a["recirculating_fraction"], failures)
    check("Meier gamma $/J", out_a[CH_GAMMA], gamma, failures)
    check("Meier driver cost $B", out_a[CH_CB], cb, failures)

    print("=== Run B: realistic HIF point ===")
    write_inputs(REALISTIC_HIF)
    out_b = run("realistic_hif")
    check("LCOE $/MWh", out_b[CH_LCOE], exp_b["lcoe_per_MWh"], failures)
    check("f_recirc", out_b[CH_FREC], exp_b["recirculating_fraction"], failures)

    print("=== Run C: Osiris plant point (gamma fed back from run A) ===")
    osiris = dict(OSIRIS, driver_cost_constant=out_a[CH_GAMMA])
    write_inputs(osiris, driver_cost_billions=out_a[CH_CB])
    out_c = run("osiris")
    check("LCOE $/MWh", out_c[CH_LCOE], exp_c["lcoe_per_MWh"], failures)
    check("f_recirc", out_c[CH_FREC], exp_c["recirculating_fraction"], failures)
    check("Meier COE c/kWh", out_c[CH_COE], coe, failures)

    print()
    print(f"Anchor A LCOE: ${out_a[CH_LCOE]:.2f}/MWh (expected $252.30)")
    print(f"Anchor B LCOE: ${out_b[CH_LCOE]:.2f}/MWh (expected $68.69)")
    print(f"Anchor C LCOE: ${out_c[CH_LCOE]:.2f}/MWh (expected ~$270, SV-013)")
    print(f"Osiris Meier COE: {out_c[CH_COE]:.2f} c/kWh (expected ~5)")
    if failures:
        raise SystemExit(f"{len(failures)} anchor check(s) FAILED: {failures}")
    print("ALL ANCHOR CHECKS PASSED (rel tol 1e-6)")


if __name__ == "__main__":
    main()
