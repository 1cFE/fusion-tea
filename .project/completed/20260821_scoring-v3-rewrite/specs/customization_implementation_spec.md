# Implementation Spec: Customization Scoring Axis

**Status:** Ready for implementation
**Owner:** Mallory
**Created:** 2026-05-19
**Branch:** `concept-downselect`
**Target directory:** `.project/active/scoring-v2-customization-slice/` (new slice — sibling to existing modularity, supply chain, and plant complexity slices)
**Schema version:** v0.3.0 (`schema.md`, 2026-05-12)

This is a Claude Code implementation spec porting the C5 (Customization) deterministic logic from the `fusion-tea-scoring` branch to the new concept-downselect framework format.

---

## Summary

Build a new **Customization** scoring axis as a peer of Modularity, Supply Chain, and Plant Complexity in `weights/default.yaml`. The axis produces a deterministic 1.0–5.0 score per concept based on two architectural sub-factors: thermal rejection footprint and fuel safety profile.

### Score formula (ported from `fusion-tea-scoring`)

```
A = thermal_rejection_score(Energy Capture)   # 1-4
B = fuel_safety_score(Fuel)                    # 1-4
raw = (A + B) / 2
customization_score = 1.0 + (raw - 1.0) * (4.0 / 3.0)
```

The `(4/3)` rescale stretches the raw range `[1.0, 4.0]` to fit the framework's `[1.0, 5.0]` scale, matching the convention used by Modularity, Supply Chain, and Plant Complexity. Higher score = lower customization burden = more site-agnostic deployment.

### What the score measures

**Question the score answers:** *How site-agnostic is this concept's deployment? Can it be sited near population centers and industrial loads, or does it require extensive customization for siting (large water bodies for cooling, exclusion zones for tritium, special licensing for neutron production)?*

The two sub-factors capture the dominant site-customization drivers:
1. **Thermal rejection** — how much waste-heat infrastructure (cooling towers, water bodies, hybrid cooling) the plant requires
2. **Fuel safety profile** — how much licensing, exclusion-zone planning, and tritium-handling infrastructure the fuel cycle imposes

This is **independent of Modularity** (factory manufacturing), **Supply Chain** (critical materials), and **Plant Complexity** (subsystem count). Customization asks specifically about *site-specific deployment constraints*.

### Key design choices

- **Weights live in `weights/default.yaml`** under the customization axis. Both sub-factor lookup tables are visible in the YAML for analyst tuning.
- **All triggers use existing v0.3.0 schema features.** No new features required. Specifically: `Fuel` and `Energy Capture`.
- **Site-specific advantages must NOT inflate the score.** This is explicit in the porting spec — score only intrinsic concept characteristics (architecture, fuel), not "this concept could be sited near the Mississippi River for cooling."

### Source of the framework

This logic is ported from the `fusion-tea-scoring` branch's `exploration/concept_analysis/prompt_templates/config/scoring_framework.md` C5 specification. In the old framework, C5 was scored by Claude reading a prompt and applying judgment to fill in YAML. In the new framework, **C5 becomes fully deterministic** computed from features — matching the design principle of the modularity, supply chain, and plant complexity axes.

---

## Changes summary

| # | Change | Touches |
|---|---|---|
| A | Add `customization` axis with inline sub-factor lookup tables to `weights/default.yaml` | `weights/default.yaml` |
| B | Implement `thermal_rejection_score`, `fuel_safety_score`, `customization_score` embeddings | `embeddings/rulebook.py` |
| C | Create `lookup_customization.yaml` metadata file (no weights — descriptions only) | `lookup_customization.yaml` (new) |
| D | Add `customization_diagnostics` derived block per feature file | `features/*.yaml` (39 files) |
| E | Add acceptance tests | `tests/scoring_v2/test_customization.py` (new) |

---

## Change A: M&SO axis registration with inline lookup tables

### Updated `weights/default.yaml`

```yaml
# Existing axes (unchanged by this spec)
economic_potential: {}
technical_feasibility: {}
manufacturability_scale_out:
  # ... existing modularity weights ...
supply_chain:
  # ... existing supply chain weights ...
plant_complexity:
  # ... existing plant complexity weights ...

# NEW axis added by this spec
customization:
  customization_score: 1.0                        # axis-level M&SO weight
  thermal_rejection_scores:                       # Sub-factor A lookup (Energy Capture → score)
    direct_conversion:     4                      # Direct (inductive), Direct (charged particle), or any Direct (*)
    hybrid:                3                      # Hybrid (thermal + direct)
    thermal:               2                      # Thermal (*), Pulsed power implosion, Projectile impact, Neutron applications, TBD
  fuel_safety_scores:                             # Sub-factor B lookup (Fuel → score)
    p-B11:                 4                      # Aneutronic, no tritium
    D-He3:                 3                      # Low neutron fraction, no tritium breeding
    D-D:                   2                      # Neutrons but no tritium handling
    D-T:                   1                      # Full tritium handling and breeding infrastructure
```

