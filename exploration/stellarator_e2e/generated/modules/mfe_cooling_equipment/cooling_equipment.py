"""Cooling_EquipmentModule Module Wrapper

TEAx module for Cooling_Equipment calculation.

Conceptual helium/HITEC cooling equipment. WI-078: selected machine design-point pumping duty/pressure and salt flow/head/efficiencies price installed packages, spares and replacements independently of operating demand. The 50hp helium normalization is pumping duty, not motor nameplate. Purchased fluid stocks are supplied; required fill derives from represented volumes and operating density. Reserve targets are suggestions only. Signed represented-fill margins are purchased minus required kg; represented_fill_ok is their nonnegative conjunction, not complete inventory qualification. Off-design machine performance remains unqualified. Source: work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md and architecture-review-r2.md. Basis: approved MR-7 interpretation; unchanged source price correlations, fixed HX/pipe geometry and operating closures. Guarded manual completion implements the equations below; all costs are USD2025 annual-CPI purchasing-power proxies. This is a priced subset, with unpriced valves, supports, insulation, salt auxiliaries and conversion-side inventory. Pressure qualification and helium/salt machine technology transfers are unvalidated. Geometry and lifecycle assumptions are agent-selected scenarios.

Output basis: HX masses and duty per IHX; HX areas per IHX; salt_flow per circuit; all pipe and inventory quantities plant total; machine outputs per machine except counts.

Normative equations: two parallel machines and one fixed OB exchanger per circuit. BNL machine1978=550000*(0.5+0.5*(p_suction/(735*6894.757293168))*(shaft_W/745.6998715822702/50)^0.28); package=1.2*machine. Design fee130000 once. Installation=0.27*1.155*vendor; procurement services remain CAS30. Tube count14852, OD0.01905m, length11.6m; area=pi*OD*length*count. Tube mass=8000*area*t*(1-t/OD). Shell bore3.2m, length13m; annular shell and spherical pair of heads; two gross0.6m tubesheets; explicit accessory mass. Required area=(Q_IHX/N)/(UF*LMTD), UF=267.8e6/[area*(35-19.3)/ln(35/19.3)]. Hot/cold approaches are helium hot minus738.15K and suction minus543.15K.

Primary mains OD1.3/1.1m,65mm walls,50m each; nine branches per leg, ID=mainID/3,30mm wall, length=(4000/9-100)/18. Straight annular steel times(1+14440/66560) prices fittings. Secondary ID0.4m,20mm wall,50m each leg. All lengths scale with layout_multiplier. Delivered fabrication=stainless_fabrication_usd2017_per_kg_in (nominal310USD2017/kg); pipe field labor=0.50*fabrication. HX installation=0.024 labor+0.002 material. Salt shell void=pi*1.6^2*11.6-tube_outer_volume-accessory_mass/8000. Inventory volume is pipe+shell void only; cold density gives required fill; times(1+reserve) gives an optional target. Purchased mass is independently supplied. Helium volume=pipe+61.5*N, pressure discharge, arithmetic-mean hot/suction temperature, ideal gas R=cp*(gamma-1)/gamma, supplies the required fill diagnostic. Standard volume uses101325Pa/288.15K;14USD2024/m3. Source879m3/9circuit check is independent, never an added inventory.

Salt cp1560, density=max(2080-0.733*T_C,1000), viscosity=max(0.00622-1.02e-5*T_C,1e-6). Flow=Q_IHX*1e6/(1560*195); two pumps/circuit. Shaft=mdot*g*head/eta_p; electric=shaft/eta_motor. Pump CE500=3*exp(9.7171-0.6019*ln(S)+0.0519*ln(S)^2), S=Qgpm*sqrt(Hft). TEFC motor CE500=1.3*exp(5.8259+0.13141*l+0.053255*l^2+0.028628*l^3-0.0035549*l^4), l=ln(electric_hp). Pump domains S400..100000; type50..3500gpm,50..200ft,<=200shaft hp; motor base1..700hp, factor1..250hp. Salt pump installation repeats0.27*1.155. Straight losses sum f*L/D*v^2/(2g); f64/Re below2300, smooth Haaland(-1.8log10(6.9/Re))^-2 otherwise; transitional2300..4000 is flagged. Saltprice0=1.23USD2011/kg;1=2.53USD2021/kg; bulk category >=10millionkg.

CPI1978=65.2,2006=201.6,2011=224.9,2017=245.1,2021=271.0,2024=313.7,2025=321.9. All prices multiply321.9/sourceCPI and costscale. One uninstalled spare of each machine per plant. Machine replacement repeats active purchases+installation+removal_multiplier*installation; bundle replacement repeats tube+accessory fabrication plus0.026 installation and0.024*removal_multiplier. Events k*life<years, discounted(1+r)^(-time), annualized r/(1-(1+r)^(-years)) or1/years at zero rate. Makeup=chosen initial inventory cost*makeup_fraction. Delivered exclusion=active primary packages+primary spare+HX+both pipe fabrication bills; no installation, design fee, inventory, salt pumps or future replacement. Installed total=purchased total+installation total. Seven child costs sum installed total. Sourcefitargument above465C fails physical-interface screen.

Disabled returns finite zeros before active guards. Active requires finite numeric inputs, positive flows/temperatures/dimensions/lives, integer n_loops and n_mod=1, gamma>1,0<efficiencies<=1, shaft<=electric, tube wall<OD/2, suction pressure>0, positive terminal approaches and shell void; invalid arithmetic inputs raise ValueError. Range/capacity failures return false diagnostics with evaluable extrapolated prices.

*Source**: BNL helium quote; ANL2018 cost algorithms; Seider2009 third edition Chapter22; NETL2002; ORNL installation; EU DEMO OB geometry; NREL SSC properties; INL2022 inventory; USGS2025 helium; annual CPI.
*Reference**: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md (released corrective details); primary-candidate.md; work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/secondary-methods.md; evidence/round2/hx-method-check.md. These records link screened registered originals and exact source locations.
*Last Updated**: 2026-09-18

Inputs:
    - bundle_life_in: bundle_life_in parameter
    - n_mod_in: n_mod_in parameter
    - helium_purchased_mass_kg_in: helium_purchased_mass_kg_in parameter
    - primary_electric_MW_in: primary_electric_MW_in parameter
    - q_ihx_MW_in: q_ihx_MW_in parameter
    - n_loops_in: n_loops_in parameter
    - salt_purchased_mass_kg_in: salt_purchased_mass_kg_in parameter
    - helium_gamma_in: helium_gamma_in parameter
    - accessory_mass_in: accessory_mass_in parameter
    - enabled_in: enabled_in parameter
    - mdot_loop_in: mdot_loop_in parameter
    - stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
    - eta_motor_in: eta_motor_in parameter
    - salt_design_eta_p_in: salt_design_eta_p_in parameter
    - years_in: years_in parameter
    - tube_wall_in: tube_wall_in parameter
    - helium_cp_in: helium_cp_in parameter
    - machine_life_in: machine_life_in parameter
    - inventory_reserve_in: inventory_reserve_in parameter
    - salt_design_flow_kg_s_in: salt_design_flow_kg_s_in parameter
    - discount_in: discount_in parameter
    - removal_multiplier_in: removal_multiplier_in parameter
    - salt_design_eta_motor_in: salt_design_eta_motor_in parameter
    - primary_shaft_MW_in: primary_shaft_MW_in parameter
    - costscale_in: costscale_in parameter
    - shell_wall_in: shell_wall_in parameter
    - makeup_fraction_in: makeup_fraction_in parameter
    - helium_hot_K_in: helium_hot_K_in parameter
    - eta_p_in: eta_p_in parameter
    - secondary_head_in: secondary_head_in parameter
    - salt_design_head_m_in: salt_design_head_m_in parameter
    - sourcefitargument_C_in: sourcefitargument_C_in parameter
    - helium_suction_K_in: helium_suction_K_in parameter
    - helium_design_shaft_MW_in: helium_design_shaft_MW_in parameter
    - layout_multiplier_in: layout_multiplier_in parameter
    - saltprice_source_choice_in: saltprice_source_choice_in parameter
    - dp_loop_in: dp_loop_in parameter
    - helium_design_suction_Pa_in: helium_design_suction_Pa_in parameter
    - helium_discharge_Pa_in: helium_discharge_Pa_in parameter

Outputs:
    - salt_pump_flow: salt_pump_flow result
    - salt_represented_fill_margin_kg: salt_represented_fill_margin_kg result
    - ihx_hot_approach: ihx_hot_approach result
    - exchangers_cost: exchangers_cost result
    - pressure_qualified: pressure_qualified result
    - ihx_installed_area: ihx_installed_area result
    - pump_flow_gpm: pump_flow_gpm result
    - design_motor_electric_hp: design_motor_electric_hp result
    - secondary_piping_cost: secondary_piping_cost result
    - secondary_installation: secondary_installation result
    - cycle_interface_ok: cycle_interface_ok result
    - salt_price_raw: salt_price_raw result
    - salt_velocity_cold: salt_velocity_cold result
    - primary_circulators_cost: primary_circulators_cost result
    - helium_represented_fill_margin_kg: helium_represented_fill_margin_kg result
    - inventory_cost: inventory_cost result
    - salt_expansion_ratio: salt_expansion_ratio result
    - salt_straight_loss: salt_straight_loss result
    - primary_pipe_installation: primary_pipe_installation result
    - salt_unit_price: salt_unit_price result
    - ihx_capacity_defined: ihx_capacity_defined result
    - salt_electric_MW: salt_electric_MW result
    - hx_tube_length: hx_tube_length result
    - secondary_pipe_purchase: secondary_pipe_purchase result
    - hx_installation: hx_installation result
    - salt_inventory_mass: salt_inventory_mass result
    - helium_inventory_volume: helium_inventory_volume result
    - replacement_annual: replacement_annual result
    - salt_makeup_annual: salt_makeup_annual result
    - helium_makeup_annual: helium_makeup_annual result
    - salt_design_shaft_MW: salt_design_shaft_MW result
    - inventory_complete: inventory_complete result
    - heads_mass: heads_mass result
    - helium_design_shaft_MW: helium_design_shaft_MW result
    - primary_design: primary_design result
    - salt_head_remaining: salt_head_remaining result
    - installation_total: installation_total result
    - salt_return_C: salt_return_C result
    - salt_design_electric_MW: salt_design_electric_MW result
    - circulator_shaft_MW: circulator_shaft_MW result
    - circulator_flow: circulator_flow result
    - source_volume_ratio: source_volume_ratio result
    - represented_fill_defined: represented_fill_defined result
    - purchased_total: purchased_total result
    - delivered_total: delivered_total result
    - primary_pipe_volume: primary_pipe_volume result
    - bundle_event_purchase: bundle_event_purchase result
    - bundle_mass: bundle_mass result
    - salt_inventory_target_mass_kg: salt_inventory_target_mass_kg result
    - helium_standard_volume: helium_standard_volume result
    - salt_shaft_MW: salt_shaft_MW result
    - helium_design_suction_Pa: helium_design_suction_Pa result
    - helium_inventory_cost: helium_inventory_cost result
    - machine_off_design_performance_qualified: machine_off_design_performance_qualified result
    - salt_Re_hot: salt_Re_hot result
    - salt_hx_volume: salt_hx_volume result
    - hx_shell_bore: hx_shell_bore result
    - inventory_source_volume_ok: inventory_source_volume_ok result
    - pump_shaft_hp: pump_shaft_hp result
    - ihx_capacity_margin_m2: ihx_capacity_margin_m2 result
    - salt_pipe_volume: salt_pipe_volume result
    - design_motor_base_ok: design_motor_base_ok result
    - cycle_temperature_gap: cycle_temperature_gap result
    - primary_piping_cost: primary_piping_cost result
    - hx_purchase: hx_purchase result
    - circulator_volume: circulator_volume result
    - salt_flow: salt_flow result
    - ihx_required_area: ihx_required_area result
    - hx_shell_wall: hx_shell_wall result
    - machine_event_purchase: machine_event_purchase result
    - shell_mass: shell_mass result
    - primary_pipe_mass: primary_pipe_mass result
    - salt_pump_transfer_validated: salt_pump_transfer_validated result
    - pump_size_ok: pump_size_ok result
    - hx_shell_length: hx_shell_length result
    - salt_inventory_cost: salt_inventory_cost result
    - design_pump_type_ok: design_pump_type_ok result
    - design_motor_factor_ok: design_motor_factor_ok result
    - conversion_heat_MW: conversion_heat_MW result
    - ihx_cold_approach: ihx_cold_approach result
    - salt_bulk_scale_ok: salt_bulk_scale_ok result
    - pump_size_factor: pump_size_factor result
    - salt_inventory_volume: salt_inventory_volume result
    - primary_installation: primary_installation result
    - circulator_count: circulator_count result
    - helium_hx_volume: helium_hx_volume result
    - tube_mass: tube_mass result
    - consumables_annual: consumables_annual result
    - design_pump_shaft_hp: design_pump_shaft_hp result
    - secondary_pipe_installation: secondary_pipe_installation result
    - design_pump_flow_gpm: design_pump_flow_gpm result
    - machine_event_installation: machine_event_installation result
    - secondary_vendor: secondary_vendor result
    - salt_design_head_m: salt_design_head_m result
    - machine_event_removal: machine_event_removal result
    - salt_Re_cold: salt_Re_cold result
    - machine_events: machine_events result
    - primary_pipe_purchase: primary_pipe_purchase result
    - primary_vendor: primary_vendor result
    - primary_spare: primary_spare result
    - secondary_spare: secondary_spare result
    - pump_head_ft: pump_head_ft result
    - helium_required_fill_mass_kg: helium_required_fill_mass_kg result
    - secondary_pipe_mass: secondary_pipe_mass result
    - pump_type_ok: pump_type_ok result
    - helium_inventory_target_mass_kg: helium_inventory_target_mass_kg result
    - salt_required_fill_mass_kg: salt_required_fill_mass_kg result
    - helium_price_year: helium_price_year result
    - ihx_count: ihx_count result
    - salt_flow_regime_ok: salt_flow_regime_ok result
    - bundle_event_installation: bundle_event_installation result
    - design_pump_head_ft: design_pump_head_ft result
    - bundle_event_removal: bundle_event_removal result
    - helium_price_raw: helium_price_raw result
    - design_pump_size_ok: design_pump_size_ok result
    - ihx_lmtd: ihx_lmtd result
    - represented_fill_ok: represented_fill_ok result
    - salt_velocity_hot: salt_velocity_hot result
    - hx_mass: hx_mass result
    - helium_inventory_mass: helium_inventory_mass result
    - salt_pump_count: salt_pump_count result
    - motor_electric_hp: motor_electric_hp result
    - secondary_pumps_cost: secondary_pumps_cost result
    - motor_factor_ok: motor_factor_ok result
    - sheets_mass: sheets_mass result
    - spares_cost: spares_cost result
    - salt_head_ok: salt_head_ok result
    - salt_price_year: salt_price_year result
    - circulator_electric_MW: circulator_electric_MW result
    - design_pump_size_factor: design_pump_size_factor result
    - ihx_capacity_ok: ihx_capacity_ok result
    - salt_pump_shaft_MW: salt_pump_shaft_MW result
    - ihx_duty_MW: ihx_duty_MW result
    - installed_total: installed_total result
    - bundle_events: bundle_events result
    - helium_price_transfer_validated: helium_price_transfer_validated result
    - salt_design_flow_kg_s: salt_design_flow_kg_s result
    - circulator_suction_Pa: circulator_suction_Pa result
    - motor_base_ok: motor_base_ok result

SysML Source: root-0/analyses/mfe_cooling_equipment.sysml:3

SysML Source: root-0/analyses/mfe_cooling_equipment.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cooling_equipment/cooling_equipment_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.cooling_equipment_output import Cooling_EquipmentOutput


class Cooling_EquipmentInput(BaseModel):
    """Input model for Cooling_EquipmentModule.

    Attributes:
        bundle_life_in: bundle_life_in input
        n_mod_in: n_mod_in input
        helium_purchased_mass_kg_in: helium_purchased_mass_kg_in input
        primary_electric_MW_in: primary_electric_MW_in input
        q_ihx_MW_in: q_ihx_MW_in input
        n_loops_in: n_loops_in input
        salt_purchased_mass_kg_in: salt_purchased_mass_kg_in input
        helium_gamma_in: helium_gamma_in input
        accessory_mass_in: accessory_mass_in input
        enabled_in: enabled_in input
        mdot_loop_in: mdot_loop_in input
        stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
        eta_motor_in: eta_motor_in input
        salt_design_eta_p_in: salt_design_eta_p_in input
        years_in: years_in input
        tube_wall_in: tube_wall_in input
        helium_cp_in: helium_cp_in input
        machine_life_in: machine_life_in input
        inventory_reserve_in: inventory_reserve_in input
        salt_design_flow_kg_s_in: salt_design_flow_kg_s_in input
        discount_in: discount_in input
        removal_multiplier_in: removal_multiplier_in input
        salt_design_eta_motor_in: salt_design_eta_motor_in input
        primary_shaft_MW_in: primary_shaft_MW_in input
        costscale_in: costscale_in input
        shell_wall_in: shell_wall_in input
        makeup_fraction_in: makeup_fraction_in input
        helium_hot_K_in: helium_hot_K_in input
        eta_p_in: eta_p_in input
        secondary_head_in: secondary_head_in input
        salt_design_head_m_in: salt_design_head_m_in input
        sourcefitargument_C_in: sourcefitargument_C_in input
        helium_suction_K_in: helium_suction_K_in input
        helium_design_shaft_MW_in: helium_design_shaft_MW_in input
        layout_multiplier_in: layout_multiplier_in input
        saltprice_source_choice_in: saltprice_source_choice_in input
        dp_loop_in: dp_loop_in input
        helium_design_suction_Pa_in: helium_design_suction_Pa_in input
        helium_discharge_Pa_in: helium_discharge_Pa_in input
    """
    bundle_life_in: float = Field(..., description="bundle_life_in input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    helium_purchased_mass_kg_in: float = Field(..., description="helium_purchased_mass_kg_in input")
    primary_electric_MW_in: float = Field(..., description="primary_electric_MW_in input")
    q_ihx_MW_in: float = Field(..., description="q_ihx_MW_in input")
    n_loops_in: float = Field(..., description="n_loops_in input")
    salt_purchased_mass_kg_in: float = Field(..., description="salt_purchased_mass_kg_in input")
    helium_gamma_in: float = Field(..., description="helium_gamma_in input")
    accessory_mass_in: float = Field(..., description="accessory_mass_in input")
    enabled_in: bool = Field(..., description="enabled_in input")
    mdot_loop_in: float = Field(..., description="mdot_loop_in input")
    stainless_fabrication_usd2017_per_kg_in: float = Field(..., description="*Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19")
    eta_motor_in: float = Field(..., description="eta_motor_in input")
    salt_design_eta_p_in: float = Field(..., description="salt_design_eta_p_in input")
    years_in: float = Field(..., description="years_in input")
    tube_wall_in: float = Field(..., description="tube_wall_in input")
    helium_cp_in: float = Field(..., description="helium_cp_in input")
    machine_life_in: float = Field(..., description="machine_life_in input")
    inventory_reserve_in: float = Field(..., description="inventory_reserve_in input")
    salt_design_flow_kg_s_in: float = Field(..., description="salt_design_flow_kg_s_in input")
    discount_in: float = Field(..., description="discount_in input")
    removal_multiplier_in: float = Field(..., description="removal_multiplier_in input")
    salt_design_eta_motor_in: float = Field(..., description="salt_design_eta_motor_in input")
    primary_shaft_MW_in: float = Field(..., description="primary_shaft_MW_in input")
    costscale_in: float = Field(..., description="costscale_in input")
    shell_wall_in: float = Field(..., description="shell_wall_in input")
    makeup_fraction_in: float = Field(..., description="makeup_fraction_in input")
    helium_hot_K_in: float = Field(..., description="helium_hot_K_in input")
    eta_p_in: float = Field(..., description="eta_p_in input")
    secondary_head_in: float = Field(..., description="secondary_head_in input")
    salt_design_head_m_in: float = Field(..., description="salt_design_head_m_in input")
    sourcefitargument_C_in: float = Field(..., description="sourcefitargument_C_in input")
    helium_suction_K_in: float = Field(..., description="helium_suction_K_in input")
    helium_design_shaft_MW_in: float = Field(..., description="helium_design_shaft_MW_in input")
    layout_multiplier_in: float = Field(..., description="layout_multiplier_in input")
    saltprice_source_choice_in: float = Field(..., description="saltprice_source_choice_in input")
    dp_loop_in: float = Field(..., description="dp_loop_in input")
    helium_design_suction_Pa_in: float = Field(..., description="helium_design_suction_Pa_in input")
    helium_discharge_Pa_in: float = Field(..., description="helium_discharge_Pa_in input")


class Cooling_EquipmentModule(ModuleBase[Cooling_EquipmentInput, Cooling_EquipmentOutput]):
    """TEAx module for Cooling_Equipment calculation.

