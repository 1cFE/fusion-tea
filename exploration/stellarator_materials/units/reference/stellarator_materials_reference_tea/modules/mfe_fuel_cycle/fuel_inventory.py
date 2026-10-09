"""Fuel_InventoryModule Module Wrapper

TEAx module for Fuel_Inventory calculation.

Nominal stage inventory and deterministic-delay commissioning supply; typed manual completion.
B=P*1e6/(Q*c), F=B/f, U=F-B, R=rU, L=(1-r)U, J=TBR*B, S=eta*J [T atoms/s].
Feed=F*tau_feed; plasma=n_T0*V/(1+alpha_n); processor=U*tau_process;
blanket=J*tau_blanket; extraction=J*tau_extract; buffer=F*tau_buffer;
reserve=F*q*tau_reserve [T atoms]. I_work=sum(first six); I_total=I_work+reserve.
Processor loss occurs once at its outlet; extraction efficiency acts once at final breeder outlet.
Feed, plasma, buffer and reserve start prefilled; processor, breeder zone and extraction start empty.
Recycle delay=tau_process; breeder delay=tau_blanket+tau_extract; H=max(delays)+extension.
D(t)=F*t-R*max(t-tau_process,0)-S*max(t-tau_blanket-tau_extract,0).
d=max(D at 0, each return delay and H); prefill=feed+plasma+buffer;
M0=prefill+reserve+d. The other stage fills are inside d, not purchased again.
k=lambda*H must be <1. A=k*(M0+J*H)/(1-k); conservative startup=M0+A.
This protects decay including extra startup stock itself, under an abstract usable supply boundary.
It is not an exact transient minimum or qualified ignition/ramp design; source compartment residence
estimates are transferred to deterministic delays. Decay-free nominal stage stocks use separate
replacement demand lambda*I_total. max_decay_residence=max(lambda*each of the five residence inputs),
excluding the reserve interruption duration, reports approximation scale without imposing a qualification threshold.
All atom stocks multiply m_T for kg. T rates export kg/s and 86400 times that for kg/day.
D+T injection/exhaust use equal isotope atom rates times (m_D+m_T), excluding ash and carrier mass.
Annual running amounts multiply availability*s_per_year. Annual decay uses all s_per_year.
Signed operating makeup=(B+L-S+lambda*I_total)*m_T; external shortfall=max(signed,0).
Annual signed makeup=((B+L-S)*availability+lambda*I_total)*m_T*s_per_year.
Passive shutdown loss=-expm1(-lambda*t_shutdown)*I_total*m_T; remaining=exp(-lambda*t_shutdown)*I_total*m_T to retain small positive late stock.
Maintained nominal inventory persists through shutdown; passive remaining is a separate policy.
Active: finite inputs/intermediates; positive power, energy, masses, year; f,eta in (0,1]; r,q,
availability in [0,1]; alpha_n>-1; nonnegative TBR, density, volume, times and decay; G_stock=0.
Invalid arithmetic/fractions raise ValueError. Undefined breeding flag 0 preserves finite diagnostic
carriers (J=0 when breeding_defined=0) and non-breeding stocks/flows, but production-dependent stocks, total/startup and supply
are physically undefined, never a zero-production prediction. defined_flag propagates that status.
Dormant enabled=false forwards held_inventory into total_atoms and returns other zero carriers
with defined_flag=0; no active stock claim. Generic legacy flow arithmetic remains unchanged.
Unsupported wall retention, permeation, detritiation, impurities and bypass remain omitted limitations.
*Source**: work/active/WI-069_fuel-inventory-and-startup/design.md
*Reference**: knowledge/research/pending/20260919-074901_fuel-inventory-residence-startup.md; evidence/proposed-abi.md
*Basis**: independently reviewed conditional scenario; source-derived residence cases, explicit storage policy.
Input units (flat Real ABI; explicit physical meaning):
in attribute enabled_in : Boolean default := false; 1; activation
in attribute held_inventory_in : Real default := 0.0; T atoms; dormant legacy amount
in attribute p_fus_in : Real; MW
in attribute q_eff_in : Real; MeV/reaction
in attribute mev_to_joules_in : Real; J/MeV
in attribute burn_fraction_in : Real; 1; (0,1]
in attribute t_recycle_in : Real; 1; [0,1]
in attribute tbr_available_in : Real; T atoms/reaction
in attribute breeding_defined_in : Real default := 1.0; 1; exact 0/1
in attribute eta_extract_in : Real; 1; (0,1]
in attribute lambda_T_in : Real; 1/s
in attribute G_stock_in : Real; T atoms/s; active zero
in attribute m_T_kg_in : Real; kg/T atom
in attribute m_D_kg_in : Real default := 0.0; kg/D atom
in attribute plasma_volume_in : Real default := 0.0; m^3
in attribute n_T0_in : Real default := 0.0; T atoms/m^3
in attribute alpha_n_in : Real default := 0.0; 1; > -1
in attribute tau_feed_in : Real default := 0.0; s
in attribute tau_process_in : Real default := 0.0; s
in attribute tau_blanket_in : Real default := 0.0; s
in attribute tau_extract_in : Real default := 0.0; s
in attribute tau_buffer_in : Real default := 0.0; s
in attribute tau_reserve_in : Real default := 0.0; s
in attribute startup_extension_in : Real default := 0.0; s
in attribute shutdown_duration_in : Real default := 0.0; s
in attribute reserve_fraction_in : Real default := 0.0; 1; [0,1]
in attribute availability_in : Real; 1; calendar productive fraction
in attribute s_per_year_in : Real default := 31536000.0; s/year; existing model 8760-hour year
*Last Updated**: 2026-09-19

Inputs:
    - enabled_in: enabled_in parameter
    - startup_extension_in: startup_extension_in parameter
    - p_fus_in: p_fus_in parameter
    - tbr_available_in: tbr_available_in parameter
    - burn_fraction_in: burn_fraction_in parameter
    - breeding_defined_in: breeding_defined_in parameter
    - q_eff_in: q_eff_in parameter
    - alpha_n_in: alpha_n_in parameter
    - m_D_kg_in: m_D_kg_in parameter
    - tau_buffer_in: tau_buffer_in parameter
    - tau_blanket_in: tau_blanket_in parameter
    - eta_extract_in: eta_extract_in parameter
    - plasma_volume_in: plasma_volume_in parameter
    - n_T0_in: n_T0_in parameter
    - shutdown_duration_in: shutdown_duration_in parameter
    - s_per_year_in: s_per_year_in parameter
    - tau_process_in: tau_process_in parameter
    - held_inventory_in: held_inventory_in parameter
    - tau_extract_in: tau_extract_in parameter
    - m_T_kg_in: m_T_kg_in parameter
    - G_stock_in: G_stock_in parameter
    - reserve_fraction_in: reserve_fraction_in parameter
    - lambda_T_in: lambda_T_in parameter
    - availability_in: availability_in parameter
    - t_recycle_in: t_recycle_in parameter
    - tau_reserve_in: tau_reserve_in parameter
    - mev_to_joules_in: mev_to_joules_in parameter
    - tau_feed_in: tau_feed_in parameter

Outputs:
    - recycle_kg_day: recycle_kg_day result [kg]
    - production_kg_s: production_kg_s result [kg]
    - shutdown_remaining_kg: shutdown_remaining_kg result [kg]
    - annual_recycle_loss_kg: annual_recycle_loss_kg result [kg]
    - extraction_loss_kg_s: extraction_loss_kg_s result [kg]
    - working_kg: working_kg result [kg]
    - startup_deficit_atoms: startup_deficit_atoms result [T]
    - injection_kg_s: injection_kg_s result [kg]
    - annual_makeup_signed_kg: annual_makeup_signed_kg result [kg]
    - max_decay_residence: max_decay_residence result
    - burn_kg_s: burn_kg_s result [kg]
    - extracted_kg_day: extracted_kg_day result [kg]
    - plasma_atoms: plasma_atoms result [T]
    - buffer_atoms: buffer_atoms result [T]
    - blanket_kg: blanket_kg result [kg]
    - extraction_atoms: extraction_atoms result [T]
    - dt_injection_kg_s: dt_injection_kg_s result [kg]
    - annual_recycle_kg: annual_recycle_kg result [kg]
    - dt_injection_kg_day: dt_injection_kg_day result [kg]
    - buffer_kg: buffer_kg result [kg]
    - exhaust_kg_day: exhaust_kg_day result [kg]
    - external_shortfall_kg_s: external_shortfall_kg_s result [kg]
    - blanket_atoms: blanket_atoms result [T]
    - injection_kg_day: injection_kg_day result [kg]
    - annual_production_kg: annual_production_kg result [kg]
    - extraction_loss_kg_day: extraction_loss_kg_day result [kg]
    - startup_conservative_atoms: startup_conservative_atoms result [T]
    - feed_atoms: feed_atoms result [T]
    - recycle_delay_s: recycle_delay_s result [s]
    - annual_extraction_loss_kg: annual_extraction_loss_kg result [kg]
    - annual_extracted_kg: annual_extracted_kg result [kg]
    - startup_decay_allowance_kg: startup_decay_allowance_kg result [kg]
    - startup_conservative_kg: startup_conservative_kg result [kg]
    - burn_kg_day: burn_kg_day result [kg]
    - total_kg: total_kg result [kg]
    - startup_deficit_kg: startup_deficit_kg result [kg]
    - dt_processor_kg_day: dt_processor_kg_day result [kg]
    - dt_processor_kg_s: dt_processor_kg_s result [kg]
    - prefill_kg: prefill_kg result [kg]
    - decay_kg_s: decay_kg_s result [kg]
    - working_atoms: working_atoms result [T]
    - breeding_delay_s: breeding_delay_s result [s]
    - feed_kg: feed_kg result [kg]
    - prefill_atoms: prefill_atoms result [T]
    - reserve_atoms: reserve_atoms result [T]
    - annual_external_shortfall_kg: annual_external_shortfall_kg result [kg]
    - annual_injection_kg: annual_injection_kg result [kg]
    - exhaust_kg_s: exhaust_kg_s result [kg]
    - reserve_kg: reserve_kg result [kg]
    - startup_horizon_s: startup_horizon_s result [s]
    - processor_atoms: processor_atoms result [T]
    - plasma_kg: plasma_kg result [kg]
    - startup_decay_allowance_atoms: startup_decay_allowance_atoms result [T]
    - production_kg_day: production_kg_day result [kg]
    - total_atoms: total_atoms result [T]
    - annual_burn_kg: annual_burn_kg result [kg]
    - processor_kg: processor_kg result [kg]
    - extracted_kg_s: extracted_kg_s result [kg]
    - extraction_kg: extraction_kg result [kg]
    - annual_decay_kg: annual_decay_kg result [kg]
    - startup_minimum_atoms: startup_minimum_atoms result [T]
    - recycle_loss_kg_s: recycle_loss_kg_s result [kg]
    - startup_minimum_kg: startup_minimum_kg result [kg]
    - makeup_signed_kg_s: makeup_signed_kg_s result [kg]
    - defined_flag: defined_flag result
    - shutdown_decay_loss_kg: shutdown_decay_loss_kg result [kg]
    - recycle_kg_s: recycle_kg_s result [kg]
    - recycle_loss_kg_day: recycle_loss_kg_day result [kg]
    - calendar_processor_kg_s: calendar_processor_kg_s result [kg]
    - annual_exhaust_kg: annual_exhaust_kg result [kg]

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:93

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:93

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_fuel_cycle/fuel_inventory_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.fuel_inventory_output import Fuel_InventoryOutput


class Fuel_InventoryInput(BaseModel):
    """Input model for Fuel_InventoryModule.

    Attributes:
        enabled_in: enabled_in input
        startup_extension_in: startup_extension_in input
        p_fus_in: p_fus_in input
        tbr_available_in: tbr_available_in input
        burn_fraction_in: burn_fraction_in input
        breeding_defined_in: breeding_defined_in input
        q_eff_in: q_eff_in input
        alpha_n_in: alpha_n_in input
        m_D_kg_in: m_D_kg_in input
        tau_buffer_in: tau_buffer_in input
        tau_blanket_in: tau_blanket_in input
        eta_extract_in: eta_extract_in input
        plasma_volume_in: plasma_volume_in input
        n_T0_in: n_T0_in input
        shutdown_duration_in: shutdown_duration_in input
        s_per_year_in: s_per_year_in input
        tau_process_in: tau_process_in input
        held_inventory_in: held_inventory_in input
        tau_extract_in: tau_extract_in input
        m_T_kg_in: m_T_kg_in input
        G_stock_in: G_stock_in input
        reserve_fraction_in: reserve_fraction_in input
        lambda_T_in: lambda_T_in input
        availability_in: availability_in input
        t_recycle_in: t_recycle_in input
        tau_reserve_in: tau_reserve_in input
        mev_to_joules_in: mev_to_joules_in input
        tau_feed_in: tau_feed_in input
    """
    enabled_in: bool = Field(..., description="enabled_in input")
    startup_extension_in: float = Field(..., description="startup_extension_in input")
    p_fus_in: float = Field(..., description="p_fus_in input")
    tbr_available_in: float = Field(..., description="tbr_available_in input")
    burn_fraction_in: float = Field(..., description="burn_fraction_in input")
    breeding_defined_in: float = Field(..., description="breeding_defined_in input")
    q_eff_in: float = Field(..., description="q_eff_in input")
    alpha_n_in: float = Field(..., description="alpha_n_in input")
    m_D_kg_in: float = Field(..., description="m_D_kg_in input")
    tau_buffer_in: float = Field(..., description="tau_buffer_in input")
    tau_blanket_in: float = Field(..., description="tau_blanket_in input")
    eta_extract_in: float = Field(..., description="eta_extract_in input")
    plasma_volume_in: float = Field(..., description="plasma_volume_in input")
    n_T0_in: float = Field(..., description="n_T0_in input")
    shutdown_duration_in: float = Field(..., description="shutdown_duration_in input")
    s_per_year_in: float = Field(..., description="s_per_year_in input")
    tau_process_in: float = Field(..., description="tau_process_in input")
    held_inventory_in: float = Field(..., description="held_inventory_in input")
    tau_extract_in: float = Field(..., description="tau_extract_in input")
    m_T_kg_in: float = Field(..., description="m_T_kg_in input")
    G_stock_in: float = Field(..., description="G_stock_in input")
    reserve_fraction_in: float = Field(..., description="reserve_fraction_in input")
    lambda_T_in: float = Field(..., description="lambda_T_in input")
    availability_in: float = Field(..., description="availability_in input")
    t_recycle_in: float = Field(..., description="t_recycle_in input")
    tau_reserve_in: float = Field(..., description="tau_reserve_in input")
    mev_to_joules_in: float = Field(..., description="mev_to_joules_in input")
    tau_feed_in: float = Field(..., description="tau_feed_in input")


class Fuel_InventoryModule(ModuleBase[Fuel_InventoryInput, Fuel_InventoryOutput]):
    """TEAx module for Fuel_Inventory calculation.

