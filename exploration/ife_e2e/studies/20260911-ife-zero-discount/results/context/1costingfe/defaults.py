"""Load and manage default parameters from YAML files."""

from dataclasses import dataclass, fields, replace
from pathlib import Path

import yaml

from costingfe.types import PowerCycle

_DATA_DIR = Path(__file__).parent / "data" / "defaults"


@dataclass(frozen=True)
class CostingConstants:
    """All costing coefficients. Immutable — use .replace() for overrides."""

    # Shared reference: plant-total net electric power (1 GWe) at which the
    # net-electric-scaling coefficients are calibrated. Used wherever an account
    # normalizes net electric to "per GWe" (CAS10 land, CAS22 plant-wide,
    # CAS40, CAS50 startup/decom, CAS70 O&M).
    ref_net_power_mwe: float = 1000.0
    # Shared reference: gross electric power of the reference plant (net plus
    # recirculating, ~1100 MWe for a 1 GWe-net plant). Used by the gross-electric
    # (p_et) scaling accounts: CAS21 buildings, CAS22 structure/vessel/power-
    # supplies/remote-handling.
    ref_gross_power_mwe: float = 1100.0

    # CAS10
    site_permits: float = 3.0
    plant_studies_foak: float = 20.0
    plant_studies_noak: float = 4.0
    plant_permits: float = 2.0
    plant_reports: float = 1.0
    other_precon: float = 1.0
    land_intensity: float = 0.25  # acres/MWe at ref_net_power (CFS 100ac/400MWe)
    land_cost: float = 10000.0  # $/acre (industrial-zoned US average)
    licensing_cost_dt: float = 5.0
    licensing_cost_dd: float = 3.0
    licensing_cost_dhe3: float = 1.0
    licensing_cost_pb11: float = 0.1
    # Licensing times per DI-015/016 regulatory framework research
    licensing_time_dt: float = 2.0  # Part 30, 1-2yr range
    licensing_time_dd: float = 1.5  # Reduced tritium, 6-18mo range
    licensing_time_dhe3: float = 0.75  # Minimal radioactivity, 6-12mo
    licensing_time_pb11: float = 0.0  # No NRC jurisdiction

    # CAS22 — Reactor Plant Equipment
    # 220101: First Wall + Blanket — volume-based unit costs (M$/m³)
    # DT 0.60 = NOAK-reduced RAFM-steel blanket mass build-up: ~3500 t
    # (steel + PbLi breeder + Be multiplier + W armor) x $150/kg fabricated
    # = $525M FOAK over ~650 m³ -> 0.60 after NOAK learning-curve reduction
    # ($389M); ITER 440-module / 2000 t cross-check. DD/DHe3/pB11 scale down
    # by blanket complexity (no breeder / minimal / X-ray liner only).
    # See docs/account_justification/CAS22_reactor_components.md
    blanket_unit_cost_dt: float = 0.60  # Full breeding blanket (TBR>1.05)
    blanket_unit_cost_dd: float = 0.30  # Energy capture, no breeding
    blanket_unit_cost_dhe3: float = 0.08  # Minimal X-ray + ~5% neutron
    blanket_unit_cost_pb11: float = 0.05  # Minimal X-ray only
    # Li2O solid ceramic breeder (DT) — chemistry-specific override applied
    # in C220101 when blanket_fill == LI2O. Derived from ~2 t/m^3 packed
    # density x ~$100k/t fusion-grade Li2O pricing; no flow loop, no MHD
    # ducts, no online tritium extraction (cheaper per m^3 than PbLi).
    blanket_unit_cost_li2o: float = 0.2

    # 220102: Shield — volume-based unit cost (M$/m³)
    # Reference: ~350 m³ steel + borated water -> $261M DT
    # (docs/account_justification/CAS22_reactor_components.md)
    shield_unit_cost: float = 0.74  # M$/m³, DT reference

    # 220103-220108: Reactor components
    # 220103: Resistive (copper) coil mass build-up. Low-field resistive coils
    # cost their bulk conductor mass + structure + fabrication, not the
    # superconductor ampere-meter price. Superconducting coils keep the
    # $/kAm path. See docs/account_justification/CAS22_reactor_components.md
    coil_cu_current_density_a_mm2: float = 5.0  # water-cooled copper current density
    coil_cu_price_per_kg: float = 11.0  # copper conductor, $/kg (LME 2026 class)
    coil_cu_fab_markup: float = 3.5  # winding, insulation, cooling, jointing, test
    coil_struct_fraction: float = 0.6  # steel support mass / copper mass
    coil_steel_price_per_kg: float = 6.0  # fabricated structural steel, $/kg
    coil_steel_fab_markup: float = 3.0  # coil-case / inter-coil support fabrication
    # Superconducting-coil conductor (tape) cost per kA-m, by coil material
    # [$/kA-m]. Promoted to CostingConstants so they are visible and enter the
    # autodiff sensitivity; the active material's value flows into C220103.
    conductor_cost_rebco: float = 50.0  # REBCO HTS tape (aggressive NOAK target)
    conductor_cost_nb3sn: float = 7.0  # Nb3Sn (ITER conductor, mature)
    conductor_cost_nbti: float = 7.0  # NbTi (LHC heritage)
    conductor_cost_copper: float = (
        1.0  # copper $/kA-m (resistive coils use the mass build-up above)
    )
    # 220104: Supplementary Heating — per-MW linear costs (M$/MW, 2025 USD)
    # Vendor-purchased turnkey systems. Source: ARIES heating-system costs
    # (2023$ base, CPI-escalated to 2025 USD); NBI 7.46 calibrated to ITER NBI
    # procurement (EUR 9-15M/MW FOAK -> NOAK discount), ECRH 5.28 to ITER
    # gyrotron procurement (EUR 5-10M/MW).
    # See docs/account_justification/CAS22_reactor_components.md
    heating_nbi_per_mw: float = 7.4639  # Neutral Beam Injection
    heating_icrf_per_mw: float = 4.3842  # Ion Cyclotron Resonance Frequency
    heating_ecrh_per_mw: float = (
        5.2829  # Electron Cyclotron Resonance Heating (gyrotrons)
    )
    heating_lhcd_per_mw: float = 4.2263  # Lower Hybrid Current Drive (klystrons)
    # Heating wall-plug source efficiency by method (wall-plug -> delivered
    # power, before plasma coupling). Combined with a per-concept eta_couple
    # (in the concept YAML) to form eta_pin = eta_source x eta_couple.
    eta_source_nbi: float = 0.60  # negative-ion NBI source (OSTI 2441289 / ITER)
    eta_source_icrf: float = 0.70  # RF tetrode transmitter (ITER ICRF ~70%)
    eta_source_ecrh: float = 0.50  # gyrotron wall-plug
    eta_source_lhcd: float = 0.50  # klystron wall-plug
    # 220104: Pulsed driver capital, concept-dispatched in cas22.py C220104.
    # Lasers, accelerators, and electromagnetic guns are costed per joule of pulse
    # energy: their capital is set by pulse energy (laser aperture / diode count,
    # ring charge, coaxial-gun size and peak current), not by how often the driver
    # fires, so the basis is rep-rate-independent. Pneumatic/mechanical injectors
    # (mag-target) keep an average-power (throughput) basis because they accelerate
    # mass each shot and their handling/recirculation plant scales with throughput
    # (M$/MW, 2023$). Like every pulsed concept, the laser keeps the C220104
    # (driver hardware) / C220107 (electrical store) split: this value is the
    # optics + diode-array $/J (the dominant part); the capacitor bank that fires
    # the diodes is the small C220107 term, so C220104 + C220107 lands at the
    # published turnkey NOAK. See CAS22_reactor_components.md (C220104).
    driver_laser_per_mj: float = 205.0  # M$/MJ; optics + diodes. With the ~$5/J
    #   C220107 cap bank the laser totals ~$210/J = aggressive DPSSL NOAK (diode
    #   roadmap to ~$0.007/W). Published DPSSL NOAK $210-700/J, FOAK $700-1000/J.
    # KrF excimer (NRL Electra / Xcimer) and flashlamp Nd:Glass (NIF-class)
    # driver capital, $/MJ of pulse energy, selected by laser_driver_type for
    # LASER_IFE. KrF 40 leans to the Xcimer/ASPEN large-aperture-optics claim
    # (range 20-200; NRL/Sethian engineering baseline ~200). Nd:Glass 1000 from
    # NIF $3.5-4.2B / 1.1-1.9 MJ UV (~$2000/J facility, driver-only ~half).
    # See docs/account_justification/CAS22_reactor_components.md (C220104).
    driver_krf_per_mj: float = 40.0  # M$/MJ KrF excimer driver hardware
    driver_ndglass_per_mj: float = 1000.0  # M$/MJ flashlamp Nd:Glass driver
    driver_heavy_ion_per_mj: float = 60.0  # M$/MJ beam energy (heavy-ion accelerator)
    driver_plasma_jet_per_mj: float = 4.0  # M$/MJ EM plasma-gun pulse energy
    driver_staged_zpinch_per_mj: float = 1.5  # M$/MJ sheared-flow gun + gas inj.
    driver_mag_target_per_mw: float = 3.0  # M$/MW avg power, pneumatic pistons
    # MAGLIF's main driver is the electrical Z-pinch, costed in C220107 on a $/J
    # basis. Its C220104 carries only laser preheat, costed per joule of preheat
    # pulse energy (same DPSSL class as the IFE driver). Concepts that magnetize and
    # compress without a preheat laser (e.g. Pacific Fusion) set e_preheat_mj=0 and
    # incur no preheat cost.
    laser_preheat_per_mj: float = (
        205.0  # M$/MJ preheat laser (same DPSSL class as driver)
    )
    # 220105: Primary Structure — volume-based (M$/m³)
    # Reference: ~200 m³ structural steel -> $28M (CAS22_reactor_components.md)
    structure_unit_cost: float = 0.15
    # 220106: Vacuum System — vessel (volume-based) + gas-load pumping.
    # See docs/account_justification/CAS220106_vacuum_pumping.md
    vessel_unit_cost: float = 0.72  # M$/m³ vessel shell, ref ~210 m³ -> $151M
    # Gas-load-driven pumping: S_req = Q_gas / P_op, cost = pump_unit_cost * S_req.
    # Q_gas = NBI neutral-gas load + fueling/exhaust throughput (outgassing negligible).
    pump_unit_cost: float = 0.015  # M$ per (m³/s) installed speed (= $15/(L/s))
    pump_nbi_gas_amplification: float = 1.0  # gas particles pumped per beam particle
    #   (un-trapped beam + neutralizer reflux); calibrated to C-2W ~2000 m³/s.
    pump_gas_temp_k: float = 300.0  # pumped-gas temperature [K] for Q = N*kT
    pump_ion_per_reaction: float = 2.0  # fuel ions consumed per fusion reaction
    nbi_beam_energy_kev: float = 120.0  # reference reactor NBI energy [keV]; gas
    #   load scales as 1/E_b (higher-energy beams inject fewer particles per MW).
    # Operating (plenum) pressure at the pump throat [Pa]. THE sensitive knob:
    # low-pressure concepts (FRC, mirror, open field lines) need far more speed for
    # the same throughput than a tokamak divertor running at a few Pa. Global
    # default here; overridden per concept in the concept YAMLs.
    vac_op_pressure_pa: float = 1.0
    # Fusion energy released per reaction [MeV], for the fueling-throughput term.
    e_fus_mev_dt: float = 17.6
    e_fus_mev_dd: float = 3.65  # branch-averaged
    e_fus_mev_dhe3: float = 18.3
    e_fus_mev_pb11: float = 8.7
    power_supplies_base: float = 80.0
    divertor_base: float = 60.0
    # IFE/MIF target-factory capital is a per-concept input (target_factory_capex,
    # CAS22.01.08), not a global constant — a precision+tritium capsule factory
    # and a metal-liner casting shop differ by ~5x. See CAS80_target_consumables.md.

    # C220109: DEC add-on for linear devices
    # Source: docs/account_justification/CAS220109_direct_energy_converter.md
    # Subsystem build-up: grids + power conditioning + incremental vacuum/tank
    dec_base: float = 125.0  # M$ at 400 MWe DEC electric output (P_DEE_REF)
    dec_grid_cost: float = 12.0  # M$ replaceable grid/collector modules at P_DEE_REF

    # DEC grid lifetime (FPY) — HIGH UNCERTAINTY, no reactor-scale data.
    # Conservative estimates. Primary degradation: sputtering + He blistering
    # from charged particle exhaust. Neutron damage additive for DT/DD.
    # Sensitivity range: 0.5x to 3x these values.
    dec_grid_lifetime_dt: float = 2.0  # Sputtering + 14.1 MeV neutron damage
    dec_grid_lifetime_dd: float = 3.0  # Sputtering + 2.45 MeV neutron damage
    dec_grid_lifetime_dhe3: float = 4.0  # 14.7 MeV proton sputtering + He blistering
    dec_grid_lifetime_pb11: float = (
        3.0  # 2.9 MeV alpha sputtering + severe He blistering
    )

    # Pulsed inductive DEC — driver cost basis
    # $/J_stored, NOAK all-in (caps + switches + charging + buswork)
    # Sensitivity range: 0.5-4.0
    c_cap_allin_per_joule: float = 0.5

    # Pulsed inductive DEC — C220109 incremental markups
    markup_switch_bidir: float = 0.06  # Bidirectional switch premium (frac of driver)
    markup_controls: float = 0.04  # FPGA/energy management (frac of driver)
    c_inv_per_kw_net: float = 150.0  # Grid-tie inverter ($/kW_net)

    # Pulsed inductive DEC — CAS72 cap replacement
    cap_shot_lifetime: float = 1.0e8  # Shots, NOAK baseline. Range: 1e7-1e9

    # CAS72 formation-electrode replacement (EM-gun concepts: staged_zpinch,
    # plasma_jet). Plasma-facing coaxial-gun electrodes erode under high current
    # density. High uncertainty, no NOAK data.
    electrode_shot_lifetime: float = 1.0e8  # Shots before replacement. Range: 1e7-1e9
    electrode_replace_frac: float = 0.5  # Consumable share of C220104. Range 0.25-0.75
    # CAS72 laser-IFE driver scheduled replacement, per architecture. Each
    # subsystem: replace_frac = share of C220104; shot_lifetime = NOAK
    # projection (shots), NOT demonstrated. Dispatched by laser_driver_type via
    # the shared geometric replacement helper. KrF/Nd:Glass cost shares are
    # engineering estimates. See CAS22_reactor_components.md (CAS72 O&M).
    # DPSSL (LIFE/HiPER): diodes are ~plant-life (≈capital), optics dominate O&M.
    dpssl_diode_replace_frac: float = 0.50  # pump diodes (dominant cost share)
    dpssl_diode_shot_lifetime: float = 1.0e10  # NOAK ≈ plant life; demonstrated ~1e8
    dpssl_crystal_replace_frac: float = 0.03  # KDP/DKDP tripler crystals (small)
    dpssl_crystal_shot_lifetime: float = 3.0e9  # long-lived
    dpssl_optics_replace_frac: float = 0.05  # final optics / GIMM / debris shields
    dpssl_optics_shot_lifetime: float = 3.0e8  # GIMM NOAK target; demonstrated ~1e5
    # KrF excimer (engineering estimates)
    krf_foil_replace_frac: float = 0.04  # hibachi foil + windows
    krf_foil_shot_lifetime: float = (
        3.0e8  # Electra durability target; demonstrated ~1e4-1e5
    )
    krf_ebeam_replace_frac: float = 0.06  # e-beam diode + gas system
    krf_ebeam_shot_lifetime: float = 3.0e8
    # Nd:Glass (NIF-class): flashlamps are Xe-arc-limited; glass slabs are capital
    ndglass_lamp_replace_frac: float = 0.10  # Xe flashlamps
    ndglass_lamp_shot_lifetime: float = 1.0e4  # demonstrated O(1e3-1e4); arc-limited

    # Pulsed radiation fraction defaults (fraction of charged-particle energy)
    f_rad_dt: float = 0.10
    f_rad_dd: float = 0.08
    f_rad_dhe3: float = 0.05
    f_rad_pb11: float = 0.15  # High Z^2 bremsstrahlung

    # Steady-state radiation fraction (fraction of P_fus radiated as bremsstrahlung)
    # Used to override compute_p_rad for fuels where bremsstrahlung dominates.
    # p-B11: 83% with alpha channeling at the optimal hybrid fast/thermal
    # operating point (P_L/P_F = 17%, Ochs et al. 2022, PhysRevE 106 055215).
    # D-He3: 24% for a 50/50 D/He3 mix at T = 70 keV with relativistic + e-e
    # bremsstrahlung (Bosch-Hale cross sections, Rider 1995 brem corrections).
    # Literature spread: Wesson ~20% at 100 keV, Santarius/Kulcinski ~25%, Rider ~30%.
    # See examples/dhe3_mix_optimization.py for the self-consistent calculation.
    f_rad_fus_pb11: float = 0.83
    f_rad_fus_dhe3: float = 0.24

    # PdV work fraction — fraction of charged-particle energy doing work
    # against confining field. For adiabatic expansion:
    # f_pdv = 1 - (1/r)^(gamma-1), gamma=5/3
    # r=10 -> 0.78, r=20 -> 0.86, r=50 -> 0.91
    f_pdv: float = 0.80

    # 220110: Remote Handling & Maintenance Equipment (M$ at 1 GWe, tokamak ref)
    # See docs/account_justification/CAS220110_remote_handling.md
    remote_handling_dt_base: float = 150.0
    remote_handling_dd_base: float = 100.0
    remote_handling_dhe3_base: float = 30.0
    remote_handling_pb11_base: float = 20.0

    # 220111: Installation labor (fraction of reactor subtotal)
    installation_frac: float = 0.14

    # 220111: Multi-unit labor factor — labor cost of each module beyond
    # the first, as a fraction of the first module's labor. Captures the
    # "twin/triplet unit" co-location effect documented in fission EPC:
    # Vogtle 3->4 ~20-30% labor reduction, Korean APR-1400 batches ~10-15%,
    # Chinese AP1000 pairs (Sanmen, Haiyang) modest. Empirical range 5-15%
    # off subsequent units; default 8% (factor 0.92). NOT a Wright's-Law
    # learning curve — that belongs at fleet-cumulative scale, not at
    # n_mod=2-6 on one site. Equipment cost (C220101-C220110) is unchanged;
    # only the on-site labor portion (C220111) is discounted.
    multi_unit_labor_factor: float = 0.92

    # Fixed core component lifetime (FPY — full power years between replacements).
    # Used by the IFE/MIF (non-steady-state) families only; steady-state MFE
    # concepts derive core lifetime from the fluence limits below (Phi_max / q_n).
    # Source: 20260208-fusion-reactor-subsystems-by-fuel-type.md
    core_lifetime_dt: float = 5.0  # 5-10 FPY, ~20 dpa/yr
    core_lifetime_dd: float = 10.0  # 10-15 FPY, ~7 dpa/yr
    core_lifetime_dhe3: float = 30.0  # 30+ FPY, ~1 dpa/yr
    core_lifetime_pb11: float = 50.0  # 50+ FPY, ~0.1 dpa/yr

    # First-wall/blanket neutron fluence limits (MW yr/m^2). Steady-state MFE
    # core lifetime = Phi_max / q_n, clamped to plant life. DT anchored to the
    # ARIES FS 200 dpa limit (18 MW yr/m^2); the ladder (1:2:6:10) follows the
    # 14 MeV >> 2.45 MeV spectrum-hardness argument and the old FPY ladder.
    # Source: docs/account_justification/wall_limits_and_fluence.md
    fluence_limit_dt: float = 18.0  # ARIES FS 200 dpa = 18 MW yr/m^2
    fluence_limit_dd: float = 36.0  # 2x DT (softer 2.45 MeV spectrum)
    fluence_limit_dhe3: float = 108.0  # 6x DT (small D-D side-channel neutrons)
    fluence_limit_pb11: float = 180.0  # 10x DT (aneutronic; surface cap governs)

    # CAS22 sub-accounts that need periodic replacement (neutron/thermal damage)
    # Default: blanket/FW + divertor. Extend to include "C220103" (coils) for
    # designs with insufficient HTS shielding.
    replaceable_accounts: tuple = ("C220101", "C220108")

    # 220500: Fuel Handling (M$ at 1 GWe reference)
    fuel_handling_dt_base: float = 120.0  # Full tritium processing
    fuel_handling_dd_base: float = 60.0  # Small-scale tritium + deuterium
    fuel_handling_dhe3_base: float = 40.0  # He-3 handling
    fuel_handling_pb11_base: float = 15.0  # Boron powder injection

    # CAS21 — per-building, per-fuel costs (M$ at 1 GWe reference)
    # Each entry has fuel keys (dt/dd/dhe3/pb11 or 'all') + 'scales' key
    building_costs: dict[str, dict] = None  # loaded from YAML

    # 220103 — per-concept SC coil manufacturing markup (conductor -> installed
    # magnet system: winding, quench protection, structural casing, cryostat,
    # testing). Keyed by ConfinementConcept.value. Loaded from YAML; this is a
    # cost-calibration constant, not a per-design knob. Copper concepts use the
    # mass build-up markups (coil_cu_fab_markup, coil_steel_fab_markup) instead.
    coil_markup: dict[str, float] = None  # loaded from YAML

    # CAS27 — Special materials: initial blanket-fill inventory.
    # Volume-based mass build-up keyed on blanket_fill (not power-scaled):
    # {fill: {density, vol_frac, price}}. Loaded from YAML.
    # See docs/account_justification/CAS27_special_materials.md
    cas27_fill_materials: dict[str, dict] = None

    # CAS23-26 — BOP equipment (M$/MW gross electric, 2025 USD)
    # Source: ARIES/NETL calibration (2019 base, CPI-escalated to 2025 USD)
    # See docs/account_justification/CAS23_26_balance_of_plant.md
    turbine_per_mw: float = 0.20284  # Steam TG, condenser, feedwater
    electric_per_mw: float = 0.08640  # Switchyard, transformers, cabling
    misc_per_mw: float = 0.05259  # Fire protection, compressed air, HVAC
    heat_rej_per_mw: float = 0.03506  # Cooling towers, circ water

    # CAS28 — Digital twin (M$, fixed). Software-dominated; does not scale
    # with plant size. Source: DOE ARPA-E GEMINA per-project reactor digital-
    # twin budgets (U. Michigan scalable reactor digital twin $5.2M; $2-10M
    # industrial plant twins). See docs/account_justification/CAS28_digital_twin.md
    digital_twin: float = 5.0

    # CAS29 — Contingency on direct costs (Gen-IV EMWG convention)
    contingency_rate_foak: float = 0.10
    contingency_rate_noak: float = 0.0

    # CAS30
    indirect_fraction: float = 0.20
    reference_construction_time: float = 6.0

    # CAS40 — Capitalized owner's costs (M$ at 1 GWe reference, 2025 USD)
    # Source: CAS40_capitalized_owners_costs.md — INL methodology on CAS71-73
    # staffing (2023$ base, CPI-escalated to 2025 USD)
    owner_cost_dt: float = 41.2  # 117 staff, full neutron + tritium pre-op training
    owner_cost_dd: float = 32.8  # 94 staff, reduced tritium scope
    owner_cost_dhe3: float = 24.3  # 69 staff, light HP program
    owner_cost_pb11: float = 21.1  # 59 staff, near-industrial, RSO-only

    # CAS50 — Capitalized supplementary costs
    # Source: CAS50_supplementary_costs.md — sub-account model
    shipping_frac: float = 0.015  # fraction of CAS20 (WNA ~2%, discounted for fusion)
    spare_parts_frac_dt: float = (
        0.03  # fraction of CAS22-28, activated component spares
    )
    spare_parts_frac_dd: float = 0.025
    spare_parts_frac_dhe3: float = 0.015
    spare_parts_frac_pb11: float = 0.01  # conventional industrial spares only
    tax_frac: float = 0.01  # fraction of CAS20, after typical energy project exemptions
    construction_insurance_frac: float = (
        0.015  # fraction of (CAS20+CAS30), builder's risk
    )
    startup_fuel_dt: float = 40.0  # M$ at 1 GWe — ~1.3 kg tritium at $30k/g
    startup_fuel_dd: float = 0.1  # M$ at 1 GWe — deuterium, commodity
    startup_fuel_dhe3: float = 10.0  # M$ at 1 GWe — He3, supply-constrained
    startup_fuel_pb11: float = 0.1  # M$ at 1 GWe — H + B11, industrial commodities
    decom_provision_dt: float = 272.0  # M$ at 1 GWe — PV of $600M over 40yr at 2%
    decom_provision_dd: float = 199.0  # M$ at 1 GWe — PV of $440M
    decom_provision_dhe3: float = 140.0  # M$ at 1 GWe — PV of $310M
    decom_provision_pb11: float = 113.0  # M$ at 1 GWe — PV of $250M

    # CAS70 — Annual O&M cost (M$/yr at 1 GWe reference, 2025 USD)
    # Source: CAS70_staffing_and_om_costs.md — staffing-based build-up by fuel
    # type (2023$ base, CPI-escalated to 2025 USD)
    # Power-law scaling: annual_om = om_cost(fuel) * (P_net / 1 GWe)^0.5
    om_cost_dt: float = 54.9  # Full neutron + tritium operational overhead
    om_cost_dd: float = 41.2  # ~1/3 DT neutron flux, smaller tritium inventory
    om_cost_dhe3: float = 27.5  # ~5% neutron fraction, minimal tritium
    om_cost_pb11: float = 25.4  # Aneutronic, no tritium, RSO-only

    # CAS80 — fuel isotope unit costs ($/kg)
    # STARFIRE (1980) inflation-adjusted via GDP IPD. Range: $1,500-3,500/kg.
    u_deuterium: float = 2175.0  # $/kg
    u_li6: float = 1000.0  # $/kg, enriched Li-6 (90%) for breeding blanket
    u_he3: float = 2_000_000.0  # $/kg, He-3 ($2,000/g — optimistic self-production)
    u_protium: float = 5.0  # $/kg, commodity H2
    u_b11: float = 10_000.0  # $/kg, FOAK enriched B-11 (no industrial supply)
    u_b11_noak: float = (
        75.0  # $/kg, NOAK B-11 (industrial chemical exchange distillation)
    )

    def replace(self, **kwargs):
        return replace(self, **kwargs)

    def owner_cost(self, fuel):
        """Pre-operational owner's cost (M$ at 1 GWe ref) for a given fuel type."""
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.owner_cost_dt,
            Fuel.DD: self.owner_cost_dd,
            Fuel.DHE3: self.owner_cost_dhe3,
            Fuel.PB11: self.owner_cost_pb11,
        }.get(fuel, self.owner_cost_dt)

    def om_cost(self, fuel):
        """Annual O&M cost (M$/yr at 1 GWe reference) for a given fuel type."""
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.om_cost_dt,
            Fuel.DD: self.om_cost_dd,
            Fuel.DHE3: self.om_cost_dhe3,
            Fuel.PB11: self.om_cost_pb11,
        }.get(fuel, self.om_cost_dt)

    def licensing_cost(self, fuel):
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.licensing_cost_dt,
            Fuel.DD: self.licensing_cost_dd,
            Fuel.DHE3: self.licensing_cost_dhe3,
            Fuel.PB11: self.licensing_cost_pb11,
        }.get(fuel, self.licensing_cost_dt)

    def licensing_time(self, fuel):
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.licensing_time_dt,
            Fuel.DD: self.licensing_time_dd,
            Fuel.DHE3: self.licensing_time_dhe3,
            Fuel.PB11: self.licensing_time_pb11,
        }.get(fuel, self.licensing_time_dt)

    def core_lifetime(self, fuel):
        """Fixed core component lifetime in FPY (IFE/MIF families only).

        Steady-state MFE concepts use the fluence-based lifetime instead
        (see fluence_limit and model._core_lifetime_fpy).
        """
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.core_lifetime_dt,
            Fuel.DD: self.core_lifetime_dd,
            Fuel.DHE3: self.core_lifetime_dhe3,
            Fuel.PB11: self.core_lifetime_pb11,
        }.get(fuel, self.core_lifetime_dt)

    def fluence_limit(self, fuel):
        """First-wall/blanket neutron fluence limit Phi_max [MW yr/m^2]."""
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.fluence_limit_dt,
            Fuel.DD: self.fluence_limit_dd,
            Fuel.DHE3: self.fluence_limit_dhe3,
            Fuel.PB11: self.fluence_limit_pb11,
        }.get(fuel, self.fluence_limit_dt)

    def dec_grid_lifetime(self, fuel):
        """DEC grid replacement interval in FPY for a given fuel type."""
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.dec_grid_lifetime_dt,
            Fuel.DD: self.dec_grid_lifetime_dd,
            Fuel.DHE3: self.dec_grid_lifetime_dhe3,
            Fuel.PB11: self.dec_grid_lifetime_pb11,
        }.get(fuel, self.dec_grid_lifetime_dt)

    def f_rad(self, fuel):
        """Default radiation fraction for pulsed concepts."""
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.f_rad_dt,
            Fuel.DD: self.f_rad_dd,
            Fuel.DHE3: self.f_rad_dhe3,
            Fuel.PB11: self.f_rad_pb11,
        }.get(fuel, self.f_rad_dt)

    def f_rad_fus(self, fuel):
        """Radiation fraction of P_fus for steady-state concepts.

        Returns None for fuels where compute_p_rad should be used instead.
        """
        from costingfe.types import Fuel

        return {
            Fuel.PB11: self.f_rad_fus_pb11,
            Fuel.DHE3: self.f_rad_fus_dhe3,
        }.get(fuel)

    def conductor_cost_per_kam(self, coil_material):
        """Conductor (tape) cost [$/kA-m] for a coil material."""
        from costingfe.types import CoilMaterial

        return {
            CoilMaterial.REBCO_HTS: self.conductor_cost_rebco,
            CoilMaterial.NB3SN: self.conductor_cost_nb3sn,
            CoilMaterial.NBTI: self.conductor_cost_nbti,
            CoilMaterial.COPPER: self.conductor_cost_copper,
        }[coil_material]

    def spare_parts_frac(self, fuel):
        """Initial spare parts fraction of CAS22-28 for a given fuel type."""
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.spare_parts_frac_dt,
            Fuel.DD: self.spare_parts_frac_dd,
            Fuel.DHE3: self.spare_parts_frac_dhe3,
            Fuel.PB11: self.spare_parts_frac_pb11,
        }.get(fuel, self.spare_parts_frac_dt)

    def startup_fuel(self, fuel):
        """Startup fuel/inventory cost (M$ at 1 GWe ref) for a given fuel type."""
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.startup_fuel_dt,
            Fuel.DD: self.startup_fuel_dd,
            Fuel.DHE3: self.startup_fuel_dhe3,
            Fuel.PB11: self.startup_fuel_pb11,
        }.get(fuel, self.startup_fuel_dt)

    def decom_provision(self, fuel):
        """Decommissioning provision (M$ at 1 GWe ref) for a given fuel type."""
        from costingfe.types import Fuel

        return {
            Fuel.DT: self.decom_provision_dt,
            Fuel.DD: self.decom_provision_dd,
            Fuel.DHE3: self.decom_provision_dhe3,
            Fuel.PB11: self.decom_provision_pb11,
        }.get(fuel, self.decom_provision_dt)

    def contingency_rate(self, noak):
        return self.contingency_rate_noak if noak else self.contingency_rate_foak


