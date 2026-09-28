"""Cooling_Equipment_With_Selected_Salt_Pump_CountModule Module Wrapper

TEAx module for Cooling_Equipment_With_Selected_Salt_Pump_Count calculation.

Conceptual helium/HITEC cooling equipment. WI-096 additive variant: independently chosen salt_pumps_per_circuit_in replaces the original two salt pumps per circuit; primary machines remain two per circuit. Source: work/active/WI-096_matched-conversion-subsystems/design.md sections 4 and 7; independent design release: work/orchestration/goals/design-study-component-alternatives/evidence/design-review-fourth-submission.md. Salt replacement purchase, installation and removal are exposed separately; total salt flow and installed total UA expose existing internal quantities for downstream bindings. WI-078: selected machine design-point pumping duty/pressure and salt flow/head/efficiencies price installed packages, spares and replacements independently of operating demand. The 50hp helium normalization is pumping duty, not motor nameplate. Purchased fluid stocks are supplied; required fill derives from represented volumes and operating density. Reserve targets are suggestions only. Signed represented-fill margins are purchased minus required kg; represented_fill_ok is their nonnegative conjunction, not complete inventory qualification. Off-design machine performance remains unqualified. Source: work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md and architecture-review-r2.md. Basis: approved MR-7 interpretation; unchanged source price correlations, fixed HX/pipe geometry and operating closures. Guarded manual completion implements the equations below; all costs are USD2025 annual-CPI purchasing-power proxies. This is a priced subset, with unpriced valves, supports, insulation, salt auxiliaries and conversion-side inventory. Pressure qualification and helium/salt machine technology transfers are unvalidated. Geometry and lifecycle assumptions are agent-selected scenarios.

Output basis: HX masses and duty per IHX; HX areas per IHX; salt_flow per circuit; all pipe and inventory quantities plant total; machine outputs per machine except counts.

Normative equations: two parallel primary machines, independently selected positive integer k salt machines and one fixed OB exchanger per circuit. BNL machine1978=550000*(0.5+0.5*(p_suction/(735*6894.757293168))*(shaft_W/745.6998715822702/50)^0.28); package=1.2*machine. Design fee130000 once. Installation=0.27*1.155*vendor; procurement services remain CAS30. Tube count14852, OD0.01905m, length11.6m; area=pi*OD*length*count. Tube mass=8000*area*t*(1-t/OD). Shell bore3.2m, length13m; annular shell and spherical pair of heads; two gross0.6m tubesheets; explicit accessory mass. Required area=(Q_IHX/N)/(UF*LMTD), UF=267.8e6/[area*(35-19.3)/ln(35/19.3)]. Hot/cold approaches are helium hot minus738.15K and suction minus543.15K.

Primary mains OD1.3/1.1m,65mm walls,50m each; nine branches per leg, ID=mainID/3,30mm wall, length=(4000/9-100)/18. Straight annular steel times(1+14440/66560) prices fittings. Secondary ID0.4m,20mm wall,50m each leg. All lengths scale with layout_multiplier. Delivered fabrication=stainless_fabrication_usd2017_per_kg_in (nominal310USD2017/kg); pipe field labor=0.50*fabrication. HX installation=0.024 labor+0.002 material. Salt shell void=pi*1.6^2*11.6-tube_outer_volume-accessory_mass/8000. Inventory volume is pipe+shell void only; cold density gives required fill; times(1+reserve) gives an optional target. Purchased mass is independently supplied. Helium volume=pipe+61.5*N, pressure discharge, arithmetic-mean hot/suction temperature, ideal gas R=cp*(gamma-1)/gamma, supplies the required fill diagnostic. Standard volume uses101325Pa/288.15K;14USD2024/m3. Source879m3/9circuit check is independent, never an added inventory.

Salt cp1560, density=max(2080-0.733*T_C,1000), viscosity=max(0.00622-1.02e-5*T_C,1e-6). Flow=Q_IHX*1e6/(1560*195); k pumps/circuit; per-machine flow=total_flow/(k*N), shaft=total_shaft/(k*N), electricity=total_electric/(k*N). Active salt vendor purchase=k*N*selected_machine_package; one plant spare is unchanged. Salt replacement purchase=active salt vendor purchase; installation=0.27*1.155*purchase; removal=removal_multiplier*installation. Shaft=mdot*g*head/eta_p; electric=shaft/eta_motor. Pump CE500=3*exp(9.7171-0.6019*ln(S)+0.0519*ln(S)^2), S=Qgpm*sqrt(Hft). TEFC motor CE500=1.3*exp(5.8259+0.13141*l+0.053255*l^2+0.028628*l^3-0.0035549*l^4), l=ln(electric_hp). Pump domains S400..100000; type50..3500gpm,50..200ft,<=200shaft hp; motor base1..700hp, factor1..250hp. Salt pump installation repeats0.27*1.155. Straight losses sum f*L/D*v^2/(2g); f64/Re below2300, smooth Haaland(-1.8log10(6.9/Re))^-2 otherwise; transitional2300..4000 is flagged. Saltprice0=1.23USD2011/kg;1=2.53USD2021/kg; bulk category >=10millionkg.

CPI1978=65.2,2006=201.6,2011=224.9,2017=245.1,2021=271.0,2024=313.7,2025=321.9. All prices multiply321.9/sourceCPI and costscale. One uninstalled spare of each machine per plant. Machine replacement repeats active purchases+installation+removal_multiplier*installation; bundle replacement repeats tube+accessory fabrication plus0.026 installation and0.024*removal_multiplier. Events k*life<years, discounted(1+r)^(-time), annualized r/(1-(1+r)^(-years)) or1/years at zero rate. Makeup=chosen initial inventory cost*makeup_fraction. Delivered exclusion=active primary packages+primary spare+HX+both pipe fabrication bills; no installation, design fee, inventory, salt pumps or future replacement. Installed total=purchased total+installation total. Seven child costs sum installed total. Sourcefitargument above465C fails physical-interface screen.

Disabled returns finite zeros before active guards. Active requires finite numeric inputs, positive flows/temperatures/dimensions/lives, integer n_loops, positive integer salt_pumps_per_circuit_in and n_mod=1, gamma>1,0<efficiencies<=1, shaft<=electric, tube wall<OD/2, suction pressure>0, positive terminal approaches and shell void; invalid arithmetic inputs raise ValueError. Range/capacity failures return false diagnostics with evaluable extrapolated prices.

*Source**: BNL helium quote; ANL2018 cost algorithms; Seider2009 third edition Chapter22; NETL2002; ORNL installation; EU DEMO OB geometry; NREL SSC properties; INL2022 inventory; USGS2025 helium; annual CPI.
*Reference**: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md (released corrective details); primary-candidate.md; work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/secondary-methods.md; evidence/round2/hx-method-check.md. These records link screened registered originals and exact source locations.
*Last Updated**: 2026-09-26

Inputs:
    - helium_purchased_mass_kg_in: helium_purchased_mass_kg_in parameter
    - salt_purchased_mass_kg_in: salt_purchased_mass_kg_in parameter
    - layout_multiplier_in: layout_multiplier_in parameter
    - primary_electric_MW_in: primary_electric_MW_in parameter
    - salt_design_eta_motor_in: salt_design_eta_motor_in parameter
    - shell_wall_in: shell_wall_in parameter
    - q_ihx_MW_in: q_ihx_MW_in parameter
    - helium_suction_K_in: helium_suction_K_in parameter
    - makeup_fraction_in: makeup_fraction_in parameter
    - n_mod_in: n_mod_in parameter
    - helium_design_suction_Pa_in: helium_design_suction_Pa_in parameter
    - dp_loop_in: dp_loop_in parameter
    - eta_p_in: eta_p_in parameter
    - bundle_life_in: bundle_life_in parameter
    - eta_motor_in: eta_motor_in parameter
    - stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
    - costscale_in: costscale_in parameter
    - saltprice_source_choice_in: saltprice_source_choice_in parameter
    - n_loops_in: n_loops_in parameter
    - tube_wall_in: tube_wall_in parameter
    - enabled_in: enabled_in parameter
    - helium_hot_K_in: helium_hot_K_in parameter
    - salt_design_head_m_in: salt_design_head_m_in parameter
    - primary_shaft_MW_in: primary_shaft_MW_in parameter
    - discount_in: discount_in parameter
    - mdot_loop_in: mdot_loop_in parameter
    - helium_gamma_in: helium_gamma_in parameter
    - inventory_reserve_in: inventory_reserve_in parameter
    - accessory_mass_in: accessory_mass_in parameter
    - years_in: years_in parameter
    - helium_cp_in: helium_cp_in parameter
    - secondary_head_in: secondary_head_in parameter
    - salt_design_flow_kg_s_in: salt_design_flow_kg_s_in parameter
    - salt_design_eta_p_in: salt_design_eta_p_in parameter
    - helium_design_shaft_MW_in: helium_design_shaft_MW_in parameter
    - removal_multiplier_in: removal_multiplier_in parameter
    - helium_discharge_Pa_in: helium_discharge_Pa_in parameter
    - salt_pumps_per_circuit_in: salt_pumps_per_circuit_in parameter
    - machine_life_in: machine_life_in parameter
    - sourcefitargument_C_in: sourcefitargument_C_in parameter

Outputs:
    - salt_electric_MW: salt_electric_MW result
    - ihx_cold_approach: ihx_cold_approach result
    - primary_pipe_installation: primary_pipe_installation result
    - salt_represented_fill_margin_kg: salt_represented_fill_margin_kg result
    - design_pump_type_ok: design_pump_type_ok result
    - cycle_temperature_gap: cycle_temperature_gap result
    - salt_makeup_annual: salt_makeup_annual result
    - primary_circulators_cost: primary_circulators_cost result
    - helium_price_year: helium_price_year result
    - salt_flow_regime_ok: salt_flow_regime_ok result
    - circulator_shaft_MW: circulator_shaft_MW result
    - helium_hx_volume: helium_hx_volume result
    - pressure_qualified: pressure_qualified result
    - hx_tube_length: hx_tube_length result
    - salt_unit_price: salt_unit_price result
    - secondary_pipe_installation: secondary_pipe_installation result
    - secondary_installation: secondary_installation result
    - pump_size_ok: pump_size_ok result
    - secondary_pumps_cost: secondary_pumps_cost result
    - shell_mass: shell_mass result
    - bundle_event_removal: bundle_event_removal result
    - salt_inventory_target_mass_kg: salt_inventory_target_mass_kg result
    - total_salt_flow_kg_s: total_salt_flow_kg_s result
    - secondary_pipe_mass: secondary_pipe_mass result
    - circulator_electric_MW: circulator_electric_MW result
    - primary_piping_cost: primary_piping_cost result
    - salt_expansion_ratio: salt_expansion_ratio result
    - salt_hx_volume: salt_hx_volume result
    - inventory_complete: inventory_complete result
    - pump_type_ok: pump_type_ok result
    - salt_pump_transfer_validated: salt_pump_transfer_validated result
    - consumables_annual: consumables_annual result
    - sheets_mass: sheets_mass result
    - salt_flow: salt_flow result
    - helium_price_transfer_validated: helium_price_transfer_validated result
    - installed_total: installed_total result
    - machine_event_purchase: machine_event_purchase result
    - salt_velocity_hot: salt_velocity_hot result
    - helium_inventory_mass: helium_inventory_mass result
    - salt_machine_event_installation: salt_machine_event_installation result
    - pump_shaft_hp: pump_shaft_hp result
    - cycle_interface_ok: cycle_interface_ok result
    - salt_velocity_cold: salt_velocity_cold result
    - ihx_installed_area: ihx_installed_area result
    - motor_electric_hp: motor_electric_hp result
    - ihx_hot_approach: ihx_hot_approach result
    - pump_flow_gpm: pump_flow_gpm result
    - salt_pump_shaft_MW: salt_pump_shaft_MW result
    - salt_straight_loss: salt_straight_loss result
    - helium_required_fill_mass_kg: helium_required_fill_mass_kg result
    - salt_pipe_volume: salt_pipe_volume result
    - inventory_source_volume_ok: inventory_source_volume_ok result
    - design_motor_factor_ok: design_motor_factor_ok result
    - circulator_count: circulator_count result
    - ihx_required_area: ihx_required_area result
    - circulator_volume: circulator_volume result
    - ihx_capacity_margin_m2: ihx_capacity_margin_m2 result
    - helium_makeup_annual: helium_makeup_annual result
    - salt_design_shaft_MW: salt_design_shaft_MW result
    - ihx_count: ihx_count result
    - salt_head_remaining: salt_head_remaining result
    - inventory_cost: inventory_cost result
    - salt_Re_cold: salt_Re_cold result
    - circulator_flow: circulator_flow result
    - pump_size_factor: pump_size_factor result
    - helium_inventory_target_mass_kg: helium_inventory_target_mass_kg result
    - helium_design_suction_Pa: helium_design_suction_Pa result
    - salt_inventory_cost: salt_inventory_cost result
    - installed_total_UA_MW_K: installed_total_UA_MW_K result
    - motor_factor_ok: motor_factor_ok result
    - primary_pipe_purchase: primary_pipe_purchase result
    - salt_pump_count: salt_pump_count result
    - installation_total: installation_total result
    - primary_vendor: primary_vendor result
    - machine_event_removal: machine_event_removal result
    - secondary_spare: secondary_spare result
    - secondary_vendor: secondary_vendor result
    - design_pump_head_ft: design_pump_head_ft result
    - helium_standard_volume: helium_standard_volume result
    - bundle_event_installation: bundle_event_installation result
    - salt_required_fill_mass_kg: salt_required_fill_mass_kg result
    - salt_bulk_scale_ok: salt_bulk_scale_ok result
    - salt_inventory_volume: salt_inventory_volume result
    - salt_price_raw: salt_price_raw result
    - salt_head_ok: salt_head_ok result
    - primary_installation: primary_installation result
    - ihx_lmtd: ihx_lmtd result
    - salt_inventory_mass: salt_inventory_mass result
    - hx_mass: hx_mass result
    - salt_price_year: salt_price_year result
    - hx_purchase: hx_purchase result
    - secondary_piping_cost: secondary_piping_cost result
    - ihx_capacity_defined: ihx_capacity_defined result
    - helium_inventory_volume: helium_inventory_volume result
    - salt_Re_hot: salt_Re_hot result
    - design_motor_base_ok: design_motor_base_ok result
    - pump_head_ft: pump_head_ft result
    - salt_machine_event_removal: salt_machine_event_removal result
    - design_pump_size_factor: design_pump_size_factor result
    - salt_design_electric_MW: salt_design_electric_MW result
    - helium_inventory_cost: helium_inventory_cost result
    - source_volume_ratio: source_volume_ratio result
    - hx_shell_bore: hx_shell_bore result
    - salt_return_C: salt_return_C result
    - replacement_annual: replacement_annual result
    - ihx_duty_MW: ihx_duty_MW result
    - hx_shell_wall: hx_shell_wall result
    - primary_pipe_volume: primary_pipe_volume result
    - salt_machine_event_purchase: salt_machine_event_purchase result
    - circulator_suction_Pa: circulator_suction_Pa result
    - helium_design_shaft_MW: helium_design_shaft_MW result
    - bundle_mass: bundle_mass result
    - machine_off_design_performance_qualified: machine_off_design_performance_qualified result
    - bundle_event_purchase: bundle_event_purchase result
    - primary_design: primary_design result
    - represented_fill_defined: represented_fill_defined result
    - hx_installation: hx_installation result
    - helium_price_raw: helium_price_raw result
    - tube_mass: tube_mass result
    - conversion_heat_MW: conversion_heat_MW result
    - exchangers_cost: exchangers_cost result
    - design_pump_shaft_hp: design_pump_shaft_hp result
    - helium_represented_fill_margin_kg: helium_represented_fill_margin_kg result
    - design_pump_size_ok: design_pump_size_ok result
    - represented_fill_ok: represented_fill_ok result
    - secondary_pipe_purchase: secondary_pipe_purchase result
    - machine_events: machine_events result
    - spares_cost: spares_cost result
    - purchased_total: purchased_total result
    - machine_event_installation: machine_event_installation result
    - hx_shell_length: hx_shell_length result
    - bundle_events: bundle_events result
    - salt_design_flow_kg_s: salt_design_flow_kg_s result
    - salt_pump_flow: salt_pump_flow result
    - primary_spare: primary_spare result
    - design_pump_flow_gpm: design_pump_flow_gpm result
    - delivered_total: delivered_total result
    - ihx_capacity_ok: ihx_capacity_ok result
    - salt_shaft_MW: salt_shaft_MW result
    - design_motor_electric_hp: design_motor_electric_hp result
    - primary_pipe_mass: primary_pipe_mass result
    - salt_design_head_m: salt_design_head_m result
    - salt_pump_electric_MW: salt_pump_electric_MW result
    - motor_base_ok: motor_base_ok result
    - heads_mass: heads_mass result

SysML Source: root-0/cooling_equipment_selected_pumps.sysml:3

SysML Source: root-0/cooling_equipment_selected_pumps.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/cooling_equipment_selected_pumps/cooling_equipment_with_selected_salt_pump_count_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float
from component_alternatives_tea.schemas.cooling_equipment_with_selected_salt_pump_count_output import Cooling_Equipment_With_Selected_Salt_Pump_CountOutput


class Cooling_Equipment_With_Selected_Salt_Pump_CountInput(BaseModel):
    """Input model for Cooling_Equipment_With_Selected_Salt_Pump_CountModule.

    Attributes:
        helium_purchased_mass_kg_in: helium_purchased_mass_kg_in input
        salt_purchased_mass_kg_in: salt_purchased_mass_kg_in input
        layout_multiplier_in: layout_multiplier_in input
        primary_electric_MW_in: primary_electric_MW_in input
        salt_design_eta_motor_in: salt_design_eta_motor_in input
        shell_wall_in: shell_wall_in input
        q_ihx_MW_in: q_ihx_MW_in input
        helium_suction_K_in: helium_suction_K_in input
        makeup_fraction_in: makeup_fraction_in input
        n_mod_in: n_mod_in input
        helium_design_suction_Pa_in: helium_design_suction_Pa_in input
        dp_loop_in: dp_loop_in input
        eta_p_in: eta_p_in input
        bundle_life_in: bundle_life_in input
        eta_motor_in: eta_motor_in input
        stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
        costscale_in: costscale_in input
        saltprice_source_choice_in: saltprice_source_choice_in input
        n_loops_in: n_loops_in input
        tube_wall_in: tube_wall_in input
        enabled_in: enabled_in input
        helium_hot_K_in: helium_hot_K_in input
        salt_design_head_m_in: salt_design_head_m_in input
        primary_shaft_MW_in: primary_shaft_MW_in input
        discount_in: discount_in input
        mdot_loop_in: mdot_loop_in input
        helium_gamma_in: helium_gamma_in input
        inventory_reserve_in: inventory_reserve_in input
        accessory_mass_in: accessory_mass_in input
        years_in: years_in input
        helium_cp_in: helium_cp_in input
        secondary_head_in: secondary_head_in input
        salt_design_flow_kg_s_in: salt_design_flow_kg_s_in input
        salt_design_eta_p_in: salt_design_eta_p_in input
        helium_design_shaft_MW_in: helium_design_shaft_MW_in input
        removal_multiplier_in: removal_multiplier_in input
        helium_discharge_Pa_in: helium_discharge_Pa_in input
        salt_pumps_per_circuit_in: salt_pumps_per_circuit_in input
        machine_life_in: machine_life_in input
        sourcefitargument_C_in: sourcefitargument_C_in input
    """
    helium_purchased_mass_kg_in: float = Field(..., description="helium_purchased_mass_kg_in input")
    salt_purchased_mass_kg_in: float = Field(..., description="salt_purchased_mass_kg_in input")
    layout_multiplier_in: float = Field(..., description="layout_multiplier_in input")
    primary_electric_MW_in: float = Field(..., description="primary_electric_MW_in input")
    salt_design_eta_motor_in: float = Field(..., description="salt_design_eta_motor_in input")
    shell_wall_in: float = Field(..., description="shell_wall_in input")
    q_ihx_MW_in: float = Field(..., description="q_ihx_MW_in input")
    helium_suction_K_in: float = Field(..., description="helium_suction_K_in input")
    makeup_fraction_in: float = Field(..., description="makeup_fraction_in input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    helium_design_suction_Pa_in: float = Field(..., description="helium_design_suction_Pa_in input")
    dp_loop_in: float = Field(..., description="dp_loop_in input")
    eta_p_in: float = Field(..., description="eta_p_in input")
    bundle_life_in: float = Field(..., description="bundle_life_in input")
    eta_motor_in: float = Field(..., description="eta_motor_in input")
    stainless_fabrication_usd2017_per_kg_in: float = Field(..., description="*Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19")
    costscale_in: float = Field(..., description="costscale_in input")
    saltprice_source_choice_in: float = Field(..., description="saltprice_source_choice_in input")
    n_loops_in: float = Field(..., description="n_loops_in input")
    tube_wall_in: float = Field(..., description="tube_wall_in input")
    enabled_in: bool = Field(..., description="enabled_in input")
    helium_hot_K_in: float = Field(..., description="helium_hot_K_in input")
    salt_design_head_m_in: float = Field(..., description="salt_design_head_m_in input")
    primary_shaft_MW_in: float = Field(..., description="primary_shaft_MW_in input")
    discount_in: float = Field(..., description="discount_in input")
    mdot_loop_in: float = Field(..., description="mdot_loop_in input")
    helium_gamma_in: float = Field(..., description="helium_gamma_in input")
    inventory_reserve_in: float = Field(..., description="inventory_reserve_in input")
    accessory_mass_in: float = Field(..., description="accessory_mass_in input")
    years_in: float = Field(..., description="years_in input")
    helium_cp_in: float = Field(..., description="helium_cp_in input")
    secondary_head_in: float = Field(..., description="secondary_head_in input")
    salt_design_flow_kg_s_in: float = Field(..., description="salt_design_flow_kg_s_in input")
    salt_design_eta_p_in: float = Field(..., description="salt_design_eta_p_in input")
    helium_design_shaft_MW_in: float = Field(..., description="helium_design_shaft_MW_in input")
    removal_multiplier_in: float = Field(..., description="removal_multiplier_in input")
    helium_discharge_Pa_in: float = Field(..., description="helium_discharge_Pa_in input")
    salt_pumps_per_circuit_in: float = Field(..., description="salt_pumps_per_circuit_in input")
    machine_life_in: float = Field(..., description="machine_life_in input")
    sourcefitargument_C_in: float = Field(..., description="sourcefitargument_C_in input")


class Cooling_Equipment_With_Selected_Salt_Pump_CountModule(ModuleBase[Cooling_Equipment_With_Selected_Salt_Pump_CountInput, Cooling_Equipment_With_Selected_Salt_Pump_CountOutput]):
    """TEAx module for Cooling_Equipment_With_Selected_Salt_Pump_Count calculation.

