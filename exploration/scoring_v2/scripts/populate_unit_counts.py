"""Populate `unit_count_estimate` (manual feature) for every concept.

The per-concept values come from `modularity_implementation_spec.md`
Change E (`.project/completed/20260821_scoring-v3-rewrite/specs/`). They are the
analyst's architectural-review counts of identical factory-built
precision units per plant (TF coil segments, DPSSL beamlines,
capacitor brick arrays, mirror cells, single bespoke drivers, etc.).

Idempotent: re-running over a tree that already has the same values
produces zero diff. To change a value, edit `_UNIT_COUNTS` below and
re-run; the change propagates to features/{cid}.yaml.

Usage:
    uv run python exploration/scoring_v2/scripts/populate_unit_counts.py
"""
from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from exploration.scoring_v2.lib import feature_io
from exploration.scoring_v2.lib.extractors import taxonomy as taxonomy_ext


# Source: modularity_implementation_spec.md Change E (2026-05-20).
# Imputed values (concepts not in v5 matrix by name) are commented inline.
_UNIT_COUNTS: dict[str, int] = {
    "01-hts-compact-tokamak":                            18,   # CFS TF coil segments
    "02-acoustic-icf-sonofusion":                       100,   # acoustic resonator array
    "03-laser-icf-liquid-jet-target":                   200,   # Cortex DPSSL beamlines
    "04-laser-icf":                                     500,   # hb11 DPSSL beamlines
    "05-planar-coil-stellarator":                        40,   # Thea planar coil segments
    "06-magnetic-mirror":                                30,   # Pale Blue mirror cells (p-B11)
    "07-maglif":                                        100,   # MagLIF Marx-generator bricks
    "08-frc-w-direct-conversion":                        75,   # Helion capacitor modules
    "09-qi-stellarator-hts":                             50,   # Proxima non-planar coil segments
    "10-large-scale-stellarator":                        40,   # Gauss HELIAS coils (W7-X-like)
    "11-magnetic-mirror":                                12,   # Realta D-T mirror cells
    "12-levitated-dipole":                                1,   # OpenStar single dipole coil
    "13-electrostatic-hybrid":                          200,   # Avalanche desktop Orbitron units
    "14-magnetized-target-fusion-pneumatic-compression": 60,   # General Fusion capacitor modules
    "15-sheared-flow-stabilized-z-pinch":                50,   # Zap capacitor modules
    "16-muon-catalyzed-fusion":                           1,   # Acceleron single muon accelerator
    "17a-laser-icf-hybrid-drive":                         4,   # Xcimer large e-beam KrF tanks
    "17b-laser-icf-fast-ignition":                      200,   # Focused Energy DPSSL beamlines
    "18-p-b11-frc":                                       8,   # TAE NBI modules
    "19-orbital-levitated-dipole":                        1,   # Zephyr single orbital dipole
    "20a-type-one-stellarator":                          40,   # Type One segmented HTS coils
    "20b-renaissance-stellarator":                       40,   # Renaissance segmented HTS
    "21-spherical-tokamak-hts":                          14,   # Tokamak Energy ST coil segments
    "22-projectile-icf":                                 50,   # First Light launcher modules
    "23-laser-icf-nanostructured-target":               500,   # Marvel DPSSL — imputed from concept 04 (hb11 p-B11 peer)
    "24-dense-plasma-focus":                              8,   # LPPFusion DPF electrode units
    "25-heavy-ion-beam-icf":                              1,   # Intensity single accelerator
    "26-laser-icf-indirect-drive":                     1000,   # Inertia DPSSL Thunderwall beamlines
    "27-polywell":                                        6,   # EMC2 Polywell grid units
    "28-hts-tokamak-full-hts":                           16,   # Energy Singularity integrated coils
    "29-negative-triangularity-tokamak":                 16,   # Firefly NTT coils (MANTA proxy)
    "30-laser-icf-nif-commercialization":              1000,   # Inertia NIF Commercialization beamlines
    "31-laser-icf-oec-architecture":                    200,   # Blue Laser OEC — imputed from concept 17b (Focused D-T DPSSL direct-drive peer)
    "32-laser-icf-french-national":                     200,   # GenF French — imputed from concept 17b (Focused D-T DPSSL direct-drive peer)
    "33-state-backed-tokamak-best":                       1,   # BEST single bespoke coil set
    "35-polomac-magnetic-confinement":                    4,   # Deutelio Polomac poloidal magnets
    "36-helical-coil-stellarator":                        1,   # Helical Fusion continuous winding
    "37-magnetized-target-inertial-fusion-mtif":        100,   # NearStar MTIF capacitor modules
    "38-particle-accelerator-driven-fusion":              1,   # SHINE single accelerator
    "39-spherical-tokamak-cs-free-p-b11":                14,   # ENN EHL-2 coil segments
}


def main() -> int:
    today = _dt.date.today().isoformat()
    ids = taxonomy_ext.all_concept_ids()
    written = 0
    missing = []
    for cid in ids:
        if cid not in _UNIT_COUNTS:
            missing.append(cid)
            continue
        doc = feature_io.read_features(cid)
        doc["_meta"] = {"concept_id": cid, "name": taxonomy_ext.concept_name(cid)}
        existing = doc.get("unit_count_estimate", {})
        # Preserve extracted_at if the value didn't change (idempotent).
        if isinstance(existing, dict) and existing.get("value") == _UNIT_COUNTS[cid]:
            continue
        doc["unit_count_estimate"] = {
            "value": _UNIT_COUNTS[cid],
            "provenance": "modularity_implementation_spec.md Change E",
            "confidence": "high",
            "extracted_at": today,
        }
        feature_io.write_features(cid, doc)
        written += 1
    print(f"populated unit_count_estimate for {written} concept(s); "
          f"{len(ids) - written - len(missing)} unchanged; "
          f"{len(missing)} missing from spec table: {missing}")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
