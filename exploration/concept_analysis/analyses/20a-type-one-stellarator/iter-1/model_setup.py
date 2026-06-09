"""1costingfe model: Type One Stellarator (Type One Energy) (Type One Energy).

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
#    Use ONLY the canonical field names below (see archetype spec-key glossary
#    rendered after this block); names like B0, laser_pulse_energy_kJ,
#    rep_rate_hz, or target_gain are not in CostingInput and would be
#    silently dropped at forward() time. F7 (validator) catches this.
spec = dict(
    R0=12.5,           # cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1
    plasma_t=1.25,     # cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 (minor radius a, canonical name is plasma_t)
    elon=1.0,          # analysis.md §5 (stellarator default, not specified in sources — stellarators typically ~1)
    B=9.0,             # cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 (on-axis field B₀; canonical name is B)
    p_input=20.0,      # cambridge-core-services-aop-cambridge-core-content-view.md §2.4 Table 1 (ECRH auxiliary heating wallplug, NOT fusion power)
    # Note: p_fus=800 MW is published fusion power but is NEVER a spec key —
    # library back-solves it from p_input + P_native via inverse power balance.
    # eta_th, eta_p, eta_de, eta_dec are NEVER spec keys — framework-owned defaults.
    # plasma_volume could be derived (~615 m³ per analysis §5) but not directly published;
    # library will compute from R0, plasma_t, and elon via stellarator scaling.
)
P_native = 350      # MWe — copied from the analysis Design Point block

# Toroidal coil-cost requirement (TOKAMAK / STELLARATOR only):
#   `plasma_t` is REQUIRED. 1costingfe's bilinear coil cost model computes
#   C220103 ∝ B × R₀ × r_coil, where r_coil = vessel_or =
#   plasma_t + blanket_t + ht_shield_t + structure_t + vessel_t. If the
#   source publishes only major radius R₀ and aspect ratio A, derive
#   `plasma_t = R₀ / A`. Leaving plasma_t unset falls back to the YAML
#   default (1.1m tokamak / 1.8m stellarator) which over-states most
#   published commercial designs.
#
# `r_bore` is silently unused for toroidal devices under the bilinear
# model (kept in YAML for backcasting compat only). Do NOT pass
# `r_bore = R₀` in spec for TOKAMAK / STELLARATOR; it's a no-op.
# Loop devices (MIRROR, FRC, DIPOLE, PULSED) still use r_bore for the
# r² coil model and must set it explicitly.

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

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
overrides = [
    # Zero enabled overrides: analysis.md §5b explicitly states "0 enabled overrides"
    # and documents the rationale:
    # "the library's modular-stellarator defaults are adequate given the available data."
    #
    # Despite comprehensive physics design documentation (7 peer-reviewed J. Plasma Phys.
    # papers), Type One Energy has not published decomposable cost data for major accounts:
    # - C220103 (HTS coils): CFS/MIT cable tech is known, but no stellarator-geometry
    #   unit cost or manufacturing timeline disclosed
    # - C220101 (blanket): HCPB + FLiBe dual-zone architecture described in neutronics
    #   (TBR=1.30), but no volume breakdown or integrated cost estimate
    # - C220108 (divertor): classical island divertor baseline + LIBD contingency, but
    #   no published cost for either
    #
    # The library's `stellarator-modular-hts` defaults are built on W7-X modular-coil
    # heritage and CFS HTS unit costs — the correct baseline for Infinity Two in the
    # absence of concept-specific overrides.
    #
    # Archetype-fit grade is High → expected override count is 0-4.
    # Zero enabled overrides falls within this band.
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
