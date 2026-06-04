"""1costingfe model: Polywell (EMC2) (EMC2).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

# Make the shared three-forward helper importable regardless of where this file
# lives (concept dir or iter-N/ dir): walk up to the scripts/ root.
_SCRIPTS = next(
    p / "scripts"
    for p in Path(__file__).resolve().parents
    if (p / "scripts" / "lib" / "model_setup_helpers.py").exists()
)
sys.path.insert(0, str(_SCRIPTS))

from costingfe import ConfinementConcept, CostModel, Fuel
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# 1. Specification — design-point inputs only, at native scale.
#    Geometry / physics / power. NO library-default re-passing.
#
#    CRITICAL: This concept has NO complete design point. The analysis states:
#    "No design-point row for this concept yet — selection is upstream-pending."
#    Park et al. (2025) provides theoretical physics scaling but no engineering
#    design with complete parameters. The spec dict below is EMPTY per the
#    archetype-fit guidance: "When no design point exists, populate spec with
#    only the fields that ARE published." Since Park 2025 gives physics values
#    but no canonical CostingInput mapping (no R0, no plasma_t, no geometry in
#    canonical form), we leave spec empty and rely entirely on library defaults.
#
#    From analysis Section 5: Park et al. provides:
#    - Device geometry: 1.6 m cube (but this is overall device, not R0 or plasma_t)
#    - Plasma volume: 4.1 m³ (BLOCKED from spec by DIPOLE archetype bug #24)
#    - Cusp magnetic field: 4.5 T (but this is boundary field, not b_center)
#    - Electron beam input: 78 MW (this is p_input, but uncertainty ±60% per γ factor)
#    - Fusion power: ~980 MW (p_fus is never a spec key — library back-solves)
#
#    None of these map cleanly to canonical DIPOLE/POLYWELL spec keys without
#    architectural assumptions the source doesn't support. Leaving spec empty
#    produces a generic POLYWELL cost estimate at P_native scale, which is the
#    honest answer given data availability.
spec = dict(
    # No canonical spec keys — Park et al. (2025) provides physics scaling
    # (cube geometry, plasma volume, field strength) but no mapping to
    # CostingInput's expected geometry parameters (R0, plasma_t, r_bore).
    # The 1.6 m cube is overall device dimension, not a canonical length scale.
    # plasma_volume is blocked by DIPOLE archetype bug (1cFE/1costingfe#24).
    # Electron beam 78 MW is p_input but has ±60% uncertainty from γ factor.
    # Leaving spec empty uses library YAML defaults for a generic POLYWELL.
)
P_native = 290.0  # MWe — derived in analysis Section 5 from Park et al. physics
                  # scaling: ~388 MWe gross thermal conversion - 97.5 MW e-beam
                  # wall-plug. CAUTION: uncertainty ±60% due to γ=0.1 assumption.

# 2. Model.
# F-1 fix: Park et al. (2025) is a D-T design point (50:50 D-T fuel, 14.1 MeV neutrons,
# tritium breeding blanket required per analysis Section 2, 4, 5, 6). Using Fuel.PB11
# would fundamentally misrepresent the cost structure (D-T needs breeding, fuel cycle,
# neutron shielding; p-B11 is aneutronic).
model = CostModel(concept=ConfinementConcept.POLYWELL, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis Section 5b states: "After walking the canonical account schema,
#    **no override candidates are proposed**." Justification: "The dossier
#    contains no company-grounded cost data, published dollar figures, or
#    engineering subsystem specifications." The concept has physics validation
#    but no power plant cost study. Zero overrides is below the Archetype-Fit:Med
#    expected band (3-8) but reflects true data availability.
overrides = [
    # No overrides — Park et al. (2025) provides physics scaling only, no cost
    # data. Analysis Section 5b: "No blanket design, no magnet engineering
    # (HTS inferred but not designed), no electron gun procurement cost, no
    # balance-of-plant specifications." Library defaults produce a generic
    # electrostatic confinement fusion plant estimate, not Polywell-specific.
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# 5. Sensitivity sweep — γ uncertainty propagation (F-3 fix)
# Analysis Section 5 states P_native = 290 MWe has "uncertainty ±60%" due to the
# loss reduction factor γ assumption (never experimentally validated). If γ=0.2
# (worse confinement), net electric drops to ~193 MWe. If γ=0.05 (better), net
# electric increases to ~368 MWe. Run scenarios to show how this unvalidated physics
# assumption propagates to LCOE uncertainty.
print("\n" + "="*80)
print("SENSITIVITY SWEEP: Loss Reduction Factor γ Uncertainty")
print("="*80)
print("Park et al. (2025) reactor scaling assumes γ=0.1 (baseline), but this")
print("value has never been measured experimentally. The analysis states:")
print("  γ=0.2 (pessimistic) → P_net ≈ 193 MWe (recirculating power doubles)")
print("  γ=0.1 (baseline)    → P_net ≈ 290 MWe (78 MW electron beam injection)")
print("  γ=0.05 (optimistic) → P_net ≈ 368 MWe (recirculating power halves)")
print("\nRunning three scenarios to bound LCOE range:\n")

# Pessimistic case: γ=0.2
print("--- Scenario 1: γ=0.2 (Pessimistic) ---")
print(f"P_native = 193 MWe (recirculating power fraction: ~16%)")
pessimistic, _ = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=193.0,
)
print(f"  LCOE (native scale): {pessimistic.lcoe:.1f} $/MWh\n")

# Baseline case: γ=0.1 (already computed above as 'native')
print("--- Scenario 2: γ=0.1 (Baseline) ---")
print(f"P_native = 290 MWe (recirculating power fraction: ~8%)")
print(f"  LCOE (native scale): {native.lcoe:.1f} $/MWh\n")

# Optimistic case: γ=0.05
print("--- Scenario 3: γ=0.05 (Optimistic) ---")
print(f"P_native = 368 MWe (recirculating power fraction: ~4%)")
optimistic, _ = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=368.0,
)
print(f"  LCOE (native scale): {optimistic.lcoe:.1f} $/MWh\n")

print("="*80)
print("SUMMARY: LCOE Range Due to γ Uncertainty")
print("="*80)
print(f"Pessimistic (γ=0.2): {pessimistic.lcoe:.1f} $/MWh")
print(f"Baseline (γ=0.1):    {native.lcoe:.1f} $/MWh")
print(f"Optimistic (γ=0.05): {optimistic.lcoe:.1f} $/MWh")
print(f"Uncertainty range:   {pessimistic.lcoe - optimistic.lcoe:.1f} $/MWh " +
      f"({100*(pessimistic.lcoe - optimistic.lcoe)/native.lcoe:.0f}% of baseline)")
print("\nThis 4× recirculating power uncertainty dominates all other cost model")
print("assumptions. Until γ is experimentally validated, the LCOE estimate carries")
print("unbounded uncertainty from the core confinement mechanism.")
print("="*80)
