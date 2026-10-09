"""Staged_Refrigeration_ScreenModule Module Wrapper

TEAx module for Staged_Refrigeration_Screen calculation.

Electrical demand and capital of the installed two-stage refrigerator, and the installed cold-stage rating compared with the calculated cold load. carnot = (T_amb - T_supply)/T_supply; carnot_ref = (T_amb - T_green)/T_green; equiv_factor = carnot/carnot_ref; R_equiv_kW = rating_cold/1000*(equiv_factor if capital_mode = 0, else 1); eta_cold = green_a*R_eta^green_b with R_eta = rating_cold/1000 (eta_mode 0) or rating_cold/1000*equiv_factor (eta_mode 2), or eta_const (eta_mode 1); p_in_cold = q_cold*carnot/eta_cold; p_in_shield = q_shield*(T_amb - T_shield)/T_shield/f_carnot_shield; p_in_total_MW = (p_in_cold + p_in_shield)/1e6; refrigerator_capital = green_c*R_equiv_kW^green_d*usd2015_to_2021. Efficiency is a property of the installed plant evaluated at its rating and applied to the operating load (part-load penalty not modeled). capacity_margin = rating_cold - q_cold; capacity_pass = 1 when >= 0. green_extrapolated = 1 when R_equiv_kW, or R_eta when a Green efficiency mode is active, lies outside Green's fitted data [0.01, 35] kW. **Source**: knowledge/sources/green_2015_cost_of_coolers_at_4_2_20_40_and_77_k_publisher/; knowledge/sources/strobridge_1974_cryogenic_refrigerators_an_updated_survey/ **Reference**: Green 2015 Eq. 1 and Eq. 2, printed p.2 (PDF p.3); Strobridge 1974 Eq. 1 (printed p.2), Fig. 1 and pp.4-6 (percent of Carnot independent of temperature band); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.6; contract section 6. **Basis**: [AGENT] one efficiency law for both temperatures at the installed capacity; 20 K capital by input-power equivalence (factor (300-20)/20 / ((300-4.5)/4.5) = 0.2132) per check-rebco-cryo-cost.md Recheck r2. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/staged_refrigeration_screen_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - T_green_in: T_green_in parameter
    - f_carnot_shield_in: f_carnot_shield_in parameter
    - capital_mode_in: capital_mode_in parameter
    - green_b_in: green_b_in parameter
    - green_a_in: green_a_in parameter
    - T_amb_in: T_amb_in parameter
    - usd2015_to_2021_in: usd2015_to_2021_in parameter
    - green_c_in: green_c_in parameter
    - green_d_in: green_d_in parameter
    - rating_cold_in: rating_cold_in parameter
    - T_shield_in: T_shield_in parameter
    - T_supply_in: T_supply_in parameter
    - q_shield_in: q_shield_in parameter
    - eta_mode_in: eta_mode_in parameter
    - eta_const_in: eta_const_in parameter
    - q_cold_in: q_cold_in parameter

Outputs:
    - p_in_total_MW: p_in_total_MW result
    - eta_cold: eta_cold result
    - green_extrapolated: green_extrapolated result
    - R_equiv_kW: R_equiv_kW result
    - refrigerator_capital: refrigerator_capital result
    - carnot_specific_power: carnot_specific_power result
    - p_in_cold: p_in_cold result
    - capacity_pass: capacity_pass result
    - capacity_margin: capacity_margin result
    - p_in_shield: p_in_shield result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:203

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:203

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_conductor_alternatives/staged_refrigeration_screen_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.staged_refrigeration_screen_output import Staged_Refrigeration_ScreenOutput


class Staged_Refrigeration_ScreenInput(BaseModel):
    """Input model for Staged_Refrigeration_ScreenModule.

    Attributes:
        T_green_in: T_green_in input
        f_carnot_shield_in: f_carnot_shield_in input
        capital_mode_in: capital_mode_in input
        green_b_in: green_b_in input
        green_a_in: green_a_in input
        T_amb_in: T_amb_in input
        usd2015_to_2021_in: usd2015_to_2021_in input
        green_c_in: green_c_in input
        green_d_in: green_d_in input
        rating_cold_in: rating_cold_in input
        T_shield_in: T_shield_in input
        T_supply_in: T_supply_in input
        q_shield_in: q_shield_in input
        eta_mode_in: eta_mode_in input
        eta_const_in: eta_const_in input
        q_cold_in: q_cold_in input
    """
    T_green_in: float = Field(..., description="T_green_in input")
    f_carnot_shield_in: float = Field(..., description="f_carnot_shield_in input")
    capital_mode_in: float = Field(..., description="capital_mode_in input")
    green_b_in: float = Field(..., description="green_b_in input")
    green_a_in: float = Field(..., description="green_a_in input")
    T_amb_in: float = Field(..., description="T_amb_in input")
    usd2015_to_2021_in: float = Field(..., description="usd2015_to_2021_in input")
    green_c_in: float = Field(..., description="green_c_in input")
    green_d_in: float = Field(..., description="green_d_in input")
    rating_cold_in: float = Field(..., description="rating_cold_in input")
    T_shield_in: float = Field(..., description="T_shield_in input")
    T_supply_in: float = Field(..., description="T_supply_in input")
    q_shield_in: float = Field(..., description="q_shield_in input")
    eta_mode_in: float = Field(..., description="eta_mode_in input")
    eta_const_in: float = Field(..., description="eta_const_in input")
    q_cold_in: float = Field(..., description="q_cold_in input")


class Staged_Refrigeration_ScreenModule(ModuleBase[Staged_Refrigeration_ScreenInput, Staged_Refrigeration_ScreenOutput]):
    """TEAx module for Staged_Refrigeration_Screen calculation.

