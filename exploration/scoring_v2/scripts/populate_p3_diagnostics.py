"""Populate the supply_chain / customization / upper_cf diagnostic blocks
in every feature file. Idempotent. Re-run after weight or feature edits.

Usage:
    uv run python exploration/scoring_v2/scripts/populate_p3_diagnostics.py
"""
from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exploration.scoring_v2 import score
from exploration.scoring_v2.lib import feature_io, schema as schema_mod
from exploration.scoring_v2.lib.extractors import taxonomy as taxonomy_ext
from exploration.scoring_v2.embeddings import rulebook  # noqa: F401  registers
from exploration.scoring_v2.embeddings.rulebook import (
    _load_bottleneck_weights,
    _compute_triggered_bottlenecks,
    _load_customization_weights,
    _classify_thermal_rejection,
    _load_upper_cf_weights,
    _compute_triggered_cf_penalties,
)

WEIGHTS_PATH = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "default.yaml"


def _v(doc: dict, name: str, default: str = "") -> str:
    block = doc.get(name)
    if isinstance(block, dict):
        return str(block.get("value", default) or default)
    return default


def _round(v, digits: int = 4):
    if v is None:
        return None
    return round(float(v), digits)


def _supply_chain_block(doc: dict, weights: dict) -> dict:
    fuel = _v(doc, "fuel")
    blanket = _v(doc, "blanket_config")
    cf = _v(doc, "confinement_family")
    heating = _v(doc, "primary_heating")
    sev = _load_bottleneck_weights(weights)
    triggered = _compute_triggered_bottlenecks(fuel, blanket, cf, heating, sev)
    total = sum(triggered.values())
    return {
        "bottlenecks_triggered": dict(sorted(triggered.items())),
        "bottleneck_weight": _round(total),
        "supply_chain_score": _round(max(1.0, 5.0 - total)),
        "blanket_assumed": blanket == "TBD",
    }


def _customization_block(doc: dict, weights: dict) -> dict:
    fuel = _v(doc, "fuel")
    energy = _v(doc, "energy_capture")
    trs, fss = _load_customization_weights(weights)
    classification = _classify_thermal_rejection(energy)
    a = trs[classification]
    b = fss.get(fuel, fss["D-T"]) if (fuel and fuel != "Unknown") else fss["D-T"]
    raw = (a + b) / 2.0
    final = round(1.0 + (raw - 1.0) * (4.0 / 3.0), 2)
    return {
        "sub_factor_a": {
            "feature": "energy_capture",
            "value": energy,
            "classification": classification,
            "score": a,
        },
        "sub_factor_b": {
            "feature": "fuel",
            "value": fuel,
            "score": b,
        },
        "raw_average": _round(raw, 2),
        "customization_score": final,
    }


def _upper_cf_block(doc: dict, weights: dict) -> dict:
    fuel = _v(doc, "fuel")
    blanket = _v(doc, "blanket_config")
    op_mode = _v(doc, "operation_mode")
    sev = _load_upper_cf_weights(weights)
    triggered = _compute_triggered_cf_penalties(fuel, blanket, op_mode, sev)
    total = sum(triggered.values())
    return {
        "penalties_triggered": dict(sorted(triggered.items())),
        "operational_penalty_weight": _round(total),
        "upper_cf_score": _round(max(1.0, 5.0 - total)),
        "blanket_assumed": blanket == "TBD",
    }


def main() -> int:
    weights = yaml.safe_load(WEIGHTS_PATH.read_text())
    schema_mod.load_schema()  # validates the schema file loads cleanly
    today = _dt.date.today().isoformat()
    ids = taxonomy_ext.all_concept_ids()
    written = 0
    for cid in ids:
        doc = feature_io.read_features(cid)
        doc["_meta"] = {"concept_id": cid, "name": taxonomy_ext.concept_name(cid)}
        sc = _supply_chain_block(doc, weights)
        cu = _customization_block(doc, weights)
        ucf = _upper_cf_block(doc, weights)
        for key, block in (
            ("supply_chain_diagnostics", sc),
            ("customization_diagnostics", cu),
            ("upper_cf_diagnostics", ucf),
        ):
            existing = doc.get(key) or {}
            existing_no_ts = {k: v for k, v in existing.items() if k != "extracted_at"}
            if existing_no_ts == block:
                continue
            block_with_ts = dict(block, extracted_at=today)
            doc[key] = block_with_ts
            written += 1
        feature_io.write_features(cid, doc)
    print(f"populated/updated {written} diagnostic blocks across "
          f"{len(ids)} concepts (supply_chain + customization + upper_cf)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
