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

P_native = 1000  # MWe — z-ife-sand2006-7148-thermal-cycles.md §3.1.1.3

# 2. Model.
model = CostModel(concept=ConfinementConcept.MAGLIF, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#
#    1 enabled override (C220107 — pulsed power driver). Archetype-fit: High,
#    expected band 0–4. The single override reflects the pulsed power driver as
#    the architecturally distinctive and cost-dominant subsystem, with the Z-IFE
#    study providing the only bottom-up cost estimate available.
overrides = [
    {
        "account": "C220107",
        "value": 372.0 * 1.57,  # $584M — $372M (2004$) × 1.57 CPI → 2024$
        "enabled": True,
        "provenance": "derived",
        "source": "z-ife-sand2006-7148-thermal-cycles.md §3.1.2",
        "rationale": (
            "Z-IFE study (SAND2006-7148) provides detailed Monte Carlo cost estimate for "
            "a 1 PW LTD-based driver: $372M median in 2004 dollars. 12,600 LTD cavities "
            "at $28,000 median each (96% of driver cost). CPI adjustment 2004→2024: ×1.57 "
            "gives ~$584M NOAK. The Z-IFE study's cost analysis methodology (Monte Carlo on "
            "unit costs with learning-curve assumptions for large-batch LTD cavity production) "
            "is inherently a NOAK-vintage estimate: the 12,600 cavities at $28k/ea median "
            "already assumes nth-unit manufacturing costs, not prototype pricing. The 10-chamber "
            "baseline uses one driver shared across chambers (via staggered firing), so this is "
            "a single capital item. The library default $/J formula may not capture the specific "
            "LTD module cost structure. Note: IMG architecture (Pacific Fusion) claims significant "
            "cost reduction over LTD, but no published IMG driver cost exists."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
