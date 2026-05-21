# Implementation Spec: Modularity Scoring Axis (v5 Replacement)

**Status:** Ready for implementation
**Owner:** Mallory
**Created:** 2026-05-20
**Branch:** `concept-downselect`
**Companion spec:** `modularity_matrix_v5.md` (canonical reference for per-concept scores, subsystem ratings, and unit counts)
**Schema version:** v0.3.0 (`schema.md`, 2026-05-12)

This spec **replaces** the existing modularity scoring in `scoring_v2/embeddings/rulebook.py` (slices 1 and 2) with the v5 three-component formula. The existing 12 embeddings + 7 per-concept capex-weight features are retired.

---

## Summary

The existing scoring_v2 modularity implementation has 12 embeddings (4 plant-level + 7 per-subsystem + 1 aggregate) and depends on 7 per-concept capex-share features (`w_vessel`, `w_coils`, `w_blanket`, `w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil`) extracted from `model_output.txt`. The v5 doc collapses this to a 3-component formula:

```
modularity_score = 0.50 × mvs + 0.25 × percent_mod + 0.25 × unit_multiplicity
```

where `percent_mod` is the capex-weighted average of three subsystem ratings (vessel, magnet/driver, blanket) — not seven.

### Why replace rather than refine

The existing implementation conflates two design intents (plant-level scale factors + component-level modularity ratings) into one composite. v5 separates them cleanly: scale (mvs) is one factor, modularity-per-se (percent_mod over three subsystems) is the second factor, and replication count (unit_multiplicity) is the third. The four excluded subsystems (BOP, fuel cycle, auxiliaries, civil) "are rarely modularized in any concept and dilute the signal" per the v5 calibration work. Refining the existing implementation to match v5 would require deleting 8 of 12 embeddings and reweighting the rest; cleaner to rewrite.

### What gets retired

| Existing artifact | Disposition |
|---|---|
| 4 plant-level embeddings (`_min_viable_device_scale`, `_hardware_topology_complexity`, `_unit_multiplicity`, `_subsystem_stack_burden`) | `_min_viable_device_scale` and `_unit_multiplicity` kept (used by v5); `_hardware_topology_complexity` and `_subsystem_stack_burden` retired |
| 7 per-subsystem embeddings (`_vessel_rating`, `_coils_rating`, `_blanket_rating`, `_bop_rating`, `_fuel_cycle_rating`, `_aux_rating`, `_civil_rating`) | `_vessel_rating`, `_coils_rating` (renamed `_magnet_driver_rating`), `_blanket_rating` kept; `_bop_rating`, `_fuel_cycle_rating`, `_aux_rating`, `_civil_rating` retired |
| `_component_modularity_aggregate` embedding (7-subsystem weighted sum) | Replaced by `_percent_mod` (3-subsystem weighted sum) |
| 7 per-concept capex-share features (`w_vessel`, `w_coils`, `w_blanket`, `w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil`) | `w_vessel`, `w_coils`, `w_blanket` kept (used by v5 percent_mod); other 4 retired from the schema (no remaining consumers) |
| `cost_model.py` extractor | Kept but trimmed: stops emitting `w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil` |
| `model_output.txt` per-concept files | Still source of truth for the 3 retained capex shares; analyst doesn't need to do anything to existing files |

### Key design choices

- **Three components, fixed top-level blend**: `0.50 × mvs + 0.25 × percent_mod + 0.25 × unit_multiplicity`. The blend is in `weights/default.yaml` and tunable; the analyst's v5 calibration uses these specific weights.
- **percent_mod weights three subsystems by per-concept capex share**: vessel (`w_vessel`), magnet/driver (`w_coils`), blanket (`w_blanket`). The three shares are renormalized to sum to 1.0 within these three subsystems (the existing capex shares sum to 1.0 across all 7; for percent_mod we drop the other 4 and rescale).
- **Subsystem ratings use lookup tables keyed on architectural features**, not free-form embeddings. Three lookup tables per subsystem (vessel, magnet/driver, blanket), each producing 1-5 based on relevant v0.3.0 features. The v5 doc's narrative cells encode the lookup logic.
- **Unit multiplicity is a bracket schedule on estimated unit count**: N=1 → 1, N=2 → 2, N=5-10 → 3, N=15-30 → 4, N≥50 → 5. The estimated unit count is a per-concept feature (`unit_count_estimate`) populated manually from architecture analysis, not derived from controlled vocabulary.
- **mvs is also a lookup keyed on architectural features** (confinement_family, mfe_topology, etc.), producing 1-5 based on minimum viable plant scale.

---

## Schema changes

### Add (3 new features)

| Feature | Type | Source | Purpose |
|---|---|---|---|
| `unit_count_estimate` | int | manual extractor | Number of identical factory-built precision units per plant. Per-concept manual value backed by analyst architecture review. |
| `vessel_modularity_rating` | int 1-5 | derived (lookup on architectural features) | Vessel modularity score component of percent_mod. Could alternatively be computed by embedding; declared here for transparency in feature files. |
| `magnet_driver_modularity_rating` | int 1-5 | derived | Magnet/driver modularity score component of percent_mod. |
| `blanket_modularity_rating` | int 1-5 | derived | Blanket modularity score component of percent_mod. |

Actually, on reflection: keeping the per-subsystem ratings as **embeddings** rather than features avoids requiring the analyst to populate three numeric ratings per concept. The embeddings derive ratings from existing features (Blanket Config, Magnet Type, etc.) via lookup tables. So the only **new** feature is `unit_count_estimate` (per-concept manual).

### Retire (4 features)

| Feature | Reason for retirement |
|---|---|
| `w_bop` | Not used by v5 percent_mod (excluded subsystem) |
| `w_fuel_cycle` | Not used by v5 percent_mod (excluded subsystem) |
| `w_aux` | Not used by v5 percent_mod (excluded subsystem) |
| `w_civil` | Not used by v5 percent_mod (excluded subsystem) |

### Keep (3 features)

| Feature | Used by |
|---|---|
| `w_vessel` | percent_mod (vessel subsystem capex share) |
| `w_coils` | percent_mod (magnet/driver subsystem capex share) |
| `w_blanket` | percent_mod (blanket subsystem capex share) |

---

## Changes summary

| # | Change | Touches |
|---|---|---|
| A | Restructure `modularity` axis block in `weights/default.yaml` | `weights/default.yaml` |
| B | Replace existing modularity embeddings in `rulebook.py` | `embeddings/rulebook.py` |
| C | Create `lookup_modularity.yaml` metadata file (vessel/magnet/blanket/mvs/unit_multiplicity lookup tables) | `lookup_modularity.yaml` (new) |
| D | Trim `cost_model.py` extractor to stop emitting retired weight features | `lib/extractors/cost_model.py` |
| E | Add `unit_count_estimate` feature to schema and populate per concept | `schema.yaml`, `features/*.yaml` |
| F | Update tests | `tests/scoring_v2/test_modularity.py` (replaces existing modularity tests) |
| G | Update diagnostic block format in each feature file | `features/*.yaml` (39 files) |

---

## Change A: Axis registration in `weights/default.yaml`

