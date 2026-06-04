"""1costingfe model: Laser ICF NIF Commercialization (Focused Energy LIFE-class) (Inertia Enterprises).

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
#    Inertia Enterprises has published minimal quantitative design data beyond
#    high-level architectural claims (see analysis.md §1 "Availability of Data",
#    §5 "Design Point Parameters"). The available sources (website, ENR interview,
#    press release) provide:
#    - Performance targets (1.5 GWe, 10 Hz, 10 MJ laser, 10% wallplug efficiency)
#    - Qualitative descriptions (liquid lithium blanket, DPSSL modular driver)
#    - Ungrounded cost claims ("$700-$1,000/J" laser, "<$1 per target")
#
#    However, none of the quantitative parameters required for CostingInput spec
#    fields are disclosed:
#    - Chamber geometry (radius, wall thickness): NOT ENOUGH DATA
#    - Target gain: Stated as "18× for pilot, >30× for commercial" but these
#      are capsule gain (fusion energy / laser energy), not mapped to spec
#    - Fusion yield per shot: Inferred as ~450 MJ from "4.5× NIF energy", not stated
#    - Thermal conversion details: Only "steam turbines" mentioned, no cycle specs
#
#    The design point table in analysis.md §5 marks most canonical spec keys as
#    "[NOT ENOUGH DATA]" or "[inferred: ...]" with low confidence.
#
#    Per analysis.md §5b "Override Candidates": "zero enabled overrides... reflects
#    the paucity of Inertia-published cost data." The analysis concludes that
#    Inertia's qualitative claims do not translate to accountable, evidence-backed
#    departures from library defaults.
#
#    DECISION: Leave spec empty. The library's LASER_IFE archetype YAML defaults
#    will provide the cost structure. This is the same approach as concept
#    26-laser-icf-indirect-drive (iter-1/model_setup.py lines 42-46: empty spec
#    dict, relying on library defaults).
#
#    Mapping analysis.md §5 table to spec fields (showing why each is omitted):
#    - fusion_power_MW: NOT a spec key (p_fus is back-solved by library)
#    - net_electric_MWe: NOT a spec key (this is P_native, not in spec dict)
#    - p_input_MW: Would be auxiliary heating power for MFE concepts, but LASER_IFE
#      does not accept p_input as a spec field (strict-kwarg validator rejects it;
#      the library models driver power via q_eng + f_rep + eta_pin from YAML, not
#      via a user-overridable p_input). The analysis table line 258 documents
#      ~100 MW laser wallplug but this is informational, not a spec field.
#    - laser_energy_MJ: Informational (drives driver architecture but not a
#      CostingInput field; library uses q_eng and f_rep from YAML)
#    - beamline_count: Informational (modular architecture, not a spec field)
#    - beamline_energy_kJ: Informational (10 kJ per beamline, not a spec field)
#    - laser_efficiency_wallplug: This would be eta_pin, but per Hard Rule 6b
#      footnote "Power-conversion efficiencies are NEVER spec keys" — eta_pin is
#      framework-owned. The library YAML default for LASER_IFE (pulsed_laser_ife.yaml)
#      already has eta_pin = 0.10, matching Inertia's claim, so no override needed.
#    - laser_wavelength_nm: Not a CostingInput field
#    - repetition_rate_Hz: Would be f_rep (rep rate) but this is YAML-defaulted
#      for the archetype; CostingInput does not expose f_rep as a spec override
#    - target_gain_capsule: Not a spec field (gain is computed via q_eng in library)
#    - fusion_yield_per_shot_MJ: Not a spec field
#    - blanket_type: Liquid lithium (analysis §5 line 274) — CostingInput does not
#      have a blanket_config field; this is archetype-determined
#    - thermal_efficiency: Would be eta_th, but per Hard Rule 6 "eta_th, eta_de,
#      eta_dec are ENUM-driven — never in spec"
#    - capacity_factor: NOT a spec key (this is availability, passed by helper)
#    - Chamber geometry: NOT ENOUGH DATA (analysis §5 line 291)
#    - Neutron wall loading: NOT ENOUGH DATA (cannot compute without chamber dims)
#    - First-wall material: NOT ENOUGH DATA (analysis §5 line 293)
#
#    CONCLUSION: No canonical LASER_IFE spec fields can be populated from Inertia's
#    published data. The library's pulsed_laser_ife.yaml defaults already encode
#    a calibrated IFE archetype model. We follow the pattern of concept 26 (empty
#    spec, rely on archetype defaults).
spec = dict(
    # No design-point-specific geometry or physics overrides — Inertia has not
    # disclosed quantitative specs beyond rep rate / laser energy / efficiency
    # (which are YAML-defaulted or not spec-overridable per Hard Rule 3).
)

P_native = 1500  # MWe — analysis.md Design Point block line 28

# 2. Model.
model = CostModel(concept=ConfinementConcept.LASER_IFE, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Analysis.md §5b "Override Candidates" conclusion: "zero enabled overrides...
#    The archetype-fit grade is High, predicting 0–4 overrides; the count of 0
#    falls within band." Rationale (§5b lines 312-353):
#
#    - C220104 (Laser driver): "$700–$1,000/J" figure on website has no provenance
#      (no component breakdown, no learning curve derivation). Cannot be grounded
#      as direct or derived. Disabled override proposed (§5b lines 336-352) pending
#      Inertia cost breakdown publication.
#    - C220108 (Target factory): "<$1 per target" claim is 3 orders of magnitude
#      below NIF target costs but not derived (no cost breakdown for lead hohlraum
#      + cryogenic layering + capsule at mass-production scale). No override proposed.
#    - All other accounts (C220101 blanket, C220102 shield, C220105 structure,
#      C220106 vacuum, C220107 pulsed-power, C220110 remote handling, C220111
#      installation, CAS21 buildings, CAS23 turbine, CAS24 electric plant, CAS26
#      heat rejection, CAS27 special materials, CAS70 O&M, CAS80 fuel): No
#      company-published data.
#
#    The analysis provides one disabled override example for C220104 (laser driver)
#    for future reference if Inertia publishes validation (§5b lines 336-352). That
#    override is NOT included here because enabled: false entries require a
#    blocked_by issue link (Hard Rule 5 footnote on disabled overrides), and the
#    analysis does not cite a tracker issue — it's a "pending validation" note.
#    Per the contract, we transcribe only the Section 5b override registry as-is.
#    Since §5b states "zero enabled overrides" and does not include any disabled
#    entries with blocked_by fields in the final registry, we emit an empty list.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
