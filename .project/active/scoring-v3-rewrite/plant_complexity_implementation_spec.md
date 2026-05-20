# Implementation Spec: Plant Complexity Scoring Axis

**Status:** Ready for implementation (converted from `plant_complexity_scoring_plan.md` 2026-05-20)
**Owner:** Mallory
**Created:** 2026-05-19 (planning), 2026-05-20 (impl-spec conversion)
**Target directory:** `.project/active/scoring-v2-plant-complexity-slice/` (new slice)
**Schema version:** v0.3.0 (`schema.md`, 2026-05-12)
**Companion to:** `integrated_implementation_plan.md`

## Summary

Build a **Plant Complexity** scoring axis as a peer of Modularity, Supply Chain,
Customization, and Upper CF in `weights/default.yaml`. The axis produces a
deterministic 1.0–5.0 score per concept based on how many distinct major plant
subsystems the concept must successfully build, integrate, and operate beyond
the baseline power-plant infrastructure.

### Score formula

```
plant_complexity_score = max(1.0, 5.0 - subsystem_weight)

where subsystem_weight = sum of severity weights of triggered subsystem flags
```

Same structural pattern as Supply Chain and Upper CF.

### What the score measures

**Question:** *How many distinct major plant subsystems must this concept
successfully build, integrate, and operate beyond the baseline?*

Score 5 = minimal complexity beyond the fusion device itself.
Score 1 = stacks every major fusion-plant subsystem.

Independent of supply chain (critical materials), modularity (device-level
manufacturability), customization (site-agnosticness), and upper CF
(operational ceiling).

### Severity tiers

| Tier | Weight | Definition |
|---|---|---|
| **Critical** | 2.0 | Architecture-rewriting subsystem with no commercial precedent (target factory at high rep rate). |
| **Severe** | 1.0 | Substantial standalone subsystem with its own facility, controls, and maintenance program. |
| **Moderate** | 0.5 | Real subsystem but smaller scope, or duplicative of something already counted. |

### Subsystem flags (15 total)

| # | Subsystem | Tier | Weight | Trigger (v0.3.0 schema) |
|---|---|---|---|---|
| 1 | tritium_plant | Severe | 1.0 | `Fuel = D-T` AND `Blanket Config != "N/A (non-power)"` |
| 2 | remote_maintenance | Severe | 1.0 | `Fuel in {D-T, D-D}` |
| 3 | hybrid_energy | Moderate | 0.5 | `Energy Capture = "Hybrid (thermal + direct)"` |
| 4 | cryoplant_lts | Severe | 1.0 | `Magnet Type in {LTS, LTS+HTS}` |
| 5 | cryoplant_hts | Moderate | 0.5 | `Magnet Type` starts with `"HTS"` |
| 6 | target_factory_high | Critical | 2.0 | Target-using concept AND `Repetition Rate in {~1 Hz, ~10 Hz, High (>10 Hz), kHz}` |
| 7 | target_factory_low | Moderate | 0.5 | Target-using concept AND `Repetition Rate = "Sub-Hz"` |
| 8 | pulsed_power_thermal | Severe | 1.0 | Pulsed-power architecture AND thermal-cycle energy capture |
| 9 | high_power_aux | Severe | 1.0 | `Primary Heating in {NBI, RF + NBI}` |
| 10 | rf_aux | Moderate | 0.5 | `Primary Heating in {RF (ECRH), RF (ICRH)}` |
| 11 | disruption_mitigation | Severe | 1.0 | `Confinement Concept` in tokamak family OR `Z-pinch (sheared-flow)` |
| 12 | current_drive | Moderate | 0.5 | Tokamak family AND `Operation Mode in {Steady-state, Quasi-steady}` |
| 13 | liquid_metal_handling | Moderate | 0.5 | `Blanket Config = "Liquid metal"` |
| 14 | levitation_stabilization | Moderate | 0.5 | `Confinement Concept in {Levitated dipole, Levitated dipole (orbital)}` |

(14 unique flags; target_factory has both _high and _low variants, mutually exclusive per concept.)

### Key design choices

