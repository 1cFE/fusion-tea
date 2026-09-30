"""Nb3Sn_Cable_Critical_SurfaceModule Module Wrapper

TEAx module for Nb3Sn_Cable_Critical_Surface calculation.

ITER-form strand critical surface (Tsui & Hampshire 2012 eq. 6-7; Breschi 2017 Table III form with C1 in A*T per whole strand), evaluated at the supplied strand count, turn current, peak field and conductor temperature. eps_sh = Ca2*eps0a/sqrt(Ca1^2 - Ca2^2); s(eps) = 1 + [Ca1(sqrt(eps_sh^2 + eps0a^2) - sqrt((eps - eps_sh)^2 + eps0a^2)) - Ca2*eps]/(1 - Ca1*eps0a); Tc* = Tc0*s^(1/3); t = T/Tc*; Bc2* = Bc20*s*(1 - t^1.52); b = B/Bc2*; Ic_strand = (C1/B)*s*(1 - t^1.52)*(1 - t^2)*b^p*(1 - b)^q for t < 1 and 0 < b < 1, else 0; Ic_cable = n*Ic_strand. T_conductor = T_supply + nuclear_rise. T_cs solves n*Ic_strand(B, T_cs) = I by bisection on [0, T_zero] (b = 1 at T_zero) to 1e-10 K; if n*Ic_strand(B, 0) < I then T_cs = 0 and tcs_defined = 0. Temperature rule margin = T_cs - (T_supply + nuclear_rise + margin_rise); fraction rule margin = fraction_rule - I/Ic_cable; acceptance_rule selects 0 temperature or 1 fraction. status_code: 1 supported (B <= B_design_max), 2 edge (B <= B_edge_max), 3 law-only (B <= B_law_max), 0 unsupported (B outside [B_law_min, B_law_max], T_conductor outside [T_law_min, T_law_max] or eps_intrinsic outside [eps_min, eps_max]). Unsupported evaluations are reported with status 0 and acceptance_pass 0, never as a pass. Strain enters as a fraction. eps_intrinsic_in is the last input so that a design may leave it unbound (usage parameters redefine definition parameters by position); a negative design literal would otherwise generate as a non-overridable constant. Areas: element_area_total = n*(pi/4)*d^2*1e6 mm2; element_copper_area = strand_copper_fraction*element_area_total. **Source**: knowledge/sources/critical_current_scaling_and_the_pivot_point_in_nb3sn/raw.pdf; knowledge/sources/performance_analysis_of_the_toroidal_field_iter_production/raw.pdf **Reference**: Tsui & Hampshire 2012 eq. (6)-(7), printed p.7 (PDF p.8); Breschi et al. 2017 Table III, PDF p.24 (images/tmpniti0z1h.pdf-0024-01.png); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.1; contract section 3. **Basis**: law form directly supported; evaluation at 5.2-6.7 K is temperature interpolation of a fitted law (contract section 2 support wording). The T >= 0 bound: the design's T_cs bracket evaluates Ic at T = 0, so the law is applied on 0 <= t < 1 (see implementation-notes.md). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/nb3sn_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - B_design_max_in: B_design_max_in parameter
    - B_edge_max_in: B_edge_max_in parameter
    - C1_in: C1_in parameter
    - T_supply_in: T_supply_in parameter
    - n_strands_in: n_strands_in parameter
    - T_law_min_in: T_law_min_in parameter
    - Ca1_in: Ca1_in parameter
    - B_peak_in: B_peak_in parameter
    - eps_max_in: eps_max_in parameter
    - nuclear_rise_in: nuclear_rise_in parameter
    - turn_current_in: turn_current_in parameter
    - acceptance_rule_in: acceptance_rule_in parameter
    - margin_rise_in: margin_rise_in parameter
    - strand_diameter_in: strand_diameter_in parameter
    - Tc0_in: Tc0_in parameter
    - strand_copper_fraction_in: strand_copper_fraction_in parameter
    - eps_min_in: eps_min_in parameter
    - Ca2_in: Ca2_in parameter
    - B_law_max_in: B_law_max_in parameter
    - eps_intrinsic_in: eps_intrinsic_in parameter
    - Bc20_in: Bc20_in parameter
    - B_law_min_in: B_law_min_in parameter
    - q_in: q_in parameter
    - p_in: p_in parameter
    - fraction_rule_in: fraction_rule_in parameter
    - T_law_max_in: T_law_max_in parameter
    - eps0a_in: eps0a_in parameter

Outputs:
    - temperature_margin: temperature_margin result
    - element_copper_area: element_copper_area result
    - acceptance_pass: acceptance_pass result
    - T_cs: T_cs result
    - acceptance_margin: acceptance_margin result
    - status_code: status_code result
    - temp_rule_margin: temp_rule_margin result
    - fraction_rule_margin: fraction_rule_margin result
    - supported: supported result
    - ic_cable_op: ic_cable_op result
    - operating_fraction: operating_fraction result
    - tcs_defined: tcs_defined result
    - ic_strand_op: ic_strand_op result
    - T_conductor: T_conductor result
    - element_area_total: element_area_total result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:5

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:5

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_conductor_alternatives/nb3sn_cable_critical_surface_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.nb3sn_cable_critical_surface_output import Nb3Sn_Cable_Critical_SurfaceOutput


class Nb3Sn_Cable_Critical_SurfaceInput(BaseModel):
    """Input model for Nb3Sn_Cable_Critical_SurfaceModule.

    Attributes:
        B_design_max_in: B_design_max_in input
        B_edge_max_in: B_edge_max_in input
        C1_in: C1_in input
        T_supply_in: T_supply_in input
        n_strands_in: n_strands_in input
        T_law_min_in: T_law_min_in input
        Ca1_in: Ca1_in input
        B_peak_in: B_peak_in input
        eps_max_in: eps_max_in input
        nuclear_rise_in: nuclear_rise_in input
        turn_current_in: turn_current_in input
        acceptance_rule_in: acceptance_rule_in input
        margin_rise_in: margin_rise_in input
        strand_diameter_in: strand_diameter_in input
        Tc0_in: Tc0_in input
        strand_copper_fraction_in: strand_copper_fraction_in input
        eps_min_in: eps_min_in input
        Ca2_in: Ca2_in input
        B_law_max_in: B_law_max_in input
        eps_intrinsic_in: eps_intrinsic_in input
        Bc20_in: Bc20_in input
        B_law_min_in: B_law_min_in input
        q_in: q_in input
        p_in: p_in input
        fraction_rule_in: fraction_rule_in input
        T_law_max_in: T_law_max_in input
        eps0a_in: eps0a_in input
    """
    B_design_max_in: float = Field(..., description="B_design_max_in input")
    B_edge_max_in: float = Field(..., description="B_edge_max_in input")
    C1_in: float = Field(..., description="C1_in input")
    T_supply_in: float = Field(..., description="T_supply_in input")
    n_strands_in: float = Field(..., description="n_strands_in input")
    T_law_min_in: float = Field(..., description="T_law_min_in input")
    Ca1_in: float = Field(..., description="Ca1_in input")
    B_peak_in: float = Field(..., description="B_peak_in input")
    eps_max_in: float = Field(..., description="eps_max_in input")
    nuclear_rise_in: float = Field(..., description="nuclear_rise_in input")
    turn_current_in: float = Field(..., description="turn_current_in input")
    acceptance_rule_in: float = Field(..., description="acceptance_rule_in input")
    margin_rise_in: float = Field(..., description="margin_rise_in input")
    strand_diameter_in: float = Field(..., description="strand_diameter_in input")
    Tc0_in: float = Field(..., description="Tc0_in input")
    strand_copper_fraction_in: float = Field(..., description="strand_copper_fraction_in input")
    eps_min_in: float = Field(..., description="eps_min_in input")
    Ca2_in: float = Field(..., description="Ca2_in input")
    B_law_max_in: float = Field(..., description="B_law_max_in input")
    eps_intrinsic_in: float = Field(..., description="eps_intrinsic_in input")
    Bc20_in: float = Field(..., description="Bc20_in input")
    B_law_min_in: float = Field(..., description="B_law_min_in input")
    q_in: float = Field(..., description="q_in input")
    p_in: float = Field(..., description="p_in input")
    fraction_rule_in: float = Field(..., description="fraction_rule_in input")
    T_law_max_in: float = Field(..., description="T_law_max_in input")
    eps0a_in: float = Field(..., description="eps0a_in input")


class Nb3Sn_Cable_Critical_SurfaceModule(ModuleBase[Nb3Sn_Cable_Critical_SurfaceInput, Nb3Sn_Cable_Critical_SurfaceOutput]):
    """TEAx module for Nb3Sn_Cable_Critical_Surface calculation.