Nominal stage inventory and deterministic-delay commissioning supply; typed manual completion.
B=P*1e6/(Q*c), F=B/f, U=F-B, R=rU, L=(1-r)U, J=TBR*B, S=eta*J [T atoms/s].
Feed=F*tau_feed; plasma=n_T0*V/(1+alpha_n); processor=U*tau_process;
blanket=J*tau_blanket; extraction=J*tau_extract; buffer=F*tau_buffer;
reserve=F*q*tau_reserve [T atoms]. I_work=sum(first six); I_total=I_work+reserve.
Processor loss occurs once at its outlet; extraction efficiency acts once at final breeder outlet.
Feed, plasma, buffer and reserve start prefilled; processor, breeder zone and extraction start empty.
Recycle delay=tau_process; breeder delay=tau_blanket+tau_extract; H=max(delays)+extension.
D(t)=F*t-R*max(t-tau_process,0)-S*max(t-tau_blanket-tau_extract,0).
d=max(D at 0, each return delay and H); prefill=feed+plasma+buffer;
M0=prefill+reserve+d. The other stage fills are inside d, not purchased again.
k=lambda*H must be <1. A=k*(M0+J*H)/(1-k); conservative startup=M0+A.
This protects decay including extra startup stock itself, under an abstract usable supply boundary.
It is not an exact transient minimum or qualified ignition/ramp design; source compartment residence
estimates are transferred to deterministic delays. Decay-free nominal stage stocks use separate
replacement demand lambda*I_total. max_decay_residence=max(lambda*each of the five residence inputs),
excluding the reserve interruption duration, reports approximation scale without imposing a qualification threshold.
All atom stocks multiply m_T for kg. T rates export kg/s and 86400 times that for kg/day.
D+T injection/exhaust use equal isotope atom rates times (m_D+m_T), excluding ash and carrier mass.
Annual running amounts multiply availability*s_per_year. Annual decay uses all s_per_year.
Signed operating makeup=(B+L-S+lambda*I_total)*m_T; external shortfall=max(signed,0).
Annual signed makeup=((B+L-S)*availability+lambda*I_total)*m_T*s_per_year.
Passive shutdown loss=-expm1(-lambda*t_shutdown)*I_total*m_T; remaining=exp(-lambda*t_shutdown)*I_total*m_T to retain small positive late stock.
Maintained nominal inventory persists through shutdown; passive remaining is a separate policy.
Active: finite inputs/intermediates; positive power, energy, masses, year; f,eta in (0,1]; r,q,
availability in [0,1]; alpha_n>-1; nonnegative TBR, density, volume, times and decay; G_stock=0.
Invalid arithmetic/fractions raise ValueError. Undefined breeding flag 0 preserves finite diagnostic
carriers (J=0 when breeding_defined=0) and non-breeding stocks/flows, but production-dependent stocks, total/startup and supply
are physically undefined, never a zero-production prediction. defined_flag propagates that status.
Dormant enabled=false forwards held_inventory into total_atoms and returns other zero carriers
with defined_flag=0; no active stock claim. Generic legacy flow arithmetic remains unchanged.
Unsupported wall retention, permeation, detritiation, impurities and bypass remain omitted limitations.
*Source**: work/active/WI-069_fuel-inventory-and-startup/design.md
*Reference**: knowledge/research/pending/20260919-074901_fuel-inventory-residence-startup.md; evidence/proposed-abi.md
*Basis**: independently reviewed conditional scenario; source-derived residence cases, explicit storage policy.
Input units (flat Real ABI; explicit physical meaning):
in attribute enabled_in : Boolean default := false; 1; activation
in attribute held_inventory_in : Real default := 0.0; T atoms; dormant legacy amount
in attribute p_fus_in : Real; MW
in attribute q_eff_in : Real; MeV/reaction
in attribute mev_to_joules_in : Real; J/MeV
in attribute burn_fraction_in : Real; 1; (0,1]
in attribute t_recycle_in : Real; 1; [0,1]
in attribute tbr_available_in : Real; T atoms/reaction
in attribute breeding_defined_in : Real default := 1.0; 1; exact 0/1
in attribute eta_extract_in : Real; 1; (0,1]
in attribute lambda_T_in : Real; 1/s
in attribute G_stock_in : Real; T atoms/s; active zero
in attribute m_T_kg_in : Real; kg/T atom
in attribute m_D_kg_in : Real default := 0.0; kg/D atom
in attribute plasma_volume_in : Real default := 0.0; m^3
in attribute n_T0_in : Real default := 0.0; T atoms/m^3
in attribute alpha_n_in : Real default := 0.0; 1; > -1
in attribute tau_feed_in : Real default := 0.0; s
in attribute tau_process_in : Real default := 0.0; s
in attribute tau_blanket_in : Real default := 0.0; s
in attribute tau_extract_in : Real default := 0.0; s
in attribute tau_buffer_in : Real default := 0.0; s
in attribute tau_reserve_in : Real default := 0.0; s
in attribute startup_extension_in : Real default := 0.0; s
in attribute shutdown_duration_in : Real default := 0.0; s
in attribute reserve_fraction_in : Real default := 0.0; 1; [0,1]
in attribute availability_in : Real; 1; calendar productive fraction
in attribute s_per_year_in : Real default := 31536000.0; s/year; existing model 8760-hour year
*Last Updated**: 2026-09-19