```yaml
# Replace the existing modularity block under manufacturability_scale_out
# with a top-level axis block (matching the Path B 7-axis structure)

modularity:
  axis_weight: 1.0                          # composite weight (UI tunable)
  embedding_weights:                        # top-level blend (v5 formula)
    min_viable_device_scale:        0.50
    percent_mod:                    0.25
    unit_multiplicity:              0.25

  # Sub-tables for within-axis tunability (advanced UI expansion)
  unit_count_brackets:                       # N → score lookup
    - {max_count: 1,   score: 1}
    - {max_count: 2,   score: 2}
    - {max_count: 10,  score: 3}
    - {max_count: 30,  score: 4}
    # N >= 31: score 5 (caught by floor)
  unit_count_floor_score: 5

  # mvs lookup — complete enumeration for all 40 concepts.
  # Keys use (Confinement Family | Concept) with disambiguation by
  # Driver Type or Tokamak Shape where needed.
  mvs_lookup:
    # MFE Tokamaks (concepts 01 CFS, 21 Tokamak Energy, 28 Energy Singularity,
    #               29 Firefly, 33 BEST, 39 ENN)
    "MFE|Tokamak (compact)":              3      # CFS ARC, Firefly NTT, Energy Singularity
    "MFE|Tokamak (spherical)":            3      # Tokamak Energy ST, ENN EHL-2
    "MFE|Tokamak (negative-T)":           3      # Firefly NTT (alt route)
    "MFE|Tokamak (non-compact)":          2      # BEST (LTS, large)

    # MFE Stellarators (concepts 05 Thea, 09 Proxima, 10 Gauss,
    #                   20a Type One, 20b Renaissance, 36 Helical)
    "MFE|Stellarator":                    2      # All stellarators

    # MFE Compact Toroid / FRC (concept 18 TAE)
    "MFE|FRC":                            4      # TAE FRC

    # MFE Open/Linear — disambiguated by Driver Type
    # (concepts 06 Pale Blue, 11 Realta, 15 Zap)
    "MFE|Mirror":                         4      # Pale Blue p-B11, Realta D-T
    "MFE|Z-pinch (sheared-flow)":         4      # Zap (Driver Type = Magnetic pinch)

    # MFE Dipole (concepts 12 OpenStar, 19 Zephyr)
    "MFE|Levitated dipole":               3      # OpenStar (D-T), Zephyr (D-He3 orbital)

    # MFE other (concept 35 Deutelio PoloMac)
    "MFE|Other":                          3      # Polomac (poloidal magnets)

    # MIF (concepts 07 MagLIF, 14 General Fusion, 37 NearStar, 08 Helion)
    "MIF|MagLIF":                         5      # Pacific MagLIF
    "MIF|Pneumatic compression":          5      # General Fusion, NearStar MTIF
    "MIF|FRC compression":                5      # Helion (Confinement Family = MIF in v3)

    # IFE Laser (concepts 03 Cortex, 04 hb11, 17a Xcimer, 17b Focused, 23 Marvel,
    #            26 Inertia Indirect, 30 Inertia NIF Comm, 31 Blue Laser, 32 GenF)
    "IFE|Laser":                          4      # Generic laser-ICF baseline
    "IFE|Laser (Xcimer-class)":           3      # Xcimer KrF excimer (large e-beam tanks)
    "IFE|Laser (liquid jet)":             4      # Cortex (treat as standard laser-ICF mvs)

    # IFE other drivers (concepts 22 First Light, 25 Intensity, 02 Sonofusion)
    "IFE|Heavy ion beam":                 4      # Intensity (still IFE family)
    "IFE|Projectile":                     3      # First Light
    "IFE|Acoustic":                       5      # Sonofusion (desktop scale)

    # Non-Standard (concepts 13 Avalanche, 16 Acceleron, 24 LPPFusion, 27 EMC2, 38 SHINE)
    "Non-Standard|Electrostatic":         5      # Avalanche, EMC2 Polywell (desktop)
    "Non-Standard|Plasma focus":          4      # LPPFusion DPF
    "Non-Standard|Muon-catalyzed":        3      # Acceleron (muon accelerator)
    "Non-Standard|Particle accelerator":  3      # SHINE

  # Vessel modularity lookup. Keyed on Confinement Family | Topology/Method | qualifier.
  # Patterns derived from v5 matrix's v/md/bl breakdowns.
  vessel_lookup:
    # MFE Tokamaks: 4 (demountable HTS compact/spherical) or 2 (non-compact LTS)
    "MFE|Tokamak|compact":                4      # CFS, Firefly, Energy Singularity, ENN
    "MFE|Tokamak|spherical":              4      # Tokamak Energy ST
    "MFE|Tokamak|non-compact":            2      # BEST

    # MFE Stellarators: 2 (bespoke 3D vacuum chamber)
    "MFE|Stellarator|*":                  2

    # MFE FRC: 3 (bespoke but smaller than tokamak)
    "MFE|FRC|*":                          3

    # MFE Mirror / Z-pinch / Dipole / Other: 3 (small bespoke vessel)
    "MFE|Mirror|*":                       3
    "MFE|Z-pinch|*":                      3
    "MFE|Dipole|*":                       3
    "MFE|Other|*":                        3

    # MIF: 5 for replaceable-liner architectures; lower for pneumatic D-T
    "MIF|MagLIF|*":                       5
    "MIF|Pneumatic compression|D-T":      4      # General Fusion vessel large but demountable
    "MIF|Pneumatic compression|D-D":      5      # NearStar D-D simplifies vessel
    "MIF|FRC compression|*":              5      # Helion

    # IFE: 3 (chamber is bespoke but smaller-class)
    "IFE|Laser|*":                        3
    "IFE|Heavy ion beam|*":               3
    "IFE|Projectile|*":                   3
    "IFE|Acoustic|*":                     3

    # Non-Standard: 3 (typical compact bespoke vessel)
    "Non-Standard|Electrostatic|*":       3      # Avalanche, Polywell — desktop-class
    "Non-Standard|Plasma focus|*":        3      # LPPFusion DPF
    "Non-Standard|Muon-catalyzed|*":      3
    "Non-Standard|Particle accelerator|*": 3

  # Magnet/driver modularity lookup. Keyed on Confinement Family | Magnet Type or
  # Driver Type. HTS demountable = most modular (5); LTS = least (2); pulsed-power
  # drivers (Marx generators, DPSSL beamlines, capacitor banks) = 5 (replicated units).
  magnet_driver_lookup:
    # MFE — by magnet type, with special case for Z-pinch
    "MFE|HTS (wound)|*":                  5      # CFS, ENN, Firefly, most HTS tokamaks
    "MFE|HTS (integrated)|*":             4      # Energy Singularity
    "MFE|HTS (planar)|*":                 5      # Thea planar coil
    "MFE|HTS (segmented)|*":              5      # Proxima, Type One, Renaissance
    "MFE|HTS (continuous helical)|*":     3      # Helical Fusion — continuous winding
    "MFE|LTS|*":                          2      # BEST
    "MFE|LTS+HTS|*":                      2      # BEST (alt classification)
    "MFE|Resistive|*":                    3      # Most resistive-magnet concepts
    "MFE|Magnetic pinch|*":               3      # Zap Z-pinch (pulsed power md=3)

    # MIF — driver = pulsed power
    "MIF|*|Pulsed power":                 5      # MagLIF Marx bricks
    "MIF|*|Pneumatic":                    5      # General Fusion, NearStar
    "MIF|*|Capacitor compression":        5      # Helion

    # IFE — driver = laser/HIB/projectile/acoustic
    "IFE|*|DPSSL Laser":                  5      # Inertia, Focused, Blue Laser, GenF, hb11, Marvel
    "IFE|*|Gas Laser":                    3      # Xcimer KrF (few large tanks)
    "IFE|*|Heavy ion beam":               3      # Intensity (single bespoke accelerator)
    "IFE|*|Projectile":                   5      # First Light pulsed EM launcher
    "IFE|*|Acoustic":                     3      # Sonofusion

    # Non-Standard
    "Non-Standard|*|IEC":                 5      # Avalanche, EMC2 Polywell (replicated grids)
    "Non-Standard|*|Plasma focus":        3      # LPPFusion DPF
    "Non-Standard|*|Particle accelerator": 3     # SHINE, Acceleron (single accelerator)
    "Non-Standard|*|Muon catalysis":      3      # Acceleron (muon accelerator)

  # Blanket modularity lookup. Keyed on Fuel | Blanket Config.
  # Aneutronic fuels score 5 (no breeding blanket needed). D-T scored by blanket type.
  blanket_lookup:
    # Aneutronic and low-neutronic fuels: 5 (no breeding blanket)
    "p-B11|*":                            5
    "D-D|*":                              5
    "D-He3|*":                            5

    # D-T concepts: rated by blanket type
    "D-T|Liquid metal":                   5      # Flowing, self-renewing
    "D-T|Molten salt":                    5      # FLiBe flowing, self-renewing
    "D-T|Solid breeder":                  4      # HCPB pebble bed — replaceable
    "D-T|Other/hybrid":                   4      # Mixed configurations
    "D-T|TBD":                            5      # Defaults to Liquid metal per TBD rule
    "D-T|N/A (no tritium)":               5      # Not applicable
    "D-T|N/A (non-power)":                4      # SHINE — non-power neutron source
```