ITER-form strand critical surface (Tsui & Hampshire 2012 eq. 6-7; Breschi 2017 Table III form with C1 in A*T per whole strand), evaluated at the supplied strand count, turn current, peak field and conductor temperature. eps_sh = Ca2*eps0a/sqrt(Ca1^2 - Ca2^2); s(eps) = 1 + [Ca1(sqrt(eps_sh^2 + eps0a^2) - sqrt((eps - eps_sh)^2 + eps0a^2)) - Ca2*eps]/(1 - Ca1*eps0a); Tc* = Tc0*s^(1/3); t = T/Tc*; Bc2* = Bc20*s*(1 - t^1.52); b = B/Bc2*; Ic_strand = (C1/B)*s*(1 - t^1.52)*(1 - t^2)*b^p*(1 - b)^q for t < 1 and 0 < b < 1, else 0; Ic_cable = n*Ic_strand. T_conductor = T_supply + nuclear_rise. T_cs solves n*Ic_strand(B, T_cs) = I by bisection on [0, T_zero] (b = 1 at T_zero) to 1e-10 K; if n*Ic_strand(B, 0) < I then T_cs = 0 and tcs_defined = 0. Temperature rule margin = T_cs - (T_supply + nuclear_rise + margin_rise); fraction rule margin = fraction_rule - I/Ic_cable; acceptance_rule selects 0 temperature or 1 fraction. status_code: 1 supported (B <= B_design_max), 2 edge (B <= B_edge_max), 3 law-only (B <= B_law_max), 0 unsupported (B outside [B_law_min, B_law_max], T_conductor outside [T_law_min, T_law_max] or eps_intrinsic outside [eps_min, eps_max]). Unsupported evaluations are reported with status 0 and acceptance_pass 0, never as a pass. Strain enters as a fraction. eps_intrinsic_in is the last input so that a design may leave it unbound (usage parameters redefine definition parameters by position); a negative design literal would otherwise generate as a non-overridable constant. Areas: element_area_total = n*(pi/4)*d^2*1e6 mm2; element_copper_area = strand_copper_fraction*element_area_total. **Source**: knowledge/sources/critical_current_scaling_and_the_pivot_point_in_nb3sn/raw.pdf; knowledge/sources/performance_analysis_of_the_toroidal_field_iter_production/raw.pdf **Reference**: Tsui & Hampshire 2012 eq. (6)-(7), printed p.7 (PDF p.8); Breschi et al. 2017 Table III, PDF p.24 (images/tmpniti0z1h.pdf-0024-01.png); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.1; contract section 3. **Basis**: law form directly supported; evaluation at 5.2-6.7 K is temperature interpolation of a fitted law (contract section 2 support wording). The T >= 0 bound: the design's T_cs bracket evaluates Ic at T = 0, so the law is applied on 0 <= t < 1 (see implementation-notes.md). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/nb3sn_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - B_design_max_in: B_design_max_in parameter
    - B_edge_max_in: B_edge_max_in parameter
    - C1_in: C1_in parameter
    - T_supply_in: T_supply_in parameter
    - n_strands_in: n_strands_in parameter
    - T_law_min_in: T_law_min_in parameter
    - Ca1_in: Ca1_in parameter
    - B_peak_in: B_peak_in parameter
    - eps_max_in: eps_max_in parameter
    - nuclear_rise_in: nuclear_rise_in parameter
    - turn_current_in: turn_current_in parameter
    - acceptance_rule_in: acceptance_rule_in parameter
    - margin_rise_in: margin_rise_in parameter
    - strand_diameter_in: strand_diameter_in parameter
    - Tc0_in: Tc0_in parameter
    - strand_copper_fraction_in: strand_copper_fraction_in parameter
    - eps_min_in: eps_min_in parameter
    - Ca2_in: Ca2_in parameter
    - B_law_max_in: B_law_max_in parameter
    - eps_intrinsic_in: eps_intrinsic_in parameter
    - Bc20_in: Bc20_in parameter
    - B_law_min_in: B_law_min_in parameter
    - q_in: q_in parameter
    - p_in: p_in parameter
    - fraction_rule_in: fraction_rule_in parameter
    - T_law_max_in: T_law_max_in parameter
    - eps0a_in: eps0a_in parameter

