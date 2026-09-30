from pydantic import Field
from simkit.config.schema import MultiOutput

class Staged_Refrigeration_ScreenOutput(MultiOutput):
    """Multi-output container for Staged_Refrigeration_Screen.

Electrical demand and capital of the installed two-stage refrigerator, and the installed cold-stage rating compared with the calculated cold load. carnot = (T_amb - T_supply)/T_supply; carnot_ref = (T_amb - T_green)/T_green; equiv_factor = carnot/carnot_ref; R_equiv_kW = rating_cold/1000*(equiv_factor if capital_mode = 0, else 1); eta_cold = green_a*R_eta^green_b with R_eta = rating_cold/1000 (eta_mode 0) or rating_cold/1000*equiv_factor (eta_mode 2), or eta_const (eta_mode 1); p_in_cold = q_cold*carnot/eta_cold; p_in_shield = q_shield*(T_amb - T_shield)/T_shield/f_carnot_shield; p_in_total_MW = (p_in_cold + p_in_shield)/1e6; refrigerator_capital = green_c*R_equiv_kW^green_d*usd2015_to_2021. Efficiency is a property of the installed plant evaluated at its rating and applied to the operating load (part-load penalty not modeled). capacity_margin = rating_cold - q_cold; capacity_pass = 1 when >= 0. green_extrapolated = 1 when R_equiv_kW, or R_eta when a Green efficiency mode is active, lies outside Green's fitted data [0.01, 35] kW. **Source**: knowledge/sources/green_2015_cost_of_coolers_at_4_2_20_40_and_77_k_publisher/; knowledge/sources/strobridge_1974_cryogenic_refrigerators_an_updated_survey/ **Reference**: Green 2015 Eq. 1 and Eq. 2, printed p.2 (PDF p.3); Strobridge 1974 Eq. 1 (printed p.2), Fig. 1 and pp.4-6 (percent of Carnot independent of temperature band); work/active/WI-099_magnet-conductor-alternatives/design.md section 2.6; contract section 6. **Basis**: [AGENT] one efficiency law for both temperatures at the installed capacity; 20 K capital by input-power equivalence (factor (300-20)/20 / ((300-4.5)/4.5) = 0.2132) per check-rebco-cryo-cost.md Recheck r2. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/staged_refrigeration_screen_impl.py. **Last Updated**: 2026-09-29

SysML Source: root-0/magnet_conductor_alternatives.sysml:203
    """
    p_in_total_MW: float = Field(description="p_in_total_MW output")
    eta_cold: float = Field(description="eta_cold output")
    green_extrapolated: float = Field(description="green_extrapolated output")
    R_equiv_kW: float = Field(description="R_equiv_kW output")
    refrigerator_capital: float = Field(description="refrigerator_capital output")
    carnot_specific_power: float = Field(description="carnot_specific_power output")
    p_in_cold: float = Field(description="p_in_cold output")
    capacity_pass: float = Field(description="capacity_pass output")
    capacity_margin: float = Field(description="capacity_margin output")
    p_in_shield: float = Field(description="p_in_shield output")
