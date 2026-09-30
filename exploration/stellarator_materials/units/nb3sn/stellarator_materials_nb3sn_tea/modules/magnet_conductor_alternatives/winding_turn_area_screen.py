"""Winding_Turn_Area_ScreenModule Module Wrapper

TEAx module for Winding_Turn_Area_Screen calculation.

Sums the supplied per-turn component areas and compares the gross area with the envelope; separately computes the allowance-rule requirements at the evaluated duty and compares them with the supplied areas. It never resizes an area. cable = element_area/cabling_factor/(1 - cable_void); net = cable + cu_space + steel_area + misc_area + solder_area; gross = net/(1 - ins_fraction); fit_margin = available_area - gross; fit_margin_fraction = fit_margin/available_area; required_envelope_J = I/gross (A/mm2). Copper rule: if J_cu_rule > 0, cu_required = max(0, I/J_cu_rule - element_copper_area)/(1 - cu_void), else cu_required = cu_per_kA_rule*I/1000. Steel rule: steel_required = steel_per_kA_rule*(I/1000)*(B/B_steel_ref if steel_B_scaling = 1, else 1). Margins are supplied minus required; pass flags are 1 when the margin is >= 0. Protection and structural adequacy are allowance rules, not evaluated physics. **Source**: knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/raw.pdf; knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png **Reference**: Demattè & Bruzzone Table I and pp.2-4 (output.md:106, :139); Stellaris Table 7; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.3; contract section 4 (constructions P and C). **Basis**: [AGENT] allowance-rule construction calibrated to reproduce EU DEMO layer 1 and Stellaris Table 7; scaling steel with B at fixed geometry is a bounded assumption. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_turn_area_screen_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - cu_void_in: cu_void_in parameter
    - J_cu_rule_in: J_cu_rule_in parameter
    - steel_per_kA_rule_in: steel_per_kA_rule_in parameter
    - cu_space_in: cu_space_in parameter
    - element_area_in: element_area_in parameter
    - steel_B_scaling_in: steel_B_scaling_in parameter
    - B_steel_ref_in: B_steel_ref_in parameter
    - ins_fraction_in: ins_fraction_in parameter
    - cable_void_in: cable_void_in parameter
    - cu_per_kA_rule_in: cu_per_kA_rule_in parameter
    - cabling_factor_in: cabling_factor_in parameter
    - steel_area_in: steel_area_in parameter
    - misc_area_in: misc_area_in parameter
    - B_peak_in: B_peak_in parameter
    - turn_current_in: turn_current_in parameter
    - available_area_in: available_area_in parameter
    - solder_area_in: solder_area_in parameter
    - element_copper_area_in: element_copper_area_in parameter

Outputs:
    - net_area: net_area result
    - fit_margin: fit_margin result
    - steel_margin: steel_margin result
    - fit_margin_fraction: fit_margin_fraction result
    - steel_pass: steel_pass result
    - cu_required: cu_required result
    - cu_pass: cu_pass result
    - steel_required: steel_required result
    - gross_area: gross_area result
    - cable_area: cable_area result
    - cu_margin: cu_margin result
    - required_envelope_J: required_envelope_J result
    - fit_pass: fit_pass result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:97

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:97

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_conductor_alternatives/winding_turn_area_screen_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.winding_turn_area_screen_output import Winding_Turn_Area_ScreenOutput


class Winding_Turn_Area_ScreenInput(BaseModel):
    """Input model for Winding_Turn_Area_ScreenModule.

    Attributes:
        cu_void_in: cu_void_in input
        J_cu_rule_in: J_cu_rule_in input
        steel_per_kA_rule_in: steel_per_kA_rule_in input
        cu_space_in: cu_space_in input
        element_area_in: element_area_in input
        steel_B_scaling_in: steel_B_scaling_in input
        B_steel_ref_in: B_steel_ref_in input
        ins_fraction_in: ins_fraction_in input
        cable_void_in: cable_void_in input
        cu_per_kA_rule_in: cu_per_kA_rule_in input
        cabling_factor_in: cabling_factor_in input
        steel_area_in: steel_area_in input
        misc_area_in: misc_area_in input
        B_peak_in: B_peak_in input
        turn_current_in: turn_current_in input
        available_area_in: available_area_in input
        solder_area_in: solder_area_in input
        element_copper_area_in: element_copper_area_in input
    """
    cu_void_in: float = Field(..., description="cu_void_in input")
    J_cu_rule_in: float = Field(..., description="J_cu_rule_in input")
    steel_per_kA_rule_in: float = Field(..., description="steel_per_kA_rule_in input")
    cu_space_in: float = Field(..., description="cu_space_in input")
    element_area_in: float = Field(..., description="element_area_in input")
    steel_B_scaling_in: float = Field(..., description="steel_B_scaling_in input")
    B_steel_ref_in: float = Field(..., description="B_steel_ref_in input")
    ins_fraction_in: float = Field(..., description="ins_fraction_in input")
    cable_void_in: float = Field(..., description="cable_void_in input")
    cu_per_kA_rule_in: float = Field(..., description="cu_per_kA_rule_in input")
    cabling_factor_in: float = Field(..., description="cabling_factor_in input")
    steel_area_in: float = Field(..., description="steel_area_in input")
    misc_area_in: float = Field(..., description="misc_area_in input")
    B_peak_in: float = Field(..., description="B_peak_in input")
    turn_current_in: float = Field(..., description="turn_current_in input")
    available_area_in: float = Field(..., description="available_area_in input")
    solder_area_in: float = Field(..., description="solder_area_in input")
    element_copper_area_in: float = Field(..., description="element_copper_area_in input")


class Winding_Turn_Area_ScreenModule(ModuleBase[Winding_Turn_Area_ScreenInput, Winding_Turn_Area_ScreenOutput]):
    """TEAx module for Winding_Turn_Area_Screen calculation.

