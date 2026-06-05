"""1costingfe model: Projectile ICF (First Light Fusion).

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
#    First Light projectile pilot plant (2022 pre-pivot ~150 MWe target).
#    Archetype-Fit: Low — HEAVY_ION (heavy-ion beam IFE) is the closest
#    available archetype but First Light's projectile approach is structurally
#    different: electromagnetic gun driver (not a heavy-ion accelerator), sub-Hz
#    rep rate (not 5-10 Hz), and liquid lithium curtain chamber (not FLiBe jets).
#
#    Data availability is Limited (Section 1). No published systems engineering
#    design, thermal-hydraulic layout, or energy balance exists for the 150 MWe
#    pilot plant. The only canonical spec key with a design-point-grounded value
#    differing from YAML defaults is f_rep.
#
#    Parameters NOT in spec (no canonical spec key or library-owned):
#    - target_gain (200-1000): no spec key; library uses q_eng for power balance
#    - driver_energy_MJ (~100 MJ stored): no spec key; library derives from q_eng
#    - projectile_speed (~60 km/s): no spec key
#    - eta_pin (~10-20% EM gun wall-plug): library-owned per Rule 6
#    - q_eng: YAML default 4.0; analysis estimates similar range from gain/efficiency
#      but no published Q_eng value. Accepting YAML default.
spec = dict(
    f_rep=0.033,  # prnewswire §Fusion Facts: "every 30 seconds" = 0.033 Hz
)
P_native = 150  # MWe — prnewswire §Next Steps: "~150 MW of electricity"

# 2. Model.
model = CostModel(concept=ConfinementConcept.HEAVY_ION, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3).
#     Run first WITHOUT installation_frac correction so we can read the
#     pre-override reactor subtotal that the library computed.
generic = generic_reference(model, spec, P_native)

# 2c. Correct installation_frac to compensate for the library computing
#     C220111 = installation_frac × pre-override reactor subtotal.
#     Cost overrides reduce CAS22 equipment from $13,247M to ~$301M, but
#     C220111 is computed in cas22.py BEFORE cost_overrides are applied in
#     model.py. At default installation_frac=0.14, C220111 = 0.14 × $13,247M
#     = $1,855M — more than 6× the post-override equipment. The physical
#     intent is 14% of the post-override subtotal (~$301M → ~$42M).
#     We set installation_frac = 0.14 × (post_override / pre_override) so
#     the library's computation produces the correct dollar amount.
#     Derivation: see analysis.md §5b C220111 entry.
_REACTOR_ACCTS = ["C220101", "C220102", "C220103", "C220104", "C220105",
                  "C220106", "C220107", "C220108", "C220109", "C220110"]
_pre_override_subtotal = sum(generic.cas22_detail[k] for k in _REACTOR_ACCTS)
# Post-override subtotal — mirror the enabled overrides (C220102 at 15%,
# C220104→$200M, C220107→$0, C220108→$5.6M, C220110 at 30%); accounts
# without an enabled override keep their generic value.
_post_override_subtotal = (
    generic.cas22_detail["C220101"]               # no enabled override
    + generic.cas22_detail["C220102"] * 0.15      # C220102 override
    + generic.cas22_detail["C220103"]              # no override
    + 200.0                                        # C220104 override
    + generic.cas22_detail["C220105"]              # no override
    + generic.cas22_detail["C220106"]              # no override
    + 0.0                                          # C220107 override
    + 5.6                                          # C220108 override
    + generic.cas22_detail["C220109"]              # no override
    + generic.cas22_detail["C220110"] * 0.30       # C220110 override
)
spec["installation_frac"] = float(
    0.14 * _post_override_subtotal / _pre_override_subtotal
)

# Re-run generic forward WITH the corrected installation_frac so all three
# forwards (generic, native, 1 GWe) use the same spec consistently.
generic = generic_reference(model, spec, P_native)

# 3. Override registry — transcribed from analysis.md Section 5b.
#    6 enabled, 1 disabled = 7 registry entries. Expected band for Low
#    archetype-fit: 6-12. 4 overrides grounded in company-published cost data
#    or peer-reviewed analysis; 2 are derived corrections for structural
#    mismatches between the HEAVY_ION archetype and the liquid-lithium-curtain,
#    sub-Hz, EM-gun architecture; 1 disabled with documented rationale.
#    C220111 (installation labor) is corrected via installation_frac in spec
#    rather than a direct C220111 override (derived rollup, forbidden by
#    validator). See spec comment for derivation. C220200 (heat transport)
#    structural mismatch is documented in-line but not as a registry entry
#    because C220200 is a CAS22.2 sub-rollup (forbidden override target).
overrides = [
    # C220101: First wall / blanket — liquid lithium curtain replaces solid blanket.
    # Disabled: structural mismatch acknowledged but no quantitative correction
    # derivable without double-counting the lithium inventory already in CAS27.
    {
        "account": "C220101",
        "value": generic.cas22_detail["C220101"],
        "enabled": False,
        "provenance": "derived",
        "source": (
            "dossier.md §Neutron Management; "
            "prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
        ),
        "rationale": (
            "Library default ($64.8M) prices a solid blanket with neutron multiplier. "
            "First Light uses flowing liquid lithium curtains serving as blanket, shield, "
            "and first wall simultaneously — structurally different. The curtain cost is "
            "better captured by the lithium inventory (CAS27 = $70M) plus the EM pump "
            "system (C220200). No company-published dollar figure for blanket alone. "
            "Disabled: structural mismatch acknowledged but no quantitative correction "
            "derivable without double-counting CAS27."
        ),
        "cost_basis": "noak",
        "blocked_by": "1cFE/fusion-tea#46",
    },
    # C220102: Radiation shield — 1 m lithium curtain absorbs all neutrons;
    # no dedicated solid shield described.  Retain 15% of generic for
    # penetration shielding (projectile entry port, target injection, diagnostics).
    {
        "account": "C220102",
        "value": generic.cas22_detail["C220102"] * 0.15,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "dossier.md §Neutron Management; "
            "prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
        ),
        "rationale": (
            "Library default ($45.2M) prices a dedicated solid radiation shield behind "
            "the blanket. First Light claims neutrons never reach the vessel wall due to "
            "1-meter-thick lithium curtains. No separate shield structure is described. "
            "15% of generic ($6.8M) retained for biological shielding of penetrations "
            "(projectile entry port, target injection, diagnostics) and secondary "
            "radiation paths not covered by the lithium curtain. Zero would under-price "
            "penetration shielding; the full default is structurally inapplicable."
        ),
        "cost_basis": "noak",
    },
    # C220104: Primary pulsed driver — electromagnetic gun at $2/J stored
    {
        "account": "C220104",
        "value": 200.0,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "pmc-articles-pmc7658748.md §2. Model; "
            "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md "
            "§Cost comparisons estimates"
        ),
        "rationale": (
            "Hawker (2020) published Machine 3 driver cost at $1.7/J stored. "
            "IP Group (2025) published FLARE demo at $2/J stored. "
            "Pilot design specifies 100 MJ stored energy (Machine 4 target). "
            "100 MJ x $2/J = $200M. Used $2/J as the more conservative (later, "
            "rep-rated) estimate. This is the electromagnetic gun + capacitor bank "
            "+ power supply cost. Library IFE driver default (heavy-ion accelerator "
            "at $12M/MW) is inapplicable to EM gun."
        ),
        "cost_basis": "noak",
    },
    # C220107: Pulsed-power capacitor bank — zeroed to avoid double-counting
    # with C220104 which already includes the capacitor bank as integral to
    # the electromagnetic launcher.
    {
        "account": "C220107",
        "value": 0.0,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md "
            "§Cost comparisons estimates"
        ),
        "rationale": (
            "The EM gun driver cost ($2/J for 100 MJ = $200M) already includes "
            "the capacitor bank as an integral part of the electromagnetic launcher "
            "system. Unlike laser IFE where the bank charges the laser and the laser "
            "is a separate cost item, here the bank IS the driver's energy store. "
            "Setting to zero avoids double-counting."
        ),
        "cost_basis": "noak",
    },
    # C220108: Target factory — annualized target manufacturing cost
    {
        "account": "C220108",
        "value": 5.6,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "pmc-articles-pmc7658748.md §2. Model; "
            "prnewswire-news-releases-first-light-achieves-world-first.md "
            "§A consumables business model"
        ),
        "rationale": (
            "Hawker (2020) establishes that target cost must be <10% of electricity "
            "revenue for economic viability. At 150 MWe, 85% CF, $50/MWh LCOE target: "
            "Annual revenue = 150,000 x 8760 x 0.85 x $50/1000 = $55.8M. "
            "10% ceiling = $5.58M/year annualized target factory + consumables cost. "
            "At 0.033 Hz x 8760 x 3600 x 0.85 = 0.99M shots/year. "
            "Max target cost = $5.58M / 0.99M = ~$5.6/target. "
            "Value represents annualized target factory cost in $M/year. "
            "Library default (high-rep-rate IFE target factory) is inapplicable at "
            "1M/year volume."
        ),
        "cost_basis": "noak",
    },
    # C220110: Remote handling — no solid in-vessel component replacement.
    # Retain 30% of generic for projectile gun, target injection, lithium loop
    # maintenance, and diagnostic equipment handling.
    {
        "account": "C220110",
        "value": generic.cas22_detail["C220110"] * 0.30,
        "enabled": True,
        "provenance": "derived",
        "source": (
            "dossier.md §Neutron Management; "
            "prnewswire-news-releases-first-light-achieves-world-first.md §A key step"
        ),
        "rationale": (
            "Library default ($33.5M) prices remote handling for periodic blanket and "
            "first-wall replacement. First Light's liquid lithium curtain eliminates "
            "solid in-vessel component replacement ('lifetime-of-plant vessel'). "
            "Remaining RH scope: projectile gun access, target injection systems, "
            "lithium loop maintenance, diagnostic equipment. 30% of generic ($10.1M) "
            "is an analogue estimate — ~70% of conventional RH cost is driven by "
            "blanket/first-wall change-out (tokamak cost studies), leaving ~30% for "
            "other in-vessel and ex-vessel handling needs."
        ),
        "cost_basis": "noak",
    },
    # C220200 (heat transport): structural mismatch acknowledged but not
    # overridable — C220200 is a CAS22.2 sub-rollup (C220201 + C220202).
    # HEAVY_ION archetype default ($38.8M) prices FLiBe molten-salt loop with
    # mechanical pumps. First Light uses liquid lithium with electromagnetic
    # pumps (HYLIFE heritage: 72 m³/s, 50–60% efficiency). The heat transport
    # medium, pump technology, and flow architecture are fundamentally different,
    # but no company-published cost data exists for the lithium EM pump system
    # to derive leaf-level (C220201/C220202) overrides.
    # CAS27: Special materials — initial lithium inventory
    {
        "account": "CAS27",
        "value": 70.0,
        "enabled": True,
        "provenance": "direct",
        "source": (
            "ipgroupplc-news-and-events-portfolio-news-2025-2025-09-19/output.md "
            "§Cost comparisons estimates"
        ),
        "rationale": (
            "IP Group press release directly states 'Natural lithium per reactor: $70M' "
            "in the cost comparison table. This represents the initial lithium inventory "
            "for the reactor chamber. Compares to '$143M-$451M for enriched lithium "
            "alternatives.' First Light uses natural lithium (no enrichment needed due "
            "to TBR 1.8 with natural Li). Library default for special materials does not "
            "account for the large liquid-metal inventory unique to this architecture."
        ),
        "cost_basis": "noak",
    },
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