Electrical demand and capital of the installed two-stage refrigerator, and the installed cold-stage rating compared with the calculated cold load. carnot = (T_amb - T_supply)/T_supply; carnot_ref = (T_amb - T_green)/T_green; equiv_factor = carnot/carnot_ref; R_equiv_kW = rating_cold/1000*(equiv_factor if capital_mode = 0, else 1); eta_cold = green_a*R_eta^green_b with R_eta = rating_cold/1000 (eta_mode 0) or rating_cold/1000*equiv_factor (eta_mode 2), or eta_const (eta_mode 1); p_in_cold = q_cold*carnot/eta_cold; p_in_shield = q_shield*(T_amb - T_shield)/T_shield/f_carnot_shield; p_in_total_MW = (p_in_cold + p_in_shield)/1e6; refrigerator_capital = green_c*R_equiv_kW^green_d*usd2015_to_2021. Efficiency is a property of the installed plant evaluated at its rating and applied to the operating load (part-load penalty not modeled). capacity_margin = rating_cold - q_cold; capacity_pass = 1 when >= 0. green_extrapolated = 1 when R_equiv_kW, or R_eta when a Green efficiency mode is active, lies outside Green's fitted data [0.01, 35] kW. **Source**: knowledge/sources/green_2015_cost_of_coolers_at_4_2_20_40_and_77_k_publisher/; knowledge/sources/strobridge_1974_cryogenic_refrigerators_an_updated_survey/ **Reference**: Green 2015 Eq. 1 and Eq. 2, printed p.2 (PDF p.3); Strobridge 1974 Eq. 1 (printed p.2), Fig. 1 and pp.4-6 (percent of Carnot independent of temperature band); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.6; contract section 6. **Basis**: [AGENT] one efficiency law for both temperatures at the installed capacity; 20 K capital by input-power equivalence (factor (300-20)/20 / ((300-4.5)/4.5) = 0.2132) per check-rebco-cryo-cost.md Recheck r2. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/staged_refrigeration_screen_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - T_green_in: T_green_in parameter
    - f_carnot_shield_in: f_carnot_shield_in parameter
    - capital_mode_in: capital_mode_in parameter
    - green_b_in: green_b_in parameter
    - green_a_in: green_a_in parameter
    - T_amb_in: T_amb_in parameter
    - usd2015_to_2021_in: usd2015_to_2021_in parameter
    - green_c_in: green_c_in parameter
    - green_d_in: green_d_in parameter
    - rating_cold_in: rating_cold_in parameter
    - T_shield_in: T_shield_in parameter
    - T_supply_in: T_supply_in parameter
    - q_shield_in: q_shield_in parameter
    - eta_mode_in: eta_mode_in parameter
    - eta_const_in: eta_const_in parameter
    - q_cold_in: q_cold_in parameter