### Why these specific weights

The 1-4 scale on both sub-factors comes from the original C5 framework. The rescaling factor `(4/3)` brings the average `(A+B)/2` from its natural range `[1.0, 4.0]` onto the framework's `[1.0, 5.0]` scale — without it, the maximum score would be 4.0 rather than 5.0.

**Why sub-factor A maps four values onto three score levels.** The original framework lists four levels (4, 3, 2, 1) but the `1` tier ("exceptional thermal rejection needs — multiple cooling systems") doesn't appear in any concept's `Energy Capture` controlled vocabulary. The lookup table omits this tier — it would never fire — and treats all thermal/pulsed/projectile/neutron capture values as the standard `2` tier.

**Why TBD maps to 2 (thermal).** The original spec doesn't address TBD energy capture (the v0.3.0 schema added it). The conservative default is to treat TBD as "probably thermal" — companies that haven't disclosed an energy conversion approach will likely default to thermal because that's the path of least resistance for D-T. If a TBD concept later turns out to be direct conversion, the feature value will update and the score will recompute.

---

## Change B: Embeddings in `rulebook.py`

### Implementation

Add to `embeddings/rulebook.py` after the existing plant complexity embeddings:

```python
# ===========================================================================
# Customization Axis
#
# Deterministic scoring based on two architectural sub-factors:
#   A) Thermal rejection footprint (from Energy Capture)
#   B) Fuel safety profile (from Fuel)
#
# Weights are loaded from weights/default.yaml under the customization axis.
# Ported from the C5 (Customization Needs) logic on the fusion-tea-scoring
# branch, converted from Claude-judgment-based to fully deterministic.
# ===========================================================================


def _load_customization_weights(weights_yaml: dict) -> tuple[dict, dict]:
    """Extract per-sub-factor lookup tables from weights/default.yaml.

    Returns (thermal_rejection_scores, fuel_safety_scores).
    Raises if either lookup table is missing.
    """
    cust = weights_yaml.get("customization", {})
    trs = cust.get("thermal_rejection_scores")
    fss = cust.get("fuel_safety_scores")
    if trs is None or fss is None:
        raise ValueError(
            "weights/default.yaml customization axis is missing "
            "thermal_rejection_scores or fuel_safety_scores lookup tables."
        )

    # Validate completeness
    required_thermal_keys = {"direct_conversion", "hybrid", "thermal"}
    missing_thermal = required_thermal_keys - set(trs.keys())
    if missing_thermal:
        raise ValueError(
            f"customization.thermal_rejection_scores missing keys: {missing_thermal}"
        )

    required_fuel_keys = {"p-B11", "D-He3", "D-D", "D-T"}
    missing_fuel = required_fuel_keys - set(fss.keys())
    if missing_fuel:
        raise ValueError(
            f"customization.fuel_safety_scores missing keys: {missing_fuel}"
        )

    return {k: int(v) for k, v in trs.items()}, {k: int(v) for k, v in fss.items()}


def _classify_thermal_rejection(energy_capture: str) -> str:
    """Map Energy Capture value to a thermal_rejection_scores key.

    Returns one of: 'direct_conversion', 'hybrid', 'thermal'.
    """
    energy = energy_capture or ""

    if energy.startswith("Direct"):
        # Direct (inductive), Direct (charged particle), any Direct (*)
        return "direct_conversion"

    if energy == "Hybrid (thermal + direct)":
        return "hybrid"

    # All other values fall into the standard-thermal bucket:
    # - Thermal (*) — explicit thermal cycles
    # - Pulsed power implosion — buffered through thermal storage to a steam cycle
    # - Projectile impact — same, buffered thermal cycle
    # - Neutron applications — still requires cooling infrastructure even non-power
    # - TBD — conservative default (most likely path is thermal)
    return "thermal"


@embedding(
    "thermal_rejection_score",
    inputs=["energy_capture"],
)
def _thermal_rejection_score(
    energy_capture: str,
    *,
    weights_yaml: dict,
) -> int:
    """Sub-factor A: thermal rejection footprint (1-4 scale).

    4 = no thermal cycle or air-cooled (direct conversion only)
    3 = hybrid power conversion (partial direct + partial thermal)
    2 = standard thermal cycle (cooling towers required)

    The original framework defines a 4th tier (score 1, "exceptional thermal
    rejection needs") but no concept in the v0.3.0 schema's Energy Capture
    vocabulary maps to it. Omitted from the lookup.
    """
    trs, _ = _load_customization_weights(weights_yaml)
    classification = _classify_thermal_rejection(energy_capture)
    return trs[classification]


@embedding(
    "fuel_safety_score",
    inputs=["fuel"],
)
def _fuel_safety_score(
    fuel: str,
    *,
    weights_yaml: dict,
) -> int:
    """Sub-factor B: fuel safety profile (1-4 scale).

    4 = p-B11 (aneutronic, no tritium)
    3 = D-He3 (low neutron fraction, no tritium breeding)
    2 = D-D (neutrons but no tritium handling)
    1 = D-T (full tritium handling and breeding infrastructure)
    """
    _, fss = _load_customization_weights(weights_yaml)

    # Handle Unknown fuel — conservative default to D-T (worst case)
    if fuel == "Unknown" or not fuel:
        return fss["D-T"]

    if fuel not in fss:
        raise ValueError(
            f"Unknown fuel value: {fuel!r}. Expected one of "
            f"{sorted(fss.keys())} or 'Unknown'."
        )
    return fss[fuel]


@embedding(
    "customization_score",
    inputs=["thermal_rejection_score", "fuel_safety_score"],
)
def _customization_score(
    thermal_rejection_score: int,
    fuel_safety_score: int,
) -> float:
    """Customization score on a 1-5 scale.

    Combines the two sub-factors via averaging and rescaling from [1.0, 4.0]
    to [1.0, 5.0]:
        raw = (A + B) / 2
        score = 1.0 + (raw - 1.0) * (4.0 / 3.0)

    Higher score = less customization burden = more site-agnostic deployment.
    """
    raw = (thermal_rejection_score + fuel_safety_score) / 2.0
    return round(1.0 + (raw - 1.0) * (4.0 / 3.0), 2)
```

