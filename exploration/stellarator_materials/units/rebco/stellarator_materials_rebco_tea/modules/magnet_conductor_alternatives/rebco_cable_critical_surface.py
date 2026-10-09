"""REBCO_Cable_Critical_SurfaceModule Module Wrapper

TEAx module for REBCO_Cable_Critical_Surface calculation.

REBCO tape critical current at the supplied tape count, turn current, peak field and conductor temperature. Field shape g(B): shape_mode 0 interpolates log-log between the measured 20 K, B||c knots g8, g10, g12, g15, g20 at 8, 10, 12, 15, 20 T (defined only on [8, 20] T; NaN outside, since no knot interval exists there); shape_mode 1 is the power law (B/20)^-alpha. Ic_tape(B, T) = anchor_ic*g(B)*exp(-(T - 20)/T_star); Ic_cable = n*degradation*Ic_tape; T_cs = 20 + T_star*ln(n*degradation*anchor_ic*g(B)/I) (closed form). Rule margins, acceptance selection and area outputs as in 'Nb3Sn Cable Critical Surface'; element_area_total = n*w*t*1e6 mm2 and element_copper_area = tape_copper_fraction*element_area_total. status_code 1 when B lies in the active shape's supported range ([B_knot_min, B_knot_max] for shape 0, [B_law_min, B_law_max] for shape 1) and T_conductor lies in [T_law_min, T_law_max]; otherwise 0 (unsupported). REBCO has no edge or law-only band. **Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf; knowledge/sources/field_and_temperature_scaling_of_the_critical_current/raw.pdf **Reference**: Molodyk et al. 2021 Fig. 1a (raw.pdf p.3), output.md:77, :93, :137; Senatore et al. 2016 eq. (1), raw.pdf p.6, validity output.md:94; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.2; contract section 3. **Basis**: measured 20 K shape digitized twice (check-rebco-cryo-cost.md section 1); Senatore exponential temperature form; field perpendicular to the tape face assumed everywhere. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/rebco_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - B_law_min_in: B_law_min_in parameter
    - g8_in: g8_in parameter
    - B_peak_in: B_peak_in parameter
    - tape_width_in: tape_width_in parameter
    - tape_thickness_in: tape_thickness_in parameter
    - B_knot_max_in: B_knot_max_in parameter
    - margin_rise_in: margin_rise_in parameter
    - g15_in: g15_in parameter
    - fraction_rule_in: fraction_rule_in parameter
    - T_law_min_in: T_law_min_in parameter
    - nuclear_rise_in: nuclear_rise_in parameter
    - n_tapes_in: n_tapes_in parameter
    - g12_in: g12_in parameter
    - turn_current_in: turn_current_in parameter
    - anchor_ic_in: anchor_ic_in parameter
    - T_supply_in: T_supply_in parameter
    - degradation_in: degradation_in parameter
    - tape_copper_fraction_in: tape_copper_fraction_in parameter
    - shape_mode_in: shape_mode_in parameter
    - B_knot_min_in: B_knot_min_in parameter
    - B_law_max_in: B_law_max_in parameter
    - alpha_in: alpha_in parameter
    - acceptance_rule_in: acceptance_rule_in parameter
    - T_law_max_in: T_law_max_in parameter
    - g10_in: g10_in parameter
    - T_star_in: T_star_in parameter
    - g20_in: g20_in parameter

Outputs:
    - acceptance_margin: acceptance_margin result
    - acceptance_pass: acceptance_pass result
    - tcs_defined: tcs_defined result
    - status_code: status_code result
    - ic_tape_op: ic_tape_op result
    - temperature_margin: temperature_margin result
    - operating_fraction: operating_fraction result
    - element_area_total: element_area_total result
    - T_conductor: T_conductor result
    - ic_cable_op: ic_cable_op result
    - element_copper_area: element_copper_area result
    - fraction_rule_margin: fraction_rule_margin result
    - supported: supported result
    - T_cs: T_cs result
    - temp_rule_margin: temp_rule_margin result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:51

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:51

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_conductor_alternatives/rebco_cable_critical_surface_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.rebco_cable_critical_surface_output import REBCO_Cable_Critical_SurfaceOutput


class REBCO_Cable_Critical_SurfaceInput(BaseModel):
    """Input model for REBCO_Cable_Critical_SurfaceModule.

    Attributes:
        B_law_min_in: B_law_min_in input
        g8_in: g8_in input
        B_peak_in: B_peak_in input
        tape_width_in: tape_width_in input
        tape_thickness_in: tape_thickness_in input
        B_knot_max_in: B_knot_max_in input
        margin_rise_in: margin_rise_in input
        g15_in: g15_in input
        fraction_rule_in: fraction_rule_in input
        T_law_min_in: T_law_min_in input
        nuclear_rise_in: nuclear_rise_in input
        n_tapes_in: n_tapes_in input
        g12_in: g12_in input
        turn_current_in: turn_current_in input
        anchor_ic_in: anchor_ic_in input
        T_supply_in: T_supply_in input
        degradation_in: degradation_in input
        tape_copper_fraction_in: tape_copper_fraction_in input
        shape_mode_in: shape_mode_in input
        B_knot_min_in: B_knot_min_in input
        B_law_max_in: B_law_max_in input
        alpha_in: alpha_in input
        acceptance_rule_in: acceptance_rule_in input
        T_law_max_in: T_law_max_in input
        g10_in: g10_in input
        T_star_in: T_star_in input
        g20_in: g20_in input
    """
    B_law_min_in: float = Field(..., description="B_law_min_in input")
    g8_in: float = Field(..., description="g8_in input")
    B_peak_in: float = Field(..., description="B_peak_in input")
    tape_width_in: float = Field(..., description="tape_width_in input")
    tape_thickness_in: float = Field(..., description="tape_thickness_in input")
    B_knot_max_in: float = Field(..., description="B_knot_max_in input")
    margin_rise_in: float = Field(..., description="margin_rise_in input")
    g15_in: float = Field(..., description="g15_in input")
    fraction_rule_in: float = Field(..., description="fraction_rule_in input")
    T_law_min_in: float = Field(..., description="T_law_min_in input")
    nuclear_rise_in: float = Field(..., description="nuclear_rise_in input")
    n_tapes_in: float = Field(..., description="n_tapes_in input")
    g12_in: float = Field(..., description="g12_in input")
    turn_current_in: float = Field(..., description="turn_current_in input")
    anchor_ic_in: float = Field(..., description="anchor_ic_in input")
    T_supply_in: float = Field(..., description="T_supply_in input")
    degradation_in: float = Field(..., description="degradation_in input")
    tape_copper_fraction_in: float = Field(..., description="tape_copper_fraction_in input")
    shape_mode_in: float = Field(..., description="shape_mode_in input")
    B_knot_min_in: float = Field(..., description="B_knot_min_in input")
    B_law_max_in: float = Field(..., description="B_law_max_in input")
    alpha_in: float = Field(..., description="alpha_in input")
    acceptance_rule_in: float = Field(..., description="acceptance_rule_in input")
    T_law_max_in: float = Field(..., description="T_law_max_in input")
    g10_in: float = Field(..., description="g10_in input")
    T_star_in: float = Field(..., description="T_star_in input")
    g20_in: float = Field(..., description="g20_in input")


class REBCO_Cable_Critical_SurfaceModule(ModuleBase[REBCO_Cable_Critical_SurfaceInput, REBCO_Cable_Critical_SurfaceOutput]):
    """TEAx module for REBCO_Cable_Critical_Surface calculation.