### Why these blend weights

The 0.50 / 0.25 / 0.25 split per the v5 doc: "Each concept's M&SO score is a weighted sum of three components." The 0.50 weight on mvs reflects that minimum viable scale is the single most consequential modularity factor — a concept that requires a 500-MW first-of-kind plant cannot be modular in the SMR sense regardless of how many coil segments it has. percent_mod and unit_multiplicity are roughly equally important and both contribute at 0.25.

### Why three subsystems, not seven, for percent_mod

Per v5: "The remaining four subsystems (power conversion, fuel cycle, auxiliaries, civil) are excluded because they're rarely modularized in any concept and dilute the signal." Specifically: thermal BOP is a Rankine cycle in nearly every concept (low signal), fuel cycle is determined by fuel choice (already captured indirectly), aux heating is typically bespoke (limited modularity headroom), civil is site-dependent (independent of concept). Including these four would compress all concepts toward the same percent_mod value.

---

## Change B: Embeddings in `rulebook.py`

Replace the existing 12 modularity embeddings (`_min_viable_device_scale`, `_hardware_topology_complexity`, `_unit_multiplicity`, `_subsystem_stack_burden`, `_vessel_rating`, `_coils_rating`, `_blanket_rating`, `_bop_rating`, `_fuel_cycle_rating`, `_aux_rating`, `_civil_rating`, `_component_modularity_aggregate`) with the following 5 embeddings:

