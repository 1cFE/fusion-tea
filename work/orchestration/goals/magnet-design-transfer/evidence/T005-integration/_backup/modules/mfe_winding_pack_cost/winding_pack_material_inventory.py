"""Winding_Pack_Material_InventoryModule Module Wrapper

TEAx module for Winding_Pack_Material_Inventory calculation.

Non-tape winding-pack inventory and procurement, excluding casing and extra cold equipment.
Normative manual-completion equations: helium_density = helium_pressure / (helium_gas_constant * temperature); mass_i = volume_in * f_i * rho_i for copper, solder, steel and helium; cost_i = mass_i * price_i; material_cost = cost_copper + cost_solder + cost_steel + cost_helium; tape_volume = volume_in * (1 - f_copper - f_solder - f_steel - f_helium).
Units: volume and tape_volume m^3; densities kg/m^3; masses kg; pressure Pa; temperature K; gas constant J/(kg K); prices dollars/kg; costs dollars. Tape is purchased separately as composite tape, with no second substrate/stabilizer charge. Fixed composition and ideal-gas helium are transfer approximations; inter-pancake insulation is unquantified and omitted.
Domain: every input and output finite; volume_in >= 0; each fraction >= 0 and < 1, with sum < 1; densities, pressure, temperature and gas constant > 0; prices >= 0. The typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic, and refuses non-finite results. Arithmetic validity does not qualify an arbitrary temperature or composition.
*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md; knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
*Reference**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md (20 K, 15/20 bar); knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
*Last Updated**: 2026-09-13

Inputs:
    - price_steel: price_steel parameter
    - f_steel: f_steel parameter
    - price_solder: price_solder parameter
    - f_copper: f_copper parameter
    - f_solder: f_solder parameter
    - rho_solder: rho_solder parameter
    - f_helium: f_helium parameter
    - rho_steel: rho_steel parameter
    - volume_in: volume_in parameter
    - rho_copper: rho_copper parameter
    - temperature: temperature parameter
    - price_helium: price_helium parameter
    - price_copper: price_copper parameter
    - helium_pressure: helium_pressure parameter
    - helium_gas_constant: helium_gas_constant parameter

Outputs:
    - tape_volume: tape_volume result
    - mass_steel: mass_steel result
    - mass_helium: mass_helium result
    - cost_copper: cost_copper result
    - mass_copper: mass_copper result
    - cost_helium: cost_helium result
    - mass_solder: mass_solder result
    - cost_steel: cost_steel result
    - material_cost: material_cost result
    - helium_density: helium_density result
    - cost_solder: cost_solder result

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:4

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_winding_pack_cost/winding_pack_material_inventory_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.winding_pack_material_inventory_output import Winding_Pack_Material_InventoryOutput


class Winding_Pack_Material_InventoryInput(BaseModel):
    """Input model for Winding_Pack_Material_InventoryModule.

    Attributes:
        price_steel: price_steel input
        f_steel: f_steel input
        price_solder: price_solder input
        f_copper: f_copper input
        f_solder: f_solder input
        rho_solder: rho_solder input
        f_helium: f_helium input
        rho_steel: rho_steel input
        volume_in: volume_in input
        rho_copper: rho_copper input
        temperature: temperature input
        price_helium: price_helium input
        price_copper: price_copper input
        helium_pressure: helium_pressure input
        helium_gas_constant: helium_gas_constant input
    """
    price_steel: float = Field(..., description="price_steel input")
    f_steel: float = Field(..., description="f_steel input")
    price_solder: float = Field(..., description="price_solder input")
    f_copper: float = Field(..., description="f_copper input")
    f_solder: float = Field(..., description="f_solder input")
    rho_solder: float = Field(..., description="rho_solder input")
    f_helium: float = Field(..., description="f_helium input")
    rho_steel: float = Field(..., description="rho_steel input")
    volume_in: float = Field(..., description="volume_in input")
    rho_copper: float = Field(..., description="rho_copper input")
    temperature: float = Field(..., description="temperature input")
    price_helium: float = Field(..., description="price_helium input")
    price_copper: float = Field(..., description="price_copper input")
    helium_pressure: float = Field(..., description="helium_pressure input")
    helium_gas_constant: float = Field(..., description="helium_gas_constant input")


class Winding_Pack_Material_InventoryModule(ModuleBase[Winding_Pack_Material_InventoryInput, Winding_Pack_Material_InventoryOutput]):
    """TEAx module for Winding_Pack_Material_Inventory calculation.