Inputs:
    - enabled_in: enabled_in parameter
    - startup_extension_in: startup_extension_in parameter
    - p_fus_in: p_fus_in parameter
    - tbr_available_in: tbr_available_in parameter
    - burn_fraction_in: burn_fraction_in parameter
    - breeding_defined_in: breeding_defined_in parameter
    - q_eff_in: q_eff_in parameter
    - alpha_n_in: alpha_n_in parameter
    - m_D_kg_in: m_D_kg_in parameter
    - tau_buffer_in: tau_buffer_in parameter
    - tau_blanket_in: tau_blanket_in parameter
    - eta_extract_in: eta_extract_in parameter
    - plasma_volume_in: plasma_volume_in parameter
    - n_T0_in: n_T0_in parameter
    - shutdown_duration_in: shutdown_duration_in parameter
    - s_per_year_in: s_per_year_in parameter
    - tau_process_in: tau_process_in parameter
    - held_inventory_in: held_inventory_in parameter
    - tau_extract_in: tau_extract_in parameter
    - m_T_kg_in: m_T_kg_in parameter
    - G_stock_in: G_stock_in parameter
    - reserve_fraction_in: reserve_fraction_in parameter
    - lambda_T_in: lambda_T_in parameter
    - availability_in: availability_in parameter
    - t_recycle_in: t_recycle_in parameter
    - tau_reserve_in: tau_reserve_in parameter
    - mev_to_joules_in: mev_to_joules_in parameter
    - tau_feed_in: tau_feed_in parameter