- **Penalty-stack, weights in `weights/default.yaml`** — all 14 weights visible in one place under `plant_complexity.subsystem_complexity_weights`.
- **All triggers use existing v0.3.0 schema features** — no new features required.
- **TBD-blanket-default rule applies**: `Blanket Config = TBD` defaults to `"Liquid metal"` (most common D-T choice) with `blanket_assumed: liquid_metal_default` flag in diagnostic.
- **Thermal BOP NOT penalized** (every electricity-producing concept needs it; not a discriminator). Hybrid energy capture penalized because dual-channel adds genuine complexity above baseline.
- **TBD energy capture NOT penalized** (per analyst direction — energy capture being undecided is a documentation gap captured by Data Availability, not a plant complexity driver).

### Target-using vs not — the explicit set

A concept "uses targets" if it consumes discrete manufactured fuel targets per shot. Specifically:

- **IFE Laser variants** (indirect/direct/fast/ultrashort/hybrid drive) → uses targets ✓
- **IFE Heavy ion beam** → uses targets ✓
- **IFE Projectile impact** → uses targets ✓ (the projectile + target are manufactured)
- **IFE Acoustic implosion** (Sonofusion) → does NOT use manufactured targets (cavitation in bulk fluid) ✗
- **MIF MagLIF** → uses targets ✓ (the liner is manufactured per shot)
- **MIF Magnetized target / Target compression** → uses targets ✓
- **MIF FRC compression** (Helion) → does NOT use targets (compresses pre-formed plasma) ✗
- **MIF Pneumatic compression** (General Fusion) → uses targets ✓ (the central plasma puff is mechanically equivalent)
- **MFE Z-pinch / DPF** → does NOT use targets (gas puff or wire array, not a manufactured capsule) ✗

This refines the "uses_targets" predicate in the planning doc to exclude Acoustic explicitly. See Open Question #1 for analyst confirmation.

---

## Changes summary

| # | Change | Touches |
|---|---|---|
| A | Add `plant_complexity` axis with inline severity weights to `weights/default.yaml` | `weights/default.yaml` |
| B | Implement `subsystem_complexity_weight` and `plant_complexity_score` embeddings | `embeddings/rulebook.py` |
| C | Create `lookup_plant_subsystems.yaml` metadata file (no weights) | `lookup_plant_subsystems.yaml` (new) |
| D | Add `plant_complexity_diagnostics` derived block per feature file | `features/*.yaml` (40 files) |
| E | Add acceptance tests | `tests/scoring_v2/test_plant_complexity.py` (new) |

---

## Change A: Axis registration with inline weights

```yaml
plant_complexity:
  axis_weight: 1.0                          # composite weight (UI tunable)
  embedding_weights:
    plant_complexity_score: 1.0             # single embedding → axis score directly
  subsystem_complexity_weights:             # severity tuning surface
    # Critical
    target_factory_high:        2.0
    # Severe
    tritium_plant:              1.0
    remote_maintenance:         1.0
    cryoplant_lts:              1.0
    high_power_aux:             1.0
    disruption_mitigation:      1.0
    pulsed_power_thermal:       1.0
    # Moderate
    cryoplant_hts:              0.5
    rf_aux:                     0.5
    hybrid_energy:              0.5
    target_factory_low:         0.5
    liquid_metal_handling:      0.5
    current_drive:              0.5
    levitation_stabilization:   0.5
```

---

## Change B: Embeddings in `rulebook.py`