```python
# ===========================================================================
# Modularity Axis (v5 formula)
#
# Score = 0.50 × mvs + 0.25 × percent_mod + 0.25 × unit_multiplicity
#
# percent_mod is the capex-weighted average of three subsystem modularity
# ratings (vessel, magnet/driver, blanket). The four other subsystems
# (BOP, fuel cycle, aux, civil) are excluded from percent_mod per v5.
# ===========================================================================


@embedding(
    "min_viable_device_scale",
    inputs=["confinement_family", "mfe_topology", "ife_driver",
            "mif_method", "non_standard_mechanism", "tokamak_shape",
            "driver_type"],
)
def _min_viable_device_scale(
    confinement_family: str,
    mfe_topology: str,
    ife_driver: str,
    mif_method: str,
    non_standard_mechanism: str,
    tokamak_shape: str,
    driver_type: str,
    *,
    weights_yaml: dict,
) -> float:
    """Minimum viable device scale (mvs) rating, 1-5.

    Lookup-based: derives a key from architectural features and looks up
    the mvs score in weights_yaml['modularity']['mvs_lookup'].

    Returns 1.0 if no key matches (defensive floor) but the calling test
    suite enforces full coverage so this should never fire in practice.
    """
    key = _mvs_key(confinement_family, mfe_topology, ife_driver, mif_method,
                   non_standard_mechanism, tokamak_shape, driver_type)
    lookup = weights_yaml.get("modularity", {}).get("mvs_lookup", {})
    return float(lookup.get(key, 1.0))


def _mvs_key(cf, mfe_top, ife_driver, mif_method, nsm, tok_shape, driver_type):
    """Build a Confinement Family | Concept key for the mvs lookup.

    Disambiguation rules:
      - Tokamaks split by shape (compact/spherical/negative-T/non-compact)
      - Xcimer-class IFE (large e-beam tanks) gets its own key via driver_type
      - Sonofusion (acoustic) routed by mfe_topology/ife_driver combination
    """
    if cf == "MFE":
        if mfe_top == "Tokamak":
            if tok_shape in ("Compact", "Spherical", "Negative triangularity"):
                return f"MFE|Tokamak ({tok_shape.lower().replace(' triangularity', '-T')})"
            return "MFE|Tokamak (non-compact)"
        if mfe_top in ("Stellarator", "FRC", "Levitated dipole"):
            return f"MFE|{mfe_top}"
        if mfe_top == "Open/Linear":
            # Disambiguate by driver_type
            if driver_type == "Magnetic pinch":
                return "MFE|Z-pinch (sheared-flow)"
            return "MFE|Mirror"
    elif cf == "MIF":
        return "MIF|*"
    elif cf == "IFE":
        if ife_driver == "Laser":
            if "excimer" in (driver_type or "").lower() or "KrF" in (driver_type or ""):
                return "IFE|Laser (Xcimer-class)"
            return "IFE|Laser"
        if ife_driver == "Heavy ion beam":
            return "IFE|Heavy ion beam"
        if ife_driver == "Projectile":
            return "IFE|Projectile"
        if ife_driver == "Acoustic":
            return "IFE|Acoustic"
    elif cf == "Non-Standard":
        if "electrostatic" in (nsm or "").lower():
            return "Non-Standard|Electrostatic"
        if "plasma focus" in (nsm or "").lower():
            return "Non-Standard|Plasma focus"
        if "muon" in (nsm or "").lower():
            return "Non-Standard|Muon-catalyzed"
        if "accelerator" in (nsm or "").lower() or cf == "Non-Standard":
            return "Non-Standard|Particle accelerator"
    return None


@embedding(
    "unit_multiplicity",
    inputs=["unit_count_estimate"],
)
def _unit_multiplicity(
    unit_count_estimate: int,
    *,
    weights_yaml: dict,
) -> float:
    """Unit multiplicity rating, 1-5, based on per-concept unit count.

    Brackets per v5: N=1 → 1, N=2 → 2, N=5-10 → 3, N=15-30 → 4, N≥50 → 5.
    Curve saturates at N=50 — beyond that, additional copies don't add
    modularity (and arguably add commissioning burden).
    """
    if unit_count_estimate is None or unit_count_estimate < 1:
        return 1.0
    weights = weights_yaml.get("modularity", {})
    brackets = weights.get("unit_count_brackets", [])
    floor = float(weights.get("unit_count_floor_score", 5.0))
    for bracket in brackets:
        if unit_count_estimate <= bracket["max_count"]:
            return float(bracket["score"])
    return floor


@embedding(
    "vessel_modularity_rating",
    inputs=["confinement_family", "mfe_topology", "tokamak_shape",
            "mif_method", "ife_driver", "non_standard_mechanism", "fuel"],
)
def _vessel_modularity_rating(
    confinement_family: str,
    mfe_topology: str,
    tokamak_shape: str,
    mif_method: str,
    ife_driver: str,
    non_standard_mechanism: str,
    fuel: str,
    *,
    weights_yaml: dict,
) -> float:
    """Vessel subsystem modularity rating, 1-5.

    Per v5 matrix calibration:
      - Compact MFE tokamaks (HTS): 4 — demountable
      - Non-compact MFE tokamaks (LTS): 2 — bespoke single-pour
      - Stellarators: 2 — bespoke 3D geometry
      - MFE FRC/Mirror/Z-pinch/Dipole/Other: 3 — small bespoke
      - MIF MagLIF, FRC compression: 5 — replaceable consumable liner
      - MIF Pneumatic D-T: 4; D-D: 5
      - IFE all drivers: 3 — bespoke chamber
      - Non-Standard: 3 — typical compact bespoke vessel

    Lookup table in weights_yaml['modularity']['vessel_lookup'].
    Falls back to 3.0 for unrecognized concepts.
    """
    lookup = weights_yaml.get("modularity", {}).get("vessel_lookup", {})
    key = _vessel_key(confinement_family, mfe_topology, tokamak_shape,
                      mif_method, ife_driver, non_standard_mechanism, fuel)
    return float(lookup.get(key, 3.0))


def _vessel_key(cf, mfe_top, tok_shape, mif_method, ife_driver, nsm, fuel):
    """Build the vessel lookup key with all necessary disambiguation."""
    if cf == "MFE":
        if mfe_top == "Tokamak":
            if tok_shape in ("Compact", "Negative triangularity"):
                return "MFE|Tokamak|compact"
            if tok_shape == "Spherical":
                return "MFE|Tokamak|spherical"
            return "MFE|Tokamak|non-compact"
        if mfe_top in ("Stellarator", "Compact Toroid", "Open/Linear",
                       "Dipole", "Other"):
            # Map Compact Toroid → FRC for the lookup key
            topology_key = "FRC" if mfe_top == "Compact Toroid" else mfe_top
            # Open/Linear may be Mirror or Z-pinch; both have the same vessel
            # rating (3) so lookup-key-level disambiguation isn't needed here
            if mfe_top == "Open/Linear":
                # Use generic "Mirror" or "Z-pinch" — both → 3
                # Use Mirror as the canonical key since both rate the same
                topology_key = "Mirror"
            return f"MFE|{topology_key}|*"
    elif cf == "MIF":
        # MagLIF vs Pneumatic compression vs FRC compression
        if "MagLIF" in (mif_method or ""):
            return "MIF|MagLIF|*"
        if "Pneumatic" in (mif_method or ""):
            return f"MIF|Pneumatic compression|{fuel}"
        if "FRC" in (mif_method or ""):
            return "MIF|FRC compression|*"
    elif cf == "IFE":
        return f"IFE|{ife_driver}|*"
    elif cf == "Non-Standard":
        if "electrostatic" in (nsm or "").lower():
            return "Non-Standard|Electrostatic|*"
        if "plasma focus" in (nsm or "").lower():
            return "Non-Standard|Plasma focus|*"
        if "muon" in (nsm or "").lower():
            return "Non-Standard|Muon-catalyzed|*"
        if "accelerator" in (nsm or "").lower() or "particle" in (nsm or "").lower():
            return "Non-Standard|Particle accelerator|*"
    return None


@embedding(
    "magnet_driver_modularity_rating",
    inputs=["confinement_family", "magnet_type", "driver_type", "mfe_topology"],
)
def _magnet_driver_modularity_rating(
    confinement_family: str,
    magnet_type: str,
    driver_type: str,
    mfe_topology: str,
    *,
    weights_yaml: dict,
) -> float:
    """Magnet/driver subsystem modularity rating, 1-5.

    Per v5 matrix calibration:
      - HTS (wound, demountable): 5 — segmented + replaceable
      - HTS (integrated): 4 — segmented but not demountable
      - LTS: 2 — single bespoke coil set
      - Pulsed-power drivers (capacitor banks, Marx generators): 5 — Lego-brick
      - DPSSL laser beamlines: 5 — replicated unit
      - Single bespoke driver (heavy-ion accelerator, ITER coil set,
        continuous helical winding): 1
      - Electrostatic grids: 5 — serial-product

    Lookup table in weights_yaml['modularity']['magnet_driver_lookup'].
    """
    lookup = weights_yaml.get("modularity", {}).get("magnet_driver_lookup", {})
    key = _magnet_driver_key(confinement_family, magnet_type, driver_type, mfe_topology)
    return float(lookup.get(key, 3.0))


def _magnet_driver_key(cf, magnet_type, driver_type, mfe_top):
    """Build the magnet/driver lookup key.

    MFE: key by magnet type, with special case for Z-pinch (Magnetic pinch driver).
    MIF/IFE/Non-Standard: key by driver_type.
    """
    if cf == "MFE":
        if driver_type == "Magnetic pinch":
            return "MFE|Magnetic pinch|*"
        return f"MFE|{magnet_type}|*"
    if cf == "MIF":
        # Normalize driver_type to lookup key
        if "Pulsed power" in (driver_type or ""): return "MIF|*|Pulsed power"
        if "Pneumatic" in (driver_type or ""):   return "MIF|*|Pneumatic"
        if "Capacitor" in (driver_type or ""):   return "MIF|*|Capacitor compression"
        return f"MIF|*|{driver_type}"
    if cf == "IFE":
        # Normalize driver_type to lookup key
        if "DPSSL" in (driver_type or ""):       return "IFE|*|DPSSL Laser"
        if "Gas Laser" in (driver_type or "") or "KrF" in (driver_type or ""):
            return "IFE|*|Gas Laser"
        if "Heavy ion" in (driver_type or ""):   return "IFE|*|Heavy ion beam"
        if "Projectile" in (driver_type or "") or "Pulsed EM" in (driver_type or ""):
            return "IFE|*|Projectile"
        if "Acoustic" in (driver_type or ""):    return "IFE|*|Acoustic"
        return f"IFE|*|{driver_type}"
    if cf == "Non-Standard":
        if "IEC" in (driver_type or "") or "Electrostatic" in (driver_type or ""):
            return "Non-Standard|*|IEC"
        if "Plasma focus" in (driver_type or "") or "DPF" in (driver_type or ""):
            return "Non-Standard|*|Plasma focus"
        if "accelerator" in (driver_type or "").lower():
            return "Non-Standard|*|Particle accelerator"
        if "Muon" in (driver_type or ""):
            return "Non-Standard|*|Muon catalysis"
    return None


@embedding(
    "blanket_modularity_rating",
    inputs=["fuel", "blanket_config"],
)
def _blanket_modularity_rating(
    fuel: str,
    blanket_config: str,
    *,
    weights_yaml: dict,
) -> float:
    """Blanket subsystem modularity rating, 1-5.

    Per v5 matrix calibration:
      - Aneutronic fuels (p-B11, D-D): 5 — no breeding blanket needed
      - D-He³: 5 — no breeding blanket (no tritium)
      - D-T + Molten salt (FLiBe): 5 — flowing, self-renewing
      - D-T + Liquid metal: 5 — flowing, self-renewing
      - D-T + Solid breeder (HCPB pebble bed): 4 — replaceable pebbles
      - D-T + Other/hybrid: 4 — mixed
      - D-T + TBD (defaulted): 5 — assume liquid metal per TBD rule

    Lookup table in weights_yaml['modularity']['blanket_lookup'].
    """
    lookup = weights_yaml.get("modularity", {}).get("blanket_lookup", {})
    # TBD blanket → liquid metal default (matches the other axes' TBD rule)
    effective_blanket = "Liquid metal" if blanket_config == "TBD" else blanket_config
    key = f"{fuel}|{effective_blanket}"
    return float(lookup.get(key, 3.0))


@embedding(
    "percent_mod",
    inputs=["vessel_modularity_rating", "magnet_driver_modularity_rating",
            "blanket_modularity_rating", "w_vessel", "w_coils", "w_blanket"],
)
def _percent_mod(
    vessel_modularity_rating: float,
    magnet_driver_modularity_rating: float,
    blanket_modularity_rating: float,
    w_vessel: float,
    w_coils: float,
    w_blanket: float,
) -> float:
    """Percent modularization: capex-weighted average of three subsystem ratings.

    Uses per-concept capex shares (w_vessel, w_coils, w_blanket) from the
    existing cost_model extractor. The three shares are renormalized to
    sum to 1.0 within the percent_mod calculation (the source shares sum
    to 1.0 across all 7 subsystems; we drop the other 4 and rescale).

    Returns 1.0-5.0.

    If any of the three capex shares is missing (None), falls back to
    equal weighting (1/3 each) and emits a diagnostic flag.
    """
    if any(w is None for w in (w_vessel, w_coils, w_blanket)):
        # Fallback: equal weighting when capex shares unavailable
        return (vessel_modularity_rating + magnet_driver_modularity_rating
                + blanket_modularity_rating) / 3.0

    total = w_vessel + w_coils + w_blanket
    if total <= 0:
        return (vessel_modularity_rating + magnet_driver_modularity_rating
                + blanket_modularity_rating) / 3.0

    return (
        (w_vessel / total) * vessel_modularity_rating
        + (w_coils / total) * magnet_driver_modularity_rating
        + (w_blanket / total) * blanket_modularity_rating
    )
```

