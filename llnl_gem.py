"""
LLNL Generalized Economic Model (GEM) v1.0
Python translation of LLNL_GEM_v1.0.xlsm

DISCLAIMER: This software is intended for educational purposes only. Numerical
values, assumptions, and conclusions do not reflect assumptions or projections
of Lawrence Livermore National Laboratory.

Reference: LLNL_GEM_v1.0.xlsm (January 2026)
"""

import math
from dataclasses import dataclass, field
from typing import Literal

# ==============================================================================
# CPI DATA (US Bureau of Labor Statistics, CPI-U, December year-end values)
# Last updated: 20250918
# ==============================================================================
CPI_DATA = {
    1990: 133.8,  1991: 137.9,  1992: 141.9,  1993: 145.8,
    1994: 149.7,  1995: 153.5,  1996: 158.6,  1997: 161.3,
    1998: 163.9,  1999: 168.3,  2000: 174.0,  2001: 176.7,
    2002: 180.9,  2003: 184.3,  2004: 190.3,  2005: 196.8,
    2006: 201.8,  2007: 210.036, 2008: 210.228, 2009: 215.949,
    2010: 219.179, 2011: 225.672, 2012: 229.601, 2013: 233.049,
    2014: 234.812, 2015: 236.525, 2016: 241.432, 2017: 246.524,
    2018: 251.233, 2019: 256.974, 2020: 260.474, 2021: 278.802,
    2022: 296.797, 2023: 306.746, 2024: 315.605, 2025: 323.976,
    2026: 330.455, 2027: 337.065,
}

def cpi_inflation(basis_year: int, eval_year: int) -> float:
    """Return CPI-based inflation factor from basis_year to eval_year."""
    return CPI_DATA[eval_year] / CPI_DATA[basis_year]


# ==============================================================================
# INPUTS
# ==============================================================================
@dataclass
class GEMInputs:
    # --- Primary Design Variables ---
    laser_energy_MJ: float = 5.0       # Laser energy on target [MJ], must be 2–10
    pulse_rep_freq_Hz: float = 10.0    # Pulse repetition frequency [Hz]

    # --- Optional Plant Size Variable ---
    net_electric_power_MWe: float = 1000.0  # Only used with fix_net_power mode

    # --- Operating and Cost Multipliers ---
    gain_curve_multiplier: float = 0.25    # Scales gain curve down from theoretical
    driver_efficiency_multiplier: float = 0.85
    driver_cost_multiplier: float = 1.0
    target_cost_multiplier: float = 1.0

    # --- Secondary Design Variables ---
    plant_type: Literal[1, 2] = 2          # 1=LIFE, 2=HAPL
    thermal_conversion_efficiency: float = 0.40
    auxiliary_power_fraction: float = 0.05
    plant_availability: float = 0.85

    # --- Economic Design Variables ---
    cost_eval_year: int = 2025
    om_fraction: float = 0.03             # O&M as fraction of direct capital cost
    fixed_charge_rate: float = 0.075
    design_construction_fraction: float = 0.35
    project_contingency_fraction: float = 0.20
    interest_during_construction_fraction: float = 0.12

    def validate(self):
        if not (2.0 <= self.laser_energy_MJ <= 10.0):
            raise ValueError("Laser energy must be between 2 and 10 MJ.")


# ==============================================================================
# MODULE 1: Target Gain and Yield (Sheet 5)
# Reference: Amendt et al., FST 60, 49 (2011), LLNL-JRNL-513734
# ==============================================================================
def calc_target_gain_yield(inputs: GEMInputs) -> dict:
    """
    Gain curve fit from two reference points extracted from Fig. 1 right panel.
    Points used: (2.0 MJ, yield=100 MJ) and (2.2 MJ, yield=132 MJ)
    plus (2.5974 MJ, 200 MJ) and (3.0928 MJ, 300 MJ) to fit gain scaling coefficient.

    Gain(E) = ref_gain * (E / ref_E)^gain_scaling_coeff
    """
    # Reference point
    ref_laser_energy_MJ = 2.2
    ref_fusion_gain = 60.0

    # Gain scaling coefficient fitted from multiple reference points
    # Derived by log-log fit: slope = ln(97/50) / ln(3.0928/2.0) = 1.5050...
    gain_scaling_coeff = 1.5050488181748096

    E = inputs.laser_energy_MJ
    G_raw = ref_fusion_gain * (E / ref_laser_energy_MJ) ** gain_scaling_coeff
    G_with_mult = G_raw * inputs.gain_curve_multiplier
    fusion_yield_MJ = E * G_with_mult

    return {
        "gain_raw": G_raw,
        "fusion_gain_at_target": G_with_mult,
        "fusion_yield_MJ": fusion_yield_MJ,
    }


# ==============================================================================
# MODULE 2: Fusion and Thermal Power (Sheet 6)
# Reference: Meier LLNL-MI-666819 (2015); Sawan 11/8-9/2005 HAPL talk
# ==============================================================================
ENERGY_MULT_FACTOR = {1: 1.19, 2: 1.09}  # LIFE=1.19, HAPL=1.09

def calc_fusion_thermal_power(inputs: GEMInputs, target: dict) -> dict:
    fusion_yield_MJ = target["fusion_yield_MJ"]
    fusion_power_MW = fusion_yield_MJ * inputs.pulse_rep_freq_Hz  # MJ/shot * shots/s = MW

    emf = ENERGY_MULT_FACTOR[inputs.plant_type]
    thermal_power_MW = fusion_power_MW * emf
    gross_electric_MW = thermal_power_MW * inputs.thermal_conversion_efficiency

    return {
        "fusion_power_MW": fusion_power_MW,
        "energy_mult_factor": emf,
        "thermal_power_MW": thermal_power_MW,
        "gross_electric_MW": gross_electric_MW,
    }