Conceptual helium/HITEC cooling equipment. WI-078: selected machine design-point pumping duty/pressure and salt flow/head/efficiencies price installed packages, spares and replacements independently of operating demand. The 50hp helium normalization is pumping duty, not motor nameplate. Purchased fluid stocks are supplied; required fill derives from represented volumes and operating density. Reserve targets are suggestions only. Signed represented-fill margins are purchased minus required kg; represented_fill_ok is their nonnegative conjunction, not complete inventory qualification. Off-design machine performance remains unqualified. Source: work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md and architecture-review-r2.md. Basis: approved MR-7 interpretation; unchanged source price correlations, fixed HX/pipe geometry and operating closures. Guarded manual completion implements the equations below; all costs are USD2025 annual-CPI purchasing-power proxies. This is a priced subset, with unpriced valves, supports, insulation, salt auxiliaries and conversion-side inventory. Pressure qualification and helium/salt machine technology transfers are unvalidated. Geometry and lifecycle assumptions are agent-selected scenarios.

Output basis: HX masses and duty per IHX; HX areas per IHX; salt_flow per circuit; all pipe and inventory quantities plant total; machine outputs per machine except counts.

Normative equations: two parallel machines and one fixed OB exchanger per circuit. BNL machine1978=550000*(0.5+0.5*(p_suction/(735*6894.757293168))*(shaft_W/745.6998715822702/50)^0.28); package=1.2*machine. Design fee130000 once. Installation=0.27*1.155*vendor; procurement services remain CAS30. Tube count14852, OD0.01905m, length11.6m; area=pi*OD*length*count. Tube mass=8000*area*t*(1-t/OD). Shell bore3.2m, length13m; annular shell and spherical pair of heads; two gross0.6m tubesheets; explicit accessory mass. Required area=(Q_IHX/N)/(UF*LMTD), UF=267.8e6/[area*(35-19.3)/ln(35/19.3)]. Hot/cold approaches are helium hot minus738.15K and suction minus543.15K.