```python
# ===========================================================================
# Plant Complexity Axis
# ===========================================================================

_PC_SUBSYSTEM_NAMES = [
    "tritium_plant", "remote_maintenance", "hybrid_energy",
    "cryoplant_lts", "cryoplant_hts",
    "target_factory_high", "target_factory_low",
    "pulsed_power_thermal", "high_power_aux", "rf_aux",
    "disruption_mitigation", "current_drive",
    "liquid_metal_handling", "levitation_stabilization",
]

TOKAMAK_CONCEPTS = {
    "Tokamak", "Compact tokamak", "Spherical tokamak",
    "Negative triangularity tokamak",
}
DISRUPTION_PRONE_CONCEPTS = TOKAMAK_CONCEPTS | {"Z-pinch (sheared-flow)"}
LEVITATED_DIPOLE_CONCEPTS = {"Levitated dipole", "Levitated dipole (orbital)"}
HIGH_REP_RATES = {"~1 Hz", "~10 Hz", "High (>10 Hz)", "kHz"}
LOW_REP_RATES = {"Sub-Hz"}

# IFE drivers that use discrete manufactured targets (excludes Acoustic)
TARGET_USING_IFE_DRIVERS = {"Laser", "Heavy ion beam", "Projectile"}
# MIF methods that use discrete manufactured targets (excludes FRC compression)
TARGET_USING_MIF_METHODS = {"MagLIF", "Target compression", "Pneumatic compression"}


def _load_pc_weights(weights_yaml: dict) -> dict[str, float]:
    pc = weights_yaml.get("plant_complexity", {})
    raw = pc.get("subsystem_complexity_weights", {})
    missing = [s for s in _PC_SUBSYSTEM_NAMES if s not in raw]
    if missing:
        raise ValueError(
            f"weights/default.yaml plant_complexity.subsystem_complexity_weights "
            f"missing keys: {missing}"
        )
    return {s: float(raw[s]) for s in _PC_SUBSYSTEM_NAMES}


def _compute_triggered_pc_subsystems(
    fuel, confinement_family, confinement_concept, ife_driver, mif_method,
    magnet_type, blanket_config, energy_capture, primary_heating,
    operation_mode, repetition_rate, weights,
):
    fuel = fuel or ""
    cfam = confinement_family or ""
    cconcept = confinement_concept or ""
    ife_drv = ife_driver or ""
    mif_meth = mif_method or ""
    magnet = magnet_type or ""
    raw_blanket = blanket_config or ""
    energy = energy_capture or ""
    heating = primary_heating or ""
    op_mode = operation_mode or ""
    rep_rate = repetition_rate or ""

    # TBD blanket → default to Liquid metal (consistent with Supply Chain TBD rule)
    blanket = "Liquid metal" if raw_blanket == "TBD" else raw_blanket

    triggered = {}

    # Tritium plant: D-T except non-power neutron sources
    if fuel == "D-T" and blanket != "N/A (non-power)":
        triggered["tritium_plant"] = weights["tritium_plant"]

    # Remote maintenance: any neutronic fuel
    if fuel in ("D-T", "D-D"):
        triggered["remote_maintenance"] = weights["remote_maintenance"]

    # Hybrid energy capture (thermal BOP itself NOT penalized — baseline cost)
    if energy == "Hybrid (thermal + direct)":
        triggered["hybrid_energy"] = weights["hybrid_energy"]

    # TBD energy capture: NOT penalized (per analyst direction; gap captured by Data Availability)

    # Cryoplant
    if magnet in ("LTS", "LTS+HTS"):
        triggered["cryoplant_lts"] = weights["cryoplant_lts"]
    elif magnet.startswith("HTS"):
        triggered["cryoplant_hts"] = weights["cryoplant_hts"]

    # Auxiliary heating
    if heating in ("NBI", "RF + NBI"):
        triggered["high_power_aux"] = weights["high_power_aux"]
    elif heating in ("RF (ECRH)", "RF (ICRH)"):
        triggered["rf_aux"] = weights["rf_aux"]

    # Target factory: concepts that consume discrete manufactured targets per shot
    # IFE: Laser/Heavy ion/Projectile (excludes Acoustic)
    # MIF: MagLIF/Target compression/Pneumatic compression (excludes FRC compression)
    uses_targets = (
        (cfam == "IFE" and ife_drv in TARGET_USING_IFE_DRIVERS)
        or (cfam == "MIF" and mif_meth in TARGET_USING_MIF_METHODS)
    )
    if uses_targets:
        if rep_rate in HIGH_REP_RATES:
            triggered["target_factory_high"] = weights["target_factory_high"]
        elif rep_rate in LOW_REP_RATES:
            triggered["target_factory_low"] = weights["target_factory_low"]

    # Pulsed-power facility with thermal storage
    is_pulsed_power_arch = (
        cfam == "MIF"
        or "Z-pinch" in cconcept
        or "Dense plasma focus" in cconcept
    )
    has_thermal = energy.startswith("Thermal") or energy == "Hybrid (thermal + direct)"
    if is_pulsed_power_arch and has_thermal:
        triggered["pulsed_power_thermal"] = weights["pulsed_power_thermal"]

    # Disruption mitigation (tokamaks + sheared-flow Z-pinch)
    if cconcept in DISRUPTION_PRONE_CONCEPTS:
        triggered["disruption_mitigation"] = weights["disruption_mitigation"]

    # Steady-state current drive (tokamaks only)
    if cconcept in TOKAMAK_CONCEPTS and op_mode in ("Steady-state", "Quasi-steady"):
        triggered["current_drive"] = weights["current_drive"]

    # Liquid metal handling
    if blanket == "Liquid metal":
        triggered["liquid_metal_handling"] = weights["liquid_metal_handling"]

    # Levitated dipole mechanical stabilization
    if cconcept in LEVITATED_DIPOLE_CONCEPTS:
        triggered["levitation_stabilization"] = weights["levitation_stabilization"]

    return triggered


@embedding(
    "subsystem_complexity_weight",
    inputs=["fuel", "confinement_family", "confinement_concept",
            "ife_driver", "mif_method", "magnet_type", "blanket_config",
            "energy_capture", "primary_heating", "operation_mode",
            "repetition_rate"],
)
def _subsystem_complexity_weight(
    fuel, confinement_family, confinement_concept, ife_driver, mif_method,
    magnet_type, blanket_config, energy_capture, primary_heating,
    operation_mode, repetition_rate, *, weights_yaml: dict,
) -> float:
    weights = _load_pc_weights(weights_yaml)
    triggered = _compute_triggered_pc_subsystems(
        fuel, confinement_family, confinement_concept, ife_driver, mif_method,
        magnet_type, blanket_config, energy_capture, primary_heating,
        operation_mode, repetition_rate, weights,
    )
    return sum(triggered.values())


@embedding(
    "plant_complexity_score",
    inputs=["subsystem_complexity_weight"],
)
def _plant_complexity_score(subsystem_complexity_weight: float) -> float:
    return max(1.0, 5.0 - subsystem_complexity_weight)
```

