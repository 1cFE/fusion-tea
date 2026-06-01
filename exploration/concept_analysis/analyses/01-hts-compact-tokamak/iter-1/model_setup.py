"""1costingfe model: HTS Compact Tokamak (Commonwealth Fusion / ARC) (Commonwealth Fusion Systems).

Design point: ARC 2015 "Conservative Pilot" phase (Sorbom et al. 2015), 233 MWe net.
The plasma/machine hardware is identical across the FNSF / conservative-Pilot /
aggressive-Pilot phases; only the blanket outlet temperature and resulting thermal
efficiency change. Cost overrides are grounded in the paper's FY2014 subsystem
cost tables (Tables 10-11), escalated CPI-U FY2014->2024 (x1.33).

Note on eta_th: ARC's 46% Brayton efficiency is contingent on unproven 1100 K
blanket-outlet materials (the demonstrated-material FNSF floor is ~40%, which is
the library default). Per the contract, an aspirational published efficiency is
not grounds to override the archetype default, so eta_th is left to the library
and carried as a sensitivity sweep below (analysis Gap 3 / Section 5).

Usage:
    uv run python model_setup.py              # print results
    uv run python model_setup.py | tee model_output.txt
"""
import sys
from pathlib import Path

# Make the shared four-step helper importable regardless of where this file
# lives (concept dir or iter-N/ dir): walk up to the scripts/ root.
_SCRIPTS = next(
    p / "scripts"
    for p in Path(__file__).resolve().parents
    if (p / "scripts" / "lib" / "model_setup_helpers.py").exists()
)
sys.path.insert(0, str(_SCRIPTS))

from costingfe import ConfinementConcept, CostModel, Fuel
from costingfe.validation import CostingInput, default_availability
from lib.model_setup_helpers import (
    generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# 1. Specification — design-point inputs only, at native scale.
spec = dict(
    # Geometry — ARC 0-D design point (conventional aspect ratio A=3.0).
    R0=3.3,        # major radius [m]; arc-reactor-specifications.md §3 ("increased from 3.2 to 3.3 m")
    plasma_t=1.13, # minor radius a [m]; arc-reactor-specifications.md §Table 7 (1/eps = 3)
    elon=1.84,     # elongation kappa; arc-reactor-specifications.md §Table 7
    plasma_volume=153.0,  # 2*pi^2*R0*a^2*kappa = 153 m^3; derived from published R0/a/kappa
    # Magnetic field — the defining high-field knob of the concept.
    B=9.2,         # on-axis toroidal field [T]; arc-reactor-specifications.md §3 ("fixed in the design")
    b_max=23.0,    # peak field on conductor [T]; arc-reactor-specifications.md §4 (defining high-field knob)
    # Auxiliary heating & current drive — 25 MW LHCD (8 GHz) + 13.6 MW ICRF (50 MHz).
    p_input=38.6,  # total aux H&CD power [MW]; arc-reactor-specifications.md §3
    p_nbi=0.0,     # no neutral-beam injection on ARC
    p_ecrh=0.0,
    p_icrf=13.6,   # ICRF fast wave [MW]; arc-reactor-specifications.md §3
    p_lhcd=25.0,   # LHCD [MW]; arc-reactor-specifications.md §3 (mix sums to p_input = 38.6)
)
P_native = 233.0   # MWe — copied from the analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale. The library's bare
# answer for a reactor this size, and the reference a relative override would be
# written against (these overrides are all absolute, so none reference it here).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 5200.0 * 1.33, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6 Table 11",
     "rationale": (
         "Sorbom 2015 publishes a magnet/structure subtotal of $5.1-5.2B fabricated "
         "(FY2014). Upper estimate $5,200M x 1.33 (CPI-U 2014->2024) = $6,916M. The "
         "figure is dominated NOT by REBCO conductor ($100-210M tape + $380M copper "
         "winding) but by 4,350 t of SS316LN structural steel ($4.6B fabricated) "
         "reacting the 23 T peak-field forces. The library default prices HTS coils "
         "from conductor geometry/length and undercounts the ARC magnet by ~10x "
         "because it misses the structural-steel cage. Single largest, best-justified "
         "departure for the archetype. Note: the subtotal bundles the magnet tension "
         "ring (~$9M) and a steel machine base a finer breakdown would assign to "
         "C220105; kept here because the mass exists to react coil loads.")},
    {"account": "C220101", "value": 108.1 * 1.33, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6 Table 11",
     "rationale": (
         "First wall (1 cm W, 3.72 t -> $4.03M) + Be neutron multiplier (3.82 t -> "
         "$4.1M) + Inconel 718 blanket tank structure (97.1 t -> $100M) = $108.1M "
         "FY2014. x 1.33 (CPI 2014->2024) = $143.8M. Prices the structural "
         "blanket/first-wall/multiplier from ARC's published neutronics-derived "
         "volumes, excluding the FLiBe fill (-> CAS27). The library default does not "
         "see ARC's thin-wall liquid-immersion architecture (~85 t total vessel solid mass).")},
    {"account": "CAS27", "value": 147.5 * 1.33, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6 Table 11",
     "rationale": (
         "Initial FLiBe inventory: ~958 t x $154/kg = $147.5M FY2014 (channel 8.07 t + "
         "blanket tank 475 t + heat-exchanger loop 475 t). x 1.33 (CPI 2014->2024) = "
         "$196.2M. Both quantity (958 t) and unit price ($154/kg) are published in the "
         "same table, so the FY2014 figure is direct; CPI escalation makes the "
         "delivered value derived. FLiBe is a special-material blanket fill distinct "
         "from the C220101 structure, with a beryllium- and Li-6-enrichment-driven "
         "price the generic special-materials default would not capture.")},
    {"account": "C220108", "value": 17.5 * 1.33, "enabled": True,
     "provenance": "derived", "source": "arc-reactor-specifications.md §6.3",
     "rationale": (
         "The 2015 design defers the divertor ('left as an open question') and gives "
         "only a rough estimate: a 2 cm tungsten divertor over ~20% of first-wall "
         "area, ~$500k materials -> ~$17.5M fabricated (FY2014). x 1.33 = $23.3M. "
         "Enabled because it is the only ARC-grounded divertor figure, but flagged "
         "low-confidence: a placeholder for an undesigned subsystem, not a costed "
         "design (Data Gap #2).")},
]

