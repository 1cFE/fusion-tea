from pydantic import Field
from simkit.config.schema import MultiOutput

class Fuel_InventoryOutput(MultiOutput):
    """Multi-output container for Fuel_Inventory.

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

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:93
    """
    recycle_kg_day: float = Field(description="recycle_kg_day output [kg]")
    production_kg_s: float = Field(description="production_kg_s output [kg]")
    shutdown_remaining_kg: float = Field(description="shutdown_remaining_kg output [kg]")
    annual_recycle_loss_kg: float = Field(description="annual_recycle_loss_kg output [kg]")
    extraction_loss_kg_s: float = Field(description="extraction_loss_kg_s output [kg]")
    working_kg: float = Field(description="working_kg output [kg]")
    startup_deficit_atoms: float = Field(description="startup_deficit_atoms output [T]")
    injection_kg_s: float = Field(description="injection_kg_s output [kg]")
    annual_makeup_signed_kg: float = Field(description="annual_makeup_signed_kg output [kg]")
    max_decay_residence: float = Field(description="max_decay_residence output")
    burn_kg_s: float = Field(description="burn_kg_s output [kg]")
    extracted_kg_day: float = Field(description="extracted_kg_day output [kg]")
    plasma_atoms: float = Field(description="plasma_atoms output [T]")
    buffer_atoms: float = Field(description="buffer_atoms output [T]")
    blanket_kg: float = Field(description="blanket_kg output [kg]")
    extraction_atoms: float = Field(description="extraction_atoms output [T]")
    dt_injection_kg_s: float = Field(description="dt_injection_kg_s output [kg]")
    annual_recycle_kg: float = Field(description="annual_recycle_kg output [kg]")
    dt_injection_kg_day: float = Field(description="dt_injection_kg_day output [kg]")
    buffer_kg: float = Field(description="buffer_kg output [kg]")
    exhaust_kg_day: float = Field(description="exhaust_kg_day output [kg]")
    external_shortfall_kg_s: float = Field(description="external_shortfall_kg_s output [kg]")
    blanket_atoms: float = Field(description="blanket_atoms output [T]")
    injection_kg_day: float = Field(description="injection_kg_day output [kg]")
    annual_production_kg: float = Field(description="annual_production_kg output [kg]")
    extraction_loss_kg_day: float = Field(description="extraction_loss_kg_day output [kg]")
    startup_conservative_atoms: float = Field(description="startup_conservative_atoms output [T]")
    feed_atoms: float = Field(description="feed_atoms output [T]")
    recycle_delay_s: float = Field(description="recycle_delay_s output [s]")
    annual_extraction_loss_kg: float = Field(description="annual_extraction_loss_kg output [kg]")
    annual_extracted_kg: float = Field(description="annual_extracted_kg output [kg]")
    startup_decay_allowance_kg: float = Field(description="startup_decay_allowance_kg output [kg]")
    startup_conservative_kg: float = Field(description="startup_conservative_kg output [kg]")
    burn_kg_day: float = Field(description="burn_kg_day output [kg]")
    total_kg: float = Field(description="total_kg output [kg]")
    startup_deficit_kg: float = Field(description="startup_deficit_kg output [kg]")
    dt_processor_kg_day: float = Field(description="dt_processor_kg_day output [kg]")
    dt_processor_kg_s: float = Field(description="dt_processor_kg_s output [kg]")
    prefill_kg: float = Field(description="prefill_kg output [kg]")
    decay_kg_s: float = Field(description="decay_kg_s output [kg]")
    working_atoms: float = Field(description="working_atoms output [T]")
    breeding_delay_s: float = Field(description="breeding_delay_s output [s]")
    feed_kg: float = Field(description="feed_kg output [kg]")
    prefill_atoms: float = Field(description="prefill_atoms output [T]")
    reserve_atoms: float = Field(description="reserve_atoms output [T]")
    annual_external_shortfall_kg: float = Field(description="annual_external_shortfall_kg output [kg]")
    annual_injection_kg: float = Field(description="annual_injection_kg output [kg]")
    exhaust_kg_s: float = Field(description="exhaust_kg_s output [kg]")
    reserve_kg: float = Field(description="reserve_kg output [kg]")
    startup_horizon_s: float = Field(description="startup_horizon_s output [s]")
    processor_atoms: float = Field(description="processor_atoms output [T]")
    plasma_kg: float = Field(description="plasma_kg output [kg]")
    startup_decay_allowance_atoms: float = Field(description="startup_decay_allowance_atoms output [T]")
    production_kg_day: float = Field(description="production_kg_day output [kg]")
    total_atoms: float = Field(description="total_atoms output [T]")
    annual_burn_kg: float = Field(description="annual_burn_kg output [kg]")
    processor_kg: float = Field(description="processor_kg output [kg]")
    extracted_kg_s: float = Field(description="extracted_kg_s output [kg]")
    extraction_kg: float = Field(description="extraction_kg output [kg]")
    annual_decay_kg: float = Field(description="annual_decay_kg output [kg]")
    startup_minimum_atoms: float = Field(description="startup_minimum_atoms output [T]")
    recycle_loss_kg_s: float = Field(description="recycle_loss_kg_s output [kg]")
    startup_minimum_kg: float = Field(description="startup_minimum_kg output [kg]")
    makeup_signed_kg_s: float = Field(description="makeup_signed_kg_s output [kg]")
    defined_flag: float = Field(description="defined_flag output")
    shutdown_decay_loss_kg: float = Field(description="shutdown_decay_loss_kg output [kg]")
    recycle_kg_s: float = Field(description="recycle_kg_s output [kg]")
    recycle_loss_kg_day: float = Field(description="recycle_loss_kg_day output [kg]")
    calendar_processor_kg_s: float = Field(description="calendar_processor_kg_s output [kg]")
    annual_exhaust_kg: float = Field(description="annual_exhaust_kg output [kg]")
