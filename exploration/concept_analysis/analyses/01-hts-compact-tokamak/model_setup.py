"""1costingfe model: HTS Compact Tokamak (Commonwealth Fusion / ARC) (Commonwealth Fusion Systems).

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
spec = dict(
    R0=3.3,              # arc-reactor-specifications.md §Abstract, Table 1 (major radius)
    plasma_t=1.1,        # arc-reactor-specifications.md §Abstract, Table 1 (minor radius a)
    elon=1.8,            # arc-reactor-specifications.md Table 1 (elongation kappa)
    B=9.2,               # arc-reactor-specifications.md §Abstract, Table 1 (on-axis field, Conservative Pilot)
    p_input=38.6,        # arc-reactor-specifications.md §Abstract (ICRF 13.6 MW + LHCD 25 MW)
)
P_native = 233.0         # MWe — arc-reactor-specifications.md §2

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#
# NOTE: The analysis Section 5b originally identified three override candidates
# (C220103, C220104, CAS27), but all are disabled or removed:
# - C220103 and CAS27: DISABLED because they violate Hard Rule 6 (strict cost_basis="noak"
#   requirement). The Sorbom et al. 2015 values are FOAK estimates, and NOAK adjustment
#   methodology (CPI + learning curves) must be reconciled with the library's own scaling
#   to avoid double-counting. Per Hard Rule 6 option (a): defer to library default when
#   source is FOAK and NOAK adjustment is uncertain.
# - C220104: REMOVED entirely (per F-2) because it provided a quantity (38.6 MW) rather
#   than a dollar cost. The auxiliary heating power is already captured in spec["p_input"],
#   and the library computes C220104 from p_input and its own ICRF/LHCD unit cost model.
overrides = [
    {
        "account": "C220103",
        "value": 5150.0,
        "enabled": False,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "arc-reactor-specifications.md §6, Table 11",
        "rationale": (
            "Sorbom et al. 2015 Table 11 reports fabricated cost for 'Magnet/structure' "
            "of $5.1B–5.2B (midpoint $5.15B) in FY2014 dollars. This encompasses the "
            "REBCO TF coils (5,730 km tape at $36–198/m → $206M–1,134M materials) plus "
            "5,670 tonnes of stainless steel 316LN magnet structure at $1.06M/tonne "
            "fabricated cost. However, this is a FOAK estimate with uncertain NOAK "
            "adjustment. Per Hard Rule 6, deferring to library default pending "
            "methodological reconciliation of Sorbom's FOAK value with library's NOAK "
            "target. CPI adjustment from FY2014 to 2024 is ~1.26; learning-curve "
            "reduction for NOAK would be ~0.7-0.8 (20% per doubling), but double-counting "
            "with library's own scaling must be avoided."
        ),
        "blocked_by": "1cFE/1costingfe#101",
    },
    {
        "account": "CAS27",
        "value": 183.0,
        "enabled": False,
        "cost_basis": "noak",
        "provenance": "derived",
        "source": "arc-reactor-specifications.md §6, Table 10",
        "rationale": (
            "FLiBe inventory: 1,190 tonnes at $154/kg (Sorbom et al. 2015, FY2014 "
            "dollars) = $183M material cost. Sorbom notes 'Since the TiH₂ is in powder "
            "form and the FLiBe is liquid, the fabricated cost for components made from "
            "these materials was set equal to the material cost,' so fabricated cost is "
            "also ~$183M. However, this is a FOAK estimate. CPI adjustment to 2024: "
            "$183M × 1.26 ≈ $231M. A 20% learning rate (per Araiinejad & Shirvan 2025) "
            "would reduce the $154/kg unit cost to ~$120/kg at 10× cumulative FLiBe "
            "production. Per Hard Rule 6, deferring to library default pending "
            "methodological reconciliation of FOAK vs NOAK adjustment."
        ),
        "blocked_by": "1cFE/1costingfe#103",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
