"""1costingfe model: HTS Tokamak Full HTS (Energy Singularity).

⚠ CRITICAL DATA LIMITATION ⚠

Energy Singularity has not disclosed specifications for HH380 (their power plant).
From analysis.md Section 5:

    "Energy Singularity has disclosed no power output (P_native), no fusion power
    target, no geometry, and no subsystem specifications for HH380, the only
    power-producing machine in their roadmap."

This model uses PLACEHOLDER VALUES derived from compact tokamak analogues to satisfy
the three-forward contract requirement. These are NOT company-grounded values. The
analysis explicitly documents this limitation in Sections 5, 5b, and 6.

Placeholder derivation:
  - P_native = 500 MWe (representative compact tokamak scale, per analysis.md
    Section 6 recommendation: "assign representative scale based on compact tokamak
    comparables")
  - Geometry scaled from HH170 targets (~14T, ~70% SPARC volume, A~3) extrapolated
    to a 2-3× linear scale-up typical for demonstrator → commercial transitions
  - All spec values are ANALOGUE-BASED, not disclosed by Energy Singularity

What IS known (from analysis.md Sections 1-3):
  - HH70 (operational prototype): R0=0.75m, B0=0.6T, 26 HTS coils (12 TF+6 PF+8 CS,
    all REBCO), 1,337-second steady-state plasma, 96% domestic localization
  - HH170 (planned 2027): Q>10 target, ~14T on-axis, 25T peak field, ~70% SPARC
    volume — but NO power output specified, NO blanket design
  - HH380 (post-2030): ZERO technical specifications public

Blocking gaps (analysis.md Section 6, gaps #1-3):
  1. HH380 net electric output — unknown (blocks P_native)
  2. Blanket design / tritium breeding — unknown (blocks C220101, CAS27)
  3. HH380 geometry — unknown (blocks spec dict)
  4. Auxiliary heating for HH380 — unknown (blocks p_input)
  5. Energy conversion pathway — unknown

Override candidates (analysis.md Section 5b):
    overrides: []   # "Zero enabled overrides due to absence of HH380 data"

This model satisfies the three-forward contract (generic, native, result_1gw) but
carries LOW GROUNDING CONFIDENCE — it's a corridor map for a compact tokamak of
this scale, NOT a company-validated estimate.

Usage:
    uv run python model_setup.py              # print results with caveats
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

# Energy Singularity discloses no HH380 specifications — see ⚠ CRITICAL DATA
# LIMITATION ⚠ block above. All spec values are compact-tokamak analogues, not
# company-grounded. Read by the explorer extractor to suppress headline LCOE
# in cross-concept views (cost landscape, comparison summary). CAS breakdown
# still renders so reviewers can see what the analogue inputs produce.
DATA_GROUNDED = False

# 1. Specification — PLACEHOLDER VALUES (analogue-based, not company-grounded).
#    These are derived from HH170 targets (~14T, ~70% SPARC volume, A~3) scaled
#    up by 2-3× linear dimensions (typical demonstrator → commercial transition).
#
#    HH170 published targets (analysis.md Section 5):
#      - ~14T on-axis field, 25T peak on conductor
#      - ~90% SPARC diameter, ~70% SPARC volume
#      - SPARC: R0~1.85m, a~0.57m (A~3.25), so HH170: R0~1.3m, a~0.43m
#
#    HH380 extrapolation (VERY LOW CONFIDENCE):
#      - Scale up 2× linear → R0~2.6m, maintain A~3 → plasma_t~0.87m
#      - Maintain high-field compact approach → B~14T (could be higher or lower)
#      - Auxiliary heating power p_input: assume NBI/ICRF mix ~50-80 MW for 500 MWe
#        pilot plant (cf. ARC 38.6 MW for 233 MWe, scales ~linearly with P_elec)
spec = dict(
    R0=2.6,           # PLACEHOLDER: HH170 R0~1.3m × 2 scale-up → 2.6m
    plasma_t=0.87,    # PLACEHOLDER: R0/A = 2.6/3 → 0.87m (A~3 compact tokamak)
    elon=1.8,         # PLACEHOLDER: typical D-shaped elongation (HH170 described as
                      # "D-shaped" but no kappa disclosed; assume ARC-class 1.8)
    B=14.0,           # PLACEHOLDER: HH170 target ~14T; HH380 may maintain or increase
    p_input=85.0,     # PLACEHOLDER: 500 MWe at Q_eng~5-7 → p_fus~3000 MW, p_input
                      # ~60-100 MW auxiliary; assume NBI + ICRF mix, mid-range
)
P_native = 500.0     # PLACEHOLDER: representative compact tokamak pilot plant scale
                      # (analysis.md Section 6: "assign 500 MWe based on comparables")

# Note on spec field choices:
# - R0, plasma_t, elon, B, p_input are the canonical TOKAMAK spec keys per the
#   archetype glossary (see model_setup_prompt.md).
# - p_input is AUXILIARY HEATING wallplug power (MW), NOT fusion power. The library
#   back-solves p_fus from p_input + plasma parameters via inverse power balance.
# - plasma_t is REQUIRED for TOKAMAK/STELLARATOR (bilinear coil cost model uses
#   it to compute r_coil = plasma_t + blanket_t + shield_t + structure_t + vessel_t).
#   Leaving it unset falls back to YAML default (1.1m) which misrepresents this
#   concept's compact scale.
# - Power-conversion efficiencies (eta_th, eta_de, eta_pin, etc.) are NOT spec keys
#   — they're library-owned, per Hard Rule 3.
# - p_fus is NOT a spec key — the library computes it from p_input.

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — analysis.md Section 5b explicitly states: "overrides: []"
#
#    From Section 5b:
#      "Zero enabled overrides. The lack of overrides is not due to close alignment
#      between library defaults and company design — it is due to absence of company
#      data for HH380."
#
#    The analysis completed the per-account walkthrough (C220101 through CAS80) and
#    concluded no company-grounded overrides are possible. Key findings:
#
#    - C220101 (blanket): no blanket design disclosed → cannot override
#    - C220103 (magnets): full-HTS architecture (TF+PF+CS all REBCO) differs from
#      library default (TF-only HTS), but no HH380 magnet costs or REBCO tape
#      procurement pricing disclosed → cannot override directly. Analysis flags
#      this as "top override candidate if HH380 magnet costs are published" but
#      data does not exist yet.
#    - C220104 (heating): HH70 uses ICRH, but HH380 heating approach unknown
#    - C220108 (divertor): no divertor design disclosed
#    - CAS27 (blanket materials): no blanket chemistry disclosed
#
#    The analysis recommends SENSITIVITY ANALYSIS (not overrides) for:
#      - C220103: vary full-HTS cost multiplier 0.7-1.5× (architectural difference)
#      - C220101+CAS27: model range of blanket chemistries (FLiBe, LiPb, HCPB)
#      - CAS21: apply China construction cost index if modeling China deployment
#      - C220111: vary construction duration (2 yr fast, 5 yr baseline, 8 yr slow)
#
#    These are SCENARIO PARAMETERS, not company overrides, and belong in a separate
#    sensitivity suite, not in this model_setup.py.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
#    Since overrides=[], native is identical to generic except for the scale
#    (P_native vs. 1 GWe), isolating pure replication scaling.
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

# Print breakdown with data limitation caveats
print("="*80)
print("⚠ DATA LIMITATION: PLACEHOLDER VALUES IN USE ⚠")
print("="*80)
print("\nThis model uses ANALOGUE-BASED placeholders, NOT company-grounded values.")
print("Energy Singularity has not disclosed HH380 specifications (see docstring).")
print("\nPlaceholder assumptions:")
print(f"  P_native = {P_native} MWe (representative compact tokamak scale)")
print(f"  R0 = {spec['R0']} m (HH170 ~1.3m × 2 scale-up)")
print(f"  plasma_t = {spec['plasma_t']} m (A~3 compact tokamak)")
print(f"  B = {spec['B']} T (HH170 target, HH380 may differ)")
print(f"  p_input = {spec['p_input']} MW (NBI+ICRF mix, scaled from ARC)")
print("\nThese numbers represent 'a compact HTS tokamak at this scale', NOT")
print("Energy Singularity's specific HH380 design (which does not exist in")
print("public sources yet).")
print("\nOverrides: 0 enabled (no company-grounded cost data for HH380)")
print("="*80)
print()

print_cas_breakdown(generic, native, result_1gw, overrides)

print("\n" + "="*80)
print("MODEL CONFIDENCE: LOW")
print("="*80)
print("This LCOE estimate is a CORRIDOR MAP for a compact tokamak of this scale,")
print("NOT a company-validated number. The analysis (analysis.md Sections 5-6)")
print("documents 14 data gaps, 3 of which are blocking (P_native, blanket design,")
print("geometry). Until Energy Singularity discloses HH380 specifications (timeline:")
print("post-2030), any cost estimate is primarily assumption-driven.")
print("\nKey uncertainties (analysis.md Section 2):")
print("  - Unknown power plant scale (100 MWe – 1 GWe corridor)")
print("  - Unknown tritium breeding pathway (FLiBe, LiPb, HCPB, other?)")
print("  - Full-HTS magnet cost (depends on REBCO tape price trajectory $10-100/kA-m)")
print("  - Unknown divertor approach for high-power-density compact design")
print("\nFor comparables-based cross-concept analysis, use result_1gw with the caveat")
print("that this concept's true 1 GWe LCOE could range from 50-130 $/MWh (the corridor")
print("stated in analysis.md Section 2), centered on this library-default estimate,")
print("once HH380 engineering decisions are disclosed.")
print("="*80)