REBCO tape critical current at the supplied tape count, turn current, peak field and conductor temperature. Field shape g(B): shape_mode 0 interpolates log-log between the measured 20 K, B||c knots g8, g10, g12, g15, g20 at 8, 10, 12, 15, 20 T (defined only on [8, 20] T; NaN outside, since no knot interval exists there); shape_mode 1 is the power law (B/20)^-alpha. Ic_tape(B, T) = anchor_ic*g(B)*exp(-(T - 20)/T_star); Ic_cable = n*degradation*Ic_tape; T_cs = 20 + T_star*ln(n*degradation*anchor_ic*g(B)/I) (closed form). Rule margins, acceptance selection and area outputs as in 'Nb3Sn Cable Critical Surface'; element_area_total = n*w*t*1e6 mm2 and element_copper_area = tape_copper_fraction*element_area_total. status_code 1 when B lies in the active shape's supported range ([B_knot_min, B_knot_max] for shape 0, [B_law_min, B_law_max] for shape 1) and T_conductor lies in [T_law_min, T_law_max]; otherwise 0 (unsupported). REBCO has no edge or law-only band. **Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf; knowledge/sources/field_and_temperature_scaling_of_the_critical_current/raw.pdf **Reference**: Molodyk et al. 2021 Fig. 1a (raw.pdf p.3), output.md:77, :93, :137; Senatore et al. 2016 eq. (1), raw.pdf p.6, validity output.md:94; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.2; contract section 3. **Basis**: measured 20 K shape digitized twice (check-rebco-cryo-cost.md section 1); Senatore exponential temperature form; field perpendicular to the tape face assumed everywhere. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/rebco_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - B_law_min_in: B_law_min_in parameter
    - g8_in: g8_in parameter
    - B_peak_in: B_peak_in parameter
    - tape_width_in: tape_width_in parameter
    - tape_thickness_in: tape_thickness_in parameter
    - B_knot_max_in: B_knot_max_in parameter
    - margin_rise_in: margin_rise_in parameter
    - g15_in: g15_in parameter
    - fraction_rule_in: fraction_rule_in parameter
    - T_law_min_in: T_law_min_in parameter
    - nuclear_rise_in: nuclear_rise_in parameter
    - n_tapes_in: n_tapes_in parameter
    - g12_in: g12_in parameter
    - turn_current_in: turn_current_in parameter
    - anchor_ic_in: anchor_ic_in parameter
    - T_supply_in: T_supply_in parameter
    - degradation_in: degradation_in parameter
    - tape_copper_fraction_in: tape_copper_fraction_in parameter
    - shape_mode_in: shape_mode_in parameter
    - B_knot_min_in: B_knot_min_in parameter
    - B_law_max_in: B_law_max_in parameter
    - alpha_in: alpha_in parameter
    - acceptance_rule_in: acceptance_rule_in parameter
    - T_law_max_in: T_law_max_in parameter
    - g10_in: g10_in parameter
    - T_star_in: T_star_in parameter
    - g20_in: g20_in parameter

