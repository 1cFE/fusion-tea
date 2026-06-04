"""1costingfe model: MagLIF (Pacific Fusion) (Pacific Fusion).

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
#    Z-IFE baseline (10-chamber, 0.1 Hz) specifies limited parameters publicly.
#    The Z-IFE study (SAND2006-7148) provides rep rate and target gain; thermal
#    efficiency (42% for steel chamber, combined Brayton-Rankine) is ENUM-owned
#    by PowerCycle and cannot be set in spec. MagLIF does not have tokamak-style
#    major radius or magnetic field as primary design parameters. The library's
#    default PowerCycle for MAGLIF (THERMAL conversion) will determine eta_th.
spec = dict(
    f_rep=0.1,        # Hz — analysis §5 table, Z-IFE baseline 10-chamber 0.1 Hz
    q_eng=30.0,       # dimensionless — analysis §5 table, target gain from Z-IFE gain formula
)
P_native = 1000.0  # MWe — copied from analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.MAGLIF, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220107", "value": 372.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct", "source": "z-ife-sand2006-7148-thermal-cycles.md §3.1.2",
     "rationale": "Z-IFE study published direct driver cost estimate of $372M for 1 PW LTD-based "
                  "pulsed power driver at $15/J delivered energy (2005 dollars, not CPI-adjusted). "
                  "This is a pulsed-power capacitor bank, not steady-state magnet supplies — fundamentally "
                  "different cost structure from the library's default. The library default is computed "
                  "from magnet geometry and does not account for capacitor banks, switches, transmission "
                  "lines, or LTD/IMG architecture. The $372M figure is median estimate from parametric "
                  "model; Z-IFE notes 'a good unit cost estimate was not received' and used $15/J as "
                  "reference (half the cost of conventional pulsed power at $30/J). Pacific Fusion's "
                  "IMG architecture claims further cost reduction via higher efficiency (90% vs 60%) "
                  "and 2× compactness, but no public bottom-up estimate exists. Enabling this override "
                  "with the Z-IFE LTD figure; an IMG-based plant would likely use a lower value "
                  "($150-250M range), but that is derived/speculative rather than published."},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# =============================================================================
# Interpretive Notes for MagLIF Z-IFE Baseline
# =============================================================================
print("\n" + "=" * 72)
print("INTERPRETATION OF 1 GWe PROJECTION")
print("=" * 72)
print("""
The 1 GWe LCOE projection above represents the Z-IFE 10-chamber 0.1 Hz
baseline design point (Olson et al., SAND2006-7148), with one enabled
cost override for the pulsed power driver (C220107 = $372M).

This projection reflects:
  • 10 chambers × 0.1 Hz repetition rate = 1 shot per 10 seconds per chamber
  • Target gain G = 30 (from Z-IFE gain scaling formula)
  • Thermal efficiency from library PowerCycle default (Z-IFE study: 42% for steel
    chamber combined Brayton-Rankine, but eta_th is ENUM-owned and not overridable)
  • Linear Transformer Driver (LTD) at $15/J delivered energy
  • Thick liquid FLiBe wall (80 cm) for neutron shielding and first-wall protection

**Critical context (analysis.md §2):**
  1. **Rep rate as first-order economic parameter**: The Z-IFE study found
     baseline 0.1 Hz operation yields ~20 ¢/kWh LCOE ("factor of 2-3 higher
     than needed to compete"), while optimized single-chamber 0.5 Hz operation
     achieves 7.0 ¢/kWh. Rep rate is the single most leveraged parameter —
     comparable to or exceeding fusion gain itself.

  2. **Per-shot consumable costs**: Each shot destroys the target liner and
     recyclable transmission line (RTL). Z-IFE estimated ~$0.70/shot for RTL.
     At 1 Hz (Pacific Fusion target), this is ~28M shots/year. Pacific Fusion's
     self-magnetizing composite targets eliminate external coil destruction
     (addressing "showstopper" economics) but combined target + RTL cost at
     volume production is uncharacterized.

  3. **Driver capital cost dominates**: The $372M driver is 40-60% of total
     direct capital. Pacific Fusion's IMG architecture claims 90% efficiency
     (vs. 60% LTD) and 2× compactness, potentially reducing driver cost to
     $150-250M, but no public bottom-up estimate exists.

**This design point vs. commercial target:**
The Z-IFE baseline (10 chambers, 0.1 Hz) is economically uncompetitive by the
study's own assessment. The commercial target is single-chamber high-rep-rate
operation (0.5-1 Hz) with IMG driver and potentially laser-free operation.
Pacific Fusion demonstrated self-magnetizing targets (Oct 2025) and states
eliminating laser preheat is their next objective, which would reduce the
system to pulser + targets only.

**Grounding confidence:** Medium. The Z-IFE study (2006) predates modern
MagLIF target physics (self-magnetization, ice-layer targets) and IMG
architecture. Critical parameters remain uncharacterized: achieved rep rate
above single-shot mode, target/RTL manufacturing cost at MHz scale, capacitor/
switch lifetime at 10⁹ shots, and chamber clearing timescales at GJ-scale
blast energies. The design point is paper-concept (no prototype, no operational
data); the override is grounded in a published parametric model but carries
significant uncertainty.

**Data gaps (analysis.md §6):**
  • Rep rate demonstration (blocking): 0.1 Hz assumed, 1 Hz target, no public
    data above single-shot mode
  • Target/RTL fabrication cost at 28M units/year (blocking)
  • IMG driver bottom-up cost (blocking): $372M LTD baseline vs. $150-250M
    IMG expectation
  • Ice-layer target production (important if needed for GJ yields)
  • Chamber clearing timescale (determines max rep rate)
  • Capacitor/switch lifetime at 10⁹ shots (important)
""")

print("=" * 72)
