"""Check historical A/B modules and the repaired computed Osiris pipeline.

The source oracle uses annual cash-flow sums independently of generated finance.
All anchor prices require generating=1 and the named net_positive verdict.
Outputs default to a temporary directory; generated input files are never edited.
"""

import argparse
import json
import tempfile
import sys
from pathlib import Path

E2E = Path(__file__).parent
REPO = E2E.parent.parent

# Independent source-equation oracle (annual discount sums).
sys.path.insert(0, str(REPO / "scripts"))
from verify_ife_lcoe import compute_ife_lcoe  # noqa: E402
from verify_hif_costs import computed_osiris  # noqa: E402
from eligibility import NET_POSITIVE_ID, module_balance, module_price, require_price

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
from ife_tea.modules.fusion_cycle.recirculating_power_fraction import (  # noqa: E402
    Recirculating_Power_FractionInput,
)

REL_TOL = 1e-9  # WI-048 numerical identity tolerance

P = "hif_plant_pkg__hif_plant__"
CH_LCOE = f"{P}hawker_price__price"
CH_FREC = f"{P}recirc_calc__f_recirc"
CH_GAMMA = f"{P}driver__meier_cost__gamma"        # canonical driver path (instance deleted)
CH_CB = f"{P}driver__meier_cost__cost_billions"
CH_COE = f"{P}meier_price__price"
CH_CAPITAL = f"{P}meier_capital_calc__total_capital_billions"

INPUTS_DIR = E2E / "generated/inputs"
GAIN_LCOE_KEY = f"{P}gain"   # authoritative plant gain entry

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
    driver_efficiency=0.28, driver_energy=5e6 / 0.28,
    driver_lifetime_shots=6.0e9, frequency=4.6, gain=87.0,
    om_cost_constant=65.0, plant_cost_constant=2000.0,
    target_cost_constant=10.0, thermal_efficiency=0.45,
    yield_cost_constant=5.0e6,
)

failures: list = []


def check(label: str, actual: float, expected: float) -> None:
    ok = abs(actual - expected) <= REL_TOL * max(abs(actual), abs(expected), 1e-30)
    print(f"  {label:38s} actual={actual:18.8f} expected={expected:18.8f}  "
          f"{'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(label)


def run_pipeline(output_dir: Path, gain=None) -> dict:
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
    # Copy a runnable package so a parameter probe cannot change the sealed source.
    import shutil
    package = output_dir / "package"
    shutil.copytree(E2E / "generated", package, dirs_exist_ok=True)
    if gain is not None:
        gain_file = package / "inputs" / _inputs_file_for(GAIN_LCOE_KEY).name
        data = json.loads(gain_file.read_text())
        data[GAIN_LCOE_KEY] = gain
        gain_file.write_text(json.dumps(data))
    result = execute_pipeline(
        package / "pipelines/pipeline.yaml",
        output_dir=output_dir / "results",
        registry=create_ife_tea_registry(),
        output_router=router,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    out = {chan: (float(val.root) if hasattr(val, "root") else val)
           for chan, val in result.outputs.items()}
    verdict = out[NET_POSITIVE_ID + "__evaluation"].status
    for prefix in ("hawker_price", "meier_price"):
        require_price(out[P + prefix + "__price"],
                      out[P + prefix + "__generating"], verdict)
    return out


def _inputs_file_for(key: str) -> Path:
    """Return the emitted inputs/*.json that carries `key` (raises if absent)."""
    for jf in sorted(INPUTS_DIR.glob("*.json")):
        if key in json.loads(jf.read_text()):
            return jf
    raise KeyError(f"emitted inputs carry no key {key!r}")


def module_level(tag: str, params: dict) -> None:
    print(f"=== {tag} (module-level: generated impls called directly) ===")
    exp = compute_ife_lcoe(**params)
    lcoe = module_balance(dict(params, construction_years=5.0, operational_years=40.0))
    f_recirc = run_recirculating_power_fraction(Recirculating_Power_FractionInput(
        eta=params["driver_efficiency"], gain_in=params["gain"],
        blanket_multiplier=params["blanket_energy_multiple"],
        thermal_efficiency_in=params["thermal_efficiency"]))
    price, verdict = module_price(lcoe)
    check("LCOE $/MWh", require_price(price.price, price.generating, verdict), exp["lcoe_per_MWh"])
    check("f_recirc", f_recirc, exp["recirculating_fraction"])


def main() -> None:
    # --- Anchors A and B: module level ------------------------------------
    module_level("Run A: historical Hawker defaults", HAWKER_DEFAULTS)
    module_level("Run B: historical realistic HIF", REALISTIC_HIF)

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output = args.output_dir or Path(tempfile.mkdtemp(prefix="ife-anchors-"))
    print("=== Computed Osiris-based point (435 MJ, equal driver/cooling allowance) ===")
    expected = computed_osiris()
    out = run_pipeline(output / "baseline")
    check("Meier driver $B", out[CH_CB], expected["driver_cost_billions"])
    check("Meier gamma $/J", out[CH_GAMMA], expected["gamma"])
    check("Meier capital $B", out[CH_CAPITAL], expected["capital_billions"])
    check("Meier 1988 cents/kWh", out[CH_COE], expected["meier_coe"])
    check("Hawker $/MWh", out[CH_LCOE], expected["lcoe_per_MWh"])
    check("Driver-only fraction", out[CH_FREC], expected["recirculating_fraction"])
    changed = run_pipeline(output / "gain100", gain=100.0)
    target = compute_ife_lcoe(
        **{**OSIRIS, "gain": 100.0, "driver_cost_constant": expected["gamma"]})
    check("Gain 87 -> 100 Hawker $/MWh", changed[CH_LCOE], target["lcoe_per_MWh"])
    print(f"Output: {output}")
    if failures:
        raise SystemExit(f"{len(failures)} anchor check(s) FAILED: {failures}")
    print("ALL ANCHOR CHECKS PASSED (rel tol 1e-9) — run C wired, single pass, JSON consumed")


if __name__ == "__main__":
    main()