# ==============================================================================
# MODULE 3: Burn Fraction and Tritium Flow (Sheet 7)
# Reference: Amendt et al. (2011); Miles et al. LLNL-TR-416932 (2009);
#            Perkins et al. PRL 103, 045004 (2009)
# ==============================================================================
def calc_tritium_flow(inputs: GEMInputs, target: dict) -> dict:
    tritium_breeding_ratio = 1.1
    fusion_yield_MJ = target["fusion_yield_MJ"]

    # Physical constants
    dt_ice_density = 0.255      # g/cm³
    dt_gas_density = 0.0004     # g/cm³
    avogadro = 6.022e23
    fusion_energy_MeV = 17.6
    eV_per_J = 1.602e-19
    fusion_energy_MJ = fusion_energy_MeV * 1e6 * eV_per_J  # MJ per reaction
    mass_DT_amu = 5.03          # amu

    # Specific yield (MJ/g DT)
    mass_per_atom_g = mass_DT_amu / avogadro
    specific_yield_MJ_per_g = fusion_energy_MJ / mass_per_atom_g

    # Reference capsule dimensions at 2.2 MJ (indirect drive)
    ref_laser_energy_MJ = 2.2
    ref_dt_gas_radius_cm = 0.18
    ref_dt_ice_inner_radius_cm = 0.18
    ref_dt_ice_thickness_cm = 0.015
    ref_capsule_inner_radius_cm = 0.195
    ref_capsule_outer_radius_cm = 0.205

    # Scale geometry with (E/E_ref)^(1/3) (constant neutron flux assumption)
    scale = (inputs.laser_energy_MJ / ref_laser_energy_MJ) ** (1.0 / 3.0)
    dt_gas_radius_cm = ref_dt_gas_radius_cm * scale
    dt_ice_inner_radius_cm = ref_dt_ice_inner_radius_cm * scale
    dt_ice_thickness_cm = ref_dt_ice_thickness_cm * scale
    capsule_inner_radius_cm = ref_capsule_inner_radius_cm * scale
    capsule_outer_radius_cm = ref_capsule_outer_radius_cm * scale

    # Volumes
    dt_gas_volume_cm3 = (4.0 / 3.0) * math.pi * dt_gas_radius_cm ** 3
    dt_ice_outer_r = dt_ice_inner_radius_cm + dt_ice_thickness_cm
    dt_ice_volume_cm3 = (4.0 / 3.0) * math.pi * (dt_ice_outer_r ** 3 - dt_ice_inner_radius_cm ** 3)
    dt_fuel_mass_g = dt_ice_volume_cm3 * dt_ice_density + dt_gas_volume_cm3 * dt_gas_density

    # 100% burn yield and burn fraction
    full_burn_yield_MJ = dt_fuel_mass_g * specific_yield_MJ_per_g
    burn_fraction = fusion_yield_MJ / full_burn_yield_MJ

    # Daily tritium mass flow rate (g/day at 100% capacity)
    seconds_per_day = 86400.0
    shots_per_day = inputs.pulse_rep_freq_Hz * seconds_per_day
    total_dt_burned_g = dt_fuel_mass_g * burn_fraction * shots_per_day
    total_dt_unburned_g = dt_fuel_mass_g * (1 - burn_fraction) * shots_per_day
    # Tritium mass ratio
    tritium_fraction = 3.016 / mass_DT_amu
    tritium_burned_g_day   = total_dt_burned_g   * tritium_fraction
    tritium_unburned_g_day = total_dt_unburned_g * tritium_fraction
    # Bred tritium from blanket = TBR x burned
    tritium_bred_g_day = tritium_breeding_ratio * tritium_burned_g_day
    # Total daily tritium handling = unburned (recycle) + bred (from blanket)
    # Matches T_Flow named range in spreadsheet (Sheet 7, row 46)
    daily_tritium_flow_g = tritium_unburned_g_day + tritium_bred_g_day

    return {
        "burn_fraction":            burn_fraction,
        "dt_fuel_mass_g":           dt_fuel_mass_g,
        "tritium_burned_g_day":     tritium_burned_g_day,
        "tritium_unburned_g_day":   tritium_unburned_g_day,
        "tritium_bred_g_day":       tritium_bred_g_day,
        "daily_tritium_flow_g_day": daily_tritium_flow_g,
        "tritium_breeding_ratio":   tritium_breeding_ratio,
    }


# ==============================================================================
# MODULE 4: Fusion Fuel (Target) Cost - Indirect Drive (Sheet 8)
# Reference: Miles et al. LLNL-TR-416932 (2009)
# ==============================================================================
def calc_fusion_fuel_cost(inputs: GEMInputs) -> dict:
    """
    Target fabrication cost (Indirect Drive).
    Reference: Miles et al. LLNL-TR-416932 (Sept. 18, 2009).

    Capital cost uses a two-point linear fit to Fig. 2b:
        annual_capital = A + B × rep_rate
    Material cost per target uses blended area scaling (Table I):
        cost = ref_cost × [ablator_frac × (E/E_ref)  +  (1-ablator_frac) × (E/E_ref)^(2/3)]
    """
    cost_basis_year = 2009
    # Sheet 8 formula references CPI range A$8:B$41 (only to 2023);
    # LOOKUP caps at last range value, so years > 2023 use 2023 CPI.
    inflation = cpi_inflation(cost_basis_year, min(inputs.cost_eval_year, 2023))

    E     = inputs.laser_energy_MJ
    f     = inputs.pulse_rep_freq_Hz
    E_ref = 2.2    # MJ
    f_ref = 15.0   # Hz
    SPY   = 3600 * 24 * 365 / 1e6   # million seconds/year = 31.536

    # ── Material cost per target ──────────────────────────────────────────
    # ablator (0.0169 $) scales linearly with E; non-ablator scales as E^(2/3)
    Target_Matl_Ref = 0.0175
    ablator_frac    = 0.0169 / Target_Matl_Ref
    ratio_E = E / E_ref
    mat_cost_per_tgt_2009 = Target_Matl_Ref * (
        ablator_frac * ratio_E + (1.0 - ablator_frac) * ratio_E ** (2.0 / 3.0)
    )
    annual_material_2009 = mat_cost_per_tgt_2009 * f * SPY   # $M

    # ── O&M and labor (scale linearly with rep rate) ──────────────────────
    annual_om_2009    = 45.161 * f / f_ref   # $M
    annual_labor_2009 = 18.800 * f / f_ref   # $M

    # ── Capital: two-point curve fit from Fig. 2b ─────────────────────────
    # Solve capital at 5 Hz and 25 Hz by subtracting materials+O&M+labor from total
    def _non_capital(freq):
        return (Target_Matl_Ref * freq * SPY
                + 45.161 * freq / f_ref
                + 18.800 * freq / f_ref)

    cap_5Hz  = 40.0  - _non_capital(5.0)
    cap_25Hz = 150.0 - _non_capital(25.0)
    B_cap = (cap_25Hz - cap_5Hz) / (25.0 - 5.0)
    A_cap = cap_25Hz - B_cap * 25.0
    annual_capital_2009 = A_cap + B_cap * f   # $M

    # ── Inflate to evaluation year ────────────────────────────────────────
    annual_material_eval = annual_material_2009 * inflation
    annual_capital_eval  = annual_capital_2009  * inflation
    annual_om_eval       = annual_om_2009       * inflation
    annual_labor_eval    = annual_labor_2009    * inflation

    total_target_cost_eval = (
        annual_material_eval + annual_capital_eval + annual_om_eval + annual_labor_eval
    ) * inputs.target_cost_multiplier

    return {
        "inflation_factor":            inflation,
        "annual_material_cost_eval_M": annual_material_eval,
        "annual_capital_cost_eval_M":  annual_capital_eval,
        "annual_om_cost_eval_M":       annual_om_eval,
        "annual_labor_cost_eval_M":    annual_labor_eval,
        "total_target_cost_eval_M":    total_target_cost_eval,
        "cost_per_target_eval":        total_target_cost_eval * 1e6 / (f * SPY * 1e6),
    }