Non-tape winding-pack inventory and procurement, excluding casing and extra cold equipment.
Normative manual-completion equations: helium_density = helium_pressure / (helium_gas_constant * temperature); mass_i = volume_in * f_i * rho_i for copper, solder, steel and helium; cost_i = mass_i * price_i; material_cost = cost_copper + cost_solder + cost_steel + cost_helium; tape_volume = volume_in * (1 - f_copper - f_solder - f_steel - f_helium).
Units: volume and tape_volume m^3; densities kg/m^3; masses kg; pressure Pa; temperature K; gas constant J/(kg K); prices dollars/kg; costs dollars. Tape is purchased separately as composite tape, with no second substrate/stabilizer charge. Fixed composition and ideal-gas helium are transfer approximations; inter-pancake insulation is unquantified and omitted.
Domain: every input and output finite; volume_in >= 0; each fraction >= 0 and < 1, with sum < 1; densities, pressure, temperature and gas constant > 0; prices >= 0. The typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic, and refuses non-finite results. Arithmetic validity does not qualify an arbitrary temperature or composition.
*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md; knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
*Reference**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md (20 K, 15/20 bar); knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
*Last Updated**: 2026-09-13

Inputs:
    - price_steel: price_steel parameter
    - f_steel: f_steel parameter
    - price_solder: price_solder parameter
    - f_copper: f_copper parameter
    - f_solder: f_solder parameter
    - rho_solder: rho_solder parameter
    - f_helium: f_helium parameter
    - rho_steel: rho_steel parameter
    - volume_in: volume_in parameter
    - rho_copper: rho_copper parameter
    - temperature: temperature parameter
    - price_helium: price_helium parameter
    - price_copper: price_copper parameter
    - helium_pressure: helium_pressure parameter
    - helium_gas_constant: helium_gas_constant parameter

Outputs:
    - tape_volume: tape_volume result
    - mass_steel: mass_steel result
    - mass_helium: mass_helium result
    - cost_copper: cost_copper result
    - mass_copper: mass_copper result
    - cost_helium: cost_helium result
    - mass_solder: mass_solder result
    - cost_steel: cost_steel result
    - material_cost: material_cost result
    - helium_density: helium_density result
    - cost_solder: cost_solder result

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:4

    SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:4

    Calculation Specification:
        See documentation:
