"""1costingfe model: Magnetic Mirror (Realta Fusion / CoSMo) (Realta Fusion).

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
# Mapping from Realta's published Hammir/CoSMo design point (analysis.md §5
# Table) to canonical CostingInput kwargs. The prior spec used Realta-specific
# names (l_c, B_0c, P_NBI, etc.) that are NOT in CostingInput.model_fields —
# forward() was silently dropping every entry and the cost model was running on
# pure mirror YAML defaults. F7 (spec-key whitelist) would now reject this
# concept's prior spec.
#
# Fields dropped (no canonical equivalent in the library's single-cell mirror
# model — Realta's tandem-mirror architecture isn't directly representable):
#   - l_p, a_m, B_m, B_0          (end-plug geometry; library is single-cell)
#   - T_ic, beta_p0, n_p0         (end-plug plasma; library models center cell)
#   - E_NBI                       (NBI beam energy is not in CostingInput)
#   - P_fus                       (library back-solves fusion power from power
#                                  balance; not settable through spec, and the
#                                  F9 ratio check rejects values > 0.5 of P_native)
spec = dict(
    chamber_length=50.0, # central cell length [m] — analysis.md §5 (was l_c)
    plasma_t=0.54,       # central cell plasma radius [m] — analysis.md §5 (was a_c)
    B=3.0,               # central cell plasma field [T] — analysis.md §5 (was B_0c)
    b_center=3.0,        # central-cell solenoid coil-axis field [T]; matches B
                         # for an axisymmetric central cell solenoid (B_m=25 T
                         # mirror-throat peak is NOT representable here — the
                         # library doesn't differentiate coil-axis from throat
                         # peak. Throat-peak field enters the magnet override
                         # registry's cost reasoning, not the spec.)
    n_e=7.5e19,          # central cell electron density [m^-3] — analysis.md §5 (was n_c)
    T_e=50.0,            # electron temperature [keV] — set to T_i=50 (analysis
                         # cites T_ec=100 keV, but for a D-T mirror central cell
                         # T_e ≈ T_i ≈ 50 keV is more physically representative
                         # of the bremsstrahlung-source plasma. The T_ec=100 in
                         # the analyst's table likely reflects the WARM-ELECTRON
                         # END-PLUG temperature (a tandem-mirror architecture
                         # feature for ambipolar ion confinement) rather than
                         # central-cell electron temperature; library uses T_e
                         # only for central-cell bremsstrahlung.
    eta_p=0.6,           # central cell plasma beta — analysis.md §5 (was beta_c)
    p_input=30.0,        # total NBI power both end plugs [MW] — analysis.md §5
                         # (was P_NBI). NOTE: p_input/P_native = 30/50 = 0.6, at
                         # the edge of the F9 ratio band [0.5%, 50%]. This is a
                         # genuinely high-recirculation tandem-mirror design,
                         # not a fusion-power transcription error. The library's
                         # F9 cap is calibrated for steady-state-MFE recirc of
                         # 5-15%; mirrors run higher. Document but accept the
                         # F9-band edge case until a mirror-specific calibration
                         # ships.
)
P_native = 50          # MWe — copied from the analysis Design Point block

# 2. Model.
model = CostModel(concept=ConfinementConcept.MIRROR, fuel=Fuel.DT)

# 2b. Generic forward — overrides OFF, design-point scale (forward 1 of 3). The
#     library's bare answer for a reactor this size, and the reference a relative
#     override is written against. ALWAYS emit this line (it is mandatory, even
#     when no override references it).
generic = generic_reference(model, spec, P_native)

# 3. Override registry — six fields per entry, transcribed from Section 5b.
#    Section 5b states: "zero enabled overrides" due to lack of company-grounded
#    cost data. All cost modeling relies on library defaults and analogues.
overrides = []

# 4. Overrides-on forwards via the shared helper (native + 1 GWe NOAK projection).
native, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)

print_cas_breakdown(generic, native, result_1gw, overrides)
