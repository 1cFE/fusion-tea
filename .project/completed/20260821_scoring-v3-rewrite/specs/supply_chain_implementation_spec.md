# Implementation Spec: Supply Chain Scoring Axis

**Status:** Ready for implementation
**Owner:** Mallory
**Created:** 2026-05-18
**Branch:** `concept-downselect`
**Target directory:** `.project/active/scoring-v2-supply-chain-slice/` (new slice — sibling to existing modularity slices)

This is a Claude Code implementation spec. The underlying design is documented in `supply_chain_scoring_plan.md`; this spec adds the framework integration details (decorator registration, file paths, YAML schemas, M&SO integration).

---

## Summary

Build a new **Supply Chain** scoring axis as a peer of Modularity in `weights/default.yaml`. The axis produces a deterministic 1.0–5.0 score per concept based on which of 7 critical-material bottlenecks the concept triggers, weighted by severity tier.

### Score formula

```
supply_chain_score = max(1.0, 5.0 - bottleneck_weight)

where bottleneck_weight = sum of severity weights of triggered bottlenecks
```

### Key design choices

- **Weights live in `weights/default.yaml`** under the supply_chain axis (not buried in lookup files). This makes the tuning surface transparent — all seven severity weights are visible right where the analyst would look to tune the framework.
- **All triggers use existing schema features from the v0.3.0 ontology.** No new features required. Specifically: `Fuel`, `Blanket Config`, `Confinement Family`, and `Primary Heating` — all in the post-SCHEMA_REVISION_PROPOSALS schema.
- **`lookup_bottlenecks.yaml` is metadata only** — tier names, trigger descriptions, supply estimates, rationale. It does not own the numerical weights.

### Schema migration note

This spec targets the v0.3.0 ontology (`schema.md`, 2026-05-12). The previous draft of this spec referenced the older feature names (`fuel`, `tritium_breeding`, `confinement_family`, `ife_driver`). Key changes from the prior schema:

- `Blanket Config` replaces `tritium_breeding`. Now controlled vocabulary (`Liquid metal`, `Molten salt`, `Solid breeder`, `Other/hybrid`, `N/A (no tritium)`, `N/A (non-power)`, `TBD`) instead of free-text strings. Eliminates brittle substring matching.
- `ife_driver` no longer exists. Laser-driver detection now uses `Primary Heating` (which starts with `Laser` for all laser IFE variants).
- `Confinement Family` now includes `Electrostatic` and `Other` (replacing the old `Non-Standard`).
- `Fuel` adds `Unknown` value.

The new schema is materially better for our triggers because the controlled-vocabulary `Blanket Config` eliminates the substring-matching brittleness that bedevilled the previous approach.

### Bottleneck list (7 entries)

| Bottleneck | Tier | Weight | Trigger feature |
|---|---|---|---|
| Helium-3 | Critical | 3.0 | `fuel` |
| Tritium | Severe | 1.0 | `Fuel` |
| Lithium-6 (enriched) | Severe | 1.0 | `Fuel`, `Blanket Config` |
| Beryllium | Severe | 1.0 | `Fuel`, `Blanket Config` |
| Vanadium (nuclear-grade) | Severe | 1.0 | `Fuel`, `Blanket Config` |
| FLiBe | Moderate | 0.5 | `Blanket Config` |
| KDP/DKDP crystals | Moderate | 0.5 | `Confinement Family`, `Primary Heating` |

All six features (`Fuel`, `Blanket Config`, `Confinement Family`, `Primary Heating`) are in the v0.3.0 schema (`schema.md`). No new features required.

---

## Changes summary

| # | Change | Touches |
|---|---|---|
| A | Add `supply_chain` axis with inline severity weights to `weights/default.yaml` | `weights/default.yaml` |
| B | Implement `bottleneck_weight` and `supply_chain_score` embeddings | `embeddings/rulebook.py` |
| C | Create `lookup_bottlenecks.yaml` metadata file (no weights) | `lookup_bottlenecks.yaml` (new) |
| D | Add `supply_chain_diagnostics` derived block per feature file | `features/*.yaml` (39 files) |
| E | Add acceptance tests | `tests/scoring_v2/test_supply_chain.py` (new) |

---

## Change A: M&SO axis registration with inline weights

### Updated `weights/default.yaml`

```yaml
# Existing axes (unchanged by this spec)
economic_potential: {}                    # not yet built
technical_feasibility: {}                 # not yet built
manufacturability_scale_out:              # modularity (unchanged from v5 restructure)
  min_viable_device_scale: 0.50
  percent_mod: 0.25
  unit_multiplicity: 0.25

# NEW axis added by this spec
supply_chain:
  supply_chain_score: 1.0                 # axis-level M&SO weight (this embedding's contribution)
  bottleneck_severity_weights:            # per-bottleneck severity weights (the tuning surface)
    helium3:   3.0                        # Critical: no terrestrial scaling path
    tritium:   1.0                        # Severe: CANDU-constrained, self-breeding is the path
    lithium6:  1.0                        # Severe: no commercial enrichment exists
    beryllium: 1.0                        # Severe: constrained mining, single fusion plant ~ global annual supply
    vanadium:  1.0                        # Severe: nuclear-grade refining doesn't exist commercially
    flibe:     0.5                        # Moderate: half-weight to avoid double-counting Li-6 + Be
    kdp:       0.5                        # Moderate: industrial manufacturing problem, partially substitutable
```

### Why weights live here (not in lookup_bottlenecks.yaml)

The supply chain axis has exactly two tuning surfaces:
1. **The axis-level M&SO weight** (`supply_chain_score: 1.0`) — how much this axis contributes when combined with Modularity, Technical Feasibility, etc.
2. **The seven severity weights** — calibrating which bottlenecks count for how much.

Putting both in `weights/default.yaml` means an analyst can see and tune the entire supply chain story from one file. If a future revisiting of severity tiers needs to happen (e.g., "should KDP be 1.0 instead of 0.5?"), it's a one-line YAML edit visible right next to the modularity weights.

This is different from Reid's modularity slice 2, which keeps capex-share weights in `lookup_family_weights.yaml` (a per-family lookup table). The distinction: family weights are per-concept lookup data (different concept gets different weights), while supply chain severity weights are global parameters (same weights apply to every concept). Global parameters belong in `default.yaml`; per-concept data belongs in lookup tables.

---

## Change B: Embeddings in `rulebook.py`

### Implementation