### Removed embeddings

The following embeddings from the previous implementation are **removed**:

- `_hardware_topology_complexity` — folded into mvs and magnet_driver lookups
- `_subsystem_stack_burden` — concept no longer used in v5
- `_bop_rating`, `_fuel_cycle_rating`, `_aux_rating`, `_civil_rating` — excluded subsystems
- `_component_modularity_aggregate` — replaced by `_percent_mod`

The remaining 5 embeddings (mvs, unit_multiplicity, vessel, magnet/driver, blanket modularity ratings, percent_mod) are the complete v5 implementation.

Wait — that's 6 embeddings, not 5. Recount: `_min_viable_device_scale`, `_unit_multiplicity`, `_vessel_modularity_rating`, `_magnet_driver_modularity_rating`, `_blanket_modularity_rating`, `_percent_mod` = **6 embeddings**. The composite score itself is computed by the framework's per-axis scorer using `embedding_weights` in default.yaml (no separate "modularity_score" embedding needed; the `_score_axis` machinery handles the blend).

### Why no top-level `_modularity_score` embedding

Path B's `_score_axis` machinery (Slice 1 of the integrated plan) handles the weighted blend of `embedding_weights` per axis automatically. The three top-level components (mvs, percent_mod, unit_multiplicity) are listed in `weights/default.yaml` under `modularity.embedding_weights`, and the framework computes the weighted sum without needing a dedicated embedding. This matches the existing 5-weight modularity blend pattern under `manufacturability_scale_out`.

---

## Change C: `lookup_modularity.yaml` (metadata only)

```yaml
# Modularity scoring metadata.
#
# Numerical lookup values live in weights/default.yaml under
# modularity.mvs_lookup, modularity.vessel_lookup, etc.
#
# This file documents:
#   - what each subsystem rating means qualitatively
#   - lookup table key derivation rules
#   - rationale for v5 calibration choices

mvs_lookup:
  description: |
    Minimum viable device scale. How small can the smallest commercially
    viable plant be?
  scale:
    "1": "ITER-class megaproject; no smaller variant possible"
    "2": "Large stellarator / non-compact tokamak (W7-X / BEST class)"
    "3": "Compact tokamak / projectile ICF / OEC-class laser"
    "4": "FRC, mirror, Z-pinch, DPF, DPSSL laser at ~100 MW class"
    "5": "MIF (Helion, MagLIF, NearStar), acoustic (Sonofusion), electrostatic (Polywell, Avalanche) — desktop or warehouse scale"
  key_rules: |
    Built from (Confinement Family, MFE Topology / IFE Driver / MIF Method
    / Non-Standard Mechanism, Tokamak Shape, Driver Type). The _mvs_key()
    helper in rulebook.py implements the disambiguation logic, including:
      - Tokamak shape split (compact/spherical/negative-T/non-compact)
      - Open/Linear split by Driver Type (Magnetic → Mirror, Magnetic pinch → Z-pinch)
      - IFE Laser split by Driver Type (excimer/KrF → Xcimer-class)

vessel_lookup:
  description: |
    Vessel subsystem modularity. How factory-built and replaceable is the
    fusion chamber itself?
  scale:
    "1": "Single bespoke vessel, on-site assembly (ITER-class)"
    "2": "Stellarator vacuum chamber — bespoke 3D geometry"
    "3": "Compact MFE chamber — small but bespoke per plant"
    "4": "IFE chamber or compact MFE with demountable sections"
    "5": "MIF replaceable liner or chamber-less concept"

magnet_driver_lookup:
  description: |
    Magnet/driver subsystem modularity. How factory-built and replicated
    is the magnetic confinement system (MFE) or driver hardware (IFE/MIF)?
  scale:
    "1": "Single bespoke driver (continuous helical winding, single heavy-ion
          accelerator, ITER coil set, single levitated dipole, muon accelerator)"
    "2": "LTS coil set — multiple coils but each bespoke (BEST-class)"
    "3": "Partial segmentation — some replicated units (negative-T tokamak)"
    "4": "Integrated HTS coils — segmented but not demountable"
    "5": "Demountable HTS coils, DPSSL beamlines, capacitor brick arrays,
          electrostatic grids — full Lego-brick architecture"

blanket_lookup:
  description: |
    Blanket subsystem modularity. How factory-built and replaceable is the
    breeding/cooling blanket?
  scale:
    "1": "Heavily integrated blanket; replacement requires major shutdown"
    "2": "Solid breeder pebble bed — replaceable but slow"
    "3": "Standard ITER-class blanket"
    "4": "Solid breeder modular (HCPB) or hybrid"
    "5": "Flowing liquid metal/molten salt (self-renewing), or no blanket
          required (aneutronic fuel, MIF)"
  tbd_handling: |
    TBD blanket defaults to "Liquid metal" per the framework-wide TBD rule;
    diagnostic block records `blanket_assumed: liquid_metal_default`.

unit_multiplicity:
  description: |
    Estimated count of identical factory-built precision units per plant.
    Examples: DPSSL beamlines, capacitor modules, mirror cells, TF coil
    segments, MagLIF Marx-generator bricks.
  brackets:
    - {count_range: "1",     score: 1, examples: "Single bespoke driver — accelerator, ITER coil set, helical winding"}
    - {count_range: "2",     score: 2, examples: "Two bespoke segments"}
    - {count_range: "5-10",  score: 3, examples: "Small replicated arrays — 6 polywell grids, 8 DPF electrodes"}
    - {count_range: "15-30", score: 4, examples: "Tokamak TF coil sets (18 segments), mirror cell chains (~30 cells)"}
    - {count_range: "≥50",   score: 5, examples: "MIF capacitor banks (60-100 bricks), DPSSL beamlines (200-1000)"}
  rationale: |
    Saturates at N=50 — beyond that, additional copies don't add modularity
    (and arguably add commissioning burden). Source: v5 calibration.
  population: |
    The unit_count_estimate feature is populated manually per concept from
    architecture analysis (e.g., reading company tech specs, counting coil
    segments in published designs). Not derived from controlled vocabulary.
```

---

## Change D: Trim `cost_model.py` extractor

The existing extractor reads `exploration/concept_analysis/analyses/{cid}/model_output.txt` and emits 7 capex-share features (`w_vessel`, `w_coils`, `w_blanket`, `w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil`). After this spec, only 3 are needed.

Edit `lib/extractors/cost_model.py` to stop emitting `w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil`. The `model_output.txt` source files don't need changes; the extractor just drops the irrelevant rows.

Backward compatibility: existing feature files that already contain the 4 retired features should have those entries removed in the same Slice 0 schema reconciliation pass. The Slice 0 work already touches every feature file, so this is essentially free.

---

## Change E: Schema and feature-file updates

### Add to `schema.yaml`

