"""Cost-model extractor.

Parses exploration/concept_analysis/analyses/{concept_id}/model_output.txt and
emits capex weight-share features for the modularity axis:

  Legacy 3-slot (MFE path):
    w_vessel, w_coils, w_blanket
    consumed by _percent_mod_mfe via the existing vessel/magnet_driver/blanket
    lookups.

  New 2-slot (IFE/MIF path, added 2026-06-17):
    w_energy_delivery, w_containment
    consumed by _percent_mod_ife_mif via driver_modularity_lookup and
    chamber_blanket_lookup. Account groupings are family-specific:
      IFE energy_delivery: C220104 + C220107 + C220103 (laser + pulsed PS + ancillary coils)
      MIF energy_delivery: C220103 + C220104 + C220107 (compression coils + driver hw + pulsed PS)
      IFE/MIF containment: C220105 + C220106 + C220108 + C220101 + CAS27
    The new path drops the sparse-capex threshold — 2-slot within-two
    normalization is well-behaved at any share level.

Behavior:
- Sum `$` per subsystem bucket using the static CAS_TO_SUBSYSTEM dict below
  (mapping kept across all 7 subsystems so the dollars are correctly
  classified before normalization).
- Each `w_*` is the bucket's share of the 7-subsystem total covered $ (so
  the source shares sum to 1.0 across all 7; the percent_mod embedding
  renormalizes the retained shares to sum to 1.0 within itself).
- For the family-specific w_energy_delivery and w_containment features,
  the extractor reads confinement_family from features/{cid}.yaml to
  pick the correct CAS account grouping.
- Codes seen in the file but absent from the dict are ignored (financial,
  indirect, O&M, fuel, IDC, contingency).
- Codes in the dict not seen in the file contribute 0 to that bucket.
- If `model_output.txt` does not exist for the concept, the extractor
  returns no value (raises KeyError). No fallback.

KNOWN LIMITATION — per-module vs plant-wide mixed basis:
For concepts where the cost model uses n_mod > 1 (Helion, GF MTF, NearStar
MTIF, possibly others), the model_output.txt sub-account values are emitted
PER MODULE for the CAS22 sub-accounts (C220101-C220110, C220112) while the
top-level CAS lines (CAS10, CAS21, ...) are plant-wide totals. The parser
reads each dollar value without rescaling per-module subs to fleet aggregate,
so capex SHARES for multi-module concepts mix per-module numerators with
plant-wide denominators. Under the 2-slot path this no longer affects the
percent_mod RATING (within-two normalization is invariant to the mismatch
since both slots are per-module sub-accounts), but the shares as DISPLAYED
in the diagnostic block remain on the mixed basis. File a separate issue
to fix the parser to derive n_mod_eff from C220000 and scale per-module
accounts before computing shares.

The dispatcher signature `extract(cid, fname, schema_entry) -> (value, prov, conf)`
is provided so the bulk pipeline can call this extractor like any other.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]
ANALYSES_DIR = ROOT / "exploration" / "concept_analysis" / "analyses"

# Internal bucket set: covers every subsystem the CAS-to-subsystem dict
# below maps onto, so the parser can classify every $ in the file.
SUBSYSTEMS = ("vessel", "coils", "blanket", "bop", "fuel_cycle", "aux", "civil")

# Externally-exposed subsystem set: the modularity percent_mod embedding
# consumes these. Legacy 3-slot (MFE path) uses vessel/coils/blanket.
# 2-slot (IFE/MIF path) uses energy_delivery/containment.
EMITTED_SUBSYSTEMS = ("vessel", "coils", "blanket")
EMITTED_2SLOT = ("energy_delivery", "containment")

# CAS account → subsystem bucket for the LEGACY 3-slot MFE path. The seven
# buckets cover every classified CAS22 sub-account so dollars are correctly
# normalized within the plant total.
CAS_TO_SUBSYSTEM: dict[str, str] = {
    # vessel
    "C220105": "vessel", "C220106": "vessel", "C220108": "vessel",
    # coils / driver
    "C220103": "coils",  "C220107": "coils",
    # blanket & first wall
    "C220101": "blanket", "CAS27":  "blanket",
    # power conversion / BOP
    "C220109": "bop", "C220200": "bop",
    "CAS23":   "bop", "CAS24":   "bop", "CAS26": "bop",
    # fuel cycle
    "C220112": "fuel_cycle", "C220400": "fuel_cycle", "C220500": "fuel_cycle",
    # auxiliaries
    "C220104": "aux", "C220110": "aux", "C220300": "aux",
    "C220600": "aux", "C220700": "aux",
    "CAS25":   "aux", "CAS28":   "aux",
    # civil / shielding
    "C220102": "civil", "C220111": "civil",
    "CAS10":   "civil", "CAS21":   "civil",
}

# Family-specific account groupings for the 2-slot path. Both slots' shares
# are computed against the same plant-wide classified total (i.e., same
# denominator as the 3-slot path) so cross-family magnitudes are comparable.
# - IFE energy_delivery: laser/driver lives in C220104; pulsed PS + ancillary
#   coils in C220107/C220103 (small for most concepts).
# - MIF energy_delivery: compression coils (C220103) + driver hardware
#   (C220104) + pulsed PS (C220107) — all three contribute meaningfully
#   depending on the MIF flavor.
# - Containment: chamber + first wall + blanket. Same set across families
#   (the chamber and blanket are physically intertwined).
TWOSLOT_ACCOUNTS: dict[str, dict[str, list[str]]] = {
    "IFE": {
        "energy_delivery": ["C220104", "C220107", "C220103"],
        "containment":     ["C220105", "C220106", "C220108", "C220101", "CAS27"],
    },
    "MIF": {
        "energy_delivery": ["C220103", "C220104", "C220107"],
        "containment":     ["C220105", "C220106", "C220108", "C220101", "CAS27"],
    },
}

# Codes ignored even when present (financial, indirect, O&M, fuel, IDC, contingency,
# and the CAS22/C220000 aggregate rollup rows).
_IGNORE_CODES = {
    "CAS22", "CAS29", "CAS30", "CAS40", "CAS50", "CAS60", "CAS70", "CAS80", "CAS90",
    "C220000",
}

# Two file shapes in the wild:
#
#   Format A (canonical, 01-hts-compact-tokamak):
#       C220103   Coils (REBCO magnets+struct)       6901.0  [ARC §6 override]
#       C220103           808.3       1500.0       1500.0  <-- OVERRIDE
#   Both bracketed annotations and the arrow-tagged "<-- OVERRIDE" marker
#   that costingfe prints after analyst-overridden CAS rows are tolerated as
#   optional trailing prose after the dollars field.
#
#   Format B (sub-allocation prose, e.g. 10-large-scale-stellarator):
#         Coil system (C220103)                     2595.5 M$  (40% of base CAS22)
#         Blanket/VV (C220101+C220106) base         2595.5 M$  (40% of base)
#
# Format B can chain multiple codes inside the parens with "+"; the dollars are
# split evenly across them.
#
# Format C variant (dollar-prefixed amounts, e.g. 12-levitated-dipole):
#       C220101 Li2O Blanket               $   349.0M  [MASS-BASED OVERRIDE]
#       C220101 Chamber Wall               $20.0k/mod  $20.00M fleet [override]
# These per-line ambiguous money tokens are not parsed in this slice.

_FORMAT_A_RE = re.compile(
    r"^\s*(?P<code>(?:CAS\d{2,3}|C\d{6}))\s+.+?\s+(?P<dollars>-?\d+(?:\.\d+)?)"
    r"\s*(?:\[[^\]]*\]|<-{1,2}\s*[A-Za-z].*)?\s*$"
)

_FORMAT_B_RE = re.compile(
    r"\((?P<codes>C\d{6}(?:\+C\d{6})*)\)[^$\n]*?(?P<dollars>\d+(?:\.\d+)?)\s*M\$"
)


def _model_output_path(concept_id: str) -> Path:
    return ANALYSES_DIR / concept_id / "model_output.txt"


def _parse_lines(text: str) -> dict[str, float]:
    """Return {code: dollars} aggregated over every recognized line in the file."""
    out: dict[str, float] = {}
    for raw in text.splitlines():
        m = _FORMAT_A_RE.match(raw)
        if m:
            code = m.group("code")
            try:
                out[code] = out.get(code, 0.0) + float(m.group("dollars"))
            except ValueError:
                pass
            continue
        m = _FORMAT_B_RE.search(raw)
        if m:
            try:
                dollars = float(m.group("dollars"))
            except ValueError:
                continue
            codes = m.group("codes").split("+")
            share = dollars / len(codes)
            for code in codes:
                out[code] = out.get(code, 0.0) + share
    return out


def compute_weights(concept_id: str) -> dict[str, float] | None:
    """Return the seven capex weight shares for `concept_id`, or None if no cost model.

    Output keys: SUBSYSTEMS. Values sum to 1.0 (within float).
    """
    p = _model_output_path(concept_id)
    if not p.exists():
        return None
    rows = _parse_lines(p.read_text(encoding="utf-8", errors="replace"))
    buckets: dict[str, float] = {s: 0.0 for s in SUBSYSTEMS}
    for code, dollars in rows.items():
        if code in _IGNORE_CODES:
            continue
        sub = CAS_TO_SUBSYSTEM.get(code)
        if sub is None:
            continue
        buckets[sub] += dollars
    total = sum(buckets.values())
    if total <= 0:
        return None
    return {s: buckets[s] / total for s in SUBSYSTEMS}


def _read_concept_family(concept_id: str) -> str | None:
    """Read confinement_family from features/{cid}.yaml.

    Returns None if the feature file is unreadable or family is missing.
    The 2-slot extractor needs this to pick the correct CAS account grouping.
    """
    import yaml
    features_path = ROOT / "exploration" / "scoring_v2" / "features" / f"{concept_id}.yaml"
    if not features_path.exists():
        return None
    try:
        data = yaml.safe_load(features_path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    entry = data.get("confinement_family")
    if isinstance(entry, dict):
        return entry.get("value")
    return entry


def compute_twoslot_weights(concept_id: str) -> dict[str, float] | None:
    """Return 2-slot capex shares (energy_delivery, containment) for IFE/MIF.

    Same denominator as compute_weights() — sum of all classified accounts —
    so the slot shares are interpretable as fraction-of-plant-cost directly.

    Returns None if:
      - no model_output.txt for the concept
      - confinement_family not IFE/MIF (MFE uses the legacy 3-slot path)
      - total classified $ is non-positive (no model output)
    """
    family = _read_concept_family(concept_id)
    if family not in TWOSLOT_ACCOUNTS:
        return None
    p = _model_output_path(concept_id)
    if not p.exists():
        return None
    rows = _parse_lines(p.read_text(encoding="utf-8", errors="replace"))
    # Filter to classified accounts (same as legacy compute_weights)
    classified_total = 0.0
    for code, dollars in rows.items():
        if code in _IGNORE_CODES:
            continue
        if CAS_TO_SUBSYSTEM.get(code) is None:
            continue
        classified_total += dollars
    if classified_total <= 0:
        return None
    slot_accounts = TWOSLOT_ACCOUNTS[family]
    return {
        slot: sum(rows.get(c, 0.0) for c in codes) / classified_total
        for slot, codes in slot_accounts.items()
    }


def unrecognized_codes(concept_id: str) -> list[str]:
    """Codes seen in model_output.txt that are neither classified nor explicitly ignored."""
    p = _model_output_path(concept_id)
    if not p.exists():
        return []
    rows = _parse_lines(p.read_text())
    return sorted(
        code for code in rows
        if code not in CAS_TO_SUBSYSTEM and code not in _IGNORE_CODES
    )


def extract(
    concept_id: str, feature_name: str, schema_entry: dict[str, Any]
) -> tuple[Any, str, str]:
    """Dispatcher entry point: return one w_* value for one concept.

    Raises KeyError if no cost model exists for the concept — the bulk caller
    treats this as "leave the feature absent" rather than fabricating a value.

    Handled feature names:
      Legacy 3-slot (all families):
        w_vessel, w_coils, w_blanket
      2-slot (IFE/MIF only, raises KeyError for MFE/Non-Standard):
        w_energy_delivery, w_containment
    """
    if not feature_name.startswith("w_"):
        raise ValueError(
            f"cost_model extractor only handles w_* features, got {feature_name!r}"
        )
    subsystem = feature_name[2:]

    if subsystem in EMITTED_2SLOT:
        # 2-slot IFE/MIF path — family-conditional
        weights = compute_twoslot_weights(concept_id)
        if weights is None:
            raise KeyError(
                f"cost_model: 2-slot {feature_name!r} unavailable for "
                f"{concept_id!r} (no model_output.txt, or family not IFE/MIF)"
            )
        return weights[subsystem], f"analyses/{concept_id}/model_output.txt", "medium"

    if subsystem not in EMITTED_SUBSYSTEMS:
        if subsystem in SUBSYSTEMS:
            raise ValueError(
                f"cost_model: subsystem {subsystem!r} (feature {feature_name!r}) "
                f"was retired by scoring-v3 P2 — only "
                f"{EMITTED_SUBSYSTEMS} are emitted for the legacy 3-slot path"
            )
        raise ValueError(
            f"cost_model: unknown subsystem {subsystem!r} (feature {feature_name!r})"
        )
    weights = compute_weights(concept_id)
    if weights is None:
        raise KeyError(
            f"cost_model: no model_output.txt for {concept_id!r} — "
            f"leave w_* features absent (no fallback)"
        )
    return weights[subsystem], f"analyses/{concept_id}/model_output.txt", "medium"