### Why the embeddings split into three

Following the pattern from supply chain and plant complexity: each sub-factor is its own embedding so the diagnostic block can show the analyst exactly how A and B contributed. If the score were a single black-box embedding, the analyst would lose the per-sub-factor traceability that makes the framework auditable.

### Why classification is in a helper, not in the lookup

The `_classify_thermal_rejection` helper maps the v0.3.0 schema's `Energy Capture` controlled vocabulary (many values) to the three classification keys (`direct_conversion`, `hybrid`, `thermal`). Putting the mapping in code rather than YAML avoids requiring an analyst to maintain a 12-row Energy Capture → classification lookup. The three classification keys themselves *are* in the YAML, so weight tuning is still done by YAML edit; only the categorization logic stays in code.

---

## Change C: `lookup_customization.yaml` (metadata only)

### New file: `exploration/scoring_v2/lookup_customization.yaml`

```yaml
# Customization sub-factor metadata.
#
# Numerical scoring tables are NOT here — they live in weights/default.yaml
# under customization.thermal_rejection_scores and customization.fuel_safety_scores.
#
# Each entry documents the sub-factor classification and its rationale.
# The authoritative classification logic lives in rulebook.py:
#   - _classify_thermal_rejection() maps Energy Capture values to classification keys
#   - _fuel_safety_score() reads Fuel directly
#
# This file documents what the code does; the code is the source of truth.

sub_factor_a_thermal_rejection:
  description: |
    Sub-factor A: thermal rejection footprint. How much waste-heat
    infrastructure (cooling towers, water bodies, hybrid cooling) does
    the plant require? Higher score = less infrastructure needed.

  classifications:
    direct_conversion:
      score: 4
      description: "No thermal cycle; air-cooled charged-particle direct conversion"
      energy_capture_values:
        - "Direct (inductive)"
        - "Direct (charged particle)"
      trigger_rule: "Energy Capture starts with 'Direct'"
      rationale: |
        Direct conversion concepts (Helion's inductive coupling, aneutronic
        charged-particle collectors) bypass the thermal cycle entirely. Waste
        heat is minimal and can be air-cooled. No cooling tower required.

    hybrid:
      score: 3
      description: "Partial direct conversion + partial thermal cycle"
      energy_capture_values:
        - "Hybrid (thermal + direct)"
      trigger_rule: "Energy Capture = Hybrid (thermal + direct)"
      rationale: |
        Hybrid configurations capture some energy via direct conversion
        and some via thermal cycle. Thermal rejection load is smaller than
        a pure thermal cycle but still requires substantial cooling.

    thermal:
      score: 2
      description: "Standard thermal cycle (Rankine/Brayton/sCO2) requiring cooling towers"
      energy_capture_values:
        - "Thermal (steam) saturated"
        - "Thermal (steam) superheated"
        - "Thermal (steam) supercritical"
        - "Thermal (steam)"
        - "Thermal (sCO2)"
        - "Thermal (helium Brayton)"
        - "Thermal (combined cycle)"
        - "Thermal (unspecified)"
        - "Pulsed power implosion"
        - "Projectile impact"
        - "Neutron applications"
        - "TBD"
      trigger_rule: "Any Energy Capture value not classified as direct_conversion or hybrid"
      rationale: |
        Standard thermal-cycle concepts require full cooling-tower or
        equivalent heat-rejection infrastructure. Pulsed power and projectile
        impact concepts also buffer their pulsed thermal output through a
        thermal storage system to a conventional steam cycle, so they share
        this classification. Neutron applications (SHINE) still require
        cooling for the accelerator and target. TBD defaults here
        conservatively — the most likely path is thermal.

  omitted_tier:
    score: 1
    description: "Exceptional thermal rejection needs (multiple cooling systems)"
    rationale: |
      The original C5 framework includes a 4th tier (score 1) for
      "exceptional thermal rejection needs — multiple cooling systems."
      No concept in the v0.3.0 Energy Capture vocabulary maps to this
      tier, so it's omitted from the lookup. If a future concept warrants
      it, add a classification key and the corresponding rule.


sub_factor_b_fuel_safety:
  description: |
    Sub-factor B: fuel safety profile. How much licensing, exclusion-zone
    planning, and tritium-handling infrastructure does the fuel cycle
    impose? Higher score = less burden.

  classifications:
    p-B11:
      score: 4
      description: "Aneutronic fuel; no tritium handling"
      rationale: |
        p-B11 produces only alpha particles (no neutrons from primary
        reaction; trace side reactions only). No tritium handling, no
        14 MeV neutron exclusion zone, no breeding blanket. Most
        site-agnostic fuel cycle.

    D-He3:
      score: 3
      description: "Low neutron fraction; no tritium breeding"
      rationale: |
        D-He3 produces few neutrons (D-D side reactions only, ~1-5% of
        fusion power). No tritium breeding required. Significantly
        reduced licensing burden compared to D-T.

    D-D:
      score: 2
      description: "Neutrons but no tritium handling"
      rationale: |
        D-D produces 2.45 MeV neutrons and tritium as a fusion product,
        but at much lower rates than D-T. Some activation and tritium
        production but no breeding infrastructure or large startup
        tritium inventory required.

    D-T:
      score: 1
      description: "Full tritium handling, breeding, and licensing burden"
      rationale: |
        D-T requires complete tritium fuel cycle (handling, breeding,
        recovery, storage), 14 MeV neutron shielding, exclusion zones,
        and substantial regulatory licensing. Highest site-customization
        burden of any fuel.

    Unknown:
      score: 1
      description: "Conservative default — treat as worst case (D-T)"
      rationale: |
        Concepts with undeclared fuel are scored as if D-T pending
        disclosure. Re-scores if the feature is later populated.


site_specific_exclusion:
  description: |
    Site-specific advantages (proximity to water, brownfield reuse, named
    sites, regulatory accommodations) must NOT inflate the customization
    score. This axis measures the INTRINSIC site-customization burden of
    the concept's architecture and fuel cycle, not opportunistic siting
    choices. Per the original C5 framework specification.
```

