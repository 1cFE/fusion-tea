"""Read generated bindings only; never evaluate or alter the native package."""
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[5]
PKG = ROOT / "exploration/aries_integrated/aries_integrated"
INV = ROOT / "exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/generated-interface-inventory.json"
inventory = json.loads(INV.read_text())
pipeline = yaml.safe_load((PKG / "pipelines/pipeline.yaml").read_text())
attributes = [
    "he_hx.selected_area", "pbli_hx.selected_area", "divertor_hx.selected_area",
    "cycle.selected_flow", "compressor_1.selected_ratio", "compressor_2.selected_ratio", "compressor_3.selected_ratio",
    "he_hx.assumed_u", "pbli_hx.assumed_u", "divertor_hx.assumed_u",
    "cycle.recuperator_effectiveness", "cycle.turbine_efficiency",
    "compressor_1.efficiency", "compressor_2.efficiency", "compressor_3.efficiency",
    "fuel_inventory.annual_recovery_kg", "finance.supply_service_annual",
    "cost_schedule.availability", "cost_schedule.replacement_life_fpy",
    "finance.discount_rate", "fuel_inventory.tritium_price", "annual_om.selected_amount",
    "he_hx.price_factor", "pbli_hx.price_factor",
    "compressor_capacity.selected_rating", "turbine_capacity.selected_rating",
]
entries = [("aries_integrated_plant::" + a.replace(".", "::"), "aries_integrated_plant__" + a.replace(".", "__")) for a in attributes]
entries.append(("aries_cs_plasma_integration::plasma::amplitude", "aries_cs_plasma_integration__plasma__amplitude"))
rows = []
for attribute, key in entries:
    group = inventory["entry_keys"][key]
    actual = json.loads((PKG / "inputs" / (group + ".json")).read_text())
    assert key in actual
    consumers = []
    for module, config in pipeline["modules"].items():
        for port, binding in config.get("inputs", {}).items():
            if isinstance(binding, str) and binding.split()[-1] == group + "." + key:
                consumers.append({"module": module, "port": port, "binding": binding})
    assert consumers, key
    rows.append(dict(attribute=attribute, entry_keys=[key], group=group, baseline=actual[key], direct_consumers=consumers))
contract = json.loads((PKG / "contracts/model_contract.json").read_text())
channels = inventory["produced_channels"]
selected_channels = [k for k in channels if k.startswith("aries_integrated_plant__lifecycle_accounts__evaluate__") or k.endswith("__lifecycle_price__evaluate__lcoe") or k.endswith("__plant_ledger__evaluate__net_electric") or k.startswith("aries_integrated_plant__fuel_inventory__annual__")]
paths = [PKG / "pipelines/pipeline.yaml", PKG / "contracts/model_contract.json", INV, ROOT / "models/designs/aries_cs_integrated/plant.sysml"]
result = dict(scope="Static independent binding audit; no native executions", files={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}, fingerprints=inventory["fingerprints"]["recorded_provenance"], attributes=rows, report_channels=sorted(selected_channels), constraints=[{k: c[k] for k in ("constraint_id", "owner_instance_path", "source_local_identity", "evaluation_channel")} for c in contract["constraint_catalog"]["concrete_entries"]])
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"attributes": len(rows), "constraints": len(result["constraints"]), "report_channels": len(selected_channels), "output": str(Path(__file__).with_suffix(".json"))}))
