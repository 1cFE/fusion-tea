# Implementation Spec: Upper Capacity Factor Scoring Axis

**Status:** Ready for implementation
**Owner:** Mallory
**Created:** 2026-05-19
**Branch:** `concept-downselect`
**Target directory:** `.project/active/scoring-v2-upper-cf-slice/` (new slice — sibling to existing modularity, supply chain, plant complexity, and customization slices)
**Schema version:** v0.3.0 (`schema.md`, 2026-05-12)

This is a Claude Code implementation spec for the Upper Capacity Factor axis. Same structural pattern as Supply Chain and Plant Complexity: penalty-based scoring with severity weights co-located in `weights/default.yaml`.

---

## Summary

Build a new **Upper Capacity Factor** scoring axis as a peer of Modularity, Supply Chain, Plant Complexity, and Customization in `weights/default.yaml`. The axis produces a deterministic 1.0–5.0 score per concept representing the **maximum capacity factor physically achievable** if the physics works as intended.

This is an *upper-bound* score: it asks how high CF *could* go, not how high it actually does. Technology immaturity, supply chain bottlenecks, plant complexity issues, and operational learning curves all live in other axes. This axis isolates the ceiling imposed by architectural and operational choices.

### Score formula

```
upper_cf_score = max(1.0, 5.0 - operational_penalty_weight)

where operational_penalty_weight = sum of severity weights of triggered operational penalties
```

Same structural pattern as Supply Chain and Plant Complexity. Higher score = higher achievable capacity factor.

### What the score measures

**Question the score answers:** *Assuming the physics works perfectly, what's the maximum capacity factor this architecture can theoretically reach?*

The fusion literature establishes ~90% as the hard upper bound for *any* power plant (standard maintenance parameter μ = 0.1). From that ceiling, three operational factors drive CF reductions:

1. **Pulsed operation** — dwell time between pulses for chamber recovery, recharge, plasma re-initiation
2. **Neutronic fuel** — 14 MeV (D-T) or 2.45 MeV (D-D) neutrons damage components and force scheduled replacement outages
3. **Non-renewable blanket** — solid or static blankets degrade under neutron flux and require physical replacement; liquid-metal flowing blankets self-renew

### Key design choices

- **Penalty-based for consistency with Supply Chain and Plant Complexity.** Per analyst direction ("scoring must be consistent with other axes"). Bonuses for steady-state, aneutronic fuel, and liquid blanket are reframed as penalties for the alternatives (pulsed, neutronic, static blanket).
- **Weights live in `weights/default.yaml`** under the upper_cf axis. All three operational penalty weights visible in one place.
- **All triggers use existing v0.3.0 schema features.** Specifically: `Fuel`, `Blanket Config`, `Operation Mode`. No new features required.
- **Penalty ordering reflects relative impact**: neutronic fuel > non-renewable blanket (per analyst direction — "[liquid waterfall bonus] should be theoretically slightly less than the bonus for aneutronic fuels").

### Source of severity weights

From the fusion CF literature:

- **Pulsed → ~10-15% CF reduction** vs steady-state (dwell + recharge), but recent grid studies (Schwartz et al., Joule 2023) find this has "little impact on marginal value" when thermal storage is integrated. Moderate penalty.
- **Neutronic fuel → 10-20% CF reduction** from blanket/PFC replacement schedules; literature notes "durability < 0.7 FPY would lead to poor economic performance as the capacity factor would be < 70%." Severe penalty.
- **Non-renewable blanket → 5-10% additional CF reduction** when stacked on neutronic fuel (forced replacements every 3-5 FPY). Moderate penalty.

The aneutronic vs. neutronic gap is intentionally larger than the liquid vs. solid blanket gap, matching the analyst's ordering direction.

### Penalty list (3 entries)

| Penalty | Tier | Weight | Trigger feature(s) |
|---|---|---|---|
| Pulsed operation | Moderate | 0.5 | `Operation Mode` |
| Neutronic fuel | Severe | 1.0 | `Fuel` |
| Non-renewable blanket (conditional on neutronic) | Moderate | 0.5 | `Fuel`, `Blanket Config` |

---

## Changes summary

| # | Change | Touches |
|---|---|---|
| A | Add `upper_cf` axis with inline penalty weights to `weights/default.yaml` | `weights/default.yaml` |
| B | Implement `operational_penalty_weight` and `upper_cf_score` embeddings | `embeddings/rulebook.py` |
| C | Create `lookup_upper_cf_penalties.yaml` metadata file (no weights) | `lookup_upper_cf_penalties.yaml` (new) |
| D | Add `upper_cf_diagnostics` derived block per feature file | `features/*.yaml` (39 files) |
| E | Add acceptance tests | `tests/scoring_v2/test_upper_cf.py` (new) |

---

## Change A: M&SO axis registration with inline weights

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
customization:
  # ... existing customization weights ...

# NEW axis added by this spec
upper_cf:
  upper_cf_score: 1.0                              # axis-level M&SO weight
  operational_penalty_weights:                     # per-penalty severity tuning
    pulsed_operation:       0.5                    # Moderate: dwell + recharge between pulses
    neutronic_fuel:         1.0                    # Severe: forced replacement outages
    non_renewable_blanket:  0.5                    # Moderate: solid/static blanket replacement