Conceptual helium/HITEC cooling equipment. WI-096 additive variant: independently chosen salt_pumps_per_circuit_in replaces the original two salt pumps per circuit; primary machines remain two per circuit. Source: work/active/WI-096_matched-conversion-subsystems/design.md sections 4 and 7; independent design release: work/orchestration/goals/design-study-component-alternatives/evidence/design-review-fourth-submission.md. Salt replacement purchase, installation and removal are exposed separately; total salt flow and installed total UA expose existing internal quantities for downstream bindings. WI-078: selected machine design-point pumping duty/pressure and salt flow/head/efficiencies price installed packages, spares and replacements independently of operating demand. The 50hp helium normalization is pumping duty, not motor nameplate. Purchased fluid stocks are supplied; required fill derives from represented volumes and operating density. Reserve targets are suggestions only. Signed represented-fill margins are purchased minus required kg; represented_fill_ok is their nonnegative conjunction, not complete inventory qualification. Off-design machine performance remains unqualified. Source: work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md and architecture-review-r2.md. Basis: approved MR-7 interpretation; unchanged source price correlations, fixed HX/pipe geometry and operating closures. Guarded manual completion implements the equations below; all costs are USD2025 annual-CPI purchasing-power proxies. This is a priced subset, with unpriced valves, supports, insulation, salt auxiliaries and conversion-side inventory. Pressure qualification and helium/salt machine technology transfers are unvalidated. Geometry and lifecycle assumptions are agent-selected scenarios.