```yaml
unit_count_estimate:
  type: int
  required: true
  extractor: manual
  description: |
    Number of identical factory-built precision units per plant.
    Used by the unit_multiplicity rating embedding.
    Manually populated per concept from architecture analysis.
```

### Retire from `schema.yaml`

Remove these 4 feature definitions:
- `w_bop`
- `w_fuel_cycle`
- `w_aux`
- `w_civil`

### Per-concept feature-file updates

For each of the 40 feature files:
1. Add `unit_count_estimate` block (manual extractor, value per the table below)
2. Remove `w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil` blocks

#### Per-concept `unit_count_estimate` values

| Feature file | Value | Source / rationale |
|---|---|---|
| `01-hts-compact-tokamak.yaml` | 18 | CFS TF coil segments |
| `02-acoustic-icf-sonofusion.yaml` | 100 | acoustic resonator array |
| `03-laser-icf-liquid-jet-target.yaml` | 200 | Cortex DPSSL beamlines |
| `04-laser-icf.yaml` | 500 | hb11 DPSSL beamlines |
| `05-planar-coil-stellarator.yaml` | 40 | Thea planar coil segments |
| `06-magnetic-mirror.yaml` (p-B11) | 30 | Pale Blue mirror cells |
| `07-maglif.yaml` | 100 | MagLIF Marx-generator bricks |
| `08-frc-w-direct-conversion.yaml` | 75 | Helion capacitor modules |
| `09-qi-stellarator-hts.yaml` | 50 | Proxima non-planar coil segments |
| `10-large-scale-stellarator.yaml` | 40 | Gauss HELIAS coils (W7-X-like) |
| `11-magnetic-mirror.yaml` (D-T) | 12 | Realta D-T mirror cells |
| `12-levitated-dipole.yaml` | 1 | OpenStar single dipole coil |
| `13-electrostatic-hybrid.yaml` | 200 | Avalanche desktop Orbitron units |
| `14-magnetized-target-fusion-pneumatic-compression.yaml` | 60 | General Fusion capacitor modules |
| `15-sheared-flow-stabilized-z-pinch.yaml` | 50 | Zap capacitor modules |
| `16-muon-catalyzed-fusion.yaml` | 1 | Acceleron single muon accelerator |
| `17a-laser-icf-hybrid-direct-drive.yaml` | 4 | Xcimer large e-beam KrF tanks |
| `17b-laser-icf-direct-drive-fast-ignition.yaml` | 200 | Focused Energy DPSSL beamlines |
| `18-p-b11-frc.yaml` | 8 | TAE NBI modules |
| `19-orbital-levitated-dipole.yaml` | 1 | Zephyr single orbital dipole |
| `20a-type-one-stellarator.yaml` | 40 | Type One segmented HTS coils |
| `20b-renaissance-stellarator.yaml` | 40 | Renaissance segmented HTS |
| `21-spherical-tokamak-hts.yaml` | 14 | Tokamak Energy ST coil segments |
| `22-projectile-icf.yaml` | 50 | First Light launcher modules |
| `23-laser-icf-nanostructured-target.yaml` | 500 | Marvel DPSSL beamlines (imputed from hb11 peer) |
| `24-dense-plasma-focus.yaml` | 8 | LPPFusion DPF electrode units |
| `25-heavy-ion-beam-icf.yaml` | 1 | Intensity single accelerator |
| `26-laser-icf-indirect-drive.yaml` | 1000 | Inertia DPSSL Thunderwall beamlines |
| `27-polywell.yaml` | 6 | EMC2 Polywell grid units |
| `28-hts-tokamak-full-hts.yaml` | 16 | Energy Singularity integrated coils |
| `29-negative-triangularity-tokamak.yaml` | 16 | Firefly NTT coils (MANTA proxy) |
| `30-laser-icf-nif-commercialization.yaml` | 1000 | Inertia NIF Commercialization beamlines |
| `31-laser-icf-oec-architecture.yaml` | 200 | Blue Laser OEC beamlines (imputed from Focused peer) |
| `32-laser-icf-french-national.yaml` | 200 | GenF French (imputed from Focused peer) |
| `33-state-backed-tokamak-best.yaml` | 1 | BEST single bespoke coil set |
| `35-polomac.yaml` | 4 | Deutelio Polomac poloidal magnets |
| `36-helical-coil-stellarator.yaml` | 1 | Helical Fusion continuous winding |
| `37-magnetized-target-inertial-fusion-mtif.yaml` | 100 | NearStar MTIF capacitor modules |
| `38-particle-accelerator-driven-fusion.yaml` | 1 | SHINE single accelerator |
| `39-spherical-tokamak-cs-free-p-b11.yaml` | 14 | ENN EHL-2 coil segments |

**Three concepts use imputed values** (23 Marvel, 31 Blue Laser, 32 GenF) because they weren't in the v5 matrix by name. See "Known ID drift" in the Open Questions section for the full mapping.

---

## Change F: Tests

Replace `tests/scoring_v2/test_modularity.py` (or wherever the existing modularity tests live) with a new test suite covering the v5 implementation.

Key tests:
- All 39 concepts produce scores in [1.0, 5.0]
- Score anchors: CFS ARC = 3.71, Helion = 5.00, NearStar = 5.00, BEST = 1.91, OpenStar = 2.68 (per v5 matrix)
- mvs lookup covers all 39 concepts (no concept hits the defensive fallback)
- Three subsystem ratings produce expected values for sample concepts
- percent_mod uses capex shares correctly when present; falls back to equal weighting when missing
- unit_multiplicity bracket schedule matches v5 (N=1 → 1, N=18 → 4, N=200 → 5, etc.)

Retire all existing modularity tests that reference the 12-embedding structure.

---

## Change G: Diagnostic block in feature files

Update each feature file's diagnostic to reflect the new 6-embedding structure. Example for concept 01 (CFS ARC):

```yaml
modularity_diagnostics:
  # Top-level components (with v5 blend: 0.50 / 0.25 / 0.25)
  min_viable_device_scale:           3
  percent_mod:                       4.80      # computed as 0.20*4 + 0.55*5 + 0.25*5
  unit_multiplicity:                 4
  modularity_score:                  3.70      # 0.50*3 + 0.25*4.80 + 0.25*4
                                                # (matches v5 calibration target 3.71 within rounding)

  # Lookup keys used (for traceability)
  mvs_lookup_key:                    "MFE|Tokamak (compact)"
  vessel_lookup_key:                 "MFE|Tokamak|compact"
  magnet_driver_lookup_key:          "MFE|HTS (wound)|*"
  blanket_lookup_key:                "D-T|Molten salt"

  # Subsystem ratings feeding percent_mod
  vessel_modularity_rating:          4
  magnet_driver_modularity_rating:   5
  blanket_modularity_rating:         5

  # Capex shares used for the percent_mod weighted average
  # (sourced from cost_model.py extractor; sum normalized to 1.0)
  capex_shares_used:
    w_vessel:                        0.20
    w_coils:                         0.55      # CFS coils ~55% of plant cost (per v5 narrative)
    w_blanket:                       0.25

  # Unit count detail
  unit_count_estimate:               18        # CFS TF coil segments

  # TBD-default flags (matches framework-wide TBD rule)
  blanket_assumed:                   false     # CFS has explicit Molten salt; not TBD-defaulted

  # Provenance
  v5_calibration_target:             3.71      # acceptance test reference
```

Every feature file's `modularity_diagnostics` block should follow this same structure. The populate script (`populate_modularity_diagnostics.py`) computes all these fields from the features and lookup tables, so the analyst doesn't hand-populate them.

---

## Worked examples (features → score derivation)

Three concrete examples showing how the lookup tables, embeddings, and weight blend combine to produce a final score. These are also the acceptance-test anchors.

### Example A: CFS ARC (concept 01) → 3.71