```

### Why these specific weights

**Neutronic fuel = Severe (1.0)** because forced replacement of blanket and PFCs is the dominant CF driver in fusion CF studies. Schwartz et al. (Joule 2023) find blanket replacement costs and durability are "the most important characteristics of a fusion plant" for economic viability. The Severe tier reflects that this is a categorical change in achievable CF, not a tunable parameter.

**Pulsed operation = Moderate (0.5)** because recent grid studies find pulsed vs steady-state has "little impact on marginal value" when integrated with thermal storage (Schwartz et al., 2024). The penalty is real (dwell time reduces nameplate CF) but smaller in fleet-scale economic terms than the neutronic penalty.

**Non-renewable blanket = Moderate (0.5)** stacked on neutronic. The penalty fires only when fuel is neutronic AND blanket is static (Solid breeder, Molten salt, Other/hybrid). For aneutronic concepts the blanket type is irrelevant — they don't have a breeding blanket. Per analyst direction, the liquid-blanket bonus is "theoretically slightly less than the bonus for aneutronic fuels," which in penalty terms means non_renewable_blanket < neutronic_fuel weight.

### Why three flags and not more

Other CF drivers exist (target factory recovery time, current drive reliability, disruption frequency, etc.) but they're captured by **Plant Complexity** as standalone subsystem flags. Adding them here would double-count. This axis specifically isolates the *architecture-mandated* CF ceiling, not the engineering-implementation CF ceiling.

---

## Change B: Embeddings in `rulebook.py`

### Implementation

Add to `embeddings/rulebook.py` after the existing customization embeddings:

```python
# ===========================================================================
# Upper Capacity Factor Axis
#
# Deterministic scoring of the theoretical maximum capacity factor based on
# operational architecture and fuel cycle. Weights are loaded from
# weights/default.yaml under the upper_cf axis.
#
# All trigger logic uses v0.3.0 schema controlled vocabulary (Fuel, Blanket
# Config, Operation Mode). No substring matching against free-text.
# ===========================================================================

# Penalty names (matched with default.yaml weight keys)
_UPPER_CF_PENALTY_NAMES = [
    "pulsed_operation",
    "neutronic_fuel",
    "non_renewable_blanket",
]

# Fuel values that produce neutrons (both D-T and D-D)
_NEUTRONIC_FUELS = {"D-T", "D-D"}

# Blanket Config values that don't self-renew under neutron flux
# (Liquid metal blankets continuously circulate, refreshing damaged material)
_STATIC_BLANKET_VALUES = {"Solid breeder", "Molten salt", "Other/hybrid"}

# Operation Mode values that incur the pulsed-operation penalty
# (Steady-state and Quasi-steady avoid the penalty per analyst direction)
_PULSED_OPERATION_MODES = {"Pulsed"}


def _load_upper_cf_weights(weights_yaml: dict) -> dict[str, float]:
    """Extract per-penalty severity weights from weights/default.yaml.

    Returns dict[penalty_name -> weight]. Raises if any expected penalty
    is missing — fail loudly rather than silently using a default.
    """
    cf_axis = weights_yaml.get("upper_cf", {})
    raw = cf_axis.get("operational_penalty_weights", {})
    missing = [p for p in _UPPER_CF_PENALTY_NAMES if p not in raw]
    if missing:
        raise ValueError(
            f"weights/default.yaml upper_cf.operational_penalty_weights is "
            f"missing required keys: {missing}. All three penalty weights "
            f"must be specified."
        )
    return {p: float(raw[p]) for p in _UPPER_CF_PENALTY_NAMES}


def _compute_triggered_cf_penalties(
    fuel: str,
    blanket_config: str,
    operation_mode: str,
    weights: dict[str, float],
) -> dict[str, float]:
    """Returns dict of {penalty_name: weight} for triggered CF penalties.

    Pure function — given the same inputs and weights, always returns the
    same dict.

    All trigger logic keys off v0.3.0 schema controlled-vocabulary features:
        fuel             (enum: D-T, D-D, D-He3, p-B11, Unknown)
        blanket_config   (enum: Liquid metal, Molten salt, Solid breeder,
                                Other/hybrid, N/A (no tritium),
                                N/A (non-power), TBD)
        operation_mode   (enum: Steady-state, Quasi-steady, Pulsed)
    """
    fuel = fuel or ""
    raw_blanket = blanket_config or ""
    op_mode = operation_mode or ""

    # TBD blanket → default to "Liquid metal". This is the most common choice
    # across all (Confinement Family, Fuel) combinations in the v3 matrix.
    # For Upper CF specifically: liquid metal is renewable (self-circulating),
    # so a TBD-defaulted-to-liquid-metal blanket does NOT trigger the
    # non_renewable_blanket penalty. The diagnostic block records
    # `blanket_assumed: liquid_metal_default` so the UI can surface the
    # inferred value with a confidence flag.
    blanket = "Liquid metal" if raw_blanket == "TBD" else raw_blanket

    triggered = {}

    # Pulsed operation: dwell + recharge between pulses
    # Steady-state and Quasi-steady operation avoid this penalty
    if op_mode in _PULSED_OPERATION_MODES:
        triggered["pulsed_operation"] = weights["pulsed_operation"]

    # Neutronic fuel: forced component replacement schedules
    # Aneutronic (p-B11) and low-neutron (D-He3) fuels avoid this
    if fuel in _NEUTRONIC_FUELS:
        triggered["neutronic_fuel"] = weights["neutronic_fuel"]

        # Non-renewable blanket: only relevant alongside neutronic fuel.
        # Liquid metal blankets self-renew (HYLIFE-2, General Fusion vortex,
        # Renaissance Li-LiH flowing wall) and avoid this penalty.
        # SHINE-class (N/A non-power) and aneutronic concepts skip both.
        # TBD blankets default to Liquid metal (above) and therefore do NOT
        # trigger this penalty.
        if blanket in _STATIC_BLANKET_VALUES:
            triggered["non_renewable_blanket"] = weights["non_renewable_blanket"]

    return triggered