Output basis: HX masses and duty per IHX; HX areas per IHX; salt_flow per circuit; all pipe and inventory quantities plant total; machine outputs per machine except counts.

Normative equations: two parallel primary machines, independently selected positive integer k salt machines and one fixed OB exchanger per circuit. BNL machine1978=550000*(0.5+0.5*(p_suction/(735*6894.757293168))*(shaft_W/745.6998715822702/50)^0.28); package=1.2*machine. Design fee130000 once. Installation=0.27*1.155*vendor; procurement services remain CAS30. Tube count14852, OD0.01905m, length11.6m; area=pi*OD*length*count. Tube mass=8000*area*t*(1-t/OD). Shell bore3.2m, length13m; annular shell and spherical pair of heads; two gross0.6m tubesheets; explicit accessory mass. Required area=(Q_IHX/N)/(UF*LMTD), UF=267.8e6/[area*(35-19.3)/ln(35/19.3)]. Hot/cold approaches are helium hot minus738.15K and suction minus543.15K.

Primary mains OD1.3/1.1m,65mm walls,50m each; nine branches per leg, ID=mainID/3,30mm wall, length=(4000/9-100)/18. Straight annular steel times(1+14440/66560) prices fittings. Secondary ID0.4m,20mm wall,50m each leg. All lengths scale with layout_multiplier. Delivered fabrication=stainless_fabrication_usd2017_per_kg_in (nominal310USD2017/kg); pipe field labor=0.50*fabrication. HX installation=0.024 labor+0.002 material. Salt shell void=pi*1.6^2*11.6-tube_outer_volume-accessory_mass/8000. Inventory volume is pipe+shell void only; cold density gives required fill; times(1+reserve) gives an optional target. Purchased mass is independently supplied. Helium volume=pipe+61.5*N, pressure discharge, arithmetic-mean hot/suction temperature, ideal gas R=cp*(gamma-1)/gamma, supplies the required fill diagnostic. Standard volume uses101325Pa/288.15K;14USD2024/m3. Source879m3/9circuit check is independent, never an added inventory.

Salt cp1560, density=max(2080-0.733*T_C,1000), viscosity=max(0.00622-1.02e-5*T_C,1e-6). Flow=Q_IHX*1e6/(1560*195); k pumps/circuit; per-machine flow=total_flow/(k*N), shaft=total_shaft/(k*N), electricity=total_electric/(k*N). Active salt vendor purchase=k*N*selected_machine_package; one plant spare is unchanged. Salt replacement purchase=active salt vendor purchase; installation=0.27*1.155*purchase; removal=removal_multiplier*installation. Shaft=mdot*g*head/eta_p; electric=shaft/eta_motor. Pump CE500=3*exp(9.7171-0.6019*ln(S)+0.0519*ln(S)^2), S=Qgpm*sqrt(Hft). TEFC motor CE500=1.3*exp(5.8259+0.13141*l+0.053255*l^2+0.028628*l^3-0.0035549*l^4), l=ln(electric_hp). Pump domains S400..100000; type50..3500gpm,50..200ft,<=200shaft hp; motor base1..700hp, factor1..250hp. Salt pump installation repeats0.27*1.155. Straight losses sum f*L/D*v^2/(2g); f64/Re below2300, smooth Haaland(-1.8log10(6.9/Re))^-2 otherwise; transitional2300..4000 is flagged. Saltprice0=1.23USD2011/kg;1=2.53USD2021/kg; bulk category >=10millionkg.

CPI1978=65.2,2006=201.6,2011=224.9,2017=245.1,2021=271.0,2024=313.7,2025=321.9. All prices multiply321.9/sourceCPI and costscale. One uninstalled spare of each machine per plant. Machine replacement repeats active purchases+installation+removal_multiplier*installation; bundle replacement repeats tube+accessory fabrication plus0.026 installation and0.024*removal_multiplier. Events k*life<years, discounted(1+r)^(-time), annualized r/(1-(1+r)^(-years)) or1/years at zero rate. Makeup=chosen initial inventory cost*makeup_fraction. Delivered exclusion=active primary packages+primary spare+HX+both pipe fabrication bills; no installation, design fee, inventory, salt pumps or future replacement. Installed total=purchased total+installation total. Seven child costs sum installed total. Sourcefitargument above465C fails physical-interface screen.

