"""WI-018 stellarator end-to-end: generated SysML -> teax -> LCOE + CAS breakdown.

Executes the generated Stellaris (concept-09) pipeline through the teax executor
and checks every channel against the pure-Python oracle (verify_stellaris.py,
which mirrors the SysML calc defs line-for-line) and the WI-018 headline numbers.

What is generated code vs harness glue (all glue is loudly labeled):

  GENERATED + EXECUTED under teax (single generated package, from the SysML):
    - physics spine: Plasma Geometry (V), DT Fusion Power (p_fus),
      MFE Power Balance (p_th/p_the/p_et/q_eng/rec_frac/p_net)
    - every per-account cost module: magnet, heating, divertor, blanket, shield,
      structure, vessel, power_supplies, turbine, electric, heat_rejection, misc
    - contingency, indirect, and the LCOE DCF core

  HARNESS GLUE (the cross-part edges sysml-codegen cannot wire, per findings):
    1. BOP power wiring (NEW finding): the 4 Linear_Power_Cost accounts bind
       `in power = p_the/p_et/p_th` (calc input name != alias name), so the
       cost-spine alias -> pb-output edge is not formed and codegen emits a
       dangling `mfe_plant__MFE_Power_Plant__p_*` schema field. We repoint those
       4 inputs to the real pb output channels in the emitted YAML (single-pass
       wiring closure). The volume-scaled accounts (which bind `in p_th = p_th`)
       wire correctly via the self-named rescue and need no patch.
    2. Capital rollup (WI-015 finding 4): powercore/bop/direct/total sum each
       subsystem capital_cost across parts (feature-chain in a CalcDef output),
       which codegen cannot compile. We sum the generated per-account module
       outputs in Python and feed direct/total back through the emitted input
       JSON, then re-run so the generated contingency/indirect/LCOE modules
       produce the final numbers. Only the additions are harness code.

Run:  cd .../exploration/stellarator_e2e && \
      /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py
"""

import json
import sys
from pathlib import Path

E2E = Path(__file__).parent
sys.path.insert(0, str(E2E))
from verify_stellaris import compute as oracle_compute  # noqa: E402

# Make the generated package importable as `stellarator_tea`.
pkg_dir = E2E / "pkg"
pkg_dir.mkdir(exist_ok=True)
link = pkg_dir / "stellarator_tea"
if not link.exists():
    link.symlink_to(E2E / "generated")
sys.path.insert(0, str(pkg_dir))

from simkit.core.pipeline import execute_pipeline  # noqa: E402
from simkit.io.output_router import (  # noqa: E402
    WriteHandler,
    create_output_router_with_json_schemas,
)

from stellarator_tea import CUSTOM_SCHEMA_TYPES, create_stellarator_tea_registry  # noqa: E402
from stellarator_tea.handwritten.mfe_account_costs.contingency_cost_impl import (  # noqa: E402
    run_contingency_cost,
)
from stellarator_tea.handwritten.mfe_account_costs.indirect_cost_impl import (  # noqa: E402
    run_indirect_cost,
)
from stellarator_tea.modules.mfe_account_costs.contingency_cost import Contingency_CostInput  # noqa: E402
from stellarator_tea.modules.mfe_account_costs.indirect_cost import Indirect_CostInput  # noqa: E402

GEN = E2E / "generated"
PIPELINE = GEN / "pipelines" / "mfe_stellarator.yaml"
MFE_PARAMS = GEN / "inputs" / "mfe_plant_params.json"
SYS_DESIGN = GEN / "inputs" / "system_design.json"
REL_TOL = 1e-9  # generated arithmetic vs oracle; expect bit-exact

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
)

# CAS27 special materials (WI-021): now MODEL-computed from the radial-build
# blanket volume (special_materials_capital = rb.blanket_vol x 0.50 x 9400 x 5.0).
# Harvested from the pipeline's rb.blanket_vol in PASS A (see below), not a
# hardcoded constant — was 26289000.0.
PBLI_VOL_FRAC, PBLI_DENSITY, PBLI_PRICE = 0.50, 9400.0, 5.0

# Rollup rates / financing needed for the harness contingency+indirect closure
# (also generated-module inputs; these match the instance bindings).
CONTINGENCY_RATE = 0.10
INDIRECT_FRACTION = 0.20
CONSTRUCTION_YEARS = 8.0
REFERENCE_CONSTRUCTION_TIME = 6.0

failures = []


def check(label, actual, expected):
    denom = max(abs(actual), abs(expected), 1e-30)
    ok = abs(actual - expected) <= REL_TOL * denom
    print(f"  {label:26s} exec={actual:20.6f}  oracle={expected:20.6f}  "
          f"{'OK' if ok else 'FAIL'}")
    if not ok:
        failures.append(label)


def patch_bop_wiring():
    """HARNESS GLUE #1: repoint the 4 BOP Linear_Power_Cost `power` inputs from the
    dangling `mfe_plant__MFE_Power_Plant__p_*` schema field to the real pb output
    channels. Idempotent."""
    text = PIPELINE.read_text()
    repl = {
        "mfe_plant_params.mfe_plant__MFE_Power_Plant__p_the": f"{P}pb__p_the",
        "mfe_plant_params.mfe_plant__MFE_Power_Plant__p_et": f"{P}pb__p_et",
        "mfe_plant_params.mfe_plant__MFE_Power_Plant__p_th": f"{P}pb__p_th",
    }
    n = 0
    for old, new in repl.items():
        n += text.count(old)
        text = text.replace(old, new)
    PIPELINE.write_text(text)
    # The same dangling alias leaves 3 required-but-unminted fields in the
    # SystemDesign schema; the EntryPoint fails validating system_design.json
    # without them. After the repoint above nothing reads these, so fill them
    # with the oracle pb powers (unused, only to satisfy the generated schema).
    o = oracle_compute()
    sd = json.loads(SYS_DESIGN.read_text())
    sd.update({
        "mfe_plant__MFE_Power_Plant__p_th": o["p_th"],
        "mfe_plant__MFE_Power_Plant__p_the": o["p_the"],
        "mfe_plant__MFE_Power_Plant__p_et": o["p_et"],
    })
    SYS_DESIGN.write_text(json.dumps(sd, indent=2))
    print(f"[glue-1] BOP power wiring: repointed {n} input(s) to pb output "
          "channels; filled 3 spurious SystemDesign schema fields (unused)")


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



# NOTE (Item 10 cutover): the two-pass main() and HARNESS GLUE #2 (the Python capital
# rollup + placeholder overwrite) are DELETED. The rollup is now compiled by codegen as
# instance-scoped aggregation producers; run_stellaris_single.py runs it in one pass.
# This module retains only the shared helpers (CH, check, patch_bop_wiring/glue-1,
# run_pipeline) that the single-pass runner imports.