Add to `embeddings/rulebook.py` after the existing modularity embeddings:

```python
# ===========================================================================
# Supply Chain Axis
#
# Deterministic scoring based on which critical-material bottlenecks a concept's
# fuel + blanket + driver choices trigger. Weights are loaded from
# weights/default.yaml under the supply_chain.bottleneck_severity_weights key.
#
# All trigger logic uses v0.3.0 schema features (Fuel, Blanket Config,
# Confinement Family, Primary Heating). No substring matching against
# free-text strings — all triggers key off controlled-vocabulary enum values.
# ===========================================================================

# Bottleneck names (matched with default.yaml weight keys)
_BOTTLENECK_NAMES = [
    "tritium", "lithium6", "helium3", "beryllium",
    "vanadium", "flibe", "kdp",
]

# Blanket Config values that indicate active tritium breeding (Li-6 dependency)
_BREEDING_BLANKET_VALUES = {"Liquid metal", "Molten salt", "Solid breeder", "Other/hybrid"}

# Blanket Config values that contain beryllium (Be dependency)
# - Solid breeder: HCPB pebble bed uses Be₁₂Ti or pure Be as neutron multiplier
# - Molten salt: FLiBe is LiF-BeF₂ (contains beryllium)
# - Other/hybrid: hybrid blankets may or may not contain Be; treated conservatively
#   as triggering (analyst can override via per-concept feature override if needed)
_BERYLLIUM_BLANKET_VALUES = {"Solid breeder", "Molten salt", "Other/hybrid"}


def _load_bottleneck_weights(weights_yaml: dict) -> dict[str, float]:
    """Extract per-bottleneck severity weights from the loaded weights/default.yaml.

    The weights live under supply_chain.bottleneck_severity_weights.
    Returns dict[bottleneck_name -> weight].
    Raises if any expected bottleneck is missing — fail loudly rather than silently
    using a default.
    """
    sc_axis = weights_yaml.get("supply_chain", {})
    raw = sc_axis.get("bottleneck_severity_weights", {})
    missing = [b for b in _BOTTLENECK_NAMES if b not in raw]
    if missing:
        raise ValueError(
            f"weights/default.yaml supply_chain.bottleneck_severity_weights is missing "
            f"required keys: {missing}. All seven bottleneck severity weights must be "
            f"specified."
        )
    return {b: float(raw[b]) for b in _BOTTLENECK_NAMES}


def _compute_triggered_bottlenecks(
    fuel: str,
    blanket_config: str,
    confinement_family: str,
    primary_heating: str,
    weights: dict[str, float],
) -> dict[str, float]:
    """Returns dict of {bottleneck_name: weight} for triggered bottlenecks only.

    Pure function — given the same feature inputs and weights, always returns
    the same dict.

    All trigger logic keys off v0.3.0 schema controlled-vocabulary features:
        fuel              (enum: D-T, D-D, D-He3, p-B11, Unknown)
        blanket_config    (enum: Liquid metal, Molten salt, Solid breeder,
                                 Other/hybrid, N/A (no tritium), N/A (non-power), TBD)
        confinement_family (enum: MFE, IFE, MIF, Electrostatic, Other)
        primary_heating   (enum: 19 values; laser triggers match prefix "Laser")
    """
    fuel = fuel or ""
    raw_blanket = blanket_config or ""
    cf = confinement_family or ""
    heating = primary_heating or ""

    # TBD blanket → default to "Liquid metal". This is the most common choice
    # across all (Confinement Family, Fuel) combinations in the v3 matrix
    # (7/11 D-T MFE concepts, 1/1 D-T MIF concept, 7/8 D-T IFE concepts).
    # The diagnostic block records `blanket_assumed: liquid_metal_default`
    # so the UI can surface the inferred value with a confidence flag.
    blanket = "Liquid metal" if raw_blanket == "TBD" else raw_blanket

    triggered = {}

    if fuel == "D-T":
        # Tritium: always fires for D-T
        triggered["tritium"] = weights["tritium"]

        # Lithium-6: fires when the concept actively breeds tritium internally.
        # N/A (no tritium) shouldn't co-occur with D-T fuel but is excluded defensively.
        # N/A (non-power) excludes neutron-source-only concepts like SHINE that buy
        # tritium externally rather than breeding.
        # TBD blankets default to Liquid metal (above) and therefore trigger li6.
        if blanket in _BREEDING_BLANKET_VALUES:
            triggered["lithium6"] = weights["lithium6"]

        # Beryllium: fires when blanket contains Be as neutron multiplier
        # (Solid breeder: HCPB pebble bed) or as chemical constituent
        # (Molten salt: FLiBe). Other/hybrid included conservatively.
        # Pure Liquid metal blankets (LiPb, pure Li) don't need separate Be.
        if blanket in _BERYLLIUM_BLANKET_VALUES:
            triggered["beryllium"] = weights["beryllium"]

        # Vanadium: fires only for Liquid metal blankets. The Blanket Config
        # vocabulary lumps LiPb, pure Li, and Li-LiH under "Liquid metal" —
        # all of which use V-Cr-Ti or compatible alloys due to lithium
        # chemistry compatibility. Renaissance's hybrid Li-LiH + Pb pebble
        # is classified as Other/hybrid, not Liquid metal, so doesn't fire here.
        # TBD blankets (defaulted to Liquid metal above) also trigger vanadium.
        if blanket == "Liquid metal":
            triggered["vanadium"] = weights["vanadium"]

        # FLiBe: fires for Molten salt blankets. The Blanket Config vocabulary
        # covers FLiBe, FLiNaBe, and related lithium-fluoride-bearing salts
        # under "Molten salt"; all carry the FLiBe-class handling burden.
        if blanket == "Molten salt":
            triggered["flibe"] = weights["flibe"]

    elif fuel == "D-He3":
        triggered["helium3"] = weights["helium3"]

    # KDP/DKDP: applies to laser-IFE concepts regardless of fuel.
    # All laser variants in v0.3.0 Primary Heating start with "Laser":
    # Laser (indirect drive), Laser (direct drive), Laser (fast ignition),
    # Laser (ultrashort pulse), Laser (novel/TBD).
    # Excludes Heavy ion beam, Projectile impact, Acoustic implosion,
    # Electromagnetic pinch (DPF), Muon catalysis.
    if cf == "IFE" and heating.startswith("Laser"):
        triggered["kdp"] = weights["kdp"]

    return triggered


@embedding(
    "bottleneck_weight",
    inputs=["fuel", "blanket_config", "confinement_family", "primary_heating"],
)
def _bottleneck_weight(
    fuel: str,
    blanket_config: str,
    confinement_family: str,
    primary_heating: str,
    *,
    weights_yaml: dict,
) -> float:
    """Sum of severity weights of all triggered bottlenecks for this concept.

    Loads severity weights from weights_yaml at call time, allowing weight
    edits in weights/default.yaml to take effect without code changes.
    """
    sev_weights = _load_bottleneck_weights(weights_yaml)
    triggered = _compute_triggered_bottlenecks(
        fuel, blanket_config, confinement_family, primary_heating, sev_weights,
    )
    return sum(triggered.values())


@embedding(
    "supply_chain_score",
    inputs=["bottleneck_weight"],
)
def _supply_chain_score(bottleneck_weight: float) -> float:
    """Supply chain score: 1.0 (floor) to 5.0 (no bottlenecks).

    Formula: max(1.0, 5.0 - bottleneck_weight)
    """
    return max(1.0, 5.0 - bottleneck_weight)
```