@embedding(
    "operational_penalty_weight",
    inputs=["fuel", "blanket_config", "operation_mode"],
)
def _operational_penalty_weight(
    fuel: str,
    blanket_config: str,
    operation_mode: str,
    *,
    weights_yaml: dict,
) -> float:
    """Sum of severity weights of all triggered CF penalties.

    Loads severity weights from weights_yaml at call time, allowing weight
    edits in weights/default.yaml to take effect without code changes.
    """
    sev_weights = _load_upper_cf_weights(weights_yaml)
    triggered = _compute_triggered_cf_penalties(
        fuel, blanket_config, operation_mode, sev_weights,
    )
    return sum(triggered.values())


@embedding(
    "upper_cf_score",
    inputs=["operational_penalty_weight"],
)
def _upper_cf_score(operational_penalty_weight: float) -> float:
    """Upper capacity factor score: 1.0 (floor) to 5.0 (no penalties).

    Formula: max(1.0, 5.0 - operational_penalty_weight)

    Higher score = higher theoretical maximum capacity factor.
    """
    return max(1.0, 5.0 - operational_penalty_weight)
```

### Why non_renewable_blanket is conditional on neutronic_fuel

In the v0.3.0 schema, aneutronic concepts don't have breeding blankets — they're typically `N/A (no tritium)`. A `Solid breeder` blanket on an aneutronic concept would be a schema inconsistency. By gating the non_renewable_blanket penalty on neutronic fuel, the framework correctly avoids penalizing aneutronic concepts for blanket choice (which doesn't apply to them).

This also means liquid-metal blankets on aneutronic concepts (rare but possible — e.g., for chamber wall protection in ICF) don't get an artificial bonus they don't deserve.

### Why pulsed isn't conditional on anything else

Pulsed operation independently reduces CF regardless of fuel or blanket. Helion (D-He³ + Other/hybrid + Pulsed) takes the pulsed penalty even though it has neither neutronic fuel nor a problematic blanket. The dwell time exists regardless.

---

## Change C: `lookup_upper_cf_penalties.yaml` (metadata only)

### New file: `exploration/scoring_v2/lookup_upper_cf_penalties.yaml`

```yaml
# Upper capacity factor penalty metadata.
#
# Numerical severity weights are NOT here — they live in
# weights/default.yaml under upper_cf.operational_penalty_weights
# to keep the tuning surface co-located with modularity, supply chain,
# plant complexity, and customization weights.
#
# Each entry documents:
#   - tier: severity classification (matches the weight in default.yaml)
#   - trigger: human-readable description of when this penalty fires
#   - features_used: which v0.3.0 schema columns the trigger reads
#   - cf_impact: typical capacity factor impact from literature
#   - rationale: why this severity tier is appropriate
#
# The authoritative trigger logic lives in
# rulebook.py:_compute_triggered_cf_penalties().

pulsed_operation:
  tier: Moderate
  trigger: "Fires when Operation Mode = Pulsed"
  features_used: [Operation Mode]
  cf_impact: |
    Typical 10-15% CF reduction vs steady-state from dwell time between
    pulses. Recent grid studies (Schwartz et al., Joule 2023) find pulsed
    vs steady-state has little impact on marginal value when thermal
    storage is integrated, but the raw nameplate CF reduction is real.
  rationale: |
    Pulsed concepts require dwell time between shots for chamber recovery,
    plasma re-initiation, and capacitor recharge. Steady-state and
    Quasi-steady operation avoid this penalty per analyst direction.
    Moderate weight reflects that thermal storage and grid integration
    can recover much of the lost economic value, even though the raw
    plant CF takes a hit.

neutronic_fuel:
  tier: Severe
  trigger: "Fires when Fuel in {D-T, D-D}"
  features_used: [Fuel]
  cf_impact: |
    Typical 10-20% CF reduction from blanket and plasma-facing component
    replacement schedules. Literature notes durability <0.7 FPY (full-power
    years) drives CF below 70%; even with 5 FPY durability, replacement
    outages cap CF around 80-85%.
  rationale: |
    14 MeV (D-T) and 2.45 MeV (D-D) neutrons activate and damage components
    that must be replaced on a multi-year cycle. Aneutronic (p-B11) and
    low-neutron (D-He3) fuels avoid this — they produce only side-reaction
    neutrons at much lower rates, with components designed for the full
    plant lifetime. The largest single CF driver in the framework.

