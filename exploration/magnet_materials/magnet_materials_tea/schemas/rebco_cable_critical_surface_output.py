from pydantic import Field
from simkit.config.schema import MultiOutput

class REBCO_Cable_Critical_SurfaceOutput(MultiOutput):
    """Multi-output container for REBCO_Cable_Critical_Surface.

REBCO tape critical current at the supplied tape count, turn current, peak field and conductor temperature. Field shape g(B): shape_mode 0 interpolates log-log between the measured 20 K, B||c knots g8, g10, g12, g15, g20 at 8, 10, 12, 15, 20 T (defined only on [8, 20] T; NaN outside, since no knot interval exists there); shape_mode 1 is the power law (B/20)^-alpha. Ic_tape(B, T) = anchor_ic*g(B)*exp(-(T - 20)/T_star); Ic_cable = n*degradation*Ic_tape; T_cs = 20 + T_star*ln(n*degradation*anchor_ic*g(B)/I) (closed form). Rule margins, acceptance selection and area outputs as in 'Nb3Sn Cable Critical Surface'; element_area_total = n*w*t*1e6 mm2 and element_copper_area = tape_copper_fraction*element_area_total. status_code 1 when B lies in the active shape's supported range ([B_knot_min, B_knot_max] for shape 0, [B_law_min, B_law_max] for shape 1) and T_conductor lies in [T_law_min, T_law_max]; otherwise 0 (unsupported). REBCO has no edge or law-only band. **Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf; knowledge/sources/field_and_temperature_scaling_of_the_critical_current/raw.pdf **Reference**: Molodyk et al. 2021 Fig. 1a (raw.pdf p.3), output.md:77, :93, :137; Senatore et al. 2016 eq. (1), raw.pdf p.6, validity output.md:94; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.2; contract section 3. **Basis**: measured 20 K shape digitized twice (check-rebco-cryo-cost.md section 1); Senatore exponential temperature form; field perpendicular to the tape face assumed everywhere. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/rebco_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29

SysML Source: root-0/magnet_conductor_alternatives.sysml:51
    """
    acceptance_margin: float = Field(description="acceptance_margin output")
    acceptance_pass: float = Field(description="acceptance_pass output")
    tcs_defined: float = Field(description="tcs_defined output")
    status_code: float = Field(description="status_code output")
    ic_tape_op: float = Field(description="ic_tape_op output")
    temperature_margin: float = Field(description="temperature_margin output")
    operating_fraction: float = Field(description="operating_fraction output")
    element_area_total: float = Field(description="element_area_total output")
    T_conductor: float = Field(description="T_conductor output")
    ic_cable_op: float = Field(description="ic_cable_op output")
    element_copper_area: float = Field(description="element_copper_area output")
    fraction_rule_margin: float = Field(description="fraction_rule_margin output")
    supported: float = Field(description="supported output")
    T_cs: float = Field(description="T_cs output")
    temp_rule_margin: float = Field(description="temp_rule_margin output")