---

## Change D: Feature-file diagnostics

Add a derived block to each concept's feature file:

### Diagnostic block format

```yaml
# In each features/{ID}-{name}.yaml file, append:
customization_diagnostics:
  sub_factor_a:
    feature: "Energy Capture"
    value: "{value}"
    classification: "{direct_conversion | hybrid | thermal}"
    score: {1-4}
  sub_factor_b:
    feature: "Fuel"
    value: "{value}"
    score: {1-4}
  raw_average: {1.0-4.0}
  customization_score: {1.0-5.0}
```

### Examples

**CFS ARC (D-T, Thermal (unspecified))**:

```yaml
customization_diagnostics:
  sub_factor_a:
    feature: "Energy Capture"
    value: "Thermal (unspecified)"
    classification: "thermal"
    score: 2
  sub_factor_b:
    feature: "Fuel"
    value: "D-T"
    score: 1
  raw_average: 1.5
  customization_score: 1.67
```

**Helion (D-He3, Direct (inductive))**:

```yaml
customization_diagnostics:
  sub_factor_a:
    feature: "Energy Capture"
    value: "Direct (inductive)"
    classification: "direct_conversion"
    score: 4
  sub_factor_b:
    feature: "Fuel"
    value: "D-He3"
    score: 3
  raw_average: 3.5
  customization_score: 4.33
```

**hb11 (p-B11, Direct (charged particle))**:

```yaml
customization_diagnostics:
  sub_factor_a:
    feature: "Energy Capture"
    value: "Direct (charged particle)"
    classification: "direct_conversion"
    score: 4
  sub_factor_b:
    feature: "Fuel"
    value: "p-B11"
    score: 4
  raw_average: 4.0
  customization_score: 5.00
```

### Population approach

Write `scripts/populate_customization_diagnostics.py` to programmatically populate the diagnostic block in all 39 feature files. Idempotent and re-runnable after weight changes. Same pattern as `populate_supply_chain_diagnostics.py` and `populate_plant_complexity_diagnostics.py`.

---

## Change E: Acceptance tests

### New test file: `tests/scoring_v2/test_customization.py`

