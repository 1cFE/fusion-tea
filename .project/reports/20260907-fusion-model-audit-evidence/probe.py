"""Reproduce audit counterexamples without changing model/package files.

Run from the repository root with uv run --no-sync python <this file>.
Results are written beside this script. STOP_PARSER_TEAX_ROOT selects TEAx.
"""

import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
os.environ.setdefault("STOP_PARSER_TEAX_ROOT", "/home/reid/1cfe/teax")
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e"))
import run_stellaris  # Strict-loads the sealed package; creates only a temp link.
import verify_stellaris as oracle


def generated(module, function, **inputs):
    fn = getattr(importlib.import_module("stellarator_tea.handwritten." + module), function)
    try:
        return {"result": fn(SimpleNamespace(**inputs))}
    except Exception as exc:
        return {"error": type(exc).__name__, "message": str(exc)}


results = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()}
results["executable_fingerprint"] = run_stellaris.EXECUTABLE_FINGERPRINT
results["equal_interest_inflation"] = generated(
    "mfe_account_costs.levelized_annual_cost_impl", "run_levelized_annual_cost",
    annual_cost=1e6, interest_rate=0.02, inflation_rate_in=0.02,
    operational_years_in=30., project_time=8.,
)
i = .02
crf = i * (1+i)**30 / ((1+i)**30-1)
results["equal_interest_inflation"]["finite_limit"] = crf * 1e6 * (1+i)**8 * 30 / (1+i)
results["zero_discount"] = generated(
    "mfe_lcoe_dcf.lcoe_dcf_impl", "run_lcoe_dcf", total_capital_in=1e9,
    annual_om_in=1e7, net_electric_mw=1000., availability_in=.85,
    discount_rate_in=0., construction_years_in=8., operational_years_in=30.,
)
results["zero_discount"]["finite_limit"] = (1e9/30 + 1e7)/(8760*1000*.85)
results["invalid_coil_bore"] = generated(
    "mfe_plasma_scaling.conductor_peak_field_impl", "run_conductor_peak_field",
    B_axis_in=9., peak_ratio_in=24.9/9., R_in=12.7, a_coil_in=13.,
    R_ref_in=12.7, a_coil_ref_in=3.1500000000000004,
)
results["ife"] = {
    "bank_energy_J": 14.286e6,
    "beam_energy_model_MJ": .35*14.286e6/1e6,
    "gross_electric_MW": 14.286e6*3.5*.43*1.15*80*.35/1e6,
    "net_electric_MW": 14.286e6*3.5*(.43*1.15*80*.35-2)/1e6,
    "reported_driver_recirc": 1/(.43*1.15*80*.35),
    "lcoe_total_recirc": 2/(.43*1.15*80*.35),
    "viable_but_negative_power": {"eta": .1, "gain":100., "M":.6, "eta_th":.3,
        "eta_gain":10., "cycle_gain":1.8, "net_per_bank_watt":-.2},
}
baseline = oracle.compute()
results["baseline_oracle"] = baseline
results["heating_operating_gap"] = {
    "installed_coupled_MW": baseline["heat_coupled"],
    "required_coupled_MW": baseline["p_aux_required"],
    "excess_heat_MW": baseline["heat_coupled"] - baseline["p_aux_required"],
    "net_increase_at_zero_required_MW_fixed_other_loads":
        baseline["heat_wallplug_total"] - baseline["heat_coupled"]*.333*(1-.03),
}

# Read-only model/citation inventory. Numeric rows are a census, not source certification.
inventory = []
numeric_rows = []
source_paths = []
for file in sorted((ROOT / "models").rglob("*.sysml")):
    raw = file.read_text()
    inventory.append({"file":str(file.relative_to(ROOT)), "sha256":hashlib.sha256(file.read_bytes()).hexdigest(),
                      "lines":len(raw.splitlines())})
    stripped = re.sub(r"/\*.*?\*/", lambda m:"\n"*m.group().count("\n"), raw, flags=re.S)
    for n, line in enumerate(stripped.splitlines(),1):
        if re.search(r"(?:=|\bdefault\b).*\d",line.split("//")[0]):
            numeric_rows.append({"file":str(file.relative_to(ROOT)),"line":n,"expression":line.strip()})
    for match in re.finditer(r"(?:work/(?:active|completed)|knowledge|modeling_project|/home/reid/1cfe)/[^\s;,)]+",raw):
        path = match.group().rstrip(".:")
        source_paths.append({"file":str(file.relative_to(ROOT)),"line":raw[:match.start()].count("\n")+1,
                             "path":path,"exists":(ROOT/path).exists()})
results["model_inventory"] = inventory
results["numeric_census_count"] = len(numeric_rows)
(OUT/"numeric-census.json").write_text(json.dumps(numeric_rows,indent=2)+"\n")
(OUT/"path-census.json").write_text(json.dumps(source_paths,indent=2)+"\n")
(OUT/"probe-results.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps({k:v for k,v in results.items() if k not in {"baseline_oracle","model_inventory"}},indent=2))