Outputs:
    - p_in_total_MW: p_in_total_MW result
    - eta_cold: eta_cold result
    - green_extrapolated: green_extrapolated result
    - R_equiv_kW: R_equiv_kW result
    - refrigerator_capital: refrigerator_capital result
    - carnot_specific_power: carnot_specific_power result
    - p_in_cold: p_in_cold result
    - capacity_pass: capacity_pass result
    - capacity_margin: capacity_margin result
    - p_in_shield: p_in_shield result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:203

    SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:203

    Calculation Specification:
        q_cold_in = 0.0
        T_supply_in = 0.0
        q_shield_in = 0.0
        T_shield_in = 0.0
        T_amb_in = 0.0
        rating_cold_in = 0.0
        eta_mode_in = 0.0
        eta_const_in = 0.0
        green_a_in = 0.0
        green_b_in = 0.0
        f_carnot_shield_in = 1.0
        capital_mode_in = 0.0
        green_c_in = 0.0
        green_d_in = 0.0
        T_green_in = 0.0
        usd2015_to_2021_in = 1.0
        
Documentation:
Electrical demand and capital of the installed two-stage refrigerator, and the installed cold-stage rating compared with the calculated cold load. carnot = (T_amb - T_supply)/T_supply; carnot_ref = (T_amb - T_green)/T_green; equiv_factor = carnot/carnot_ref; R_equiv_kW = rating_cold/1000*(equiv_factor if capital_mode = 0, else 1); eta_cold = green_a*R_eta^green_b with R_eta = rating_cold/1000 (eta_mode 0) or rating_cold/1000*equiv_factor (eta_mode 2), or eta_const (eta_mode 1); p_in_cold = q_cold*carnot/eta_cold; p_in_shield = q_shield*(T_amb - T_shield)/T_shield/f_carnot_shield; p_in_total_MW = (p_in_cold + p_in_shield)/1e6; refrigerator_capital = green_c*R_equiv_kW^green_d*usd2015_to_2021. Efficiency is a property of the installed plant evaluated at its rating and applied to the operating load (part-load penalty not modeled). capacity_margin = rating_cold - q_cold; capacity_pass = 1 when >= 0. green_extrapolated = 1 when R_equiv_kW, or R_eta when a Green efficiency mode is active, lies outside Green's fitted data [0.01, 35] kW. **Source**: knowledge/sources/green_2015_cost_of_coolers_at_4_2_20_40_and_77_k_publisher/; knowledge/sources/strobridge_1974_cryogenic_refrigerators_an_updated_survey/ **Reference**: Green 2015 Eq. 1 and Eq. 2, printed p.2 (PDF p.3); Strobridge 1974 Eq. 1 (printed p.2), Fig. 1 and pp.4-6 (percent of Carnot independent of temperature band); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.6; contract section 6. **Basis**: [AGENT] one efficiency law for both temperatures at the installed capacity; 20 K capital by input-power equivalence (factor (300-20)/20 / ((300-4.5)/4.5) = 0.2132) per check-rebco-cryo-cost.md Recheck r2. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/staged_refrigeration_screen_impl.py. **Last Updated**: 2026-09-29

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.magnet_conductor_alternatives.staged_refrigeration_screen_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts p_in_total_MW, eta_cold, green_extrapolated, R_equiv_kW, refrigerator_capital, carnot_specific_power, p_in_cold, capacity_pass, capacity_margin, p_in_shield fields to separate channels.
    """

    name: str = "Staged_Refrigeration_ScreenModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, T_green_in: float, f_carnot_shield_in: float, capital_mode_in: float, green_b_in: float, green_a_in: float, T_amb_in: float, usd2015_to_2021_in: float, green_c_in: float, green_d_in: float, rating_cold_in: float, T_shield_in: float, T_supply_in: float, q_shield_in: float, eta_mode_in: float, eta_const_in: float, q_cold_in: float    ) -> Staged_Refrigeration_ScreenInput:
        """Validate inputs and fill defaults.

        Args:
            T_green_in: T_green_in input
            f_carnot_shield_in: f_carnot_shield_in input
            capital_mode_in: capital_mode_in input
            green_b_in: green_b_in input
            green_a_in: green_a_in input
            T_amb_in: T_amb_in input
            usd2015_to_2021_in: usd2015_to_2021_in input
            green_c_in: green_c_in input
            green_d_in: green_d_in input
            rating_cold_in: rating_cold_in input
            T_shield_in: T_shield_in input
            T_supply_in: T_supply_in input
            q_shield_in: q_shield_in input
            eta_mode_in: eta_mode_in input
            eta_const_in: eta_const_in input
            q_cold_in: q_cold_in input

        Returns:
            Validated input model
        """
        return Staged_Refrigeration_ScreenInput(T_green_in=T_green_in, f_carnot_shield_in=f_carnot_shield_in, capital_mode_in=capital_mode_in, green_b_in=green_b_in, green_a_in=green_a_in, T_amb_in=T_amb_in, usd2015_to_2021_in=usd2015_to_2021_in, green_c_in=green_c_in, green_d_in=green_d_in, rating_cold_in=rating_cold_in, T_shield_in=T_shield_in, T_supply_in=T_supply_in, q_shield_in=q_shield_in, eta_mode_in=eta_mode_in, eta_const_in=eta_const_in, q_cold_in=q_cold_in)

    def run(
        self, T_green_in: float, f_carnot_shield_in: float, capital_mode_in: float, green_b_in: float, green_a_in: float, T_amb_in: float, usd2015_to_2021_in: float, green_c_in: float, green_d_in: float, rating_cold_in: float, T_shield_in: float, T_supply_in: float, q_shield_in: float, eta_mode_in: float, eta_const_in: float, q_cold_in: float    ) -> ModuleResult[Staged_Refrigeration_ScreenOutput]:
        """Execute calculation.

        Args:
            T_green_in: T_green_in input
            f_carnot_shield_in: f_carnot_shield_in input
            capital_mode_in: capital_mode_in input
            green_b_in: green_b_in input
            green_a_in: green_a_in input
            T_amb_in: T_amb_in input
            usd2015_to_2021_in: usd2015_to_2021_in input
            green_c_in: green_c_in input
            green_d_in: green_d_in input
            rating_cold_in: rating_cold_in input
            T_shield_in: T_shield_in input
            T_supply_in: T_supply_in input
            q_shield_in: q_shield_in input
            eta_mode_in: eta_mode_in input
            eta_const_in: eta_const_in input
            q_cold_in: q_cold_in input

        Returns:
            Module result with Staged_Refrigeration_ScreenOutput (p_in_total_MW, eta_cold, green_extrapolated, R_equiv_kW, refrigerator_capital, carnot_specific_power, p_in_cold, capacity_pass, capacity_margin, p_in_shield)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(T_green_in, f_carnot_shield_in, capital_mode_in, green_b_in, green_a_in, T_amb_in, usd2015_to_2021_in, green_c_in, green_d_in, rating_cold_in, T_shield_in, T_supply_in, q_shield_in, eta_mode_in, eta_const_in, q_cold_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.magnet_conductor_alternatives.staged_refrigeration_screen_impl import (
            run_staged_refrigeration_screen,
        )

        # Execute implementation - returns tuple of values
        p_in_total_MW, eta_cold, green_extrapolated, R_equiv_kW, refrigerator_capital, carnot_specific_power, p_in_cold, capacity_pass, capacity_margin, p_in_shield = run_staged_refrigeration_screen(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Staged_Refrigeration_ScreenOutput(
                p_in_total_MW=p_in_total_MW,
                eta_cold=eta_cold,
                green_extrapolated=green_extrapolated,
                R_equiv_kW=R_equiv_kW,
                refrigerator_capital=refrigerator_capital,
                carnot_specific_power=carnot_specific_power,
                p_in_cold=p_in_cold,
                capacity_pass=capacity_pass,
                capacity_margin=capacity_margin,
                p_in_shield=p_in_shield,
            )
        )