# ==============================================================================
# MODULE 5: Driver Power and Cost (Sheet 9)
# References: Anklam LLNL-TR-480444 (2011); Amendt et al. FST 60, 49 (2011)
# ==============================================================================
def calc_driver_power_cost(inputs: GEMInputs, power: dict) -> dict:
    cost_basis_year = 2011
    inflation = cpi_inflation(cost_basis_year, inputs.cost_eval_year)

    ref_unit_cost_per_kW = 1400.0    # $/kW
    ref_plant_size_MWe = 900.0       # MWe
    ref_laser_energy_MJ = 2.2        # MJ

    # Convert $/kWe to $/J for the driver
    basis_unit_cost_per_J = (
        ref_unit_cost_per_kW * ref_plant_size_MWe * 1e3 / (ref_laser_energy_MJ * 1e6)
    )
    eval_unit_cost_per_J = basis_unit_cost_per_J * inflation

    # Driver equipment cost scales linearly with laser energy
    driver_cost_M = (
        eval_unit_cost_per_J * inputs.laser_energy_MJ * 1e6 / 1e6
        * inputs.driver_cost_multiplier
    )

    # Driver efficiency and power
    ref_driver_efficiency = 0.15
    driver_efficiency = ref_driver_efficiency * inputs.driver_efficiency_multiplier
    driver_power_MWe = (
        inputs.laser_energy_MJ * inputs.pulse_rep_freq_Hz / driver_efficiency
    )

    return {
        "inflation_factor": inflation,
        "driver_efficiency": driver_efficiency,
        "driver_power_MWe": driver_power_MWe,
        "driver_direct_cost_M": driver_cost_M,
    }


# ==============================================================================
# MODULE 6a: Balance of Plant Cost – LIFE (Sheet 10)
# Reference: Anklam LLNL-TR-480444 (2011)
# ==============================================================================
def calc_tritium_flow_life_reference(inputs: GEMInputs) -> float:
    """
    Compute the LIFE-reference tritium flow (g/day) used for scaling.
    This is the tritium flow at the LIFE reference laser energy (2.2 MJ) and rep freq (15 Hz).
    Named range T_Flow_LIFE in the spreadsheet = 1522.17 g/day.
    Hardcoded to match the spreadsheet reference value exactly.
    """
    return 1522.1663844952807  # g/day, from Sheet 7 row 46 column B


def calc_bop_cost_life(inputs: GEMInputs, power: dict, tritium: dict) -> dict:
    cost_basis_year = 2011
    inflation = cpi_inflation(cost_basis_year, inputs.cost_eval_year)

    # Reference LIFE plant (2nd of a kind, 910 MWe)
    ref_net_MWe = 910.0
    tech_discount = 0.15     # 2nd-of-a-kind technology improvement discount
    learn_discount = 0.05    # 2nd-of-a-kind learning discount
    first_of_kind_factor = 1.0 / ((1.0 - tech_discount) * (1.0 - learn_discount))

    # 2nd-of-a-kind unit costs ($/kWe) from Figure 4 of LLNL-TR-480444
    unit_costs_per_kW = {
        "target_tracking":  10.0,
        "controls":        100.0,
        "tritium_plant":   150.0,
        "power_conversion": 500.0,
        "fusion_engine":   550.0,
        "facilities":      700.0,
    }

    # Which items have technology/learning applied (vs. fixed)
    apply_discount = {
        "target_tracking":  True,
        "controls":         True,
        "tritium_plant":    True,
        "power_conversion": False,  # No discount applied
        "fusion_engine":    True,
        "facilities":       False,  # No discount applied
    }

    # Reference costs in basis year ($M) – 2nd-of-a-kind
    ref_2nd_M = {k: v * ref_net_MWe * 1e3 / 1e6 for k, v in unit_costs_per_kW.items()}

    # Convert to 1st-of-a-kind
    ref_1st_M = {}
    for k, v in ref_2nd_M.items():
        ref_1st_M[k] = v * first_of_kind_factor if apply_discount[k] else v

    # Inflate to evaluation year ($M)
    ref_eval_M = {k: v * inflation for k, v in ref_1st_M.items()}

    # Reference scaling parameters (from sheet 10 rows 42-46)
    ref_thermal_MW     = 2640.0   # MWt (reference scaling parameter for thermal-scaled items)
    t_flow_life_ref    = calc_tritium_flow_life_reference(inputs)  # g/day

    thermal_MW    = power["thermal_power_MW"]
    tritium_flow  = tritium["daily_tritium_flow_g_day"]

    current_M = {
        "target_tracking":  ref_eval_M["target_tracking"],                             # Fixed
        "controls":         ref_eval_M["controls"]        * thermal_MW / ref_thermal_MW,
        "tritium_plant":    ref_eval_M["tritium_plant"]   * tritium_flow / t_flow_life_ref,
        "power_conversion": ref_eval_M["power_conversion"] * thermal_MW / ref_thermal_MW,
        "fusion_engine":    ref_eval_M["fusion_engine"]   * thermal_MW / ref_thermal_MW,
        "facilities":       ref_eval_M["facilities"]      * thermal_MW / ref_thermal_MW,
    }

    total_bop_M = sum(current_M.values())

    return {
        "inflation_factor": inflation,
        "line_items_M": current_M,
        "total_bop_direct_cost_M": total_bop_M,
    }