Outputs:
    - temperature_margin: temperature_margin result
    - element_copper_area: element_copper_area result
    - acceptance_pass: acceptance_pass result
    - T_cs: T_cs result
    - acceptance_margin: acceptance_margin result
    - status_code: status_code result
    - temp_rule_margin: temp_rule_margin result
    - fraction_rule_margin: fraction_rule_margin result
    - supported: supported result
    - ic_cable_op: ic_cable_op result
    - operating_fraction: operating_fraction result
    - tcs_defined: tcs_defined result
    - ic_strand_op: ic_strand_op result
    - T_conductor: T_conductor result
    - element_area_total: element_area_total result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:5

    SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:5

    Calculation Specification:
        n_strands_in = 0.0
        strand_diameter_in = 0.0
        strand_copper_fraction_in = 0.0
        turn_current_in = 0.0
        B_peak_in = 0.0
        T_supply_in = 0.0
        nuclear_rise_in = 0.0
        margin_rise_in = 0.0
        p_in = 0.0
        q_in = 0.0
        C1_in = 0.0
        Ca1_in = 0.0
        Ca2_in = 0.0
        eps0a_in = 0.0
        Bc20_in = 0.0
        Tc0_in = 0.0
        fraction_rule_in = 0.0
        acceptance_rule_in = 0.0
        B_law_min_in = 0.0
        B_law_max_in = 0.0
        B_design_max_in = 0.0
        B_edge_max_in = 0.0
        T_law_min_in = 0.0
        T_law_max_in = 0.0
        eps_min_in = 0.0
        eps_max_in = 0.0
        eps_intrinsic_in = 0.0
        
