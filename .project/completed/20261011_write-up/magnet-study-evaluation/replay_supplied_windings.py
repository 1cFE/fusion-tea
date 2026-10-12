"""Targeted replay: the 15 September windings as supplied designer choices on the current model.

Question: under the post-repair model (MR-7: supplied winding, capacity checks, nothing
enlarged), does the 15 September three-step sequence still hold when the larger windings
are supplied rather than sized?

Four cases on the current generated package; only magnet geometry inputs change:
  s0  published winding (current defaults: 0.36 m side, 0.30 m radial / 0.40 m transverse)
  s1  15 Sept current-sized side 0.525309 m supplied, original allocation
  s2  same supplied 0.525309 m winding, allocation enlarged to 0.60 / 0.60 m
  s3  15 Sept re-sized side 0.527810 m supplied, allocation 0.60 / 0.60 m (c0007 winding)
Turns (308), turn current (50 kA), support/casing masses, cryoplant and all other inputs
stay at package defaults. No model or package file is edited; hashes are compared.

Run from the repository root (needs the sealed runtime environment):

    .codex-test/run python .project/active/write-up/magnet-study-evaluation/replay_supplied_windings.py
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent / "replay"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(os.environ["STOP_PARSER_TEAX_ROOT"]) / "packages/teax-simkit"))
sys.path.insert(0, str(ROOT / "exploration/stellarator_e2e/studies"))
import study_route as route  # noqa: E402

P = route.P
SIDE_C0005 = 0.5253087270279885  # 20260915 native c0005 magnet__wp_sizing__wp_side
SIDE_C0007 = 0.5278095832116102  # 20260915 native c0007 magnet__wp_sizing__wp_side
CASES = {
    "s0-published": {},
    "s1-supplied-sized-side": {P + "magnet__winding_pack__wp_side": SIDE_C0005},
    "s2-same-winding-enlarged": {
        P + "magnet__winding_pack__wp_side": SIDE_C0005,
        P + "magnet__coil__coil_t": 0.6,
        P + "magnet__casing__interior_y": 0.6,
    },
    "s3-c0007-winding-enlarged": {
        P + "magnet__winding_pack__wp_side": SIDE_C0007,
        P + "magnet__coil__coil_t": 0.6,
        P + "magnet__casing__interior_y": 0.6,
    },
}
REPORT = (
    "magnet__winding_pack__wp_side", "magnet__coil__coil_t", "magnet__casing__interior_y",
    "rb__r_coil_centre", "peak_field", "B_peak", "tape_critical_current", "parallel_tapes_reference",
    "operating_fraction_reference", "margin_current", "field_extrapolated", "wp_fit__margin_x",
    "wp_fit__margin_y", "tape_length", "conductor_length", "magnet_capital_rollup__capital_cost",
    "vol_cold_total", "cold_stage", "intercept", "refrigeration", "sigma_wp", "eps_cond", "lcoe_calc__lcoe",
)


def hashes() -> dict[str, str]:
    bases = [ROOT / "exploration/stellarator_e2e/generated", ROOT / "models"]
    return {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for base in bases for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts
    }


def save(name: str, value) -> None:
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    before = hashes()
    route.write_identity_document(route.PACKAGE_DIR, OUT / "package-identity.json")
    save("declared-cases.json", CASES)
    try:
        cases, _db = route.run_points("magnet-supplied-winding-replay", list(CASES.values()), OUT / "native")
        rows = [dataclasses.asdict(c) if dataclasses.is_dataclass(c) else dict(vars(c)) for c in cases]
        save("native-cases.json", rows)
        summary = []
        for label, row in zip(CASES, rows):
            outputs = {k.replace(P, ""): v for k, v in (row.get("outputs") or {}).items()}
            inputs = {k.replace(P, ""): v for k, v in (row.get("inputs") or {}).items()}
            picked = {k: v for k, v in {**inputs, **outputs}.items() if any(s in k for s in REPORT)}
            verdicts = {k.replace(P, "").rsplit("__", 1)[0]: v for k, v in (row.get("verdicts") or {}).items()}
            summary.append({
                "label": label,
                "candidate_id": row.get("candidate_id"),
                "state": row.get("state"),
                "values": picked,
                "violated": sorted(k for k, v in verdicts.items() if v != "satisfied"),
                "magnet_verdicts": {k: verdicts.get(k) for k in ("reference_conductor_current_ok", "wp_fit_ok", "peak_field_ok", "cold_stage_capacity_ok", "intercept_stage_capacity_ok", "wp_stress_ok", "cond_strain_ok")},
            })
        save("summary.json", summary)
        print(json.dumps(summary, indent=1, default=str))
    finally:
        after = hashes()
        save("preservation.json", {
            "before_count": len(before), "after_count": len(after),
            "changed": [k for k in before if before[k] != after.get(k)],
            "added": sorted(set(after) - set(before)), "removed": sorted(set(before) - set(after)),
        })


if __name__ == "__main__":
    main()
