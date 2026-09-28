"""Bounded normative model and typed completion edits authorized at eb341aee."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
p=ROOT/'models/library/analyses/mfe_magnet_field.sysml';s=p.read_text()
s=s.replace('quadratic in coil current once B_peak follows the derived field --','quadratic at fixed side once B_peak follows the derived field --')
s=s.replace('        out attribute sigma_wp : Real = k_sigma * I_coil * B_peak_in / wp_side;', '''        // Normative domain: wp_side must be nonzero (WI-055).
        // Native typed manual completion raises ValueError before division.
        // Valid ordered equation: k_sigma * I_coil * B_peak_in / wp_side.
        out attribute sigma_wp : Real;''')
s=s.replace('        Force density (current x field)', '''        Domain: wp_side != 0. Native typed manual completion raises
        ValueError for a zero denominator before evaluating the stated equation.
        A locally zero-sized pack has no defined stress in this expression.

        Force density (current x field)''')
s=s.replace('        sigma_wp = k_sigma * B_peak * sqrt(I_coil * j_wp), so winding stress\n        grows as the square root of coil current rather than linearly once\n        the pack is allowed to size itself.', '''        sigma_wp = 1000 * k_sigma * B_peak * sqrt(I_coil * j_wp).
        At fixed peak field and density, stress grows as sqrt(I_coil).
        When peak field follows current at fixed geometry, it grows as
        I_coil^(3/2) at fixed density. The factor 1000 follows the side's
        millimetre-to-metre conversion; it is not a calibration coefficient.

        Domain: I_coil and j_wp are finite magnitudes, with I_coil >= 0
        and j_wp > 0. Native typed manual completion raises ValueError
        before evaluating the sizing equation for an invalid domain (WI-055).
        I_coil = 0 gives local side = 0, not a de-energized finite coil model.
        The composed stress and plasma equations enforce their own nonzero
        denominators. Source coil values are examples, not universal bounds.''')
s=s.replace('        out attribute wp_side : Real = (I_coil / j_wp) ** 0.5 / 1000.0;', '''        // Native manual completion enforces the documented finite magnitude
        // domain before unchanged (I_coil / j_wp) ** 0.5 / 1000.0 arithmetic.
        out attribute wp_side : Real;''')
p.write_text(s)
p=ROOT/'models/library/analyses/mfe_plasma_sustainment.sysml';s=p.read_text().replace('        DORMANT (no-ash) CASE', '''        ZERO-FIELD DOMAIN (WI-055): B_in must be nonzero. The composed
        Albajar relation uses p_a0 = 6.04e3*a*n_e0_20/B; the confinement
        chain also divides W_th by tau_E, which is zero at B = 0.
        Native manual completion raises SustainmentError before the chain
        when B_in = 0. This local mathematical precondition is separate
        from an engineering field limit and leaves standalone axis-field
        and winding-sizing zero behavior unchanged.

        DORMANT (no-ash) CASE''');p.write_text(s)
for name in ('mfe_magnet_field.sysml','mfe_plasma_sustainment.sysml'):
 (ROOT/'exploration/stellarator_e2e/models/analyses'/name).write_bytes((ROOT/'models/library/analyses'/name).read_bytes())
p=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_magnet_field/winding_pack_sizing_impl.py'
p.write_text('''"""WI-055 typed completion of the canonical finite winding-magnitude contract."""
import math
from stellarator_tea.modules.mfe_magnet_field.winding_pack_sizing import Winding_Pack_SizingInput

AUTO_IMPLEMENTED = False


def run_winding_pack_sizing(inputs: Winding_Pack_SizingInput) -> float:
    """Size finite nonnegative amp-turn magnitude at finite positive A/mm²."""
    if not math.isfinite(inputs.I_coil) or inputs.I_coil < 0:
        raise ValueError("Winding Pack Sizing: I_coil must be finite and nonnegative")
    if not math.isfinite(inputs.j_wp) or inputs.j_wp <= 0:
        raise ValueError("Winding Pack Sizing: j_wp must be finite and positive")
    return (((inputs.I_coil / inputs.j_wp) ** 0.5) / 1000.0)
''')
p=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_magnet_field/winding_pack_stress_impl.py'
p.write_text('''"""WI-055 typed completion of the canonical nonzero stress-side contract."""
from stellarator_tea.modules.mfe_magnet_field.winding_pack_stress import Winding_Pack_StressInput

AUTO_IMPLEMENTED = False


def run_winding_pack_stress(inputs: Winding_Pack_StressInput) -> float:
    """Evaluate the unchanged mean-stress equation on a nonzero side."""
    if inputs.wp_side == 0:
        raise ValueError("Winding Pack Stress: wp_side must be nonzero")
    return (((inputs.k_sigma * inputs.I_coil) * inputs.B_peak_in) / inputs.wp_side)
''')
p=ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py';s=p.read_text();old='    n_e0 = inputs.n_e0_in\n';assert s.count(old)==1;s=s.replace(old,'''    # WI-055: the composed synchrotron and confinement equations divide by
    # field and confinement time; zero field is outside this local domain.
    if inputs.B_in == 0:
        raise SustainmentError(
            "Plasma Sustainment: B_in must be nonzero for synchrotron and confinement equations")
    n_e0 = inputs.n_e0_in
''');p.write_text(s)
print('Updated two canonical calculations, sustainment contract, twins and three completion bodies')