non_renewable_blanket:
  tier: Moderate
  trigger: |
    Fires when Fuel in {D-T, D-D} AND Blanket Config in
    {Solid breeder, Molten salt, Other/hybrid}.
    Does NOT trigger if Fuel is aneutronic or blanket is Liquid metal
    or N/A (any flavor).
  features_used: [Fuel, Blanket Config]
  cf_impact: |
    Typical 5-10% additional CF reduction (stacked on neutronic_fuel)
    from forced blanket replacement outages every 3-5 full-power-years.
    Liquid metal flowing blankets (HYLIFE-2, General Fusion vortex,
    Renaissance Li-LiH walls) self-renew and avoid the discrete
    replacement outage cost.
  rationale: |
    Solid breeder pebble beds (HCPB), molten salt blankets (FLiBe), and
    hybrid blankets degrade structurally under sustained neutron flux
    and require physical replacement. Liquid metal blankets continuously
    circulate, with damaged material flushed out and replaced by fresh
    material on the fly — the blanket effectively never needs scheduled
    replacement. Per analyst direction, the liquid-blanket bonus is
    "theoretically slightly less than the bonus for aneutronic fuels,"
    so this penalty (Moderate, 0.5) is smaller than the neutronic fuel
    penalty (Severe, 1.0).
```

---

## Change D: Feature-file diagnostics

Add a derived block to each concept's feature file:

### Diagnostic block format

```yaml
# In each features/{ID}-{name}.yaml file, append:
upper_cf_diagnostics:
  penalties_triggered:
    {penalty_name}: {weight}     # one entry per triggered penalty
  operational_penalty_weight: {sum}
  upper_cf_score: {score}
```

### Examples

**Pale Blue (p-B11, N/A, Steady-state)** — best case:

```yaml
upper_cf_diagnostics:
  penalties_triggered: {}
  operational_penalty_weight: 0.0
  upper_cf_score: 5.0
```

**Helion (D-He3, Other/hybrid, Pulsed)** — aneutronic but pulsed:

```yaml
upper_cf_diagnostics:
  penalties_triggered:
    pulsed_operation: 0.5
  operational_penalty_weight: 0.5
  upper_cf_score: 4.5
```

**CFS ARC (D-T, Molten salt, Quasi-steady)** — neutronic with static blanket:

```yaml
upper_cf_diagnostics:
  penalties_triggered:
    neutronic_fuel: 1.0
    non_renewable_blanket: 0.5
  operational_penalty_weight: 1.5
  upper_cf_score: 3.5
```

**Helical Fusion (D-T, Liquid metal, Steady-state)** — best D-T case:

```yaml
upper_cf_diagnostics:
  penalties_triggered:
    neutronic_fuel: 1.0
  operational_penalty_weight: 1.0
  upper_cf_score: 4.0
```

**Pacific MagLIF (D-T, Solid breeder, Pulsed)** — worst case stack:

```yaml
upper_cf_diagnostics:
  penalties_triggered:
    pulsed_operation: 0.5
    neutronic_fuel: 1.0
    non_renewable_blanket: 0.5
  operational_penalty_weight: 2.0
  upper_cf_score: 3.0
```

### Population approach

Write `scripts/populate_upper_cf_diagnostics.py` to programmatically populate the diagnostic block in all 39 feature files. Idempotent and re-runnable after weight changes. Same pattern as the diagnostic population scripts for the other axes.

---

## Change E: Acceptance tests

### New test file: `tests/scoring_v2/test_upper_cf.py`

```python
"""Acceptance tests for the upper capacity factor scoring axis."""
import pytest
import yaml
from pathlib import Path

from exploration.scoring_v2.embeddings.rulebook import (
    REGISTRY,
    _compute_triggered_cf_penalties,
    _load_upper_cf_weights,
)


_BASE = Path(__file__).parent.parent.parent / "exploration" / "scoring_v2"
_WEIGHTS_YAML = yaml.safe_load((_BASE / "weights" / "default.yaml").read_text())
_PENALTY_WEIGHTS = _load_upper_cf_weights(_WEIGHTS_YAML)


# ============================================================================
# Weights are visible in default.yaml
# ============================================================================

class TestWeightsExposedInDefaultYaml:
    """Verify the three penalty weights are visible in weights/default.yaml."""

    def test_upper_cf_axis_exists(self):
        assert "upper_cf" in _WEIGHTS_YAML

    def test_axis_weight_is_one(self):
        assert _WEIGHTS_YAML["upper_cf"]["upper_cf_score"] == 1.0

    def test_all_three_penalty_weights_present(self):
        weights = _WEIGHTS_YAML["upper_cf"]["operational_penalty_weights"]
        for name in ["pulsed_operation", "neutronic_fuel", "non_renewable_blanket"]:
            assert name in weights

    def test_neutronic_is_severe(self):
        """Per analyst direction, aneutronic bonus > liquid blanket bonus."""
        assert _PENALTY_WEIGHTS["neutronic_fuel"] == 1.0  # Severe
        assert _PENALTY_WEIGHTS["pulsed_operation"] == 0.5  # Moderate
        assert _PENALTY_WEIGHTS["non_renewable_blanket"] == 0.5  # Moderate

    def test_neutronic_penalty_exceeds_blanket_penalty(self):
        """Verify ordering: aneutronic bonus > liquid blanket bonus
        (in penalty terms: neutronic > non_renewable_blanket)."""
        assert _PENALTY_WEIGHTS["neutronic_fuel"] > _PENALTY_WEIGHTS["non_renewable_blanket"]

    def test_missing_weight_raises(self):
        """If any penalty weight is missing, _load_upper_cf_weights raises."""
        partial = {"upper_cf": {"operational_penalty_weights": {"pulsed_operation": 0.5}}}
        with pytest.raises(ValueError, match="missing required keys"):
            _load_upper_cf_weights(partial)