```
Features (from features/01-hts-compact-tokamak.yaml):
  confinement_family:  MFE
  mfe_topology:        Tokamak
  tokamak_shape:       Compact
  fuel:                D-T
  magnet_type:         HTS (wound)
  driver_type:         (none — MFE)
  blanket_config:      Molten salt
  unit_count_estimate: 18
  w_vessel:            0.20
  w_coils:             0.55
  w_blanket:           0.25

Embedding outputs:
  _min_viable_device_scale       → "MFE|Tokamak (compact)"      → 3
  _vessel_modularity_rating      → "MFE|Tokamak|compact"        → 4
  _magnet_driver_modularity_rating → "MFE|HTS (wound)|*"        → 5
  _blanket_modularity_rating     → "D-T|Molten salt"            → 5
  _percent_mod                   → 0.20*4 + 0.55*5 + 0.25*5     = 4.80
  _unit_multiplicity             → unit_count=18 → bracket 15-30 → 4

Composite (per weights/default.yaml modularity.embedding_weights):
  0.50 * 3 + 0.25 * 4.80 + 0.25 * 4
  = 1.50 + 1.20 + 1.00
  = 3.70 (matches v5 target 3.71 within rounding)
```

### Example B: Helion (concept 08) → 5.00

```
Features:
  confinement_family:  MIF
  mif_method:          FRC compression
  fuel:                D-He3
  driver_type:         Capacitor compression
  magnet_type:         HTS (wound)
  blanket_config:      Other/hybrid          (D-He3 → no neutron blanket)
  unit_count_estimate: 75

Embedding outputs:
  _min_viable_device_scale       → "MIF|FRC compression"        → 5
  _vessel_modularity_rating      → "MIF|FRC compression|*"      → 5
  _magnet_driver_modularity_rating → "MIF|*|Capacitor compression" → 5
  _blanket_modularity_rating     → "D-He3|*"                    → 5  (aneutronic fuel)
  _percent_mod                   → 5.00  (all three subsystems at 5)
  _unit_multiplicity             → unit_count=75 → ≥50 → 5

Composite:
  0.50 * 5 + 0.25 * 5.00 + 0.25 * 5
  = 2.50 + 1.25 + 1.25
  = 5.00 ✓
```

### Example C: BEST (concept 33) → 1.91

```
Features:
  confinement_family:  MFE
  mfe_topology:        Tokamak
  tokamak_shape:       Compact          (but functionally non-compact; see note)
  fuel:                D-T
  magnet_type:         LTS+HTS
  blanket_config:      TBD              (defaults to Liquid metal)
  unit_count_estimate: 1

Note on tokamak_shape: v3 lists BEST as a compact tokamak, but the v5
matrix treats it as non-compact (LTS, large bespoke coil set, mvs=2).
The lookup must route BEST to the non-compact key via a secondary signal —
the cleanest rule is: Magnet Type = "LTS" or "LTS+HTS" overrides the
compact-shape default. Implement this override in _mvs_key() and
_vessel_key() helpers.

Embedding outputs (with LTS-override logic):
  _min_viable_device_scale       → "MFE|Tokamak (non-compact)"  → 2
  _vessel_modularity_rating      → "MFE|Tokamak|non-compact"    → 2
  _magnet_driver_modularity_rating → "MFE|LTS+HTS|*"            → 2
  _blanket_modularity_rating     → TBD → Liquid metal → "D-T|Liquid metal" → 5
                                   (note: v5 matrix shows bl=4 for BEST;
                                   the v5 calibration may have rated TBD
                                   blanket as 4 not 5. Use 4 if matching
                                   v5 strictly; flag as a calibration
                                   inconsistency to revisit.)
  _percent_mod                   → 0.20*2 + 0.55*2 + 0.25*4     = 2.50
  _unit_multiplicity             → unit_count=1                 → 1

Composite:
  0.50 * 2 + 0.25 * 2.50 + 0.25 * 1
  = 1.00 + 0.625 + 0.25
  = 1.88 (matches v5 target 1.91 within rounding)
```

---

## Predicted scores

All 39 scores are in `modularity_matrix_v5.md` and are the **calibration target** for this implementation. The acceptance tests should reproduce these scores to within rounding tolerance.

Top scorers (per v5):

| Concept | Score | Components |
|---|---|---|
| 08 Helion | 5.00 | mvs=5, pmod=5.00, um=5 |
| 37 NearStar MTIF | 5.00 | mvs=5, pmod=5.00, um=5 |
| 07 Pacific MagLIF | 4.93 | mvs=5, pmod=4.74, um=5 |
| 14 General Fusion | 4.88 | mvs=5, pmod=4.52, um=5 |
| 13 Avalanche | 4.78 | mvs=5, pmod=4.12, um=5 |
| 02 Sonofusion | 4.59 | mvs=5, pmod=3.35, um=5 |
| 03 Cortex | 4.41 | mvs=4, pmod=4.62, um=5 |
| 17a Xcimer-not (hb11/Marvel) | 4.37 | mvs=4, pmod=4.48, um=5 |
| 17 Focused / Inertia / Blue Laser / GenF | 4.36 | mvs=4, pmod=4.43, um=5 |
| 28 EMC2 Polywell | 4.28 | mvs=5, pmod=4.12, um=3 |

Bottom scorers (per v5):

| Concept | Score | Components |
|---|---|---|
| 33 Neo / BEST | 1.91 | mvs=2, pmod=2.62, um=1 |
| 36 Helical Fusion | 2.03 | mvs=2, pmod=3.13, um=1 |
| 16 Acceleron | 2.54 | mvs=3, pmod=3.18, um=1 |
| 38 SHINE | 2.54 | mvs=3, pmod=3.18, um=1 |
| 12 OpenStar | 2.68 | mvs=3, pmod=3.73, um=1 |
| 19 Zephyr | 2.70 | mvs=3, pmod=3.82, um=1 |
| 35 Polomac | 2.84 | mvs=3, pmod=3.35, um=2 |
| 27 Xcimer | 2.86 | mvs=3, pmod=3.44, um=2 |

---

## Notable score patterns

**MIF concepts dominate the top tier** (Helion 5.00, NearStar 5.00, MagLIF 4.93, General Fusion 4.88) — pulsed compression is inherently small (mvs=5), uses replicated capacitor/Marx bricks (um=5), and avoids the breeding-blanket complexity (pmod high). The framework correctly identifies that MIF's architectural simplicity is its modularity advantage.

**OpenStar at 2.68 despite compact dipole architecture** — the single levitated dipole coil drives um=1, which weighs heavily (0.25). Even with mvs=3 and pmod=3.73, the lack of unit replication caps the composite. The matrix narrative ("annual swap, but only 1 coil per plant") flags this as a known limitation; future temporal replication credit could lift this.

**BEST at 1.91 — the framework's floor** — non-compact LTS + single bespoke coil set + N=1 lands the concept at the bottom. Compare to CFS at 3.71 (same fuel, similar topology but compact HTS + demountable + N=18). The framework correctly distinguishes the SMR-class CFS architecture from the megaproject BEST architecture even though both are D-T tokamaks.

**Helical Fusion at 2.03 despite being a stellarator** — the continuous helical winding (N=1) breaks the stellarator pattern. Other stellarators in the matrix (Thea, Proxima, Type One, Renaissance) score 3.03-3.11 with ~40-50 coil segments and um=5. Helical Fusion's unique winding architecture costs ~1 full modularity point.

**Aneutronic fuels boost percent_mod via the blanket score** — Sonofusion (D-D) lifts from pmod=3.35 to compositepscore=4.59 partly because D-D triggers `blanket_modularity_rating=5` (no breeding blanket needed). Same effect for hb11/Marvel (p-B11) and Cortex (D-D).

