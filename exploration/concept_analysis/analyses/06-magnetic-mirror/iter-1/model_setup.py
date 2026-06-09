"""1costingfe model: Magnetic Mirror (Pale Blue) (Pale Blue).

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
# CRITICAL DATA GAP: Pale Blue Fusion has disclosed no quantitative reactor
# parameters for the CHARM commercial plant beyond P_native = 150 MWe. The
# analysis (Section 5) explicitly states: "The company has disclosed only
# `P_native = 150 MWe` and fuel choice (p-B11). All other values are
# analyst-derived from library defaults, radial build arithmetic, or inferred
# from the CMFX experiment scaling." The Section 5b walkthrough concludes:
# "Zero enabled overrides. The company has disclosed no quantitative reactor
# parameters beyond `P_native = 150 MWe`."
#
# The spec below contains minimal estimated values where the analysis provides
# them. However, Archetype-Fit is Low (modeling a centrifugal multi-chamber
# mirror as the generic MIRROR archetype), so even these estimates are
# uncertain. Per the canonical glossary blocklist, power-conversion
# efficiencies (eta_th, eta_de, eta_dec, eta_pin, eta_couple, eta_p) are
# framework-owned and must NOT appear in spec — the library carries them.
#
# The analysis flags that bore radius library default (1.85 m) "under-sizes
# the coil bore for an open-ended mirror" (analyst-patch-data-grounded.md),
# providing an analyst-derived 2.75 m, but this is low-confidence (radial
# build arithmetic, not company disclosure). However, r_bore is NOT in the
# canonical field allow-list for forward(), so we cannot express this.
#
# chamber_length is also not canonical (despite appearing in pb_mirror.py
# example). The canonical field is plasma_volume. Estimating plasma volume
# from plasma_t ~ 1.0 m radius and chamber_length ~ 20 m:
# V ≈ π r² L ≈ 3.14 × 1.0² × 20 ≈ 63 m³
spec = dict(
    R0=0.0,             # No axis offset for cylindrical mirror
    plasma_t=1.0,       # Estimated plasma radius 0.5-1.0 m (Section 5 table row "Plasma radius (minor radius)")
    plasma_volume=63.0, # Estimated from plasma_t ~ 1 m, chamber_length ~ 20 m (Section 5 table row "Central cell length")
    p_input=75.0,       # RF power for alpha channeling + startup; estimated 50-150 MW (Section 5 table row "Auxiliary heating power")
    T_e=150.0,          # p-B11 requires high temperature 100-300 keV protons (Section 5 table notes T_e 150 keV)
    # NOTE: f_dec (DEC fraction) is NOT set here. The analysis does not provide
    # a company-disclosed f_dec value. The library default will be used.
    # B (on-axis midplane field) is estimated at 2-3 T but low confidence (Section 5 table).
    # Not including it here as the library default may be more appropriate given low archetype fit.
    # blanket_t=0.0 and ht_shield_t=0.0 for p-B11 near-aneutronic, but leaving
    # as library defaults since no company disclosure exists.
)
P_native = 150.0       # MWe — analysis Design Point block; ONLY company-disclosed value

# 2. Model.
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.PB11)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     `generic` is the library's overrides-off forward at P_native. It is BOTH the
#     writing frame for relative overrides AND the reference the framework rescales
#     against at projection time (see `_scale_overrides` in
#     1costingfe/src/costingfe/model.py). Under the headline invariant, a relative
#     override lands on `M x (the library's 1 GWe fleet cost for that account)`
#     regardless of class — the framework rescales your native-frame anchor to the
#     fleet frame by the per-account ratio fleet_cost/native_cost, so you never
#     compute that ratio yourself. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#
# ZERO ENABLED OVERRIDES. The analysis Section 5b concludes: "Zero enabled
# overrides (expected band for low archetype-fit: 6-12). The count falls
# **below** the expected band because the design point is paper-concept with
# no disclosed reactor parameters." The per-account walkthrough shows that
# every canonical account lacks company-grounded data to justify departing
# from the library default.
#
# The resulting LCOE is a **library-default scenario**, not a company-validated
# estimate. The DATA_GROUNDED = False flag must be preserved in the frontmatter.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

# Pass data_grounded=False to emit the honest-output mode marker for concepts
# whose spec is minimal/estimated because the company has not disclosed any
# reactor design point. This prevents library-default artifacts from silently
# propagating as if they were grounded analyses. The breakdown still prints
# below so a reviewer can see what the library produced for MIRROR+PB11, but
# the headline LCOE refuses to make a claim about the actual Pale Blue concept.
print_cas_breakdown(generic, native, result_1gw, overrides, data_grounded=False)