# ============================================================================
# Trigger rule tests
# ============================================================================

def _triggered(fuel, blanket, op_mode):
    return _compute_triggered_cf_penalties(fuel, blanket, op_mode, _PENALTY_WEIGHTS)


class TestTriggerRules:
    """Verify penalties fire correctly using v0.3.0 schema controlled vocabulary."""

    def test_pulsed_fires_for_pulsed_only(self):
        # Pulsed fires
        assert "pulsed_operation" in _triggered("p-B11", "N/A (no tritium)", "Pulsed")
        # Steady-state doesn't fire
        assert "pulsed_operation" not in _triggered("p-B11", "N/A (no tritium)", "Steady-state")
        # Quasi-steady doesn't fire (per analyst direction)
        assert "pulsed_operation" not in _triggered("D-T", "Molten salt", "Quasi-steady")

    def test_neutronic_fires_for_dt_and_dd(self):
        assert "neutronic_fuel" in _triggered("D-T", "Solid breeder", "Steady-state")
        assert "neutronic_fuel" in _triggered("D-D", "N/A (no tritium)", "Pulsed")
        # Aneutronic doesn't fire
        assert "neutronic_fuel" not in _triggered("p-B11", "N/A (no tritium)", "Steady-state")
        assert "neutronic_fuel" not in _triggered("D-He3", "Other/hybrid", "Pulsed")

    def test_non_renewable_blanket_requires_neutronic_fuel(self):
        # Fires for D-T + static blanket
        assert "non_renewable_blanket" in _triggered("D-T", "Solid breeder", "Steady-state")
        assert "non_renewable_blanket" in _triggered("D-T", "Molten salt", "Steady-state")
        assert "non_renewable_blanket" in _triggered("D-T", "Other/hybrid", "Steady-state")
        # Doesn't fire for D-T + Liquid metal (self-renewing)
        assert "non_renewable_blanket" not in _triggered("D-T", "Liquid metal", "Steady-state")
        # Doesn't fire for D-T + N/A blanket (e.g., SHINE)
        assert "non_renewable_blanket" not in _triggered("D-T", "N/A (non-power)", "Steady-state")
        assert "non_renewable_blanket" not in _triggered("D-T", "N/A (no tritium)", "Steady-state")
        # Doesn't fire for D-T + TBD blanket (penalty waits for disclosure)
        assert "non_renewable_blanket" not in _triggered("D-T", "TBD", "Steady-state")
        # Doesn't fire for aneutronic regardless of blanket
        assert "non_renewable_blanket" not in _triggered("p-B11", "Solid breeder", "Pulsed")

    def test_liquid_blanket_avoids_blanket_penalty_dt(self):
        """Per analyst direction: liquid waterfall = theoretically no replacements."""
        triggered = _triggered("D-T", "Liquid metal", "Steady-state")
        assert "neutronic_fuel" in triggered
        assert "non_renewable_blanket" not in triggered


# ============================================================================
# Per-concept score anchors
# ============================================================================

def _score(concept_id: str) -> float:
    """Load a concept's features and return its upper_cf_score."""
    matches = list((_BASE / "features").glob(f"{concept_id}-*.yaml"))
    assert len(matches) == 1, f"Expected one feature file for {concept_id}"
    features = yaml.safe_load(matches[0].read_text())
    weight = REGISTRY["operational_penalty_weight"].fn(
        features.get("fuel"),
        features.get("blanket_config"),
        features.get("operation_mode"),
        weights_yaml=_WEIGHTS_YAML,
    )
    return REGISTRY["upper_cf_score"].fn(weight)


def test_aneutronic_steady_state_top_tier():
    """Aneutronic + steady-state concepts score 5.0 — no penalties."""
    # Pale Blue, TAE, Zephyr (D-He3 steady), ENN EHL-2
    for cid in ["06", "18", "19", "39"]:
        assert _score(cid) == 5.0

def test_aneutronic_pulsed_score_4_5():
    """Aneutronic + pulsed score 4.5 — only pulsed penalty."""
    # hb11, Marvel, LPP DPF, Helion (D-He3 pulsed)
    for cid in ["04", "08", "24", "25"]:
        assert _score(cid) == 4.5

def test_dt_liquid_blanket_steady_score_4(self):
    """D-T + Liquid metal + Steady-state scores 4.0 — only neutronic penalty.

    Best D-T case (Helical Fusion). Liquid blanket self-renews, no
    blanket replacement penalty.
    """
    assert _score("36") == 4.0

def test_shine_non_power_score_4(self):
    """SHINE: D-T but N/A (non-power) blanket avoids the blanket penalty.

    SHINE doesn't breed tritium; the blanket field is N/A, so the
    non_renewable_blanket penalty doesn't fire. Only the neutronic
    fuel penalty applies.
    """
    assert _score("38") == 4.0