Outputs:
    - recycle_kg_day: recycle_kg_day result [kg]
    - production_kg_s: production_kg_s result [kg]
    - shutdown_remaining_kg: shutdown_remaining_kg result [kg]
    - annual_recycle_loss_kg: annual_recycle_loss_kg result [kg]
    - extraction_loss_kg_s: extraction_loss_kg_s result [kg]
    - working_kg: working_kg result [kg]
    - startup_deficit_atoms: startup_deficit_atoms result [T]
    - injection_kg_s: injection_kg_s result [kg]
    - annual_makeup_signed_kg: annual_makeup_signed_kg result [kg]
    - max_decay_residence: max_decay_residence result
    - burn_kg_s: burn_kg_s result [kg]
    - extracted_kg_day: extracted_kg_day result [kg]
    - plasma_atoms: plasma_atoms result [T]
    - buffer_atoms: buffer_atoms result [T]
    - blanket_kg: blanket_kg result [kg]
    - extraction_atoms: extraction_atoms result [T]
    - dt_injection_kg_s: dt_injection_kg_s result [kg]
    - annual_recycle_kg: annual_recycle_kg result [kg]
    - dt_injection_kg_day: dt_injection_kg_day result [kg]
    - buffer_kg: buffer_kg result [kg]
    - exhaust_kg_day: exhaust_kg_day result [kg]
    - external_shortfall_kg_s: external_shortfall_kg_s result [kg]
    - blanket_atoms: blanket_atoms result [T]
    - injection_kg_day: injection_kg_day result [kg]
    - annual_production_kg: annual_production_kg result [kg]
    - extraction_loss_kg_day: extraction_loss_kg_day result [kg]
    - startup_conservative_atoms: startup_conservative_atoms result [T]
    - feed_atoms: feed_atoms result [T]
    - recycle_delay_s: recycle_delay_s result [s]
    - annual_extraction_loss_kg: annual_extraction_loss_kg result [kg]
    - annual_extracted_kg: annual_extracted_kg result [kg]
    - startup_decay_allowance_kg: startup_decay_allowance_kg result [kg]
    - startup_conservative_kg: startup_conservative_kg result [kg]
    - burn_kg_day: burn_kg_day result [kg]
    - total_kg: total_kg result [kg]
    - startup_deficit_kg: startup_deficit_kg result [kg]
    - dt_processor_kg_day: dt_processor_kg_day result [kg]
    - dt_processor_kg_s: dt_processor_kg_s result [kg]
    - prefill_kg: prefill_kg result [kg]
    - decay_kg_s: decay_kg_s result [kg]
    - working_atoms: working_atoms result [T]
    - breeding_delay_s: breeding_delay_s result [s]
    - feed_kg: feed_kg result [kg]
    - prefill_atoms: prefill_atoms result [T]
    - reserve_atoms: reserve_atoms result [T]
    - annual_external_shortfall_kg: annual_external_shortfall_kg result [kg]
    - annual_injection_kg: annual_injection_kg result [kg]
    - exhaust_kg_s: exhaust_kg_s result [kg]
    - reserve_kg: reserve_kg result [kg]
    - startup_horizon_s: startup_horizon_s result [s]
    - processor_atoms: processor_atoms result [T]
    - plasma_kg: plasma_kg result [kg]
    - startup_decay_allowance_atoms: startup_decay_allowance_atoms result [T]
    - production_kg_day: production_kg_day result [kg]
    - total_atoms: total_atoms result [T]
    - annual_burn_kg: annual_burn_kg result [kg]
    - processor_kg: processor_kg result [kg]
    - extracted_kg_s: extracted_kg_s result [kg]
    - extraction_kg: extraction_kg result [kg]
    - annual_decay_kg: annual_decay_kg result [kg]
    - startup_minimum_atoms: startup_minimum_atoms result [T]
    - recycle_loss_kg_s: recycle_loss_kg_s result [kg]
    - startup_minimum_kg: startup_minimum_kg result [kg]
    - makeup_signed_kg_s: makeup_signed_kg_s result [kg]
    - defined_flag: defined_flag result
    - shutdown_decay_loss_kg: shutdown_decay_loss_kg result [kg]
    - recycle_kg_s: recycle_kg_s result [kg]
    - recycle_loss_kg_day: recycle_loss_kg_day result [kg]
    - calendar_processor_kg_s: calendar_processor_kg_s result [kg]
    - annual_exhaust_kg: annual_exhaust_kg result [kg]

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:93

    SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:93

    Calculation Specification:
        enabled_in = false
        held_inventory_in = 0.0
        breeding_defined_in = 1.0
        m_D_kg_in = 0.0
        plasma_volume_in = 0.0
        n_T0_in = 0.0
        alpha_n_in = 0.0
        tau_feed_in = 0.0
        tau_process_in = 0.0
        tau_blanket_in = 0.0
        tau_extract_in = 0.0
        tau_buffer_in = 0.0
        tau_reserve_in = 0.0
        startup_extension_in = 0.0
        shutdown_duration_in = 0.0
        reserve_fraction_in = 0.0
        s_per_year_in = 31536000.0
        