### Schema feature key naming

The v0.3.0 schema describes columns with title-case names (`Fuel`, `Blanket Config`, etc.), but Reid's feature files typically use snake_case keys (`fuel`, `blanket_config`). The embedding `inputs=` list uses snake_case to match the feature-file key convention. If Reid's extractor produces different key names from the schema columns, adapt accordingly — but the trigger logic itself is independent of the key naming.

### Why Other/hybrid triggers beryllium

The Blanket Config vocabulary lists `Other/hybrid` as architecturally novel blankets that may include Be (e.g., Renaissance's Li-LiH + Pb pebble multiplier doesn't include Be, but other hypothetical hybrids might). Treating Other/hybrid as triggering beryllium is the conservative default — it can be overridden per-concept if a specific hybrid blanket genuinely avoids Be. The Other/hybrid flag is described in the schema as requiring per-concept cost-model overrides anyway, so this fits the pattern.

### Weight-loading injection pattern

The `_bottleneck_weight` embedding takes `weights_yaml` as a keyword-only argument. This requires the framework to inject the loaded weights file into embeddings that need it.

**If Reid's framework already supports this** (e.g., embeddings can receive the weights file as a context argument): use the pattern above as-is.

**If not**: load `weights/default.yaml` once at module init via a module-level cache, like:

```python
import yaml
from pathlib import Path

_WEIGHTS_PATH = Path(__file__).parent.parent / "weights" / "default.yaml"
_CACHED_WEIGHTS = yaml.safe_load(_WEIGHTS_PATH.read_text())

# Then in the embedding:
@embedding("bottleneck_weight", inputs=[...])
def _bottleneck_weight(fuel, tritium_breeding, confinement_family, ife_driver):
    sev_weights = _load_bottleneck_weights(_CACHED_WEIGHTS)
    ...
```

Module-level caching is acceptable because `weights/default.yaml` is loaded once per process and shouldn't change at runtime. If hot-reloading becomes a requirement later, the cache can be replaced with explicit injection.

**Implementation note for Claude Code**: examine how `lookup_family_weights.yaml` is loaded in the slice 2 component-modularity code (`embeddings/component_modularity.py` or wherever it lives) and match that pattern. Whatever the framework uses for one is what the framework should use for the other.

---

## Change C: `lookup_bottlenecks.yaml` (metadata only)

### New file: `exploration/scoring_v2/lookup_bottlenecks.yaml`

Note: this file documents bottleneck *metadata* (tier names, trigger descriptions, supply estimates, rationale). **Numerical weights are NOT in this file** — they're in `weights/default.yaml` under `supply_chain.bottleneck_severity_weights`. This file exists for analyst reference and future framework introspection (e.g., emitting human-readable explanations of why a concept scored what it did).

