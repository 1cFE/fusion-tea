"""1costingfe model: Renaissance Stellarator (Renaissance Fusion) (Renaissance Fusion).

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
#    From analysis.md Section 5, Design Point Parameters table.
#    Source: Prost, Ogier-Collin & Volpe, J. Nuclear Materials 599 (2024) 155239
#    (blanket paper, reproduces design-point values from Nuclear Fusion 64 (2024) 026007).
spec = dict(
    R0=3.8,          # Major radius [m] — infoscience-bitstreams...output.md §1, §2.2
    plasma_t=0.93,   # Minor radius a [m] — inferred from R0/A = 3.8/4.1 = 0.927 m.
                     # Blanket paper uses 1.0 m in cylindrical model approximation;
                     # 0.93 m is the design-point value. Drives r_coil = vessel_or
                     # in the bilinear coil cost model.
    elon=1.0,        # Elongation — stellarator (complex 3D cross-section, no
                     # tokamak-like elongation parameter; 1.0 as modeling placeholder)
    B=10.2,          # On-axis magnetic field [T] — infoscience-bitstreams...output.md §1
    p_input=5.0,     # Auxiliary heating wallplug [MW] — design point is ignited
                     # (Q = ∞, dossier.md §Plasma State), with NNBI at 60%
                     # neutralization efficiency for startup/ramp-up only. No
                     # published figure for installed NNBI capacity or steady-
                     # state burn-control power. 5 MW is a conservative estimate
                     # for minimal burn-control / impurity-management ECRH/NBI
                     # in a 1 GWe ignited stellarator (cf. Thea Energy Helios:
                     # 2.5 MW operational ECRH for 390 MWe ignited stellarator,
                     # = 0.64% of P_native; 5 MW / 1000 MWe = 0.5%).
                     # Data gap: Nuclear Fusion 64 (2024) 026007 (design-point
                     # paper, not extracted) likely specifies the NNBI system
                     # sizing — re-extraction would resolve this.
    # plasma_volume: not set. Geometric estimate V ≈ 2π²·R₀·a² ≈ 65 m³ for this
    # compact machine, vs library default 800 m³. However, stellarator plasma
    # volumes are not well-approximated by the simple torus formula (complex 3D
    # shape, 4-field-period geometry). The design-point paper does not publish
    # a plasma volume. Leaving unset accepts the library default; the radiation
    # calculation will overestimate for this compact geometry, but setting an
    # under-justified 65 m³ could introduce its own errors. The dominant cost
    # drivers (coils, structure, buildings) scale with R0 and plasma_t, not
    # plasma_volume.
    # T_e: design point at ~10 keV (dossier.md §Fuel). Library default 12 keV.
    # Not set — difference is small and density is unknown (data gap #4).
    # n_e: not available in extracted sources (data gap #4).
    # B_peak: 20-40 T on conductor (dossier.md §Magnet Type). Informational only;
    # the library uses b_max from YAML defaults (18 T for STELLARATOR).
)
P_native = 1000  # MWe — analysis Design Point block: "1 GWe"

# Design point notes (informational, not spec kwargs):
# - P_fus ≈ 2000 MW — infoscience-bitstreams...output.md §1: "approximately 2 GW
#   of fusion power". Library back-solves from p_input + P_native.
# - P_th ≈ 2200 MWth — infoscience-bitstreams...output.md §1
# - Thermal cycle: sCO2 Brayton-Rankine at 49-51% gross efficiency (Famà et al.
#   2023). Library STELLARATOR default uses Rankine at 40%. Renaissance's higher
#   efficiency is noted but eta_th is not a spec key (ENUM-driven, Rule 6).
# - Availability: 80% at 40-year lifetime — infoscience-bitstreams...output.md §2.1.
#   Library-owned default; not passed in spec.
# - Radial build: 32 cm liquid metal + 5 cm V-Cr-Ti vessel + 54 cm VH2 shield
#   = 91 cm plasma-to-HTS. Significantly more compact than library default
#   (blanket_t=0.80 + ht_shield_t=0.20 + structure_t=0.15 + vessel_t=0.10 = 1.25 m).
#   Not overriding individual build thicknesses — the liquid metal wall integrates
#   FW/blanket/shield in a non-standard way that doesn't map cleanly to the
#   library's discrete-layer model.
# - Laser-patterned HTS REBCO film on cylindrical surfaces — no cost data published.

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis §5b: "Override count: 0 enabled overrides." No published cost data
#    from Renaissance Fusion for any subsystem. Multiple accounts (C220101, C220103,
#    CAS21, CAS27) would likely warrant overrides if company-grounded cost data
#    were available. See analysis §5b per-account walkthrough for full rationale.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
