"""Populate plant_complexity_diagnostics and technical_feasibility_diagnostics
blocks for every concept. Idempotent.

Usage:
    uv run python exploration/scoring_v2/scripts/populate_p4_diagnostics.py
"""
from __future__ import annotations

import datetime as _dt
import math
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exploration.scoring_v2.lib import feature_io
from exploration.scoring_v2.lib.extractors import taxonomy as taxonomy_ext
from exploration.scoring_v2.embeddings import rulebook  # noqa: F401  registers
from exploration.scoring_v2.embeddings.rulebook import (
    _load_pc_weights,
    _compute_triggered_pc_subsystems,
    _load_tf_tables,
    _required_for,
    _tf_score_from_log_gap,
    _TF_FLOOR_SCORE,
)

WEIGHTS_PATH = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "default.yaml"


def _v(doc: dict, name: str) -> str:
    block = doc.get(name)
    if isinstance(block, dict):
        return str(block.get("value", "") or "")
    return ""


def _round(v, digits: int = 4):
    if v is None:
        return None
    return round(float(v), digits)


def _plant_complexity_block(doc: dict, weights: dict) -> dict:
    sev = _load_pc_weights(weights)
    triggered = _compute_triggered_pc_subsystems(
        _v(doc, "fuel"),
        _v(doc, "confinement_family"),
        _v(doc, "confinement_concept"),
        _v(doc, "ife_driver"),
        _v(doc, "mif_method"),
        _v(doc, "magnet_type"),
        _v(doc, "blanket_config"),
        _v(doc, "energy_capture"),
        _v(doc, "primary_heating"),
        _v(doc, "operation_mode"),
        _v(doc, "repetition_rate"),
        sev,
    )
    total = sum(triggered.values())
    return {
        "subsystems_triggered": dict(sorted(triggered.items())),
        "subsystem_complexity_weight": _round(total),
        "plant_complexity_score": _round(max(1.0, 5.0 - total)),
        "blanket_assumed": _v(doc, "blanket_config") == "TBD",
    }


def _technical_feasibility_block(doc: dict, weights: dict) -> dict:
    required, achieved = _load_tf_tables(weights)
    fuel = _v(doc, "fuel") or "Unknown"
    cf = _v(doc, "confinement_family")
    cc = _v(doc, "confinement_concept")
    laser = _v(doc, "laser_approach")
    key = f"{cf}|{cc}"
    required_value = _required_for(required, fuel, cf) if fuel in required else None
    achieved_value = achieved.get(key)
    if achieved_value is None or achieved_value <= 0:
        gap = None
        log_gap = None
        base_score = _TF_FLOOR_SCORE
    else:
        gap = required_value / achieved_value
        log_gap = math.log10(gap) if gap > 0 else None
        base_score = _tf_score_from_log_gap(log_gap)
    modifier = 0.0
    if cf == "IFE" and laser:
        mods = weights.get("technical_feasibility", {}).get("laser_approach_modifier", {})
        modifier = float(mods.get(laser, 0.0))
    final = max(1.0, min(5.0, base_score + modifier))
    return {
        "required_triple_product": required_value,
        "achieved_triple_product": achieved_value,
        "achieved_lookup_key": key,
        "triple_product_gap": _round(gap),
        "log10_gap": _round(log_gap, 3),
        "base_score_from_gap": base_score,
        "laser_approach_modifier": _round(modifier, 2),
        "technical_feasibility_score": _round(final, 2),
        "no_data_floor": achieved_value is None,
    }


def main() -> int:
    weights = yaml.safe_load(WEIGHTS_PATH.read_text())
    today = _dt.date.today().isoformat()
    ids = taxonomy_ext.all_concept_ids()
    written = 0
    for cid in ids:
        doc = feature_io.read_features(cid)
        doc["_meta"] = {"concept_id": cid, "name": taxonomy_ext.concept_name(cid)}
        for key, block_fn in (
            ("plant_complexity_diagnostics", _plant_complexity_block),
            ("technical_feasibility_diagnostics", _technical_feasibility_block),
        ):
            block = block_fn(doc, weights)
            existing = doc.get(key) or {}
            existing_no_ts = {k: v for k, v in existing.items() if k != "extracted_at"}
            if existing_no_ts == block:
                continue
            doc[key] = dict(block, extracted_at=today)
            written += 1
        feature_io.write_features(cid, doc)
    print(f"populated/updated {written} diagnostic blocks across {len(ids)} concepts "
          f"(plant_complexity + technical_feasibility)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
