"""Cost-model extractor.

Parses exploration/concept_analysis/analyses/{concept_id}/model_output.txt and
emits the three `w_*` capex weight-share features (w_vessel, w_coils,
w_blanket) consumed by the modularity v5 `_percent_mod` embedding.

Behavior per design (.project/active/scoring-v2-component-modularity-slice/design.md):
- Sum `$` per subsystem bucket using the static CAS_TO_SUBSYSTEM dict below
  (mapping kept across all 7 subsystems so the dollars are correctly
  classified before normalization).
- Each `w_*` is the bucket's share of the 7-subsystem total covered $ (so
  the source shares sum to 1.0 across all 7; the v5 percent_mod embedding
  renormalizes the 3 retained shares to sum to 1.0 within itself).
- Codes seen in the file but absent from the dict are ignored (financial,
  indirect, O&M, fuel, IDC, contingency — see the design note).
- Codes in the dict not seen in the file contribute 0 to that bucket.
- If `model_output.txt` does not exist for the concept, the extractor
  returns no value (raises KeyError). No fallback.

P2 of the scoring-v3 rewrite trimmed the EMITTED_SUBSYSTEMS tuple from
seven to three. The internal SUBSYSTEMS tuple stays at seven so the
parser correctly aggregates dollars classified to the retired
bop/fuel_cycle/aux/civil subsystems before normalization. Only the
three retained subsystems are visible to the bulk extractor pipeline.

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

# Externally-exposed subsystem set: the modularity v5 percent_mod embedding
# only consumes these three. P2 of the scoring-v3 rewrite retired the
# other four (their shares dilute the modularity signal per v5).
EMITTED_SUBSYSTEMS = ("vessel", "coils", "blanket")

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
    r"^\s*(?P<code>(?:CAS\d{2,3}|C\d{6}))\s+.+?\s+(?P<dollars>-?\d+(?:\.\d+)?)\s*(?:\[[^\]]*\])?\s*$"
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
    rows = _parse_lines(p.read_text())
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

    Only the three EMITTED_SUBSYSTEMS (vessel, coils, blanket) are
    addressable through the dispatcher; the retired bop/fuel_cycle/aux/civil
    raise ValueError per fail-loud policy.
    """
    if not feature_name.startswith("w_"):
        raise ValueError(
            f"cost_model extractor only handles w_* features, got {feature_name!r}"
        )
    subsystem = feature_name[2:]
    if subsystem not in EMITTED_SUBSYSTEMS:
        if subsystem in SUBSYSTEMS:
            raise ValueError(
                f"cost_model: subsystem {subsystem!r} (feature {feature_name!r}) "
                f"was retired by scoring-v3 P2 — only "
                f"{EMITTED_SUBSYSTEMS} are emitted"
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