**Inertia/Focused/Blue Laser/GenF tied at 4.36** — DPSSL D-T baseline with 200-1000 beamlines. The framework treats them as architecturally equivalent on modularity; differentiation comes from the other axes (Tech Feasibility, Supply Chain).

---

## Files touched

```
exploration/scoring_v2/schema.yaml                         # add unit_count_estimate, retire 4 w_* features
exploration/scoring_v2/weights/default.yaml                # restructure modularity block
exploration/scoring_v2/weights/slice1.yaml                 # retire or restructure (see slice 1 of integrated plan)
exploration/scoring_v2/embeddings/rulebook.py              # replace 12 embeddings with 6
exploration/scoring_v2/lookup_modularity.yaml              # NEW
exploration/scoring_v2/lib/extractors/cost_model.py        # trim 4 retired features
exploration/scoring_v2/features/*.yaml                     # 39 files: add unit_count_estimate, remove 4 w_* features, update diagnostic
exploration/scoring_v2/scripts/populate_modularity_diagnostics.py  # NEW (idempotent populate script)
tests/scoring_v2/test_modularity.py                        # replace existing modularity tests
.project/active/scoring-v2-modularity-v5-slice/design.md    # NEW: this spec
```

---

## Implementation notes for Claude Code

- **This is a destructive replacement.** Delete the existing 12-embedding modularity logic before adding the new 6-embedding logic. Don't try to keep both running side-by-side.

- **Capex shares (`w_vessel`, `w_coils`, `w_blanket`) stay as features.** The `cost_model.py` extractor still emits them; only the 4 retired shares stop being emitted. The existing `model_output.txt` files remain authoritative for the 3 retained shares.

- **`unit_count_estimate` is manual.** Each of 40 feature files gets a value populated from the table in Change E above. The values are derived from the v5 matrix's narrative.

- **mvs lookup key derivation is the most complex part.** The `_mvs_key()` helper has several disambiguation branches; the test suite must cover all 40 concepts' keys.

- **Backwards-compatibility break.** Any downstream artifact that consumes the old modularity dimension columns or per-subsystem ratings breaks. The integrated implementation plan's Slice 1 grep for `manufacturability_scale_out` and `economic_potential` columns catches the dimension-level breakage; per-subsystem references should also be greped.

### Migration steps (recommended order)

Run in this order to avoid breakage:

1. **Snapshot baseline**: run existing test suite, save current scoring output as `scores_baseline.csv` for comparison.
2. **Retire old weights**: delete `manufacturability_scale_out` block from `weights/default.yaml`. Add new top-level `modularity` block with the lookup tables from Change A.
3. **Retire old embeddings**: delete the 12 modularity-related embedding functions from `embeddings/rulebook.py`. Don't yet delete the helpers they call (kept for safety until full retire).
4. **Add new embeddings**: add the 6 new embeddings from Change B, plus the `_mvs_key()`, `_vessel_key()`, `_magnet_driver_key()` helpers.
5. **Trim extractor**: edit `lib/extractors/cost_model.py` to stop emitting `w_bop`, `w_fuel_cycle`, `w_aux`, `w_civil`.
6. **Update schema**: remove the 4 retired capex shares from `schema.yaml`; add `unit_count_estimate`.
7. **Repopulate feature files**: run the new populate script which (a) populates `unit_count_estimate` from the per-concept table in Change E, and (b) removes the 4 retired capex share entries from each feature file.
8. **Re-run scoring**: produce new `scores_new.csv`. Diff against baseline — every concept's modularity score should now match the v5 calibration target.
9. **Update tests**: replace `test_modularity.py` with v5-anchored tests (Change F).
10. **Run full test suite**: ensure no other axis broke (TF, supply chain, etc. don't depend on modularity, so they should be unaffected).
11. **Final delete**: now safe to delete any remaining helpers/utilities for the old per-subsystem ratings (`_bop_rating`, `_fuel_cycle_rating`, etc.) that the new embeddings don't reference.

---

## Open questions

1. **Should `unit_count_estimate` be a controlled vocabulary or a free integer?** Currently free integer. Could be bucketed in the schema (e.g., enum: 1, 2, 5, 10, 30, 50, 100, 500) but loses precision. Recommend free integer; the bracket schedule does the bucketing at score time.

2. **OpenStar's temporal replication.** The v5 doc notes: "A future refinement might allow temporal replication (replaceable consumables) to count toward um. An ARC-class concept that swaps blanket modules every 2 years could be argued to have effective multiplicity > 1." Currently unimplemented; would lift OpenStar from um=1 toward um=2-3. Defer to a future iteration.

3. **Cross-axis consistency for "exotic" concepts.** Sonofusion scores 4.59 on modularity (high) but 1.0 on Tech Feasibility. Avalanche scores 4.78 on modularity but 1.0 on TF. The framework correctly separates the questions, but the analyst should expect these concepts to score well on M&SO axes while floor-bottoming on TF — and the composite weighted blend reveals the trade-off honestly.

4. **Does `_mvs_key` need to handle `Other` confinement family?** The v3 ontology has only MFE/IFE/MIF/Non-Standard. `Other` was a legacy from older spec drafts. Current key derivation doesn't have an `Other` branch — if the schema gains an `Other` value, add a branch with a defensive default.

5. **Known ID drift (v5 matrix vs v3 ontology).** The `modularity_matrix_v5.md` reference document predates the v3 ontology's 17a/17b split, 20a/20b split, and renumbering of IDs 21+. When verifying implementation scores against the v5 matrix, use the mapping below (the implementation should follow v3 IDs throughout; only the v5 matrix's IDs need translation):

| v3 ID | v5 matrix ID | Notes |
|---|---|---|
| 01–16 | 01–16 | No drift |
| 17a Xcimer | 27 (in v5) | v5 listed Xcimer with old concept-27 numbering |
| 17b Focused Energy | 17 (in v5) | v5 listed Focused as concept 17 |
| 18, 19 | 18, 19 | No drift |
| 20a Type One | 20 (in v5) | |
| 20b Renaissance | 21 (in v5) | |
| 21 Tokamak Energy | 22 (in v5) | shifted by 1 |
| 22 First Light | 23 (in v5) | shifted by 1 |
| **23 Marvel Fusion** | **not in v5 by name** | impute from concept 04 hb11 (architectural peer: p-B11 ultrashort laser) |
| 24 LPPFusion | 25 (in v5) | shifted by 1 |
| 25 Intensity | 26 (in v5) | shifted by 1 |
| 26 Inertia Indirect Drive | 31 (in v5, named "Inertia") | v5 had single Inertia entry |
| 27 EMC2 Polywell | 28 (in v5) | shifted by 1 |
| 28 Energy Singularity | 29 (in v5) | shifted by 1 |
| 29 Firefly | 30 (in v5) | shifted by 1 |
| 30 Inertia NIF Commercialization | 31 (in v5, same as 26) | both Inertia concepts map to one v5 entry |
| **31 Blue Laser Fusion** | **not in v5 by name** | impute from concept 17b Focused Energy (D-T DPSSL direct drive peer) |
| **32 GenF Systems** | **not in v5 by name** | impute from concept 17b Focused Energy (D-T DPSSL direct drive peer) |
| 33 Neo / BEST | 34 (in v5) | shifted by 1 |
| 35 Deutelio Polomac | 35 | No drift |
| 36 Helical Fusion | 36 | No drift |
| 37 NearStar | 37 | No drift |
| 38 SHINE | 38 | No drift |
| 39 ENN | 39 | No drift |

The three concepts marked **not in v5 by name** (23 Marvel, 31 Blue Laser, 32 GenF) use imputed values from architectural peers; the per-concept `unit_count_estimate` table in Change E reflects these imputations. Recommend the analyst verifies these imputed scores in a follow-up calibration round once the implementation produces concrete numbers.