def cc_float_fields() -> list[str]:
    """Return names of all float fields on CostingConstants."""
    return [
        f.name for f in fields(CostingConstants) if f.type == "float" or f.type is float
    ]


def load_costing_constants(path: Path = None) -> CostingConstants:
    """Load costing constants from YAML, falling back to dataclass defaults."""
    if path is None:
        path = _DATA_DIR / "costing_constants.yaml"
    if path.exists():
        with open(path) as f:
            data = yaml.safe_load(f)
        valid_fields = {f.name for f in fields(CostingConstants)}
        return CostingConstants(**{k: v for k, v in data.items() if k in valid_fields})
    return CostingConstants()


def load_engineering_defaults(concept_fuel: str) -> dict:
    """Load engineering defaults for a concept (e.g., 'mfe_tokamak')."""
    path = _DATA_DIR / f"{concept_fuel}.yaml"
    if path.exists():
        with open(path) as f:
            return yaml.safe_load(f)
    return {}


POWER_CYCLE_DEFAULTS: dict[PowerCycle, dict[str, float]] = {
    PowerCycle.RANKINE: {
        "eta_th": 0.40,
        "turbine_per_mw": 0.20284,
        "heat_rej_per_mw": 0.03506,
    },
    PowerCycle.BRAYTON_SCO2: {
        "eta_th": 0.47,
        "turbine_per_mw": 0.15908,
        "heat_rej_per_mw": 0.02258,
    },
    PowerCycle.COMBINED: {
        "eta_th": 0.53,
        "turbine_per_mw": 0.24118,
        "heat_rej_per_mw": 0.01847,
    },
}


