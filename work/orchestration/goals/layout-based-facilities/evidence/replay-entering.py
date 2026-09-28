"""Reproduce entering package diagnostics before facilities implementation.

Use only at entering package identity; later runs must use preserved entering package.
No historical study is modified. Both actual defaults and retained selected18 inputs are evaluated.
"""
from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[5]
HOME = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(os.environ["STOP_PARSER_TEAX_ROOT"]) / "packages/teax-simkit"))
from exploration.stellarator_e2e.studies import study_route as route

points = [{}, json.loads((ROOT / "work/orchestration/goals/installed-cooling-equipment-costs/evidence/starting-cases.json").read_text())["cases"][0]["inputs"]]
contract = json.loads((route.PACKAGE_DIR / "contracts/model_contract.json").read_text())
required = {o["channel_name"]: o["channel_name"] for o in contract["outputs"] if o["python_type"] in ("float", "int")}
cases, db = route.run_points("layout-facilities-entering", points, HOME / "entering-replay", required_channels=required)
rows = [{"id": c.candidate_id, "inputs": dict(c.inputs), "outputs": dict(c.outputs or {}), "verdicts": dict(c.verdicts or {}), "state": c.state} for c in cases]
(HOME / "entering-replay.json").write_text(json.dumps({"scope": "Current-default and prior selected-point diagnostic replay of entering package; not historical results or a facilities study", "store": str(db.relative_to(ROOT)), "cases": rows}, indent=2, allow_nan=False) + "\n")
assert all(c.state == "completed" for c in cases)
