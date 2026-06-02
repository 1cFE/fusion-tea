"""1costingfe model: Planar-Coil Stellarator (Thea Energy).

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
    R0=8.0,              # major radius [m] — arxiv Table 1
    B=6.0,               # on-axis magnetic field [T] — arxiv Table 1
    elon=1.0,            # elongation — stellarators are typically ~1
    plasma_volume=418.0, # plasma volume [m³] — arxiv Table 1
    eta_p=0.027,         # plasma beta — arxiv Table 1 (2.7%)
    f_rad=1.4,           # ISS04 confinement factor — arxiv Table 1, §3.5
    p_input=958.0,       # fusion power [MW] — arxiv Table 1
)
P_native = 390.0       # MWe — copied from the analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.STELLARATOR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
overrides = [
    {"account": "C220103", "value": 0.70 * generic.cas22_detail["C220103"], "enabled": True,
     "cost_basis": "noak",
     "provenance": "derived", "source": "thea-energy-helios-arxiv-2512-08027.md §1, §3.6; thea-energy-canis-prototype-arxiv-2503-18960.md §I, §III",
     "rationale": "The library default for C220103 (confinement magnets) is computed from HTS conductor mass, "
                  "winding complexity, and structural requirements appropriate for conventional 3D stellarator "
                  "coils or tokamak TF coils. Helios uses 336 planar HTS coils (12 encircling + 324 shaping) "
                  "instead of complex modular 3D coils. The cost advantage derives from: "
                  "(1) Planar geometry: 'all coils are planar and convex, and can be wound in tension' (arxiv "
                  "§3.6) versus ARIES-CS 3D coils that 'were extremely difficult and expensive to manufacture' "
                  "and 'envisioned to be 3D printed on-site, as it was too big to transport' (Canis §I). "
                  "(2) Relaxed tolerances: 'tolerances are significantly relaxed as manufacturing and assembly "
                  "errors can be corrected during operation by the device's control system' (arxiv §1) versus "
                  "tight geometric tolerances on 3D shapes. "
                  "(3) Demonstrated manufacturing speed: Canis prototype achieved ≤1 day double-pancake takt "
                  "time (Canis §III), validating mass manufacturing feasibility. "
                  "The tradeoff is 324 shaping coils (versus ~20-50 modular coils in conventional stellarators), "
                  "increasing coil count but reducing per-coil cost. The net effect is estimated as 30% cost "
                  "reduction (0.70 multiplier) relative to library default for 3D stellarator coils. This is "
                  "conservative given NCSX cancellation due to modular coil complexity; actual savings may be "
                  "higher but unquantified without vendor quotes. "
                  "The override is relative (0.70 * generic.cas22_detail['C220103']) because the absolute coil cost "
                  "depends on conductor quantity, operating field, and structural requirements that the library "
                  "computes correctly; only the winding/fabrication complexity factor changes."},

    {"account": "C220104", "value": 2.5, "enabled": True,
     "cost_basis": "noak",
     "provenance": "direct", "source": "thea-energy-helios-arxiv-2512-08027.md §3.3, §4.4, Table 1",
     "rationale": "The library default for C220104 (supplementary plasma heating) scales with installed heating "
                  "power in MW. Helios requires only 2.5 MW operational ECRH budget (1 MW for impurity control "
                  "during ignition + overhead) per arxiv §4.4, dramatically lower than typical stellarators due "
                  "to ignited operation where alpha heating dominates. "
                  "Direct quote: 'Of the gross electric power, 48 MW are required to maintain the facility in "
                  "power producing state' (§4.4), which includes 2.5 MW ECRH plus tritium separation, cryogenics, "
                  "and other auxiliaries. The ECRH system uses '10 MW of electron cyclotron resonance heating "
                  "power' at 170 GHz for startup (§3.3, Table 1), but operational requirement is only 1 MW. "
                  "The value 2.5 MW is company-grounded (stated operational budget) and represents installed "
                  "capacity for steady-state impurity control, not the 10 MW startup transient. The library's "
                  "$/MW_heating cost function should be applied to this operational value, not the startup peak."},
]

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