```yaml
# Supply chain bottleneck metadata.
#
# Numerical severity weights are NOT here — they live in
# weights/default.yaml under supply_chain.bottleneck_severity_weights
# to keep the tuning surface co-located with modularity weights.
#
# Each entry documents:
#   - tier: severity classification (matches the weight assignment in default.yaml)
#   - trigger: human-readable description of when this bottleneck fires
#   - features_used: which v0.3.0 schema columns the trigger reads
#   - current_supply: current global supply situation (analyst reference)
#   - rationale: why this severity tier is appropriate (analyst reference)
#
# The authoritative trigger logic lives in rulebook.py:_compute_triggered_bottlenecks().
# This file documents what the code does; the code is the source of truth for trigger rules.

helium3:
  tier: Critical
  trigger: "Fires when Fuel = D-He3"
  features_used: [Fuel]
  current_supply: "15-60 kg/yr globally (US/Russia weapons byproduct); $18.7M/kg"
  rationale: |
    Produced only by tritium decay (12.3-yr half-life). No terrestrial production
    scaling path. Lunar mining is decades away. Helion's 50MWe plant needs ~2 kg/yr —
    annual global supply fuels ~10-30 plants total, ever. Single Critical bottleneck
    imposes more penalty than three Severe bottlenecks combined.

tritium:
  tier: Severe
  trigger: "Fires when Fuel = D-T"
  features_used: [Fuel]
  current_supply: "~50 kg total stockpile; ~2 kg/yr CANDU production; declining"
  rationale: |
    Constrained to CANDU fleet but self-breeding from Li-6 is a credible path
    (ARC, ITER, EU-DEMO all assume it). Startup tritium plus breeding ratio
    demonstration are the binding problems.

lithium6:
  tier: Severe
  trigger: |
    Fires when Fuel = D-T AND Blanket Config in
    {Liquid metal, Molten salt, Solid breeder, Other/hybrid}.
    Does NOT trigger for N/A (no tritium) or N/A (non-power) blankets.
    TBD blankets default to Liquid metal (per analyst-approved TBD rule)
    and therefore DO trigger this penalty; the diagnostic block records
    `blanket_assumed: liquid_metal_default`.
  features_used: [Fuel, Blanket Config]
  current_supply: "Effectively zero western supply; COLEX is Minamata-banned"
  rationale: |
    No commercial enrichment exists, but industry-wide problem affecting all D-T
    concepts with breeding blankets. Multi-decade nation-state-scale buildout
    required, but chemistry/physics is well-understood. Not a fundamentally
    impossible bottleneck like He-3.

    Note: SHINE-class neutron-source concepts (Fuel=D-T but Blanket Config=N/A
    (non-power)) don't trigger this — they buy tritium externally rather than
    breeding it. The v0.3.0 schema captures this correctly via the N/A (non-power)
    blanket value.

beryllium:
  tier: Severe
  trigger: |
    Fires when Fuel = D-T AND Blanket Config in
    {Solid breeder, Molten salt, Other/hybrid}.
  features_used: [Fuel, Blanket Config]
  current_supply: "~330 t/yr global mine production; ~$1.27B/yr metal/alloy market"
  rationale: |
    Required as neutron multiplier in HCPB pebble beds (Solid breeder) and as a
    chemical constituent of FLiBe (Molten salt: LiF-BeF₂). Other/hybrid is
    included conservatively — most hybrid blankets include some Be component;
    per-concept override available if a specific hybrid genuinely avoids Be.
    Pure liquid-metal blankets (LiPb, pure Li) don't need separate Be neutron
    multiplier and don't trigger this.

vanadium:
  tier: Severe
  trigger: "Fires when Fuel = D-T AND Blanket Config = Liquid metal"
  features_used: [Fuel, Blanket Config]
  current_supply: |
    Vanadium metal: ~80-100 kt/yr global;
    nuclear-grade V-4Cr-4Ti: pilot scale only
  rationale: |
    V-Cr-Ti alloys are the natural structural material for liquid-lithium blankets
    (chemical compatibility with lithium). The v0.3.0 schema groups LiPb, pure Li,
    Li-LiH, and other liquid-metal first walls under "Liquid metal" — all of these
    architectures face the V-alloy supply chain question even though specific
    compatibility varies (LiPb can use RAFM steel in some configurations, but
    V-alloy remains the preferred structural material for fusion-grade designs).

    Renaissance's hybrid Li-LiH + Pb pebble system is classified as Other/hybrid
    in the schema, not Liquid metal, so doesn't fire this. That partitioning
    decision was made in the schema; we inherit it.

flibe:
  tier: Moderate
  trigger: "Fires when Blanket Config = Molten salt"
  features_used: [Blanket Config]
  current_supply: "<$10M/yr scale (research only)"
  rationale: |
    Half-weight to avoid double-counting — Li-6 and Be are already counted
    separately when Molten salt blanket is selected. The FLiBe-specific burden
    is molten-salt handling expertise, corrosion-resistant alloys (Hastelloy-N
    class), and tritium-permeation management. The v0.3.0 schema includes
    FLiNaBe and related salts under Molten salt; all carry similar handling
    burden.

kdp:
  tier: Moderate
  trigger: "Fires when Confinement Family = IFE AND Primary Heating starts with 'Laser'"
  features_used: [Confinement Family, Primary Heating]
  current_supply: "Cleveland Crystals (US) + Saint-Gobain heritage (Russia); 1-2 month boule growth"
  rationale: |
    Industrial-scale manufacturing problem rather than no-path-forward. Slow
    growth cycles + concentrated supplier base. Partially substitutable with
    LBO/BBO for some frequency conversion. Applies to all laser variants in
    the v0.3.0 Primary Heating vocabulary: Laser (indirect drive), Laser
    (direct drive), Laser (fast ignition), Laser (ultrashort pulse), Laser
    (novel/TBD). Does not trigger for non-laser IFE drivers: Heavy ion beam
    (Intensity), Projectile impact (First Light), Acoustic implosion
    (Sonofusion), Electromagnetic pinch (LPP DPF).
```

---

## Change D: Feature-file diagnostics

Add a derived block to each concept's feature file showing supply-chain calculation transparency.

### Diagnostic block format

```yaml
# In each features/{ID}-{name}.yaml file, append:
supply_chain_diagnostics:
  bottlenecks_triggered:
    {bottleneck_name}: {weight}     # one entry per triggered bottleneck
  bottleneck_weight: {sum}
  supply_chain_score: {score}
```

### Examples

**CFS ARC (`features/01-cfs-arc.yaml`)**:

```yaml
supply_chain_diagnostics:
  bottlenecks_triggered:
    tritium: 1.0
    lithium6: 1.0
    beryllium: 1.0
    flibe: 0.5
  bottleneck_weight: 3.5
  supply_chain_score: 1.5
```

**Helion (`features/08-frc-w-direct-conversion.yaml`)**:

```yaml
supply_chain_diagnostics:
  bottlenecks_triggered:
    helium3: 3.0
  bottleneck_weight: 3.0
  supply_chain_score: 2.0
```

**Pale Blue (no bottlenecks)**:

```yaml
supply_chain_diagnostics:
  bottlenecks_triggered: {}
  bottleneck_weight: 0.0
  supply_chain_score: 5.0
```

### Population approach

Write `scripts/populate_supply_chain_diagnostics.py` to programmatically populate the diagnostic block in all 39 feature files. This script:

1. Loads `weights/default.yaml` (to get severity weights)
2. Loads each feature file
3. Calls `_compute_triggered_bottlenecks` with the concept's features and the loaded weights
4. Writes the diagnostic block back to the feature file (appending or replacing)

The script is idempotent and re-runnable. It serves as both the initial population mechanism and as a way to refresh diagnostics after weight or rule changes.

---

## Change E: Acceptance tests

### New test file: `tests/scoring_v2/test_supply_chain.py`