# ==============================================================================
# MODULE 6b: Chamber Cost – HAPL (Sheet 11)
# Reference: Sviatoslavsky et al., FST 47, 535 (2005)
# ==============================================================================
def calc_chamber_cost_hapl(inputs: GEMInputs, target: dict) -> dict:
    # Material costs
    W_basis_year = 2016
    W_inflation = cpi_inflation(W_basis_year, inputs.cost_eval_year)
    W_basis_cost_per_kg = 43.67      # $/kg
    W_manufacture_premium = 3.0
    W_unit_cost = W_basis_cost_per_kg * W_inflation * W_manufacture_premium

    ODS_basis_year = 2016
    ODS_inflation = cpi_inflation(ODS_basis_year, inputs.cost_eval_year)
    ODS_basis_cost_per_kg = 10.0     # $/kg
    ODS_manufacture_premium = 3.0
    ODS_unit_cost = ODS_basis_cost_per_kg * ODS_inflation * ODS_manufacture_premium

    # Material densities
    W_density   = 19300.0    # kg/m³
    ODS_density = 7470.0     # kg/m³

    # First-wall radius scaling: R ~ sqrt(yield) at constant neutron flux
    # Reference: base design (6.5 m, 150 MJ); Sviatoslavsky et al. Fig. 2
    ref_fw_radius_m  = 6.5
    ref_yield_MJ     = 150.0
    Yield_HAPL       = ref_yield_MJ
    FW_Radius_HAPL   = ref_fw_radius_m
    current_yield_MJ = target["fusion_yield_MJ"]
    fw_radius_m      = FW_Radius_HAPL * math.sqrt(current_yield_MJ / Yield_HAPL)
    fw_radius_cm     = fw_radius_m * 100.0

    # Blanket layer stack (cm thicknesses from Fig. 2 of Sviatoslavsky et al.)
    layers = [
        ("Tungsten Armor",          "W",   0.10),
        ("First wall",              "ODS", 0.35),
        ("Li channel – FW",         "Li",  0.50),
        ("Li channel wall",         "ODS", 0.20),
        ("W coating inner channel", "W",   0.10),
        ("Li blanket",              "Li",  55.0),
        ("W coating outer channel", "W",   0.10),
        ("Li channel wall",         "ODS", 0.20),
        ("Li channel – outer",      "Li",  0.50),
        ("Outer wall",              "ODS", 0.35),
    ]

    # Volume of each spherical shell: 4π/3 * (r_out³ - r_in³), with r in cm → m³ by /1e6
    r = fw_radius_cm
    layer_vols = {}
    for name, mat, thick_cm in layers:
        r_out = r + thick_cm
        vol_m3 = (4.0 / 3.0) * math.pi * (r_out ** 3 - r ** 3) / 1e6
        layer_vols[name] = (mat, vol_m3)
        r = r_out

    blanket_outer_radius_m = r / 100.0   # same as E48/100 in spreadsheet

    # Aggregate by material (only structural layers, not Li)
    W_vol_blanket   = sum(v for _, (m, v) in layer_vols.items() if m == "W")
    ODS_vol_blanket = sum(v for _, (m, v) in layer_vols.items() if m == "ODS")

    # Submodule side walls
    # Submodule area = π * (blanket_outer² − fw_radius²)  [total washer area, not per submodule]
    submodule_area_m2 = math.pi * (blanket_outer_radius_m ** 2 - fw_radius_m ** 2)
    # Volume per wall = thickness_cm / 100 * submodule_area_m2
    # Total volume = 312 * volume_per_wall  (row 78: =312*C78)
    W_vol_side   = (0.10 / 100.0) * submodule_area_m2 * 312   # W coating
    ODS_vol_side = (0.20 / 100.0) * submodule_area_m2 * 312   # channel inner wall
    ODS_vol_side += (0.35 / 100.0) * submodule_area_m2 * 312  # channel outer wall

    # Total structural volumes
    W_total_vol   = W_vol_blanket   + W_vol_side
    ODS_total_vol = ODS_vol_blanket + ODS_vol_side

    # Chamber structure cost
    W_mass   = W_total_vol   * W_density
    ODS_mass = ODS_total_vol * ODS_density
    chamber_cost_M = (W_mass * W_unit_cost + ODS_mass * ODS_unit_cost) / 1e6

    # Vacuum vessel (ODS ferritic steel, 0.5 m thick)
    # Inner radius = blanket_outer + 0.1 m gap  (row 96: =Blanket_Outer_Radius+0.1)
    vv_inner_radius_m = blanket_outer_radius_m + 0.1
    vv_wall_thick_m   = 0.5
    vv_outer_radius_m = vv_inner_radius_m + vv_wall_thick_m
    # Height = 2 * inner_radius * 1.7  (row 96: =2*B96*1.7)
    vv_height_m       = 2.0 * vv_inner_radius_m * 1.7
    # Side wall volume (cylindrical shell)
    vv_side_vol_m3    = math.pi * (vv_outer_radius_m ** 2 - vv_inner_radius_m ** 2) * vv_height_m
    # Top + bottom caps (flat discs: 2 * π * outer² * thickness)  (row 102: =2*PI()*D97^2*C97)
    vv_disk_vol_m3    = 2.0 * math.pi * vv_outer_radius_m ** 2 * vv_wall_thick_m
    # 15% helium coolant channel reduces solid material  (rows 101-102: (1-0.15)*volume)
    vv_side_solid_m3  = vv_side_vol_m3 * (1.0 - 0.15)
    vv_disk_solid_m3  = vv_disk_vol_m3 * (1.0 - 0.15)
    vv_cost_M = (
        (vv_side_solid_m3 + vv_disk_solid_m3) * ODS_density * ODS_unit_cost / 1e6
    )

    total_chamber_cost_M = chamber_cost_M + vv_cost_M

    # Lithium volume in chamber shell (from row 107: 4/3*π*(outer³ - fw³))
    Li_vol_in_chamber_m3 = (
        (4.0 / 3.0) * math.pi * (blanket_outer_radius_m ** 3 - fw_radius_m ** 3)
        - W_total_vol - ODS_total_vol
    )

    return {
        "fw_radius_m":              fw_radius_m,
        "blanket_outer_radius_m":   blanket_outer_radius_m,
        "W_total_vol_m3":           W_total_vol,
        "ODS_total_vol_m3":         ODS_total_vol,
        "chamber_structure_cost_M": chamber_cost_M,
        "vacuum_vessel_cost_M":     vv_cost_M,
        "total_chamber_cost_M":     total_chamber_cost_M,
        "Li_vol_in_chamber_m3":     Li_vol_in_chamber_m3,
    }