Documentation:
ITER-form strand critical surface (Tsui & Hampshire 2012 eq. 6-7; Breschi 2017 Table III form with C1 in A*T per whole strand), evaluated at the supplied strand count, turn current, peak field and conductor temperature. eps_sh = Ca2*eps0a/sqrt(Ca1^2 - Ca2^2); s(eps) = 1 + [Ca1(sqrt(eps_sh^2 + eps0a^2) - sqrt((eps - eps_sh)^2 + eps0a^2)) - Ca2*eps]/(1 - Ca1*eps0a); Tc* = Tc0*s^(1/3); t = T/Tc*; Bc2* = Bc20*s*(1 - t^1.52); b = B/Bc2*; Ic_strand = (C1/B)*s*(1 - t^1.52)*(1 - t^2)*b^p*(1 - b)^q for t < 1 and 0 < b < 1, else 0; Ic_cable = n*Ic_strand. T_conductor = T_supply + nuclear_rise. T_cs solves n*Ic_strand(B, T_cs) = I by bisection on [0, T_zero] (b = 1 at T_zero) to 1e-10 K; if n*Ic_strand(B, 0) < I then T_cs = 0 and tcs_defined = 0. Temperature rule margin = T_cs - (T_supply + nuclear_rise + margin_rise); fraction rule margin = fraction_rule - I/Ic_cable; acceptance_rule selects 0 temperature or 1 fraction. status_code: 1 supported (B <= B_design_max), 2 edge (B <= B_edge_max), 3 law-only (B <= B_law_max), 0 unsupported (B outside [B_law_min, B_law_max], T_conductor outside [T_law_min, T_law_max] or eps_intrinsic outside [eps_min, eps_max]). Unsupported evaluations are reported with status 0 and acceptance_pass 0, never as a pass. Strain enters as a fraction. eps_intrinsic_in is the last input so that a design may leave it unbound (usage parameters redefine definition parameters by position); a negative design literal would otherwise generate as a non-overridable constant. Areas: element_area_total = n*(pi/4)*d^2*1e6 mm2; element_copper_area = strand_copper_fraction*element_area_total. **Source**: knowledge/sources/critical_current_scaling_and_the_pivot_point_in_nb3sn/raw.pdf; knowledge/sources/performance_analysis_of_the_toroidal_field_iter_production/raw.pdf **Reference**: Tsui & Hampshire 2012 eq. (6)-(7), printed p.7 (PDF p.8); Breschi et al. 2017 Table III, PDF p.24 (images/tmpniti0z1h.pdf-0024-01.png); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.1; contract section 3. **Basis**: law form directly supported; evaluation at 5.2-6.7 K is temperature interpolation of a fitted law (contract section 2 support wording). The T >= 0 bound: the design's T_cs bracket evaluates Ic at T = 0, so the law is applied on 0 <= t < 1 (see implementation-notes.md). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/nb3sn_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.magnet_conductor_alternatives.nb3sn_cable_critical_surface_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts temperature_margin, element_copper_area, acceptance_pass, T_cs, acceptance_margin, status_code, temp_rule_margin, fraction_rule_margin, supported, ic_cable_op, operating_fraction, tcs_defined, ic_strand_op, T_conductor, element_area_total fields to separate channels.
    """

    name: str = "Nb3Sn_Cable_Critical_SurfaceModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, B_design_max_in: float, B_edge_max_in: float, C1_in: float, T_supply_in: float, n_strands_in: float, T_law_min_in: float, Ca1_in: float, B_peak_in: float, eps_max_in: float, nuclear_rise_in: float, turn_current_in: float, acceptance_rule_in: float, margin_rise_in: float, strand_diameter_in: float, Tc0_in: float, strand_copper_fraction_in: float, eps_min_in: float, Ca2_in: float, B_law_max_in: float, eps_intrinsic_in: float, Bc20_in: float, B_law_min_in: float, q_in: float, p_in: float, fraction_rule_in: float, T_law_max_in: float, eps0a_in: float    ) -> Nb3Sn_Cable_Critical_SurfaceInput:
        """Validate inputs and fill defaults.

        Args:
            B_design_max_in: B_design_max_in input
            B_edge_max_in: B_edge_max_in input
            C1_in: C1_in input
            T_supply_in: T_supply_in input
            n_strands_in: n_strands_in input
            T_law_min_in: T_law_min_in input
            Ca1_in: Ca1_in input
            B_peak_in: B_peak_in input
            eps_max_in: eps_max_in input
            nuclear_rise_in: nuclear_rise_in input
            turn_current_in: turn_current_in input
            acceptance_rule_in: acceptance_rule_in input
            margin_rise_in: margin_rise_in input
            strand_diameter_in: strand_diameter_in input
            Tc0_in: Tc0_in input
            strand_copper_fraction_in: strand_copper_fraction_in input
            eps_min_in: eps_min_in input
            Ca2_in: Ca2_in input
            B_law_max_in: B_law_max_in input
            eps_intrinsic_in: eps_intrinsic_in input
            Bc20_in: Bc20_in input
            B_law_min_in: B_law_min_in input
            q_in: q_in input
            p_in: p_in input
            fraction_rule_in: fraction_rule_in input
            T_law_max_in: T_law_max_in input
            eps0a_in: eps0a_in input

        Returns:
            Validated input model
        """
        return Nb3Sn_Cable_Critical_SurfaceInput(B_design_max_in=B_design_max_in, B_edge_max_in=B_edge_max_in, C1_in=C1_in, T_supply_in=T_supply_in, n_strands_in=n_strands_in, T_law_min_in=T_law_min_in, Ca1_in=Ca1_in, B_peak_in=B_peak_in, eps_max_in=eps_max_in, nuclear_rise_in=nuclear_rise_in, turn_current_in=turn_current_in, acceptance_rule_in=acceptance_rule_in, margin_rise_in=margin_rise_in, strand_diameter_in=strand_diameter_in, Tc0_in=Tc0_in, strand_copper_fraction_in=strand_copper_fraction_in, eps_min_in=eps_min_in, Ca2_in=Ca2_in, B_law_max_in=B_law_max_in, eps_intrinsic_in=eps_intrinsic_in, Bc20_in=Bc20_in, B_law_min_in=B_law_min_in, q_in=q_in, p_in=p_in, fraction_rule_in=fraction_rule_in, T_law_max_in=T_law_max_in, eps0a_in=eps0a_in)

    def run(
        self, B_design_max_in: float, B_edge_max_in: float, C1_in: float, T_supply_in: float, n_strands_in: float, T_law_min_in: float, Ca1_in: float, B_peak_in: float, eps_max_in: float, nuclear_rise_in: float, turn_current_in: float, acceptance_rule_in: float, margin_rise_in: float, strand_diameter_in: float, Tc0_in: float, strand_copper_fraction_in: float, eps_min_in: float, Ca2_in: float, B_law_max_in: float, eps_intrinsic_in: float, Bc20_in: float, B_law_min_in: float, q_in: float, p_in: float, fraction_rule_in: float, T_law_max_in: float, eps0a_in: float    ) -> ModuleResult[Nb3Sn_Cable_Critical_SurfaceOutput]:
        """Execute calculation.

        Args:
            B_design_max_in: B_design_max_in input
            B_edge_max_in: B_edge_max_in input
            C1_in: C1_in input
            T_supply_in: T_supply_in input
            n_strands_in: n_strands_in input
            T_law_min_in: T_law_min_in input
            Ca1_in: Ca1_in input
            B_peak_in: B_peak_in input
            eps_max_in: eps_max_in input
            nuclear_rise_in: nuclear_rise_in input
            turn_current_in: turn_current_in input
            acceptance_rule_in: acceptance_rule_in input
            margin_rise_in: margin_rise_in input
            strand_diameter_in: strand_diameter_in input
            Tc0_in: Tc0_in input
            strand_copper_fraction_in: strand_copper_fraction_in input
            eps_min_in: eps_min_in input
            Ca2_in: Ca2_in input
            B_law_max_in: B_law_max_in input
            eps_intrinsic_in: eps_intrinsic_in input
            Bc20_in: Bc20_in input
            B_law_min_in: B_law_min_in input
            q_in: q_in input
            p_in: p_in input
            fraction_rule_in: fraction_rule_in input
            T_law_max_in: T_law_max_in input
            eps0a_in: eps0a_in input

        Returns:
            Module result with Nb3Sn_Cable_Critical_SurfaceOutput (temperature_margin, element_copper_area, acceptance_pass, T_cs, acceptance_margin, status_code, temp_rule_margin, fraction_rule_margin, supported, ic_cable_op, operating_fraction, tcs_defined, ic_strand_op, T_conductor, element_area_total)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(B_design_max_in, B_edge_max_in, C1_in, T_supply_in, n_strands_in, T_law_min_in, Ca1_in, B_peak_in, eps_max_in, nuclear_rise_in, turn_current_in, acceptance_rule_in, margin_rise_in, strand_diameter_in, Tc0_in, strand_copper_fraction_in, eps_min_in, Ca2_in, B_law_max_in, eps_intrinsic_in, Bc20_in, B_law_min_in, q_in, p_in, fraction_rule_in, T_law_max_in, eps0a_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.magnet_conductor_alternatives.nb3sn_cable_critical_surface_impl import (
            run_nb3sn_cable_critical_surface,
        )

        # Execute implementation - returns tuple of values
        temperature_margin, element_copper_area, acceptance_pass, T_cs, acceptance_margin, status_code, temp_rule_margin, fraction_rule_margin, supported, ic_cable_op, operating_fraction, tcs_defined, ic_strand_op, T_conductor, element_area_total = run_nb3sn_cable_critical_surface(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Nb3Sn_Cable_Critical_SurfaceOutput(
                temperature_margin=temperature_margin,
                element_copper_area=element_copper_area,
                acceptance_pass=acceptance_pass,
                T_cs=T_cs,
                acceptance_margin=acceptance_margin,
                status_code=status_code,
                temp_rule_margin=temp_rule_margin,
                fraction_rule_margin=fraction_rule_margin,
                supported=supported,
                ic_cable_op=ic_cable_op,
                operating_fraction=operating_fraction,
                tcs_defined=tcs_defined,
                ic_strand_op=ic_strand_op,
                T_conductor=T_conductor,
                element_area_total=element_area_total,
            )
        )
