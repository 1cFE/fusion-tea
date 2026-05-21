"""Populate the `modularity_diagnostics` block in every feature file.

The block records the per-concept modularity score breakdown — what
embeddings fired, what lookup keys they used, what subsystem ratings
fed percent_mod, what the v5 calibration target is. Consumed by the
Score Explorer UI's concept-detail panel and useful for spot-debugging
calibration drift.

Idempotent: re-running produces zero diff if the inputs haven't changed.

Usage:
    uv run python exploration/scoring_v2/scripts/populate_modularity_diagnostics.py
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
from exploration.scoring_v2.embeddings import rulebook as _rulebook  # noqa: F401
from exploration.scoring_v2.embeddings.rulebook import (
    _mvs_key, _vessel_key, _magnet_driver_key,
)

WEIGHTS_PATH = REPO_ROOT / "exploration" / "scoring_v2" / "weights" / "default.yaml"
PREDICTED_SCORES_PATH = REPO_ROOT / "tests" / "scoring_v2" / "predicted_scores.yaml"


def _v(doc: dict, key: str, default: str = "") -> str:
    block = doc.get(key)
    if isinstance(block, dict):
        return str(block.get("value", default) or default)
    return default


def _populate_one(cid: str, doc: dict, weights: dict, schema: dict,
                  predicted: dict[str, float]) -> dict:
    """Compute the diagnostic block for one concept."""
    emb_values, _emb_conf = score._evaluate_concept(doc, weights, schema)

    cf       = _v(doc, "confinement_family")
    mfe_top  = _v(doc, "mfe_topology")
    ife_drv  = _v(doc, "ife_driver")
    mif_meth = _v(doc, "mif_method")
    nsm      = _v(doc, "non_standard_mechanism")
    tok_sh   = _v(doc, "tokamak_shape")
    stel_t   = _v(doc, "stellarator_type")
    mt       = _v(doc, "magnet_type")
    drv_t    = _v(doc, "driver_technology")
    ph       = _v(doc, "primary_heating")
    laser_a  = _v(doc, "laser_approach")
    fuel     = _v(doc, "fuel")
    blanket  = _v(doc, "blanket_config")

    mvs_key      = _mvs_key(cf, mfe_top, ife_drv, mif_meth, nsm, tok_sh,
                            drv_t, mt, ph, laser_a)
    vessel_key   = _vessel_key(cf, mfe_top, tok_sh, mif_meth, ife_drv, nsm,
                               fuel, mt)
    magnet_key   = _magnet_driver_key(cf, mt, drv_t, mfe_top, stel_t,
                                      ife_drv, mif_meth, nsm, ph)
    effective_blanket = "Liquid metal" if blanket == "TBD" else blanket
    blanket_key  = (f"{fuel}|*" if fuel in ("p-B11", "D-D", "D-He3")
                    else f"{fuel}|{effective_blanket}")

    # Capex shares used for the percent_mod weighted average
    w_vessel  = _v_num(doc, "w_vessel")
    w_coils   = _v_num(doc, "w_coils")
    w_blanket = _v_num(doc, "w_blanket")
    capex_total = sum(w for w in (w_vessel, w_coils, w_blanket) if w is not None)
    sparse_threshold = 0.30
    if any(w is None for w in (w_vessel, w_coils, w_blanket)):
        percent_mod_method = "equal_weight_fallback_missing_capex"
    elif capex_total <= 0 or capex_total < sparse_threshold:
        percent_mod_method = "equal_weight_fallback_sparse_capex"
    else:
        percent_mod_method = "capex_weighted"

    mvs                = emb_values.get("min_viable_device_scale")
    pmod               = emb_values.get("percent_mod")
    um                 = emb_values.get("unit_multiplicity")
    vessel_rating      = emb_values.get("vessel_modularity_rating")
    magnet_rating      = emb_values.get("magnet_driver_modularity_rating")
    blanket_rating     = emb_values.get("blanket_modularity_rating")

    # Composite score per axis (matches what score.py emits)
    axis_block = weights.get("modularity") or {}
    composite_score, _ev = score._score_axis(axis_block, emb_values, _emb_conf)

    block = {
        "min_viable_device_scale": _round(mvs),
        "percent_mod":             _round(pmod),
        "unit_multiplicity":       _round(um),
        "modularity_score":        _round(composite_score),
        "mvs_lookup_key":          mvs_key,
        "vessel_lookup_key":       vessel_key,
        "magnet_driver_lookup_key": magnet_key,
        "blanket_lookup_key":      blanket_key,
        "vessel_modularity_rating":         _round(vessel_rating),
        "magnet_driver_modularity_rating":  _round(magnet_rating),
        "blanket_modularity_rating":        _round(blanket_rating),
        "capex_shares_used": {
            "w_vessel":  _round(w_vessel),
            "w_coils":   _round(w_coils),
            "w_blanket": _round(w_blanket),
            "sum":       _round(capex_total) if capex_total is not None else None,
            "method":    percent_mod_method,
        },
        "unit_count_estimate":   _v_int(doc, "unit_count_estimate"),
        "blanket_assumed":       blanket == "TBD",
        "v5_calibration_target": predicted.get(cid),
    }
    return block


def _v_num(doc: dict, key: str) -> float | None:
    block = doc.get(key)
    if isinstance(block, dict):
        v = block.get("value")
        if v is None:
            return None
        try:
            return float(v)
        except (TypeError, ValueError):
            return None
    return None


def _v_int(doc: dict, key: str) -> int | None:
    block = doc.get(key)
    if isinstance(block, dict):
        v = block.get("value")
        try:
            return int(v)
        except (TypeError, ValueError):
            return None
    return None


def _round(v: float | None, digits: int = 4) -> float | None:
    if v is None:
        return None
    return round(float(v), digits)


def main() -> int:
    weights = yaml.safe_load(WEIGHTS_PATH.read_text())
    schema = schema_mod.load_schema()
    predicted = yaml.safe_load(PREDICTED_SCORES_PATH.read_text()).get("modularity", {})
    today = _dt.date.today().isoformat()

    ids = taxonomy_ext.all_concept_ids()
    written = 0
    for cid in ids:
        doc = feature_io.read_features(cid)
        doc["_meta"] = {"concept_id": cid, "name": taxonomy_ext.concept_name(cid)}
        block = _populate_one(cid, doc, weights, schema, predicted)
        existing = doc.get("modularity_diagnostics") or {}
        # Strip extracted_at from comparison; we always refresh that field
        existing_no_ts = {k: v for k, v in existing.items() if k != "extracted_at"}
        if existing_no_ts == block:
            continue
        block["extracted_at"] = today
        doc["modularity_diagnostics"] = block
        feature_io.write_features(cid, doc)
        written += 1
    print(f"updated modularity_diagnostics for {written} concept(s); "
          f"{len(ids) - written} unchanged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