Outputs:
    - acceptance_margin: acceptance_margin result
    - acceptance_pass: acceptance_pass result
    - tcs_defined: tcs_defined result
    - status_code: status_code result
    - ic_tape_op: ic_tape_op result
    - temperature_margin: temperature_margin result
    - operating_fraction: operating_fraction result
    - element_area_total: element_area_total result
    - T_conductor: T_conductor result
    - ic_cable_op: ic_cable_op result
    - element_copper_area: element_copper_area result
    - fraction_rule_margin: fraction_rule_margin result
    - supported: supported result
    - T_cs: T_cs result
    - temp_rule_margin: temp_rule_margin result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:51

    SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:51

    Calculation Specification:
        n_tapes_in = 0.0
        tape_width_in = 0.0
        tape_thickness_in = 0.0
        tape_copper_fraction_in = 0.0
        turn_current_in = 0.0
        B_peak_in = 0.0
        T_supply_in = 0.0
        nuclear_rise_in = 0.0
        margin_rise_in = 0.0
        anchor_ic_in = 0.0
        shape_mode_in = 0.0
        g8_in = 1.0
        g10_in = 1.0
        g12_in = 1.0
        g15_in = 1.0
        g20_in = 1.0
        alpha_in = 0.0
        T_star_in = 1.0
        degradation_in = 1.0
        fraction_rule_in = 0.0
        acceptance_rule_in = 0.0
        B_knot_min_in = 0.0
        B_knot_max_in = 0.0
        B_law_min_in = 0.0
        B_law_max_in = 0.0
        T_law_min_in = 0.0
        T_law_max_in = 0.0
        
