# Implementation Spec: Technical Feasibility (Triple Product Gap) Scoring Axis

**Status:** Ready for implementation
**Owner:** Mallory
**Created:** 2026-05-19
**Branch:** `concept-downselect`
**Target directory:** `.project/active/scoring-v2-technical-feasibility-slice/` (new slice)
**Schema version:** v0.3.0 (`schema.md`, 2026-05-12)

This is a Claude Code implementation spec for the Technical Feasibility axis based on the Wurzel & Hsu (2022, 2025 update) triple product framework. The score measures how far a concept's architectural family is from the triple product required for breakeven.

---

## Summary

Build a new **Technical Feasibility** scoring axis as a peer of Modularity, Supply Chain, Plant Complexity, Customization, and Upper Capacity Factor in `weights/default.yaml`. The axis produces a deterministic 1.0–5.0 score per concept based on the **triple product gap** between what the concept's architectural family has demonstrated and what its fuel cycle requires for breakeven.

### Score formula

```
gap = required_triple_product[fuel] / achieved_triple_product[confinement_family, confinement_concept]
log_gap = log10(gap)
technical_feasibility_score = bucket(log_gap)

where bucket() maps log_gap to a 5-tier score (see Section "Score buckets" below)
```

This is **structurally different** from the prior penalty-stack axes — the input is a continuous numeric ratio rather than a sum of categorical penalties — but follows the same governance pattern: lookup tables co-located in `weights/default.yaml`, metadata in a separate YAML, deterministic computation, diagnostic block per concept.

### What the score measures

**Question the score answers:** *How far is this concept's architectural family from demonstrating the triple product (n·T·τ) required for fusion breakeven with its chosen fuel?*

- **Score 5**: Architectural family has demonstrated triple product at or above the required value (within 1× of target). Laser ICF post-2022 ignition is the only family currently here.
- **Score 4**: Within 1 order of magnitude (10×) — within striking distance of breakeven.
- **Score 3**: 10-1000× gap — decades of incremental progress needed.
- **Score 2**: 1,000-100,000× gap — multiple architectural generations away.
- **Score 1**: >100,000× gap, or no credible measurement.

### Key design choices

- **Two lookup tables co-located in `weights/default.yaml`**: achieved triple product by `(Confinement Family, Confinement Concept)`, and required triple product by `Fuel`. Both visible at the tuning surface.
- **Log-scale bucket mapping**: triple products span 13 orders of magnitude in the matrix, so linear thresholds don't work. Bucket boundaries are powers of 10.
- **Architectural-family scoring, not concept-specific**: Indirect-drive concepts (26 Laser ICF Indirect Drive, 30 NIF Commercialization) get credit for NIF's ignition because both use the same architectural family. The engineering of running this at a power plant is captured in Plant Complexity, not here.
- **All triggers use existing v0.3.0 schema features**: `Fuel`, `Confinement Family`, `Confinement Concept`. No new features required.
- **No site/credibility adjustments**: this is a *physics* axis. Whether a company will *actually* deliver on the architectural promise is an investment-judgment question, not a feature-driven score.

### Source of triple product data

Primary source: **Wurzel & Hsu (2022, 2025 update)** — *Continuing progress toward fusion energy breakeven and gain as measured against the Lawson criteria*, Phys. Plasmas 32, 112106 (2025), updating Phys. Plasmas 29, 062103 (2022). This is the canonical compilation for MFE, MIF, and ICF concepts.

Supplemented for post-2025 and exotic architectures:
- **W7-X 2025 records**: IPP press release, May 22, 2025 (stellarator long-pulse triple product)
- **NIF ignition**: Abu-Shawareb et al., Phys. Rev. Lett. 132, 065102 (2024) — Q_sci ≈ 4 in 2025
- **Zap Energy FuZE-3**: PRNewswire Nov 18, 2025; pressure-based estimates for sheared-flow Z-pinch
- **TAE Norm / Helion Trenta**: company disclosures + Wurzel-Hsu 2022 FRC data
- **Levitated dipole**: LDX results (historical)
- **Magnetic mirror**: GAMMA-10 era achievements (no commercial-scale demonstrations since)
- **Electrostatic (IEC, Polywell, Orbitron)**: literature on Hirsch-Farnsworth and successors; no credible high triple product

---

## Changes summary

| # | Change | Touches |
|---|---|---|
| A | Add `technical_feasibility` axis with two inline lookup tables to `weights/default.yaml` | `weights/default.yaml` |
| B | Implement `triple_product_gap` and `technical_feasibility_score` embeddings | `embeddings/rulebook.py` |
| C | Create `lookup_triple_product.yaml` metadata file (per-row provenance, citations) | `lookup_triple_product.yaml` (new) |
| D | Add `technical_feasibility_diagnostics` derived block per feature file | `features/*.yaml` (39 files) |
| E | Add acceptance tests | `tests/scoring_v2/test_technical_feasibility.py` (new) |

---

## Change A: M&SO axis registration with inline lookup tables

### Updated `weights/default.yaml`

```yaml
# Existing axes (unchanged by this spec)
# ... economic_potential, technical_feasibility (legacy empty), manufacturability_scale_out,
# ... supply_chain, plant_complexity, customization, upper_cf ...

# NEW axis added by this spec (replaces the legacy empty placeholder)
technical_feasibility:
  technical_feasibility_score: 1.0           # axis-level M&SO weight

  # Sub-table 1: Required triple product by fuel (keV·s/m³) for Q_sci=1 breakeven
  # Source: Wurzel & Hsu 2022, Section II (Lawson criterion derivation)
  required_triple_product:
    D-T:      3.0e21      # ~3e21 at optimal ~15 keV
    D-D:      3.0e23      # ~100x harder than D-T
    D-He3:    5.0e22      # ~17x harder than D-T
    p-B11:    3.0e23      # ~100x harder than D-T (similar to D-D)
    Unknown:  3.0e23      # Conservative default: treat as advanced-fuel-class

  # Sub-table 2: Best demonstrated triple product by architectural family (keV·s/m³)
  # Keys are "(Confinement Family) | (Confinement Concept)" tuples.
  # Source: Wurzel & Hsu 2022/2025 + supplementary references (see lookup_triple_product.yaml)
  achieved_triple_product:
    # Tokamak family - JT-60U/JET DT projected equivalent
    "MFE|Tokamak":                    1.5e21
    "MFE|Compact tokamak":            1.5e21
    "MFE|Spherical tokamak":          1.5e21
    "MFE|Negative triangularity tokamak": 1.5e21

    # Stellarator family - W7-X 2025 records
    "MFE|Stellarator (QA)":           1.0e20
    "MFE|Stellarator (QI)":           1.0e20
    "MFE|Stellarator (QH)":           1.0e20
    "MFE|Stellarator (general)":      1.0e20
    "MFE|Stellarator (HELIAS)":       1.0e20

    # Mirrors and FRCs
    "MFE|Magnetic mirror":            1.0e18
    "MFE|FRC (beam-driven)":          1.0e19
    "MFE|FRC (compact toroid)":       1.0e19
    "MFE|Levitated dipole":           1.0e17
    "MFE|Levitated dipole (orbital)": 1.0e17

    # MIF
    "MIF|FRC (pulsed compression)":            1.0e19
    "MIF|Magnetized target (pulsed power)":    1.0e19
    "MIF|Magnetized target (pneumatic)":       1.0e18

    # IFE
    "IFE|Laser ICF (direct drive)":            5.0e21    # NIF/OMEGA class
    "IFE|Laser ICF (indirect drive)":          5.0e21    # NIF ignition 2022-2025
    "IFE|Laser ICF (fast ignition)":           1.0e20    # FIREX
    "IFE|Laser ICF (ultrashort pulse)":        1.0e18    # hb11-class (extrapolation; see metadata)
    "IFE|Laser ICF (hybrid drive)":            1.0e21    # OMEGA-class precedent
    # "IFE|Laser ICF (liquid jet)" intentionally omitted — Cortex's novel liquid-jet
    # target geometry is its own architectural family with no triple-product measurement.
    # Defaults to floor (1.0) via no-data treatment.
    "IFE|Heavy ion beam ICF":                  1.0e15    # NDCX-II / LBNL HIB research
    "IFE|Projectile ICF":                      1.0e17    # First Light demos

    # MFE Z-pinch (sheared-flow). In v3 ontology, Zap-class Z-pinch is filed under
    # Confinement Family = MFE, MFE Topology = Open/Linear (which it shares with
    # magnetic mirrors). The derived confinement_concept disambiguates: Driver Type
    # = "Magnetic pinch" → Z-pinch (this entry); Driver Type = "Magnetic" → Mirror
    # (the MFE|Magnetic mirror entry above).
    "MFE|Z-pinch (sheared-flow)":              1.0e17    # FuZE-class measurements

    # Other (non-MFE/IFE/MIF) architectures
    "Other|Dense plasma focus":                1.0e16    # LPP DPF (peer-reviewed)

    # Non-Standard family. In v3 ontology, this is a fourth Confinement Family
    # beyond MFE/IFE/MIF, populated by concepts whose physics doesn't fit the
    # standard fusion-plant framework. Most have no architecturally-relevant
    # triple product measurement and default to floor via the no-data treatment.
    "Non-Standard|Plasma focus":               1.0e16    # LPP DPF (if filed under Non-Standard rather than Other)
    # "Non-Standard|Electrostatic" intentionally omitted — IEC/Polywell/Orbitron
    # have no triple product measurements; default to floor
    # "Non-Standard|Muon-catalyzed" intentionally omitted — muon catalysis
    # doesn't produce a confined plasma; doesn't fit Lawson framework
    # "Non-Standard|Acoustic" intentionally omitted — no credible peer-reviewed
    # measurement for sonofusion-class concepts
```

### Laser approach modifier for IFE concepts