# ==============================================================================
# MODULE 6c: Lithium Mass and Cost (Sheet 13)
# Reference: Hoffman, Fusion Technology 19, 625 (1991)
# ==============================================================================
def calc_lithium_cost(inputs: GEMInputs, power: dict, chamber: dict) -> dict:
    Li_basis_year = 2016
    Li_inflation = cpi_inflation(Li_basis_year, inputs.cost_eval_year)
    Li_basis_cost_per_kg = 180.0
    Li_manufacture_premium = 1.5
    Li_unit_cost = Li_basis_cost_per_kg * Li_inflation * Li_manufacture_premium

    # Lithium density
    Li_density = 485.0   # kg/m³

    # Thermal properties
    thermal_MW = power["thermal_power_MW"]
    cp_Li = 4200.0       # J/kg-K
    T_inlet = 405.0      # °C
    T_outlet = 575.0     # °C
    dT = T_outlet - T_inlet

    mass_flow_kg_s = thermal_MW * 1e6 / (cp_Li * dT)
    vol_flow_m3_s = mass_flow_kg_s / Li_density

    # Piping volume
    Li_velocity = 5.0     # m/s
    flow_area_m2 = vol_flow_m3_s / Li_velocity
    n_loops = 4
    pipe_length_per_loop = 30.0    # m (outbound + return)
    Li_pipe_vol_m3 = (flow_area_m2 / n_loops) * pipe_length_per_loop * n_loops  # = flow_area * pipe_length

    # Intermediate heat exchanger volume
    ref_IHX_vol_m3 = 25.0           # m³ per HX
    ref_thermal_per_loop_MW = 1000.0
    current_thermal_per_loop_MW = thermal_MW / n_loops
    Li_IHX_vol_m3 = (
        ref_IHX_vol_m3 * (current_thermal_per_loop_MW / ref_thermal_per_loop_MW) * n_loops
    )

    # Chamber volume from chamber sheet
    Li_chamber_vol_m3 = chamber.get("Li_vol_in_chamber_m3", 482.27)

    total_Li_vol_m3 = Li_pipe_vol_m3 + Li_IHX_vol_m3 + Li_chamber_vol_m3
    Li_mass_MT = total_Li_vol_m3 * Li_density / 1000.0   # metric tonnes
    Li_cost_M = Li_mass_MT * 1000.0 * Li_unit_cost / 1e6

    return {
        "Li_unit_cost_per_kg": Li_unit_cost,
        "Li_pipe_vol_m3": Li_pipe_vol_m3,
        "Li_IHX_vol_m3": Li_IHX_vol_m3,
        "Li_chamber_vol_m3": Li_chamber_vol_m3,
        "total_Li_vol_m3": total_Li_vol_m3,
        "Li_mass_MT": Li_mass_MT,
        "Li_cost_M": Li_cost_M,
    }


# ==============================================================================
# MODULE 6d: Molten Salt Mass and Cost (Sheet 14)
# References: ASME ES2007-36172; Hoffman, FT 19, 625 (1991)
# ==============================================================================
def calc_molten_salt_cost(inputs: GEMInputs, power: dict) -> dict:
    ms_basis_year = 2007
    ms_inflation = cpi_inflation(ms_basis_year, inputs.cost_eval_year)
    ms_basis_cost_per_kg = 0.50     # $/kg (NaNO3-KNO3 mixture)
    ms_manufacture_premium = 1.5
    ms_unit_cost = ms_basis_cost_per_kg * ms_inflation * ms_manufacture_premium

    # Molten salt thermal properties (NaNO3-KNO3 60/40 wt%)
    thermal_MW = power["thermal_power_MW"]
    cp_ms = 1510.0      # J/kg-K
    T_inlet = 324.0     # °C
    T_outlet = 568.0    # °C
    dT = T_outlet - T_inlet
    ms_density = 1729.0  # kg/m³

    mass_flow_kg_s = thermal_MW * 1e6 / (cp_ms * dT)
    vol_flow_m3_s = mass_flow_kg_s / ms_density

    # Piping volume
    ms_velocity = 5.0    # m/s
    flow_area_m2 = vol_flow_m3_s / ms_velocity
    n_loops = 4
    pipe_length_per_loop = 30.0   # m
    ms_pipe_vol_m3 = (flow_area_m2 / n_loops) * pipe_length_per_loop * n_loops  # = flow_area * pipe_length

    # Intermediate heat exchanger + steam generator volumes
    ref_IHX_vol_m3 = 100.0
    ref_thermal_per_loop_MW = 1000.0
    current_thermal_per_loop_MW = thermal_MW / n_loops
    ms_IHX_vol_m3 = (
        ref_IHX_vol_m3 * (current_thermal_per_loop_MW / ref_thermal_per_loop_MW) * n_loops
    )
    ms_SG_vol_m3 = ms_IHX_vol_m3   # Same assumption

    total_ms_vol_m3 = ms_pipe_vol_m3 + ms_IHX_vol_m3 + ms_SG_vol_m3
    ms_mass_MT = total_ms_vol_m3 * ms_density / 1000.0
    ms_cost_M = ms_mass_MT * 1000.0 * ms_unit_cost / 1e6

    return {
        "ms_unit_cost_per_kg": ms_unit_cost,
        "ms_pipe_vol_m3": ms_pipe_vol_m3,
        "ms_IHX_vol_m3": ms_IHX_vol_m3,
        "ms_SG_vol_m3": ms_SG_vol_m3,
        "total_ms_vol_m3": total_ms_vol_m3,
        "ms_mass_MT": ms_mass_MT,
        "ms_cost_M": ms_cost_M,
    }