def test_dt_static_blanket_steady_score_3_5(self):
    """D-T + static blanket + Steady-state scores 3.5."""
    # Many D-T stellarators, tokamaks at steady-state
    for cid in ["05", "09", "10", "11", "12", "13", "16", "20", "21", "22", "28", "29", "34"]:
        assert _score(cid) == 3.5

def test_dt_liquid_pulsed_score_3_5(self):
    """D-T + Liquid metal + Pulsed scores 3.5 (pulsed + neutronic, no blanket penalty)."""
    # General Fusion MTF, Zap Z-pinch, First Light, Intensity, Inertia
    for cid in ["14", "15", "23", "26", "31"]:
        assert _score(cid) == 3.5

def test_dt_static_pulsed_worst_case_score_3(self):
    """D-T + static blanket + Pulsed: worst case, all three penalties fire."""
    # Pacific MagLIF, Focused, Xcimer, Blue Laser, GenF French
    for cid in ["07", "17", "27", "32", "33"]:
        assert _score(cid) == 3.0

def test_dd_steady_score_4(self):
    """D-D + steady-state scores 4.0 — neutronic but blanket N/A."""
    assert _score("35") == 4.0  # Polomac

def test_dd_pulsed_score_3_5(self):
    """D-D + pulsed scores 3.5 — pulsed + neutronic."""
    for cid in ["02", "03", "37"]:  # Sonofusion, Cortex, NearStar
        assert _score(cid) == 3.5

def test_all_within_bounds():
    """Every concept scores in [1.0, 5.0]."""
    for cid in [f"{i:02d}" for i in range(1, 40)]:
        score = _score(cid)
        assert 1.0 <= score <= 5.0


# ============================================================================
# Weight tuning is functional
# ============================================================================

def test_increasing_pulsed_weight_drops_pulsed_concepts():
    """If pulsed penalty becomes Severe (1.0), Helion drops from 4.5 to 4.0."""
    custom = dict(_PENALTY_WEIGHTS)
    custom["pulsed_operation"] = 1.0
    triggered = _compute_triggered_cf_penalties("D-He3", "Other/hybrid", "Pulsed", custom)
    weight = sum(triggered.values())
    score = max(1.0, 5.0 - weight)
    assert score == 4.0

def test_promoting_blanket_penalty_drops_static_blanket_concepts():
    """If non_renewable_blanket becomes Severe (1.0), D-T static blanket drops further."""
    custom = dict(_PENALTY_WEIGHTS)
    custom["non_renewable_blanket"] = 1.0
    triggered = _compute_triggered_cf_penalties("D-T", "Solid breeder", "Steady-state", custom)
    weight = sum(triggered.values())
    score = max(1.0, 5.0 - weight)
    assert score == 3.0