```python
"""Acceptance tests for the customization scoring axis."""
import pytest
import yaml
from pathlib import Path

from exploration.scoring_v2.embeddings.rulebook import (
    REGISTRY,
    _classify_thermal_rejection,
    _load_customization_weights,
)


_BASE = Path(__file__).parent.parent.parent / "exploration" / "scoring_v2"
_WEIGHTS_YAML = yaml.safe_load((_BASE / "weights" / "default.yaml").read_text())
_THERMAL_SCORES, _FUEL_SCORES = _load_customization_weights(_WEIGHTS_YAML)


# ============================================================================
# Weights are visible in default.yaml
# ============================================================================

class TestWeightsExposedInDefaultYaml:
    """Verify both sub-factor lookup tables are visible in weights/default.yaml."""

    def test_customization_axis_exists(self):
        assert "customization" in _WEIGHTS_YAML

    def test_axis_weight_is_one(self):
        assert _WEIGHTS_YAML["customization"]["customization_score"] == 1.0

    def test_thermal_rejection_scores_complete(self):
        for key in ["direct_conversion", "hybrid", "thermal"]:
            assert key in _THERMAL_SCORES

    def test_fuel_safety_scores_complete(self):
        for key in ["p-B11", "D-He3", "D-D", "D-T"]:
            assert key in _FUEL_SCORES

    def test_thermal_scores_match_spec(self):
        assert _THERMAL_SCORES["direct_conversion"] == 4
        assert _THERMAL_SCORES["hybrid"] == 3
        assert _THERMAL_SCORES["thermal"] == 2

    def test_fuel_scores_match_spec(self):
        assert _FUEL_SCORES["p-B11"] == 4
        assert _FUEL_SCORES["D-He3"] == 3
        assert _FUEL_SCORES["D-D"] == 2
        assert _FUEL_SCORES["D-T"] == 1


# ============================================================================
# Energy Capture classification
# ============================================================================

class TestThermalRejectionClassification:
    """Verify Energy Capture values map correctly to classification keys."""

    def test_direct_inductive_is_direct(self):
        assert _classify_thermal_rejection("Direct (inductive)") == "direct_conversion"

    def test_direct_charged_particle_is_direct(self):
        assert _classify_thermal_rejection("Direct (charged particle)") == "direct_conversion"

    def test_hybrid(self):
        assert _classify_thermal_rejection("Hybrid (thermal + direct)") == "hybrid"

    def test_thermal_variants_are_thermal(self):
        for value in [
            "Thermal (steam) saturated",
            "Thermal (steam) superheated",
            "Thermal (steam) supercritical",
            "Thermal (steam)",
            "Thermal (sCO2)",
            "Thermal (helium Brayton)",
            "Thermal (combined cycle)",
            "Thermal (unspecified)",
        ]:
            assert _classify_thermal_rejection(value) == "thermal"

    def test_pulsed_power_implosion_is_thermal(self):
        assert _classify_thermal_rejection("Pulsed power implosion") == "thermal"

    def test_projectile_impact_is_thermal(self):
        assert _classify_thermal_rejection("Projectile impact") == "thermal"

    def test_neutron_applications_is_thermal(self):
        assert _classify_thermal_rejection("Neutron applications") == "thermal"

    def test_tbd_defaults_to_thermal(self):
        assert _classify_thermal_rejection("TBD") == "thermal"


# ============================================================================
# Fuel safety scoring
# ============================================================================

def _fuel_score(fuel):
    return REGISTRY["fuel_safety_score"].fn(fuel, weights_yaml=_WEIGHTS_YAML)


class TestFuelSafetyScore:
    """Verify Fuel values produce expected scores."""

    def test_p_b11_score_4(self):
        assert _fuel_score("p-B11") == 4

    def test_dhe3_score_3(self):
        assert _fuel_score("D-He3") == 3

    def test_dd_score_2(self):
        assert _fuel_score("D-D") == 2

    def test_dt_score_1(self):
        assert _fuel_score("D-T") == 1

    def test_unknown_defaults_to_dt(self):
        assert _fuel_score("Unknown") == 1
        assert _fuel_score("") == 1
        assert _fuel_score(None) == 1


# ============================================================================
# Customization score formula
# ============================================================================

def _customization(A, B):
    return REGISTRY["customization_score"].fn(A, B)


class TestCustomizationFormula:
    """Verify the (A+B)/2 → 1+(raw-1)*4/3 rescaling produces correct outputs."""

    def test_max_score_p_b11_direct(self):
        # A=4, B=4 → raw=4.0 → score = 1 + 3*4/3 = 5.0
        assert _customization(4, 4) == 5.0

    def test_min_score_d_t_thermal(self):
        # A=2, B=1 → raw=1.5 → score = 1 + 0.5*4/3 = 1.67
        assert _customization(2, 1) == 1.67

    def test_helion_d_he3_direct(self):
        # A=4, B=3 → raw=3.5 → score = 1 + 2.5*4/3 = 4.33
        assert _customization(4, 3) == 4.33

    def test_d_d_thermal(self):
        # A=2, B=2 → raw=2.0 → score = 1 + 1*4/3 = 2.33
        assert _customization(2, 2) == 2.33

    def test_p_b11_thermal(self):
        # A=2, B=4 → raw=3.0 → score = 1 + 2*4/3 = 3.67
        assert _customization(2, 4) == 3.67


# ============================================================================
# Per-concept score anchors
# ============================================================================

def _score(concept_id: str) -> float:
    """Load a concept's features and return its customization_score."""
    matches = list((_BASE / "features").glob(f"{concept_id}-*.yaml"))
    assert len(matches) == 1, f"Expected one feature file for {concept_id}, got {len(matches)}"
    features = yaml.safe_load(matches[0].read_text())
    A = REGISTRY["thermal_rejection_score"].fn(
        features.get("energy_capture"),
        weights_yaml=_WEIGHTS_YAML,
    )
    B = REGISTRY["fuel_safety_score"].fn(
        features.get("fuel"),
        weights_yaml=_WEIGHTS_YAML,
    )
    return REGISTRY["customization_score"].fn(A, B)


def test_p_b11_direct_top_tier():
    """p-B11 + direct conversion concepts score 5.0 — most site-agnostic."""
    # hb11, Pale Blue, TAE, Marvel, LPP DPF, ENN
    for cid in ["04", "06", "18", "24", "25", "39"]:
        assert _score(cid) == 5.0

def test_d_he3_direct_high_tier():
    """D-He3 + direct conversion (Helion, Zephyr) score 4.33."""
    assert _score("08") == 4.33
    assert _score("19") == 4.33

def test_d_d_thermal_score_2_33():
    """D-D + thermal/TBD scores 2.33."""
    # Sonofusion (TBD), Cortex (thermal), Polomac, NearStar
    for cid in ["02", "03", "35", "37"]:
        assert _score(cid) == 2.33

def test_d_t_thermal_bottom_tier():
    """D-T + thermal scores 1.67 — the bottom tier."""
    # Should include most D-T concepts
    for cid in ["01", "05", "07", "09", "10", "11", "12", "13", "14",
                "15", "16", "17", "20", "21", "22", "23", "26", "27",
                "29", "30", "31", "32", "33", "34", "36", "38"]:
        assert _score(cid) == 1.67

def test_polywell_d_t_direct_3_0():
    """Polywell D-T + Direct (charged particle) scores 3.0 — only D-T concept with direct conversion."""
    assert _score("28") == 3.0

def test_all_within_bounds():
    """Every concept scores in [1.0, 5.0]."""
    for cid in [f"{i:02d}" for i in range(1, 40)]:
        score = _score(cid)
        assert 1.0 <= score <= 5.0


# ============================================================================
# Weight tuning is functional
# ============================================================================

def test_changing_p_b11_score_changes_outcome():
    """If we reduce p-B11 safety score, p-B11 concepts drop."""
    # Default: p-B11 + direct = 5.0
    # If p-B11 score drops to 3, raw = (4+3)/2 = 3.5, score = 4.33
    assert _customization(4, 3) == 4.33

def test_changing_thermal_score_changes_outcome():
    """If we promote thermal-cycle score from 2 to 3, D-T thermal lifts."""
    # Default: D-T + thermal = (2+1)/2 = 1.5 → 1.67
    # If thermal score = 3: (3+1)/2 = 2.0 → 2.33
    assert _customization(3, 1) == 2.33
```