# ==============================================================================
# MODULE 7: Balance of Plant Cost – HAPL (Sheet 12)
# References: Multiple (Prometheus 1991, Osiris 1991/1995, NETL 2018, WSI 2020, LIFE 2011)
# ==============================================================================
def calc_bop_cost_hapl(
    inputs: GEMInputs,
    power: dict,
    tritium: dict,
    chamber: dict,
    lithium: dict,
    molten_salt: dict,
) -> dict:
    inf_1991 = cpi_inflation(1991, inputs.cost_eval_year)
    inf_1995 = cpi_inflation(1995, inputs.cost_eval_year)
    inf_2011 = cpi_inflation(2011, inputs.cost_eval_year)
    inf_2018 = cpi_inflation(2018, inputs.cost_eval_year)
    inf_2020 = cpi_inflation(2020, inputs.cost_eval_year)

    thermal_MW  = power["thermal_power_MW"]
    gross_MW    = power["gross_electric_MW"]
    tritium_flow = tritium["daily_tritium_flow_g_day"]

    # Reference scaling parameters (columns I in sheet 12)
    ref_gross_prometheus_MWe  = 1382.0   # MWe  (Accts 21, 23, 24, 40–41)
    ref_thermal_osiris_MWt    = 2504.0   # MWt  (HTS items)
    t_flow_life_ref           = calc_tritium_flow_life_reference(inputs)   # g/day
    ref_thermal_IC_MWt        = 3264.0   # MWt  (I&C)
    ref_gross_NETL_MWe        = 685.0    # MWe  (turbine, electrical)
    ref_gross_WSI_MWe         = 1000.0   # MWe  (misc equipment)
    ref_heat_rej_MW           = 928.0    # MW   (heat rejection = thermal - gross)

    # Account 20: Land (fixed)
    acct20_land = 10.0 * inf_1991

    # Account 21: Structures (Prometheus 1991, scale with gross power / 1382)
    structures_basis = {
        "site_improvements":          21.00,
        "fusion_operations_building": 106.06,
        "laser_building":              36.52,
        "turbine_building":            57.18,
        "heat_rejection":              11.48,
        "target_fab_building":         46.92,
        "tritium_waste_building":      46.92,
        "misc_structures":             35.03,
    }
    acct21_structures = sum(
        v * inf_1991 * (gross_MW / ref_gross_prometheus_MWe)
        for v in structures_basis.values()
    )

    # Account 22: Fusion Plant Equipment
    fusion_chamber_cost_M   = chamber["chamber_structure_cost_M"]
    vacuum_vessel_cost_M    = chamber["vacuum_vessel_cost_M"]

    # HTS (Osiris 1991, scale with thermal / 2504)
    primary_HTS     = 49.1  * inf_1991 * thermal_MW / ref_thermal_osiris_MWt
    IHX             = 97.8  * inf_1991 * thermal_MW / ref_thermal_osiris_MWt
    secondary_HTS   = 39.8  * inf_1991 * thermal_MW / ref_thermal_osiris_MWt
    steam_generator = 58.0  * inf_1991 * thermal_MW / ref_thermal_osiris_MWt
    HTS_total = primary_HTS + IHX + secondary_HTS + steam_generator

    # Tritium plant equipment (LIFE 2011, scale with T_Flow / T_Flow_LIFE)
    tritium_plant_equip = 136.5 * inf_2011 * tritium_flow / t_flow_life_ref

    # Fusion Engine I&C (Prometheus 1991, scale with thermal / 3264)
    fusion_IC = 26.6 * inf_1991 * thermal_MW / ref_thermal_IC_MWt

    # Remote Maintenance (Osiris 1995, fixed)
    remote_maintenance = 50.0 * inf_1995

    fusion_fuel_systems = tritium_plant_equip
    acct22_fusion_equip = (
        fusion_chamber_cost_M + vacuum_vessel_cost_M
        + HTS_total + fusion_fuel_systems + fusion_IC + remote_maintenance
    )

    # Account 23: Turbine Plant (NETL 2018, scale with gross / 685)
    acct23_turbine = 150.0 * inf_2018 * gross_MW / ref_gross_NETL_MWe

    # Account 24: Electrical (NETL 2018, scale with gross / 685)
    acct24_electrical = 37.0 * inf_2018 * gross_MW / ref_gross_NETL_MWe

    # Account 25: Misc Equipment (WSI 2020, scale with gross / 1000)
    acct25_misc = 38.0 * inf_2020 * gross_MW / ref_gross_WSI_MWe

    # Account 26: Heat Rejection (NETL 2018, scale with (thermal-gross) / 928)
    heat_rej_MW = thermal_MW - gross_MW
    acct26_heat_rejection = 47.0 * inf_2018 * heat_rej_MW / ref_heat_rej_MW

    # Account 27: Special Materials (lithium + molten salt)
    Li_cost = lithium["Li_cost_M"]
    ms_cost = molten_salt["ms_cost_M"]
    acct27_special = Li_cost + ms_cost

    total_bop_M = (
        acct20_land + acct21_structures + acct22_fusion_equip
        + acct23_turbine + acct24_electrical + acct25_misc
        + acct26_heat_rejection + acct27_special
    )

    return {
        "acct20_land_M":           acct20_land,
        "acct21_structures_M":     acct21_structures,
        "acct22_fusion_equip_M":   acct22_fusion_equip,
        "acct23_turbine_M":        acct23_turbine,
        "acct24_electrical_M":     acct24_electrical,
        "acct25_misc_M":           acct25_misc,
        "acct26_heat_rejection_M": acct26_heat_rejection,
        "acct27_special_M":        acct27_special,
        "total_bop_direct_cost_M": total_bop_M,
        "breakdown": {
            "fusion_chamber":  fusion_chamber_cost_M,
            "vacuum_system":   vacuum_vessel_cost_M,
            "HTS":             HTS_total,
            "fuel_systems":    fusion_fuel_systems,
            "IC":              fusion_IC,
            "remote_maint":    remote_maintenance,
        },
    }