Disabled returns finite zeros before active guards. Active requires finite numeric inputs, positive flows/temperatures/dimensions/lives, integer n_loops, positive integer salt_pumps_per_circuit_in and n_mod=1, gamma>1,0<efficiencies<=1, shaft<=electric, tube wall<OD/2, suction pressure>0, positive terminal approaches and shell void; invalid arithmetic inputs raise ValueError. Range/capacity failures return false diagnostics with evaluable extrapolated prices.

*Source**: BNL helium quote; ANL2018 cost algorithms; Seider2009 third edition Chapter22; NETL2002; ORNL installation; EU DEMO OB geometry; NREL SSC properties; INL2022 inventory; USGS2025 helium; annual CPI.
*Reference**: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md (released corrective details); primary-candidate.md; work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/secondary-methods.md; evidence/round2/hx-method-check.md. These records link screened registered originals and exact source locations.
*Last Updated**: 2026-09-26

Inputs:
    - helium_purchased_mass_kg_in: helium_purchased_mass_kg_in parameter
    - salt_purchased_mass_kg_in: salt_purchased_mass_kg_in parameter
    - layout_multiplier_in: layout_multiplier_in parameter
    - primary_electric_MW_in: primary_electric_MW_in parameter
    - salt_design_eta_motor_in: salt_design_eta_motor_in parameter
    - shell_wall_in: shell_wall_in parameter
    - q_ihx_MW_in: q_ihx_MW_in parameter
    - helium_suction_K_in: helium_suction_K_in parameter
    - makeup_fraction_in: makeup_fraction_in parameter
    - n_mod_in: n_mod_in parameter
    - helium_design_suction_Pa_in: helium_design_suction_Pa_in parameter
    - dp_loop_in: dp_loop_in parameter
    - eta_p_in: eta_p_in parameter
    - bundle_life_in: bundle_life_in parameter
    - eta_motor_in: eta_motor_in parameter
    - stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
    - costscale_in: costscale_in parameter
    - saltprice_source_choice_in: saltprice_source_choice_in parameter
    - n_loops_in: n_loops_in parameter
    - tube_wall_in: tube_wall_in parameter
    - enabled_in: enabled_in parameter
    - helium_hot_K_in: helium_hot_K_in parameter
    - salt_design_head_m_in: salt_design_head_m_in parameter
    - primary_shaft_MW_in: primary_shaft_MW_in parameter
    - discount_in: discount_in parameter
    - mdot_loop_in: mdot_loop_in parameter
    - helium_gamma_in: helium_gamma_in parameter
    - inventory_reserve_in: inventory_reserve_in parameter
    - accessory_mass_in: accessory_mass_in parameter
    - years_in: years_in parameter
    - helium_cp_in: helium_cp_in parameter
    - secondary_head_in: secondary_head_in parameter
    - salt_design_flow_kg_s_in: salt_design_flow_kg_s_in parameter
    - salt_design_eta_p_in: salt_design_eta_p_in parameter
    - helium_design_shaft_MW_in: helium_design_shaft_MW_in parameter
    - removal_multiplier_in: removal_multiplier_in parameter
    - helium_discharge_Pa_in: helium_discharge_Pa_in parameter
    - salt_pumps_per_circuit_in: salt_pumps_per_circuit_in parameter
    - machine_life_in: machine_life_in parameter
    - sourcefitargument_C_in: sourcefitargument_C_in parameter

Outputs:
    - salt_electric_MW: salt_electric_MW result
    - ihx_cold_approach: ihx_cold_approach result
    - primary_pipe_installation: primary_pipe_installation result
    - salt_represented_fill_margin_kg: salt_represented_fill_margin_kg result
    - design_pump_type_ok: design_pump_type_ok result
    - cycle_temperature_gap: cycle_temperature_gap result
    - salt_makeup_annual: salt_makeup_annual result
    - primary_circulators_cost: primary_circulators_cost result
    - helium_price_year: helium_price_year result
    - salt_flow_regime_ok: salt_flow_regime_ok result
    - circulator_shaft_MW: circulator_shaft_MW result
    - helium_hx_volume: helium_hx_volume result
    - pressure_qualified: pressure_qualified result
    - hx_tube_length: hx_tube_length result
    - salt_unit_price: salt_unit_price result
    - secondary_pipe_installation: secondary_pipe_installation result
    - secondary_installation: secondary_installation result
    - pump_size_ok: pump_size_ok result
    - secondary_pumps_cost: secondary_pumps_cost result
    - shell_mass: shell_mass result
    - bundle_event_removal: bundle_event_removal result
    - salt_inventory_target_mass_kg: salt_inventory_target_mass_kg result
    - total_salt_flow_kg_s: total_salt_flow_kg_s result
    - secondary_pipe_mass: secondary_pipe_mass result
    - circulator_electric_MW: circulator_electric_MW result
    - primary_piping_cost: primary_piping_cost result
    - salt_expansion_ratio: salt_expansion_ratio result
    - salt_hx_volume: salt_hx_volume result
    - inventory_complete: inventory_complete result
    - pump_type_ok: pump_type_ok result
    - salt_pump_transfer_validated: salt_pump_transfer_validated result
    - consumables_annual: consumables_annual result
    - sheets_mass: sheets_mass result
    - salt_flow: salt_flow result
    - helium_price_transfer_validated: helium_price_transfer_validated result
    - installed_total: installed_total result
    - machine_event_purchase: machine_event_purchase result
    - salt_velocity_hot: salt_velocity_hot result
    - helium_inventory_mass: helium_inventory_mass result
    - salt_machine_event_installation: salt_machine_event_installation result
    - pump_shaft_hp: pump_shaft_hp result
    - cycle_interface_ok: cycle_interface_ok result
    - salt_velocity_cold: salt_velocity_cold result
    - ihx_installed_area: ihx_installed_area result
    - motor_electric_hp: motor_electric_hp result
    - ihx_hot_approach: ihx_hot_approach result
    - pump_flow_gpm: pump_flow_gpm result
    - salt_pump_shaft_MW: salt_pump_shaft_MW result
    - salt_straight_loss: salt_straight_loss result
    - helium_required_fill_mass_kg: helium_required_fill_mass_kg result
    - salt_pipe_volume: salt_pipe_volume result
    - inventory_source_volume_ok: inventory_source_volume_ok result
    - design_motor_factor_ok: design_motor_factor_ok result
    - circulator_count: circulator_count result
    - ihx_required_area: ihx_required_area result
    - circulator_volume: circulator_volume result
    - ihx_capacity_margin_m2: ihx_capacity_margin_m2 result
    - helium_makeup_annual: helium_makeup_annual result
    - salt_design_shaft_MW: salt_design_shaft_MW result
    - ihx_count: ihx_count result
    - salt_head_remaining: salt_head_remaining result
    - inventory_cost: inventory_cost result
    - salt_Re_cold: salt_Re_cold result
    - circulator_flow: circulator_flow result
    - pump_size_factor: pump_size_factor result
    - helium_inventory_target_mass_kg: helium_inventory_target_mass_kg result
    - helium_design_suction_Pa: helium_design_suction_Pa result
    - salt_inventory_cost: salt_inventory_cost result
    - installed_total_UA_MW_K: installed_total_UA_MW_K result
    - motor_factor_ok: motor_factor_ok result
    - primary_pipe_purchase: primary_pipe_purchase result
    - salt_pump_count: salt_pump_count result
    - installation_total: installation_total result
    - primary_vendor: primary_vendor result
    - machine_event_removal: machine_event_removal result
    - secondary_spare: secondary_spare result
    - secondary_vendor: secondary_vendor result
    - design_pump_head_ft: design_pump_head_ft result
    - helium_standard_volume: helium_standard_volume result
    - bundle_event_installation: bundle_event_installation result
    - salt_required_fill_mass_kg: salt_required_fill_mass_kg result
    - salt_bulk_scale_ok: salt_bulk_scale_ok result
    - salt_inventory_volume: salt_inventory_volume result
    - salt_price_raw: salt_price_raw result
    - salt_head_ok: salt_head_ok result
    - primary_installation: primary_installation result
    - ihx_lmtd: ihx_lmtd result
    - salt_inventory_mass: salt_inventory_mass result
    - hx_mass: hx_mass result
    - salt_price_year: salt_price_year result
    - hx_purchase: hx_purchase result
    - secondary_piping_cost: secondary_piping_cost result
    - ihx_capacity_defined: ihx_capacity_defined result
    - helium_inventory_volume: helium_inventory_volume result
    - salt_Re_hot: salt_Re_hot result
    - design_motor_base_ok: design_motor_base_ok result
    - pump_head_ft: pump_head_ft result
    - salt_machine_event_removal: salt_machine_event_removal result
    - design_pump_size_factor: design_pump_size_factor result
    - salt_design_electric_MW: salt_design_electric_MW result
    - helium_inventory_cost: helium_inventory_cost result
    - source_volume_ratio: source_volume_ratio result
    - hx_shell_bore: hx_shell_bore result
    - salt_return_C: salt_return_C result
    - replacement_annual: replacement_annual result
    - ihx_duty_MW: ihx_duty_MW result
    - hx_shell_wall: hx_shell_wall result
    - primary_pipe_volume: primary_pipe_volume result
    - salt_machine_event_purchase: salt_machine_event_purchase result
    - circulator_suction_Pa: circulator_suction_Pa result
    - helium_design_shaft_MW: helium_design_shaft_MW result
    - bundle_mass: bundle_mass result
    - machine_off_design_performance_qualified: machine_off_design_performance_qualified result
    - bundle_event_purchase: bundle_event_purchase result
    - primary_design: primary_design result
    - represented_fill_defined: represented_fill_defined result
    - hx_installation: hx_installation result
    - helium_price_raw: helium_price_raw result
    - tube_mass: tube_mass result
    - conversion_heat_MW: conversion_heat_MW result
    - exchangers_cost: exchangers_cost result
    - design_pump_shaft_hp: design_pump_shaft_hp result
    - helium_represented_fill_margin_kg: helium_represented_fill_margin_kg result
    - design_pump_size_ok: design_pump_size_ok result
    - represented_fill_ok: represented_fill_ok result
    - secondary_pipe_purchase: secondary_pipe_purchase result
    - machine_events: machine_events result
    - spares_cost: spares_cost result
    - purchased_total: purchased_total result
    - machine_event_installation: machine_event_installation result
    - hx_shell_length: hx_shell_length result
    - bundle_events: bundle_events result
    - salt_design_flow_kg_s: salt_design_flow_kg_s result
    - salt_pump_flow: salt_pump_flow result
    - primary_spare: primary_spare result
    - design_pump_flow_gpm: design_pump_flow_gpm result
    - delivered_total: delivered_total result
    - ihx_capacity_ok: ihx_capacity_ok result
    - salt_shaft_MW: salt_shaft_MW result
    - design_motor_electric_hp: design_motor_electric_hp result
    - primary_pipe_mass: primary_pipe_mass result
    - salt_design_head_m: salt_design_head_m result
    - salt_pump_electric_MW: salt_pump_electric_MW result
    - motor_base_ok: motor_base_ok result
    - heads_mass: heads_mass result