@dataclass(frozen=True)
class MagnetProperties:
    """Physical properties carried by a coil-conductor selection."""

    b_max: float  # Peak field ceiling at the conductor [T]
    recirc_power_factor: float  # Recirculating power [MW / (T^2 * m^3)]; 0 for SC
    cryo_temp_k: float  # Coil operating temperature [K]


# Peak-field ceilings: REBCO HTS ~23 T, Nb3Sn ~13 T, NbTi ~9 T (superconductors,
# zero recirculating power). Copper is resistive: stress/cooling-limited field,
# continuous dissipation. Values are engineering ceilings, sourced here rather
# than inline in any solver.
MAGNET_TABLE: dict[str, MagnetProperties] = {
    "rebco_hts": MagnetProperties(
        b_max=23.0, recirc_power_factor=0.0, cryo_temp_k=20.0
    ),
    "nb3sn": MagnetProperties(b_max=13.0, recirc_power_factor=0.0, cryo_temp_k=4.5),
    "nbti": MagnetProperties(b_max=9.0, recirc_power_factor=0.0, cryo_temp_k=4.5),
    "copper": MagnetProperties(
        b_max=8.0, recirc_power_factor=2.0e-4, cryo_temp_k=300.0
    ),
}


def get_magnet_properties(coil_material: str) -> MagnetProperties:
    """Look up magnet properties by conductor selection. Raises KeyError on
    an unknown material rather than substituting a default."""
    return MAGNET_TABLE[coil_material]