# 4. Both forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# ── Sensitivity: thermal efficiency (analysis Gap 3 / Section 5) ─────────────
# ARC's 233 MWe rests on an aspirational 1100 K / ~46% Brayton cycle; the
# demonstrated-material FNSF floor is ~40% (= library default). Sweep eta_th
# 40-50% on the native design point to show the LCOE elasticity of this
# materials-contingent assumption. (Native scale only; not run for result_1gw.)
_avail = default_availability(model.concept)
_life = CostingInput.model_fields["lifetime_yr"].default
print("\neta_th sweep (native 233 MWe; 40% = FNSF demonstrated floor, 46% = conservative-Pilot target):")
for _eta in [0.40, 0.43, 0.46, 0.50]:
    _r = model.forward(
        net_electric_mw=P_native, n_mod=1,
        availability=_avail, lifetime_yr=_life, noak=True,
        **{**spec, "eta_th": _eta},
    )
    _mark = "  <- conservative-Pilot target" if _eta == 0.46 else (
        "  <- FNSF demonstrated floor" if _eta == 0.40 else "")
    print(f"  eta_th={_eta:.2f}: LCOE={_r.costs.lcoe:.1f} $/MWh{_mark}")

# ── Sensitivity (JAX autodiff) on the generic (overrides-off) design point ───
sens = model.sensitivity(generic.params)

print("\nSensitivity (elasticity = %LCOE / %param) — generic design point")
print("\nEngineering levers:")
for k, v in sorted(sens["engineering"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")
print("\nFinancial:")
for k, v in sorted(sens["financial"].items(), key=lambda x: abs(x[1]), reverse=True):
    print(f"  {k:<36} {v:+.4f}")
print("\nCosting constants (top 15):")
for k, v in sorted(sens["costing"].items(), key=lambda x: abs(x[1]), reverse=True)[:15]:
    print(f"  {k:<36} {v:+.4f}")