---

## Change C: `lookup_plant_subsystems.yaml` (metadata only)

```yaml
# Plant complexity subsystem metadata.
# Numerical weights live in weights/default.yaml under
# plant_complexity.subsystem_complexity_weights.

target_factory_high:
  tier: Critical
  trigger: "Target-using concept (IFE Laser/Heavy-ion/Projectile, or MIF MagLIF/Target/Pneumatic) AND Repetition Rate ≥ 1 Hz"
  rationale: |
    A 1-10 Hz target-using fusion plant needs ~86,000-500,000 precision targets/day.
    No commercial precedent. Target factory + injection + chamber recovery between
    shots is a complete second plant alongside the driver.

tritium_plant:
  tier: Severe
  trigger: "Fuel = D-T AND Blanket Config != N/A (non-power)"
  rationale: |
    Closed tritium fuel cycle: breeding processing, recovery from blanket,
    exhaust isotope separation, storage. ITER's tritium plant is ~7 integrated
    subsystems. SHINE-class concepts buy tritium externally → not penalized.

remote_maintenance:
  tier: Severe
  trigger: "Fuel in {D-T, D-D}"
  rationale: |
    14 MeV (D-T) and 2.45 MeV (D-D) neutron environments activate components
    beyond hands-on access. Aneutronic (p-B11, D-He3) concepts can largely
    use conventional maintenance.

cryoplant_lts:
  tier: Severe
  trigger: "Magnet Type in {LTS, LTS+HTS}"
  rationale: |
    4 K cryogenics: helium refrigeration, distribution, recovery, cold storage.
    ITER's cryoplant is one of the largest in the world.

cryoplant_hts:
  tier: Moderate
  trigger: "Magnet Type starts with HTS"
  rationale: |
    20-50 K operation materially simpler than 4 K — smaller refrigeration plant,
    less stringent insulation, faster cooldown. Still a real plant subsystem.

high_power_aux:
  tier: Severe
  trigger: "Primary Heating in {NBI, RF + NBI}"
  rationale: |
    Neutral beam injection at 100+ MW is a substantial plant subsystem:
    ion sources, neutralizers, beam dumps, transmission lines, large vacuum tanks.

rf_aux:
  tier: Moderate
  trigger: "Primary Heating in {RF (ECRH), RF (ICRH)}"
  rationale: |
    Gyrotrons or ICRH antennas + power supplies + transmission lines.
    Substantial but less so than NBI.

pulsed_power_thermal:
  tier: Severe
  trigger: "Pulsed-power architecture (MIF / Z-pinch / DPF) AND thermal-cycle energy capture"
  rationale: |
    Z-machine-class pulsed-power infrastructure PLUS thermal energy storage /
    intermediate heat transport to buffer pulsed thermal output into continuous
    turbine power. Direct-conversion pulsed concepts (Helion, LPP DPF) avoid this.

disruption_mitigation:
  tier: Severe
  trigger: "Confinement Concept in tokamak family OR Z-pinch (sheared-flow)"
  rationale: |
    Tokamaks face kink/vertical-displacement disruptions; Z-pinches face
    m=0 sausage and m=1 kink. Multiple coupled mitigation systems (MGI, SPI,
    REMC, fast plasma control).

current_drive:
  tier: Moderate
  trigger: "Tokamak family AND Operation Mode in {Steady-state, Quasi-steady}"
  rationale: |
    Tokamaks need non-inductive current drive for steady-state. Pulsed
    tokamaks avoid this. Stellarators are intrinsically current-free.

hybrid_energy:
  tier: Moderate
  trigger: "Energy Capture = Hybrid (thermal + direct)"
  rationale: |
    Two independent energy conversion paths add complexity beyond standard
    thermal conversion. Only for explicit dual-channel.

target_factory_low:
  tier: Moderate
  trigger: "Target-using concept AND Repetition Rate = Sub-Hz"
  rationale: |
    Sub-Hz target-using concepts still need a target factory but at pilot-plant
    scale rather than mass production. Significantly less complex than high-rep.

liquid_metal_handling:
  tier: Moderate
  trigger: "Blanket Config = Liquid metal (incl. TBD-defaulted-to-Liquid-metal)"
  rationale: |
    Pumps, purification, leak management, MHD considerations for liquid Li or
    LiPb in magnetic fields.

levitation_stabilization:
  tier: Moderate
  trigger: "Confinement Concept in {Levitated dipole, Levitated dipole (orbital)}"
  rationale: |
    Active feedback-controlled magnetic levitation of a ~500 kg superconducting
    ring inside a vacuum chamber. Distinct from disruption mitigation
    (plasma-physics complexity); this is mechanical/control complexity.
```