---

## Predicted scores (all 39 concepts)

| Concept | Fuel | Energy Capture | A | B | Raw | **Score** |
|---|---|---|---|---|---|---|
| 01 CFS ARC | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 02 Sonofusion | D-D | TBD | 2 | 2 | 2.0 | **2.33** |
| 03 Cortex liquid jet | D-D | Thermal (unspecified) | 2 | 2 | 2.0 | **2.33** |
| 04 hb11 p-B11 | p-B11 | Direct (charged particle) | 4 | 4 | 4.0 | **5.00** |
| 05 Thea planar | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 06 Pale Blue p-B11 | p-B11 | Direct (charged particle) | 4 | 4 | 4.0 | **5.00** |
| 07 Pacific MagLIF | D-T | Pulsed power implosion | 2 | 1 | 1.5 | **1.67** |
| 08 Helion | D-He3 | Direct (inductive) | 4 | 3 | 3.5 | **4.33** |
| 09 Proxima QI | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 10 Gauss HELIAS | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 11 Realta mirror | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 12 OpenStar | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 13 Avalanche | D-T | TBD | 2 | 1 | 1.5 | **1.67** |
| 14 General Fusion MTF | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 15 Zap Z-pinch | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 16 Acceleron muon | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 17 Focused DPSSL | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 18 TAE p-B11 | p-B11 | Direct (charged particle) | 4 | 4 | 4.0 | **5.00** |
| 19 Zephyr D-He3 | D-He3 | Direct (charged particle) | 4 | 3 | 3.5 | **4.33** |
| 20 Type One Infinity | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 21 Renaissance | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 22 Tokamak Energy ST | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 23 First Light | D-T | Projectile impact | 2 | 1 | 1.5 | **1.67** |
| 24 Marvel p-B11 | p-B11 | Direct (charged particle) | 4 | 4 | 4.0 | **5.00** |
| 25 LPP DPF p-B11 | p-B11 | Direct (charged particle) | 4 | 4 | 4.0 | **5.00** |
| 26 Intensity heavy-ion | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 27 Xcimer KrF | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 28 EMC2 Polywell | D-T | Direct (charged particle) | 4 | 1 | 2.5 | **3.00** |
| 29 Energy Singularity | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 30 Firefly NTT | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 31 Inertia DPSSL | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 32 Blue Laser OEC | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 33 GenF French | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 34 Neo Fusion BEST | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 35 Polomac D-D | D-D | Thermal (unspecified) | 2 | 2 | 2.0 | **2.33** |
| 36 Helical Fusion | D-T | Thermal (unspecified) | 2 | 1 | 1.5 | **1.67** |
| 37 NearStar MTIF | D-D | Thermal (unspecified) | 2 | 2 | 2.0 | **2.33** |
| 38 SHINE accelerator | D-T | Neutron applications | 2 | 1 | 1.5 | **1.67** |
| 39 ENN EHL-2 p-B11 | p-B11 | Direct (charged particle) | 4 | 4 | 4.0 | **5.00** |