Documentation:
Nominal stage inventory and deterministic-delay commissioning supply; typed manual completion.
B=P*1e6/(Q*c), F=B/f, U=F-B, R=rU, L=(1-r)U, J=TBR*B, S=eta*J [T atoms/s].
Feed=F*tau_feed; plasma=n_T0*V/(1+alpha_n); processor=U*tau_process;
blanket=J*tau_blanket; extraction=J*tau_extract; buffer=F*tau_buffer;
reserve=F*q*tau_reserve [T atoms]. I_work=sum(first six); I_total=I_work+reserve.
Processor loss occurs once at its outlet; extraction efficiency acts once at final breeder outlet.
Feed, plasma, buffer and reserve start prefilled; processor, breeder zone and extraction start empty.
Recycle delay=tau_process; breeder delay=tau_blanket+tau_extract; H=max(delays)+extension.
D(t)=F*t-R*max(t-tau_process,0)-S*max(t-tau_blanket-tau_extract,0).
d=max(D at 0, each return delay and H); prefill=feed+plasma+buffer;
M0=prefill+reserve+d. The other stage fills are inside d, not purchased again.
k=lambda*H must be <1. A=k*(M0+J*H)/(1-k); conservative startup=M0+A.
This protects decay including extra startup stock itself, under an abstract usable supply boundary.
It is not an exact transient minimum or qualified ignition/ramp design; source compartment residence
estimates are transferred to deterministic delays. Decay-free nominal stage stocks use separate
replacement demand lambda*I_total. max_decay_residence=max(lambda*each of the five residence inputs),
excluding the reserve interruption duration, reports approximation scale without imposing a qualification threshold.
All atom stocks multiply m_T for kg. T rates export kg/s and 86400 times that for kg/day.
D+T injection/exhaust use equal isotope atom rates times (m_D+m_T), excluding ash and carrier mass.
Annual running amounts multiply availability*s_per_year. Annual decay uses all s_per_year.
Signed operating makeup=(B+L-S+lambda*I_total)*m_T; external shortfall=max(signed,0).
Annual signed makeup=((B+L-S)*availability+lambda*I_total)*m_T*s_per_year.
Passive shutdown loss=-expm1(-lambda*t_shutdown)*I_total*m_T; remaining=exp(-lambda*t_shutdown)*I_total*m_T to retain small positive late stock.
Maintained nominal inventory persists through shutdown; passive remaining is a separate policy.
Active: finite inputs/intermediates; positive power, energy, masses, year; f,eta in (0,1]; r,q,
availability in [0,1]; alpha_n>-1; nonnegative TBR, density, volume, times and decay; G_stock=0.
Invalid arithmetic/fractions raise ValueError. Undefined breeding flag 0 preserves finite diagnostic
carriers (J=0 when breeding_defined=0) and non-breeding stocks/flows, but production-dependent stocks, total/startup and supply
are physically undefined, never a zero-production prediction. defined_flag propagates that status.
Dormant enabled=false forwards held_inventory into total_atoms and returns other zero carriers
with defined_flag=0; no active stock claim. Generic legacy flow arithmetic remains unchanged.
Unsupported wall retention, permeation, detritiation, impurities and bypass remain omitted limitations.
*Source**: work/active/WI-069_fuel-inventory-and-startup/design.md
*Reference**: knowledge/research/pending/20260919-074901_fuel-inventory-residence-startup.md; evidence/proposed-abi.md
*Basis**: independently reviewed conditional scenario; source-derived residence cases, explicit storage policy.
Input units (flat Real ABI; explicit physical meaning):
in attribute enabled_in : Boolean default := false; 1; activation
in attribute held_inventory_in : Real default := 0.0; T atoms; dormant legacy amount
in attribute p_fus_in : Real; MW
in attribute q_eff_in : Real; MeV/reaction
in attribute mev_to_joules_in : Real; J/MeV
in attribute burn_fraction_in : Real; 1; (0,1]
in attribute t_recycle_in : Real; 1; [0,1]
in attribute tbr_available_in : Real; T atoms/reaction
in attribute breeding_defined_in : Real default := 1.0; 1; exact 0/1
in attribute eta_extract_in : Real; 1; (0,1]
in attribute lambda_T_in : Real; 1/s
in attribute G_stock_in : Real; T atoms/s; active zero
in attribute m_T_kg_in : Real; kg/T atom
in attribute m_D_kg_in : Real default := 0.0; kg/D atom
in attribute plasma_volume_in : Real default := 0.0; m^3
in attribute n_T0_in : Real default := 0.0; T atoms/m^3
in attribute alpha_n_in : Real default := 0.0; 1; > -1
in attribute tau_feed_in : Real default := 0.0; s
in attribute tau_process_in : Real default := 0.0; s
in attribute tau_blanket_in : Real default := 0.0; s
in attribute tau_extract_in : Real default := 0.0; s
in attribute tau_buffer_in : Real default := 0.0; s
in attribute tau_reserve_in : Real default := 0.0; s
in attribute startup_extension_in : Real default := 0.0; s
in attribute shutdown_duration_in : Real default := 0.0; s
in attribute reserve_fraction_in : Real default := 0.0; 1; [0,1]
in attribute availability_in : Real; 1; calendar productive fraction
in attribute s_per_year_in : Real default := 31536000.0; s/year; existing model 8760-hour year
*Last Updated**: 2026-09-19

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_fuel_cycle.fuel_inventory_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts recycle_kg_day, production_kg_s, shutdown_remaining_kg, annual_recycle_loss_kg, extraction_loss_kg_s, working_kg, startup_deficit_atoms, injection_kg_s, annual_makeup_signed_kg, max_decay_residence, burn_kg_s, extracted_kg_day, plasma_atoms, buffer_atoms, blanket_kg, extraction_atoms, dt_injection_kg_s, annual_recycle_kg, dt_injection_kg_day, buffer_kg, exhaust_kg_day, external_shortfall_kg_s, blanket_atoms, injection_kg_day, annual_production_kg, extraction_loss_kg_day, startup_conservative_atoms, feed_atoms, recycle_delay_s, annual_extraction_loss_kg, annual_extracted_kg, startup_decay_allowance_kg, startup_conservative_kg, burn_kg_day, total_kg, startup_deficit_kg, dt_processor_kg_day, dt_processor_kg_s, prefill_kg, decay_kg_s, working_atoms, breeding_delay_s, feed_kg, prefill_atoms, reserve_atoms, annual_external_shortfall_kg, annual_injection_kg, exhaust_kg_s, reserve_kg, startup_horizon_s, processor_atoms, plasma_kg, startup_decay_allowance_atoms, production_kg_day, total_atoms, annual_burn_kg, processor_kg, extracted_kg_s, extraction_kg, annual_decay_kg, startup_minimum_atoms, recycle_loss_kg_s, startup_minimum_kg, makeup_signed_kg_s, defined_flag, shutdown_decay_loss_kg, recycle_kg_s, recycle_loss_kg_day, calendar_processor_kg_s, annual_exhaust_kg fields to separate channels.
    """

    name: str = "Fuel_InventoryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, enabled_in: bool, startup_extension_in: float, p_fus_in: float, tbr_available_in: float, burn_fraction_in: float, breeding_defined_in: float, q_eff_in: float, alpha_n_in: float, m_D_kg_in: float, tau_buffer_in: float, tau_blanket_in: float, eta_extract_in: float, plasma_volume_in: float, n_T0_in: float, shutdown_duration_in: float, s_per_year_in: float, tau_process_in: float, held_inventory_in: float, tau_extract_in: float, m_T_kg_in: float, G_stock_in: float, reserve_fraction_in: float, lambda_T_in: float, availability_in: float, t_recycle_in: float, tau_reserve_in: float, mev_to_joules_in: float, tau_feed_in: float    ) -> Fuel_InventoryInput:
        """Validate inputs and fill defaults.

        Args:
            enabled_in: enabled_in input
            startup_extension_in: startup_extension_in input
            p_fus_in: p_fus_in input
            tbr_available_in: tbr_available_in input
            burn_fraction_in: burn_fraction_in input
            breeding_defined_in: breeding_defined_in input
            q_eff_in: q_eff_in input
            alpha_n_in: alpha_n_in input
            m_D_kg_in: m_D_kg_in input
            tau_buffer_in: tau_buffer_in input
            tau_blanket_in: tau_blanket_in input
            eta_extract_in: eta_extract_in input
            plasma_volume_in: plasma_volume_in input
            n_T0_in: n_T0_in input
            shutdown_duration_in: shutdown_duration_in input
            s_per_year_in: s_per_year_in input
            tau_process_in: tau_process_in input
            held_inventory_in: held_inventory_in input
            tau_extract_in: tau_extract_in input
            m_T_kg_in: m_T_kg_in input
            G_stock_in: G_stock_in input
            reserve_fraction_in: reserve_fraction_in input
            lambda_T_in: lambda_T_in input
            availability_in: availability_in input
            t_recycle_in: t_recycle_in input
            tau_reserve_in: tau_reserve_in input
            mev_to_joules_in: mev_to_joules_in input
            tau_feed_in: tau_feed_in input

        Returns:
            Validated input model
        """
        return Fuel_InventoryInput(enabled_in=enabled_in, startup_extension_in=startup_extension_in, p_fus_in=p_fus_in, tbr_available_in=tbr_available_in, burn_fraction_in=burn_fraction_in, breeding_defined_in=breeding_defined_in, q_eff_in=q_eff_in, alpha_n_in=alpha_n_in, m_D_kg_in=m_D_kg_in, tau_buffer_in=tau_buffer_in, tau_blanket_in=tau_blanket_in, eta_extract_in=eta_extract_in, plasma_volume_in=plasma_volume_in, n_T0_in=n_T0_in, shutdown_duration_in=shutdown_duration_in, s_per_year_in=s_per_year_in, tau_process_in=tau_process_in, held_inventory_in=held_inventory_in, tau_extract_in=tau_extract_in, m_T_kg_in=m_T_kg_in, G_stock_in=G_stock_in, reserve_fraction_in=reserve_fraction_in, lambda_T_in=lambda_T_in, availability_in=availability_in, t_recycle_in=t_recycle_in, tau_reserve_in=tau_reserve_in, mev_to_joules_in=mev_to_joules_in, tau_feed_in=tau_feed_in)

    def run(
        self, enabled_in: bool, startup_extension_in: float, p_fus_in: float, tbr_available_in: float, burn_fraction_in: float, breeding_defined_in: float, q_eff_in: float, alpha_n_in: float, m_D_kg_in: float, tau_buffer_in: float, tau_blanket_in: float, eta_extract_in: float, plasma_volume_in: float, n_T0_in: float, shutdown_duration_in: float, s_per_year_in: float, tau_process_in: float, held_inventory_in: float, tau_extract_in: float, m_T_kg_in: float, G_stock_in: float, reserve_fraction_in: float, lambda_T_in: float, availability_in: float, t_recycle_in: float, tau_reserve_in: float, mev_to_joules_in: float, tau_feed_in: float    ) -> ModuleResult[Fuel_InventoryOutput]:
        """Execute calculation.

        Args:
            enabled_in: enabled_in input
            startup_extension_in: startup_extension_in input
            p_fus_in: p_fus_in input
            tbr_available_in: tbr_available_in input
            burn_fraction_in: burn_fraction_in input
            breeding_defined_in: breeding_defined_in input
            q_eff_in: q_eff_in input
            alpha_n_in: alpha_n_in input
            m_D_kg_in: m_D_kg_in input
            tau_buffer_in: tau_buffer_in input
            tau_blanket_in: tau_blanket_in input
            eta_extract_in: eta_extract_in input
            plasma_volume_in: plasma_volume_in input
            n_T0_in: n_T0_in input
            shutdown_duration_in: shutdown_duration_in input
            s_per_year_in: s_per_year_in input
            tau_process_in: tau_process_in input
            held_inventory_in: held_inventory_in input
            tau_extract_in: tau_extract_in input
            m_T_kg_in: m_T_kg_in input
            G_stock_in: G_stock_in input
            reserve_fraction_in: reserve_fraction_in input
            lambda_T_in: lambda_T_in input
            availability_in: availability_in input
            t_recycle_in: t_recycle_in input
            tau_reserve_in: tau_reserve_in input
            mev_to_joules_in: mev_to_joules_in input
            tau_feed_in: tau_feed_in input

        Returns:
            Module result with Fuel_InventoryOutput (recycle_kg_day, production_kg_s, shutdown_remaining_kg, annual_recycle_loss_kg, extraction_loss_kg_s, working_kg, startup_deficit_atoms, injection_kg_s, annual_makeup_signed_kg, max_decay_residence, burn_kg_s, extracted_kg_day, plasma_atoms, buffer_atoms, blanket_kg, extraction_atoms, dt_injection_kg_s, annual_recycle_kg, dt_injection_kg_day, buffer_kg, exhaust_kg_day, external_shortfall_kg_s, blanket_atoms, injection_kg_day, annual_production_kg, extraction_loss_kg_day, startup_conservative_atoms, feed_atoms, recycle_delay_s, annual_extraction_loss_kg, annual_extracted_kg, startup_decay_allowance_kg, startup_conservative_kg, burn_kg_day, total_kg, startup_deficit_kg, dt_processor_kg_day, dt_processor_kg_s, prefill_kg, decay_kg_s, working_atoms, breeding_delay_s, feed_kg, prefill_atoms, reserve_atoms, annual_external_shortfall_kg, annual_injection_kg, exhaust_kg_s, reserve_kg, startup_horizon_s, processor_atoms, plasma_kg, startup_decay_allowance_atoms, production_kg_day, total_atoms, annual_burn_kg, processor_kg, extracted_kg_s, extraction_kg, annual_decay_kg, startup_minimum_atoms, recycle_loss_kg_s, startup_minimum_kg, makeup_signed_kg_s, defined_flag, shutdown_decay_loss_kg, recycle_kg_s, recycle_loss_kg_day, calendar_processor_kg_s, annual_exhaust_kg)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(enabled_in, startup_extension_in, p_fus_in, tbr_available_in, burn_fraction_in, breeding_defined_in, q_eff_in, alpha_n_in, m_D_kg_in, tau_buffer_in, tau_blanket_in, eta_extract_in, plasma_volume_in, n_T0_in, shutdown_duration_in, s_per_year_in, tau_process_in, held_inventory_in, tau_extract_in, m_T_kg_in, G_stock_in, reserve_fraction_in, lambda_T_in, availability_in, t_recycle_in, tau_reserve_in, mev_to_joules_in, tau_feed_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_fuel_cycle.fuel_inventory_impl import (
            run_fuel_inventory,
        )

        # Execute implementation - returns tuple of values
        recycle_kg_day, production_kg_s, shutdown_remaining_kg, annual_recycle_loss_kg, extraction_loss_kg_s, working_kg, startup_deficit_atoms, injection_kg_s, annual_makeup_signed_kg, max_decay_residence, burn_kg_s, extracted_kg_day, plasma_atoms, buffer_atoms, blanket_kg, extraction_atoms, dt_injection_kg_s, annual_recycle_kg, dt_injection_kg_day, buffer_kg, exhaust_kg_day, external_shortfall_kg_s, blanket_atoms, injection_kg_day, annual_production_kg, extraction_loss_kg_day, startup_conservative_atoms, feed_atoms, recycle_delay_s, annual_extraction_loss_kg, annual_extracted_kg, startup_decay_allowance_kg, startup_conservative_kg, burn_kg_day, total_kg, startup_deficit_kg, dt_processor_kg_day, dt_processor_kg_s, prefill_kg, decay_kg_s, working_atoms, breeding_delay_s, feed_kg, prefill_atoms, reserve_atoms, annual_external_shortfall_kg, annual_injection_kg, exhaust_kg_s, reserve_kg, startup_horizon_s, processor_atoms, plasma_kg, startup_decay_allowance_atoms, production_kg_day, total_atoms, annual_burn_kg, processor_kg, extracted_kg_s, extraction_kg, annual_decay_kg, startup_minimum_atoms, recycle_loss_kg_s, startup_minimum_kg, makeup_signed_kg_s, defined_flag, shutdown_decay_loss_kg, recycle_kg_s, recycle_loss_kg_day, calendar_processor_kg_s, annual_exhaust_kg = run_fuel_inventory(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Fuel_InventoryOutput(
                recycle_kg_day=recycle_kg_day,
                production_kg_s=production_kg_s,
                shutdown_remaining_kg=shutdown_remaining_kg,
                annual_recycle_loss_kg=annual_recycle_loss_kg,
                extraction_loss_kg_s=extraction_loss_kg_s,
                working_kg=working_kg,
                startup_deficit_atoms=startup_deficit_atoms,
                injection_kg_s=injection_kg_s,
                annual_makeup_signed_kg=annual_makeup_signed_kg,
                max_decay_residence=max_decay_residence,
                burn_kg_s=burn_kg_s,
                extracted_kg_day=extracted_kg_day,
                plasma_atoms=plasma_atoms,
                buffer_atoms=buffer_atoms,
                blanket_kg=blanket_kg,
                extraction_atoms=extraction_atoms,
                dt_injection_kg_s=dt_injection_kg_s,
                annual_recycle_kg=annual_recycle_kg,
                dt_injection_kg_day=dt_injection_kg_day,
                buffer_kg=buffer_kg,
                exhaust_kg_day=exhaust_kg_day,
                external_shortfall_kg_s=external_shortfall_kg_s,
                blanket_atoms=blanket_atoms,
                injection_kg_day=injection_kg_day,
                annual_production_kg=annual_production_kg,
                extraction_loss_kg_day=extraction_loss_kg_day,
                startup_conservative_atoms=startup_conservative_atoms,
                feed_atoms=feed_atoms,
                recycle_delay_s=recycle_delay_s,
                annual_extraction_loss_kg=annual_extraction_loss_kg,
                annual_extracted_kg=annual_extracted_kg,
                startup_decay_allowance_kg=startup_decay_allowance_kg,
                startup_conservative_kg=startup_conservative_kg,
                burn_kg_day=burn_kg_day,
                total_kg=total_kg,
                startup_deficit_kg=startup_deficit_kg,
                dt_processor_kg_day=dt_processor_kg_day,
                dt_processor_kg_s=dt_processor_kg_s,
                prefill_kg=prefill_kg,
                decay_kg_s=decay_kg_s,
                working_atoms=working_atoms,
                breeding_delay_s=breeding_delay_s,
                feed_kg=feed_kg,
                prefill_atoms=prefill_atoms,
                reserve_atoms=reserve_atoms,
                annual_external_shortfall_kg=annual_external_shortfall_kg,
                annual_injection_kg=annual_injection_kg,
                exhaust_kg_s=exhaust_kg_s,
                reserve_kg=reserve_kg,
                startup_horizon_s=startup_horizon_s,
                processor_atoms=processor_atoms,
                plasma_kg=plasma_kg,
                startup_decay_allowance_atoms=startup_decay_allowance_atoms,
                production_kg_day=production_kg_day,
                total_atoms=total_atoms,
                annual_burn_kg=annual_burn_kg,
                processor_kg=processor_kg,
                extracted_kg_s=extracted_kg_s,
                extraction_kg=extraction_kg,
                annual_decay_kg=annual_decay_kg,
                startup_minimum_atoms=startup_minimum_atoms,
                recycle_loss_kg_s=recycle_loss_kg_s,
                startup_minimum_kg=startup_minimum_kg,
                makeup_signed_kg_s=makeup_signed_kg_s,
                defined_flag=defined_flag,
                shutdown_decay_loss_kg=shutdown_decay_loss_kg,
                recycle_kg_s=recycle_kg_s,
                recycle_loss_kg_day=recycle_loss_kg_day,
                calendar_processor_kg_s=calendar_processor_kg_s,
                annual_exhaust_kg=annual_exhaust_kg,
            )
        )
