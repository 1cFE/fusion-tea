"""Auto-generated implementation for DT_Fuel_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:730

SysML Expressions:
    n_mod_in = 1.0
    annual_raw = n_mod_in * p_fus * (3600.0 * 8760.0) * 1000000.0 * availability_in * cost_per_rxn / (q_eff * mev_to_joules_in)
    burn_correction = 1.0 + (1.0 - burn_fraction_in) / burn_fraction_in * (1.0 - fuel_recovery_in)
    annual_fuel = annual_raw * burn_correction
    
Documentation:
CAS80 RAW (unlevelized) annual D-T fuel cost:

  annual_raw = n_mod * p_fus * (3600*8760) * availability
cost_per_rxn / (q_eff * mev_to_joules)
annual_fuel = annual_raw * (1 + (1-burn_fraction)/burn_fraction
(1 - fuel_recovery))

The first line converts annual fusion energy to reactions (dividing by
the per-reaction energy q_eff in MeV, converted to joules) and prices
them at the blended deuterium + Li-6 cost per reaction. The second line
is the burn-up recovery correction: only `burn_fraction` of the fuel
injected is burnt, and `fuel_recovery` of the unburnt remainder is
recycled, so the make-up stream scales the raw cost.

The levelization to the reported CAS80 is NOT carried here -- the plant
feeds `annual_fuel` into 'Levelized Annual Cost' (one levelization
wrapper, MR-3). The MFE target-consumable term of 1cfe's cas80_fuel is
structurally zero (IFE-only) and is likewise not carried.

All fuel constants are inputs, never library defaults (MR-3) -- a
concept binds its own fuel chemistry and unit prices.

Flat-Real (+ - * / **) -- Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:476-544 (cas80_fuel, DT branch); defaults.py
(M_D_KG, u_deuterium, M_Li6_KG, u_li6, burn_fraction, fuel_recovery);
physics.py:31 (Q_DT = 17.58 MeV)
*Basis**: Reaction-rate-priced annual fuel with burn-up recovery correction
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.dt_fuel_cost import DT_Fuel_CostInput


def run_dt_fuel_cost(inputs: DT_Fuel_CostInput) -> float:
    """Execute DT_Fuel_Cost calculation.

CAS80 RAW (unlevelized) annual D-T fuel cost:

  annual_raw = n_mod * p_fus * (3600*8760) * availability
cost_per_rxn / (q_eff * mev_to_joules)
annual_fuel = annual_raw * (1 + (1-burn_fraction)/burn_fraction
(1 - fuel_recovery))

The first line converts annual fusion energy to reactions (dividing by
the per-reaction energy q_eff in MeV, converted to joules) and prices
them at the blended deuterium + Li-6 cost per reaction. The second line
is the burn-up recovery correction: only `burn_fraction` of the fuel
injected is burnt, and `fuel_recovery` of the unburnt remainder is
recycled, so the make-up stream scales the raw cost.

The levelization to the reported CAS80 is NOT carried here -- the plant
feeds `annual_fuel` into 'Levelized Annual Cost' (one levelization
wrapper, MR-3). The MFE target-consumable term of 1cfe's cas80_fuel is
structurally zero (IFE-only) and is likewise not carried.

All fuel constants are inputs, never library defaults (MR-3) -- a
concept binds its own fuel chemistry and unit prices.

Flat-Real (+ - * / **) -- Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:476-544 (cas80_fuel, DT branch); defaults.py
(M_D_KG, u_deuterium, M_Li6_KG, u_li6, burn_fraction, fuel_recovery);
physics.py:31 (Q_DT = 17.58 MeV)
*Basis**: Reaction-rate-priced annual fuel with burn-up recovery correction

SysML Source: root-0/analyses/mfe_account_costs.sysml:730

SysML Expressions:
    n_mod_in = 1.0
    annual_raw = n_mod_in * p_fus * (3600.0 * 8760.0) * 1000000.0 * availability_in * cost_per_rxn / (q_eff * mev_to_joules_in)
    burn_correction = 1.0 + (1.0 - burn_fraction_in) / burn_fraction_in * (1.0 - fuel_recovery_in)
    annual_fuel = annual_raw * burn_correction
    
Documentation:
CAS80 RAW (unlevelized) annual D-T fuel cost:

  annual_raw = n_mod * p_fus * (3600*8760) * availability
cost_per_rxn / (q_eff * mev_to_joules)
annual_fuel = annual_raw * (1 + (1-burn_fraction)/burn_fraction
(1 - fuel_recovery))

The first line converts annual fusion energy to reactions (dividing by
the per-reaction energy q_eff in MeV, converted to joules) and prices
them at the blended deuterium + Li-6 cost per reaction. The second line
is the burn-up recovery correction: only `burn_fraction` of the fuel
injected is burnt, and `fuel_recovery` of the unburnt remainder is
recycled, so the make-up stream scales the raw cost.

The levelization to the reported CAS80 is NOT carried here -- the plant
feeds `annual_fuel` into 'Levelized Annual Cost' (one levelization
wrapper, MR-3). The MFE target-consumable term of 1cfe's cas80_fuel is
structurally zero (IFE-only) and is likewise not carried.

All fuel constants are inputs, never library defaults (MR-3) -- a
concept binds its own fuel chemistry and unit prices.

Flat-Real (+ - * / **) -- Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:476-544 (cas80_fuel, DT branch); defaults.py
(M_D_KG, u_deuterium, M_Li6_KG, u_li6, burn_fraction, fuel_recovery);
physics.py:31 (Q_DT = 17.58 MeV)
*Basis**: Reaction-rate-priced annual fuel with burn-up recovery correction

Args:
    inputs: Input parameters validated against DT_Fuel_CostInput schema

Returns:
    float: annual_fuel

Example:
    >>> inputs = DT_Fuel_CostInput(...)
    >>> result = run_dt_fuel_cost(inputs)
    """
    annual_raw = ((((((inputs.n_mod_in * inputs.p_fus) * (3600.0 * 8760.0)) * 1000000.0) * inputs.availability_in) * inputs.cost_per_rxn) / (inputs.q_eff * inputs.mev_to_joules_in))
    burn_correction = (1.0 + (((1.0 - inputs.burn_fraction_in) / inputs.burn_fraction_in) * (1.0 - inputs.fuel_recovery_in)))
    return (annual_raw * burn_correction)
