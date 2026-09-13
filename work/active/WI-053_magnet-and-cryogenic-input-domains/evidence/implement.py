"""Apply the two bounded normative model/manual-completion corrections."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
field=ROOT/'models/library/analyses/mfe_plasma_scaling.sysml'
s=field.read_text()
s=s.replace('the factors are\n        intermediate attributes so the executed arithmetic is exactly', 'the manual completion evaluates factors in the documented order\n        so the executed arithmetic is exactly')
s=s.replace('        // eq.-39 bore factor at the operating geometry and at the reference\n        attribute bore_factor : Real = R_in / (R_in - a_coil_in);\n        attribute bore_factor_ref : Real = R_ref_in / (R_ref_in - a_coil_ref_in);\n        // normalised bore factor [1]: exactly 1.0 at the reference geometry\n        attribute bore_norm : Real = bore_factor / bore_factor_ref;\n\n        // peak field on the conductor [T]\n        out attribute B_peak : Real = B_axis_in * peak_ratio_in * bore_norm;', '''        // Normative domain: both clearances must be strictly positive.
        // Native typed manual completion rejects invalid input with ValueError
        // before evaluating either bore factor. This is an input precondition,
        // separate from the downstream evaluated conductor-field limit.
        // Valid equations and operation order are documented above (WI-053).
        out attribute B_peak : Real;''')
s=s.replace('        **Basis**: peak-on-winding', '''        Domain: R_in - a_coil_in > 0 and R_ref_in - a_coil_ref_in > 0.
        Native manual completion enforces both before any bore arithmetic.
        An invalid domain raises ValueError; a valid computed field remains a
        signed diagnostic evaluated separately by the conductor-field limit.

        **Basis**: peak-on-winding''')
field.write_text(s)
cryo=ROOT/'models/library/analyses/mfe_cryo_plant.sysml'
s=cryo.read_text().replace('        **Basis**: reversed-Carnot', '''        Domain: 0 < T_cold < T_amb. Native typed manual completion raises
        ValueError before any COP arithmetic when the temperature ordering
        fails. Valid default temperatures retain dormant/direct-power behavior.

        **Basis**: reversed-Carnot''')
s=s.replace('        attribute p_cold : Real = (q_nuc * vol_cold * 1.0e-6 + p_fixed) * f_uplift;\n        attribute cop_carnot : Real = T_cold / (T_amb - T_cold);\n        attribute cop : Real = f_carnot * cop_carnot;\n\n        out attribute p_elec : Real = p_cold / cop + p_direct;', '''        // Native manual completion enforces the documented temperature domain
        // before evaluating the unchanged refrigeration equations (WI-053).
        out attribute p_elec : Real;''')
cryo.write_text(s)
for p in (field,cryo):
    (ROOT/'exploration/stellarator_e2e/models/analyses'/p.name).write_bytes(p.read_bytes())