---

## Change D: Feature-file diagnostics

### Format

```yaml
plant_complexity_diagnostics:
  subsystems_triggered:
    {subsystem_name}: {weight}     # one entry per triggered subsystem
  subsystem_weight: {sum}
  plant_complexity_score: {score}
  blanket_assumed: liquid_metal_default   # OPTIONAL — only present when Blanket Config = TBD
```

### Example — CFS ARC

```yaml
plant_complexity_diagnostics:
  subsystems_triggered:
    tritium_plant: 1.0
    remote_maintenance: 1.0
    cryoplant_hts: 0.5
    rf_aux: 0.5
    disruption_mitigation: 1.0
    current_drive: 0.5
  subsystem_weight: 4.5
  plant_complexity_score: 1.0
```

### Population

`scripts/populate_plant_complexity_diagnostics.py` (idempotent, re-runnable
after weight changes).

---

## Change E: Acceptance tests

`tests/scoring_v2/test_plant_complexity.py` with classes:

- `TestWeightsExposedInDefaultYaml` — verify all 14 weights present in `default.yaml`
- `TestTriggerRules` — per-subsystem trigger correctness (with v0.3.0 controlled vocab)
- `TestTargetUsingClassification` — explicit checks that Sonofusion does NOT trigger target_factory; Zap Z-pinch does NOT; Helion FRC does NOT; First Light projectile DOES; MagLIF DOES
- `TestPerConceptScoreAnchors` — anchored to `tests/scoring_v2/predicted_scores.yaml`
- `TestWeightTuning` — verify weight edits in `default.yaml` change scores as expected

---

## Predicted scores (40 concepts)

Computed from the trigger logic + v3-ontology features per concept. Where the planning doc enumerated 24 representative concepts, the remaining 16 are computed by applying the trigger rules.