Sums the supplied per-turn component areas and compares the gross area with the envelope; separately computes the allowance-rule requirements at the evaluated duty and compares them with the supplied areas. It never resizes an area. cable = element_area/cabling_factor/(1 - cable_void); net = cable + cu_space + steel_area + misc_area + solder_area; gross = net/(1 - ins_fraction); fit_margin = available_area - gross; fit_margin_fraction = fit_margin/available_area; required_envelope_J = I/gross (A/mm2). Copper rule: if J_cu_rule > 0, cu_required = max(0, I/J_cu_rule - element_copper_area)/(1 - cu_void), else cu_required = cu_per_kA_rule*I/1000. Steel rule: steel_required = steel_per_kA_rule*(I/1000)*(B/B_steel_ref if steel_B_scaling = 1, else 1). Margins are supplied minus required; pass flags are 1 when the margin is >= 0. Protection and structural adequacy are allowance rules, not evaluated physics. **Source**: knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/raw.pdf; knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png **Reference**: Demattè & Bruzzone Table I and pp.2-4 (output.md:106, :139); Stellaris Table 7; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.3; contract section 4 (constructions P and C). **Basis**: [AGENT] allowance-rule construction calibrated to reproduce EU DEMO layer 1 and Stellaris Table 7; scaling steel with B at fixed geometry is a bounded assumption. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_turn_area_screen_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - cu_void_in: cu_void_in parameter
    - J_cu_rule_in: J_cu_rule_in parameter
    - steel_per_kA_rule_in: steel_per_kA_rule_in parameter
    - cu_space_in: cu_space_in parameter
    - element_area_in: element_area_in parameter
    - steel_B_scaling_in: steel_B_scaling_in parameter
    - B_steel_ref_in: B_steel_ref_in parameter
    - ins_fraction_in: ins_fraction_in parameter
    - cable_void_in: cable_void_in parameter
    - cu_per_kA_rule_in: cu_per_kA_rule_in parameter
    - cabling_factor_in: cabling_factor_in parameter
    - steel_area_in: steel_area_in parameter
    - misc_area_in: misc_area_in parameter
    - B_peak_in: B_peak_in parameter
    - turn_current_in: turn_current_in parameter
    - available_area_in: available_area_in parameter
    - solder_area_in: solder_area_in parameter
    - element_copper_area_in: element_copper_area_in parameter

