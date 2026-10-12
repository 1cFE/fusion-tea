"""Compare the 15 Sept sized cases with the current-model supplied-winding replay.

Run after extract_joint_sizing.py and replay_supplied_windings.py:
    uv run python .project/active/write-up/magnet-study-evaluation/compare_replay.py
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = "stellarator_09__stellaris__"
old = {r["proposal_id"]: r for r in csv.DictReader((HERE / "data/joint-sizing-three-cases.csv").open())}
new = {r["candidate_id"].split(":")[1]: r for r in json.loads((HERE / "replay/native-cases.json").read_text())}
PAIRS = [("reference", "c0000"), ("g-12.7-1.3-1.54e+07-0.3", "c0001"), ("g-12.7-1.3-1.54e+07-0.6", "c0003")]
FIELDS = [
    ("installed_tapes_ref", "magnet__conductor_current__parallel_tapes_reference"),
    ("fit_margin_x_m", "magnet__wp_fit__margin_x"),
    ("fit_margin_y_m", "magnet__wp_fit__margin_y"),
    ("B_peak_T", "magnet__peak_field_calc__B_peak"),
    ("tape_length_m", "magnet__winding_procurement__tape_length"),
    ("stored_energy_J", "magnet__stored_energy__W_mag"),
    ("magnet_priced_subtotal_usd", "magnet__magnet_capital_rollup__capital_cost"),
    ("lcoe_usd_per_MWh", "lcoe_calc__lcoe"),
]
rows = []
for old_id, new_id in PAIRS:
    o, n = old[old_id], {k.replace(P, ""): v for k, v in new[new_id]["outputs"].items()}
    for name, channel in FIELDS:
        a, b = float(o[name]), n.get(channel)
        rows.append({"sept15_case": o["candidate_id"], "replay_case": new_id, "quantity": name,
                     "sept15": a, "replay": b, "rel_diff": None if b is None else (b - a) / a if a else b - a})
with (HERE / "data/sept15-vs-replay.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
for r in rows:
    print(f"{r['replay_case']} {r['quantity']:28s} {r['sept15']:>18.6g} {r['replay'] if r['replay'] is None else format(r['replay'], '>18.6g')} {r['rel_diff'] if r['rel_diff'] is None else format(r['rel_diff'], '+.2e')}")