# ==============================================================================
# MODULE 8: Key Outputs and Cost of Electricity (Sheet 2)
# ==============================================================================
def calc_key_outputs(
    inputs: GEMInputs,
    target: dict,
    power: dict,
    tritium: dict,
    fuel_cost: dict,
    driver: dict,
    bop: dict,
) -> dict:
    # Net electric power
    driver_power_MWe = driver["driver_power_MWe"]
    gross_MWe = power["gross_electric_MW"]
    aux_power_MWe = gross_MWe * inputs.auxiliary_power_fraction
    net_electric_MWe = gross_MWe - driver_power_MWe - aux_power_MWe

    # Direct capital costs
    driver_direct_cost_M = driver["driver_direct_cost_M"]
    bop_direct_cost_M = bop["total_bop_direct_cost_M"]
    total_direct_cost_M = driver_direct_cost_M + bop_direct_cost_M

    # Indirect costs
    design_construction_M = total_direct_cost_M * inputs.design_construction_fraction
    project_contingency_M = total_direct_cost_M * inputs.project_contingency_fraction
    total_overnight_cost_M = total_direct_cost_M + design_construction_M + project_contingency_M
    interest_construction_M = total_overnight_cost_M * inputs.interest_during_construction_fraction
    total_capital_cost_M = total_overnight_cost_M + interest_construction_M

    # Annual costs
    annual_capital_cost_M = total_capital_cost_M * inputs.fixed_charge_rate
    annual_om_cost_M = total_direct_cost_M * inputs.om_fraction
    annual_target_cost_M = fuel_cost["total_target_cost_eval_M"]

    # Annual net electricity to grid (MWh)
    hours_per_year = 8760.0  # spreadsheet uses 24*365
    annual_net_MWh = net_electric_MWe * hours_per_year * inputs.plant_availability

    # Cost of electricity ($/MWh)
    total_annual_cost_M = annual_capital_cost_M + annual_om_cost_M + annual_target_cost_M
    COE_per_MWh = total_annual_cost_M * 1e6 / annual_net_MWh

    # COE breakdown
    COE_capital = annual_capital_cost_M * 1e6 / annual_net_MWh
    COE_om = annual_om_cost_M * 1e6 / annual_net_MWh
    COE_fuel = annual_target_cost_M * 1e6 / annual_net_MWh

    return {
        # Technical
        "fusion_gain_at_target":           target["fusion_gain_at_target"],
        "fusion_yield_MJ":                 target["fusion_yield_MJ"],
        "fusion_power_MW":                 power["fusion_power_MW"],
        "thermal_power_MW":                power["thermal_power_MW"],
        "gross_electric_MWe":              gross_MWe,
        "driver_power_MWe":                driver_power_MWe,
        "driver_efficiency":               driver["driver_efficiency"],
        "aux_power_MWe":                   aux_power_MWe,
        "net_electric_MWe":                net_electric_MWe,
        "driver_recirc_fraction":          driver_power_MWe / gross_MWe,
        # Capital costs ($M)
        "driver_direct_cost_M":            driver_direct_cost_M,
        "bop_direct_cost_M":               bop_direct_cost_M,
        "total_direct_cost_M":             total_direct_cost_M,
        "design_construction_M":           design_construction_M,
        "project_contingency_M":           project_contingency_M,
        "total_overnight_cost_M":          total_overnight_cost_M,
        "interest_construction_M":         interest_construction_M,
        "total_capital_cost_M":            total_capital_cost_M,
        # Annual costs ($M)
        "annual_capital_cost_M":           annual_capital_cost_M,
        "annual_om_cost_M":                annual_om_cost_M,
        "annual_target_cost_M":            annual_target_cost_M,
        "annual_net_electricity_MWh":      annual_net_MWh,
        # COE ($/MWh)
        "COE_total_per_MWh":               COE_per_MWh,
        "COE_capital_per_MWh":             COE_capital,
        "COE_om_per_MWh":                  COE_om,
        "COE_fuel_per_MWh":                COE_fuel,
        "COE_capital_fraction":            COE_capital / COE_per_MWh,
        "COE_om_fraction":                 COE_om / COE_per_MWh,
        "COE_fuel_fraction":               COE_fuel / COE_per_MWh,
    }


# ==============================================================================
# TOP-LEVEL RUNNER
# ==============================================================================
def run_gem(inputs: GEMInputs) -> dict:
    """Run the full GEM model and return all results."""
    inputs.validate()

    target   = calc_target_gain_yield(inputs)
    power    = calc_fusion_thermal_power(inputs, target)
    tritium  = calc_tritium_flow(inputs, target)
    fuel     = calc_fusion_fuel_cost(inputs)
    driver   = calc_driver_power_cost(inputs, power)

    if inputs.plant_type == 1:   # LIFE
        bop = calc_bop_cost_life(inputs, power, tritium)
        chamber  = {"total_chamber_cost_M": 0.0, "vacuum_vessel_cost_M": 0.0,
                    "Li_vol_in_chamber_m3": 0.0}
        lithium  = {"Li_cost_M": 0.0, "Li_mass_MT": 0.0, "total_Li_vol_m3": 0.0,
                    "Li_unit_cost_per_kg": 0.0}
        ms       = {"ms_cost_M": 0.0, "ms_mass_MT": 0.0}
    else:                        # HAPL
        chamber  = calc_chamber_cost_hapl(inputs, target)
        lithium  = calc_lithium_cost(inputs, power, chamber)
        ms       = calc_molten_salt_cost(inputs, power)
        bop      = calc_bop_cost_hapl(inputs, power, tritium, chamber, lithium, ms)

    outputs = calc_key_outputs(inputs, target, power, tritium, fuel, driver, bop)

    return {
        "inputs":   inputs,
        "target":   target,
        "power":    power,
        "tritium":  tritium,
        "fuel":     fuel,
        "driver":   driver,
        "chamber":  chamber,
        "lithium":  lithium,
        "molten_salt": ms,
        "bop":      bop,
        "outputs":  outputs,
    }


