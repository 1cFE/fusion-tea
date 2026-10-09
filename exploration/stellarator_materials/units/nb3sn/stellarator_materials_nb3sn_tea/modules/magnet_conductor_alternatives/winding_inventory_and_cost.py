"""Winding_Inventory_and_CostModule Module Wrapper

TEAx module for Winding_Inventory_and_Cost calculation.

Inventory and cost of the supplied winding; never from demand. conductor_length = turns*coils*turn_length; element_length = n_elements*conductor_length; element_mass = element_area*1e-6*conductor_length*element_density (element_area is the total element area per turn, mm2); cu_mass = cu_space*(1 - cu_void)*1e-6*conductor_length*rho_cu; steel_mass = steel_area*1e-6*conductor_length*rho_steel; solder_mass = solder_area*1e-6*conductor_length*rho_solder; sc_cost = element_length*element_price_per_m; materials_cost = cu_mass*price_cu + steel_mass*price_steel + solder_mass*price_solder; manufacturing_cost = conductor_length*manufacturing_per_m; winding_capital = sc_cost + materials_cost + manufacturing_cost; ampere_metres = turn_current*conductor_length. Cabling twist is ignored (contract section 7). **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.4; contract section 7 (cost accounting and boundary). **Basis**: [AGENT] partial accounting within the evaluated categories; winding labour, heat treatment, stacking, case and structure excluded (contract section 7). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_inventory_and_cost_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - turn_length_in: turn_length_in parameter
    - price_solder_in: price_solder_in parameter
    - coils_in: coils_in parameter
    - price_cu_in: price_cu_in parameter
    - element_area_in: element_area_in parameter
    - solder_area_in: solder_area_in parameter
    - element_price_per_m_in: element_price_per_m_in parameter
    - rho_cu_in: rho_cu_in parameter
    - n_elements_in: n_elements_in parameter
    - manufacturing_per_m_in: manufacturing_per_m_in parameter
    - cu_void_in: cu_void_in parameter
    - price_steel_in: price_steel_in parameter
    - cu_space_in: cu_space_in parameter
    - rho_steel_in: rho_steel_in parameter
    - turn_current_in: turn_current_in parameter
    - turns_in: turns_in parameter
    - rho_solder_in: rho_solder_in parameter
    - steel_area_in: steel_area_in parameter
    - element_density_in: element_density_in parameter

Outputs:
    - cu_mass: cu_mass result
    - sc_cost: sc_cost result
    - winding_capital: winding_capital result
    - manufacturing_cost: manufacturing_cost result
    - conductor_length: conductor_length result
    - element_length: element_length result
    - materials_cost: materials_cost result
    - element_mass: element_mass result
    - steel_mass: steel_mass result
    - solder_mass: solder_mass result
    - ampere_metres: ampere_metres result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:132

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:132

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_conductor_alternatives/winding_inventory_and_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.winding_inventory_and_cost_output import Winding_Inventory_and_CostOutput


class Winding_Inventory_and_CostInput(BaseModel):
    """Input model for Winding_Inventory_and_CostModule.

    Attributes:
        turn_length_in: turn_length_in input
        price_solder_in: price_solder_in input
        coils_in: coils_in input
        price_cu_in: price_cu_in input
        element_area_in: element_area_in input
        solder_area_in: solder_area_in input
        element_price_per_m_in: element_price_per_m_in input
        rho_cu_in: rho_cu_in input
        n_elements_in: n_elements_in input
        manufacturing_per_m_in: manufacturing_per_m_in input
        cu_void_in: cu_void_in input
        price_steel_in: price_steel_in input
        cu_space_in: cu_space_in input
        rho_steel_in: rho_steel_in input
        turn_current_in: turn_current_in input
        turns_in: turns_in input
        rho_solder_in: rho_solder_in input
        steel_area_in: steel_area_in input
        element_density_in: element_density_in input
    """
    turn_length_in: float = Field(..., description="turn_length_in input")
    price_solder_in: float = Field(..., description="price_solder_in input")
    coils_in: float = Field(..., description="coils_in input")
    price_cu_in: float = Field(..., description="price_cu_in input")
    element_area_in: float = Field(..., description="element_area_in input")
    solder_area_in: float = Field(..., description="solder_area_in input")
    element_price_per_m_in: float = Field(..., description="element_price_per_m_in input")
    rho_cu_in: float = Field(..., description="rho_cu_in input")
    n_elements_in: float = Field(..., description="n_elements_in input")
    manufacturing_per_m_in: float = Field(..., description="manufacturing_per_m_in input")
    cu_void_in: float = Field(..., description="cu_void_in input")
    price_steel_in: float = Field(..., description="price_steel_in input")
    cu_space_in: float = Field(..., description="cu_space_in input")
    rho_steel_in: float = Field(..., description="rho_steel_in input")
    turn_current_in: float = Field(..., description="turn_current_in input")
    turns_in: float = Field(..., description="turns_in input")
    rho_solder_in: float = Field(..., description="rho_solder_in input")
    steel_area_in: float = Field(..., description="steel_area_in input")
    element_density_in: float = Field(..., description="element_density_in input")


class Winding_Inventory_and_CostModule(ModuleBase[Winding_Inventory_and_CostInput, Winding_Inventory_and_CostOutput]):
    """TEAx module for Winding_Inventory_and_Cost calculation.