```python
"""Acceptance tests for the supply chain scoring axis."""
import pytest
import yaml
from pathlib import Path

from exploration.scoring_v2.embeddings.rulebook import (
    REGISTRY,
    _compute_triggered_bottlenecks,
    _load_bottleneck_weights,
)


_BASE = Path(__file__).parent.parent.parent / "exploration" / "scoring_v2"
_WEIGHTS_YAML = yaml.safe_load((_BASE / "weights" / "default.yaml").read_text())
_SEVERITY_WEIGHTS = _load_bottleneck_weights(_WEIGHTS_YAML)


# ============================================================================
# Weights are visible in default.yaml
# ============================================================================

class TestWeightsExposedInDefaultYaml:
    """Verify the seven severity weights are visible in weights/default.yaml."""

    def test_supply_chain_axis_exists(self):
        assert "supply_chain" in _WEIGHTS_YAML

    def test_axis_weight_is_one(self):
        assert _WEIGHTS_YAML["supply_chain"]["supply_chain_score"] == 1.0

    def test_all_seven_severity_weights_present(self):
        sev = _WEIGHTS_YAML["supply_chain"]["bottleneck_severity_weights"]
        for name in ["tritium", "lithium6", "helium3", "beryllium",
                     "vanadium", "flibe", "kdp"]:
            assert name in sev, f"Missing severity weight for {name}"

    def test_critical_tier_weight(self):
        assert _SEVERITY_WEIGHTS["helium3"] == 3.0   # Critical

    def test_severe_tier_weights(self):
        assert _SEVERITY_WEIGHTS["tritium"] == 1.0
        assert _SEVERITY_WEIGHTS["lithium6"] == 1.0
        assert _SEVERITY_WEIGHTS["beryllium"] == 1.0
        assert _SEVERITY_WEIGHTS["vanadium"] == 1.0

    def test_moderate_tier_weights(self):
        assert _SEVERITY_WEIGHTS["flibe"] == 0.5
        assert _SEVERITY_WEIGHTS["kdp"] == 0.5

    def test_missing_weight_raises(self):
        """If any of the seven bottleneck weights are missing, _load_bottleneck_weights raises."""
        partial = {"supply_chain": {"bottleneck_severity_weights": {"helium3": 3.0}}}
        with pytest.raises(ValueError, match="missing required keys"):
            _load_bottleneck_weights(partial)


# ============================================================================
# Trigger rule tests (using v0.3.0 schema controlled-vocabulary values)
# ============================================================================

def _triggered(fuel, blanket, cf, heating):
    return _compute_triggered_bottlenecks(fuel, blanket, cf, heating, _SEVERITY_WEIGHTS)


class TestTriggerRulesUseV03Schema:
    """Verify triggers fire correctly using v0.3.0 schema controlled vocabulary."""

    def test_tritium_fires_for_dt_only(self):
        # D-T fires
        assert "tritium" in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")
        # Other fuels don't fire
        assert "tritium" not in _triggered("D-D", "N/A (no tritium)", "IFE", "Laser (direct drive)")
        assert "tritium" not in _triggered("D-He3", "Other/hybrid", "MIF", "Magnetic compression")
        assert "tritium" not in _triggered("p-B11", "N/A (no tritium)", "IFE", "Laser (ultrashort pulse)")

    def test_lithium6_requires_breeding_blanket(self):
        # All four breeding blanket types trigger Li-6
        assert "lithium6" in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")
        assert "lithium6" in _triggered("D-T", "Molten salt", "MFE", "RF (ECRH)")
        assert "lithium6" in _triggered("D-T", "Liquid metal", "MFE", "RF (ECRH)")
        assert "lithium6" in _triggered("D-T", "Other/hybrid", "MFE", "RF (ECRH)")
        # N/A doesn't trigger
        assert "lithium6" not in _triggered("D-T", "N/A (no tritium)", "MFE", "RF (ECRH)")
        assert "lithium6" not in _triggered("D-T", "N/A (non-power)", "Other", "Particle accelerator")
        # TBD blanket defaults to "Liquid metal" → DOES trigger Li-6
        assert "lithium6" in _triggered("D-T", "TBD", "MFE", "RF (ECRH)")

    def test_helium3_fires_for_dhe3_only(self):
        assert "helium3" in _triggered("D-He3", "Other/hybrid", "MFE", "NBI")
        assert "helium3" in _triggered("D-He3", "Other/hybrid", "MIF", "Magnetic compression")
        assert "helium3" not in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")

    def test_beryllium_fires_for_solid_breeder_and_molten_salt(self):
        # Solid breeder (HCPB pebble bed uses Be) fires
        assert "beryllium" in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")
        # Molten salt (FLiBe contains Be) fires
        assert "beryllium" in _triggered("D-T", "Molten salt", "MFE", "RF (ECRH)")
        # Other/hybrid fires conservatively (per-concept override if specific hybrid avoids Be)
        assert "beryllium" in _triggered("D-T", "Other/hybrid", "MFE", "RF (ECRH)")
        # Pure Liquid metal (LiPb, pure Li) doesn't need separate Be
        assert "beryllium" not in _triggered("D-T", "Liquid metal", "MFE", "RF (ECRH)")
        # N/A doesn't fire
        assert "beryllium" not in _triggered("p-B11", "N/A (no tritium)", "IFE", "Laser (ultrashort pulse)")
        # TBD doesn't fire (concept hasn't disclosed blanket)
        assert "beryllium" not in _triggered("D-T", "TBD", "MFE", "RF (ECRH)")

    def test_vanadium_fires_for_liquid_metal_only(self):
        # Liquid metal fires (V-Cr-Ti for lithium compatibility)
        assert "vanadium" in _triggered("D-T", "Liquid metal", "MFE", "RF (ECRH)")
        # Other blankets don't fire
        assert "vanadium" not in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")
        assert "vanadium" not in _triggered("D-T", "Molten salt", "MFE", "RF (ECRH)")
        assert "vanadium" not in _triggered("D-T", "Other/hybrid", "MFE", "RF (ECRH)")
        assert "vanadium" not in _triggered("D-T", "TBD", "MFE", "RF (ECRH)")

    def test_flibe_fires_for_molten_salt(self):
        # Molten salt fires (FLiBe, FLiNaBe, etc.)
        assert "flibe" in _triggered("D-T", "Molten salt", "MFE", "RF (ECRH)")
        # Other blankets don't fire
        assert "flibe" not in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")
        assert "flibe" not in _triggered("D-T", "Liquid metal", "MFE", "RF (ECRH)")
        assert "flibe" not in _triggered("D-T", "Other/hybrid", "MFE", "RF (ECRH)")

    def test_kdp_fires_for_all_laser_ife_variants(self):
        # All five Laser (*) Primary Heating values fire
        assert "kdp" in _triggered("D-T", "Molten salt", "IFE", "Laser (indirect drive)")
        assert "kdp" in _triggered("D-T", "Solid breeder", "IFE", "Laser (direct drive)")
        assert "kdp" in _triggered("D-T", "Liquid metal", "IFE", "Laser (fast ignition)")
        assert "kdp" in _triggered("p-B11", "N/A (no tritium)", "IFE", "Laser (ultrashort pulse)")
        assert "kdp" in _triggered("D-T", "Solid breeder", "IFE", "Laser (novel/TBD)")
        # Non-laser IFE doesn't fire
        assert "kdp" not in _triggered("D-T", "Liquid metal", "IFE", "Heavy ion beam")
        assert "kdp" not in _triggered("D-T", "Liquid metal", "IFE", "Projectile impact")
        assert "kdp" not in _triggered("D-D", "N/A (no tritium)", "Other", "Acoustic implosion")
        assert "kdp" not in _triggered("p-B11", "N/A (no tritium)", "Other", "Electromagnetic pinch (DPF)")
        # MFE doesn't fire (not IFE)
        assert "kdp" not in _triggered("D-T", "Solid breeder", "MFE", "RF (ECRH)")


# ============================================================================
# Per-concept score anchors (against existing feature files)
# ============================================================================

def _score(concept_id: str) -> float:
    """Load a concept's features and return its supply_chain_score.

    Adapter assumes features are keyed by snake_case versions of the v0.3.0
    schema column names: fuel, blanket_config, confinement_family,
    primary_heating. If Reid's extractor uses different keys, adjust here.
    """
    matches = list((_BASE / "features").glob(f"{concept_id}-*.yaml"))
    assert len(matches) == 1, f"Expected one feature file for {concept_id}, got {len(matches)}"
    features = yaml.safe_load(matches[0].read_text())
    weight = REGISTRY["bottleneck_weight"].fn(
        features.get("fuel"),
        features.get("blanket_config"),
        features.get("confinement_family"),
        features.get("primary_heating"),
        weights_yaml=_WEIGHTS_YAML,
    )
    return REGISTRY["supply_chain_score"].fn(weight)


def test_aneutronic_non_laser_score_5():
    """Aneutronic + D-D non-laser concepts score 5.0 — no bottlenecks fire."""
    for cid in ["02", "06", "18", "25", "35", "37", "39"]:
        assert _score(cid) == 5.0

def test_aneutronic_laser_score_4_5():
    """hb11, Marvel, Cortex score 4.5 — only KDP fires."""
    for cid in ["03", "04", "24"]:
        assert _score(cid) == 4.5

def test_openstar_score_3():
    """OpenStar's ceramic blanket avoids Be and V → score 3.0.

    NOTE: This test depends on how OpenStar's Li2O ceramic blanket is classified
    in the v0.3.0 schema. The schema's Solid breeder definition references HCPB
    (which contains Be), so Li2O-only ceramic might need a per-concept feature
    override or could be re-classified as Other/hybrid. Verify with the
    populated feature file before relying on this anchor.
    """
    assert _score("12") == 3.0

def test_he3_concepts_score_2():
    """Helion and Zephyr score 2.0 — He-3 Critical floors them at the D-T mainstream tier."""
    assert _score("08") == 2.0
    assert _score("19") == 2.0

def test_d_t_mainstream_score_2():
    """D-T HCPB or liquid-Li concepts score 2.0 (three Severe bottlenecks)."""
    for cid in ["07", "09", "10", "11", "13", "14", "15", "16",
                "20", "21", "22", "23", "26", "28", "29", "34", "36", "38"]:
        assert _score(cid) == 2.0

def test_flibe_d_t_score_1_5():
    """D-T + Molten salt (no Laser) scores 1.5."""
    for cid in ["01", "05", "30"]:
        assert _score(cid) == 1.5

def test_dpssl_d_t_score_1_5():
    """D-T DPSSL concepts score 1.5 (three Severe + KDP)."""
    for cid in ["17", "31", "32", "33"]:
        assert _score(cid) == 1.5

def test_xcimer_at_floor():
    """Xcimer: D-T + Molten salt + Laser (weight 4.0) → floor at 1.0."""
    assert _score("27") == 1.0

def test_all_within_bounds():
    """Every concept scores in [1.0, 5.0]."""
    for cid in [f"{i:02d}" for i in range(1, 40)]:
        score = _score(cid)
        assert 1.0 <= score <= 5.0


# ============================================================================
# Weight tuning is functional (analyst can change weights in default.yaml)
# ============================================================================

def test_changing_helium3_weight_changes_helion_score():
    """If we override He-3 severity to 2.0, Helion's score should change from 2.0 to 3.0."""
    custom_weights = dict(_SEVERITY_WEIGHTS)
    custom_weights["helium3"] = 2.0
    triggered = _compute_triggered_bottlenecks(
        "D-He3", "Other/hybrid", "MIF", "Magnetic compression", custom_weights,
    )
    weight = sum(triggered.values())
    score = max(1.0, 5.0 - weight)
    assert score == 3.0, "He-3 weight 2.0 should give Helion score 3.0"

def test_changing_kdp_weight_to_severe_changes_dpssl_score():
    """If we promote KDP from Moderate (0.5) to Severe (1.0), DPSSL-D-T concepts drop from 1.5 to 1.0."""
    custom_weights = dict(_SEVERITY_WEIGHTS)
    custom_weights["kdp"] = 1.0
    triggered = _compute_triggered_bottlenecks(
        "D-T", "Solid breeder", "IFE", "Laser (direct drive)", custom_weights,
    )
    weight = sum(triggered.values())
    score = max(1.0, 5.0 - weight)
    assert score == 1.0, "KDP weight 1.0 should drop DPSSL-D-T to floor"
```