def print_results(results: dict):
    o = results["outputs"]
    i = results["inputs"]
    plant_name = "LIFE" if i.plant_type == 1 else "HAPL"
    print("=" * 65)
    print("  LLNL Generalized Economic Model (GEM) v1.0 – Python Port")
    print("=" * 65)
    print(f"\n  Plant type: {plant_name} | Eval year: {i.cost_eval_year}")
    print(f"  Laser energy: {i.laser_energy_MJ} MJ  |  Rep freq: {i.pulse_rep_freq_Hz} Hz")
    print(f"  Gain multiplier: {i.gain_curve_multiplier}  |  Driver eff. mult.: {i.driver_efficiency_multiplier}")

    print("\n--- Technical Results ---")
    print(f"  Fusion gain at target:          {o['fusion_gain_at_target']:.2f}  [-]")
    print(f"  Fusion yield at target:         {o['fusion_yield_MJ']:.1f}  [MJ]")
    print(f"  Fusion power:                   {o['fusion_power_MW']:.1f}  [MW]")
    print(f"  Thermal power:                  {o['thermal_power_MW']:.1f}  [MWt]")
    print(f"  Gross electric power:           {o['gross_electric_MWe']:.1f}  [MWe]")
    print(f"  Driver power:                   {o['driver_power_MWe']:.1f}  [MWe]")
    print(f"  Driver efficiency:              {o['driver_efficiency']:.4f}  [-]")
    print(f"  Aux power consumption:          {o['aux_power_MWe']:.1f}  [MWe]")
    print(f"  Net electric power:             {o['net_electric_MWe']:.1f}  [MWe]")
    print(f"  Driver recirc. fraction:        {o['driver_recirc_fraction']:.3f}  [-]")

    print("\n--- Capital Cost Summary ---")
    print(f"  Driver direct cost:             ${o['driver_direct_cost_M']:.1f}M")
    print(f"  BOP direct cost:                ${o['bop_direct_cost_M']:.1f}M")
    print(f"  Total direct cost:              ${o['total_direct_cost_M']:.1f}M")
    print(f"  Design & construction:          ${o['design_construction_M']:.1f}M")
    print(f"  Project contingency:            ${o['project_contingency_M']:.1f}M")
    print(f"  Total overnight cost:           ${o['total_overnight_cost_M']:.1f}M")
    print(f"  Interest during construction:   ${o['interest_construction_M']:.1f}M")
    print(f"  Total capital cost:             ${o['total_capital_cost_M']:.1f}M")

    print("\n--- Cost of Electricity ---")
    print(f"  Annual capital cost:            ${o['annual_capital_cost_M']:.1f}M")
    print(f"  Annual O&M cost:                ${o['annual_om_cost_M']:.1f}M")
    print(f"  Annual target (fuel) cost:      ${o['annual_target_cost_M']:.1f}M")
    print(f"  Annual net electricity:         {o['annual_net_electricity_MWh']/1e6:.2f}M MWh")
    print(f"  COE – Capital:                  ${o['COE_capital_per_MWh']:.2f}/MWh  ({o['COE_capital_fraction']*100:.1f}%)")
    print(f"  COE – O&M:                      ${o['COE_om_per_MWh']:.2f}/MWh  ({o['COE_om_fraction']*100:.1f}%)")
    print(f"  COE – Fuel (targets):           ${o['COE_fuel_per_MWh']:.2f}/MWh  ({o['COE_fuel_fraction']*100:.1f}%)")
    print(f"\n  ★ Cost of Electricity (COE):    ${o['COE_total_per_MWh']:.2f}/MWh")
    print("=" * 65)


# ==============================================================================
# PARAMETRIC SCAN HELPER
# ==============================================================================
def parametric_scan(
    base_inputs: GEMInputs,
    param: str,
    values: list,
) -> list[dict]:
    """
    Run GEM across a range of values for a single input parameter.

    Args:
        base_inputs: baseline GEMInputs (will be copied and modified)
        param:       attribute name on GEMInputs to vary (e.g. 'laser_energy_MJ')
        values:      list of values to sweep

    Returns:
        List of output dicts (one per value), each containing the param value
        and all key outputs.
    """
    from copy import deepcopy
    rows = []
    for v in values:
        inp = deepcopy(base_inputs)
        setattr(inp, param, v)
        try:
            r = run_gem(inp)
            row = {param: v, **r["outputs"]}
        except Exception as e:
            row = {param: v, "error": str(e)}
        rows.append(row)
    return rows


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    # --- Default run (matches spreadsheet defaults) ---
    inputs = GEMInputs(
        laser_energy_MJ=5.0,
        pulse_rep_freq_Hz=10.0,
        gain_curve_multiplier=0.25,
        driver_efficiency_multiplier=0.85,
        plant_type=2,            # HAPL
        cost_eval_year=2025,
    )
    results = run_gem(inputs)
    print_results(results)

    # --- Example parametric scan: laser energy vs COE ---
    print("\n--- Parametric Scan: Laser Energy vs COE ---")
    print(f"{'Laser (MJ)':>12}  {'Net MWe':>10}  {'COE ($/MWh)':>14}")
    print("-" * 42)
    scan = parametric_scan(inputs, "laser_energy_MJ", [2, 3, 4, 5, 6, 7, 8, 9, 10])
    for row in scan:
        if "error" in row:
            print(f"{row['laser_energy_MJ']:>12.1f}  ERROR: {row['error']}")
        else:
            print(f"{row['laser_energy_MJ']:>12.1f}  {row['net_electric_MWe']:>10.1f}  {row['COE_total_per_MWh']:>14.2f}")
