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
#
#    Z-IFE reference plant (SAND2006-7148): 10-chamber, 0.1 Hz per chamber,
#    thick-liquid FLiBe curtain blanket/shield, LTD pulsed-power driver.
#    Archetype-Fit: High (MAGLIF archetype matches Z-IFE/MagLIF architecture).
#
#    Most Z-IFE design-point parameters (target yield, driver stored energy,
#    driver efficiency 60%, thermal efficiency 42%, plant capacity factor 85%,
#    indirect cost fraction 93.6%) are either:
#      (a) not canonical MAGLIF spec keys (target yield, driver energy),
#      (b) blocklisted efficiencies (eta_th, eta_pin — library-owned), or
#      (c) financial/operating parameters (availability, lifetime_yr — library-owned).
#
#    The MAGLIF YAML default f_rep=0.1 Hz matches the Z-IFE per-chamber rep rate,
#    so it is not re-passed. The p_input parameter is not in the MIF forward()
#    signature (MIF concepts use q_eng for the inverse power balance, not p_input).
#
#    Published driver efficiency is 60% (LTD era); library default eta_pin=0.15.
#    Per contract, eta_pin is never a spec key. The mismatch is noted but accepted.
#
#    Published aggregate fusion power ~1.6 GW; p_fus is never a spec key (back-solved).
spec = dict(
    blanket_t=1.0,   # 1 m FLiBe shielding (z-ife-sand2006-7148-thermal-cycles.md §4.2.1)
                      # YAML default 0.80; Z-IFE pocket has "1 m of FLiBe shielding
                      # all structures from neutrons, X-rays, and debris"
)

P_native = 200  # MWe — Pacific Fusion's published commercial-plant range is
                # 100-300 MWe per their public roadmap; 200 is the midpoint.
                # Previous value (1000 MWe) was the Sandia Z-IFE reference
                # design (SAND2006-7148 §3.1.1.3), which Pacific Fusion does
                # NOT claim — that was inherited from the academic reference
                # paper, not the company's stated target.

# 2. Model.
model = CostModel(concept=ConfinementConcept.MAGLIF, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#
#    0 enabled overrides. Archetype-fit: High, expected band 0–4.
#    The Z-IFE study has substantial cost data but none yields an extractable
#    total-plant driver figure for the 10-chamber baseline: the $372M detailed
#    estimate is for a single 1 PW reference driver, each of the 10 chambers
#    has its own independent (smaller) driver, and the systems model uses a
#    parametric $15/J assumption rather than a company-grounded cost.
overrides = [
    {
        "account": "C220107",
        "value": 372.0 * 1.57,  # $584M — $372M (2004$) × 1.57 CPI → 2024$
        "enabled": False,
        "blocked_by": "1cFE/fusion-tea#47",
        "provenance": "derived",
        "source": "z-ife-sand2006-7148-thermal-cycles.md §3.1.2",
        "rationale": (
            "DISABLED — driver-count contradiction (F-1). The prior rationale incorrectly "
            "claimed the 10-chamber baseline shares one driver; §3.1.1.3 states each chamber "
            "has an independent driver, heat transfer system, and power conversion system. "
            "The $372M (2004$) detailed estimate is for a single 1 PW LTD reference driver — "
            "a much larger unit than any individual 10-chamber driver. Applying it as the "
            "total plant driver cost understates driver capital by up to ~10×. The systems "
            "model used $15/J × per-chamber energy × 10 chambers (§3.1.1.2), not the $372M "
            "figure. Neither cost model provides an extractable company-grounded total-plant "
            "driver cost: the $15/J is a researcher-estimated parametric assumption, and the "
            "$372M applies to the wrong scale of driver. Override disabled until a traceable "
            "total-plant driver cost can be derived."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