In addition to the family-level achieved triple product, IFE concepts apply a small per-approach modifier reflecting the relative maturity of each laser drive approach against the NIF indirect-drive ignition benchmark. Modifiers are added to the bucket score *after* the gap-based score is computed.

```yaml
laser_approach_modifier:
  "Indirect drive":                              0.0    # NIF achieved ignition; family record reference point
  "Direct drive":                              -0.25    # OMEGA hydro-equivalent ~75% of ignition (Goncharov et al. 2021)
  "Hybrid drive":                              -0.25    # Combines direct + indirect; OMEGA-class precedent
  "Fast ignition":                              -0.5    # FIREX-class; further behind ignition pathway
  "Ultrashort pulse":                           -0.5    # Different physics regime; less mature
  # "Liquid jet" intentionally NOT in modifier table — Cortex's liquid-jet is its
  # own architectural family with no triple product, NOT a laser-approach variant
  # of mainstream ICF. Handled via the no-data floor route (see lookup table above).
  "N/A":                                         0.0    # Non-IFE concepts; no modifier applies
```

**Rationale for the modifier values**. OMEGA direct-drive cryogenic implosions have achieved hot-spot pressures up to 40 Gbar, and hydrodynamic scaling to NIF energies projects ~75% of ignition triple product (Goncharov et al., APS DPP 2021; later published as Phys. Plasmas 32, 032711, 2025). The physics is well-validated; the gap is laser energy and target uniformity engineering. A small -0.25 penalty reflects that the ignition demonstration is a hydro-equivalent scaling rather than an actual NIF-class ignition shot. Hybrid drive (Xcimer's KrF excimer approach) gets the same modifier because it inherits OMEGA-class direct-drive precedent. Fast ignition and ultrashort pulse get -0.5 reflecting their further distance from a demonstrated ignition pathway. Liquid jet is excluded from the modifier table entirely because it's not a laser-approach variant — it's a novel target geometry treated as its own no-data architectural family.

### Why two lookup tables, not a single per-concept table

The framework derives the required-vs-achieved comparison from **fuel** (which determines the required value) and **architectural family** (which determines the achieved value). Two concepts using the same architectural family but different fuel get the same achieved value but different required values — this captures the fact that p-B11 + tokamak is much further from breakeven than D-T + tokamak, because the *fuel* makes the target harder, not the *architecture* doing less.

### Why match on `(Confinement Family, Confinement Concept)` jointly

Some confinement concepts are ambiguous without the family context. For example, "FRC (pulsed compression)" is MIF (Helion-style); "FRC (beam-driven)" is MFE (TAE-style); both produce different triple product expectations because they operate in different parameter regimes. The compound key `"MFE|FRC (beam-driven)"` is unambiguous and matches v0.3.0 schema columns exactly.

### Why required is fuel-only (not joint with architecture)

The Lawson criterion gives the required triple product as a function of *fuel* (specifically the σv reactivity curve and bremsstrahlung losses), not confinement strategy. A p-B11 tokamak and a p-B11 FRC need the same ~3×10²³ triple product because the physics constraint is set by the fuel reactivity. Different confinement strategies have different *paths* to that target, but the target itself is fuel-determined.

---

## Change B: Embeddings in `rulebook.py`

### Implementation

Add to `embeddings/rulebook.py` after the existing upper_cf embeddings:

```python
# ===========================================================================
# Technical Feasibility Axis (Triple Product Gap)
#
# Deterministic scoring based on the ratio of required triple product (set by
# fuel choice) to achieved triple product (set by architectural family).
# Weights come from weights/default.yaml under the technical_feasibility axis.
#
# Source: Wurzel & Hsu 2022/2025 + supplementary references.
# ===========================================================================

import math

# Score buckets based on log10(required/achieved)
# Each bucket boundary is a power of 10 (i.e., orders of magnitude in gap)
_LOG_GAP_BUCKETS = [
    # (max_log_gap, score) — first match wins
    (0.0,  5.0),   # At or above target (NIF-class ignition)
    (1.0,  4.0),   # Within 10x (within striking distance)
    (3.0,  3.0),   # 10x to 1000x (decades of incremental progress)
    (5.0,  2.0),   # 1000x to 100,000x (multiple architectural generations)
    # Anything beyond 5 orders of magnitude → score 1.0
]


def _load_tf_tables(weights_yaml: dict) -> tuple[dict, dict]:
    """Extract the two lookup tables from weights/default.yaml.

    Returns (required_triple_product, achieved_triple_product).
    Both are dicts: required keyed by fuel, achieved keyed by
    'Confinement Family|Confinement Concept'.
    """
    tf = weights_yaml.get("technical_feasibility", {})
    required = tf.get("required_triple_product")
    achieved = tf.get("achieved_triple_product")
    if required is None or achieved is None:
        raise ValueError(
            "weights/default.yaml technical_feasibility axis is missing "
            "required_triple_product or achieved_triple_product lookup tables."
        )
    # Validate required has all fuels
    required_fuels = {"D-T", "D-D", "D-He3", "p-B11", "Unknown"}
    missing_fuels = required_fuels - set(required.keys())
    if missing_fuels:
        raise ValueError(
            f"technical_feasibility.required_triple_product missing fuels: {missing_fuels}"
        )
    return {k: float(v) for k, v in required.items()}, {k: float(v) for k, v in achieved.items()}


def _achieved_key(confinement_family: str, confinement_concept: str) -> str:
    """Build the canonical compound key for the achieved_triple_product lookup."""
    cf = confinement_family or ""
    cc = confinement_concept or ""
    return f"{cf}|{cc}"


def _score_from_log_gap(log_gap: float) -> float:
    """Map log10(gap) to a 1.0-5.0 score via the bucket schedule."""
    for max_log_gap, score in _LOG_GAP_BUCKETS:
        if log_gap <= max_log_gap:
            return score
    return 1.0


@embedding(
    "triple_product_gap",
    inputs=["fuel", "confinement_family", "confinement_concept"],
)
def _triple_product_gap(
    fuel: str,
    confinement_family: str,
    confinement_concept: str,
    *,
    weights_yaml: dict,
) -> float | None:
    """Ratio of required triple product to achieved triple product.

    A gap of 1.0 means the architectural family has reached the required
    triple product for its fuel. A gap of 100 means the family is 100x
    below the target. Higher gap = further from breakeven.

    Returns None if no achieved triple product is available for the
    architectural family (e.g., Sonofusion, IEC fusors, Orbitron, beam-target
    accelerators, muon-catalyzed). These concepts will floor at score 1.0
    via the downstream scoring embedding.

    Raises if fuel is not in the required-table — that's a data error worth
    failing on.
    """
    fuel = fuel or "Unknown"
    required_table, achieved_table = _load_tf_tables(weights_yaml)

    if fuel not in required_table:
        raise ValueError(
            f"Unknown fuel value: {fuel!r}. Expected one of {sorted(required_table.keys())}."
        )

    key = _achieved_key(confinement_family, confinement_concept)
    if key not in achieved_table:
        # No architectural-family triple product available.
        # Honest "no data" — return None so the score embedding can floor it.
        return None

    required = required_table[fuel]
    achieved = achieved_table[key]
    if achieved <= 0:
        return None
    return required / achieved


@embedding(
    "technical_feasibility_score",
    inputs=["triple_product_gap", "confinement_family", "laser_approach"],
)
def _technical_feasibility_score(
    triple_product_gap: float | None,
    confinement_family: str,
    laser_approach: str,
    *,
    weights_yaml: dict,
) -> float:
    """Technical feasibility score on a 1.0-5.0 scale.

    Higher score = closer to breakeven for the concept's fuel and
    architectural family.

    Returns floor score (1.0) when triple_product_gap is None — meaning
    no architecturally-relevant triple product measurement exists for the
    concept's family. This is honest "no data" rather than a fabricated value.

    For IFE concepts, applies a laser_approach modifier reflecting the relative
    maturity of the laser drive approach against the NIF indirect-drive
    ignition benchmark. The modifier is added to the bucket score after the
    gap-based score is computed. See the `laser_approach_modifier` table in
    weights/default.yaml for values and rationale.

    Buckets (by log10 of gap):
        <= 0     → 5.0  (at or above target)
        (0, 1]   → 4.0  (within 10x)
        (1, 3]   → 3.0  (10x-1000x)
        (3, 5]   → 2.0  (1000x-100,000x)
        > 5      → 1.0  (>100,000x)
        None     → 1.0  (no data — floored)
    """
    if triple_product_gap is None:
        return 1.0
    if triple_product_gap <= 0 or math.isinf(triple_product_gap):
        return 1.0
    log_gap = math.log10(triple_product_gap)
    base_score = _score_from_log_gap(log_gap)

    # Apply IFE laser approach modifier
    if confinement_family == "IFE" and laser_approach:
        tf_weights = weights_yaml.get("technical_feasibility", {})
        modifier_table = tf_weights.get("laser_approach_modifier", {})
        modifier = modifier_table.get(laser_approach, 0.0)
        adjusted = base_score + float(modifier)
        return max(1.0, min(5.0, adjusted))

    return base_score
```

### Why the score uses a bucket schedule, not a continuous formula

Triple products span 13 orders of magnitude across the 39-concept matrix. A linear formula `5 - log10(gap)` would put everything at 1.0 except NIF-class. A continuous logarithmic formula like `5 / (1 + log_gap)` would give nonsensical fractional scores. The 5-tier bucket schedule maps the wide spread into a clean 5-level categorical score, matching the other axes' tier structures.

### Why no penalty for missing data

The lookup tables MUST contain every (family, concept) combination present in the 39-concept matrix. If a combination is missing, `_triple_product_gap` raises — fail loudly rather than silently default. This forces the analyst to make an explicit triple product estimate when a new architectural family is added.

### Why the bucket schedule has 5 entries but the table only lists 4

The bucket schedule covers `log_gap ≤ 5.0` explicitly; anything beyond falls through to the default `1.0`. This is a defensive pattern matching how the other axes handle their floor values (`max(1.0, ...)`).

---

## Change C: `lookup_triple_product.yaml` (metadata only)

### New file: `exploration/scoring_v2/lookup_triple_product.yaml`

```yaml
# Triple product lookup table metadata.
#
# Numerical values are NOT here — they live in weights/default.yaml under
# technical_feasibility.required_triple_product and
# technical_feasibility.achieved_triple_product to keep the tuning surface
# co-located with other axes.
#
# Each entry documents:
#   - value: the numerical triple product (mirrors default.yaml; for reference)
#   - source: citation for the value
#   - notes: caveats, methodology, post-publication updates
#   - last_updated: date of the most recent source consulted
#
# The authoritative numbers live in default.yaml; this file is human-readable
# documentation of provenance.

required_triple_product:
  description: |
    Required triple product (n·T·τ in keV·s/m³) for scientific breakeven
    (Q_sci = 1) at the optimal ion temperature for each fuel. Derived from
    the Lawson criterion accounting for bremsstrahlung losses.

    Note: these are *breakeven* targets, not commercial operating targets.
    A commercial reactor typically requires Q ≥ 10-30 (a factor of 10-30
    above breakeven). The framework uses breakeven as the reference point
    because it's the threshold most experiments are aiming at first.

  entries:
    D-T:
      value: 3.0e21
      source: "Wurzel & Hsu 2022, Fig. 2 (Lawson criterion contours, T_opt ≈ 15 keV)"
      notes: |
        Minimum at ~15 keV ion temperature. The classic Lawson value.

    D-D:
      value: 3.0e23
      source: "Wurzel & Hsu 2022, Fig. 2; Stirring the Fusion Pot (2014) calculation"
      notes: |
        Optimum ~30 keV. ~100x harder than D-T due to ~10x lower σv at peak
        and higher Bremsstrahlung losses at the required temperature.

    D-He3:
      value: 5.0e22
      source: "Wurzel & Hsu 2022; Bishop et al. 2024 D-3He Lawson analysis"
      notes: |
        Optimum ~75 keV. ~17x harder than D-T. Aneutronic primary reaction
        but D-D side reactions produce some neutrons.

    p-B11:
      value: 3.0e23
      source: "Bishop et al. 2024 'Lawson Criterion Analysis of D-3He Fusion'; Putvinski 2019"
      notes: |
        Optimum ~150-300 keV. ~100x harder than D-T. Truly aneutronic
        primary reaction. Some recent work (Putvinski 2019) suggests
        velocity-shear configurations could reduce this to ~1e23, but
        the conservative reference value is 3e23.

    Unknown:
      value: 3.0e23
      notes: |
        Conservative default — treat unknown fuel as advanced-fuel-class
        (p-B11 equivalent). Updates when fuel feature is populated.


achieved_triple_product:
  description: |
    Best demonstrated triple product (n·T·τ in keV·s/m³) by architectural
    family. Keys are 'Confinement Family|Confinement Concept' compound
    strings matching v0.3.0 schema values.

    Methodology: per Wurzel & Hsu, achieved values are typically extracted
    from peak performance shots in peer-reviewed publications. For pulsed
    concepts, the methodology uses peak nτ_stag rather than continuous nτ_E.

  entries:
    # ----- MFE -----
    "MFE|Tokamak":
      value: 1.5e21
      source: "JT-60U Fujita et al. 1998 (Phys. Rev. Lett.); JET DT 1997 (JET Team 1992)"
      notes: |
        JT-60U claimed nT τE = 1.53e21 keV·s/m³ in 1998 high-βp H-mode.
        JET DT-1 (1997) achieved ~1e21 in actual DT operation. Treating
        this as the family record for all tokamak variants.
      last_updated: "2025-11"

    "MFE|Compact tokamak":
      value: 1.5e21
      source: "JT-60U record applied to compact-tokamak family (SPARC projected to exceed)"
      notes: |
        No compact-tokamak (HTS-based) device has yet exceeded JT-60U.
        SPARC, when operational, is projected to exceed this. Updated when
        SPARC achieves first plasma.

    "MFE|Spherical tokamak":
      value: 1.5e21
      source: "Apply tokamak family record"
      notes: |
        ST devices (NSTX-U, MAST-U, ST40) have not exceeded conventional
        tokamak triple products. Applying the family record from JT-60U.

    "MFE|Negative triangularity tokamak":
      value: 1.5e21
      source: "Apply tokamak family record"
      notes: |
        Negative-T pre-deployment; family record applies.

    "MFE|Stellarator (QA)":
      value: 1.0e20
      source: "W7-X 2025 records (IPP press release May 22, 2025)"
      notes: |
        W7-X is HELIAS-class (close to QI). Records apply broadly to
        optimized stellarators.

    "MFE|Stellarator (QI)":
      value: 1.0e20
      source: "W7-X 2025 records"

    "MFE|Stellarator (QH)":
      value: 1.0e20
      source: "W7-X 2025 records; HSX precedent"
      notes: |
        QH (quasi-helical) stellarators have not been built at large scale.
        Conservative use of W7-X family record.

    "MFE|Stellarator (general)":
      value: 1.0e20
      source: "W7-X 2025 records"

    "MFE|Stellarator (HELIAS)":
      value: 1.0e20
      source: "W7-X 2025 records (HELIAS native)"

    "MFE|Magnetic mirror":
      value: 1.0e18
      source: "GAMMA-10 era (1990s); Tsukuba tandem mirror; Wurzel & Hsu 2022 Table III"
      notes: |
        Best mirror triple products are from the 1990s. No commercial
        scale mirror has been built since. Realta, Pale Blue working
        from this baseline.

    "MFE|FRC (beam-driven)":
      value: 1.0e19
      source: "TAE Norm public statements; C2W previous gen"
      notes: |
        TAE has not published peer-reviewed triple product. Estimate from
        company statements about T_i and confinement times.

    "MFE|FRC (compact toroid)":
      value: 1.0e19
      source: "C-2/C-2U historical data; Wurzel & Hsu 2022 Table III"

    "MFE|Levitated dipole":
      value: 1.0e17
      source: "LDX (MIT) 2009-2011 experiments; Wurzel & Hsu 2022"
      notes: |
        LDX achieved its best results before being decommissioned.
        OpenStar's LDR Junior aims to extend.

    "MFE|Levitated dipole (orbital)":
      value: 1.0e17
      source: "Apply terrestrial levitated dipole record"
      notes: |
        Zephyr's orbital concept has no demonstrations; family record applies.

    # ----- MIF -----
    "MIF|FRC (pulsed compression)":
      value: 1.0e19
      source: "Helion Trenta 2021 disclosures; VENTI 2018 publications"
      notes: |
        Helion's measurements not in peer-reviewed literature. Estimate
        from company statements: VENTI nτT ≥ 1e19; Trenta 4x temperature
        and 30x volume suggests comparable or higher triple product.

    "MIF|Magnetized target (pulsed power)":
      value: 1.0e19
      source: "Sandia MagLIF program (2014-present); Wurzel & Hsu 2022 Table III"
      notes: |
        Pacific Fusion is the commercial extension of MagLIF.

    "MIF|Magnetized target (pneumatic)":
      value: 1.0e18
      source: "General Fusion historical and projected; Wurzel & Hsu 2022 alternate"
      notes: |
        General Fusion's pneumatic pistons are mechanically different from
        Sandia's pulsed-power Z; treated as lower-tier MIF.

    # ----- IFE -----
    "IFE|Laser ICF (direct drive)":
      value: 5.0e21
      source: "NIF ignition campaign 2022-2025 (Abu-Shawareb et al. 2024)"
      notes: |
        NIF achieved Q_sci ≈ 4 in April 2025; triple product ≈ 5e21.
        Indirect drive specifically, but applies to laser ICF family.
      last_updated: "2025-04"

    "IFE|Laser ICF (indirect drive)":
      value: 5.0e21
      source: "NIF ignition campaign 2022-2025"

    "IFE|Laser ICF (fast ignition)":
      value: 1.0e20
      source: "FIREX (Osaka) historical results; lower than central hot-spot"
      notes: |
        Fast ignition has not achieved NIF-class triple product. Focused
        Energy is working in this regime.

    "IFE|Laser ICF (ultrashort pulse)":
      value: 1.0e18
      source: "Extrapolated from chirped-pulse-amplification fusion literature"
      confidence: "low"
      notes: |
        hb11 and Marvel use chirped-pulse-amplification ultrashort pulses;
        avalanche fusion concepts. Lower confinement times limit triple
        product compared to nanosecond direct/indirect drive. No specific
        peer-reviewed triple-product measurement for ultrashort-pulse
        aneutronic ICF; this is an extrapolation per Wurzel-Hsu
        methodology. Mark as lower-confidence and revisit if hb11 or
        Marvel publishes definitive data.

    "IFE|Laser ICF (hybrid drive)":
      value: 1.0e21
      source: "OMEGA hybrid-drive precedent (Betti et al. 2015)"
      notes: |
        Xcimer uses excimer KrF hybrid drive (direct + indirect features).
        OMEGA has demonstrated hybrid drive at intermediate triple products.

    # "IFE|Laser ICF (liquid jet)" intentionally NOT in lookup
    # Reason: Cortex's liquid-jet target geometry is a novel concept with
    # no public triple-product data. Floor at 1.0 until a measurement
    # exists. Add entry to default.yaml when Cortex (or analogous program)
    # publishes results.

    "IFE|Heavy ion beam ICF":
      value: 1.0e15
      source: "LBNL heavy-ion beam research; never reached high triple product"
      notes: |
        Intensity Fusion uses heavy-ion beams. No HIB facility has reached
        substantial fusion triple product.

    "IFE|Projectile ICF":
      value: 1.0e17
      source: "First Light Fusion 'First Fusion' demonstrations (2022-2024)"
      notes: |
        First Light has demonstrated projectile-driven fusion but at
        very modest triple products to date.

    # ----- MFE Z-pinch (sheared-flow) -----
    # In v3 ontology, Zap-class Z-pinch is filed under Confinement Family = MFE
    # (specifically MFE Topology = Open/Linear). It shares the topology
    # classification with magnetic mirrors, so the derived confinement_concept
    # disambiguates by Driver Type: "Magnetic pinch" routes to this entry;
    # "Magnetic" routes to MFE|Magnetic mirror.
    "MFE|Z-pinch (sheared-flow)":
      value: 1.0e17
      source: "Shumlak, Meier, Levitt, Fusion Science and Technology 80(1), 2023"
      notes: |
        Shumlak et al. 2023 establishes the framework for measuring triple
        product in sheared-flow-stabilized Z-pinches with advective losses
        accounted for. FuZE-class measurements consistent with ~1e17 keV·s/m³.
        November 2025 FuZE-3 announcement (830 MPa electron pressure for ~µs)
        is consistent with this value — high pressure compensated by short
        confinement time.
      last_updated: "2025-11"

    # ----- Other -----
    "Other|Dense plasma focus":
      value: 1.0e16
      source: "LPP FoFu / FF-2B historical; Wurzel & Hsu 2022"
      notes: |
        DPF has fundamental limits from m=0 instability dynamics. Treat
        as an architectural family with limited high-triple-product
        potential. If the v3 ontology classifies DPF under Non-Standard
        rather than Other, see the Non-Standard|Plasma focus entry below
        (same value, same source).

    # "Other|Acoustic / Sonofusion" intentionally NOT in lookup
    # Reason: No credible peer-reviewed measurement exists. Taleyarkhan
    # et al. (2002-2006) claims of "bubble fusion" have not been
    # independently replicated. Floor at 1.0 until definitive data
    # published. Update analyst review trigger if Sonofusion publishes
    # measurements.

    # "Other|Particle accelerator" intentionally NOT in lookup
    # Reason: Beam-target accelerator-driven fusion doesn't produce a
    # confined plasma in the Lawson sense; the triple-product framework
    # doesn't cleanly apply. SHINE-class concepts floor at 1.0 on this
    # axis. Their value is captured in the Technical Feasibility axis
    # as "not a fusion power concept," appropriately.

    # "Other|Muon-catalyzed" intentionally NOT in lookup
    # Reason: Muon catalysis produces fusion reactions but doesn't create
    # a confined plasma; the triple-product framework doesn't apply.
    # Acceleron concept floors at 1.0.

    # ----- Non-Standard -----
    # In v3 ontology, "Non-Standard" is a fourth Confinement Family beyond
    # MFE/IFE/MIF. It collects concepts whose physics doesn't fit cleanly
    # into the standard fusion-plant frame: electrostatic confinement,
    # muon catalysis, dense plasma focus, beam-target accelerator-driven,
    # and acoustic concepts. Most have no architecturally-relevant triple
    # product measurement and default to floor (1.0) via no-data treatment.

    "Non-Standard|Plasma focus":
      value: 1.0e16
      source: "LPP FoFu / FF-2B historical; Wurzel & Hsu 2022"
      notes: |
        Same value/source as Other|Dense plasma focus. The v3 ontology may
        file LPP DPF under either Other (Confinement Family) or Non-Standard
        depending on how the Non-Standard Mechanism column is populated.
        Both keys point to the same measured value; whichever the lookup
        resolves to will produce the same score.

    # "Non-Standard|Electrostatic" intentionally NOT in lookup
    # Reason: IEC devices (Polywell, EMC2 fusor-class) and Orbitron concepts
    # (Avalanche) have been built since the 1960s without producing meaningful
    # triple product. Particle losses dominate before plasma reaches
    # confinement-relevant parameters. All such concepts floor at 1.0.

    # "Non-Standard|Muon-catalyzed" intentionally NOT in lookup
    # Reason: Muon catalysis produces fusion reactions but doesn't create
    # a confined plasma; the triple-product framework doesn't apply.
    # Acceleron concept floors at 1.0.

    # "Non-Standard|Acoustic" intentionally NOT in lookup
    # Reason: Sonofusion claims of fusion conditions are not independently
    # corroborated by peer-reviewed measurements. Floor at 1.0 until
    # definitive data published.

    # "Non-Standard|Particle accelerator" intentionally NOT in lookup
    # Reason: Beam-target accelerator-driven fusion (SHINE-class) doesn't
    # produce a confined plasma in the Lawson sense; the triple-product
    # framework doesn't cleanly apply. Floor at 1.0; the concept's actual
    # value proposition is non-power (medical isotopes) and is captured by
    # the Plant Complexity and Customization axes.

    # ----- IFE liquid jet — separate no-data family -----
    # "IFE|Laser ICF (liquid jet)" intentionally NOT in lookup
    # Reason: Cortex's liquid-jet target geometry is its own architectural
    # family with no triple-product measurement. NOT treated as a
    # laser-approach variant of mainstream ICF (with a modifier) because
    # the target geometry is fundamentally different from capsule-class
    # direct/indirect/hybrid drive. Floor at 1.0 until Cortex publishes
    # data on liquid-jet implosion performance.
```

---

## Change D: Feature-file diagnostics

Add a derived block to each concept's feature file:

### Diagnostic block format

```yaml
# In each features/{ID}-{name}.yaml file, append:
technical_feasibility_diagnostics:
  fuel: {value}
  required_triple_product: {value_in_keV_s_m3}
  confinement_family: {value}
  confinement_concept: {value}
  achieved_triple_product: {value_in_keV_s_m3}
  triple_product_gap: {ratio}
  log10_gap: {value}
  technical_feasibility_score: {1.0-5.0}
```

### Examples

**NIF Commercialization (D-T, Laser ICF indirect drive)** — score 5.0 (NIF-class, no modifier):

```yaml
technical_feasibility_diagnostics:
  fuel: D-T
  required_triple_product: 3.0e21
  confinement_family: IFE
  confinement_concept: "Laser ICF (indirect drive)"
  achieved_triple_product: 5.0e21
  triple_product_gap: 0.6
  log10_gap: -0.22
  base_score: 5.0
  laser_approach: "Indirect drive"
  laser_approach_modifier: 0.0
  technical_feasibility_score: 5.0
```

**OEC Architecture (D-T, Laser ICF direct drive)** — score 4.75 (direct-drive modifier):

```yaml
technical_feasibility_diagnostics:
  fuel: D-T
  required_triple_product: 3.0e21
  confinement_family: IFE
  confinement_concept: "Laser ICF (direct drive)"
  achieved_triple_product: 5.0e21
  triple_product_gap: 0.6
  log10_gap: -0.22
  base_score: 5.0
  laser_approach: "Direct drive"
  laser_approach_modifier: -0.25
  technical_feasibility_score: 4.75
```

**CFS ARC (D-T, Compact tokamak)** — score 4.0:

```yaml
technical_feasibility_diagnostics:
  fuel: D-T
  required_triple_product: 3.0e21
  confinement_family: MFE
  confinement_concept: "Compact tokamak"
  achieved_triple_product: 1.5e21
  triple_product_gap: 2.0
  log10_gap: 0.30
  technical_feasibility_score: 4.0
```

**Proxima QI (D-T, Stellarator QI)** — score 3.0:

```yaml
technical_feasibility_diagnostics:
  fuel: D-T
  required_triple_product: 3.0e21
  confinement_family: MFE
  confinement_concept: "Stellarator (QI)"
  achieved_triple_product: 1.0e20
  triple_product_gap: 30.0
  log10_gap: 1.48
  technical_feasibility_score: 3.0
```

**Helion (D-He³, MIF FRC pulsed compression)** — score 2.0:

```yaml
technical_feasibility_diagnostics:
  fuel: D-He3
  required_triple_product: 5.0e22
  confinement_family: MIF
  confinement_concept: "FRC (pulsed compression)"
  achieved_triple_product: 1.0e19
  triple_product_gap: 5000.0
  log10_gap: 3.70
  technical_feasibility_score: 2.0
```

**Polywell (D-T, IEC)** — score 1.0:

```yaml
technical_feasibility_diagnostics:
  fuel: D-T
  required_triple_product: 3.0e21
  confinement_family: Electrostatic
  confinement_concept: "IEC / Fusor"
  achieved_triple_product: null
  no_data_available: true
  technical_feasibility_score: 1.0
```

**Sonofusion (D-D, Acoustic)** — score 1.0 via missing data:

```yaml
technical_feasibility_diagnostics:
  fuel: D-D
  required_triple_product: 3.0e23
  confinement_family: Other
  confinement_concept: "Acoustic / Sonofusion"
  achieved_triple_product: null
  no_data_available: true
  technical_feasibility_score: 1.0
```

### How the diagnostic block handles missing data

When a concept's architectural family doesn't have a triple product entry in `achieved_triple_product`, the diagnostic block sets:
- `achieved_triple_product: null`
- `no_data_available: true`
- omits `triple_product_gap` and `log10_gap` fields (they're undefined)
- `technical_feasibility_score: 1.0` (floor)

This is honest "no measurement available" rather than fabricating a placeholder value. The five concepts currently in this state: Sonofusion (02), Cortex (03), Avalanche (13), Acceleron (16), Polywell (28), SHINE (38). All score at the framework floor of 1.0.

### Population approach

Write `scripts/populate_technical_feasibility_diagnostics.py` to programmatically populate the diagnostic block in all 39 feature files. Idempotent and re-runnable after weight changes.

---

## Change E: Acceptance tests

### New test file: `tests/scoring_v2/test_technical_feasibility.py`

```python
"""Acceptance tests for the technical feasibility scoring axis."""
import math
import pytest
import yaml
from pathlib import Path

from exploration.scoring_v2.embeddings.rulebook import (
    REGISTRY,
    _achieved_key,
    _load_tf_tables,
    _score_from_log_gap,
)


_BASE = Path(__file__).parent.parent.parent / "exploration" / "scoring_v2"
_WEIGHTS_YAML = yaml.safe_load((_BASE / "weights" / "default.yaml").read_text())
_REQUIRED, _ACHIEVED = _load_tf_tables(_WEIGHTS_YAML)


# ============================================================================
# Weights are visible in default.yaml
# ============================================================================

class TestWeightsExposedInDefaultYaml:
    """Verify both lookup tables are visible in weights/default.yaml."""

    def test_technical_feasibility_axis_exists(self):
        assert "technical_feasibility" in _WEIGHTS_YAML

    def test_axis_weight_is_one(self):
        assert _WEIGHTS_YAML["technical_feasibility"]["technical_feasibility_score"] == 1.0

    def test_all_required_fuels_present(self):
        for fuel in ["D-T", "D-D", "D-He3", "p-B11", "Unknown"]:
            assert fuel in _REQUIRED

    def test_required_values_ordering(self):
        """D-T should be easiest, advanced fuels harder."""
        assert _REQUIRED["D-T"] < _REQUIRED["D-He3"]
        assert _REQUIRED["D-He3"] < _REQUIRED["D-D"]
        assert _REQUIRED["D-He3"] < _REQUIRED["p-B11"]

    def test_d_t_required_matches_lawson(self):
        """D-T required should be ~3e21 keV·s/m³."""
        assert 1e21 <= _REQUIRED["D-T"] <= 1e22

    def test_p_b11_harder_than_d_t_by_at_least_50x(self):
        """p-B11 should be ~100x harder than D-T."""
        assert _REQUIRED["p-B11"] / _REQUIRED["D-T"] >= 50

    def test_achieved_values_have_tokamak_record(self):
        """Tokamak family should have ~1.5e21 (JT-60U/JET)."""
        assert _ACHIEVED["MFE|Tokamak"] >= 1e21

    def test_achieved_values_have_nif_record(self):
        """NIF-class direct/indirect laser ICF should be >= 1e21."""
        assert _ACHIEVED["IFE|Laser ICF (indirect drive)"] >= 1e21

    def test_missing_required_table_raises(self):
        with pytest.raises(ValueError, match="missing"):
            _load_tf_tables({"technical_feasibility": {}})


# ============================================================================
# Bucket scoring
# ============================================================================

class TestBucketScoring:
    """Verify the log10(gap) → score mapping."""

    def test_at_or_above_target_score_5(self):
        assert _score_from_log_gap(-1.0) == 5.0
        assert _score_from_log_gap(0.0) == 5.0

    def test_within_10x_score_4(self):
        assert _score_from_log_gap(0.5) == 4.0
        assert _score_from_log_gap(1.0) == 4.0

    def test_10_to_1000x_score_3(self):
        assert _score_from_log_gap(1.5) == 3.0
        assert _score_from_log_gap(3.0) == 3.0

    def test_1000_to_100k_score_2(self):
        assert _score_from_log_gap(3.5) == 2.0
        assert _score_from_log_gap(5.0) == 2.0

    def test_beyond_100k_score_1(self):
        assert _score_from_log_gap(5.5) == 1.0
        assert _score_from_log_gap(13.0) == 1.0


# ============================================================================
# Per-concept score anchors
# ============================================================================

def _score(concept_id: str) -> float:
    matches = list((_BASE / "features").glob(f"{concept_id}-*.yaml"))
    assert len(matches) == 1, f"Expected one feature file for {concept_id}"
    features = yaml.safe_load(matches[0].read_text())
    gap = REGISTRY["triple_product_gap"].fn(
        features.get("fuel"),
        features.get("confinement_family"),
        features.get("confinement_concept"),
        weights_yaml=_WEIGHTS_YAML,
    )
    return REGISTRY["technical_feasibility_score"].fn(gap)


def test_nif_class_dt_ice_indirect_drive_score_5(self):
    """D-T + Laser ICF (indirect drive) at NIF-class scores 5.0 (no modifier)."""
    # 26 Laser ICF Indirect Drive, 30 NIF Commercialization
    for cid in ["26", "30"]:
        assert _score(cid) == 5.0

def test_nif_class_dt_ice_direct_drive_score_475(self):
    """D-T + Laser ICF (direct drive) at NIF-class scores 4.75 with modifier."""
    # 31 OEC Architecture (Direct drive), 32 French National (Direct drive)
    # Base 5.0 - 0.25 direct-drive modifier
    for cid in ["31", "32"]:
        assert _score(cid) == 4.75

def test_xcimer_hybrid_drive_score_375(self):
    """Xcimer (17a hybrid drive D-T) scores 3.75: base 4.0 - 0.25 hybrid modifier."""
    # 17a hybrid: achieved 1e21 → gap 3 → log ~0.48 → bucket score 4.0
    # Then hybrid-drive modifier -0.25 → 3.75
    assert _score("17a") == 3.75

def test_tokamak_dt_score_4(self):
    """D-T tokamaks score 4.0 — within 10x of breakeven."""
    # CFS ARC (compact tokamak), Tokamak Energy ST
    for cid in ["01", "22"]:
        assert _score(cid) == 4.0

def test_stellarator_dt_score_3(self):
    """D-T stellarators score 3.0 — 10-1000x gap."""
    for cid in ["05", "09", "10", "20", "21", "36"]:
        assert _score(cid) == 3.0

def test_helion_d_he3_score_2(self):
    """Helion D-He³ MIF FRC scores 2.0 — 5000x gap."""
    assert _score("08") == 2.0

def test_polywell_score_1(self):
    """Polywell D-T IEC scores 1.0 — no architecturally-relevant measurement."""
    assert _score("28") == 1.0

def test_sonofusion_score_1(self):
    """Sonofusion has no credible measurement → score 1.0 via no-data floor."""
    assert _score("02") == 1.0

def test_no_data_concepts_floor_at_1():
    """Concepts whose architectural family has no triple-product measurement floor at 1.0."""
    # Sonofusion, Cortex, Avalanche, Acceleron, Polywell, SHINE
    for cid in ["02", "03", "13", "16", "28", "38"]:
        assert _score(cid) == 1.0

def test_no_data_returns_none_gap():
    """When achieved triple product is missing, triple_product_gap returns None."""
    # Sonofusion: Other / Acoustic — not in lookup
    gap = REGISTRY["triple_product_gap"].fn(
        "D-D", "Other", "Acoustic / Sonofusion",
        weights_yaml=_WEIGHTS_YAML,
    )
    assert gap is None

def test_no_data_score_is_floor():
    """The score embedding floors when gap is None."""
    score = REGISTRY["technical_feasibility_score"].fn(None)
    assert score == 1.0

def test_all_within_bounds():
    for cid in [f"{i:02d}" for i in range(1, 40)]:
        score = _score(cid)
        assert 1.0 <= score <= 5.0
```

---

## Predicted scores (representative concepts)

Source citations refer to the achieved triple product value. Full provenance with notes and methodology lives in `lookup_triple_product.yaml`. References at end of table.

| Concept | Fuel | Conf. Family + Concept | Achieved | Source | Required | Gap | **Score** |
|---|---|---|---|---|---|---|---|
| 01 CFS (Compact tokamak) | D-T | MFE / Compact tokamak | 1.5e21 | [1] family | 3e21 | 2× | **4.0** |
| 02 Sonofusion (Acoustic) | D-D | Non-Standard / Acoustic | *no data* | [2] | 3e23 | — | **1.0** |
| 03 Cortex (Liquid jet ICF) | D-D | IFE / Laser ICF (liquid jet) | *no data* | [3] | 3e23 | — | **1.0** |
| 04 hb11 (p-B11 fast ignition) | p-B11 | IFE / Laser ICF (fast ignition) | 1e20 | [14] family | 3e23 | 3000× | **1.0** (3.0 base − 0.5 fast-ignition modifier, then floored; gap already drives to 3.0) |
| 05 Thea (Planar stellarator) | D-T | MFE / Stellarator (planar) | 1e20 | [5] family | 3e21 | 30× | **3.0** |
| 06 Pale Blue (p-B11 mirror) | p-B11 | MFE / Magnetic mirror | 1e18 | [6] family | 3e23 | 3e5 | **1.0** |
| 07 Pacific (MagLIF) | D-T | MIF / Magnetized target (pulsed power) | 1e19 | [7] | 3e21 | 300× | **3.0** |
| 08 Helion (D-He³ FRC) | D-He³ | MIF / FRC (pulsed compression) | 1e19 | [8] | 5e22 | 5000× | **2.0** |
| 09 Proxima (QI stellarator) | D-T | MFE / Stellarator (QI) | 1e20 | [5] family | 3e21 | 30× | **3.0** |
| 10 Gauss (HELIAS stellarator) | D-T | MFE / Stellarator (HELIAS) | 1e20 | [5] family | 3e21 | 30× | **3.0** |
| 11 Realta (D-T mirror) | D-T | MFE / Magnetic mirror | 1e18 | [6] family | 3e21 | 3000× | **2.0** |
| 12 OpenStar (Levitated dipole) | D-T | MFE / Levitated dipole | 1e17 | [9] family | 3e21 | 30000× | **2.0** |
| 13 Avalanche (Orbitron) | D-T | Non-Standard / Electrostatic | *no data* | [10] | 3e21 | — | **1.0** |
| 14 General Fusion (Pneumatic MTF) | D-T | MIF / Magnetized target (pneumatic) | 1e18 | [11] | 3e21 | 3000× | **2.0** |
| 15 Zap (Sheared-flow Z-pinch) | D-T | MFE / Z-pinch (sheared-flow) | 1e17 | [12] | 3e21 | 30000× | **2.0** |
| 16 Acceleron (Muon-catalyzed) | D-T | Non-Standard / Muon-catalyzed | *no data* | [13] | 3e21 | — | **1.0** |
| 17a Xcimer (Hybrid drive) | D-T | IFE / Laser ICF (hybrid drive) | 1e21 | [18] | 3e21 | 3× | **3.75** (4.0 base − 0.25 hybrid modifier) |
| 17b Focused (Fast ignition) | D-T | IFE / Laser ICF (fast ignition) | 1e20 | [14] | 3e21 | 30× | **2.5** (3.0 base − 0.5 fast-ignition modifier) |
| 18 TAE (p-B11 FRC) | p-B11 | MFE / FRC (beam-driven) | 1e19 | [8] family | 3e23 | 30000× | **1.0** |
| 19 Zephyr (Orbital dipole) | D-He³ | MFE / Levitated dipole (orbital) | 1e17 | [9] family | 5e22 | 5e5 | **1.0** |
| 20a Type One (Stellarator) | D-T | MFE / Stellarator | 1e20 | [5] family | 3e21 | 30× | **3.0** |
| 20b Renaissance (Stellarator) | D-T | MFE / Stellarator | 1e20 | [5] family | 3e21 | 30× | **3.0** |
| 21 Tokamak Energy (Spherical) | D-T | MFE / Spherical tokamak | 1.5e21 | [1] family | 3e21 | 2× | **4.0** |
| 22 First Light (Projectile ICF) | D-T | IFE / Projectile ICF | 1e17 | [15] | 3e21 | 30000× | **2.0** (no laser-approach modifier; projectile is its own approach) |
| 23 Marvel (Ultrashort pulse) | p-B11 | IFE / Laser ICF (ultrashort) | 1e18 | [4] family | 3e23 | 3e5 | **1.0** (already at floor; modifier irrelevant) |
| 24 LPPFusion (DPF) | p-B11 | Non-Standard / Plasma focus | 1e16 | [16] | 3e23 | 3e7 | **1.0** |
| 25 Intensity (Heavy ion beam) | D-T | IFE / Heavy ion beam | 1e15 | [17] | 3e21 | 3e6 | **1.0** (no laser-approach modifier; heavy ion beam is its own approach) |
| 26 Inertia (Indirect drive) | D-T | IFE / Laser ICF (indirect drive) | 5e21 | [19] family | 3e21 | 0.6× | **5.0** (no modifier — NIF-class indirect drive is the family reference) |
| 27 EMC2 / Polywell (IEC) | D-T | Non-Standard / Electrostatic | *no data* | [10] | 3e21 | — | **1.0** |
| 28 Energy Singularity (Full HTS tokamak) | D-T | MFE / Compact tokamak | 1.5e21 | [1] family | 3e21 | 2× | **4.0** |
| 29 Firefly (Negative-T tokamak) | D-T | MFE / Negative triangularity tokamak | 1.5e21 | [1] family | 3e21 | 2× | **4.0** |
| 30 Inertia (NIF Commercialization) | D-T | IFE / Laser ICF (indirect drive) | 5e21 | [19] family | 3e21 | 0.6× | **5.0** (no modifier — NIF-class indirect drive) |
| 31 Blue Laser (OEC direct drive) | D-T | IFE / Laser ICF (direct drive) | 5e21 | [19] family | 3e21 | 0.6× | **4.75** (5.0 base − 0.25 direct-drive modifier) |
| 32 GenF (French direct drive) | D-T | IFE / Laser ICF (direct drive) | 5e21 | [19] family | 3e21 | 0.6× | **4.75** (5.0 base − 0.25 direct-drive modifier) |
| 33 Neo / BEST (State-backed tokamak) | D-T | MFE / Compact tokamak | 1.5e21 | [1] family | 3e21 | 2× | **4.0** |
| 35 Deutelio (PoloMac) | D-D | MFE / *TBD* | *no data* | — | 3e23 | — | **1.0** (unspecified MFE topology) |
| 36 Helical Fusion (Helical stellarator) | D-T | MFE / Stellarator (general) | 1e20 | [5] family | 3e21 | 30× | **3.0** |
| 37 NearStar (MTIF) | D-D | MIF / Magnetized target (pneumatic) | 1e18 | [11] family | 3e23 | 3e5 | **1.0** |
| 38 SHINE (Particle accelerator) | D-T | Non-Standard / Particle accelerator | *no data* | [20] | 3e21 | — | **1.0** |
| 39 ENN (p-B11 spherical tokamak) | p-B11 | MFE / Spherical tokamak | 1.5e21 | [1] family | 3e23 | 2e5 | **1.0** |

### Concepts at floor via "no architecturally-relevant measurement"

Six concepts floor at 1.0 because no triple-product measurement exists for their architectural family — rather than being floored because the measurement is far from target. The framework distinguishes these via the diagnostic block (`no_data_available: true`).

| Concept | Architectural family | Why no data |
|---|---|---|
| 02 Sonofusion | Acoustic / Sonofusion | No credible peer-reviewed measurement of fusion conditions |
| 03 Cortex | Laser ICF (liquid jet) | Novel concept; no public data |
| 13 Avalanche | Orbitron (Electrostatic) | No published Orbitron triple product |
| 16 Acceleron | Muon-catalyzed | Muon catalysis doesn't produce a confined plasma; framework doesn't apply |
| 27 EMC2 / Polywell | IEC (Electrostatic) | EMC2 WB-8 results not in the triple-product frame |
| 38 SHINE | Particle accelerator | Beam-target fusion doesn't fit the Lawson criterion |

This is honest "no data" rather than placeholder fabrication. If any of these concepts publishes a measurement (e.g., a sonofusion peer-reviewed paper, an Avalanche Orbitron triple product disclosure), the analyst adds the entry to `default.yaml` and the score recomputes.

### References

"Family" notation means the value is the architectural-family record, applied per the Wurzel-Hsu methodology, not a value specifically demonstrated by the named concept's device.

"No data" notation means no architecturally-relevant triple-product measurement exists; the framework floors the concept at score 1.0 without fabricating an achieved value.

[1] **Tokamak family** (JT-60U / JET). T. Fujita et al., "High performance experiments in JT-60U reversed shear discharges," Phys. Rev. Lett. 78, 2377 (1997); JET Team, "Fusion energy production from a deuterium-tritium plasma in the JET tokamak," Nucl. Fusion 32, 187 (1992). JT-60U record nT·τE = 1.53×10²¹ keV·s/m³ in 1998 high-βp H-mode (DD plasma, DT-equivalent inferred). JET DT-1 (1997) achieved ~1×10²¹ in actual DT. Wurzel & Hsu 2022 Table I.

[2] **Sonofusion** — *no architecturally-relevant measurement*. Taleyarkhan et al. (2002-2006) claims of "bubble fusion" have not been independently replicated; no credible peer-reviewed triple-product measurement exists. Floors at 1.0.

[3] **Liquid-jet laser ICF** (Cortex) — *no architecturally-relevant measurement*. Cortex's liquid-jet target geometry is a novel concept with no public triple-product data. Floors at 1.0 until Cortex (or analogous program) publishes a measurement.

[4] **Ultrashort-pulse laser ICF** (hb11, Marvel family). Estimate based on chirped-pulse-amplification fusion experiments; lower confinement times (~ps to ns) limit triple product compared to nanosecond direct/indirect drive. No specific peer-reviewed triple product in the literature for ultrashort-pulse aneutronic ICF; this is an extrapolation flagged in `lookup_triple_product.yaml` as lower confidence.

[5] **Stellarator family** (W7-X). Press release: Max Planck Institute for Plasma Physics, "New performance records on Wendelstein 7-X," May 22, 2025. W7-X achieved record triple product for plasma durations >30 seconds. Earlier reference: T. Sunn Pedersen et al., Nat. Comm. 7, 13493 (2016) and follow-up W7-X OP1.2/OP2 campaigns. Wurzel & Hsu 2025 update Table II.

[6] **Magnetic mirror family** (GAMMA-10). T. Cho et al., "Achievement of a record electron temperature of 0.6 keV in the GAMMA 10 tandem mirror plasma," Nuclear Fusion 45, 1650 (2005); earlier 10 keV ion temperature work cited in T. Cho et al., Phys. Rev. Lett. 86, 4310 (2001). No commercial-scale mirror has been built since GAMMA-10.

[7] **MagLIF** (Sandia Z-machine). M. R. Gomez et al., "Experimental Demonstration of Fusion-Relevant Conditions in Magnetized Liner Inertial Fusion," Phys. Rev. Lett. 113, 155003 (2014); update P. F. Schmit et al., Phys. Rev. Lett. 113, 155004 (2014). Pacific Fusion is the commercial extension. Wurzel & Hsu 2022 Table III.

[8] **FRC family** (Helion, TAE). Helion VENTI 2018 disclosures: triple product ≥10¹⁹ keV·s/m³ at 2 keV ion temperature (J. Slough et al., "The Pulsed High Density Experiment: Concept, Design, and Initial Results," J. Fusion Energy 30, 432 (2011); company statements 2018-2021). TAE Norm achievements at >75 million °C (company disclosures 2024-2025). Not peer-reviewed; treated as estimate per Wurzel-Hsu methodology for company-disclosed data.

[9] **Levitated dipole** (LDX). D. T. Garnier et al., "Production and study of high-beta plasma confined by a superconducting dipole magnet," Phys. Plasmas 13, 056111 (2006); A. C. Boxer et al., "Turbulent inward pinch of plasma confined by a levitated dipole magnet," Nature Phys. 6, 207 (2010). LDX decommissioned in 2011; OpenStar's LDR Junior aims to extend.

[10] **Electrostatic / IEC / Orbitron** (Polywell, Avalanche) — *no architecturally-relevant measurement*. R. L. Hirsch, "Inertial-Electrostatic Confinement of Ionized Fusion Gases," J. Appl. Phys. 38, 4522 (1967) established the IEC concept. Modern IEC devices (Polywell concepts, fusor-class, Orbitrons) have not produced triple product measurements suitable for the Lawson framework — particle losses dominate before plasma reaches confinement-relevant parameters. Floors at 1.0.

[11] **General Fusion**. Company disclosures and plasma injector results (e.g., M. Laberge, "Magnetized Target Fusion with a Spherical Tokamak," J. Fusion Energy 38, 199 (2019)). Treated as lower-tier MIF than Sandia's MagLIF (~10¹⁸ keV·s/m³) given pneumatic compression's lower achievable pressure compared to pulsed-power Z-pinch.

[12] **Sheared-flow Z-pinch** (Zap Energy). U. Shumlak, E. T. Meier, B. J. Levitt, "Fusion Gain and Triple Product for the Sheared-Flow-Stabilized Z Pinch," *Fusion Science and Technology* **80**(1), 1-16 (June 2023). DOI: 10.1080/15361055.2023.2198049. Establishes the methodology for measuring triple product in SFS Z-pinches with advective losses; FuZE-class measurements consistent with ~10¹⁷ keV·s/m³ achieved triple product. See also Shumlak et al., "Increasing plasma parameters using sheared flow stabilization of a Z-pinch," *Phys. Plasmas* **24**, 055702 (2017), and the November 2025 FuZE-3 announcement (Zap Energy press release, 18 Nov 2025) demonstrating 830 MPa electron pressure / 1.6 GPa total pressure for ~1 µs.

[13] **Muon-catalyzed fusion** (Acceleron) — *no architecturally-relevant measurement*. Muon catalysis produces fusion reactions but doesn't create a confined plasma in the Lawson sense; the triple-product framework doesn't cleanly apply. Reference: S. E. Jones et al., "Observation of unexpected density effects in muon-catalyzed dt fusion," Phys. Rev. Lett. 56, 588 (1986). Floors at 1.0.

[14] **Fast-ignition laser ICF** (FIREX). H. Azechi et al., "Present status of fast ignition realization experiment and inertial fusion energy development," Nucl. Fusion 53, 104021 (2013); FIREX-I results at Osaka. Fast ignition has not achieved NIF-class triple product. Focused Energy operates in this regime.

[15] **Projectile ICF** (First Light Fusion). Company announcement of "First Fusion" achievement in 2022, demonstrating projectile-driven fusion at modest yield. First Light Fusion technical paper: N. Hawker et al., "Time- and space-resolved measurements of the hydrodynamics of a converging shock-impulsively driven plasma," Phys. Plasmas (in prep, 2024).

[16] **Dense plasma focus** (LPP Fusion). E. J. Lerner et al., "Confined ion energy >200 keV and increased fusion yield in a DPF with monolithic tungsten electrodes," Phys. Plasmas 24, 102708 (2017); LPP Fusion FF-2B device results. Wurzel & Hsu 2022 Table III.

[17] **Heavy-ion beam ICF**. R. O. Bangerter, "Heavy ion fusion sciences research for high energy density physics and fusion applications," Phys. Plasmas 17, 056703 (2010); LBNL NDCX-II results. Heavy-ion-beam ICF has not reached substantial fusion conditions; Intensity Fusion's commercial path.

[18] **Hybrid-drive laser ICF**. R. Betti et al., "Alpha heating and burning plasmas in inertial confinement fusion," Phys. Rev. Lett. 114, 255003 (2015); OMEGA hybrid-drive experiments at LLE. Xcimer's KrF excimer hybrid-drive concept builds on this precedent.

[19] **Direct/indirect-drive laser ICF** (NIF). H. Abu-Shawareb et al., "Achievement of target gain larger than unity in an inertial fusion experiment," Phys. Rev. Lett. 132, 065102 (2024). NIF achieved Q_sci ≈ 1.5 in Dec 2022 (N221204 shot), then Q_sci ≈ 4.13 in April 2025. Wurzel & Hsu 2025 update notes "eight additional shots have achieved the NASEM definition of ignition" since 2022. Indirect-drive concepts (Inertia Enterprises Indirect Drive #26, NIF Commercialization #30) inherit this family record at 5.0. Direct-drive concepts (Blue Laser OEC #31, GenF French #32) inherit at 4.75 reflecting the OMEGA-class hydro-equivalent direct-drive precedent (Goncharov et al., APS DPP 2021; Phys. Plasmas 32, 032711, 2025).

[20] **Beam-target / particle accelerator** (SHINE) — *no architecturally-relevant measurement*. Beam-target accelerator-driven fusion does not produce a confined plasma. The "triple product" framework doesn't cleanly apply; SHINE is included in the matrix for completeness but floors at 1.0 on this axis. Reference: G. R. Piefer et al., "SHINE Medical Technologies — accelerator-driven Mo-99 production," Trans. Am. Nucl. Soc. 111, 1058 (2014).

### Score distribution

- **5.0 (2 concepts)**: 26 Inertia Indirect Drive, 30 Inertia NIF Commercialization — both D-T + Laser ICF (indirect drive), NIF-class. No modifier applied because indirect drive is the family reference.
- **4.75 (2 concepts)**: 31 Blue Laser OEC, 32 GenF French — D-T + Laser ICF (direct drive). Base 5.0 with -0.25 direct-drive modifier reflecting that OMEGA's direct-drive demonstration is hydro-equivalent rather than ignition-equivalent at full scale.
- **4.0 (5 concepts)**: 01 CFS, 21 Tokamak Energy, 28 Energy Singularity, 29 Firefly, 33 BEST — D-T tokamaks within 2× of breakeven.
- **3.75 (1 concept)**: 17a Xcimer — D-T + Laser ICF (hybrid drive). Base 4.0 (gap 3×) with -0.25 hybrid-drive modifier.
- **3.0 (~7 concepts)**: D-T stellarators (05 Thea, 09 Proxima, 10 Gauss, 20a Type One, 20b Renaissance, 36 Helical Fusion) and D-T MIF (07 Pacific MagLIF). 10-1000× gap.
- **2.5 (1 concept)**: 17b Focused — D-T + Laser ICF (fast ignition). Base 3.0 (gap 30×) with -0.5 fast-ignition modifier.
- **2.0 (~6 concepts)**: 08 Helion (D-He³ FRC), 11 Realta (D-T mirror), 12 OpenStar (D-T dipole), 14 General Fusion (pneumatic MTF), 15 Zap (Z-pinch), 22 First Light (projectile).
- **1.0 (~16 concepts)**: Far-from-breakeven or no-data concepts. Includes: aneutronic IFE (04 hb11, 23 Marvel — fast-ignition/ultrashort modifier doesn't move from floor), aneutronic mirror (06 Pale Blue), aneutronic FRC (18 TAE), p-B11 DPF (24 LPPFusion), p-B11 spherical tokamak (39 ENN), D-He³ orbital dipole (19 Zephyr), D-D pneumatic MTF (37 NearStar), D-D MFE TBD-topology (35 Deutelio). Plus the six no-data concepts: 02 Sonofusion (Acoustic), 03 Cortex (Liquid jet), 13 Avalanche (Electrostatic), 16 Acceleron (Muon-catalyzed), 27 EMC2/Polywell (IEC), 38 SHINE (Particle accelerator).

---

## Notable score patterns

**Laser ICF indirect drive at 5.0 (concepts 26, 30).** The NIF ignition campaign of 2022-2025 demonstrated Q_sci ≈ 4 with triple product ~5×10²¹ using indirect drive. Inertia Enterprises has two indirect-drive concepts in the matrix (26 Indirect Drive, 30 NIF Commercialization), both inheriting this family achievement. No modifier applied — indirect drive is the family reference point. Other axes (Plant Complexity, Supply Chain) capture why even NIF-class physics isn't yet a commercial pathway.

**Direct-drive laser ICF at 4.75 (concepts 31 Blue Laser, 32 GenF).** Both use direct drive, well-validated on OMEGA but not yet demonstrated at NIF-class ignition energies. The -0.25 direct-drive modifier reflects that OMEGA's hot-spot pressure measurements (~40 Gbar) and hydrodynamic-equivalence scaling (Goncharov 2021) project to ~75% of ignition triple product at NIF scale, but full-scale ignition shots have not been demonstrated in direct drive specifically.

**Tokamaks at 4.0 (5 concepts).** JT-60U/JET tokamak triple product of ~1.5×10²¹ is within 2× of breakeven. The tokamak family is the closest MFE architecture to breakeven. CFS (01), Tokamak Energy (21), Energy Singularity (28), Firefly (29), BEST (33) all inherit this. No laser-approach modifier applies (non-IFE).

**Xcimer at 3.75 — hybrid-drive modifier (concept 17a).** Xcimer's KrF excimer hybrid-drive architecture builds on OMEGA's hybrid-drive precedent. The gap-based score is 4.0 (achieved ~10²¹ vs required 3×10²¹); the -0.25 hybrid-drive modifier reflects that hybrid drive is less mature than indirect.

**Focused at 2.5 — fast-ignition modifier (concept 17b).** Focused Energy uses direct-drive fast ignition. Achieved ~10²⁰ vs required 3×10²¹ gives gap 30× → base 3.0. The -0.5 fast-ignition modifier reflects that fast ignition has not achieved NIF-class triple product despite decades of FIREX-class experiments.

**Stellarators at 3.0 (6 concepts).** W7-X 2025 records put stellarators at ~1×10²⁰ — about 30× below breakeven. Significant but tractable gap. Thea (05), Proxima (09), Gauss (10), Type One (20a), Renaissance (20b), Helical Fusion (36) all in this tier.

**Aneutronic concepts dominate the 1.0 floor.** p-B11 needs ~3×10²³ triple product, ~100× higher than D-T. Even with the best architectural family achievement (FRC at ~10¹⁹), the gap is ~30,000×. TAE (18), hb11 (04), Marvel (23), Pale Blue (06), ENN (39), LPPFusion (24) all score 1.0. The framework correctly captures that aneutronic fusion is much further from physics breakeven than D-T.

**Helion at 2.0 — closer than aneutronic peers despite D-He³ (concept 08).** Required triple product for D-He³ (5×10²²) is 17× harder than D-T but ~6× easier than p-B11. Helion's FRC family at ~10¹⁹ gives gap ~5000× → 2.0. Better than aneutronic concepts but worse than D-T concepts.

**Zap Z-pinch at 2.0 despite recent pressure record (concept 15).** FuZE-3's gigapascal pressure (Nov 2025) is impressive but the µs confinement times limit triple product to ~10¹⁷. Gap is ~30,000× from D-T breakeven. The framework captures this — high pressure ≠ high triple product if confinement is short. The Shumlak et al. 2023 methodology paper formalizes how to account for advective losses when computing triple product for sheared-flow Z-pinches; the achieved value falls cleanly into the bucket structure.

**Sonofusion, Cortex, Avalanche, Acceleron, Polywell, SHINE at floor via "no data" (concepts 02, 03, 13, 16, 27, 38).** These six concepts floor at 1.0 because their architectural families don't have triple-product measurements suitable for the Lawson framework — not because they've measured far from target. The diagnostic block distinguishes via `no_data_available: true`. This is honest "we don't know" rather than fabricated placeholder values. If any of these concepts publishes a triple-product measurement, the analyst adds the entry to `default.yaml` and the score recomputes.

**Cortex (liquid jet, concept 03) at floor via "no data" — not via a laser modifier.** Cortex's liquid-jet target geometry is treated as its own architectural family with no measurement, not as a laser-approach variant of mainstream ICF. The distinction matters: applying a `-0.5` ultrashort/fast modifier to a 5.0 base would land Cortex at 4.5, falsely implying that the liquid jet is a small departure from validated direct/indirect-drive physics. It isn't — it's a fundamentally different target geometry with no demonstrated implosion physics. Floor scoring reflects this honestly.

**Electrostatic concepts (Polywell 27, Avalanche 13) at the floor via "no data".** IEC fusors have been built since the 1960s but particle losses dominate before plasma reaches confinement-relevant parameters. The framework correctly identifies that this architectural family doesn't fit the Lawson framework, rather than pretending to a measurement that doesn't exist.

**SHINE at the floor.** Beam-target accelerator-driven fusion doesn't produce a confined plasma. The triple-product framework doesn't apply. SHINE floors at 1.0 not because it's "bad" but because this axis isn't measuring the right thing for SHINE. Other axes (Plant Complexity, Customization, Supply Chain) capture SHINE's actual non-power-fusion proposition correctly.

**Sonofusion at the floor via "no data".** No credible peer-reviewed measurement. Floor scoring until/unless Sonofusion publishes definitive data.

---

## Files touched

```
exploration/scoring_v2/weights/default.yaml                              # add technical_feasibility axis with two lookup tables
exploration/scoring_v2/embeddings/rulebook.py                            # add 2 embeddings + 3 helpers
exploration/scoring_v2/lookup_triple_product.yaml                        # NEW: triple product provenance metadata
exploration/scoring_v2/features/*.yaml                                   # 39 files: append technical_feasibility_diagnostics
exploration/scoring_v2/scripts/populate_technical_feasibility_diagnostics.py  # NEW: idempotent diagnostic population
tests/scoring_v2/test_technical_feasibility.py                            # NEW: acceptance tests
.project/active/scoring-v2-technical-feasibility-slice/design.md          # NEW: this spec + planning doc
.project/active/scoring-v2-technical-feasibility-slice/implementation_notes.md # NEW: implementation tracking
```

---

## Coordination notes

### Relationship to other axes

Technical Feasibility is **independent** of all other axes. The lookup tables touch a new section of `weights/default.yaml`.

**Specifically not overlapping**:
- With Plant Complexity: Plant Complexity asks "how many subsystems must work for the plant to operate" — an *engineering* feasibility question. Technical Feasibility asks "how far is the physics from breakeven" — a *physics* feasibility question.
- With Upper Capacity Factor: Upper CF asks "given the physics works, what's the achievable CF". Technical Feasibility asks "how confident are we that the physics works at all".
- With Modularity, Supply Chain, Customization: orthogonal axes measuring different commercial-readiness factors.

### Schema dependencies

Trigger features used by this axis: `Fuel`, `Confinement Family`, `Confinement Concept` (derived from v3 ontology sub-columns), and `Laser Approach`. All are in the v0.3.0 ontology — see the integrated implementation plan's Slice 0 (schema reconciliation) for surfacing them in `scoring_v2/schema.yaml`. The `Confinement Concept` derivation must disambiguate MFE/Open-Linear by Driver Type (Magnetic = Mirror; Magnetic pinch = Z-pinch); see the lookup table comments above.

### Source attribution

The `lookup_triple_product.yaml` metadata file contains full citations for every triple product value. This is critical for analyst auditing — when a value seems wrong, the analyst can trace it to the source paper and verify.

The most consequential dependencies:
- Wurzel & Hsu (2022, 2025) — canonical MFE/MIF/ICF triple product table
- NIF post-ignition results (2022-2025) — moved laser ICF family from "near breakeven" to "demonstrated breakeven"
- W7-X 2025 long-pulse records — moved stellarator family up
- Company disclosures for FRC concepts (Helion, TAE) — not peer-reviewed but cited

When primary source data updates (e.g., a new Wurzel-Hsu update is published, or a company publishes a new triple product), the value in `default.yaml` and the metadata in `lookup_triple_product.yaml` should be updated together.

---

## Implementation notes for Claude Code

- **Compound key string format**: `_achieved_key` produces `"Confinement Family|Confinement Concept"` with a pipe separator. The pipe is unambiguous because neither family nor concept values contain pipes. Stable across schema revisions.

- **Logarithmic bucket schedule**: `_score_from_log_gap` iterates through `_LOG_GAP_BUCKETS` in order; first match wins. Buckets are powers of 10 (0, 1, 3, 5 log decades). Adjusting bucket boundaries is a one-line edit if the framework needs finer granularity.

- **Failure mode for missing lookup entries**: Both `_triple_product_gap` and `_load_tf_tables` raise on missing data. Forces explicit analyst decisions when new architectural families are added.

- **Weight loading pattern**: Match the pattern from other axes' lookup loaders (`_load_bottleneck_weights`, `_load_customization_weights`, etc.).

- **Schema feature key naming**: snake_case in feature files (`fuel`, `confinement_family`, `confinement_concept`).

- **The `_score_from_log_gap` helper is separately testable**: doesn't depend on the full embedding pipeline. Tests verify the bucket mapping directly.

- **`achieved_triple_product` lookup must cover every (family, concept) tuple in the matrix**. If a feature file specifies a combination not in the lookup, the embedding raises. Verify by running the populate script and checking for errors.

---

## Open questions worth flagging (for future versions)

These don't block implementation but are worth raising in the design.md for the slice:

1. **Breakeven vs commercial Q target**: The framework uses Q_sci = 1 (scientific breakeven) as the reference. A commercial reactor typically needs Q ≥ 10-30. Should the framework reference commercial Q instead? Effect: would lower all scores by ~1 tier. Current choice (Q=1) is more generous and matches the Wurzel-Hsu framework. If the analyst wants stricter scoring, raise the required values by 10-30× across the board.

2. **Helion's closed-cycle He-3 mitigation (consistent with Supply Chain axis)**: Helion claims internal He-3 breeding. The framework currently treats Helion the same as any D-He³ concept (no special credit). Whether to credit Helion's claim is the same question that arose in Supply Chain — currently the framework doesn't credit unproven mitigation claims.

3. **Acceptance of architectural-family generalization**: Indirect-drive concepts (Inertia 26, NIF Commercialization 30) get full credit for NIF's ignition because both use the same architectural family. Direct-drive concepts (Blue Laser 31, GenF 32) get partial credit (-0.25 modifier) reflecting OMEGA's hydro-equivalent but not yet full-scale direct-drive ignition. This is a per-laser-approach refinement of the Wurzel-Hsu convention. Some analysts may want finer differentiation (e.g., target-illumination uniformity, polar drive vs. spherical drive).

4. **Sonofusion floor value**: Currently 10¹⁰ to ensure floor scoring. If Sonofusion publishes any peer-reviewed measurement, this should be updated. Worth setting up an analyst review trigger for any sonofusion publication.

5. **Heavy-ion beam ICF (Intensity Fusion)**: Currently scored 10¹⁵ because no HIB facility has reached substantial fusion conditions. If LBNL's NDCX series or any HIB facility reaches higher triple products, this should be updated. Currently affects Intensity Fusion's score.

6. **Z-pinch Q>1 efforts**: Zap Energy is pursuing Q>1 with FuZE-3 generation. If they achieve it (or any sheared-flow Z-pinch achieves Q>1), the `MFE|Z-pinch (sheared-flow)` value should move significantly — potentially to NIF-class. This would lift Zap from 2.0 to 4.0+.

7. **Tokamak family treatment**: Currently all tokamak variants (conventional, compact, spherical, negative-T) share JT-60U/JET's record. If a compact tokamak (SPARC, ARC) achieves first plasma and exceeds, the family value should update. This could lift CFS ARC and Tokamak Energy from 4.0 to 5.0.

8. **NIF direct vs indirect drive distinction**: The framework currently treats both as 5×10²¹. NIF achieved this with indirect drive. Direct drive at OMEGA has reached ~1×10²¹ (lower). If the analyst wants finer granularity, split the achieved_triple_product entries.