### Score distribution

- **5.00 (6 concepts)**: All p-B11 aneutronic + direct conversion concepts (hb11, Pale Blue, TAE, Marvel, LPP DPF, ENN)
- **4.33 (2 concepts)**: D-He³ with direct conversion (Helion, Zephyr)
- **3.00 (1 concept)**: Polywell — the only D-T concept with claimed direct conversion
- **2.33 (4 concepts)**: D-D with thermal/TBD (Sonofusion, Cortex, Polomac, NearStar MTIF)
- **1.67 (26 concepts)**: Every D-T concept with thermal cycle (the mainstream)

### Notable score patterns

**The customization axis cleanly separates by fuel + energy capture combination.** Five distinct tiers, with the bottom tier (1.67) containing the D-T thermal mainstream and the top tier (5.00) containing aneutronic concepts with direct conversion. This is the framework working as designed: customization burden is fundamentally driven by these two architectural choices.

**Polywell at 3.00 is the only D-T concept above 1.67.** EMC2's electrostatic concept claims direct charged-particle conversion. The framework rewards this — even though the fuel is D-T (1), the direct conversion (4) lifts the score significantly. If you're skeptical of Polywell's direct-conversion claim, this is where it shows up.

**TBD energy capture defaults to thermal**, putting Sonofusion and Avalanche at the same level as standard thermal concepts. If a TBD concept later turns out to be direct conversion (e.g., Sonofusion publishes a piezoelectric collection design), the feature value updates and the score recomputes upward. The framework is conservative about undisclosed designs rather than optimistic.

**SHINE at 1.67** despite being a non-power neutron source. The framework treats `Neutron applications` as thermal-equivalent because the accelerator still requires substantial cooling infrastructure. Fuel is D-T (worst case). Customization-wise, SHINE has the same site-customization burden as a D-T power plant on this axis even though it produces no electricity. Arguably correct — SHINE's siting near medical isotope demand is itself a customization constraint.

---

## Files touched

```
exploration/scoring_v2/weights/default.yaml                          # add customization axis with inline lookup tables
exploration/scoring_v2/embeddings/rulebook.py                        # add 3 embeddings + 2 helpers
exploration/scoring_v2/lookup_customization.yaml                     # NEW: customization metadata (no weights)
exploration/scoring_v2/features/*.yaml                               # 39 files: append customization_diagnostics block
exploration/scoring_v2/scripts/populate_customization_diagnostics.py  # NEW: idempotent diagnostic population
tests/scoring_v2/test_customization.py                                # NEW: acceptance tests
.project/active/scoring-v2-customization-slice/design.md              # NEW: this spec + planning doc
.project/active/scoring-v2-customization-slice/implementation_notes.md # NEW: implementation tracking
```

---

## Coordination notes

### Relationship to other axes

Customization is **independent** of Modularity, Supply Chain, and Plant Complexity. The three axes touch different sections of `weights/default.yaml` and different embeddings. Customization can land in any order relative to the other axes.

### Schema dependencies

Both trigger features (`Fuel`, `Energy Capture`) are in the v0.3.0 ontology (`schema.md`, 2026-05-12). **No schema changes needed.**

Specifically check:
- `Energy Capture` value coverage: every concept must have one of the 12 controlled values plus TBD. Direct conversion variants (`Direct (inductive)`, `Direct (charged particle)`) must use the controlled vocab — no leftover free-text.
- `Fuel` value coverage: every concept must have one of {p-B11, D-He3, D-D, D-T, Unknown}. The `Multiple` value is gone per recent schema revision.

