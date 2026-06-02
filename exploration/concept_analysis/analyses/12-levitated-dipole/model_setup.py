"""1costingfe model: Levitated Dipole (OpenStar Technologies).

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
    # Geometry (arxiv-2602-20564-dt-dipole-power-plants.md §Table 5, §Table 7)
    R0=5.3,              # Core magnet outer radius (m)
    # Note: Dipole geometry doesn't use tokamak-style elon/plasma_t; omit them
    # Note: B (or B0) is NOT in CostingInput.model_fields and would be silently
    # dropped by forward() — the coil center field for cost is the YAML's
    # b_center (= 6.26 T, derived from Simpson's B_max=23 T via the
    # peak_to_center_ratio=3.67). Do not re-pass B0=23 here (F7 rejects it).
    # Note: plasma_volume is intentionally OMITTED. Passing Simpson's geometric
    # 13,600 m^3 drives the MFE radiation calc out of its calibrated range
    # (formulas assume uniform profile; dipole is highly peaked, with the
    # radiating core <10% of the geometric volume per Hasegawa-Mauel scaling).
    # The library default plasma_volume=200 m^3 in steady_state_dipole.yaml is
    # NOT the geometric volume — it's a calibrated effective value that
    # produces the right p_fus (~700 MW) against Simpson Reactor A. A proper
    # `radiation_peaking_factor` field is filed as 1costingfe issue (see below).

    # Power flow (arxiv-2602-20564-dt-dipole-power-plants.md §Table 5, §Table 9)
    p_input=44.5,        # Auxiliary heating power (MW ICRH)

    # Note: eta_th=0.40 from §4.4 matches library default RANKINE cycle (0.40),
    # so no PowerCycle override needed. Thermal efficiency is ENUM-owned, not spec-authorable.
)
P_native = 208.0       # MWe — arxiv-2602-20564-dt-dipole-power-plants.md §Table 5

# 2. Model.
model = CostModel(concept=ConfinementConcept.DIPOLE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 1.34 * generic.cas22_detail["C220103"], "enabled": True,
     "cost_basis": "noak", "provenance": "derived",
     "source": "arxiv-2602-20564-dt-dipole-power-plants.md §Table 5, §2.3.1",
     "rationale": "Simpson et al. specify 4,320 km REBCO tape for the full core magnet, with sacrificial section (~20% of coil) replaced annually. The design includes tungsten neutron shield (1,760 t), B₄C (82 t), WC (168 t), and SS316LN structure (351 t) that must be replaced with the sacrificial section. The library default for C220103 prices HTS coils based on conductor but does not account for an in-plasma neutron shield or annual replacement cycle. The override multiplier 1.34 (34% increase) reflects: (1) added tungsten shield mass (~$53M at $30/kg for 1,760 t) amortized over sacrificial lifetime, (2) B₄C/WC shield layers (~$10M combined), and (3) annual replacement labor/hot-cell costs vs. one-time installation."},

    {"account": "CAS70", "value": 0.05 * generic.cas22_detail["C220103"], "enabled": True,
     "cost_basis": "noak", "provenance": "derived",
     "source": "arxiv-2602-20564-dt-dipole-power-plants.md §Table 8, §4.3",
     "rationale": "The sacrificial REBCO section and neutron shield tiles require annual replacement (1.2 year lifetime per Table 8). This creates a recurring O&M cost distinct from the library's default CAS70 model, which assumes staffing-based O&M without major component replacement. Annual replacement cost = (Sacrificial REBCO + tungsten tiles + hot-cell labor) / plant lifetime. Estimating conservatively: sacrificial section is ~5% of full magnet capital cost per year (1.2 year lifetime ≈ annual). The override sets CAS70 additive to 5% of C220103 annually, reflecting this replacement burden."},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