---

## Predicted scores (all 40 concepts)

These are the **acceptance bar** for the implementation — Claude Code's embeddings should reproduce these scores exactly for every concept in the v3 ontology. Computed from the trigger logic in Change B with the severity weights in Change A and the TBD-blanket-default rule.

| ID | Company | Fuel | Blanket Config | Triggers | **Score** |
|---|---|---|---|---|---|
| 01 | Commonwealth Fusion Systems | D-T | Molten salt | tritium, lithium6, beryllium, flibe | **2.0** |
| 02 | Sonofusion Energy | D-D | N/A (no tritium) | (none) | **5.0** |
| 03 | Cortex Fusion | D-D | N/A (no tritium) | kdp | **4.0** |
| 04 | hb11 | p-B11 | N/A (no tritium) | kdp | **4.0** |
| 05 | Thea Energy | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 06 | Pale Blue | p-B11 | N/A (no tritium) | (none) | **5.0** |
| 07 | Pacific Fusion | D-T | TBD → Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 08 | Helion Energy | D-He³ | Other/hybrid | helium3 | **2.0** |
| 09 | Proxima Fusion | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 10 | Gauss Fusion | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 11 | Realta Fusion | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 12 | OpenStar Technologies | D-T | Solid breeder | tritium, lithium6, beryllium | **2.5** |
| 13 | Avalanche Energy | D-T | TBD → Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 14 | General Fusion | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 15 | Zap Energy | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 16 | Acceleron Fusion | D-T | TBD → Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 17a | Xcimer Energy | D-T | Molten salt | tritium, lithium6, beryllium, flibe, kdp | **1.0** |
| 17b | Focused Energy | D-T | Liquid metal | tritium, lithium6, vanadium, kdp | **2.0** |
| 18 | TAE Technologies | p-B11 | N/A (no tritium) | (none) | **5.0** |
| 19 | Zephyr Fusion | D-He³ | N/A (no tritium) | helium3 | **2.0** |
| 20a | Type One Energy | D-T | Solid breeder | tritium, lithium6, beryllium | **2.5** |
| 20b | Renaissance Fusion | D-T | Other/hybrid | tritium, lithium6, beryllium | **2.5** |
| 21 | Tokamak Energy | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 22 | First Light Fusion | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 23 | Marvel Fusion | p-B11 | N/A (no tritium) | kdp | **4.0** |
| 24 | LPPFusion | p-B11 | N/A (no tritium) | (none) | **5.0** |
| 25 | Intensity Energy | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 26 | Inertia Enterprises | D-T | Liquid metal | tritium, lithium6, vanadium, kdp | **2.0** |
| 27 | EMC2 / Polywell | D-T | TBD → Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 28 | Energy Singularity | D-T | TBD → Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 29 | Firefly Fusion | D-T | TBD → Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 30 | Inertia Enterprises (NIF Comm.) | D-T | Liquid metal | tritium, lithium6, vanadium, kdp | **2.0** |
| 31 | Blue Laser Fusion | D-T | Liquid metal | tritium, lithium6, vanadium, kdp | **2.0** |
| 32 | GenF Systems | D-T | Liquid metal | tritium, lithium6, vanadium, kdp | **2.0** |
| 33 | Neo / BEST | D-T | TBD → Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 35 | Deutelio (PoloMac) | D-D | N/A (no tritium) | (none) | **5.0** |
| 36 | Helical Fusion | D-T | Liquid metal | tritium, lithium6, vanadium | **3.0** |
| 37 | NearStar Fusion | D-D | TBD → Liquid metal | (none) | **5.0** |
| 38 | SHINE Technologies | D-T | N/A (non-power) | tritium | **4.0** |
| 39 | ENN Energy | p-B11 | N/A (no tritium) | (none) | **5.0** |

