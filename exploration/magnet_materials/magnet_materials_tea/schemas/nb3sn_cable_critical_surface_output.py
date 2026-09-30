from pydantic import Field
from simkit.config.schema import MultiOutput

class Nb3Sn_Cable_Critical_SurfaceOutput(MultiOutput):
    """Multi-output container for Nb3Sn_Cable_Critical_Surface.

ITER-form strand critical surface (Tsui & Hampshire 2012 eq. 6-7; Breschi 2017 Table III form with C1 in A*T per whole strand), evaluated at the supplied strand count, turn current, peak field and conductor temperature. eps_sh = Ca2*eps0a/sqrt(Ca1^2 - Ca2^2); s(eps) = 1 + [Ca1(sqrt(eps_sh^2 + eps0a^2) - sqrt((eps - eps_sh)^2 + eps0a^2)) - Ca2*eps]/(1 - Ca1*eps0a); Tc* = Tc0*s^(1/3); t = T/Tc*; Bc2* = Bc20*s*(1 - t^1.52); b = B/Bc2*; Ic_strand = (C1/B)*s*(1 - t^1.52)*(1 - t^2)*b^p*(1 - b)^q for t < 1 and 0 < b < 1, else 0; Ic_cable = n*Ic_strand. T_conductor = T_supply + nuclear_rise. T_cs solves n*Ic_strand(B, T_cs) = I by bisection on [0, T_zero] (b = 1 at T_zero) to 1e-10 K; if n*Ic_strand(B, 0) < I then T_cs = 0 and tcs_defined = 0. Temperature rule margin = T_cs - (T_supply + nuclear_rise + margin_rise); fraction rule margin = fraction_rule - I/Ic_cable; acceptance_rule selects 0 temperature or 1 fraction. status_code: 1 supported (B <= B_design_max), 2 edge (B <= B_edge_max), 3 law-only (B <= B_law_max), 0 unsupported (B outside [B_law_min, B_law_max], T_conductor outside [T_law_min, T_law_max] or eps_intrinsic outside [eps_min, eps_max]). Unsupported evaluations are reported with status 0 and acceptance_pass 0, never as a pass. Strain enters as a fraction. eps_intrinsic_in is the last input so that a design may leave it unbound (usage parameters redefine definition parameters by position); a negative design literal would otherwise generate as a non-overridable constant. Areas: element_area_total = n*(pi/4)*d^2*1e6 mm2; element_copper_area = strand_copper_fraction*element_area_total. **Source**: knowledge/sources/critical_current_scaling_and_the_pivot_point_in_nb3sn/raw.pdf; knowledge/sources/performance_analysis_of_the_toroidal_field_iter_production/raw.pdf **Reference**: Tsui & Hampshire 2012 eq. (6)-(7), printed p.7 (PDF p.8); Breschi et al. 2017 Table III, PDF p.24 (images/tmpniti0z1h.pdf-0024-01.png); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.1; contract section 3. **Basis**: law form directly supported; evaluation at 5.2-6.7 K is temperature interpolation of a fitted law (contract section 2 support wording). The T >= 0 bound: the design's T_cs bracket evaluates Ic at T = 0, so the law is applied on 0 <= t < 1 (see implementation-notes.md). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/nb3sn_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29

SysML Source: root-0/magnet_conductor_alternatives.sysml:5
    """
    temperature_margin: float = Field(description="temperature_margin output")
    element_copper_area: float = Field(description="element_copper_area output")
    acceptance_pass: float = Field(description="acceptance_pass output")
    T_cs: float = Field(description="T_cs output")
    acceptance_margin: float = Field(description="acceptance_margin output")
    status_code: float = Field(description="status_code output")
    temp_rule_margin: float = Field(description="temp_rule_margin output")
    fraction_rule_margin: float = Field(description="fraction_rule_margin output")
    supported: float = Field(description="supported output")
    ic_cable_op: float = Field(description="ic_cable_op output")
    operating_fraction: float = Field(description="operating_fraction output")
    tcs_defined: float = Field(description="tcs_defined output")
    ic_strand_op: float = Field(description="ic_strand_op output")
    T_conductor: float = Field(description="T_conductor output")
    element_area_total: float = Field(description="element_area_total output")