Non-tape winding-pack inventory and procurement, excluding casing and extra cold equipment.
Normative manual-completion equations: helium_density = helium_pressure / (helium_gas_constant * temperature); mass_i = volume_in * f_i * rho_i for copper, solder, steel and helium; cost_i = mass_i * price_i; material_cost = cost_copper + cost_solder + cost_steel + cost_helium; tape_volume = volume_in * (1 - f_copper - f_solder - f_steel - f_helium).
Units: volume and tape_volume m^3; densities kg/m^3; masses kg; pressure Pa; temperature K; gas constant J/(kg K); prices dollars/kg; costs dollars. Tape is purchased separately as composite tape, with no second substrate/stabilizer charge. Fixed composition and ideal-gas helium are transfer approximations; inter-pancake insulation is unquantified and omitted.
Domain: every input and output finite; volume_in >= 0; each fraction >= 0 and < 1, with sum < 1; densities, pressure, temperature and gas constant > 0; prices >= 0. The typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic, and refuses non-finite results. Arithmetic validity does not qualify an arbitrary temperature or composition.
*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md; knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
*Reference**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details/images/page_021_table_0.png; knowledge/sources/nist_helium_isotherm_20_k_15_to_20_bar/output.md (20 K, 15/20 bar); knowledge/sources/nist_helium_isobar_20_bar_10_to_50_k/output.md.
*Last Updated**: 2026-09-13

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_winding_pack_cost.winding_pack_material_inventory_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts tape_volume, mass_steel, mass_helium, cost_copper, mass_copper, cost_helium, mass_solder, cost_steel, material_cost, helium_density, cost_solder fields to separate channels.
    """

    name: str = "Winding_Pack_Material_InventoryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, price_steel: float, f_steel: float, price_solder: float, f_copper: float, f_solder: float, rho_solder: float, f_helium: float, rho_steel: float, volume_in: float, rho_copper: float, temperature: float, price_helium: float, price_copper: float, helium_pressure: float, helium_gas_constant: float    ) -> Winding_Pack_Material_InventoryInput:
        """Validate inputs and fill defaults.

        Args:
            price_steel: price_steel input
            f_steel: f_steel input
            price_solder: price_solder input
            f_copper: f_copper input
            f_solder: f_solder input
            rho_solder: rho_solder input
            f_helium: f_helium input
            rho_steel: rho_steel input
            volume_in: volume_in input
            rho_copper: rho_copper input
            temperature: temperature input
            price_helium: price_helium input
            price_copper: price_copper input
            helium_pressure: helium_pressure input
            helium_gas_constant: helium_gas_constant input

        Returns:
            Validated input model
        """
        return Winding_Pack_Material_InventoryInput(price_steel=price_steel, f_steel=f_steel, price_solder=price_solder, f_copper=f_copper, f_solder=f_solder, rho_solder=rho_solder, f_helium=f_helium, rho_steel=rho_steel, volume_in=volume_in, rho_copper=rho_copper, temperature=temperature, price_helium=price_helium, price_copper=price_copper, helium_pressure=helium_pressure, helium_gas_constant=helium_gas_constant)

    def run(
        self, price_steel: float, f_steel: float, price_solder: float, f_copper: float, f_solder: float, rho_solder: float, f_helium: float, rho_steel: float, volume_in: float, rho_copper: float, temperature: float, price_helium: float, price_copper: float, helium_pressure: float, helium_gas_constant: float    ) -> ModuleResult[Winding_Pack_Material_InventoryOutput]:
        """Execute calculation.

        Args:
            price_steel: price_steel input
            f_steel: f_steel input
            price_solder: price_solder input
            f_copper: f_copper input
            f_solder: f_solder input
            rho_solder: rho_solder input
            f_helium: f_helium input
            rho_steel: rho_steel input
            volume_in: volume_in input
            rho_copper: rho_copper input
            temperature: temperature input
            price_helium: price_helium input
            price_copper: price_copper input
            helium_pressure: helium_pressure input
            helium_gas_constant: helium_gas_constant input

        Returns:
            Module result with Winding_Pack_Material_InventoryOutput (tape_volume, mass_steel, mass_helium, cost_copper, mass_copper, cost_helium, mass_solder, cost_steel, material_cost, helium_density, cost_solder)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(price_steel, f_steel, price_solder, f_copper, f_solder, rho_solder, f_helium, rho_steel, volume_in, rho_copper, temperature, price_helium, price_copper, helium_pressure, helium_gas_constant)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_winding_pack_cost.winding_pack_material_inventory_impl import (
            run_winding_pack_material_inventory,
        )

        # Execute implementation - returns tuple of values
        tape_volume, mass_steel, mass_helium, cost_copper, mass_copper, cost_helium, mass_solder, cost_steel, material_cost, helium_density, cost_solder = run_winding_pack_material_inventory(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Pack_Material_InventoryOutput(
                tape_volume=tape_volume,
                mass_steel=mass_steel,
                mass_helium=mass_helium,
                cost_copper=cost_copper,
                mass_copper=mass_copper,
                cost_helium=cost_helium,
                mass_solder=mass_solder,
                cost_steel=cost_steel,
                material_cost=material_cost,
                helium_density=helium_density,
                cost_solder=cost_solder,
            )
        )
