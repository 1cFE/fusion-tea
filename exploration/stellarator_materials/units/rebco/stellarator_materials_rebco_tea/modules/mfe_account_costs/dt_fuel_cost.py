"""DT_Fuel_CostModule Module Wrapper

TEAx module for DT_Fuel_Cost calculation.

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

The annual_raw, burn_correction and annual_fuel SysML expressions
generate the fuel arithmetic directly.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:476-544 (cas80_fuel, DT branch); defaults.py
(M_D_KG, u_deuterium, M_Li6_KG, u_li6, burn_fraction, fuel_recovery);
physics.py:31 (Q_DT = 17.58 MeV)
*Basis**: Reaction-rate-priced annual fuel with burn-up recovery correction

Inputs:
    - burn_fraction_in: burn_fraction_in parameter
    - cost_per_rxn: cost_per_rxn parameter
    - fuel_recovery_in: fuel_recovery_in parameter
    - mev_to_joules_in: mev_to_joules_in parameter
    - availability_in: availability_in parameter
    - n_mod_in: n_mod_in parameter
    - p_fus: p_fus parameter
    - q_eff: q_eff parameter

Outputs:
    - annual_fuel: annual_fuel result

SysML Source: root-0/analyses/mfe_account_costs.sysml:804

SysML Source: root-0/analyses/mfe_account_costs.sysml:804

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/dt_fuel_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float


class DT_Fuel_CostInput(BaseModel):
    """Input model for DT_Fuel_CostModule.

    Attributes:
        burn_fraction_in: burn_fraction_in input
        cost_per_rxn: cost_per_rxn input
        fuel_recovery_in: fuel_recovery_in input
        mev_to_joules_in: mev_to_joules_in input
        availability_in: availability_in input
        n_mod_in: n_mod_in input
        p_fus: p_fus input
        q_eff: q_eff input
    """
    burn_fraction_in: float = Field(..., description="burn_fraction_in input")
    cost_per_rxn: float = Field(..., description="cost_per_rxn input")
    fuel_recovery_in: float = Field(..., description="fuel_recovery_in input")
    mev_to_joules_in: float = Field(..., description="mev_to_joules_in input")
    availability_in: float = Field(..., description="availability_in input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    p_fus: float = Field(..., description="p_fus input")
    q_eff: float = Field(..., description="q_eff input")


class DT_Fuel_CostModule(ModuleBase[DT_Fuel_CostInput, Float]):
    """TEAx module for DT_Fuel_Cost calculation.

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

The annual_raw, burn_correction and annual_fuel SysML expressions
generate the fuel arithmetic directly.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:476-544 (cas80_fuel, DT branch); defaults.py
(M_D_KG, u_deuterium, M_Li6_KG, u_li6, burn_fraction, fuel_recovery);
physics.py:31 (Q_DT = 17.58 MeV)
*Basis**: Reaction-rate-priced annual fuel with burn-up recovery correction

Inputs:
    - burn_fraction_in: burn_fraction_in parameter
    - cost_per_rxn: cost_per_rxn parameter
    - fuel_recovery_in: fuel_recovery_in parameter
    - mev_to_joules_in: mev_to_joules_in parameter
    - availability_in: availability_in parameter
    - n_mod_in: n_mod_in parameter
    - p_fus: p_fus parameter
    - q_eff: q_eff parameter

Outputs:
    - annual_fuel: annual_fuel result

SysML Source: root-0/analyses/mfe_account_costs.sysml:804

    SysML Source: root-0/analyses/mfe_account_costs.sysml:804

    Calculation Specification:
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

The annual_raw, burn_correction and annual_fuel SysML expressions
generate the fuel arithmetic directly.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/costs.py (pin 0254385)
*Ref**: costs.py:476-544 (cas80_fuel, DT branch); defaults.py
(M_D_KG, u_deuterium, M_Li6_KG, u_li6, burn_fraction, fuel_recovery);
physics.py:31 (Q_DT = 17.58 MeV)
*Basis**: Reaction-rate-priced annual fuel with burn-up recovery correction

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_account_costs.dt_fuel_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "DT_Fuel_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, burn_fraction_in: float, cost_per_rxn: float, fuel_recovery_in: float, mev_to_joules_in: float, availability_in: float, n_mod_in: float, p_fus: float, q_eff: float    ) -> DT_Fuel_CostInput:
        """Validate inputs and fill defaults.

        Args:
            burn_fraction_in: burn_fraction_in input
            cost_per_rxn: cost_per_rxn input
            fuel_recovery_in: fuel_recovery_in input
            mev_to_joules_in: mev_to_joules_in input
            availability_in: availability_in input
            n_mod_in: n_mod_in input
            p_fus: p_fus input
            q_eff: q_eff input

        Returns:
            Validated input model
        """
        return DT_Fuel_CostInput(burn_fraction_in=burn_fraction_in, cost_per_rxn=cost_per_rxn, fuel_recovery_in=fuel_recovery_in, mev_to_joules_in=mev_to_joules_in, availability_in=availability_in, n_mod_in=n_mod_in, p_fus=p_fus, q_eff=q_eff)

    def run(
        self, burn_fraction_in: float, cost_per_rxn: float, fuel_recovery_in: float, mev_to_joules_in: float, availability_in: float, n_mod_in: float, p_fus: float, q_eff: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            burn_fraction_in: burn_fraction_in input
            cost_per_rxn: cost_per_rxn input
            fuel_recovery_in: fuel_recovery_in input
            mev_to_joules_in: mev_to_joules_in input
            availability_in: availability_in input
            n_mod_in: n_mod_in input
            p_fus: p_fus input
            q_eff: q_eff input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(burn_fraction_in, cost_per_rxn, fuel_recovery_in, mev_to_joules_in, availability_in, n_mod_in, p_fus, q_eff)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_account_costs.dt_fuel_cost_impl import (
            run_dt_fuel_cost,
        )

        # Execute implementation - returns single value
        annual_fuel = run_dt_fuel_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(annual_fuel))
