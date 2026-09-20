package mfe_cooling_equipment {
    private import ScalarValues::*;
    calc def 'Cooling Equipment' {
        doc /*
Conceptual helium/HITEC cooling equipment. WI-078: selected machine design-point pumping duty/pressure and salt flow/head/efficiencies price installed packages, spares and replacements independently of operating demand. The 50hp helium normalization is pumping duty, not motor nameplate. Purchased fluid stocks are supplied; required fill derives from represented volumes and operating density. Reserve targets are suggestions only. Signed represented-fill margins are purchased minus required kg; represented_fill_ok is their nonnegative conjunction, not complete inventory qualification. Off-design machine performance remains unqualified. Source: work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md and architecture-review-r2.md. Basis: approved MR-7 interpretation; unchanged source price correlations, fixed HX/pipe geometry and operating closures. Guarded manual completion implements the equations below; all costs are USD2025 annual-CPI purchasing-power proxies. This is a priced subset, with unpriced valves, supports, insulation, salt auxiliaries and conversion-side inventory. Pressure qualification and helium/salt machine technology transfers are unvalidated. Geometry and lifecycle assumptions are agent-selected scenarios.

Output basis: HX masses and duty per IHX; HX areas per IHX; salt_flow per circuit; all pipe and inventory quantities plant total; machine outputs per machine except counts.

Normative equations: two parallel machines and one fixed OB exchanger per circuit. BNL machine1978=550000*(0.5+0.5*(p_suction/(735*6894.757293168))*(shaft_W/745.6998715822702/50)^0.28); package=1.2*machine. Design fee130000 once. Installation=0.27*1.155*vendor; procurement services remain CAS30. Tube count14852, OD0.01905m, length11.6m; area=pi*OD*length*count. Tube mass=8000*area*t*(1-t/OD). Shell bore3.2m, length13m; annular shell and spherical pair of heads; two gross0.6m tubesheets; explicit accessory mass. Required area=(Q_IHX/N)/(UF*LMTD), UF=267.8e6/[area*(35-19.3)/ln(35/19.3)]. Hot/cold approaches are helium hot minus738.15K and suction minus543.15K.

Primary mains OD1.3/1.1m,65mm walls,50m each; nine branches per leg, ID=mainID/3,30mm wall, length=(4000/9-100)/18. Straight annular steel times(1+14440/66560) prices fittings. Secondary ID0.4m,20mm wall,50m each leg. All lengths scale with layout_multiplier. Delivered fabrication=stainless_fabrication_usd2017_per_kg_in (nominal310USD2017/kg); pipe field labor=0.50*fabrication. HX installation=0.024 labor+0.002 material. Salt shell void=pi*1.6^2*11.6-tube_outer_volume-accessory_mass/8000. Inventory volume is pipe+shell void only; cold density gives required fill; times(1+reserve) gives an optional target. Purchased mass is independently supplied. Helium volume=pipe+61.5*N, pressure discharge, arithmetic-mean hot/suction temperature, ideal gas R=cp*(gamma-1)/gamma, supplies the required fill diagnostic. Standard volume uses101325Pa/288.15K;14USD2024/m3. Source879m3/9circuit check is independent, never an added inventory.

Salt cp1560, density=max(2080-0.733*T_C,1000), viscosity=max(0.00622-1.02e-5*T_C,1e-6). Flow=Q_IHX*1e6/(1560*195); two pumps/circuit. Shaft=mdot*g*head/eta_p; electric=shaft/eta_motor. Pump CE500=3*exp(9.7171-0.6019*ln(S)+0.0519*ln(S)^2), S=Qgpm*sqrt(Hft). TEFC motor CE500=1.3*exp(5.8259+0.13141*l+0.053255*l^2+0.028628*l^3-0.0035549*l^4), l=ln(electric_hp). Pump domains S400..100000; type50..3500gpm,50..200ft,<=200shaft hp; motor base1..700hp, factor1..250hp. Salt pump installation repeats0.27*1.155. Straight losses sum f*L/D*v^2/(2g); f64/Re below2300, smooth Haaland(-1.8log10(6.9/Re))^-2 otherwise; transitional2300..4000 is flagged. Saltprice0=1.23USD2011/kg;1=2.53USD2021/kg; bulk category >=10millionkg.

CPI1978=65.2,2006=201.6,2011=224.9,2017=245.1,2021=271.0,2024=313.7,2025=321.9. All prices multiply321.9/sourceCPI and costscale. One uninstalled spare of each machine per plant. Machine replacement repeats active purchases+installation+removal_multiplier*installation; bundle replacement repeats tube+accessory fabrication plus0.026 installation and0.024*removal_multiplier. Events k*life<years, discounted(1+r)^(-time), annualized r/(1-(1+r)^(-years)) or1/years at zero rate. Makeup=chosen initial inventory cost*makeup_fraction. Delivered exclusion=active primary packages+primary spare+HX+both pipe fabrication bills; no installation, design fee, inventory, salt pumps or future replacement. Installed total=purchased total+installation total. Seven child costs sum installed total. Sourcefitargument above465C fails physical-interface screen.

Disabled returns finite zeros before active guards. Active requires finite numeric inputs, positive flows/temperatures/dimensions/lives, integer n_loops and n_mod=1, gamma>1,0<efficiencies<=1, shaft<=electric, tube wall<OD/2, suction pressure>0, positive terminal approaches and shell void; invalid arithmetic inputs raise ValueError. Range/capacity failures return false diagnostics with evaluable extrapolated prices.

**Source**: BNL helium quote; ANL2018 cost algorithms; Seider2009 third edition Chapter22; NETL2002; ORNL installation; EU DEMO OB geometry; NREL SSC properties; INL2022 inventory; USGS2025 helium; annual CPI.
**Reference**: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md (released corrective details); primary-candidate.md; work/orchestration/goals/installed-cooling-equipment-costs/evidence/round3/secondary-methods.md; evidence/round2/hx-method-check.md. These records link screened registered originals and exact source locations.
**Last Updated**: 2026-09-18
        */
        // WI-078 supplied price point and stock; no demand-selected purchase.
        // [MW] Selected design input; active evaluation requires an explicit value.
        in attribute helium_design_shaft_MW_in : Real;
        // [Pa] Selected design input; active evaluation requires an explicit value.
        in attribute helium_design_suction_Pa_in : Real;
        // [kg/s] Selected design input; active evaluation requires an explicit value.
        in attribute salt_design_flow_kg_s_in : Real;
        // [m] Selected design input; active evaluation requires an explicit value.
        in attribute salt_design_head_m_in : Real;
        // [1] Selected design input; active evaluation requires an explicit value.
        in attribute salt_design_eta_p_in : Real;
        // [1] Selected design input; active evaluation requires an explicit value.
        in attribute salt_design_eta_motor_in : Real;
        // [kg] Selected design input; active evaluation requires an explicit value.
        in attribute helium_purchased_mass_kg_in : Real;
        // [kg] Selected design input; active evaluation requires an explicit value.
        in attribute salt_purchased_mass_kg_in : Real;
        // [1]
        in attribute enabled_in : Boolean default := false;
        // [1]
        in attribute n_mod_in : Real default := 1;
        // [1]
        in attribute n_loops_in : Real default := 18;
        // [kg/s]
        in attribute mdot_loop_in : Real default := 156.575;
        // [Pa]
        in attribute dp_loop_in : Real default := 159300;
        // [K]
        in attribute helium_suction_K_in : Real default := 567.221;
        // [Pa]
        in attribute helium_discharge_Pa_in : Real default := 8000000.0;
        // [K]
        in attribute helium_hot_K_in : Real default := 773.15;
        // [J/(kg K)]
        in attribute helium_cp_in : Real default := 5193;
        // [1]
        in attribute helium_gamma_in : Real default := 1.6666666666666667;
        // [MW]
        in attribute primary_shaft_MW_in : Real default := 86.7762;
        // [MW]
        in attribute primary_electric_MW_in : Real default := 86.7762;
        // [MW]
        in attribute q_ihx_MW_in : Real default := 3013.914942;
        // [1]
        in attribute layout_multiplier_in : Real default := 1;
        // [m]
        in attribute tube_wall_in : Real default := 0.0015;
        // [m]
        in attribute shell_wall_in : Real default := 0.2;
        // [kg]
        in attribute accessory_mass_in : Real default := 10000;
        // [m]
        in attribute secondary_head_in : Real default := 40;
        // [1]
        in attribute eta_p_in : Real default := 0.75;
        // [1]
        in attribute eta_motor_in : Real default := 0.95;
        // [year]
        in attribute machine_life_in : Real default := 10;
        // [year]
        in attribute bundle_life_in : Real default := 15;
        // [year]
        in attribute years_in : Real default := 30;
        // [1]
        in attribute discount_in : Real default := 0.07;
        // [1/year]
        in attribute makeup_fraction_in : Real default := 0.001;
        // [1]
        in attribute inventory_reserve_in : Real default := 0.1;
        // [1]
        in attribute removal_multiplier_in : Real default := 1;
        // [1]
        in attribute saltprice_source_choice_in : Real default := 0;
        // [1]
        in attribute costscale_in : Real default := 1;
        // [USD2017/kg], one shared finished-fabrication source rate.
        in attribute stainless_fabrication_usd2017_per_kg_in : Real default := 310 {
            doc /* **Source**: knowledge/sources/anl_2018_report_on_the_update_of_fuel_cycle_cost_algorithms/output.md **Ref**: sections 2.4, 3.6.2-3.6.3, printed 26-27. **Basis**: 310000 USD per metric tonne / 1000 kg per tonne = 310 USD2017/kg, delivered finished stainless fabrication. Shared by initial HX, both pipe bills and future bundle. January2017 source basis uses inherited annual CPI2017=245.1 to CPI2025=321.9 purchasing-power proxy, not equipment escalation. Conditional 240/360 source-family alternatives hold the carbon base fixed at 120 USD2017/kg times 2/3; target transfer and missing scope remain unbounded. **Last Updated**: 2026-09-19 */
        }
        // [degC]
        in attribute sourcefitargument_C_in : Real default := 480;
        // [USD2025_CPI_proxy]
        out attribute primary_circulators_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute primary_piping_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute exchangers_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute secondary_pumps_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute secondary_piping_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute inventory_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute spares_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute purchased_total : Real;
        // [USD2025_CPI_proxy]
        out attribute installation_total : Real;
        // [USD2025_CPI_proxy]
        out attribute installed_total : Real;
        // [USD2025_CPI_proxy]
        out attribute delivered_total : Real;
        // [USD2025_CPI_proxy]
        out attribute primary_vendor : Real;
        // [USD2025_CPI_proxy]
        out attribute primary_installation : Real;
        // [USD2025_CPI_proxy]
        out attribute primary_design : Real;
        // [USD2025_CPI_proxy]
        out attribute primary_spare : Real;
        // [USD2025_CPI_proxy]
        out attribute secondary_vendor : Real;
        // [USD2025_CPI_proxy]
        out attribute secondary_installation : Real;
        // [USD2025_CPI_proxy]
        out attribute secondary_spare : Real;
        // [USD2025_CPI_proxy]
        out attribute hx_purchase : Real;
        // [USD2025_CPI_proxy]
        out attribute hx_installation : Real;
        // [USD2025_CPI_proxy]
        out attribute primary_pipe_purchase : Real;
        // [USD2025_CPI_proxy]
        out attribute primary_pipe_installation : Real;
        // [USD2025_CPI_proxy]
        out attribute secondary_pipe_purchase : Real;
        // [USD2025_CPI_proxy]
        out attribute secondary_pipe_installation : Real;
        // [USD2025_CPI_proxy]
        out attribute helium_inventory_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute salt_inventory_cost : Real;
        // [USD2025_CPI_proxy]
        out attribute machine_event_purchase : Real;
        // [USD2025_CPI_proxy]
        out attribute machine_event_installation : Real;
        // [USD2025_CPI_proxy]
        out attribute machine_event_removal : Real;
        // [USD2025_CPI_proxy]
        out attribute bundle_event_purchase : Real;
        // [USD2025_CPI_proxy]
        out attribute bundle_event_installation : Real;
        // [USD2025_CPI_proxy]
        out attribute bundle_event_removal : Real;
        // [USD2025_CPI_proxy/year]
        out attribute replacement_annual : Real;
        // [USD2025_CPI_proxy/year]
        out attribute consumables_annual : Real;
        // [USD2025_CPI_proxy/year]
        out attribute helium_makeup_annual : Real;
        // [USD2025_CPI_proxy/year]
        out attribute salt_makeup_annual : Real;
        // [MW]
        out attribute salt_electric_MW : Real;
        // [MW]
        out attribute salt_shaft_MW : Real;
        // [MW]
        out attribute conversion_heat_MW : Real;
        // [MW]
        out attribute circulator_shaft_MW : Real;
        // [MW]
        out attribute circulator_electric_MW : Real;
        // [MW]
        out attribute ihx_duty_MW : Real;
        // [kg]
        out attribute tube_mass : Real;
        // [kg]
        out attribute shell_mass : Real;
        // [kg]
        out attribute heads_mass : Real;
        // [kg]
        out attribute sheets_mass : Real;
        // [kg]
        out attribute hx_mass : Real;
        // [kg]
        out attribute bundle_mass : Real;
        // [kg]
        out attribute primary_pipe_mass : Real;
        // [kg]
        out attribute secondary_pipe_mass : Real;
        // [kg]
        out attribute helium_inventory_mass : Real;
        // [kg]
        out attribute salt_inventory_mass : Real;
        // [m^3]
        out attribute primary_pipe_volume : Real;
        // [m^3]
        out attribute helium_hx_volume : Real;
        // [m^3]
        out attribute helium_inventory_volume : Real;
        // [m^3]
        out attribute helium_standard_volume : Real;
        // [m^3]
        out attribute salt_pipe_volume : Real;
        // [m^3]
        out attribute salt_hx_volume : Real;
        // [m^3]
        out attribute salt_inventory_volume : Real;
        // [m^2]
        out attribute ihx_installed_area : Real;
        // [m^2]
        out attribute ihx_required_area : Real;
        // [1]
        out attribute circulator_count : Real;
        // [1]
        out attribute salt_pump_count : Real;
        // [1]
        out attribute source_volume_ratio : Real;
        // [1]
        out attribute salt_expansion_ratio : Real;
        // [1]
        out attribute salt_Re_hot : Real;
        // [1]
        out attribute salt_Re_cold : Real;
        // [1]
        out attribute pump_size_factor : Real;
        // [1]
        out attribute pump_shaft_hp : Real;
        // [1]
        out attribute motor_electric_hp : Real;
        // [1]
        out attribute machine_events : Real;
        // [1]
        out attribute bundle_events : Real;
        // [1]
        out attribute salt_price_raw : Real;
        // [1]
        out attribute salt_price_year : Real;
        // [1]
        out attribute salt_unit_price : Real;
        // [1]
        out attribute helium_price_raw : Real;
        // [1]
        out attribute helium_price_year : Real;
        // [kg/s]
        out attribute circulator_flow : Real;
        // [m^3/s]
        out attribute circulator_volume : Real;
        // [Pa]
        out attribute circulator_suction_Pa : Real;
        // [K]
        out attribute ihx_hot_approach : Real;
        // [K]
        out attribute ihx_cold_approach : Real;
        // [K]
        out attribute ihx_lmtd : Real;
        // [kg/s]
        out attribute salt_flow : Real;
        // [m/s]
        out attribute salt_velocity_hot : Real;
        // [m/s]
        out attribute salt_velocity_cold : Real;
        // [m]
        out attribute salt_straight_loss : Real;
        // [m]
        out attribute salt_head_remaining : Real;
        // [degC]
        out attribute salt_return_C : Real;
        // [K]
        out attribute cycle_temperature_gap : Real;
        // [USgal/min]
        out attribute pump_flow_gpm : Real;
        // [ft]
        out attribute pump_head_ft : Real;
        // [1]
        out attribute ihx_capacity_ok : Boolean;
        // [1]
        out attribute pump_size_ok : Boolean;
        // [1]
        out attribute pump_type_ok : Boolean;
        // [1]
        out attribute motor_base_ok : Boolean;
        // [1]
        out attribute motor_factor_ok : Boolean;
        // [1]
        out attribute salt_head_ok : Boolean;
        // [1]
        out attribute salt_flow_regime_ok : Boolean;
        // [1]
        out attribute cycle_interface_ok : Boolean;
        // [1]
        out attribute salt_bulk_scale_ok : Boolean;
        // [1]
        out attribute inventory_source_volume_ok : Boolean;
        // [1]
        out attribute pressure_qualified : Boolean;
        // [1]
        out attribute helium_price_transfer_validated : Boolean;
        // [1]
        out attribute salt_pump_transfer_validated : Boolean;
        // [1]
        out attribute inventory_complete : Boolean;
        // [kg/s], per machine
        out attribute salt_pump_flow : Real;
        // [MW], per machine
        out attribute salt_pump_shaft_MW : Real;
        // [1], per plant
        out attribute ihx_count : Real;
        // WI-068 pure geometry interfaces [m]. These are the same quantities
        // used by this calculation's installed exchanger pricing, not new inputs.
        out attribute hx_shell_bore : Real;
        out attribute hx_shell_wall : Real;
        out attribute hx_shell_length : Real;
        out attribute hx_tube_length : Real;
        // [MW] WI-078 selected design or represented-fill diagnostic.
        out attribute helium_design_shaft_MW : Real;
        // [Pa] WI-078 selected design or represented-fill diagnostic.
        out attribute helium_design_suction_Pa : Real;
        // [kg/s] WI-078 selected design or represented-fill diagnostic.
        out attribute salt_design_flow_kg_s : Real;
        // [m] WI-078 selected design or represented-fill diagnostic.
        out attribute salt_design_head_m : Real;
        // [MW] WI-078 selected design or represented-fill diagnostic.
        out attribute salt_design_shaft_MW : Real;
        // [MW] WI-078 selected design or represented-fill diagnostic.
        out attribute salt_design_electric_MW : Real;
        // [gpm] WI-078 selected design or represented-fill diagnostic.
        out attribute design_pump_flow_gpm : Real;
        // [ft] WI-078 selected design or represented-fill diagnostic.
        out attribute design_pump_head_ft : Real;
        // [gpm*sqrt(ft)] WI-078 selected design or represented-fill diagnostic.
        out attribute design_pump_size_factor : Real;
        // [hp] WI-078 selected design or represented-fill diagnostic.
        out attribute design_pump_shaft_hp : Real;
        // [hp] WI-078 selected design or represented-fill diagnostic.
        out attribute design_motor_electric_hp : Real;
        // [kg] WI-078 selected design or represented-fill diagnostic.
        out attribute helium_required_fill_mass_kg : Real;
        // [kg] WI-078 selected design or represented-fill diagnostic.
        out attribute salt_required_fill_mass_kg : Real;
        // [kg] WI-078 selected design or represented-fill diagnostic.
        out attribute helium_inventory_target_mass_kg : Real;
        // [kg] WI-078 selected design or represented-fill diagnostic.
        out attribute salt_inventory_target_mass_kg : Real;
        // [kg] WI-078 selected design or represented-fill diagnostic.
        out attribute helium_represented_fill_margin_kg : Real;
        // [kg] WI-078 selected design or represented-fill diagnostic.
        out attribute salt_represented_fill_margin_kg : Real;
        out attribute design_pump_size_ok : Boolean;
        out attribute design_pump_type_ok : Boolean;
        out attribute design_motor_base_ok : Boolean;
        out attribute design_motor_factor_ok : Boolean;
        out attribute machine_off_design_performance_qualified : Boolean;
        out attribute represented_fill_ok : Boolean;
        // [1] 1 active partial inventory evaluation; 0 dormant.
        out attribute represented_fill_defined : Real;

    }
}