Inventory and cost of the supplied winding; never from demand. conductor_length = turns*coils*turn_length; element_length = n_elements*conductor_length; element_mass = element_area*1e-6*conductor_length*element_density (element_area is the total element area per turn, mm2); cu_mass = cu_space*(1 - cu_void)*1e-6*conductor_length*rho_cu; steel_mass = steel_area*1e-6*conductor_length*rho_steel; solder_mass = solder_area*1e-6*conductor_length*rho_solder; sc_cost = element_length*element_price_per_m; materials_cost = cu_mass*price_cu + steel_mass*price_steel + solder_mass*price_solder; manufacturing_cost = conductor_length*manufacturing_per_m; winding_capital = sc_cost + materials_cost + manufacturing_cost; ampere_metres = turn_current*conductor_length. Cabling twist is ignored (contract section 7). **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.4; contract section 7 (cost accounting and boundary). **Basis**: [AGENT] partial accounting within the evaluated categories; winding labour, heat treatment, stacking, case and structure excluded (contract section 7). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_inventory_and_cost_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - turn_length_in: turn_length_in parameter
    - price_solder_in: price_solder_in parameter
    - coils_in: coils_in parameter
    - price_cu_in: price_cu_in parameter
    - element_area_in: element_area_in parameter
    - solder_area_in: solder_area_in parameter
    - element_price_per_m_in: element_price_per_m_in parameter
    - rho_cu_in: rho_cu_in parameter
    - n_elements_in: n_elements_in parameter
    - manufacturing_per_m_in: manufacturing_per_m_in parameter
    - cu_void_in: cu_void_in parameter
    - price_steel_in: price_steel_in parameter
    - cu_space_in: cu_space_in parameter
    - rho_steel_in: rho_steel_in parameter
    - turn_current_in: turn_current_in parameter
    - turns_in: turns_in parameter
    - rho_solder_in: rho_solder_in parameter
    - steel_area_in: steel_area_in parameter
    - element_density_in: element_density_in parameter

Outputs:
    - cu_mass: cu_mass result
    - sc_cost: sc_cost result
    - winding_capital: winding_capital result
    - manufacturing_cost: manufacturing_cost result
    - conductor_length: conductor_length result
    - element_length: element_length result
    - materials_cost: materials_cost result
    - element_mass: element_mass result
    - steel_mass: steel_mass result
    - solder_mass: solder_mass result
    - ampere_metres: ampere_metres result

SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:132

    SysML Source: root-0/analyses/magnet_conductor_alternatives.sysml:132

    Calculation Specification:
        n_elements_in = 0.0
        element_area_in = 0.0
        element_density_in = 0.0
        turns_in = 0.0
        coils_in = 0.0
        turn_length_in = 0.0
        turn_current_in = 0.0
        cu_space_in = 0.0
        cu_void_in = 0.0
        steel_area_in = 0.0
        solder_area_in = 0.0
        rho_cu_in = 0.0
        rho_steel_in = 0.0
        rho_solder_in = 0.0
        price_cu_in = 0.0
        price_steel_in = 0.0
        price_solder_in = 0.0
        element_price_per_m_in = 0.0
        manufacturing_per_m_in = 0.0
        