Documentation:
REBCO tape critical current at the supplied tape count, turn current, peak field and conductor temperature. Field shape g(B): shape_mode 0 interpolates log-log between the measured 20 K, B||c knots g8, g10, g12, g15, g20 at 8, 10, 12, 15, 20 T (defined only on [8, 20] T; NaN outside, since no knot interval exists there); shape_mode 1 is the power law (B/20)^-alpha. Ic_tape(B, T) = anchor_ic*g(B)*exp(-(T - 20)/T_star); Ic_cable = n*degradation*Ic_tape; T_cs = 20 + T_star*ln(n*degradation*anchor_ic*g(B)/I) (closed form). Rule margins, acceptance selection and area outputs as in 'Nb3Sn Cable Critical Surface'; element_area_total = n*w*t*1e6 mm2 and element_copper_area = tape_copper_fraction*element_area_total. status_code 1 when B lies in the active shape's supported range ([B_knot_min, B_knot_max] for shape 0, [B_law_min, B_law_max] for shape 1) and T_conductor lies in [T_law_min, T_law_max]; otherwise 0 (unsupported). REBCO has no edge or law-only band. **Source**: knowledge/sources/development_and_large_volume_production_of_extremely_high/raw.pdf; knowledge/sources/field_and_temperature_scaling_of_the_critical_current/raw.pdf **Reference**: Molodyk et al. 2021 Fig. 1a (raw.pdf p.3), output.md:77, :93, :137; Senatore et al. 2016 eq. (1), raw.pdf p.6, validity output.md:94; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.2; contract section 3. **Basis**: measured 20 K shape digitized twice (check-rebco-cryo-cost.md section 1); Senatore exponential temperature form; field perpendicular to the tape face assumed everywhere. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/rebco_cable_critical_surface_impl.py. **Last Updated**: 2026-09-29

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.magnet_conductor_alternatives.rebco_cable_critical_surface_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts acceptance_margin, acceptance_pass, tcs_defined, status_code, ic_tape_op, temperature_margin, operating_fraction, element_area_total, T_conductor, ic_cable_op, element_copper_area, fraction_rule_margin, supported, T_cs, temp_rule_margin fields to separate channels.
    """

    name: str = "REBCO_Cable_Critical_SurfaceModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, B_law_min_in: float, g8_in: float, B_peak_in: float, tape_width_in: float, tape_thickness_in: float, B_knot_max_in: float, margin_rise_in: float, g15_in: float, fraction_rule_in: float, T_law_min_in: float, nuclear_rise_in: float, n_tapes_in: float, g12_in: float, turn_current_in: float, anchor_ic_in: float, T_supply_in: float, degradation_in: float, tape_copper_fraction_in: float, shape_mode_in: float, B_knot_min_in: float, B_law_max_in: float, alpha_in: float, acceptance_rule_in: float, T_law_max_in: float, g10_in: float, T_star_in: float, g20_in: float    ) -> REBCO_Cable_Critical_SurfaceInput:
        """Validate inputs and fill defaults.

        Args:
            B_law_min_in: B_law_min_in input
            g8_in: g8_in input
            B_peak_in: B_peak_in input
            tape_width_in: tape_width_in input
            tape_thickness_in: tape_thickness_in input
            B_knot_max_in: B_knot_max_in input
            margin_rise_in: margin_rise_in input
            g15_in: g15_in input
            fraction_rule_in: fraction_rule_in input
            T_law_min_in: T_law_min_in input
            nuclear_rise_in: nuclear_rise_in input
            n_tapes_in: n_tapes_in input
            g12_in: g12_in input
            turn_current_in: turn_current_in input
            anchor_ic_in: anchor_ic_in input
            T_supply_in: T_supply_in input
            degradation_in: degradation_in input
            tape_copper_fraction_in: tape_copper_fraction_in input
            shape_mode_in: shape_mode_in input
            B_knot_min_in: B_knot_min_in input
            B_law_max_in: B_law_max_in input
            alpha_in: alpha_in input
            acceptance_rule_in: acceptance_rule_in input
            T_law_max_in: T_law_max_in input
            g10_in: g10_in input
            T_star_in: T_star_in input
            g20_in: g20_in input

        Returns:
            Validated input model
        """
        return REBCO_Cable_Critical_SurfaceInput(B_law_min_in=B_law_min_in, g8_in=g8_in, B_peak_in=B_peak_in, tape_width_in=tape_width_in, tape_thickness_in=tape_thickness_in, B_knot_max_in=B_knot_max_in, margin_rise_in=margin_rise_in, g15_in=g15_in, fraction_rule_in=fraction_rule_in, T_law_min_in=T_law_min_in, nuclear_rise_in=nuclear_rise_in, n_tapes_in=n_tapes_in, g12_in=g12_in, turn_current_in=turn_current_in, anchor_ic_in=anchor_ic_in, T_supply_in=T_supply_in, degradation_in=degradation_in, tape_copper_fraction_in=tape_copper_fraction_in, shape_mode_in=shape_mode_in, B_knot_min_in=B_knot_min_in, B_law_max_in=B_law_max_in, alpha_in=alpha_in, acceptance_rule_in=acceptance_rule_in, T_law_max_in=T_law_max_in, g10_in=g10_in, T_star_in=T_star_in, g20_in=g20_in)

    def run(
        self, B_law_min_in: float, g8_in: float, B_peak_in: float, tape_width_in: float, tape_thickness_in: float, B_knot_max_in: float, margin_rise_in: float, g15_in: float, fraction_rule_in: float, T_law_min_in: float, nuclear_rise_in: float, n_tapes_in: float, g12_in: float, turn_current_in: float, anchor_ic_in: float, T_supply_in: float, degradation_in: float, tape_copper_fraction_in: float, shape_mode_in: float, B_knot_min_in: float, B_law_max_in: float, alpha_in: float, acceptance_rule_in: float, T_law_max_in: float, g10_in: float, T_star_in: float, g20_in: float    ) -> ModuleResult[REBCO_Cable_Critical_SurfaceOutput]:
        """Execute calculation.

        Args:
            B_law_min_in: B_law_min_in input
            g8_in: g8_in input
            B_peak_in: B_peak_in input
            tape_width_in: tape_width_in input
            tape_thickness_in: tape_thickness_in input
            B_knot_max_in: B_knot_max_in input
            margin_rise_in: margin_rise_in input
            g15_in: g15_in input
            fraction_rule_in: fraction_rule_in input
            T_law_min_in: T_law_min_in input
            nuclear_rise_in: nuclear_rise_in input
            n_tapes_in: n_tapes_in input
            g12_in: g12_in input
            turn_current_in: turn_current_in input
            anchor_ic_in: anchor_ic_in input
            T_supply_in: T_supply_in input
            degradation_in: degradation_in input
            tape_copper_fraction_in: tape_copper_fraction_in input
            shape_mode_in: shape_mode_in input
            B_knot_min_in: B_knot_min_in input
            B_law_max_in: B_law_max_in input
            alpha_in: alpha_in input
            acceptance_rule_in: acceptance_rule_in input
            T_law_max_in: T_law_max_in input
            g10_in: g10_in input
            T_star_in: T_star_in input
            g20_in: g20_in input

        Returns:
            Module result with REBCO_Cable_Critical_SurfaceOutput (acceptance_margin, acceptance_pass, tcs_defined, status_code, ic_tape_op, temperature_margin, operating_fraction, element_area_total, T_conductor, ic_cable_op, element_copper_area, fraction_rule_margin, supported, T_cs, temp_rule_margin)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(B_law_min_in, g8_in, B_peak_in, tape_width_in, tape_thickness_in, B_knot_max_in, margin_rise_in, g15_in, fraction_rule_in, T_law_min_in, nuclear_rise_in, n_tapes_in, g12_in, turn_current_in, anchor_ic_in, T_supply_in, degradation_in, tape_copper_fraction_in, shape_mode_in, B_knot_min_in, B_law_max_in, alpha_in, acceptance_rule_in, T_law_max_in, g10_in, T_star_in, g20_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.magnet_conductor_alternatives.rebco_cable_critical_surface_impl import (
            run_rebco_cable_critical_surface,
        )

        # Execute implementation - returns tuple of values
        acceptance_margin, acceptance_pass, tcs_defined, status_code, ic_tape_op, temperature_margin, operating_fraction, element_area_total, T_conductor, ic_cable_op, element_copper_area, fraction_rule_margin, supported, T_cs, temp_rule_margin = run_rebco_cable_critical_surface(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=REBCO_Cable_Critical_SurfaceOutput(
                acceptance_margin=acceptance_margin,
                acceptance_pass=acceptance_pass,
                tcs_defined=tcs_defined,
                status_code=status_code,
                ic_tape_op=ic_tape_op,
                temperature_margin=temperature_margin,
                operating_fraction=operating_fraction,
                element_area_total=element_area_total,
                T_conductor=T_conductor,
                ic_cable_op=ic_cable_op,
                element_copper_area=element_copper_area,
                fraction_rule_margin=fraction_rule_margin,
                supported=supported,
                T_cs=T_cs,
                temp_rule_margin=temp_rule_margin,
            )
        )