### Score distribution

- **5.0 (6 concepts)**: Aneutronic fuels without laser driver — Sonofusion, Pale Blue, TAE, LPPFusion, Deutelio, ENN. Also NearStar (D-D MIF) and Pacific MagLIF... wait, MagLIF is D-T so not at 5.0. **NearStar at 5.0** because D-D + TBD blanket (defaulted to liquid metal but D-D doesn't trigger li6/vanadium since fuel is the gate).
- **4.0 (3 concepts)**: D-D Cortex with KDP laser; p-B11 hb11/Marvel with KDP laser; SHINE D-T non-power neutron source (tritium-only trigger, no breeding blanket).
- **3.0 (15 concepts)**: D-T concepts with Liquid metal (or TBD→Liquid metal) blanket — the modal D-T pattern. Triggers tritium+lithium6+vanadium = weight 2.0 → score 3.0.
- **2.5 (3 concepts)**: D-T concepts with Solid breeder or Other/hybrid blanket (HCPB pebble bed). Triggers tritium+lithium6+beryllium = weight 2.5 → score 2.5.
- **2.0 (8 concepts)**: D-He³ Helion and Zephyr (helium3 weight 3.0 alone drives to 2.0); D-T DPSSL concepts with liquid metal blanket (Focused, Inertia×2, Blue Laser, GenF) — KDP penalty pushes them down; CFS with Molten salt (tritium+li6+Be+flibe = weight 3.0).
- **1.0 (1 concept)**: Xcimer Energy — D-T + Molten salt + Gas Laser (KrF) stacks ALL the major triggers (tritium+li6+Be+flibe+kdp = weight 4.0) to floor at 1.0.

### Notable score patterns

**Xcimer at floor (1.0) is the single worst supply-chain score.** D-T fuel + FLiBe molten salt blanket + KrF gas laser stacks every major bottleneck simultaneously. This is the framework correctly identifying that Xcimer's commercial supply chain has the most exposure of any concept in the matrix.

**CFS at 2.0 despite no laser driver.** FLiBe choice (Molten salt) adds the FLiBe penalty (0.5) on top of the standard D-T tritium+li6+Be stack. CFS pays a real supply chain cost for choosing FLiBe over liquid metal blankets.

**Most D-T concepts cluster at 3.0** (15 of 40). The modal pattern is D-T + Liquid metal blanket → tritium+li6+vanadium → weight 2.0 → score 3.0. The framework treats all D-T MFE and most D-T MIF concepts as having similar supply-chain risk, which is honest — they all face the same Li-6 enrichment bottleneck.

**TBD-blanket concepts (8 total) all score 3.0**: Pacific MagLIF, Avalanche, Acceleron, EMC2 Polywell, Energy Singularity, Firefly, BEST, NearStar. The TBD → Liquid metal default treats them identically to confirmed-liquid-metal concepts. The diagnostic block records `blanket_assumed: liquid_metal_default` for transparency.

**Helion and Zephyr at 2.0 despite aneutronic-leaning D-He³** — the He-3 supply bottleneck (weight 3.0) is so severe it dominates the score on its own. This is the framework correctly identifying that D-He³ is a *worse* supply chain bet than D-T despite being "cleaner" on the customization axis, because terrestrial He-3 supply is effectively zero.

**SHINE at 4.0** — D-T fuel but no breeding blanket (N/A non-power). Tritium is the only trigger (weight 1.0 → score 4.0). The framework correctly differentiates SHINE's neutron-source business model from full fusion-power concepts that need full breeding infrastructure.

**Aneutronic concepts without lasers (Sonofusion, Pale Blue, TAE, LPPFusion, Deutelio, ENN) score 5.0.** Zero triggers because (a) no D-T or D-He³ fuel, (b) no laser driver. Pale Blue mirror with p-B11 is the best of both worlds on this axis.

---

## Files touched

```
exploration/scoring_v2/weights/default.yaml                          # add supply_chain axis with inline severity weights
exploration/scoring_v2/embeddings/rulebook.py                        # add 2 embeddings + 2 helpers
exploration/scoring_v2/lookup_bottlenecks.yaml                       # NEW: bottleneck metadata (no weights)
exploration/scoring_v2/features/*.yaml                               # 39 files: append supply_chain_diagnostics block
exploration/scoring_v2/scripts/populate_supply_chain_diagnostics.py  # NEW: idempotent diagnostic population
tests/scoring_v2/test_supply_chain.py                                # NEW: acceptance tests
.project/active/scoring-v2-supply-chain-slice/design.md              # NEW: this spec + planning doc
.project/active/scoring-v2-supply-chain-slice/implementation_notes.md # NEW: implementation tracking
```

---

## Coordination notes

### Relationship to v5 modularity restructure

Independent. Both touch `weights/default.yaml` but different sections (`manufacturability_scale_out` vs new `supply_chain`). Can land in either order; if same PR, combine the YAML edits.

### Schema dependencies

All four trigger features (`Fuel`, `Blanket Config`, `Confinement Family`, `Primary Heating`) are in the v0.3.0 ontology (`schema.md`, 2026-05-12). **No schema changes needed.**

Verify before implementation:
- The schema columns are populated with their controlled-vocabulary values in all 39 feature files (no leftover free-text from the prior schema).
- Feature-file keys use the snake_case convention (`fuel`, `blanket_config`, `confinement_family`, `primary_heating`) that the embedding `inputs=` list expects. If the extractor uses different key names, adjust the embedding declarations.

Specifically check:
- `Blanket Config` value coverage: every concept should have one of the 7 controlled values (`Liquid metal`, `Molten salt`, `Solid breeder`, `Other/hybrid`, `N/A (no tritium)`, `N/A (non-power)`, `TBD`). The v0.3.0 schema explicitly renamed and consolidated this column — any feature files extracted under v0.2.x need re-extraction.
- `Primary Heating` value coverage: laser concepts should use one of the five `Laser (*)` values, not the legacy `Laser` (which doesn't exist in v0.3.0).
- OpenStar's blanket: the schema's `Solid breeder` definition references HCPB (which contains Be). OpenStar's pure Li₂O ceramic blanket may need to be classified as `Other/hybrid` to avoid the beryllium trigger, OR a per-concept override may be needed. The score anchor test for OpenStar (3.0) depends on this resolution.

### Other slices

- Non-Standard mvs bugfix: independent, different files
- v5 modularity restructure: independent, separate axis
- Slice 2 (component_modularity): independent, separate axis

---

## Implementation notes for Claude Code

- **All trigger logic uses controlled-vocabulary equality checks**, not substring matching. The v0.3.0 schema's `Blanket Config` is a controlled vocabulary (7 values: `Liquid metal`, `Molten salt`, `Solid breeder`, `Other/hybrid`, `N/A (no tritium)`, `N/A (non-power)`, `TBD`), which means triggers can use set-membership tests cleanly. This is materially more robust than the substring approach the previous draft used against free-text strings.

- **The diagnostic block emission ordering should be stable**. Sort the `bottlenecks_triggered` dict alphabetically when emitting to feature YAML for human readability. Don't rely on dict insertion order being meaningful.

- **Weight loading pattern**: examine how Reid's framework loads `lookup_family_weights.yaml` in the slice 2 component-modularity code. Whatever pattern is used there is the right pattern here. The injection vs. module-cache choice is a framework convention question.

- **Schema feature key naming**: the v0.3.0 schema document (`schema.md`) uses title-case column names (`Fuel`, `Blanket Config`, etc.), but feature files typically use snake_case keys (`fuel`, `blanket_config`). The embedding `inputs=` list uses snake_case to match feature-file convention. Verify the extractor's output key naming before implementation; adjust if needed.

- **`supply_chain_score` is a single-input embedding** (just applies `max(1.0, 5.0 - x)`). If the framework distinguishes derived/passthrough embeddings from substantive ones, use the appropriate annotation. If not, standard `@embedding` is fine.

- **Failure mode for missing weights**: `_load_bottleneck_weights` raises if any of the seven bottleneck weights are absent. This is intentional — fail loudly rather than silently default to zero. If the analyst removes a weight from `default.yaml`, the framework should refuse to score rather than silently produce wrong scores.

- **Feature value validation**: before computing scores, verify that all 39 feature files have v0.3.0 schema values populated (not legacy free-text). The acceptance tests will catch most issues, but `Blanket Config` is the highest-risk field — any leftover v0.2.x free-text strings (`"HCPB pebble"`, `"FLiBe blanket"`, `"Liquid Li wall"`) won't match the controlled vocabulary and will produce zero bottleneck triggers (giving wrong score 5.0).

---

## Open questions worth flagging (for future versions)

These don't block implementation but are worth raising in the design.md for the slice:

1. **Helion's closed He-3 cycle mitigation** — should the framework conditionally suppress the He-3 bottleneck for Helion specifically based on their published closed-cycle claim? Current implementation does not. If desired, would need a new feature like `claims_internal_he3_breeding: bool` and a small modification to the helium3 trigger.

2. **KDP/DKDP weight** — currently 0.5. If laser-optics manufacturing is more binding at fleet scale than assumed, easy one-line edit in `default.yaml` to promote to 1.0 (Severe). Effect: DPSSL D-T concepts drop from 1.5 to 1.0 (joining Xcimer at floor); aneutronic laser concepts drop from 4.5 to 4.0.

3. **Tritium self-breeding mitigation** — similar to Helion's claim, all D-T concepts plan to self-breed tritium from Li-6. Should the framework suppress the tritium bottleneck for D-T concepts demonstrating breeding ratio > 1.0? Current implementation does not.

4. **Vanadium scoping precision** — the v0.3.0 schema's `Liquid metal` blanket category groups LiPb, pure Li, and Li-LiH together. LiPb is RAFM-steel-compatible (doesn't strictly require V), while pure Li requires V-Cr-Ti. The current rule fires vanadium for all Liquid metal blankets, which over-penalizes LiPb concepts. Two options if precision matters: (a) extend the schema with a sub-classification, or (b) use per-concept feature overrides for LiPb concepts. Defer until a Liquid-metal-LiPb concept appears in the matrix and the over-penalty matters.

5. **OpenStar's ceramic blanket** — the schema's `Solid breeder` definition explicitly references HCPB with Be neutron multiplier, but OpenStar uses pure Li₂O ceramic without Be. Need to decide whether OpenStar should be classified as `Solid breeder` (triggering Be) or `Other/hybrid` (also triggering Be, conservatively) or some new sub-category. Per-concept feature override may be needed to suppress the Be trigger for OpenStar specifically.