Documentation:
Inventory and cost of the supplied winding; never from demand. conductor_length = turns*coils*turn_length; element_length = n_elements*conductor_length; element_mass = element_area*1e-6*conductor_length*element_density (element_area is the total element area per turn, mm2); cu_mass = cu_space*(1 - cu_void)*1e-6*conductor_length*rho_cu; steel_mass = steel_area*1e-6*conductor_length*rho_steel; solder_mass = solder_area*1e-6*conductor_length*rho_solder; sc_cost = element_length*element_price_per_m; materials_cost = cu_mass*price_cu + steel_mass*price_steel + solder_mass*price_solder; manufacturing_cost = conductor_length*manufacturing_per_m; winding_capital = sc_cost + materials_cost + manufacturing_cost; ampere_metres = turn_current*conductor_length. Cabling twist is ignored (contract section 7). **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.4; contract section 7 (cost accounting and boundary). **Basis**: [AGENT] partial accounting within the evaluated categories; winding labour, heat treatment, stacking, case and structure excluded (contract section 7). Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/winding_inventory_and_cost_impl.py. **Last Updated**: 2026-09-29

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.magnet_conductor_alternatives.winding_inventory_and_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cu_mass, sc_cost, winding_capital, manufacturing_cost, conductor_length, element_length, materials_cost, element_mass, steel_mass, solder_mass, ampere_metres fields to separate channels.
    """

    name: str = "Winding_Inventory_and_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, turn_length_in: float, price_solder_in: float, coils_in: float, price_cu_in: float, element_area_in: float, solder_area_in: float, element_price_per_m_in: float, rho_cu_in: float, n_elements_in: float, manufacturing_per_m_in: float, cu_void_in: float, price_steel_in: float, cu_space_in: float, rho_steel_in: float, turn_current_in: float, turns_in: float, rho_solder_in: float, steel_area_in: float, element_density_in: float    ) -> Winding_Inventory_and_CostInput:
        """Validate inputs and fill defaults.

        Args:
            turn_length_in: turn_length_in input
            price_solder_in: price_solder_in input
            coils_in: coils_in input
            price_cu_in: price_cu_in input
            element_area_in: element_area_in input
            solder_area_in: solder_area_in input
            element_price_per_m_in: element_price_per_m_in input
            rho_cu_in: rho_cu_in input
            n_elements_in: n_elements_in input
            manufacturing_per_m_in: manufacturing_per_m_in input
            cu_void_in: cu_void_in input
            price_steel_in: price_steel_in input
            cu_space_in: cu_space_in input
            rho_steel_in: rho_steel_in input
            turn_current_in: turn_current_in input
            turns_in: turns_in input
            rho_solder_in: rho_solder_in input
            steel_area_in: steel_area_in input
            element_density_in: element_density_in input

        Returns:
            Validated input model
        """
        return Winding_Inventory_and_CostInput(turn_length_in=turn_length_in, price_solder_in=price_solder_in, coils_in=coils_in, price_cu_in=price_cu_in, element_area_in=element_area_in, solder_area_in=solder_area_in, element_price_per_m_in=element_price_per_m_in, rho_cu_in=rho_cu_in, n_elements_in=n_elements_in, manufacturing_per_m_in=manufacturing_per_m_in, cu_void_in=cu_void_in, price_steel_in=price_steel_in, cu_space_in=cu_space_in, rho_steel_in=rho_steel_in, turn_current_in=turn_current_in, turns_in=turns_in, rho_solder_in=rho_solder_in, steel_area_in=steel_area_in, element_density_in=element_density_in)

    def run(
        self, turn_length_in: float, price_solder_in: float, coils_in: float, price_cu_in: float, element_area_in: float, solder_area_in: float, element_price_per_m_in: float, rho_cu_in: float, n_elements_in: float, manufacturing_per_m_in: float, cu_void_in: float, price_steel_in: float, cu_space_in: float, rho_steel_in: float, turn_current_in: float, turns_in: float, rho_solder_in: float, steel_area_in: float, element_density_in: float    ) -> ModuleResult[Winding_Inventory_and_CostOutput]:
        """Execute calculation.

        Args:
            turn_length_in: turn_length_in input
            price_solder_in: price_solder_in input
            coils_in: coils_in input
            price_cu_in: price_cu_in input
            element_area_in: element_area_in input
            solder_area_in: solder_area_in input
            element_price_per_m_in: element_price_per_m_in input
            rho_cu_in: rho_cu_in input
            n_elements_in: n_elements_in input
            manufacturing_per_m_in: manufacturing_per_m_in input
            cu_void_in: cu_void_in input
            price_steel_in: price_steel_in input
            cu_space_in: cu_space_in input
            rho_steel_in: rho_steel_in input
            turn_current_in: turn_current_in input
            turns_in: turns_in input
            rho_solder_in: rho_solder_in input
            steel_area_in: steel_area_in input
            element_density_in: element_density_in input

        Returns:
            Module result with Winding_Inventory_and_CostOutput (cu_mass, sc_cost, winding_capital, manufacturing_cost, conductor_length, element_length, materials_cost, element_mass, steel_mass, solder_mass, ampere_metres)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(turn_length_in, price_solder_in, coils_in, price_cu_in, element_area_in, solder_area_in, element_price_per_m_in, rho_cu_in, n_elements_in, manufacturing_per_m_in, cu_void_in, price_steel_in, cu_space_in, rho_steel_in, turn_current_in, turns_in, rho_solder_in, steel_area_in, element_density_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.magnet_conductor_alternatives.winding_inventory_and_cost_impl import (
            run_winding_inventory_and_cost,
        )

        # Execute implementation - returns tuple of values
        cu_mass, sc_cost, winding_capital, manufacturing_cost, conductor_length, element_length, materials_cost, element_mass, steel_mass, solder_mass, ampere_metres = run_winding_inventory_and_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Inventory_and_CostOutput(
                cu_mass=cu_mass,
                sc_cost=sc_cost,
                winding_capital=winding_capital,
                manufacturing_cost=manufacturing_cost,
                conductor_length=conductor_length,
                element_length=element_length,
                materials_cost=materials_cost,
                element_mass=element_mass,
                steel_mass=steel_mass,
                solder_mass=solder_mass,
                ampere_metres=ampere_metres,
            )
        )