SysML Source: root-0/cooling_equipment_selected_pumps.sysml:3

    SysML Source: root-0/cooling_equipment_selected_pumps.sysml:3

    Calculation Specification:
        enabled_in = false
        n_mod_in = 1
        n_loops_in = 18
        mdot_loop_in = 156.575
        dp_loop_in = 159300
        helium_suction_K_in = 567.221
        helium_discharge_Pa_in = 8000000.0
        helium_hot_K_in = 773.15
        helium_cp_in = 5193
        helium_gamma_in = 1.6666666666666667
        primary_shaft_MW_in = 86.7762
        primary_electric_MW_in = 86.7762
        q_ihx_MW_in = 3013.914942
        layout_multiplier_in = 1
        tube_wall_in = 0.0015
        shell_wall_in = 0.2
        accessory_mass_in = 10000
        secondary_head_in = 40
        eta_p_in = 0.75
        eta_motor_in = 0.95
        machine_life_in = 10
        bundle_life_in = 15
        years_in = 30
        discount_in = 0.07
        makeup_fraction_in = 0.001
        inventory_reserve_in = 0.1
        removal_multiplier_in = 1
        saltprice_source_choice_in = 0
        costscale_in = 1
        stainless_fabrication_usd2017_per_kg_in = 310
        sourcefitargument_C_in = 480
        
Documentation:
Conceptual helium/HITEC cooling equipment. WI-096 additive variant: independently chosen salt_pumps_per_circuit_in replaces the original two salt pumps per circuit; primary machines remain two per circuit. Source: work/active/WI-096_matched-conversion-subsystems/design.md sections 4 and 7; independent design release: work/orchestration/goals/design-study-component-alternatives/evidence/design-review-fourth-submission.md. Salt replacement purchase, installation and removal are exposed separately; total salt flow and installed total UA expose existing internal quantities for downstream bindings. WI-078: selected machine design-point pumping duty/pressure and salt flow/head/efficiencies price installed packages, spares and replacements independently of operating demand. The 50hp helium normalization is pumping duty, not motor nameplate. Purchased fluid stocks are supplied; required fill derives from represented volumes and operating density. Reserve targets are suggestions only. Signed represented-fill margins are purchased minus required kg; represented_fill_ok is their nonnegative conjunction, not complete inventory qualification. Off-design machine performance remains unqualified. Source: work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md and architecture-review-r2.md. Basis: approved MR-7 interpretation; unchanged source price correlations, fixed HX/pipe geometry and operating closures. Guarded manual completion implements the equations below; all costs are USD2025 annual-CPI purchasing-power proxies. This is a priced subset, with unpriced valves, supports, insulation, salt auxiliaries and conversion-side inventory. Pressure qualification and helium/salt machine technology transfers are unvalidated. Geometry and lifecycle assumptions are agent-selected scenarios.

Output basis: HX masses and duty per IHX; HX areas per IHX; salt_flow per circuit; all pipe and inventory quantities plant total; machine outputs per machine except counts.

Normative equations: two parallel primary machines, independently selected positive integer k salt machines and one fixed OB exchanger per circuit. BNL machine1978=550000*(0.5+0.5*(p_suction/(735*6894.757293168))*(shaft_W/745.6998715822702/50)^0.28); package=1.2*machine. Design fee130000 once. Installation=0.27*1.155*vendor; procurement services remain CAS30. Tube count14852, OD0.01905m, length11.6m; area=pi*OD*length*count. Tube mass=8000*area*t*(1-t/OD). Shell bore3.2m, length13m; annular shell and spherical pair of heads; two gross0.6m tubesheets; explicit accessory mass. Required area=(Q_IHX/N)/(UF*LMTD), UF=267.8e6/[area*(35-19.3)/ln(35/19.3)]. Hot/cold approaches are helium hot minus738.15K and suction minus543.15K.

Primary mains OD1.3/1.1m,65mm walls,50m each; nine branches per leg, ID=mainID/3,30mm wall, length=(4000/9-100)/18. Straight annular steel times(1+14440/66560) prices fittings. Secondary ID0.4m,20mm wall,50m each leg. All lengths scale with layout_multiplier. Delivered fabrication=stainless_fabrication_usd2017_per_kg_in (nominal310USD2017/kg); pipe field labor=0.50*fabrication. HX installation=0.024 labor+0.002 material. Salt shell void=pi*1.6^2*11.6-tube_outer_volume-accessory_mass/8000. Inventory volume is pipe+shell void only; cold density gives required fill; times(1+reserve) gives an optional target. Purchased mass is independently supplied. Helium volume=pipe+61.5*N, pressure discharge, arithmetic-mean hot/suction temperature, ideal gas R=cp*(gamma-1)/gamma, supplies the required fill diagnostic. Standard volume uses101325Pa/288.15K;14USD2024/m3. Source879m3/9circuit check is independent, never an added inventory.

Salt cp1560, density=max(2080-0.733*T_C,1000), viscosity=max(0.00622-1.02e-5*T_C,1e-6). Flow=Q_IHX*1e6/(1560*195); k pumps/circuit; per-machine flow=total_flow/(k*N), shaft=total_shaft/(k*N), electricity=total_electric/(k*N). Active salt vendor purchase=k*N*selected_machine_package; one plant spare is unchanged. Salt replacement purchase=active salt vendor purchase; installation=0.27*1.155*purchase; removal=removal_multiplier*installation. Shaft=mdot*g*head/eta_p; electric=shaft/eta_motor. Pump CE500=3*exp(9.7171-0.6019*ln(S)+0.0519*ln(S)^2), S=Qgpm*sqrt(Hft). TEFC motor CE500=1.3*exp(5.8259+0.13141*l+0.053255*l^2+0.028628*l^3-0.0035549*l^4), l=ln(electric_hp). Pump domains S400..100000; type50..3500gpm,50..200ft,<=200shaft hp; motor base1..700hp, factor1..250hp. Salt pump installation repeats0.27*1.155. Straight losses sum f*L/D*v^2/(2g); f64/Re below2300, smooth Haaland(-1.8log10(6.9/Re))^-2 otherwise; transitional2300..4000 is flagged. Saltprice0=1.23USD2011/kg;1=2.53USD2021/kg; bulk category >=10millionkg.

CPI1978=65.2,2006=201.6,2011=224.9,2017=245.1,2021=271.0,2024=313.7,2025=321.9. All prices multiply321.9/sourceCPI and costscale. One uninstalled spare of each machine per plant. Machine replacement repeats active purchases+installation+removal_multiplier*installation; bundle replacement repeats tube+accessory fabrication plus0.026 installation and0.024*removal_multiplier. Events k*life<years, discounted(1+r)^(-time), annualized r/(1-(1+r)^(-years)) or1/years at zero rate. Makeup=chosen initial inventory cost*makeup_fraction. Delivered exclusion=active primary packages+primary spare+HX+both pipe fabrication bills; no installation, design fee, inventory, salt pumps or future replacement. Installed total=purchased total+installation total. Seven child costs sum installed total. Sourcefitargument above465C fails physical-interface screen.

Disabled returns finite zeros before active guards. Active requires finite numeric inputs, positive flows/temperatures/dimensions/lives, integer n_loops, positive integer salt_pumps_per_circuit_in and n_mod=1, gamma>1,0<efficiencies<=1, shaft<=electric, tube wall<OD/2, suction pressure>0, positive terminal approaches and shell void; invalid arithmetic inputs raise ValueError. Range/capacity failures return false diagnostics with evaluable extrapolated prices.

