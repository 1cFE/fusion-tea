"""1costingfe model: Laser ICF Hybrid Drive (Xcimer Energy) (Xcimer Energy).

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
    generic_reference, run_native_and_1gw, print_cas_breakdown,
    enabled_overrides,
)

# 1. Specification — design-point inputs only, at native scale.
#    Xcimer Athena pilot power plant (Galloway & Valys, XEC whitepaper Feb 2026).
#    Archetype-Fit: Low — LASER_IFE is the closest available ConfinementConcept
#    but does not model the KrF excimer + NLO beam-combining architecture, the
#    sub-Hz high-yield-per-shot regime, or the thick-liquid FLiBe chamber.
#
#    Key pulsed IFE parameters mapped from the analysis:
#    - q_eng = 5.5: Athena-native Q_eng at 5% laser WPE and Qc >200.  The whitepaper
#      §Next Steps gives a NOAK recirc fraction of 11-13% at 7% WPE / 250 Qsci
#      (Q_eng ~8.2), but Athena is a pilot-demonstrator at 5% WPE.  At 5% WPE the
#      recirc fraction rises to ~18%, yielding Q_eng ~5.5 (analysis §5 derivation).
#      Sensitivity sweep below covers [5.5, 6.5, 8.2] per F-2.
#    - f_rep = 0.7: whitepaper §Roadmap "just under once per second"; the mid-range
#      of the stated 0.25-1 Hz commercial band.
#
#    eta_pin (laser wall-plug efficiency): whitepaper states 5-7% for Xcimer's KrF+NLO
#    architecture. Library default is 0.10 (10%). Per framework rules, eta_pin is not
#    a spec key — the library default governs. The Xcimer value being LOWER than the
#    default means the library is more optimistic on recirculating power than the
#    published architecture; this is accepted as a cross-concept standardization choice.
#
#    No chamber geometry is published. Library YAML defaults (plasma_t=4.0 m chamber
#    radius, blanket_t=0.80 m, etc.) are used.
spec = dict(
    q_eng=5.5,    # Engineering Q (Athena-native at 5% WPE); analysis §5 derivation
    f_rep=0.7,    # Repetition rate [Hz]; xec-whitepaper §Roadmap "just under once per second"
    p_target=1.0,  # Target factory power [MW]; no Xcimer-specific data, library default
    # p_trit: library default 10.0 MW adequate for DT with FLiBe extraction
    # plasma_t: no chamber radius published; using YAML default 4.0 m
    # blanket_t, ht_shield_t, structure_t, vessel_t: no Xcimer data; YAML defaults
    # mn: neutron energy multiplier; YAML default 1.1 adequate for DT
)

P_native = 400  # MWe — xec-whitepaper §Roadmap: "8 MJ on-target / 400 MWe output"

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — transcribed from analysis.md Section 5b.
#    7 enabled overrides for Low archetype-fit (expected band: 6-12).
#    C220104: NOAK midpoint used ($560M) instead of analysis FOAK value ($960M),
#    because cost_basis must be "noak" and the whitepaper provides NOAK range.
#    CAS70 omitted: not overridable in 1costingFE; silently dropped (1cFE/1costingfe#106).
overrides = [
    # C220104: Primary pulsed driver — KrF excimer laser with NLO beam combining.
    # Xcimer published NOAK laser cost: $60-$80/J on-target (whitepaper Table 1).
    # At 8 MJ on-target: midpoint $70/J × 8 MJ = $560M.
    {
        "account": "C220104",
        "value": 560.0,
        "enabled": True,
        "provenance": "direct",
        "source": "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer Laser Cost and Schedule",
        "rationale": (
            "Xcimer published NOAK laser cost of $60-$80/J on-target (whitepaper Table 1 "
            "with component breakdown: capacitors, Marx generators, e-beam, laser chamber, "
            "optics, NLO/seed, controls). At 8 MJ on-target for Athena: midpoint $70/J × "
            "8 MJ = $560M. FOAK range is $100-$120/J ($800M-$960M). Library default for a "
            "generic laser IFE driver does not reflect the KrF excimer + NLO architecture. "
            "Architecture never built at MJ scale; Phoenix prototype (1-2 kJ, Q2 2026) is "
            "first integration test."
        ),
        "cost_basis": "noak",
    },
    # C220107: Pulsed-power capacitor bank — zeroed (double-count avoidance).
    # Xcimer's Marx generator capacitor bank is internal to the laser driver and
    # fully costed in C220104. No separate standalone pulsed-power bank.
    {
        "account": "C220107",
        "value": 0.0,
        "enabled": True,
        "provenance": "direct",
        "source": "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer Laser Cost and Schedule",
        "rationale": (
            "Xcimer's architecture is a gas excimer laser, not an electrically-driven pulsed "
            "scheme. The capacitor bank (Marx generators) is internal to the laser driver and "
            "is fully costed in C220104. There is no separate standalone pulsed-power capacitor "
            "bank. C220107 zeroed to avoid double-counting with C220104."
        ),
        "cost_basis": "noak",
    },
    # C220101: First wall / blanket — thick-liquid FLiBe jet wall replaces solid blanket.
    {
        "account": "C220101",
        "value": 0.40 * generic.cas22_detail["C220101"],
        "enabled": True,
        "provenance": "derived",
        "source": "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Chamber Design",
        "rationale": (
            "Xcimer's thick-liquid FLiBe jet wall replaces the conventional solid first wall "
            "and blanket module. There is no solid breeding blanket structure — the flowing "
            "FLiBe itself is the blanket, first wall, and shield. The structural component is "
            "a conventional steel chamber behind the liquid. Cost character is fundamentally "
            "different from a solid blanket (no RAFM steel modules, no Be multiplier pebble "
            "beds, no helium coolant channels). FLiBe inventory cost is captured in CAS27. "
            "0.40x reflects that the 'blanket' is a steel vessel + FLiBe nozzle/pump system "
            "rather than engineered solid blanket modules. No company cost figure; analyst "
            "estimate."
        ),
        "cost_basis": "noak",
    },
    # C220102: Radiation shield — thick-liquid FLiBe provides primary shielding.
    {
        "account": "C220102",
        "value": 0.30 * generic.cas22_detail["C220102"],
        "enabled": True,
        "provenance": "derived",
        "source": "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Chamber Design",
        "rationale": (
            "The thick-liquid FLiBe wall (~50+ cm) provides the primary radiation shielding "
            "function. Xcimer claims 30-year facility lifetime without first-wall replacement. "
            "The structural shield behind the liquid wall is conventional steel, not a "
            "purpose-built nuclear-grade radiation shield. 0.30x reflects that the liquid "
            "itself provides most shielding. No company cost figure; analyst estimate."
        ),
        "cost_basis": "noak",
    },
    # C220108: Target factory — sub-Hz rep rate with simpler targets.
    {
        "account": "C220108",
        "value": 0.60 * generic.cas22_detail["C220108"],
        "enabled": True,
        "provenance": "derived",
        "source": (
            "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Challenge 2; "
            "xcimer-energy-approach.md §Fuel Capsules"
        ),
        "rationale": (
            "Xcimer targets use liquid DT + plastic ablator with no gold hohlraum and no "
            "cryogenic ice layer, operating at sub-Hz rep rate (0.7 Hz for Athena vs 10 Hz "
            "for DPSSL IFE). Target throughput is ~22M/yr vs ~315M/yr for a 10 Hz plant — "
            "an order-of-magnitude reduction in factory scale. The simpler target construction "
            "and dramatically lower throughput should reduce target factory cost substantially. "
            "However, no company-published factory cost exists. 0.60x multiplier is an analyst "
            "estimate reflecting the lower throughput and simpler target; this should be "
            "treated as a sensitivity parameter. Enabled with low confidence."
        ),
        "cost_basis": "noak",
    },
    # CAS21: Buildings — larger footprint due to 50 m standoff and ~100 Argos modules.
    {
        "account": "CAS21",
        "value": 1.25 * generic.costs.cas21,
        "enabled": True,
        "provenance": "derived",
        "source": "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Xcimer Laser Cost and Schedule",
        "rationale": (
            "The 50 m standoff distance from laser to target implies a larger building "
            "footprint than a compact laser IFE plant. The ~100 Argos amplifier modules, "
            "Marx generator banks, and NLO beam combining optics require substantial floor "
            "space. No building cost is published. 1.25x multiplier is an analyst estimate "
            "reflecting the larger footprint; should be treated as a sensitivity parameter."
        ),
        "cost_basis": "noak",
    },
    # CAS27: Special materials — FLiBe initial inventory.
    {
        "account": "CAS27",
        "value": 92.0,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md §Chamber Design; "
            "Araiinejad 2025 FLiBe cost estimate"
        ),
        "rationale": (
            "FLiBe initial inventory for a HYLIFE-III chamber. Xcimer does not publish the "
            "FLiBe mass. HYLIFE-II reference used ~600 t of FLiBe for a 6 Hz, 350 MJ-yield "
            "chamber. Athena operates at lower yield (~1.6 GJ) but sub-Hz rate. Assuming a "
            "comparable ~600 t inventory (uncertain — could range 300-1000 t). At $154/kg NOAK "
            "FLiBe (Araiinejad 2025, adjusted for learning): 600 t x $154/kg = $92.4M ~ $92M. "
            "Both mass and unit cost are analyst-sourced, not company-published. High uncertainty."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)

# ── Sensitivity: Q_eng (F-2 — most critical parameter) ──────────────────────
# Athena pilot at 5% WPE → Q_eng ~5.5 (spec value); NOAK maturity at 7% WPE /
# 250 Qsci → Q_eng ~8.2.  Sweep brackets the range from Athena-native to
# NOAK-mature performance.  Native scale only.
# F-1 fix: apply overrides so sweep values are consistent with the native LCOE.
_avail = default_availability(model.concept)
_life = CostingInput.model_fields["lifetime_yr"].default
_enabled = enabled_overrides(overrides)
print("\nQ_eng sweep (native 400 MWe; 5.5 = Athena 5% WPE, 8.2 = NOAK 7% WPE target):")
for _qe in [5.5, 6.5, 8.2]:
    _r = model.forward(
        net_electric_mw=P_native, n_mod=1,
        availability=_avail, lifetime_yr=_life, noak=True,
        cost_overrides=_enabled,
        override_reference_mw=P_native,
        **{**spec, "q_eng": _qe},
    )
    _mark = "  <- spec (Athena-native)" if _qe == 5.5 else (
        "  <- NOAK target" if _qe == 8.2 else "")
    print(f"  Q_eng={_qe:.1f}: LCOE={_r.costs.lcoe:.1f} $/MWh{_mark}")
