"""Exercise migration admission on real controls and a synthetic new input schema."""
import json
from pathlib import Path
from exploration.whole_plant_conversion.studies.migrate_controls import GROUPS, NEW, OLD, RETIRED, migrate

ROOT = Path.cwd()
HERE = Path(__file__).resolve().parent
source = ROOT / "exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/results/cases.json"
rows = json.loads(source.read_text())["cases"]
base = rows[0]["inputs"]
schema = {NEW + k.removeprefix(OLD): v for k, v in base.items() if k not in RETIRED}
schema.update({NEW + key: base[OLD + sources[0]] for key, sources in GROUPS.items()})
schema[NEW + "new_fixture_only"] = 123.0
checks = []
for row in rows:
    result = migrate(row["inputs"], schema)
    assert result[NEW + "source_basis__q_source_MW"] == row["inputs"][OLD + "blanket_source__q_source"]
    assert result[NEW + "finance__availability"] == .85
    assert result[NEW + "new_fixture_only"] == 123.0
    assert len(result) == len(schema)


def refusal(name, changes=None, removed=None, overrides=None):
    values = dict(base)
    values.update(changes or {})
    if removed:
        values.pop(removed)
    try:
        migrate(values, schema, overrides=overrides)
    except ValueError:
        checks.append(name)
    else:
        raise AssertionError("accepted invalid request: " + name)


refusal("source_collision", {NEW + "source_basis__q_source_MW": 999.0})
refusal("rate_collision", {OLD + "gas_ledger__rate": .2})
refusal("availability_collision_before_override", {OLD + "gas_ledger__availability": .9}, overrides={NEW + "finance__availability": .8})
refusal("new_finance_collision", {NEW + "finance__years": 20})
refusal("missing_old", removed=OLD + "blanket_source__q_source")
refusal("unknown_key", {OLD + "unknown": 1})
refusal("nonfinite", {OLD + "blanket_source__q_source": float("nan")})
refusal("fractional_legacy_horizon", {OLD + "steam_ledger__years": 30.5, OLD + "gas_ledger__years": 30.5}, overrides={NEW + "finance__years": 30})
refusal("fractional_scenario_horizon", overrides={NEW + "finance__years": 30.5})
refusal("unknown_override", overrides={NEW + "unknown": 1})
assert migrate(base | {NEW + "source_basis__q_source_MW": base[OLD + "blanket_source__q_source"]}, schema) == migrate(base, schema)
assert migrate(base, schema, overrides={NEW + "finance__availability": .8})[NEW + "finance__availability"] == .8
receipt = {"status": "pass", "controls": len(rows), "refusals": checks,
           "equal_source_duplicate_accepted": True, "explicit_shared_override_accepted": True,
           "scope": "Input mapping only; synthetic new schema. No new package or model execution."}
(HERE / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt))
