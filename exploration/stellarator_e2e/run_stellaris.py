"""Shared helpers for the single-point stellarator runner (`run_stellaris_single.py`).

WI-018 ran the generated Stellaris (concept-09) pipeline through the teax executor and
checked every channel against the pure-Python oracle (`verify_stellaris.py`, which mirrors
the SysML calc defs line-for-line). Its two-pass main and the two harness-glue rungs --
the BOP repoint / schema fillers (glue-1) and the Python capital rollup (glue-2) -- are
gone: since the stellarator model migration (2026-08-21) the package is sealed at runtime
contract 2.0.0 with every cross-part edge wired by codegen, and it is loaded here through
stock teax's strict loader, which refuses any tampered artifact. What remains is the
channel map, the check helper, and the pipeline runner.

Teax comes from `STOP_PARSER_TEAX_ROOT` (a teax checkout; `packages/teax-simkit` goes on
sys.path), the same contract the study tests use.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

E2E = Path(__file__).parent
sys.path.insert(0, str(E2E))
from verify_stellaris import compute as oracle_compute  # noqa: E402, F401  (re-exported)

_TEAX_ROOT = os.environ.get("STOP_PARSER_TEAX_ROOT")
if not _TEAX_ROOT:
    raise SystemExit("STOP_PARSER_TEAX_ROOT is not set; point it at a teax checkout")
sys.path.insert(0, str(Path(_TEAX_ROOT) / "packages" / "teax-simkit"))

from simkit.core.pipeline import execute_pipeline  # noqa: E402
from simkit.evaluation.package_load import ProvisionalPackageLoader  # noqa: E402
from simkit.io.output_router import (  # noqa: E402
    WriteHandler,
    create_output_router_with_json_schemas,
)

GEN = E2E / "generated"
PIPELINE = GEN / "pipelines" / "pipeline.yaml"
REL_TOL = 1e-9  # generated arithmetic vs oracle; expect bit-exact

# Strict load: the seal is verified (every artifact hash, the runtime-contract version)
# before the package is imported. The loader writes its import link into a scratch
# directory, never under the package.
_LINK_ROOT = Path(tempfile.mkdtemp(prefix="stellarator_tea_link_"))
PACKAGE, EXECUTABLE_FINGERPRINT = ProvisionalPackageLoader(
    package_dir=GEN.resolve(), package_name="stellarator_tea", link_root=_LINK_ROOT, strict=True
).load()
CUSTOM_SCHEMA_TYPES = PACKAGE.CUSTOM_SCHEMA_TYPES
create_stellarator_tea_registry = PACKAGE.create_stellarator_tea_registry

P = "stellarator_09__stellaris__"

# Channel names (from the emitted pipeline YAML).
CH = dict(
    V=f"{P}geom__V", p_fus=f"{P}fusion__p_fus", wall_load=f"{P}wall_load_calc__wall_load",
    p_th=f"{P}pb__p_th", p_the=f"{P}pb__p_the", p_et=f"{P}pb__p_et",
    p_cryo=f"{P}cryo_elec__p_elec",  # derived cryoplant electrical (WI-024)
    q_eng=f"{P}pb__q_eng", rec_frac=f"{P}pb__rec_frac", p_net=f"{P}pb__p_net",
    magnet=f"{P}magnet_cost__capital_cost", heating=f"{P}heating_cost__cost",
    divertor=f"{P}divertor_cost__cost", blanket=f"{P}blanket_cost__cost",
    shield=f"{P}shield_cost__cost", structure=f"{P}structure_cost__cost",
    vessel=f"{P}vessel_cost__cost", power_supplies=f"{P}power_supplies_cost__cost",
    turbine=f"{P}turbine_cost__cost", electric=f"{P}electric_cost__cost",
    heat_rejection=f"{P}heat_rejection_cost__cost", misc=f"{P}misc_cost__cost",
    # forward-computed direct accounts (WI-025): CAS21/CAS10/CAS70 are now
    # generated-module outputs tracking the computed powers (the BUILDINGS/
    # PRECON harness constants are retired).
    buildings=f"{P}buildings_cost__cost", precon=f"{P}precon_cost__cost",
    annual_om=f"{P}om_cost__annual_om",
    contingency=f"{P}contingency__cost", indirect=f"{P}indirect__cost",
    lcoe=f"{P}lcoe_calc__lcoe",
    # WI-029 annual-cost side + Option-(ii) 1cfe-form comparison channels
    cas71=f"{P}cas71_calc__levelized", cas72=f"{P}cas72_calc__cost",
    cas70=f"{P}cas70_calc__cas70", cas80=f"{P}cas80_calc__levelized",
    annual_fuel=f"{P}fuel_calc__annual_fuel",
    annual_om_levelized=f"{P}cas70_calc__annual_total",
    # WI-030 physics channels
    beta=f"{P}beta_calc__beta", B_peak=f"{P}peak_field_calc__B_peak",
    # WI-035 field, stress, and decomposed magnet accounts
    B_axis=f"{P}field_calc__B_axis", sigma_wp=f"{P}wp_stress__sigma_wp",
    winding_pack=f"{P}winding_pack_cost__cost",
    magnet_structure=f"{P}magnet_structure_cost__cost",
    magnet_capital_rollup=f"{P}magnet_capital_rollup__capital_cost",
    cas90_1cfe=f"{P}cas90_1cfe_calc__cas90", lcoe_1cfe=f"{P}lcoe_1cfe_calc__lcoe",
    # WI-037 sustainment channels
    n_bar19=f"{P}sustain__n_bar19", n_He0=f"{P}sustain__n_He0",
    n_D0=f"{P}sustain__n_D0", n_T0=f"{P}sustain__n_T0",
    T_e0=f"{P}sustain__T_e0", W_th=f"{P}sustain__W_th",
    tau_E=f"{P}sustain__tau_E", p_brems=f"{P}sustain__p_brems",
    p_line=f"{P}sustain__p_line", p_sync=f"{P}sustain__p_sync",
    p_rad=f"{P}sustain__p_rad", p_alpha_heat=f"{P}sustain__p_alpha_heat",
    p_aux_required=f"{P}sustain__p_aux_required",
)

failures = []


def check(label, actual, expected):
    denom = max(abs(actual), abs(expected), 1e-30)
    ok = abs(actual - expected) <= REL_TOL * denom
    print(f"  {label:26s} exec={actual:20.6f}  oracle={expected:20.6f}  "
          f"{'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(label)


def run_pipeline(tag):
    router = create_output_router_with_json_schemas(["RootModel[float]"])
    router.register_handler(
        "float",
        WriteHandler(fn=lambda v, p: Path(p).write_text(json.dumps(v)), extension=".json"),
    )
    result = execute_pipeline(
        PIPELINE,
        output_dir=E2E / "outputs" / tag,
        registry=create_stellarator_tea_registry(),
        output_router=router,
        custom_schema_types=CUSTOM_SCHEMA_TYPES,
    )
    return {c: (float(v.root) if hasattr(v, "root") else float(v))
            for c, v in result.outputs.items()}