Primary mains OD1.3/1.1m,65mm walls,50m each; nine branches per leg, ID=mainID/3,30mm wall, length=(4000/9-100)/18. Straight annular steel times(1+14440/66560) prices fittings. Secondary ID0.4m,20mm wall,50m each leg. All lengths scale with layout_multiplier. Delivered fabrication=stainless_fabrication_usd2017_per_kg_in (nominal310USD2017/kg); pipe field labor=0.50*fabrication. HX installation=0.024 labor+0.002 material. Salt shell void=pi*1.6^2*11.6-tube_outer_volume-accessory_mass/8000. Inventory volume is pipe+shell void only; cold density gives required fill; times(1+reserve) gives an optional target. Purchased mass is independently supplied. Helium volume=pipe+61.5*N, pressure discharge, arithmetic-mean hot/suction temperature, ideal gas R=cp*(gamma-1)/gamma, supplies the required fill diagnostic. Standard volume uses101325Pa/288.15K;14USD2024/m3. Source879m3/9circuit check is independent, never an added inventory.

Salt cp1560, density=max(2080-0.733*T_C,1000), viscosity=max(0.00622-1.02e-5*T_C,1e-6). Flow=Q_IHX*1e6/(1560*195); two pumps/circuit. Shaft=mdot*g*head/eta_p; electric=shaft/eta_motor. Pump CE500=3*exp(9.7171-0.6019*ln(S)+0.0519*ln(S)^2), S=Qgpm*sqrt(Hft). TEFC motor CE500=1.3*exp(5.8259+0.13141*l+0.053255*l^2+0.028628*l^3-0.0035549*l^4), l=ln(electric_hp). Pump domains S400..100000; type50..3500gpm,50..200ft,<=200shaft hp; motor base1..700hp, factor1..250hp. Salt pump installation repeats0.27*1.155. Straight losses sum f*L/D*v^2/(2g); f64/Re below2300, smooth Haaland(-1.8log10(6.9/Re))^-2 otherwise; transitional2300..4000 is flagged. Saltprice0=1.23USD2011/kg;1=2.53USD2021/kg; bulk category >=10millionkg.

CPI1978=65.2,2006=201.6,2011=224.9,2017=245.1,2021=271.0,2024=313.7,2025=321.9. All prices multiply321.9/sourceCPI and costscale. One uninstalled spare of each machine per plant. Machine replacement repeats active purchases+installation+removal_multiplier*installation; bundle replacement repeats tube+accessory fabrication plus0.026 installation and0.024*removal_multiplier. Events k*life<years, discounted(1+r)^(-time), annualized r/(1-(1+r)^(-years)) or1/years at zero rate. Makeup=chosen initial inventory cost*makeup_fraction. Delivered exclusion=active primary packages+primary spare+HX+both pipe fabrication bills; no installation, design fee, inventory, salt pumps or future replacement. Installed total=purchased total+installation total. Seven child costs sum installed total. Sourcefitargument above465C fails physical-interface screen.