```

---

## Predicted scores (all 39 concepts)

| Concept | Fuel | Blanket | OpMode | Penalties | Wt | **Score** |
|---|---|---|---|---|---|---|
| 01 CFS ARC | D-T | Molten salt | Quasi-steady | neutronic, non_renewable | 1.5 | **3.5** |
| 02 Sonofusion | D-D | N/A (no tritium) | Pulsed | pulsed, neutronic | 1.5 | **3.5** |
| 03 Cortex | D-D | Liquid metal | Pulsed | pulsed, neutronic | 1.5 | **3.5** |
| 04 hb11 | p-B11 | N/A (no tritium) | Pulsed | pulsed | 0.5 | **4.5** |
| 05 Thea planar | D-T | Molten salt | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 06 Pale Blue | p-B11 | N/A (no tritium) | Steady-state | (none) | 0.0 | **5.0** |
| 07 Pacific MagLIF | D-T | Solid breeder | Pulsed | pulsed, neutronic, non_renewable | 2.0 | **3.0** |
| 08 Helion | D-He3 | Other/hybrid | Pulsed | pulsed | 0.5 | **4.5** |
| 09 Proxima QI | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 10 Gauss HELIAS | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 11 Realta mirror | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 12 OpenStar | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 13 Avalanche | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 14 General Fusion MTF | D-T | Liquid metal | Pulsed | pulsed, neutronic | 1.5 | **3.5** |
| 15 Zap Z-pinch | D-T | Liquid metal | Pulsed | pulsed, neutronic | 1.5 | **3.5** |
| 16 Acceleron | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 17 Focused DPSSL | D-T | Solid breeder | Pulsed | pulsed, neutronic, non_renewable | 2.0 | **3.0** |
| 18 TAE | p-B11 | N/A (no tritium) | Steady-state | (none) | 0.0 | **5.0** |
| 19 Zephyr | D-He3 | N/A (no tritium) | Steady-state | (none) | 0.0 | **5.0** |
| 20 Type One Infinity | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 21 Renaissance | D-T | Other/hybrid | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 22 Tokamak Energy ST | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 23 First Light | D-T | Liquid metal | Pulsed | pulsed, neutronic | 1.5 | **3.5** |
| 24 Marvel | p-B11 | N/A (no tritium) | Pulsed | pulsed | 0.5 | **4.5** |
| 25 LPP DPF | p-B11 | N/A (no tritium) | Pulsed | pulsed | 0.5 | **4.5** |
| 26 Intensity heavy-ion | D-T | Liquid metal | Pulsed | pulsed, neutronic | 1.5 | **3.5** |
| 27 Xcimer KrF | D-T | Molten salt | Pulsed | pulsed, neutronic, non_renewable | 2.0 | **3.0** |
| 28 EMC2 Polywell | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 29 Energy Singularity | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 30 Firefly NTT | D-T | Molten salt | Quasi-steady | neutronic, non_renewable | 1.5 | **3.5** |
| 31 Inertia DPSSL | D-T | Liquid metal | Pulsed | pulsed, neutronic | 1.5 | **3.5** |
| 32 Blue Laser OEC | D-T | Solid breeder | Pulsed | pulsed, neutronic, non_renewable | 2.0 | **3.0** |
| 33 GenF French | D-T | Solid breeder | Pulsed | pulsed, neutronic, non_renewable | 2.0 | **3.0** |
| 34 Neo Fusion BEST | D-T | Solid breeder | Steady-state | neutronic, non_renewable | 1.5 | **3.5** |
| 35 Polomac | D-D | N/A (no tritium) | Steady-state | neutronic | 1.0 | **4.0** |
| 36 Helical Fusion | D-T | Liquid metal | Steady-state | neutronic | 1.0 | **4.0** |
| 37 NearStar MTIF | D-D | N/A (no tritium) | Pulsed | pulsed, neutronic | 1.5 | **3.5** |
| 38 SHINE | D-T | N/A (non-power) | Steady-state | neutronic | 1.0 | **4.0** |
| 39 ENN EHL-2 | p-B11 | N/A (no tritium) | Steady-state | (none) | 0.0 | **5.0** |

### Score distribution

- **5.0 (4 concepts)**: Aneutronic + steady-state — Pale Blue, TAE, Zephyr (D-He³ steady), ENN EHL-2. Framework ceiling.
- **4.5 (4 concepts)**: Aneutronic + pulsed — hb11, Marvel, LPP DPF, Helion (D-He³ pulsed). One Moderate penalty.
- **4.0 (3 concepts)**: D-T with liquid blanket + steady-state (Helical Fusion), or D-D steady (Polomac), or D-T non-power (SHINE). One Severe penalty, no other.
- **3.5 (23 concepts)**: The mixed middle — D-T steady-state with static blanket, D-T pulsed with liquid blanket, D-D pulsed. Two penalties summing to 1.5.
- **3.0 (5 concepts)**: D-T + static blanket + Pulsed — Pacific MagLIF, Focused, Xcimer, Blue Laser, GenF French. All three penalties stack.

---

## Notable score patterns

**Helion at 4.5 is striking.** D-He³ avoids the neutronic and non-renewable-blanket penalties; only the pulsed penalty applies. The framework correctly identifies that Helion's architectural choices target the theoretical CF ceiling — *if the D-He³ physics works*, Helion can run at higher CF than any D-T concept.

**Pale Blue and TAE at 5.0 (framework ceiling).** Steady-state aneutronic concepts with no penalties triggered. These represent the theoretical best-case CF: ~90% by the literature, the upper bound for any thermal power plant.

**Helical Fusion at 4.0 is the best D-T concept.** Steady-state + Liquid metal blanket means the only penalty is the neutronic fuel itself. The framework rewards Helical's design choice to use a flowing liquid blanket that self-renews — the same architectural advantage as HYLIFE-2.

**SHINE at 4.0** matches Helical Fusion. As a non-power neutron source, SHINE has `Blanket Config = N/A (non-power)` — no tritium breeding, no blanket replacement. Only the neutronic fuel penalty applies. Operationally, SHINE can run nearly continuously like a particle accelerator.

**CFS ARC at 3.5 (not 4.0).** Quasi-steady operation avoids the pulsed penalty, but Molten salt blanket triggers the non_renewable_blanket penalty. The framework distinguishes CFS (FLiBe blanket → replacement schedule) from Helical Fusion (liquid Li wall → self-renewing). Worth flagging because CFS markets ARC as having a "FLiBe blanket" — the framework treats this as static for CF purposes.

**The pulsed-vs-steady gap is 0.5 (Moderate).** Helion (4.5, pulsed) vs Zephyr (5.0, steady) shows the pulsed penalty in isolation. CFS ARC (3.5, quasi-steady) vs Pacific MagLIF (3.0, pulsed, same fuel and blanket type) shows the penalty applied within D-T. The gap is intentionally smaller than the neutronic-vs-aneutronic gap (1.0), per analyst direction.

**The 3.5 tier is the mixed middle (23 concepts, 59%)** — D-T concepts that pick *some* good operational choices but not all. D-T steady-state with static blanket (most stellarators), D-T pulsed with liquid blanket (most MIF and IFE concepts), D-D pulsed. The framework correctly identifies these as the operational mainstream.

**The 3.0 tier (5 concepts) is the worst case.** D-T + static blanket + Pulsed — all three penalties stack. Pacific MagLIF and most DPSSL D-T concepts. Operationally these concepts have the most replacement outages plus the most dwell time, capping CF lowest.

---

## Files touched

```
exploration/scoring_v2/weights/default.yaml                       # add upper_cf axis with inline penalty weights
exploration/scoring_v2/embeddings/rulebook.py                     # add 2 embeddings + 2 helpers
exploration/scoring_v2/lookup_upper_cf_penalties.yaml             # NEW: penalty metadata (no weights)
exploration/scoring_v2/features/*.yaml                            # 39 files: append upper_cf_diagnostics block
exploration/scoring_v2/scripts/populate_upper_cf_diagnostics.py    # NEW: idempotent diagnostic population
tests/scoring_v2/test_upper_cf.py                                  # NEW: acceptance tests
.project/active/scoring-v2-upper-cf-slice/design.md                # NEW: this spec + planning doc
.project/active/scoring-v2-upper-cf-slice/implementation_notes.md  # NEW: implementation tracking
```

---

## Coordination notes

### Relationship to other axes

Upper Capacity Factor is **independent** of Modularity, Supply Chain, Plant Complexity, and Customization. The five axes touch different sections of `weights/default.yaml` and different embeddings.

**Specifically not overlapping with Plant Complexity**: this axis isolates the *architecture-mandated* CF ceiling. Plant Complexity captures the engineering-implementation CF challenges (target factory recovery, current drive reliability, disruption frequency, etc.) as separate subsystem flags. The two axes complement rather than duplicate.

### Schema dependencies

All three trigger features (`Fuel`, `Blanket Config`, `Operation Mode`) are in the v0.3.0 ontology (`schema.md`, 2026-05-12). **No schema changes needed.**

Verify before implementation:
- `Operation Mode` value coverage: every concept must have one of {Steady-state, Quasi-steady, Pulsed}.
- `Blanket Config` consistency with neutronic fuel: D-T and D-D concepts should have a meaningful blanket value (not just always TBD). The non_renewable_blanket penalty depends on this distinction.

---

## Implementation notes for Claude Code

- **All trigger logic uses controlled-vocabulary equality checks**, not substring matching. The v0.3.0 schema's controlled vocabulary lets triggers use clean set-membership tests.

- **The diagnostic block emission ordering should be stable**. Sort the `penalties_triggered` dict alphabetically when emitting to feature YAML.

- **Weight loading pattern**: match how `_load_bottleneck_weights`, `_load_subsystem_weights`, and `_load_customization_weights` are implemented in the other axes.

- **Schema feature key naming**: snake_case in feature files (`fuel`, `blanket_config`, `operation_mode`).

- **Failure mode for missing weights**: `_load_upper_cf_weights` raises if any penalty weight is absent. Intentional — fail loudly rather than silently default to zero.

- **`upper_cf_score` is a single-input embedding** (just applies `max(1.0, 5.0 - x)`). Use the appropriate framework annotation if derived/passthrough embeddings are distinguished.

- **Conditional penalty logic**: `non_renewable_blanket` only fires when `neutronic_fuel` is already triggered. The implementation reflects this with nested logic, ensuring the conditional dependency is explicit.

---

## Open questions worth flagging (for future versions)

These don't block implementation but are worth raising in the design.md for the slice:

1. **Pulsed penalty for ICF**: The pulsed penalty applies uniformly to all `Pulsed` Operation Mode concepts. But ICF concepts at 10 Hz (50,000+ shots per day) operate quasi-continuously from a CF perspective — the dwell time per shot is 0.1 seconds. Should high-rep-rate ICF be reclassified? Current implementation treats all Pulsed as Pulsed; the analyst may want to add a `~1+ Hz` exemption later.

2. **Quasi-steady tokamaks**: CFS ARC and Firefly NTT use Quasi-steady operation (long pulses, brief dwell). Currently get full credit (no pulsed penalty). Defensible because the dwell-to-burn ratio is small, but worth confirming this is the intended treatment.

3. **D-He³ side-reaction neutrons**: D-He³ concepts produce some neutrons from D-D side reactions (~5% of fusion power). The framework currently treats D-He³ as fully aneutronic (no neutronic_fuel penalty). For very long-running plants, those side-reaction neutrons still drive some component activation. Worth flagging but probably not worth penalizing — the rate is so low that activation timescales are decades.

4. **Liquid metal blanket realism**: The framework gives Liquid metal blankets a full pass on the blanket penalty, assuming continuous self-renewal works as designed. In practice, liquid metal blankets have their own maintenance issues (MHD pressure drop, corrosion of structural materials, tritium permeation). These are captured under Supply Chain (vanadium) and Plant Complexity (liquid_metal_handling), but the CF impact may still be larger than the framework assumes. Consider tightening if liquid-metal concepts show unexpectedly high real-world CFs.

5. **TBD blanket on D-T concepts**: Currently, D-T concepts with `Blanket Config = TBD` trigger the neutronic_fuel penalty but NOT the non_renewable_blanket penalty (because TBD isn't in the static blanket set). Conservative interpretation: don't penalize for blanket choice until the choice is disclosed. Alternative: penalize TBD by default (assume worst-case static blanket until proven otherwise). Currently the conservative interpretation applies.

6. **The 3.5 compression**: 23 of 39 concepts (59%) score at 3.5. This is a wide middle that doesn't differentiate between "D-T steady-state stellarator with solid breeder" and "D-T pulsed MIF with liquid blanket" — both score 3.5 via different paths. If the analyst wants more differentiation, consider splitting one of the moderate penalties into two sub-tiers (e.g., pulsed-with-thermal-storage vs pulsed-without). Currently the framework accepts this compression because the underlying operational choices balance out.
