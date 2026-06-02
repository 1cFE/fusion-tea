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
    R0=3.3,              # arc-reactor-specifications.md §3.1 Table 1
    a=1.1,               # arc-reactor-specifications.md §3.1 Table 1
    elon=1.84,           # arc-reactor-specifications.md §3.2.1 Table 1
    triang=0.50,         # arc-reactor-specifications.md §3.2.1 Table 1
    B0=9.2,              # arc-reactor-specifications.md §3.1 (on-axis field)
    Ip=7.8,              # arc-reactor-specifications.md Table 1 (MA)
    p_fus=525.0,         # arc-reactor-specifications.md §3.2.1 (MW)
    p_input=38.0,        # arc-reactor-specifications.md §3.2.1 (13.6 MW ICRF + 25 MW LHCD)
    blanket_t=0.85,      # arc-reactor-specifications.md §3.1 (inboard blanket/shield)
    n_e20=1.3,           # arc-reactor-specifications.md §3.2.1 (volume-average, 10^20 m^-3)
    T_e_keV=13.9,        # arc-reactor-specifications.md §3.2.1 (volume-average)
)
P_native = 233.0         # MWe — arc-reactor-specifications.md §2 Conservative Pilot phase

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    # C220103 (HTS coil) override DISABLED pending vintage discipline (fusion-tea#38,
    # strict F8: only `cost_basis: noak` overrides are admitted).
    # Sorbom 2015 Table 11 publishes $5.1B-$5.2B for the magnet/structure subtotal,
    # but the methodology is vintage-unspecified academic conceptual-design cost
    # via $1.06M/tonne mass scaling from pre-2010 paper reactors (FIRE/BPX/PCASTS/
    # ARIES-RS), with no learning curve applied. The framework runs `noak=True`;
    # the library's NOAK $/kA*m x 8x markup path produces ~$516M for ARC, which
    # sits within the CFS SPARC NOAK target band. Defer to library default until
    # fusion-tea#38 lands the strict F8 cost_basis check.
    {"account": "C220103", "value": 5100.0, "enabled": False,
     "cost_basis": "noak", "provenance": "derived", "source": "arc-reactor-specifications.md §6 Table 11",
     "rationale": "Sorbom et al. 2015 provide a bottom-up magnet cost: 5730 km REBCO tape at $36-198/m (2014 USD) = $103M-$206M material, plus 4350 t SS316LN structure ($42M), 358 t copper ($3.03M), $1.06M/tonne fabrication scaling -> $5.1B-$5.2B fabricated. The $1.06M/tonne scaling averages four pre-2010 conceptual designs (FIRE, BPX, PCASTS, ARIES-RS) with no FOAK/NOAK label and no learning curve applied. Sorbom himself does not classify the value as NOAK. Library default for HTS coils uses calibrated $/kA*m at NOAK (~$516M for ARC at b_center=12T, r_bore=1.85m, 8x tokamak markup) which is consistent with CFS's published SPARC magnet program targets. Defer to library default until fusion-tea#38 lands the strict F8 `cost_basis: noak` requirement (forcing the analyst to either apply a documented learning curve to Sorbom's number or rely on the library default).",
     "blocked_by": "1cFE/fusion-tea#38"},

    {"account": "C220104", "value": 38.0, "enabled": True,
     "cost_basis": "noak", "provenance": "direct", "source": "arc-reactor-specifications.md §3.2.1",
     "rationale": "ARC Conservative Pilot: 38 MW external heating (13.6 MW ICRF + ~25 MW LHCD). Directly published for design point. Library would scale from plasma volume/fusion power; ARC's current-drive-dominated heating (63% bootstrap fraction) requires explicit override."},

    {"account": "CAS27", "value": 160.0, "enabled": False,
     "cost_basis": "noak", "provenance": "derived", "source": "arc-reactor-specifications.md §6 Table 11",
     "rationale": "FLiBe inventory: 950 tonnes at $154/kg (2014 USD) = $146M material (initial blanket fill, distinct from blanket structure C220101). However, $154/kg is 2014 vintage and FLiBe not produced at industrial scale. Library may already include blanket material inventory in C220101; enabling risks double-counting. If enabled: adjust to 2024 USD ($146M × 1.31 ≈ $191M), but FLiBe learning curve (Araiinejad 2025 ~20% learning rate) could drive to $120–150M at NOAK. Use $160M midpoint if needed.",
     "blocked_by": "1cFE/1costingfe#1"},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