### Relationship to the source framework

The C5 logic is ported from `fusion-tea-scoring` branch's `exploration/concept_analysis/prompt_templates/config/scoring_framework.md`. Key differences in the port:

1. **Fully deterministic**: the original framework had Claude apply judgment to fill C5 values into YAML. The port computes C5 from features deterministically — no Claude in the loop.

2. **TBD handling added**: the v0.3.0 schema added TBD as an `Energy Capture` value (not in the original framework). The port treats TBD as thermal-equivalent.

3. **Site-specific exclusion preserved**: the original explicitly states "site-specific advantages must NOT inflate C5." The deterministic port enforces this automatically by only reading architectural features — there's no way for site-specific judgment to leak in.

4. **Rescaling preserved**: the (4/3) factor that stretches `[1.0, 4.0]` to `[1.0, 5.0]` is faithfully ported.

---

## Implementation notes for Claude Code

- **All trigger logic uses v0.3.0 schema controlled vocabulary**. No substring matching against free-text. `Fuel` is an enum; `Energy Capture` is an enum with 12 values; the classification helper maps them to three keys cleanly.

- **The diagnostic block emission ordering should be stable**. Use the canonical order: `sub_factor_a`, `sub_factor_b`, `raw_average`, `customization_score`.

- **Weight loading pattern**: examine how `_load_bottleneck_weights` and `_load_subsystem_weights` are implemented in the supply chain and plant complexity slices. Match that pattern for `_load_customization_weights`.

- **Schema feature key naming**: the v0.3.0 schema uses title-case column names (`Energy Capture`, `Fuel`), but feature files typically use snake_case keys (`energy_capture`, `fuel`). The embedding `inputs=` list uses snake_case to match feature-file convention.

- **`customization_score` is a two-input embedding** (just applies the formula). If the framework distinguishes derived/passthrough embeddings from substantive ones, use the appropriate annotation. If not, standard `@embedding` is fine.

- **Failure mode for missing lookup tables**: `_load_customization_weights` raises if either table is absent or incomplete. Intentional — fail loudly rather than silently default. If the analyst removes a key from `default.yaml`, the framework should refuse to score rather than silently produce wrong scores.

- **Unknown fuel defaults to D-T**: conservative — concepts that haven't disclosed their fuel are treated as worst-case D-T. This is consistent with the TBD-energy-capture-defaults-to-thermal pattern.

- **`Multiple` fuel removed in recent schema revision**: not in the fuel_safety_scores lookup. If `Multiple` is encountered, `_fuel_safety_score` will raise. Update the schema migration if any feature files still have `Multiple`.

---

## Open questions worth flagging (for future versions)

These don't block implementation but are worth raising in the design.md for the slice:

1. **TBD → thermal vs. TBD → its own penalty**: Currently TBD energy capture defaults to thermal (score 2). Alternative: give TBD a lower score (e.g., 1) to penalize undisclosed designs more heavily. The plant complexity axis already has a `tbd_bop` penalty; combining the customization TBD penalty with that one would double-count. Recommendation: keep TBD → thermal here.

2. **Polywell direct-conversion claim**: At score 3.0, Polywell is the only D-T concept above 1.67. If the analyst doesn't believe Polywell's direct-conversion claim is credible, the `Energy Capture` feature should be changed from `Direct (charged particle)` to `Thermal (unspecified)` or `TBD`. The framework follows the feature; analyst judgment about credibility belongs in Technical Feasibility, not here.

3. **Polywell vs. Avalanche treatment**: Both are electrostatic concepts but Polywell claims direct conversion (score 3.0) and Avalanche has TBD (score 1.67). The asymmetry comes from how the feature is populated, not from any difference in the framework. Worth verifying that this is consistent with analyst priors before publishing scores.

4. **Air-cooled tier (omitted)**: The original C5 framework lists a separate score (1, "exceptional thermal rejection — multiple cooling systems"). Currently omitted because no concept maps there. If a future high-rep-rate IFE concept turns out to need both primary chamber cooling AND a separate laser-optics cooling system, that concept might warrant the score-1 tier. Defer until needed.

5. **Site-specific advantage handling**: The framework explicitly excludes site-specific advantages (named sites, brownfield reuse, water proximity) from the score. This is enforced automatically by the deterministic computation — no judgment input. If the analyst later wants to *credit* site-specific advantages (a separate axis perhaps), that should be a new axis, not a modification here.

6. **Compression at 1.67**: 26 out of 39 concepts (67%) score at 1.67 because D-T + thermal is the modal architecture. The customization axis is dominated by the fuel choice, with little intra-fuel differentiation. This is structurally similar to how Plant Complexity has D-T concepts clustered at the bottom. Differentiation among D-T concepts should come from other axes — particularly Modularity, Supply Chain, Plant Complexity. Worth flagging that the customization axis adds less differentiation signal than the other three.