Outputs:
    - net_area: net_area result
    - fit_margin: fit_margin result
    - steel_margin: steel_margin result
    - fit_margin_fraction: fit_margin_fraction result
    - steel_pass: steel_pass result
    - cu_required: cu_required result
    - cu_pass: cu_pass result
    - steel_required: steel_required result
    - gross_area: gross_area result
    - cable_area: cable_area result
    - cu_margin: cu_margin result
    - required_envelope_J: required_envelope_J result
    - fit_pass: fit_pass result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:97

    SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:97

    Calculation Specification:
        turn_current_in = 0.0
        B_peak_in = 0.0
        available_area_in = 0.0
        element_area_in = 0.0
        element_copper_area_in = 0.0
        cabling_factor_in = 1.0
        cable_void_in = 0.0
        cu_space_in = 0.0
        steel_area_in = 0.0
        misc_area_in = 0.0
        solder_area_in = 0.0
        ins_fraction_in = 0.0
        J_cu_rule_in = 0.0
        cu_void_in = 0.0
        cu_per_kA_rule_in = 0.0
        steel_per_kA_rule_in = 0.0
        B_steel_ref_in = 1.0
        steel_B_scaling_in = 0.0
        
Documentation:
Sums the supplied per-turn component areas and compares the gross area with the envelope; separately computes the allowance-rule requirements at the evaluated duty and compares them with the supplied areas. It never resizes an area. cable = element_area/cabling_factor/(1 - cable_void); net = cable + cu_space + steel_area + misc_area + solder_area; gross = net/(1 - ins_fraction); fit_margin = available_area - gross; fit_margin_fraction = fit_margin/available_area; required_envelope_J = I/gross (A/mm2). Copper rule: if J_cu_rule > 0, cu_required = max(0, I/J_cu_rule - element_copper_area)/(1 - cu_void), else cu_required = cu_per_kA_rule*I/1000. Steel rule: steel_required = steel_per_kA_rule*(I/1000)*(B/B_steel_ref if steel_B_scaling = 1, else 1). Margins are supplied minus required; pass flags are 1 when the margin is >= 0. Protection and structural adequacy are allowance rules, not evaluated physics. **Source**: knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/raw.pdf; knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png **Reference**: Demattè & Bruzzone Table I and pp.2-4 (output.md:106, :139); Stellaris Table 7; work/active/WI-099_magnet-conductor-alternatives/design.md section 2.3; contract section 4 (constructions P and C). **Basis**: [AGENT] allowance-rule construction calibrated to reproduce EU DEMO layer 1 and Stellaris Table 7; scaling steel with B at fixed geometry is a bounded assumption. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_turn_area_screen_impl.py. **Last Updated**: 2026-09-29

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.magnet_conductor_alternatives.winding_turn_area_screen_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts net_area, fit_margin, steel_margin, fit_margin_fraction, steel_pass, cu_required, cu_pass, steel_required, gross_area, cable_area, cu_margin, required_envelope_J, fit_pass fields to separate channels.
    """

    name: str = "Winding_Turn_Area_ScreenModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, cu_void_in: float, J_cu_rule_in: float, steel_per_kA_rule_in: float, cu_space_in: float, element_area_in: float, steel_B_scaling_in: float, B_steel_ref_in: float, ins_fraction_in: float, cable_void_in: float, cu_per_kA_rule_in: float, cabling_factor_in: float, steel_area_in: float, misc_area_in: float, B_peak_in: float, turn_current_in: float, available_area_in: float, solder_area_in: float, element_copper_area_in: float    ) -> Winding_Turn_Area_ScreenInput:
        """Validate inputs and fill defaults.

        Args:
            cu_void_in: cu_void_in input
            J_cu_rule_in: J_cu_rule_in input
            steel_per_kA_rule_in: steel_per_kA_rule_in input
            cu_space_in: cu_space_in input
            element_area_in: element_area_in input
            steel_B_scaling_in: steel_B_scaling_in input
            B_steel_ref_in: B_steel_ref_in input
            ins_fraction_in: ins_fraction_in input
            cable_void_in: cable_void_in input
            cu_per_kA_rule_in: cu_per_kA_rule_in input
            cabling_factor_in: cabling_factor_in input
            steel_area_in: steel_area_in input
            misc_area_in: misc_area_in input
            B_peak_in: B_peak_in input
            turn_current_in: turn_current_in input
            available_area_in: available_area_in input
            solder_area_in: solder_area_in input
            element_copper_area_in: element_copper_area_in input

        Returns:
            Validated input model
        """
        return Winding_Turn_Area_ScreenInput(cu_void_in=cu_void_in, J_cu_rule_in=J_cu_rule_in, steel_per_kA_rule_in=steel_per_kA_rule_in, cu_space_in=cu_space_in, element_area_in=element_area_in, steel_B_scaling_in=steel_B_scaling_in, B_steel_ref_in=B_steel_ref_in, ins_fraction_in=ins_fraction_in, cable_void_in=cable_void_in, cu_per_kA_rule_in=cu_per_kA_rule_in, cabling_factor_in=cabling_factor_in, steel_area_in=steel_area_in, misc_area_in=misc_area_in, B_peak_in=B_peak_in, turn_current_in=turn_current_in, available_area_in=available_area_in, solder_area_in=solder_area_in, element_copper_area_in=element_copper_area_in)

    def run(
        self, cu_void_in: float, J_cu_rule_in: float, steel_per_kA_rule_in: float, cu_space_in: float, element_area_in: float, steel_B_scaling_in: float, B_steel_ref_in: float, ins_fraction_in: float, cable_void_in: float, cu_per_kA_rule_in: float, cabling_factor_in: float, steel_area_in: float, misc_area_in: float, B_peak_in: float, turn_current_in: float, available_area_in: float, solder_area_in: float, element_copper_area_in: float    ) -> ModuleResult[Winding_Turn_Area_ScreenOutput]:
        """Execute calculation.

        Args:
            cu_void_in: cu_void_in input
            J_cu_rule_in: J_cu_rule_in input
            steel_per_kA_rule_in: steel_per_kA_rule_in input
            cu_space_in: cu_space_in input
            element_area_in: element_area_in input
            steel_B_scaling_in: steel_B_scaling_in input
            B_steel_ref_in: B_steel_ref_in input
            ins_fraction_in: ins_fraction_in input
            cable_void_in: cable_void_in input
            cu_per_kA_rule_in: cu_per_kA_rule_in input
            cabling_factor_in: cabling_factor_in input
            steel_area_in: steel_area_in input
            misc_area_in: misc_area_in input
            B_peak_in: B_peak_in input
            turn_current_in: turn_current_in input
            available_area_in: available_area_in input
            solder_area_in: solder_area_in input
            element_copper_area_in: element_copper_area_in input

        Returns:
            Module result with Winding_Turn_Area_ScreenOutput (net_area, fit_margin, steel_margin, fit_margin_fraction, steel_pass, cu_required, cu_pass, steel_required, gross_area, cable_area, cu_margin, required_envelope_J, fit_pass)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(cu_void_in, J_cu_rule_in, steel_per_kA_rule_in, cu_space_in, element_area_in, steel_B_scaling_in, B_steel_ref_in, ins_fraction_in, cable_void_in, cu_per_kA_rule_in, cabling_factor_in, steel_area_in, misc_area_in, B_peak_in, turn_current_in, available_area_in, solder_area_in, element_copper_area_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.magnet_conductor_alternatives.winding_turn_area_screen_impl import (
            run_winding_turn_area_screen,
        )

        # Execute implementation - returns tuple of values
        net_area, fit_margin, steel_margin, fit_margin_fraction, steel_pass, cu_required, cu_pass, steel_required, gross_area, cable_area, cu_margin, required_envelope_J, fit_pass = run_winding_turn_area_screen(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Turn_Area_ScreenOutput(
                net_area=net_area,
                fit_margin=fit_margin,
                steel_margin=steel_margin,
                fit_margin_fraction=fit_margin_fraction,
                steel_pass=steel_pass,
                cu_required=cu_required,
                cu_pass=cu_pass,
                steel_required=steel_required,
                gross_area=gross_area,
                cable_area=cable_area,
                cu_margin=cu_margin,
                required_envelope_J=required_envelope_J,
                fit_pass=fit_pass,
            )
        )
