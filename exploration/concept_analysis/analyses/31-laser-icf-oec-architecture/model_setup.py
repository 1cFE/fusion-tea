"""1costingfe model: Laser ICF OEC Architecture (BLF) (Blue Laser Fusion).

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
from costingfe.validation import CostingInput, default_availability
from lib.model_setup_helpers import (
    enabled_overrides, generic_reference, run_native_and_1gw, print_cas_breakdown,
)

# 1. Specification — design-point inputs only, at native scale.
#    Sunahara et al. (2025) Optics Express paper provides laser physics and power
#    balance but minimal reactor geometry. Archetype-Fit: Low (IFE with hybrid
#    thermal + DEC conversion modeled as pure-thermal LASER_IFE archetype).
#
#    Mapping published design point (analysis.md §5) to canonical CostingInput
#    spec fields:
#
#    plasma_t (chamber radius): Paper §4.1 gives 8–10 m chamber radius (medium
#      confidence). Midpoint 9 m used. YAML default is 4.0 m — half the published
#      value — which would undersize all radial-build-dependent costs (blanket,
#      shield, structure, vessel volumes scale as r²). For a Low archetype-fit
#      concept the prompt requires populating spec with published values.
#
#    q_eng (engineering gain): Derivable from published power balance. P_grid =
#      2820 MWe, P_recirc = 600 MW (500 MW laser + 100 MW facility), so q_eng =
#      P_grid / P_recirc ≈ 4.7. YAML default is 4.0. Using the paper's power
#      balance rather than the default.
#
#    mn (neutron multiplier): Paper §4.2 states M_n = 1.10 from exothermic
#      6Li(n,α)T blanket reaction. YAML default is 1.1 — matches. Not overridden.
#
#    f_rep (repetition rate): Paper Table 2 states 10 Hz. YAML default is 10.0 Hz
#      — matches. Not overridden.
#
#    NOT in spec (blocked or not canonical):
#    - eta_pin (0.10 wallplug): Hard Rule 6 blocker. YAML default 0.10 matches
#      the paper's composite η_w* = 0.16 × 0.60 = 0.10. Documented, not passed.
#    - eta_th (0.44 thermal): Hard Rule 6 blocker. Library-owned via PowerCycle
#      ENUM. Paper's 0.44 includes 10% exothermic Li-6 boost over base 0.40.
#    - eta_dec (0.44 DEC): Hard Rule 6 blocker. DEC channel (30% of P_fus) not
#      expressible in LASER_IFE pulsed_conversion=thermal mode anyway.
#    - p_fus (8000 MW): Never a spec key (back-solved by library).
#    - E_driver (5 MJ laser energy): Not a CostingInput field; library back-solves
#      driver energy from q_eng + f_rep + eta_pin via inverse power balance.
#    - f_dec: Not in PULSED_REQUIRED; LASER_IFE uses pulsed_conversion=thermal.
#      BLF's 30% DEC channel is a modeling gap (no hybrid thermal+DEC mode exists).
spec = dict(
    plasma_t=9.0,   # chamber radius [m], midpoint of 8–10 m (paper §4.1, medium confidence)
    q_eng=4.7,      # P_grid/P_recirc = 2820/600 (paper Table 2 power balance)
)
P_native = 2820  # MWe — analysis.md Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    BLF (Sunahara et al. 2025) publishes zero dollar figures for any subsystem.
#    Two overrides are derived from IFE comparable literature (Xcimer KrF $/J
#    bracket for C220104; Goodin et al. 2004 DD target factory for C220108).
#    Remaining 14 accounts reviewed — no analogue evidence narrows them beyond
#    the library default. Override count (2) falls below the expected 6–12 band
#    for Low archetype-fit; the shortfall reflects genuinely thin economic data
#    for this paper-concept, not analytical omission.
overrides = [
    {
        "account": "C220104",
        "value": 2000.0,
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": (
            "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md"
            " §Xcimer Laser Cost and Schedule;"
            " optics-express-2025-paper.md §Table 2"
        ),
        "rationale": (
            "BLF publishes no laser driver cost. Bracketed from IFE comparable"
            " literature: Xcimer KrF excimer $60–$80/J NOAK (Xcimer white paper);"
            " DPSSL class $700–$1,000/J (ibid.). BLF E_L = 5 MJ UV on target."
            " OEC/CBC fiber laser architecture is structurally between excimer"
            " (commodity gas laser) and DPSSL (specialty glass amplifiers)."
            " Central estimate: ~$400/J × 5 MJ = $2,000M. Geometric-mean"
            " positioning — fiber lasers share the commodity-component argument"
            " with excimer but lack excimer's published cost basis."
            " Range: $350M ($70/J excimer-like) to $4,250M ($850/J DPSSL-like)."
        ),
    },
    {
        "account": "C220108",
        "value": 219.0,
        "enabled": True,
        "provenance": "derived",
        "cost_basis": "noak",
        "source": (
            "osti-servlets-purl-828518/output.md"
            " §IV.A. Direct Drive Target Cost Analysis Results"
        ),
        "rationale": (
            "BLF publishes no target factory cost. Derived from Goodin et al."
            " (2004, GA-A24429) nth-of-a-kind DD target factory for 1 GWe IFE"
            " plant: $100M installed capital (2004$), 500K targets/day."
            " BLF at 10 Hz needs ~864K targets/day."
            " CPI 2004→2024 factor ~1.59 → $159M;"
            " throughput scale-up 1.7× at 0.6 exponent → 1.7^0.6 ≈ 1.38"
            " → $159M × 1.38 ≈ $219M."
            " Excludes tritium plant (separate account). High uncertainty:"
            " BLF cryogenic D-T targets may differ from GA reference design."
        ),
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# ── F-2: DEC-Unavailable Sensitivity Scenario ───────────────────────────────
# The BLF design routes 30% of fusion power through direct energy conversion at
# η_DEC = 0.44 (TRL ~2, no hardware design). The LASER_IFE archetype models 100%
# thermal conversion, so the model cannot express the hybrid thermal+DEC mode
# directly. At the native design point η_th = η_DEC = 0.44, making the structural
# mismatch numerically invisible. This scenario bounds the LCOE impact if DEC is
# unavailable and the 30% charged-particle energy is simply lost (no recovery path
# designed):
#
#   Native: P_fus = 8000 MW, η_e = 0.44, P_gross ≈ 3520 MWe, P_recirc = 600 MW,
#           P_net = 2820 MWe, q_eng = 2820/600 = 4.7
#   DEC-off: 30% charged-particle energy lost → effective η_e = 0.7 × 0.44 = 0.308,
#           P_gross ≈ 2464 MWe, P_recirc = 600 MW (laser+facility unchanged),
#           P_net ≈ 1864 MWe, q_eng = 1864/600 ≈ 3.1
#
# The q_eng reduction from 4.7 → 3.1 captures the DEC-off power balance via the
# library's existing machinery (q_eng drives recirculating fraction and net output).
_spec_dec_off = dict(spec, q_eng=3.1)
_P_dec_off = 1864  # MWe — analysis.md §2.4 DEC-off derivation

_dec_off = model.forward(
    net_electric_mw=_P_dec_off,
    n_mod=1,
    availability=default_availability(model.concept),
    lifetime_yr=CostingInput.model_fields["lifetime_yr"].default,
    noak=True,
    cost_overrides=enabled_overrides(overrides),
    override_reference_mw=_P_dec_off,
    **_spec_dec_off,
)

print()
print("=" * 60)
print("F-2: DEC-UNAVAILABLE SENSITIVITY SCENARIO")
print("=" * 60)
print("If DEC (TRL ~2) is unavailable, the 30% charged-particle energy is lost.")
print("Effective η_e drops from 0.44 → 0.308; P_net drops from 2820 → 1864 MWe.")
print(f"  Native  (DEC on):  q_eng=4.7, P_net=2820 MWe, LCOE={native.costs.lcoe:.1f} $/MWh")
print(f"  DEC-off scenario:  q_eng=3.1, P_net=1864 MWe, LCOE={_dec_off.costs.lcoe:.1f} $/MWh")
_lcoe_delta = float(_dec_off.costs.lcoe) - float(native.costs.lcoe)
print(f"  LCOE delta: +{_lcoe_delta:.1f} $/MWh ({_lcoe_delta / float(native.costs.lcoe) * 100:.0f}% increase)")
print(f"  Overnight: {native.costs.overnight_cost:.0f} → {_dec_off.costs.overnight_cost:.0f} $/kW")
print("DEC availability is a first-order economic risk for the BLF concept.")
