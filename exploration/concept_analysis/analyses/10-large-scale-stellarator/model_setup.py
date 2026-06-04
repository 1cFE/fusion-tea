"""1costingfe model: Large-Scale Stellarator (Gauss Fusion).

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
    R0=18.0,             # gauss-fusion-technical-summary.md §GIGA Power Plant; helias-reactor-context.md Table I
    plasma_t=1.7,        # minor radius [m] — gauss-fusion-technical-summary.md §GIGA Power Plant
    plasma_volume=1500.0,# gauss-fusion-technical-summary.md §GIGA Power Plant (m³)
    B=6.0,               # on-axis magnetic field [T] — gauss-fusion-technical-summary.md §GIGA Power Plant
    p_input=75.0,        # [estimated: ECRH for startup/profile control; 50-100 MW band from analysis §5]
    elon=1.6,            # [effective average elongation for toroidally-varying bean/triangular cross-sections]
    # Note: p_fus dropped from spec — library back-solves P_fus via inverse power
    # balance from p_input + P_native. Source p_fus=3000 MW would have been
    # silently ignored by forward() under loose validation and now raises with
    # the strict kwarg validator (1costingfe master).
)
P_native = 1000.0        # MWe — Design Point selection (orchestrator-fixed)

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 0.60 * generic.costs.cas21, "enabled": False,
     "cost_basis": "noak", "provenance": "derived", "source": "helias-reactor-context.md §8",
     "rationale": "HELIAS HSR4/18 study claims 'costs of the magnet system certainly far below those of an ITER-type tokamak reactor' due to NbTi at 1.8 K with 400 km total length and 700 t weight. However, this is invalidated for GIGA: (a) 12-13 T peak field requires Nb3Sn or HTS, not NbTi; (b) demountable joints add cost (~250 per coil × 40 coils); (c) 35,000 t total coil system mass vs HELIAS 4,100 t coils + 10,000 t supports suggests GIGA is larger/heavier. Enabled=false because the HELIAS cost claim does not apply to GIGA's higher-field demountable design. If future data confirms cost parity or advantage vs tokamaks despite these changes, re-enable with updated derivation. The 0.60 factor is the HSR4/18 claim that stellarator coils cost 60% of ITER-class tokamak coils for same plasma volume.",
     "blocked_by": "1cFE/1costingfe#100"},

    {"account": "C220108", "value": 0.0, "enabled": False,
     "cost_basis": "noak", "provenance": "derived", "source": "helias-reactor-context.md §7; gauss-fusion-technical-summary.md",
     "rationale": "Stellarators do not have a separable divertor in the tokamak sense — the island divertor concept (W7-X) integrates heat exhaust into the last closed flux surface geometry. HELIAS studies flag divertor heat flux >10 MW/m² as 'a critical issue,' but no discrete divertor component or cost estimate exists. GIGA's divertor architecture is not disclosed. Enabled=false because (a) uncertainty whether GIGA uses island divertor, discrete divertor target plates, or another concept; (b) heat exhaust may be embedded in first-wall/blanket cost (C220101) rather than separate CAS account. If future data shows a tokamak-like discrete divertor with cost estimate, re-enable with that value. The zero value reflects 'no separable divertor component' not 'divertor is free.'",
     "blocked_by": "1cFE/1costingfe#101"},

    {"account": "CAS70", "value": 1.15 * generic.costs.cas70, "enabled": False,
     "cost_basis": "noak", "provenance": "derived", "source": "helias-reactor-context.md §8; helias-blanket-studies.md",
     "rationale": "Stellarator blanket has 'large number of different blanket segments' vs tokamak's 2 shapes (inboard/outboard). Maintenance via 32 portholes (8 per field period, 2×6 m² each) vs tokamak's fewer, larger ports. Remote handling for 3D geometry is more complex. However, stellarator avoids disruptions (no sudden mechanical loading on PFCs), and HELIAS studies claim 9-year blanket life vs DEMO tokamak's 2.3 years — longer component life reduces replacement frequency. The 1.15 factor assumes geometric complexity adds 15% to maintenance labor, but this is speculative. Enabled=false because (a) no Gauss Fusion O&M estimate exists; (b) complexity penalty vs component lifetime benefit may cancel; (c) disruption avoidance may reduce unplanned maintenance. If CDR provides O&M cost estimate or detailed maintenance schedule, re-enable with that data.",
     "blocked_by": "1cFE/1costingfe#102"},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