Disabled returns finite zeros before active guards. Active requires finite numeric inputs, positive flows/temperatures/dimensions/lives, integer n_loops and n_mod=1, gamma>1,0<efficiencies<=1, shaft<=electric, tube wall<OD/2, suction pressure>0, positive terminal approaches and shell void; invalid arithmetic inputs raise ValueError. Range/capacity failures return false diagnostics with evaluable extrapolated prices.

*Source**: BNL helium quote; ANL2018 cost algorithms; Seider2009 third edition Chapter22; NETL2002; ORNL installation; EU DEMO OB geometry; NREL SSC properties; INL2022 inventory; USGS2025 helium; annual CPI.
*Reference**: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md (released corrective details); primary-candidate.md; work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/secondary-methods.md; evidence/round2/hx-method-check.md. These records link screened registered originals and exact source locations.
*Last Updated**: 2026-09-18

Inputs:
    - bundle_life_in: bundle_life_in parameter
    - n_mod_in: n_mod_in parameter
    - helium_purchased_mass_kg_in: helium_purchased_mass_kg_in parameter
    - primary_electric_MW_in: primary_electric_MW_in parameter
    - q_ihx_MW_in: q_ihx_MW_in parameter
    - n_loops_in: n_loops_in parameter
    - salt_purchased_mass_kg_in: salt_purchased_mass_kg_in parameter
    - helium_gamma_in: helium_gamma_in parameter
    - accessory_mass_in: accessory_mass_in parameter
    - enabled_in: enabled_in parameter
    - mdot_loop_in: mdot_loop_in parameter
    - stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
    - eta_motor_in: eta_motor_in parameter
    - salt_design_eta_p_in: salt_design_eta_p_in parameter
    - years_in: years_in parameter
    - tube_wall_in: tube_wall_in parameter
    - helium_cp_in: helium_cp_in parameter
    - machine_life_in: machine_life_in parameter
    - inventory_reserve_in: inventory_reserve_in parameter
    - salt_design_flow_kg_s_in: salt_design_flow_kg_s_in parameter
    - discount_in: discount_in parameter
    - removal_multiplier_in: removal_multiplier_in parameter
    - salt_design_eta_motor_in: salt_design_eta_motor_in parameter
    - primary_shaft_MW_in: primary_shaft_MW_in parameter
    - costscale_in: costscale_in parameter
    - shell_wall_in: shell_wall_in parameter
    - makeup_fraction_in: makeup_fraction_in parameter
    - helium_hot_K_in: helium_hot_K_in parameter
    - eta_p_in: eta_p_in parameter
    - secondary_head_in: secondary_head_in parameter
    - salt_design_head_m_in: salt_design_head_m_in parameter
    - sourcefitargument_C_in: sourcefitargument_C_in parameter
    - helium_suction_K_in: helium_suction_K_in parameter
    - helium_design_shaft_MW_in: helium_design_shaft_MW_in parameter
    - layout_multiplier_in: layout_multiplier_in parameter
    - saltprice_source_choice_in: saltprice_source_choice_in parameter
    - dp_loop_in: dp_loop_in parameter
    - helium_design_suction_Pa_in: helium_design_suction_Pa_in parameter
    - helium_discharge_Pa_in: helium_discharge_Pa_in parameter

Outputs:
    - salt_pump_flow: salt_pump_flow result
    - salt_represented_fill_margin_kg: salt_represented_fill_margin_kg result
    - ihx_hot_approach: ihx_hot_approach result
    - exchangers_cost: exchangers_cost result
    - pressure_qualified: pressure_qualified result
    - ihx_installed_area: ihx_installed_area result
    - pump_flow_gpm: pump_flow_gpm result
    - design_motor_electric_hp: design_motor_electric_hp result
    - secondary_piping_cost: secondary_piping_cost result
    - secondary_installation: secondary_installation result
    - cycle_interface_ok: cycle_interface_ok result
    - salt_price_raw: salt_price_raw result
    - salt_velocity_cold: salt_velocity_cold result
    - primary_circulators_cost: primary_circulators_cost result
    - helium_represented_fill_margin_kg: helium_represented_fill_margin_kg result
    - inventory_cost: inventory_cost result
    - salt_expansion_ratio: salt_expansion_ratio result
    - salt_straight_loss: salt_straight_loss result
    - primary_pipe_installation: primary_pipe_installation result
    - salt_unit_price: salt_unit_price result
    - ihx_capacity_defined: ihx_capacity_defined result
    - salt_electric_MW: salt_electric_MW result
    - hx_tube_length: hx_tube_length result
    - secondary_pipe_purchase: secondary_pipe_purchase result
    - hx_installation: hx_installation result
    - salt_inventory_mass: salt_inventory_mass result
    - helium_inventory_volume: helium_inventory_volume result
    - replacement_annual: replacement_annual result
    - salt_makeup_annual: salt_makeup_annual result
    - helium_makeup_annual: helium_makeup_annual result
    - salt_design_shaft_MW: salt_design_shaft_MW result
    - inventory_complete: inventory_complete result
    - heads_mass: heads_mass result
    - helium_design_shaft_MW: helium_design_shaft_MW result
    - primary_design: primary_design result
    - salt_head_remaining: salt_head_remaining result
    - installation_total: installation_total result
    - salt_return_C: salt_return_C result
    - salt_design_electric_MW: salt_design_electric_MW result
    - circulator_shaft_MW: circulator_shaft_MW result
    - circulator_flow: circulator_flow result
    - source_volume_ratio: source_volume_ratio result
    - represented_fill_defined: represented_fill_defined result
    - purchased_total: purchased_total result
    - delivered_total: delivered_total result
    - primary_pipe_volume: primary_pipe_volume result
    - bundle_event_purchase: bundle_event_purchase result
    - bundle_mass: bundle_mass result
    - salt_inventory_target_mass_kg: salt_inventory_target_mass_kg result
    - helium_standard_volume: helium_standard_volume result
    - salt_shaft_MW: salt_shaft_MW result
    - helium_design_suction_Pa: helium_design_suction_Pa result
    - helium_inventory_cost: helium_inventory_cost result
    - machine_off_design_performance_qualified: machine_off_design_performance_qualified result
    - salt_Re_hot: salt_Re_hot result
    - salt_hx_volume: salt_hx_volume result
    - hx_shell_bore: hx_shell_bore result
    - inventory_source_volume_ok: inventory_source_volume_ok result
    - pump_shaft_hp: pump_shaft_hp result
    - ihx_capacity_margin_m2: ihx_capacity_margin_m2 result
    - salt_pipe_volume: salt_pipe_volume result
    - design_motor_base_ok: design_motor_base_ok result
    - cycle_temperature_gap: cycle_temperature_gap result
    - primary_piping_cost: primary_piping_cost result
    - hx_purchase: hx_purchase result
    - circulator_volume: circulator_volume result
    - salt_flow: salt_flow result
    - ihx_required_area: ihx_required_area result
    - hx_shell_wall: hx_shell_wall result
    - machine_event_purchase: machine_event_purchase result
    - shell_mass: shell_mass result
    - primary_pipe_mass: primary_pipe_mass result
    - salt_pump_transfer_validated: salt_pump_transfer_validated result
    - pump_size_ok: pump_size_ok result
    - hx_shell_length: hx_shell_length result
    - salt_inventory_cost: salt_inventory_cost result
    - design_pump_type_ok: design_pump_type_ok result
    - design_motor_factor_ok: design_motor_factor_ok result
    - conversion_heat_MW: conversion_heat_MW result
    - ihx_cold_approach: ihx_cold_approach result
    - salt_bulk_scale_ok: salt_bulk_scale_ok result
    - pump_size_factor: pump_size_factor result
    - salt_inventory_volume: salt_inventory_volume result
    - primary_installation: primary_installation result
    - circulator_count: circulator_count result
    - helium_hx_volume: helium_hx_volume result
    - tube_mass: tube_mass result
    - consumables_annual: consumables_annual result
    - design_pump_shaft_hp: design_pump_shaft_hp result
    - secondary_pipe_installation: secondary_pipe_installation result
    - design_pump_flow_gpm: design_pump_flow_gpm result
    - machine_event_installation: machine_event_installation result
    - secondary_vendor: secondary_vendor result
    - salt_design_head_m: salt_design_head_m result
    - machine_event_removal: machine_event_removal result
    - salt_Re_cold: salt_Re_cold result
    - machine_events: machine_events result
    - primary_pipe_purchase: primary_pipe_purchase result
    - primary_vendor: primary_vendor result
    - primary_spare: primary_spare result
    - secondary_spare: secondary_spare result
    - pump_head_ft: pump_head_ft result
    - helium_required_fill_mass_kg: helium_required_fill_mass_kg result
    - secondary_pipe_mass: secondary_pipe_mass result
    - pump_type_ok: pump_type_ok result
    - helium_inventory_target_mass_kg: helium_inventory_target_mass_kg result
    - salt_required_fill_mass_kg: salt_required_fill_mass_kg result
    - helium_price_year: helium_price_year result
    - ihx_count: ihx_count result
    - salt_flow_regime_ok: salt_flow_regime_ok result
    - bundle_event_installation: bundle_event_installation result
    - design_pump_head_ft: design_pump_head_ft result
    - bundle_event_removal: bundle_event_removal result
    - helium_price_raw: helium_price_raw result
    - design_pump_size_ok: design_pump_size_ok result
    - ihx_lmtd: ihx_lmtd result
    - represented_fill_ok: represented_fill_ok result
    - salt_velocity_hot: salt_velocity_hot result
    - hx_mass: hx_mass result
    - helium_inventory_mass: helium_inventory_mass result
    - salt_pump_count: salt_pump_count result
    - motor_electric_hp: motor_electric_hp result
    - secondary_pumps_cost: secondary_pumps_cost result
    - motor_factor_ok: motor_factor_ok result
    - sheets_mass: sheets_mass result
    - spares_cost: spares_cost result
    - salt_head_ok: salt_head_ok result
    - salt_price_year: salt_price_year result
    - circulator_electric_MW: circulator_electric_MW result
    - design_pump_size_factor: design_pump_size_factor result
    - ihx_capacity_ok: ihx_capacity_ok result
    - salt_pump_shaft_MW: salt_pump_shaft_MW result
    - ihx_duty_MW: ihx_duty_MW result
    - installed_total: installed_total result
    - bundle_events: bundle_events result
    - helium_price_transfer_validated: helium_price_transfer_validated result
    - salt_design_flow_kg_s: salt_design_flow_kg_s result
    - circulator_suction_Pa: circulator_suction_Pa result
    - motor_base_ok: motor_base_ok result