| Concept | Triggers | Wt | **Score** |
|---|---|---|---|
| 01 CFS ARC | tritium, remote, cryo_hts, rf_aux, disruption, current_drive | 4.0 | **1.0** |
| 02 Sonofusion | remote_maintenance | 1.0 | **4.0** |
| 03 Cortex liquid-jet | remote, target_factory_high, liquid_metal | 3.5 | **1.5** |
| 04 hb11 | target_factory_high | 2.0 | **3.0** |
| 05 Thea planar | tritium, remote, cryo_hts, rf_aux | 3.0 | **2.0** |
| 06 Pale Blue mirror | cryo_hts, high_power_aux | 1.5 | **3.5** |
| 07 Pacific MagLIF | tritium, remote, pulsed_power_thermal, target_factory_low, liquid_metal | 3.5 | **1.5** |
| 08 Helion | (none) | 0.0 | **5.0** |
| 09 Proxima QI | tritium, remote, cryo_hts, rf_aux | 3.0 | **2.0** |
| 10 Gauss HELIAS | tritium, remote, cryo_hts, rf_aux | 3.0 | **2.0** |
| 11 Realta mirror | tritium, remote, cryo_hts, high_power_aux | 3.5 | **1.5** |
| 12 OpenStar | tritium, remote, cryo_hts, rf_aux, levitation | 3.5 | **1.5** |
| 13 Avalanche | tritium, remote | 2.0 | **3.0** |
| 14 General Fusion MTF | tritium, remote, pulsed_power_thermal, target_factory_high, liquid_metal | 4.5 | **1.0** |
| 15 Zap Z-pinch | tritium, remote, pulsed_power_thermal, disruption_mitigation, liquid_metal | 4.5 | **1.0** |
| 16 Acceleron muon | tritium, remote | 2.0 | **3.0** |
| 17a Xcimer | tritium, remote, target_factory_high | 4.0 | **1.0** |
| 17b Focused | tritium, remote, target_factory_high, liquid_metal | 4.5 | **1.0** |
| 18 TAE p-B11 | cryo_hts, high_power_aux | 1.5 | **3.5** |
| 19 Zephyr orbital | cryo_hts, rf_aux, levitation | 1.5 | **3.5** |
| 20a Type One | tritium, remote, cryo_hts, rf_aux | 3.0 | **2.0** |
| 20b Renaissance | tritium, remote, cryo_hts, high_power_aux | 3.5 | **1.5** |
| 21 Tokamak Energy ST | tritium, remote, cryo_hts, rf_aux, disruption, current_drive | 4.0 | **1.0** |
| 22 First Light projectile | tritium, remote, target_factory_low, liquid_metal | 3.0 | **2.0** |
| 23 Marvel ultrashort | target_factory_high | 2.0 | **3.0** |
| 24 LPP DPF | (none — direct conversion, aneutronic) | 0.0 | **5.0** |
| 25 Intensity heavy-ion | tritium, remote, target_factory_high, liquid_metal | 4.5 | **1.0** |
| 26 Inertia DPSSL | tritium, remote, target_factory_high, liquid_metal | 4.5 | **1.0** |
| 27 EMC2 Polywell | tritium, remote | 2.0 | **3.0** |
| 28 Energy Singularity | tritium, remote, cryo_hts, rf_aux, disruption, current_drive | 4.0 | **1.0** |
| 29 Firefly NTT | tritium, remote, cryo_hts, rf_aux, disruption, current_drive | 4.0 | **1.0** |
| 30 NIF-comm | tritium, remote, target_factory_high, liquid_metal | 4.5 | **1.0** |
| 31 Blue Laser OEC | tritium, remote, target_factory_high | 4.0 | **1.0** |
| 32 GenF French | tritium, remote, target_factory_high, liquid_metal | 4.5 | **1.0** |
| 33 BEST | tritium, remote, cryo_lts, rf_aux, disruption, current_drive | 4.5 | **1.0** |
| 35 Deutelio Polomac | remote | 1.0 | **4.0** |
| 36 Helical Fusion | tritium, remote, cryo_hts, rf_aux, liquid_metal | 3.5 | **1.5** |
| 37 NearStar MTIF | remote, pulsed_power_thermal | 2.0 | **3.0** |
| 38 SHINE | remote | 1.0 | **4.0** |
| 39 ENN p-B11 ST | cryo_hts, high_power_aux, disruption, current_drive | 3.0 | **2.0** |

### Score distribution (40 concepts)