*Source**: BNL helium quote; ANL2018 cost algorithms; Seider2009 third edition Chapter22; NETL2002; ORNL installation; EU DEMO OB geometry; NREL SSC properties; INL2022 inventory; USGS2025 helium; annual CPI.
*Reference**: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md (released corrective details); primary-candidate.md; work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/secondary-methods.md; evidence/round2/hx-method-check.md. These records link screened registered originals and exact source locations.
*Last Updated**: 2026-09-26

    IMPLEMENTATION: See component_alternatives_tea.handwritten.cooling_equipment_selected_pumps.cooling_equipment_with_selected_salt_pump_count_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts salt_electric_MW, ihx_cold_approach, primary_pipe_installation, salt_represented_fill_margin_kg, design_pump_type_ok, cycle_temperature_gap, salt_makeup_annual, primary_circulators_cost, helium_price_year, salt_flow_regime_ok, circulator_shaft_MW, helium_hx_volume, pressure_qualified, hx_tube_length, salt_unit_price, secondary_pipe_installation, secondary_installation, pump_size_ok, secondary_pumps_cost, shell_mass, bundle_event_removal, salt_inventory_target_mass_kg, total_salt_flow_kg_s, secondary_pipe_mass, circulator_electric_MW, primary_piping_cost, salt_expansion_ratio, salt_hx_volume, inventory_complete, pump_type_ok, salt_pump_transfer_validated, consumables_annual, sheets_mass, salt_flow, helium_price_transfer_validated, installed_total, machine_event_purchase, salt_velocity_hot, helium_inventory_mass, salt_machine_event_installation, pump_shaft_hp, cycle_interface_ok, salt_velocity_cold, ihx_installed_area, motor_electric_hp, ihx_hot_approach, pump_flow_gpm, salt_pump_shaft_MW, salt_straight_loss, helium_required_fill_mass_kg, salt_pipe_volume, inventory_source_volume_ok, design_motor_factor_ok, circulator_count, ihx_required_area, circulator_volume, ihx_capacity_margin_m2, helium_makeup_annual, salt_design_shaft_MW, ihx_count, salt_head_remaining, inventory_cost, salt_Re_cold, circulator_flow, pump_size_factor, helium_inventory_target_mass_kg, helium_design_suction_Pa, salt_inventory_cost, installed_total_UA_MW_K, motor_factor_ok, primary_pipe_purchase, salt_pump_count, installation_total, primary_vendor, machine_event_removal, secondary_spare, secondary_vendor, design_pump_head_ft, helium_standard_volume, bundle_event_installation, salt_required_fill_mass_kg, salt_bulk_scale_ok, salt_inventory_volume, salt_price_raw, salt_head_ok, primary_installation, ihx_lmtd, salt_inventory_mass, hx_mass, salt_price_year, hx_purchase, secondary_piping_cost, ihx_capacity_defined, helium_inventory_volume, salt_Re_hot, design_motor_base_ok, pump_head_ft, salt_machine_event_removal, design_pump_size_factor, salt_design_electric_MW, helium_inventory_cost, source_volume_ratio, hx_shell_bore, salt_return_C, replacement_annual, ihx_duty_MW, hx_shell_wall, primary_pipe_volume, salt_machine_event_purchase, circulator_suction_Pa, helium_design_shaft_MW, bundle_mass, machine_off_design_performance_qualified, bundle_event_purchase, primary_design, represented_fill_defined, hx_installation, helium_price_raw, tube_mass, conversion_heat_MW, exchangers_cost, design_pump_shaft_hp, helium_represented_fill_margin_kg, design_pump_size_ok, represented_fill_ok, secondary_pipe_purchase, machine_events, spares_cost, purchased_total, machine_event_installation, hx_shell_length, bundle_events, salt_design_flow_kg_s, salt_pump_flow, primary_spare, design_pump_flow_gpm, delivered_total, ihx_capacity_ok, salt_shaft_MW, design_motor_electric_hp, primary_pipe_mass, salt_design_head_m, salt_pump_electric_MW, motor_base_ok, heads_mass fields to separate channels.
    """

    name: str = "Cooling_Equipment_With_Selected_Salt_Pump_CountModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, helium_purchased_mass_kg_in: float, salt_purchased_mass_kg_in: float, layout_multiplier_in: float, primary_electric_MW_in: float, salt_design_eta_motor_in: float, shell_wall_in: float, q_ihx_MW_in: float, helium_suction_K_in: float, makeup_fraction_in: float, n_mod_in: float, helium_design_suction_Pa_in: float, dp_loop_in: float, eta_p_in: float, bundle_life_in: float, eta_motor_in: float, stainless_fabrication_usd2017_per_kg_in: float, costscale_in: float, saltprice_source_choice_in: float, n_loops_in: float, tube_wall_in: float, enabled_in: bool, helium_hot_K_in: float, salt_design_head_m_in: float, primary_shaft_MW_in: float, discount_in: float, mdot_loop_in: float, helium_gamma_in: float, inventory_reserve_in: float, accessory_mass_in: float, years_in: float, helium_cp_in: float, secondary_head_in: float, salt_design_flow_kg_s_in: float, salt_design_eta_p_in: float, helium_design_shaft_MW_in: float, removal_multiplier_in: float, helium_discharge_Pa_in: float, salt_pumps_per_circuit_in: float, machine_life_in: float, sourcefitargument_C_in: float    ) -> Cooling_Equipment_With_Selected_Salt_Pump_CountInput:
        """Validate inputs and fill defaults.

        Args:
            helium_purchased_mass_kg_in: helium_purchased_mass_kg_in input
            salt_purchased_mass_kg_in: salt_purchased_mass_kg_in input
            layout_multiplier_in: layout_multiplier_in input
            primary_electric_MW_in: primary_electric_MW_in input
            salt_design_eta_motor_in: salt_design_eta_motor_in input
            shell_wall_in: shell_wall_in input
            q_ihx_MW_in: q_ihx_MW_in input
            helium_suction_K_in: helium_suction_K_in input
            makeup_fraction_in: makeup_fraction_in input
            n_mod_in: n_mod_in input
            helium_design_suction_Pa_in: helium_design_suction_Pa_in input
            dp_loop_in: dp_loop_in input
            eta_p_in: eta_p_in input
            bundle_life_in: bundle_life_in input
            eta_motor_in: eta_motor_in input
            stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
            costscale_in: costscale_in input
            saltprice_source_choice_in: saltprice_source_choice_in input
            n_loops_in: n_loops_in input
            tube_wall_in: tube_wall_in input
            enabled_in: enabled_in input
            helium_hot_K_in: helium_hot_K_in input
            salt_design_head_m_in: salt_design_head_m_in input
            primary_shaft_MW_in: primary_shaft_MW_in input
            discount_in: discount_in input
            mdot_loop_in: mdot_loop_in input
            helium_gamma_in: helium_gamma_in input
            inventory_reserve_in: inventory_reserve_in input
            accessory_mass_in: accessory_mass_in input
            years_in: years_in input
            helium_cp_in: helium_cp_in input
            secondary_head_in: secondary_head_in input
            salt_design_flow_kg_s_in: salt_design_flow_kg_s_in input
            salt_design_eta_p_in: salt_design_eta_p_in input
            helium_design_shaft_MW_in: helium_design_shaft_MW_in input
            removal_multiplier_in: removal_multiplier_in input
            helium_discharge_Pa_in: helium_discharge_Pa_in input
            salt_pumps_per_circuit_in: salt_pumps_per_circuit_in input
            machine_life_in: machine_life_in input
            sourcefitargument_C_in: sourcefitargument_C_in input

        Returns:
            Validated input model
        """
        return Cooling_Equipment_With_Selected_Salt_Pump_CountInput(helium_purchased_mass_kg_in=helium_purchased_mass_kg_in, salt_purchased_mass_kg_in=salt_purchased_mass_kg_in, layout_multiplier_in=layout_multiplier_in, primary_electric_MW_in=primary_electric_MW_in, salt_design_eta_motor_in=salt_design_eta_motor_in, shell_wall_in=shell_wall_in, q_ihx_MW_in=q_ihx_MW_in, helium_suction_K_in=helium_suction_K_in, makeup_fraction_in=makeup_fraction_in, n_mod_in=n_mod_in, helium_design_suction_Pa_in=helium_design_suction_Pa_in, dp_loop_in=dp_loop_in, eta_p_in=eta_p_in, bundle_life_in=bundle_life_in, eta_motor_in=eta_motor_in, stainless_fabrication_usd2017_per_kg_in=stainless_fabrication_usd2017_per_kg_in, costscale_in=costscale_in, saltprice_source_choice_in=saltprice_source_choice_in, n_loops_in=n_loops_in, tube_wall_in=tube_wall_in, enabled_in=enabled_in, helium_hot_K_in=helium_hot_K_in, salt_design_head_m_in=salt_design_head_m_in, primary_shaft_MW_in=primary_shaft_MW_in, discount_in=discount_in, mdot_loop_in=mdot_loop_in, helium_gamma_in=helium_gamma_in, inventory_reserve_in=inventory_reserve_in, accessory_mass_in=accessory_mass_in, years_in=years_in, helium_cp_in=helium_cp_in, secondary_head_in=secondary_head_in, salt_design_flow_kg_s_in=salt_design_flow_kg_s_in, salt_design_eta_p_in=salt_design_eta_p_in, helium_design_shaft_MW_in=helium_design_shaft_MW_in, removal_multiplier_in=removal_multiplier_in, helium_discharge_Pa_in=helium_discharge_Pa_in, salt_pumps_per_circuit_in=salt_pumps_per_circuit_in, machine_life_in=machine_life_in, sourcefitargument_C_in=sourcefitargument_C_in)

    def run(
        self, helium_purchased_mass_kg_in: float, salt_purchased_mass_kg_in: float, layout_multiplier_in: float, primary_electric_MW_in: float, salt_design_eta_motor_in: float, shell_wall_in: float, q_ihx_MW_in: float, helium_suction_K_in: float, makeup_fraction_in: float, n_mod_in: float, helium_design_suction_Pa_in: float, dp_loop_in: float, eta_p_in: float, bundle_life_in: float, eta_motor_in: float, stainless_fabrication_usd2017_per_kg_in: float, costscale_in: float, saltprice_source_choice_in: float, n_loops_in: float, tube_wall_in: float, enabled_in: bool, helium_hot_K_in: float, salt_design_head_m_in: float, primary_shaft_MW_in: float, discount_in: float, mdot_loop_in: float, helium_gamma_in: float, inventory_reserve_in: float, accessory_mass_in: float, years_in: float, helium_cp_in: float, secondary_head_in: float, salt_design_flow_kg_s_in: float, salt_design_eta_p_in: float, helium_design_shaft_MW_in: float, removal_multiplier_in: float, helium_discharge_Pa_in: float, salt_pumps_per_circuit_in: float, machine_life_in: float, sourcefitargument_C_in: float    ) -> ModuleResult[Cooling_Equipment_With_Selected_Salt_Pump_CountOutput]:
        """Execute calculation.

        Args:
            helium_purchased_mass_kg_in: helium_purchased_mass_kg_in input
            salt_purchased_mass_kg_in: salt_purchased_mass_kg_in input
            layout_multiplier_in: layout_multiplier_in input
            primary_electric_MW_in: primary_electric_MW_in input
            salt_design_eta_motor_in: salt_design_eta_motor_in input
            shell_wall_in: shell_wall_in input
            q_ihx_MW_in: q_ihx_MW_in input
            helium_suction_K_in: helium_suction_K_in input
            makeup_fraction_in: makeup_fraction_in input
            n_mod_in: n_mod_in input
            helium_design_suction_Pa_in: helium_design_suction_Pa_in input
            dp_loop_in: dp_loop_in input
            eta_p_in: eta_p_in input
            bundle_life_in: bundle_life_in input
            eta_motor_in: eta_motor_in input
            stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
            costscale_in: costscale_in input
            saltprice_source_choice_in: saltprice_source_choice_in input
            n_loops_in: n_loops_in input
            tube_wall_in: tube_wall_in input
            enabled_in: enabled_in input
            helium_hot_K_in: helium_hot_K_in input
            salt_design_head_m_in: salt_design_head_m_in input
            primary_shaft_MW_in: primary_shaft_MW_in input
            discount_in: discount_in input
            mdot_loop_in: mdot_loop_in input
            helium_gamma_in: helium_gamma_in input
            inventory_reserve_in: inventory_reserve_in input
            accessory_mass_in: accessory_mass_in input
            years_in: years_in input
            helium_cp_in: helium_cp_in input
            secondary_head_in: secondary_head_in input
            salt_design_flow_kg_s_in: salt_design_flow_kg_s_in input
            salt_design_eta_p_in: salt_design_eta_p_in input
            helium_design_shaft_MW_in: helium_design_shaft_MW_in input
            removal_multiplier_in: removal_multiplier_in input
            helium_discharge_Pa_in: helium_discharge_Pa_in input
            salt_pumps_per_circuit_in: salt_pumps_per_circuit_in input
            machine_life_in: machine_life_in input
            sourcefitargument_C_in: sourcefitargument_C_in input

        Returns:
            Module result with Cooling_Equipment_With_Selected_Salt_Pump_CountOutput (salt_electric_MW, ihx_cold_approach, primary_pipe_installation, salt_represented_fill_margin_kg, design_pump_type_ok, cycle_temperature_gap, salt_makeup_annual, primary_circulators_cost, helium_price_year, salt_flow_regime_ok, circulator_shaft_MW, helium_hx_volume, pressure_qualified, hx_tube_length, salt_unit_price, secondary_pipe_installation, secondary_installation, pump_size_ok, secondary_pumps_cost, shell_mass, bundle_event_removal, salt_inventory_target_mass_kg, total_salt_flow_kg_s, secondary_pipe_mass, circulator_electric_MW, primary_piping_cost, salt_expansion_ratio, salt_hx_volume, inventory_complete, pump_type_ok, salt_pump_transfer_validated, consumables_annual, sheets_mass, salt_flow, helium_price_transfer_validated, installed_total, machine_event_purchase, salt_velocity_hot, helium_inventory_mass, salt_machine_event_installation, pump_shaft_hp, cycle_interface_ok, salt_velocity_cold, ihx_installed_area, motor_electric_hp, ihx_hot_approach, pump_flow_gpm, salt_pump_shaft_MW, salt_straight_loss, helium_required_fill_mass_kg, salt_pipe_volume, inventory_source_volume_ok, design_motor_factor_ok, circulator_count, ihx_required_area, circulator_volume, ihx_capacity_margin_m2, helium_makeup_annual, salt_design_shaft_MW, ihx_count, salt_head_remaining, inventory_cost, salt_Re_cold, circulator_flow, pump_size_factor, helium_inventory_target_mass_kg, helium_design_suction_Pa, salt_inventory_cost, installed_total_UA_MW_K, motor_factor_ok, primary_pipe_purchase, salt_pump_count, installation_total, primary_vendor, machine_event_removal, secondary_spare, secondary_vendor, design_pump_head_ft, helium_standard_volume, bundle_event_installation, salt_required_fill_mass_kg, salt_bulk_scale_ok, salt_inventory_volume, salt_price_raw, salt_head_ok, primary_installation, ihx_lmtd, salt_inventory_mass, hx_mass, salt_price_year, hx_purchase, secondary_piping_cost, ihx_capacity_defined, helium_inventory_volume, salt_Re_hot, design_motor_base_ok, pump_head_ft, salt_machine_event_removal, design_pump_size_factor, salt_design_electric_MW, helium_inventory_cost, source_volume_ratio, hx_shell_bore, salt_return_C, replacement_annual, ihx_duty_MW, hx_shell_wall, primary_pipe_volume, salt_machine_event_purchase, circulator_suction_Pa, helium_design_shaft_MW, bundle_mass, machine_off_design_performance_qualified, bundle_event_purchase, primary_design, represented_fill_defined, hx_installation, helium_price_raw, tube_mass, conversion_heat_MW, exchangers_cost, design_pump_shaft_hp, helium_represented_fill_margin_kg, design_pump_size_ok, represented_fill_ok, secondary_pipe_purchase, machine_events, spares_cost, purchased_total, machine_event_installation, hx_shell_length, bundle_events, salt_design_flow_kg_s, salt_pump_flow, primary_spare, design_pump_flow_gpm, delivered_total, ihx_capacity_ok, salt_shaft_MW, design_motor_electric_hp, primary_pipe_mass, salt_design_head_m, salt_pump_electric_MW, motor_base_ok, heads_mass)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(helium_purchased_mass_kg_in, salt_purchased_mass_kg_in, layout_multiplier_in, primary_electric_MW_in, salt_design_eta_motor_in, shell_wall_in, q_ihx_MW_in, helium_suction_K_in, makeup_fraction_in, n_mod_in, helium_design_suction_Pa_in, dp_loop_in, eta_p_in, bundle_life_in, eta_motor_in, stainless_fabrication_usd2017_per_kg_in, costscale_in, saltprice_source_choice_in, n_loops_in, tube_wall_in, enabled_in, helium_hot_K_in, salt_design_head_m_in, primary_shaft_MW_in, discount_in, mdot_loop_in, helium_gamma_in, inventory_reserve_in, accessory_mass_in, years_in, helium_cp_in, secondary_head_in, salt_design_flow_kg_s_in, salt_design_eta_p_in, helium_design_shaft_MW_in, removal_multiplier_in, helium_discharge_Pa_in, salt_pumps_per_circuit_in, machine_life_in, sourcefitargument_C_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.cooling_equipment_selected_pumps.cooling_equipment_with_selected_salt_pump_count_impl import (
            run_cooling_equipment_with_selected_salt_pump_count,
        )

        # Execute implementation - returns tuple of values
        salt_electric_MW, ihx_cold_approach, primary_pipe_installation, salt_represented_fill_margin_kg, design_pump_type_ok, cycle_temperature_gap, salt_makeup_annual, primary_circulators_cost, helium_price_year, salt_flow_regime_ok, circulator_shaft_MW, helium_hx_volume, pressure_qualified, hx_tube_length, salt_unit_price, secondary_pipe_installation, secondary_installation, pump_size_ok, secondary_pumps_cost, shell_mass, bundle_event_removal, salt_inventory_target_mass_kg, total_salt_flow_kg_s, secondary_pipe_mass, circulator_electric_MW, primary_piping_cost, salt_expansion_ratio, salt_hx_volume, inventory_complete, pump_type_ok, salt_pump_transfer_validated, consumables_annual, sheets_mass, salt_flow, helium_price_transfer_validated, installed_total, machine_event_purchase, salt_velocity_hot, helium_inventory_mass, salt_machine_event_installation, pump_shaft_hp, cycle_interface_ok, salt_velocity_cold, ihx_installed_area, motor_electric_hp, ihx_hot_approach, pump_flow_gpm, salt_pump_shaft_MW, salt_straight_loss, helium_required_fill_mass_kg, salt_pipe_volume, inventory_source_volume_ok, design_motor_factor_ok, circulator_count, ihx_required_area, circulator_volume, ihx_capacity_margin_m2, helium_makeup_annual, salt_design_shaft_MW, ihx_count, salt_head_remaining, inventory_cost, salt_Re_cold, circulator_flow, pump_size_factor, helium_inventory_target_mass_kg, helium_design_suction_Pa, salt_inventory_cost, installed_total_UA_MW_K, motor_factor_ok, primary_pipe_purchase, salt_pump_count, installation_total, primary_vendor, machine_event_removal, secondary_spare, secondary_vendor, design_pump_head_ft, helium_standard_volume, bundle_event_installation, salt_required_fill_mass_kg, salt_bulk_scale_ok, salt_inventory_volume, salt_price_raw, salt_head_ok, primary_installation, ihx_lmtd, salt_inventory_mass, hx_mass, salt_price_year, hx_purchase, secondary_piping_cost, ihx_capacity_defined, helium_inventory_volume, salt_Re_hot, design_motor_base_ok, pump_head_ft, salt_machine_event_removal, design_pump_size_factor, salt_design_electric_MW, helium_inventory_cost, source_volume_ratio, hx_shell_bore, salt_return_C, replacement_annual, ihx_duty_MW, hx_shell_wall, primary_pipe_volume, salt_machine_event_purchase, circulator_suction_Pa, helium_design_shaft_MW, bundle_mass, machine_off_design_performance_qualified, bundle_event_purchase, primary_design, represented_fill_defined, hx_installation, helium_price_raw, tube_mass, conversion_heat_MW, exchangers_cost, design_pump_shaft_hp, helium_represented_fill_margin_kg, design_pump_size_ok, represented_fill_ok, secondary_pipe_purchase, machine_events, spares_cost, purchased_total, machine_event_installation, hx_shell_length, bundle_events, salt_design_flow_kg_s, salt_pump_flow, primary_spare, design_pump_flow_gpm, delivered_total, ihx_capacity_ok, salt_shaft_MW, design_motor_electric_hp, primary_pipe_mass, salt_design_head_m, salt_pump_electric_MW, motor_base_ok, heads_mass = run_cooling_equipment_with_selected_salt_pump_count(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cooling_Equipment_With_Selected_Salt_Pump_CountOutput(
                salt_electric_MW=salt_electric_MW,
                ihx_cold_approach=ihx_cold_approach,
                primary_pipe_installation=primary_pipe_installation,
                salt_represented_fill_margin_kg=salt_represented_fill_margin_kg,
                design_pump_type_ok=design_pump_type_ok,
                cycle_temperature_gap=cycle_temperature_gap,
                salt_makeup_annual=salt_makeup_annual,
                primary_circulators_cost=primary_circulators_cost,
                helium_price_year=helium_price_year,
                salt_flow_regime_ok=salt_flow_regime_ok,
                circulator_shaft_MW=circulator_shaft_MW,
                helium_hx_volume=helium_hx_volume,
                pressure_qualified=pressure_qualified,
                hx_tube_length=hx_tube_length,
                salt_unit_price=salt_unit_price,
                secondary_pipe_installation=secondary_pipe_installation,
                secondary_installation=secondary_installation,
                pump_size_ok=pump_size_ok,
                secondary_pumps_cost=secondary_pumps_cost,
                shell_mass=shell_mass,
                bundle_event_removal=bundle_event_removal,
                salt_inventory_target_mass_kg=salt_inventory_target_mass_kg,
                total_salt_flow_kg_s=total_salt_flow_kg_s,
                secondary_pipe_mass=secondary_pipe_mass,
                circulator_electric_MW=circulator_electric_MW,
                primary_piping_cost=primary_piping_cost,
                salt_expansion_ratio=salt_expansion_ratio,
                salt_hx_volume=salt_hx_volume,
                inventory_complete=inventory_complete,
                pump_type_ok=pump_type_ok,
                salt_pump_transfer_validated=salt_pump_transfer_validated,
                consumables_annual=consumables_annual,
                sheets_mass=sheets_mass,
                salt_flow=salt_flow,
                helium_price_transfer_validated=helium_price_transfer_validated,
                installed_total=installed_total,
                machine_event_purchase=machine_event_purchase,
                salt_velocity_hot=salt_velocity_hot,
                helium_inventory_mass=helium_inventory_mass,
                salt_machine_event_installation=salt_machine_event_installation,
                pump_shaft_hp=pump_shaft_hp,
                cycle_interface_ok=cycle_interface_ok,
                salt_velocity_cold=salt_velocity_cold,
                ihx_installed_area=ihx_installed_area,
                motor_electric_hp=motor_electric_hp,
                ihx_hot_approach=ihx_hot_approach,
                pump_flow_gpm=pump_flow_gpm,
                salt_pump_shaft_MW=salt_pump_shaft_MW,
                salt_straight_loss=salt_straight_loss,
                helium_required_fill_mass_kg=helium_required_fill_mass_kg,
                salt_pipe_volume=salt_pipe_volume,
                inventory_source_volume_ok=inventory_source_volume_ok,
                design_motor_factor_ok=design_motor_factor_ok,
                circulator_count=circulator_count,
                ihx_required_area=ihx_required_area,
                circulator_volume=circulator_volume,
                ihx_capacity_margin_m2=ihx_capacity_margin_m2,
                helium_makeup_annual=helium_makeup_annual,
                salt_design_shaft_MW=salt_design_shaft_MW,
                ihx_count=ihx_count,
                salt_head_remaining=salt_head_remaining,
                inventory_cost=inventory_cost,
                salt_Re_cold=salt_Re_cold,
                circulator_flow=circulator_flow,
                pump_size_factor=pump_size_factor,
                helium_inventory_target_mass_kg=helium_inventory_target_mass_kg,
                helium_design_suction_Pa=helium_design_suction_Pa,
                salt_inventory_cost=salt_inventory_cost,
                installed_total_UA_MW_K=installed_total_UA_MW_K,
                motor_factor_ok=motor_factor_ok,
                primary_pipe_purchase=primary_pipe_purchase,
                salt_pump_count=salt_pump_count,
                installation_total=installation_total,
                primary_vendor=primary_vendor,
                machine_event_removal=machine_event_removal,
                secondary_spare=secondary_spare,
                secondary_vendor=secondary_vendor,
                design_pump_head_ft=design_pump_head_ft,
                helium_standard_volume=helium_standard_volume,
                bundle_event_installation=bundle_event_installation,
                salt_required_fill_mass_kg=salt_required_fill_mass_kg,
                salt_bulk_scale_ok=salt_bulk_scale_ok,
                salt_inventory_volume=salt_inventory_volume,
                salt_price_raw=salt_price_raw,
                salt_head_ok=salt_head_ok,
                primary_installation=primary_installation,
                ihx_lmtd=ihx_lmtd,
                salt_inventory_mass=salt_inventory_mass,
                hx_mass=hx_mass,
                salt_price_year=salt_price_year,
                hx_purchase=hx_purchase,
                secondary_piping_cost=secondary_piping_cost,
                ihx_capacity_defined=ihx_capacity_defined,
                helium_inventory_volume=helium_inventory_volume,
                salt_Re_hot=salt_Re_hot,
                design_motor_base_ok=design_motor_base_ok,
                pump_head_ft=pump_head_ft,
                salt_machine_event_removal=salt_machine_event_removal,
                design_pump_size_factor=design_pump_size_factor,
                salt_design_electric_MW=salt_design_electric_MW,
                helium_inventory_cost=helium_inventory_cost,
                source_volume_ratio=source_volume_ratio,
                hx_shell_bore=hx_shell_bore,
                salt_return_C=salt_return_C,
                replacement_annual=replacement_annual,
                ihx_duty_MW=ihx_duty_MW,
                hx_shell_wall=hx_shell_wall,
                primary_pipe_volume=primary_pipe_volume,
                salt_machine_event_purchase=salt_machine_event_purchase,
                circulator_suction_Pa=circulator_suction_Pa,
                helium_design_shaft_MW=helium_design_shaft_MW,
                bundle_mass=bundle_mass,
                machine_off_design_performance_qualified=machine_off_design_performance_qualified,
                bundle_event_purchase=bundle_event_purchase,
                primary_design=primary_design,
                represented_fill_defined=represented_fill_defined,
                hx_installation=hx_installation,
                helium_price_raw=helium_price_raw,
                tube_mass=tube_mass,
                conversion_heat_MW=conversion_heat_MW,
                exchangers_cost=exchangers_cost,
                design_pump_shaft_hp=design_pump_shaft_hp,
                helium_represented_fill_margin_kg=helium_represented_fill_margin_kg,
                design_pump_size_ok=design_pump_size_ok,
                represented_fill_ok=represented_fill_ok,
                secondary_pipe_purchase=secondary_pipe_purchase,
                machine_events=machine_events,
                spares_cost=spares_cost,
                purchased_total=purchased_total,
                machine_event_installation=machine_event_installation,
                hx_shell_length=hx_shell_length,
                bundle_events=bundle_events,
                salt_design_flow_kg_s=salt_design_flow_kg_s,
                salt_pump_flow=salt_pump_flow,
                primary_spare=primary_spare,
                design_pump_flow_gpm=design_pump_flow_gpm,
                delivered_total=delivered_total,
                ihx_capacity_ok=ihx_capacity_ok,
                salt_shaft_MW=salt_shaft_MW,
                design_motor_electric_hp=design_motor_electric_hp,
                primary_pipe_mass=primary_pipe_mass,
                salt_design_head_m=salt_design_head_m,
                salt_pump_electric_MW=salt_pump_electric_MW,
                motor_base_ok=motor_base_ok,
                heads_mass=heads_mass,
            )
        )