SysML Source: root-0/analyses/mfe_cooling_equipment.sysml:3

    SysML Source: root-0/analyses/mfe_cooling_equipment.sysml:3

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
Conceptual helium/HITEC cooling equipment. WI-078: selected machine design-point pumping duty/pressure and salt flow/head/efficiencies price installed packages, spares and replacements independently of operating demand. The 50hp helium normalization is pumping duty, not motor nameplate. Purchased fluid stocks are supplied; required fill derives from represented volumes and operating density. Reserve targets are suggestions only. Signed represented-fill margins are purchased minus required kg; represented_fill_ok is their nonnegative conjunction, not complete inventory qualification. Off-design machine performance remains unqualified. Source: work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md and architecture-review-r2.md. Basis: approved MR-7 interpretation; unchanged source price correlations, fixed HX/pipe geometry and operating closures. Guarded manual completion implements the equations below; all costs are USD2025 annual-CPI purchasing-power proxies. This is a priced subset, with unpriced valves, supports, insulation, salt auxiliaries and conversion-side inventory. Pressure qualification and helium/salt machine technology transfers are unvalidated. Geometry and lifecycle assumptions are agent-selected scenarios.

Output basis: HX masses and duty per IHX; HX areas per IHX; salt_flow per circuit; all pipe and inventory quantities plant total; machine outputs per machine except counts.

Normative equations: two parallel machines and one fixed OB exchanger per circuit. BNL machine1978=550000*(0.5+0.5*(p_suction/(735*6894.757293168))*(shaft_W/745.6998715822702/50)^0.28); package=1.2*machine. Design fee130000 once. Installation=0.27*1.155*vendor; procurement services remain CAS30. Tube count14852, OD0.01905m, length11.6m; area=pi*OD*length*count. Tube mass=8000*area*t*(1-t/OD). Shell bore3.2m, length13m; annular shell and spherical pair of heads; two gross0.6m tubesheets; explicit accessory mass. Required area=(Q_IHX/N)/(UF*LMTD), UF=267.8e6/[area*(35-19.3)/ln(35/19.3)]. Hot/cold approaches are helium hot minus738.15K and suction minus543.15K.

Primary mains OD1.3/1.1m,65mm walls,50m each; nine branches per leg, ID=mainID/3,30mm wall, length=(4000/9-100)/18. Straight annular steel times(1+14440/66560) prices fittings. Secondary ID0.4m,20mm wall,50m each leg. All lengths scale with layout_multiplier. Delivered fabrication=stainless_fabrication_usd2017_per_kg_in (nominal310USD2017/kg); pipe field labor=0.50*fabrication. HX installation=0.024 labor+0.002 material. Salt shell void=pi*1.6^2*11.6-tube_outer_volume-accessory_mass/8000. Inventory volume is pipe+shell void only; cold density gives required fill; times(1+reserve) gives an optional target. Purchased mass is independently supplied. Helium volume=pipe+61.5*N, pressure discharge, arithmetic-mean hot/suction temperature, ideal gas R=cp*(gamma-1)/gamma, supplies the required fill diagnostic. Standard volume uses101325Pa/288.15K;14USD2024/m3. Source879m3/9circuit check is independent, never an added inventory.

Salt cp1560, density=max(2080-0.733*T_C,1000), viscosity=max(0.00622-1.02e-5*T_C,1e-6). Flow=Q_IHX*1e6/(1560*195); two pumps/circuit. Shaft=mdot*g*head/eta_p; electric=shaft/eta_motor. Pump CE500=3*exp(9.7171-0.6019*ln(S)+0.0519*ln(S)^2), S=Qgpm*sqrt(Hft). TEFC motor CE500=1.3*exp(5.8259+0.13141*l+0.053255*l^2+0.028628*l^3-0.0035549*l^4), l=ln(electric_hp). Pump domains S400..100000; type50..3500gpm,50..200ft,<=200shaft hp; motor base1..700hp, factor1..250hp. Salt pump installation repeats0.27*1.155. Straight losses sum f*L/D*v^2/(2g); f64/Re below2300, smooth Haaland(-1.8log10(6.9/Re))^-2 otherwise; transitional2300..4000 is flagged. Saltprice0=1.23USD2011/kg;1=2.53USD2021/kg; bulk category >=10millionkg.

CPI1978=65.2,2006=201.6,2011=224.9,2017=245.1,2021=271.0,2024=313.7,2025=321.9. All prices multiply321.9/sourceCPI and costscale. One uninstalled spare of each machine per plant. Machine replacement repeats active purchases+installation+removal_multiplier*installation; bundle replacement repeats tube+accessory fabrication plus0.026 installation and0.024*removal_multiplier. Events k*life<years, discounted(1+r)^(-time), annualized r/(1-(1+r)^(-years)) or1/years at zero rate. Makeup=chosen initial inventory cost*makeup_fraction. Delivered exclusion=active primary packages+primary spare+HX+both pipe fabrication bills; no installation, design fee, inventory, salt pumps or future replacement. Installed total=purchased total+installation total. Seven child costs sum installed total. Sourcefitargument above465C fails physical-interface screen.

Disabled returns finite zeros before active guards. Active requires finite numeric inputs, positive flows/temperatures/dimensions/lives, integer n_loops and n_mod=1, gamma>1,0<efficiencies<=1, shaft<=electric, tube wall<OD/2, suction pressure>0, positive terminal approaches and shell void; invalid arithmetic inputs raise ValueError. Range/capacity failures return false diagnostics with evaluable extrapolated prices.