- **5.0 (2)**: Helion, LPP DPF — zero subsystems triggered (aneutronic + direct + no targets).
- **4.0 (3)**: SHINE (non-power), Sonofusion, Polomac — D-D or non-power D-T with only remote_maintenance.
- **3.5 (3)**: TAE, Pale Blue, Zephyr — aneutronic with one or two moderate triggers.
- **3.0 (5)**: hb11, NearStar, Avalanche, Acceleron, Marvel, Polywell — D-D/D-T/p-B11 with limited triggers.
- **2.0 (5)**: Thea, Proxima, Gauss, Type One, ENN, First Light — D-T or aneutronic ST.
- **1.5 (6)**: Realta, OpenStar, Cortex, Pacific MagLIF, Renaissance, Helical — D-T concepts with one moderate beyond baseline.
- **1.0 (13)**: Tokamaks, Z-pinch, BEST, high-rep IFE, General Fusion MTF — full D-T stack.

---

## Files touched

```
exploration/scoring_v2/weights/default.yaml                       # add plant_complexity axis
exploration/scoring_v2/embeddings/rulebook.py                     # +2 embeddings, +1 helper, +5 constants
exploration/scoring_v2/lookup_plant_subsystems.yaml               # NEW
exploration/scoring_v2/features/*.yaml                            # 40 files: plant_complexity_diagnostics
exploration/scoring_v2/scripts/populate_plant_complexity_diagnostics.py  # NEW
tests/scoring_v2/test_plant_complexity.py                          # NEW
.project/active/scoring-v2-plant-complexity-slice/design.md        # NEW: this spec + planning doc
.project/active/scoring-v2-plant-complexity-slice/implementation_notes.md # NEW
```

---

## Implementation notes for Claude Code

- All trigger logic uses v0.3.0 controlled vocabulary equality checks.
- `_compute_triggered_pc_subsystems` is pure (given features + weights → triggered dict). Test independently.
- `target_factory` is the most subtle trigger — verify all 4 cases via `TestTargetUsingClassification`: Sonofusion ✗, Zap Z-pinch ✗, Helion ✗, First Light ✓.
- TBD-blanket-default rule: consistent with Supply Chain and Upper CF (`"TBD" → "Liquid metal"`); diagnostic records the substitution.
- Weight loading pattern: match `_load_bottleneck_weights` from supply chain spec.

---

## Open questions

1. **Sonofusion target-factory carve-out (refines planning doc).** The planning doc's `uses_targets = (cfam == "IFE" or ...)` predicate would trigger target_factory for Sonofusion (IFE Acoustic). This spec refines to `(cfam == "IFE" and ife_driver in {Laser, Heavy ion beam, Projectile})` — explicitly excludes Acoustic. **Confirm**: is this the analyst's intent?

2. **General Fusion (MIF Pneumatic) target-factory carve-out.** Planning doc text says "MIF concepts that compress already-injected plasma (FRC merging, plasma liner) do NOT use targets" — but General Fusion's plasma puff is mechanically equivalent to a target. This spec treats Pneumatic compression as target-using (target_factory_high fires at 1 Hz). **Confirm**: does General Fusion need a target factory, or does the in-situ plasma generation avoid it?

3. **Tritium plant tier (Severe vs Critical)** — currently 1.0. ITER's tritium plant has no commercial precedent. Bumping to Critical (2.0) would floor all D-T concepts and increase D-T vs aneutronic contrast.

4. **No "linear architecture" bonus** — considered and rejected. Linear/mirror/dipole concepts are already credited by *not* being penalized for disruption mitigation + current drive. Adding a separate bonus would double-count.

5. **Helion + LPP DPF at 5.0** — framework finds zero triggers. Defensible (genuinely simple architectures) but does omit: Helion's 50k capacitor banks, LPP DPF electrode erosion, hydrodynamic chamber recovery. Worth a flag?

6. **NBI threshold** — TAE's ~10 NBI lines (core plasma sustainment) vs tokamak's 1-2 NBI lines (auxiliary heating) get the same weight. Could split via a "NBI count" feature, but adds analyst judgment per concept.

7. **TBD energy capture** — currently NOT penalized (per analyst direction). Affects Avalanche, Sonofusion. Could be revisited if these concepts cluster suspiciously.