*Source**: BNL helium quote; ANL2018 cost algorithms; Seider2009 third edition Chapter22; NETL2002; ORNL installation; EU DEMO OB geometry; NREL SSC properties; INL2022 inventory; USGS2025 helium; annual CPI.
*Reference**: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md (released corrective details); primary-candidate.md; work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/secondary-methods.md; evidence/round2/hx-method-check.md. These records link screened registered originals and exact source locations.
*Last Updated**: 2026-09-18

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_cooling_equipment.cooling_equipment_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts salt_pump_flow, salt_represented_fill_margin_kg, ihx_hot_approach, exchangers_cost, pressure_qualified, ihx_installed_area, pump_flow_gpm, design_motor_electric_hp, secondary_piping_cost, secondary_installation, cycle_interface_ok, salt_price_raw, salt_velocity_cold, primary_circulators_cost, helium_represented_fill_margin_kg, inventory_cost, salt_expansion_ratio, salt_straight_loss, primary_pipe_installation, salt_unit_price, ihx_capacity_defined, salt_electric_MW, hx_tube_length, secondary_pipe_purchase, hx_installation, salt_inventory_mass, helium_inventory_volume, replacement_annual, salt_makeup_annual, helium_makeup_annual, salt_design_shaft_MW, inventory_complete, heads_mass, helium_design_shaft_MW, primary_design, salt_head_remaining, installation_total, salt_return_C, salt_design_electric_MW, circulator_shaft_MW, circulator_flow, source_volume_ratio, represented_fill_defined, purchased_total, delivered_total, primary_pipe_volume, bundle_event_purchase, bundle_mass, salt_inventory_target_mass_kg, helium_standard_volume, salt_shaft_MW, helium_design_suction_Pa, helium_inventory_cost, machine_off_design_performance_qualified, salt_Re_hot, salt_hx_volume, hx_shell_bore, inventory_source_volume_ok, pump_shaft_hp, ihx_capacity_margin_m2, salt_pipe_volume, design_motor_base_ok, cycle_temperature_gap, primary_piping_cost, hx_purchase, circulator_volume, salt_flow, ihx_required_area, hx_shell_wall, machine_event_purchase, shell_mass, primary_pipe_mass, salt_pump_transfer_validated, pump_size_ok, hx_shell_length, salt_inventory_cost, design_pump_type_ok, design_motor_factor_ok, conversion_heat_MW, ihx_cold_approach, salt_bulk_scale_ok, pump_size_factor, salt_inventory_volume, primary_installation, circulator_count, helium_hx_volume, tube_mass, consumables_annual, design_pump_shaft_hp, secondary_pipe_installation, design_pump_flow_gpm, machine_event_installation, secondary_vendor, salt_design_head_m, machine_event_removal, salt_Re_cold, machine_events, primary_pipe_purchase, primary_vendor, primary_spare, secondary_spare, pump_head_ft, helium_required_fill_mass_kg, secondary_pipe_mass, pump_type_ok, helium_inventory_target_mass_kg, salt_required_fill_mass_kg, helium_price_year, ihx_count, salt_flow_regime_ok, bundle_event_installation, design_pump_head_ft, bundle_event_removal, helium_price_raw, design_pump_size_ok, ihx_lmtd, represented_fill_ok, salt_velocity_hot, hx_mass, helium_inventory_mass, salt_pump_count, motor_electric_hp, secondary_pumps_cost, motor_factor_ok, sheets_mass, spares_cost, salt_head_ok, salt_price_year, circulator_electric_MW, design_pump_size_factor, ihx_capacity_ok, salt_pump_shaft_MW, ihx_duty_MW, installed_total, bundle_events, helium_price_transfer_validated, salt_design_flow_kg_s, circulator_suction_Pa, motor_base_ok fields to separate channels.
    """

    name: str = "Cooling_EquipmentModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, bundle_life_in: float, n_mod_in: float, helium_purchased_mass_kg_in: float, primary_electric_MW_in: float, q_ihx_MW_in: float, n_loops_in: float, salt_purchased_mass_kg_in: float, helium_gamma_in: float, accessory_mass_in: float, enabled_in: bool, mdot_loop_in: float, stainless_fabrication_usd2017_per_kg_in: float, eta_motor_in: float, salt_design_eta_p_in: float, years_in: float, tube_wall_in: float, helium_cp_in: float, machine_life_in: float, inventory_reserve_in: float, salt_design_flow_kg_s_in: float, discount_in: float, removal_multiplier_in: float, salt_design_eta_motor_in: float, primary_shaft_MW_in: float, costscale_in: float, shell_wall_in: float, makeup_fraction_in: float, helium_hot_K_in: float, eta_p_in: float, secondary_head_in: float, salt_design_head_m_in: float, sourcefitargument_C_in: float, helium_suction_K_in: float, helium_design_shaft_MW_in: float, layout_multiplier_in: float, saltprice_source_choice_in: float, dp_loop_in: float, helium_design_suction_Pa_in: float, helium_discharge_Pa_in: float    ) -> Cooling_EquipmentInput:
        """Validate inputs and fill defaults.

        Args:
            bundle_life_in: bundle_life_in input
            n_mod_in: n_mod_in input
            helium_purchased_mass_kg_in: helium_purchased_mass_kg_in input
            primary_electric_MW_in: primary_electric_MW_in input
            q_ihx_MW_in: q_ihx_MW_in input
            n_loops_in: n_loops_in input
            salt_purchased_mass_kg_in: salt_purchased_mass_kg_in input
            helium_gamma_in: helium_gamma_in input
            accessory_mass_in: accessory_mass_in input
            enabled_in: enabled_in input
            mdot_loop_in: mdot_loop_in input
            stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
            eta_motor_in: eta_motor_in input
            salt_design_eta_p_in: salt_design_eta_p_in input
            years_in: years_in input
            tube_wall_in: tube_wall_in input
            helium_cp_in: helium_cp_in input
            machine_life_in: machine_life_in input
            inventory_reserve_in: inventory_reserve_in input
            salt_design_flow_kg_s_in: salt_design_flow_kg_s_in input
            discount_in: discount_in input
            removal_multiplier_in: removal_multiplier_in input
            salt_design_eta_motor_in: salt_design_eta_motor_in input
            primary_shaft_MW_in: primary_shaft_MW_in input
            costscale_in: costscale_in input
            shell_wall_in: shell_wall_in input
            makeup_fraction_in: makeup_fraction_in input
            helium_hot_K_in: helium_hot_K_in input
            eta_p_in: eta_p_in input
            secondary_head_in: secondary_head_in input
            salt_design_head_m_in: salt_design_head_m_in input
            sourcefitargument_C_in: sourcefitargument_C_in input
            helium_suction_K_in: helium_suction_K_in input
            helium_design_shaft_MW_in: helium_design_shaft_MW_in input
            layout_multiplier_in: layout_multiplier_in input
            saltprice_source_choice_in: saltprice_source_choice_in input
            dp_loop_in: dp_loop_in input
            helium_design_suction_Pa_in: helium_design_suction_Pa_in input
            helium_discharge_Pa_in: helium_discharge_Pa_in input

        Returns:
            Validated input model
        """
        return Cooling_EquipmentInput(bundle_life_in=bundle_life_in, n_mod_in=n_mod_in, helium_purchased_mass_kg_in=helium_purchased_mass_kg_in, primary_electric_MW_in=primary_electric_MW_in, q_ihx_MW_in=q_ihx_MW_in, n_loops_in=n_loops_in, salt_purchased_mass_kg_in=salt_purchased_mass_kg_in, helium_gamma_in=helium_gamma_in, accessory_mass_in=accessory_mass_in, enabled_in=enabled_in, mdot_loop_in=mdot_loop_in, stainless_fabrication_usd2017_per_kg_in=stainless_fabrication_usd2017_per_kg_in, eta_motor_in=eta_motor_in, salt_design_eta_p_in=salt_design_eta_p_in, years_in=years_in, tube_wall_in=tube_wall_in, helium_cp_in=helium_cp_in, machine_life_in=machine_life_in, inventory_reserve_in=inventory_reserve_in, salt_design_flow_kg_s_in=salt_design_flow_kg_s_in, discount_in=discount_in, removal_multiplier_in=removal_multiplier_in, salt_design_eta_motor_in=salt_design_eta_motor_in, primary_shaft_MW_in=primary_shaft_MW_in, costscale_in=costscale_in, shell_wall_in=shell_wall_in, makeup_fraction_in=makeup_fraction_in, helium_hot_K_in=helium_hot_K_in, eta_p_in=eta_p_in, secondary_head_in=secondary_head_in, salt_design_head_m_in=salt_design_head_m_in, sourcefitargument_C_in=sourcefitargument_C_in, helium_suction_K_in=helium_suction_K_in, helium_design_shaft_MW_in=helium_design_shaft_MW_in, layout_multiplier_in=layout_multiplier_in, saltprice_source_choice_in=saltprice_source_choice_in, dp_loop_in=dp_loop_in, helium_design_suction_Pa_in=helium_design_suction_Pa_in, helium_discharge_Pa_in=helium_discharge_Pa_in)

    def run(
        self, bundle_life_in: float, n_mod_in: float, helium_purchased_mass_kg_in: float, primary_electric_MW_in: float, q_ihx_MW_in: float, n_loops_in: float, salt_purchased_mass_kg_in: float, helium_gamma_in: float, accessory_mass_in: float, enabled_in: bool, mdot_loop_in: float, stainless_fabrication_usd2017_per_kg_in: float, eta_motor_in: float, salt_design_eta_p_in: float, years_in: float, tube_wall_in: float, helium_cp_in: float, machine_life_in: float, inventory_reserve_in: float, salt_design_flow_kg_s_in: float, discount_in: float, removal_multiplier_in: float, salt_design_eta_motor_in: float, primary_shaft_MW_in: float, costscale_in: float, shell_wall_in: float, makeup_fraction_in: float, helium_hot_K_in: float, eta_p_in: float, secondary_head_in: float, salt_design_head_m_in: float, sourcefitargument_C_in: float, helium_suction_K_in: float, helium_design_shaft_MW_in: float, layout_multiplier_in: float, saltprice_source_choice_in: float, dp_loop_in: float, helium_design_suction_Pa_in: float, helium_discharge_Pa_in: float    ) -> ModuleResult[Cooling_EquipmentOutput]:
        """Execute calculation.

        Args:
            bundle_life_in: bundle_life_in input
            n_mod_in: n_mod_in input
            helium_purchased_mass_kg_in: helium_purchased_mass_kg_in input
            primary_electric_MW_in: primary_electric_MW_in input
            q_ihx_MW_in: q_ihx_MW_in input
            n_loops_in: n_loops_in input
            salt_purchased_mass_kg_in: salt_purchased_mass_kg_in input
            helium_gamma_in: helium_gamma_in input
            accessory_mass_in: accessory_mass_in input
            enabled_in: enabled_in input
            mdot_loop_in: mdot_loop_in input
            stainless_fabrication_usd2017_per_kg_in: *Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19
            eta_motor_in: eta_motor_in input
            salt_design_eta_p_in: salt_design_eta_p_in input
            years_in: years_in input
            tube_wall_in: tube_wall_in input
            helium_cp_in: helium_cp_in input
            machine_life_in: machine_life_in input
            inventory_reserve_in: inventory_reserve_in input
            salt_design_flow_kg_s_in: salt_design_flow_kg_s_in input
            discount_in: discount_in input
            removal_multiplier_in: removal_multiplier_in input
            salt_design_eta_motor_in: salt_design_eta_motor_in input
            primary_shaft_MW_in: primary_shaft_MW_in input
            costscale_in: costscale_in input
            shell_wall_in: shell_wall_in input
            makeup_fraction_in: makeup_fraction_in input
            helium_hot_K_in: helium_hot_K_in input
            eta_p_in: eta_p_in input
            secondary_head_in: secondary_head_in input
            salt_design_head_m_in: salt_design_head_m_in input
            sourcefitargument_C_in: sourcefitargument_C_in input
            helium_suction_K_in: helium_suction_K_in input
            helium_design_shaft_MW_in: helium_design_shaft_MW_in input
            layout_multiplier_in: layout_multiplier_in input
            saltprice_source_choice_in: saltprice_source_choice_in input
            dp_loop_in: dp_loop_in input
            helium_design_suction_Pa_in: helium_design_suction_Pa_in input
            helium_discharge_Pa_in: helium_discharge_Pa_in input

        Returns:
            Module result with Cooling_EquipmentOutput (salt_pump_flow, salt_represented_fill_margin_kg, ihx_hot_approach, exchangers_cost, pressure_qualified, ihx_installed_area, pump_flow_gpm, design_motor_electric_hp, secondary_piping_cost, secondary_installation, cycle_interface_ok, salt_price_raw, salt_velocity_cold, primary_circulators_cost, helium_represented_fill_margin_kg, inventory_cost, salt_expansion_ratio, salt_straight_loss, primary_pipe_installation, salt_unit_price, ihx_capacity_defined, salt_electric_MW, hx_tube_length, secondary_pipe_purchase, hx_installation, salt_inventory_mass, helium_inventory_volume, replacement_annual, salt_makeup_annual, helium_makeup_annual, salt_design_shaft_MW, inventory_complete, heads_mass, helium_design_shaft_MW, primary_design, salt_head_remaining, installation_total, salt_return_C, salt_design_electric_MW, circulator_shaft_MW, circulator_flow, source_volume_ratio, represented_fill_defined, purchased_total, delivered_total, primary_pipe_volume, bundle_event_purchase, bundle_mass, salt_inventory_target_mass_kg, helium_standard_volume, salt_shaft_MW, helium_design_suction_Pa, helium_inventory_cost, machine_off_design_performance_qualified, salt_Re_hot, salt_hx_volume, hx_shell_bore, inventory_source_volume_ok, pump_shaft_hp, ihx_capacity_margin_m2, salt_pipe_volume, design_motor_base_ok, cycle_temperature_gap, primary_piping_cost, hx_purchase, circulator_volume, salt_flow, ihx_required_area, hx_shell_wall, machine_event_purchase, shell_mass, primary_pipe_mass, salt_pump_transfer_validated, pump_size_ok, hx_shell_length, salt_inventory_cost, design_pump_type_ok, design_motor_factor_ok, conversion_heat_MW, ihx_cold_approach, salt_bulk_scale_ok, pump_size_factor, salt_inventory_volume, primary_installation, circulator_count, helium_hx_volume, tube_mass, consumables_annual, design_pump_shaft_hp, secondary_pipe_installation, design_pump_flow_gpm, machine_event_installation, secondary_vendor, salt_design_head_m, machine_event_removal, salt_Re_cold, machine_events, primary_pipe_purchase, primary_vendor, primary_spare, secondary_spare, pump_head_ft, helium_required_fill_mass_kg, secondary_pipe_mass, pump_type_ok, helium_inventory_target_mass_kg, salt_required_fill_mass_kg, helium_price_year, ihx_count, salt_flow_regime_ok, bundle_event_installation, design_pump_head_ft, bundle_event_removal, helium_price_raw, design_pump_size_ok, ihx_lmtd, represented_fill_ok, salt_velocity_hot, hx_mass, helium_inventory_mass, salt_pump_count, motor_electric_hp, secondary_pumps_cost, motor_factor_ok, sheets_mass, spares_cost, salt_head_ok, salt_price_year, circulator_electric_MW, design_pump_size_factor, ihx_capacity_ok, salt_pump_shaft_MW, ihx_duty_MW, installed_total, bundle_events, helium_price_transfer_validated, salt_design_flow_kg_s, circulator_suction_Pa, motor_base_ok)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(bundle_life_in, n_mod_in, helium_purchased_mass_kg_in, primary_electric_MW_in, q_ihx_MW_in, n_loops_in, salt_purchased_mass_kg_in, helium_gamma_in, accessory_mass_in, enabled_in, mdot_loop_in, stainless_fabrication_usd2017_per_kg_in, eta_motor_in, salt_design_eta_p_in, years_in, tube_wall_in, helium_cp_in, machine_life_in, inventory_reserve_in, salt_design_flow_kg_s_in, discount_in, removal_multiplier_in, salt_design_eta_motor_in, primary_shaft_MW_in, costscale_in, shell_wall_in, makeup_fraction_in, helium_hot_K_in, eta_p_in, secondary_head_in, salt_design_head_m_in, sourcefitargument_C_in, helium_suction_K_in, helium_design_shaft_MW_in, layout_multiplier_in, saltprice_source_choice_in, dp_loop_in, helium_design_suction_Pa_in, helium_discharge_Pa_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_cooling_equipment.cooling_equipment_impl import (
            run_cooling_equipment,
        )

        # Execute implementation - returns tuple of values
        salt_pump_flow, salt_represented_fill_margin_kg, ihx_hot_approach, exchangers_cost, pressure_qualified, ihx_installed_area, pump_flow_gpm, design_motor_electric_hp, secondary_piping_cost, secondary_installation, cycle_interface_ok, salt_price_raw, salt_velocity_cold, primary_circulators_cost, helium_represented_fill_margin_kg, inventory_cost, salt_expansion_ratio, salt_straight_loss, primary_pipe_installation, salt_unit_price, ihx_capacity_defined, salt_electric_MW, hx_tube_length, secondary_pipe_purchase, hx_installation, salt_inventory_mass, helium_inventory_volume, replacement_annual, salt_makeup_annual, helium_makeup_annual, salt_design_shaft_MW, inventory_complete, heads_mass, helium_design_shaft_MW, primary_design, salt_head_remaining, installation_total, salt_return_C, salt_design_electric_MW, circulator_shaft_MW, circulator_flow, source_volume_ratio, represented_fill_defined, purchased_total, delivered_total, primary_pipe_volume, bundle_event_purchase, bundle_mass, salt_inventory_target_mass_kg, helium_standard_volume, salt_shaft_MW, helium_design_suction_Pa, helium_inventory_cost, machine_off_design_performance_qualified, salt_Re_hot, salt_hx_volume, hx_shell_bore, inventory_source_volume_ok, pump_shaft_hp, ihx_capacity_margin_m2, salt_pipe_volume, design_motor_base_ok, cycle_temperature_gap, primary_piping_cost, hx_purchase, circulator_volume, salt_flow, ihx_required_area, hx_shell_wall, machine_event_purchase, shell_mass, primary_pipe_mass, salt_pump_transfer_validated, pump_size_ok, hx_shell_length, salt_inventory_cost, design_pump_type_ok, design_motor_factor_ok, conversion_heat_MW, ihx_cold_approach, salt_bulk_scale_ok, pump_size_factor, salt_inventory_volume, primary_installation, circulator_count, helium_hx_volume, tube_mass, consumables_annual, design_pump_shaft_hp, secondary_pipe_installation, design_pump_flow_gpm, machine_event_installation, secondary_vendor, salt_design_head_m, machine_event_removal, salt_Re_cold, machine_events, primary_pipe_purchase, primary_vendor, primary_spare, secondary_spare, pump_head_ft, helium_required_fill_mass_kg, secondary_pipe_mass, pump_type_ok, helium_inventory_target_mass_kg, salt_required_fill_mass_kg, helium_price_year, ihx_count, salt_flow_regime_ok, bundle_event_installation, design_pump_head_ft, bundle_event_removal, helium_price_raw, design_pump_size_ok, ihx_lmtd, represented_fill_ok, salt_velocity_hot, hx_mass, helium_inventory_mass, salt_pump_count, motor_electric_hp, secondary_pumps_cost, motor_factor_ok, sheets_mass, spares_cost, salt_head_ok, salt_price_year, circulator_electric_MW, design_pump_size_factor, ihx_capacity_ok, salt_pump_shaft_MW, ihx_duty_MW, installed_total, bundle_events, helium_price_transfer_validated, salt_design_flow_kg_s, circulator_suction_Pa, motor_base_ok = run_cooling_equipment(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cooling_EquipmentOutput(
                salt_pump_flow=salt_pump_flow,
                salt_represented_fill_margin_kg=salt_represented_fill_margin_kg,
                ihx_hot_approach=ihx_hot_approach,
                exchangers_cost=exchangers_cost,
                pressure_qualified=pressure_qualified,
                ihx_installed_area=ihx_installed_area,
                pump_flow_gpm=pump_flow_gpm,
                design_motor_electric_hp=design_motor_electric_hp,
                secondary_piping_cost=secondary_piping_cost,
                secondary_installation=secondary_installation,
                cycle_interface_ok=cycle_interface_ok,
                salt_price_raw=salt_price_raw,
                salt_velocity_cold=salt_velocity_cold,
                primary_circulators_cost=primary_circulators_cost,
                helium_represented_fill_margin_kg=helium_represented_fill_margin_kg,
                inventory_cost=inventory_cost,
                salt_expansion_ratio=salt_expansion_ratio,
                salt_straight_loss=salt_straight_loss,
                primary_pipe_installation=primary_pipe_installation,
                salt_unit_price=salt_unit_price,
                ihx_capacity_defined=ihx_capacity_defined,
                salt_electric_MW=salt_electric_MW,
                hx_tube_length=hx_tube_length,
                secondary_pipe_purchase=secondary_pipe_purchase,
                hx_installation=hx_installation,
                salt_inventory_mass=salt_inventory_mass,
                helium_inventory_volume=helium_inventory_volume,
                replacement_annual=replacement_annual,
                salt_makeup_annual=salt_makeup_annual,
                helium_makeup_annual=helium_makeup_annual,
                salt_design_shaft_MW=salt_design_shaft_MW,
                inventory_complete=inventory_complete,
                heads_mass=heads_mass,
                helium_design_shaft_MW=helium_design_shaft_MW,
                primary_design=primary_design,
                salt_head_remaining=salt_head_remaining,
                installation_total=installation_total,
                salt_return_C=salt_return_C,
                salt_design_electric_MW=salt_design_electric_MW,
                circulator_shaft_MW=circulator_shaft_MW,
                circulator_flow=circulator_flow,
                source_volume_ratio=source_volume_ratio,
                represented_fill_defined=represented_fill_defined,
                purchased_total=purchased_total,
                delivered_total=delivered_total,
                primary_pipe_volume=primary_pipe_volume,
                bundle_event_purchase=bundle_event_purchase,
                bundle_mass=bundle_mass,
                salt_inventory_target_mass_kg=salt_inventory_target_mass_kg,
                helium_standard_volume=helium_standard_volume,
                salt_shaft_MW=salt_shaft_MW,
                helium_design_suction_Pa=helium_design_suction_Pa,
                helium_inventory_cost=helium_inventory_cost,
                machine_off_design_performance_qualified=machine_off_design_performance_qualified,
                salt_Re_hot=salt_Re_hot,
                salt_hx_volume=salt_hx_volume,
                hx_shell_bore=hx_shell_bore,
                inventory_source_volume_ok=inventory_source_volume_ok,
                pump_shaft_hp=pump_shaft_hp,
                ihx_capacity_margin_m2=ihx_capacity_margin_m2,
                salt_pipe_volume=salt_pipe_volume,
                design_motor_base_ok=design_motor_base_ok,
                cycle_temperature_gap=cycle_temperature_gap,
                primary_piping_cost=primary_piping_cost,
                hx_purchase=hx_purchase,
                circulator_volume=circulator_volume,
                salt_flow=salt_flow,
                ihx_required_area=ihx_required_area,
                hx_shell_wall=hx_shell_wall,
                machine_event_purchase=machine_event_purchase,
                shell_mass=shell_mass,
                primary_pipe_mass=primary_pipe_mass,
                salt_pump_transfer_validated=salt_pump_transfer_validated,
                pump_size_ok=pump_size_ok,
                hx_shell_length=hx_shell_length,
                salt_inventory_cost=salt_inventory_cost,
                design_pump_type_ok=design_pump_type_ok,
                design_motor_factor_ok=design_motor_factor_ok,
                conversion_heat_MW=conversion_heat_MW,
                ihx_cold_approach=ihx_cold_approach,
                salt_bulk_scale_ok=salt_bulk_scale_ok,
                pump_size_factor=pump_size_factor,
                salt_inventory_volume=salt_inventory_volume,
                primary_installation=primary_installation,
                circulator_count=circulator_count,
                helium_hx_volume=helium_hx_volume,
                tube_mass=tube_mass,
                consumables_annual=consumables_annual,
                design_pump_shaft_hp=design_pump_shaft_hp,
                secondary_pipe_installation=secondary_pipe_installation,
                design_pump_flow_gpm=design_pump_flow_gpm,
                machine_event_installation=machine_event_installation,
                secondary_vendor=secondary_vendor,
                salt_design_head_m=salt_design_head_m,
                machine_event_removal=machine_event_removal,
                salt_Re_cold=salt_Re_cold,
                machine_events=machine_events,
                primary_pipe_purchase=primary_pipe_purchase,
                primary_vendor=primary_vendor,
                primary_spare=primary_spare,
                secondary_spare=secondary_spare,
                pump_head_ft=pump_head_ft,
                helium_required_fill_mass_kg=helium_required_fill_mass_kg,
                secondary_pipe_mass=secondary_pipe_mass,
                pump_type_ok=pump_type_ok,
                helium_inventory_target_mass_kg=helium_inventory_target_mass_kg,
                salt_required_fill_mass_kg=salt_required_fill_mass_kg,
                helium_price_year=helium_price_year,
                ihx_count=ihx_count,
                salt_flow_regime_ok=salt_flow_regime_ok,
                bundle_event_installation=bundle_event_installation,
                design_pump_head_ft=design_pump_head_ft,
                bundle_event_removal=bundle_event_removal,
                helium_price_raw=helium_price_raw,
                design_pump_size_ok=design_pump_size_ok,
                ihx_lmtd=ihx_lmtd,
                represented_fill_ok=represented_fill_ok,
                salt_velocity_hot=salt_velocity_hot,
                hx_mass=hx_mass,
                helium_inventory_mass=helium_inventory_mass,
                salt_pump_count=salt_pump_count,
                motor_electric_hp=motor_electric_hp,
                secondary_pumps_cost=secondary_pumps_cost,
                motor_factor_ok=motor_factor_ok,
                sheets_mass=sheets_mass,
                spares_cost=spares_cost,
                salt_head_ok=salt_head_ok,
                salt_price_year=salt_price_year,
                circulator_electric_MW=circulator_electric_MW,
                design_pump_size_factor=design_pump_size_factor,
                ihx_capacity_ok=ihx_capacity_ok,
                salt_pump_shaft_MW=salt_pump_shaft_MW,
                ihx_duty_MW=ihx_duty_MW,
                installed_total=installed_total,
                bundle_events=bundle_events,
                helium_price_transfer_validated=helium_price_transfer_validated,
                salt_design_flow_kg_s=salt_design_flow_kg_s,
                circulator_suction_Pa=circulator_suction_Pa,
                motor_base_ok=motor_base_ok,
            )
        )
