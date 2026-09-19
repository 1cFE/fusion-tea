"""Fuel_Processing_CostModule Module Wrapper

TEAx module for Fuel_Processing_Cost calculation.

Conditional conventional D+T exhaust processing, four subsystem rows and direct installation.
Source: knowledge/sources/bartlit_1983_tsta_subsystem_costs_original_osti_paper/output.md, Table II and Section III; knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/output.md, fuel-processing relation.
Reference: work/active/WI-070_throughput-based-fuel-processing-costs/design.md and evidence/account-reconciliation.md; reviewed price and transfer records in goal evidence.
Basis: near-equimolar D/T, source-like impurities, cleaned feed below 1 ppm noncondensibles, atmospheric cryogenic separation and 20 K refrigeration. Conditional 99 percent functional recovery is inherited, not established by this price. CPI is purchasing power, not current procurement. Per-module running inlet, identical independent trains times module count; no shared discount or certified capacity. Source-like conditions are declared, not measured. Included local controls belong exclusively to C220500. Limited purchased containment; no full building, storage, blanket extraction, added specialized fuel instrumentation or source installation design/inspection claim.

Inputs:
    - distiller_installation_in: distiller_installation_in parameter
    - cleanup_capital_in: cleanup_capital_in parameter
    - exponent_in: exponent_in parameter
    - enabled_in: enabled_in parameter
    - containment_installation_in: containment_installation_in parameter
    - price_multiplier_in: price_multiplier_in parameter
    - inventory_enabled_in: inventory_enabled_in parameter
    - cleanup_installation_in: cleanup_installation_in parameter
    - flow_in: flow_in parameter
    - legacy_cost_in: legacy_cost_in parameter
    - containment_capital_in: containment_capital_in parameter
    - n_mod_in: n_mod_in parameter
    - distiller_cpi_in: distiller_cpi_in parameter
    - capacity_margin_in: capacity_margin_in parameter
    - cleanup_cpi_in: cleanup_cpi_in parameter
    - transfer_installation_in: transfer_installation_in parameter
    - transfer_cpi_in: transfer_cpi_in parameter
    - reference_flow_in: reference_flow_in parameter
    - containment_cpi_in: containment_cpi_in parameter
    - transfer_capital_in: transfer_capital_in parameter
    - distiller_capital_in: distiller_capital_in parameter
    - source_conditions_in: source_conditions_in parameter
    - target_cpi_in: target_cpi_in parameter

Outputs:
    - containment_installation: containment_installation result
    - cost: cost result
    - transfer_capital: transfer_capital result
    - cleanup_reference_installation: cleanup_reference_installation result
    - cleanup_capital: cleanup_capital result
    - new_total: new_total result
    - containment_capital: containment_capital result
    - containment_reference_installation: containment_reference_installation result
    - scaling_factor: scaling_factor result
    - distiller_installation: distiller_installation result
    - cleanup_reference_capital: cleanup_reference_capital result
    - distiller_capital: distiller_capital result
    - capacity_kg_s: capacity_kg_s result
    - transfer_reference_installation: transfer_reference_installation result
    - plant_capacity_kg_s: plant_capacity_kg_s result
    - distiller_reference_capital: distiller_reference_capital result
    - installation_total: installation_total result
    - defined_flag: defined_flag result
    - flow_ratio: flow_ratio result
    - cleanup_installation: cleanup_installation result
    - equipment_total: equipment_total result
    - flow_kg_s: flow_kg_s result
    - module_total: module_total result
    - distiller_reference_installation: distiller_reference_installation result
    - transfer_reference_capital: transfer_reference_capital result
    - transfer_installation: transfer_installation result
    - containment_reference_capital: containment_reference_capital result

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:258

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:258

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_fuel_cycle/fuel_processing_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.fuel_processing_cost_output import Fuel_Processing_CostOutput


class Fuel_Processing_CostInput(BaseModel):
    """Input model for Fuel_Processing_CostModule.

    Attributes:
        distiller_installation_in: distiller_installation_in input
        cleanup_capital_in: cleanup_capital_in input
        exponent_in: exponent_in input
        enabled_in: enabled_in input
        containment_installation_in: containment_installation_in input
        price_multiplier_in: price_multiplier_in input
        inventory_enabled_in: inventory_enabled_in input
        cleanup_installation_in: cleanup_installation_in input
        flow_in: flow_in input
        legacy_cost_in: legacy_cost_in input
        containment_capital_in: containment_capital_in input
        n_mod_in: n_mod_in input
        distiller_cpi_in: distiller_cpi_in input
        capacity_margin_in: capacity_margin_in input
        cleanup_cpi_in: cleanup_cpi_in input
        transfer_installation_in: transfer_installation_in input
        transfer_cpi_in: transfer_cpi_in input
        reference_flow_in: reference_flow_in input
        containment_cpi_in: containment_cpi_in input
        transfer_capital_in: transfer_capital_in input
        distiller_capital_in: distiller_capital_in input
        source_conditions_in: source_conditions_in input
        target_cpi_in: target_cpi_in input
    """
    distiller_installation_in: float = Field(..., description="distiller_installation_in input")
    cleanup_capital_in: float = Field(..., description="cleanup_capital_in input")
    exponent_in: float = Field(..., description="exponent_in input")
    enabled_in: bool = Field(..., description="enabled_in input")
    containment_installation_in: float = Field(..., description="containment_installation_in input")
    price_multiplier_in: float = Field(..., description="price_multiplier_in input")
    inventory_enabled_in: bool = Field(..., description="inventory_enabled_in input")
    cleanup_installation_in: float = Field(..., description="cleanup_installation_in input")
    flow_in: float = Field(..., description="flow_in input")
    legacy_cost_in: float = Field(..., description="legacy_cost_in input")
    containment_capital_in: float = Field(..., description="containment_capital_in input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    distiller_cpi_in: float = Field(..., description="distiller_cpi_in input")
    capacity_margin_in: float = Field(..., description="capacity_margin_in input")
    cleanup_cpi_in: float = Field(..., description="cleanup_cpi_in input")
    transfer_installation_in: float = Field(..., description="transfer_installation_in input")
    transfer_cpi_in: float = Field(..., description="transfer_cpi_in input")
    reference_flow_in: float = Field(..., description="reference_flow_in input")
    containment_cpi_in: float = Field(..., description="containment_cpi_in input")
    transfer_capital_in: float = Field(..., description="transfer_capital_in input")
    distiller_capital_in: float = Field(..., description="distiller_capital_in input")
    source_conditions_in: bool = Field(..., description="source_conditions_in input")
    target_cpi_in: float = Field(..., description="target_cpi_in input")


class Fuel_Processing_CostModule(ModuleBase[Fuel_Processing_CostInput, Fuel_Processing_CostOutput]):
    """TEAx module for Fuel_Processing_Cost calculation.

Conditional conventional D+T exhaust processing, four subsystem rows and direct installation.
Source: knowledge/sources/bartlit_1983_tsta_subsystem_costs_original_osti_paper/output.md, Table II and Section III; knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/output.md, fuel-processing relation.
Reference: work/active/WI-070_throughput-based-fuel-processing-costs/design.md and evidence/account-reconciliation.md; reviewed price and transfer records in goal evidence.
Basis: near-equimolar D/T, source-like impurities, cleaned feed below 1 ppm noncondensibles, atmospheric cryogenic separation and 20 K refrigeration. Conditional 99 percent functional recovery is inherited, not established by this price. CPI is purchasing power, not current procurement. Per-module running inlet, identical independent trains times module count; no shared discount or certified capacity. Source-like conditions are declared, not measured. Included local controls belong exclusively to C220500. Limited purchased containment; no full building, storage, blanket extraction, added specialized fuel instrumentation or source installation design/inspection claim.

Inputs:
    - distiller_installation_in: distiller_installation_in parameter
    - cleanup_capital_in: cleanup_capital_in parameter
    - exponent_in: exponent_in parameter
    - enabled_in: enabled_in parameter
    - containment_installation_in: containment_installation_in parameter
    - price_multiplier_in: price_multiplier_in parameter
    - inventory_enabled_in: inventory_enabled_in parameter
    - cleanup_installation_in: cleanup_installation_in parameter
    - flow_in: flow_in parameter
    - legacy_cost_in: legacy_cost_in parameter
    - containment_capital_in: containment_capital_in parameter
    - n_mod_in: n_mod_in parameter
    - distiller_cpi_in: distiller_cpi_in parameter
    - capacity_margin_in: capacity_margin_in parameter
    - cleanup_cpi_in: cleanup_cpi_in parameter
    - transfer_installation_in: transfer_installation_in parameter
    - transfer_cpi_in: transfer_cpi_in parameter
    - reference_flow_in: reference_flow_in parameter
    - containment_cpi_in: containment_cpi_in parameter
    - transfer_capital_in: transfer_capital_in parameter
    - distiller_capital_in: distiller_capital_in parameter
    - source_conditions_in: source_conditions_in parameter
    - target_cpi_in: target_cpi_in parameter

Outputs:
    - containment_installation: containment_installation result
    - cost: cost result
    - transfer_capital: transfer_capital result
    - cleanup_reference_installation: cleanup_reference_installation result
    - cleanup_capital: cleanup_capital result
    - new_total: new_total result
    - containment_capital: containment_capital result
    - containment_reference_installation: containment_reference_installation result
    - scaling_factor: scaling_factor result
    - distiller_installation: distiller_installation result
    - cleanup_reference_capital: cleanup_reference_capital result
    - distiller_capital: distiller_capital result
    - capacity_kg_s: capacity_kg_s result
    - transfer_reference_installation: transfer_reference_installation result
    - plant_capacity_kg_s: plant_capacity_kg_s result
    - distiller_reference_capital: distiller_reference_capital result
    - installation_total: installation_total result
    - defined_flag: defined_flag result
    - flow_ratio: flow_ratio result
    - cleanup_installation: cleanup_installation result
    - equipment_total: equipment_total result
    - flow_kg_s: flow_kg_s result
    - module_total: module_total result
    - distiller_reference_installation: distiller_reference_installation result
    - transfer_reference_capital: transfer_reference_capital result
    - transfer_installation: transfer_installation result
    - containment_reference_capital: containment_reference_capital result

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:258

    SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:258

    Calculation Specification:
        See documentation:
Conditional conventional D+T exhaust processing, four subsystem rows and direct installation.
Source: knowledge/sources/bartlit_1983_tsta_subsystem_costs_original_osti_paper/output.md, Table II and Section III; knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/output.md, fuel-processing relation.
Reference: work/active/WI-070_throughput-based-fuel-processing-costs/design.md and evidence/account-reconciliation.md; reviewed price and transfer records in goal evidence.
Basis: near-equimolar D/T, source-like impurities, cleaned feed below 1 ppm noncondensibles, atmospheric cryogenic separation and 20 K refrigeration. Conditional 99 percent functional recovery is inherited, not established by this price. CPI is purchasing power, not current procurement. Per-module running inlet, identical independent trains times module count; no shared discount or certified capacity. Source-like conditions are declared, not measured. Included local controls belong exclusively to C220500. Limited purchased containment; no full building, storage, blanket extraction, added specialized fuel instrumentation or source installation design/inspection claim.

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_fuel_cycle.fuel_processing_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts containment_installation, cost, transfer_capital, cleanup_reference_installation, cleanup_capital, new_total, containment_capital, containment_reference_installation, scaling_factor, distiller_installation, cleanup_reference_capital, distiller_capital, capacity_kg_s, transfer_reference_installation, plant_capacity_kg_s, distiller_reference_capital, installation_total, defined_flag, flow_ratio, cleanup_installation, equipment_total, flow_kg_s, module_total, distiller_reference_installation, transfer_reference_capital, transfer_installation, containment_reference_capital fields to separate channels.
    """

    name: str = "Fuel_Processing_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, distiller_installation_in: float, cleanup_capital_in: float, exponent_in: float, enabled_in: bool, containment_installation_in: float, price_multiplier_in: float, inventory_enabled_in: bool, cleanup_installation_in: float, flow_in: float, legacy_cost_in: float, containment_capital_in: float, n_mod_in: float, distiller_cpi_in: float, capacity_margin_in: float, cleanup_cpi_in: float, transfer_installation_in: float, transfer_cpi_in: float, reference_flow_in: float, containment_cpi_in: float, transfer_capital_in: float, distiller_capital_in: float, source_conditions_in: bool, target_cpi_in: float    ) -> Fuel_Processing_CostInput:
        """Validate inputs and fill defaults.

        Args:
            distiller_installation_in: distiller_installation_in input
            cleanup_capital_in: cleanup_capital_in input
            exponent_in: exponent_in input
            enabled_in: enabled_in input
            containment_installation_in: containment_installation_in input
            price_multiplier_in: price_multiplier_in input
            inventory_enabled_in: inventory_enabled_in input
            cleanup_installation_in: cleanup_installation_in input
            flow_in: flow_in input
            legacy_cost_in: legacy_cost_in input
            containment_capital_in: containment_capital_in input
            n_mod_in: n_mod_in input
            distiller_cpi_in: distiller_cpi_in input
            capacity_margin_in: capacity_margin_in input
            cleanup_cpi_in: cleanup_cpi_in input
            transfer_installation_in: transfer_installation_in input
            transfer_cpi_in: transfer_cpi_in input
            reference_flow_in: reference_flow_in input
            containment_cpi_in: containment_cpi_in input
            transfer_capital_in: transfer_capital_in input
            distiller_capital_in: distiller_capital_in input
            source_conditions_in: source_conditions_in input
            target_cpi_in: target_cpi_in input

        Returns:
            Validated input model
        """
        return Fuel_Processing_CostInput(distiller_installation_in=distiller_installation_in, cleanup_capital_in=cleanup_capital_in, exponent_in=exponent_in, enabled_in=enabled_in, containment_installation_in=containment_installation_in, price_multiplier_in=price_multiplier_in, inventory_enabled_in=inventory_enabled_in, cleanup_installation_in=cleanup_installation_in, flow_in=flow_in, legacy_cost_in=legacy_cost_in, containment_capital_in=containment_capital_in, n_mod_in=n_mod_in, distiller_cpi_in=distiller_cpi_in, capacity_margin_in=capacity_margin_in, cleanup_cpi_in=cleanup_cpi_in, transfer_installation_in=transfer_installation_in, transfer_cpi_in=transfer_cpi_in, reference_flow_in=reference_flow_in, containment_cpi_in=containment_cpi_in, transfer_capital_in=transfer_capital_in, distiller_capital_in=distiller_capital_in, source_conditions_in=source_conditions_in, target_cpi_in=target_cpi_in)

    def run(
        self, distiller_installation_in: float, cleanup_capital_in: float, exponent_in: float, enabled_in: bool, containment_installation_in: float, price_multiplier_in: float, inventory_enabled_in: bool, cleanup_installation_in: float, flow_in: float, legacy_cost_in: float, containment_capital_in: float, n_mod_in: float, distiller_cpi_in: float, capacity_margin_in: float, cleanup_cpi_in: float, transfer_installation_in: float, transfer_cpi_in: float, reference_flow_in: float, containment_cpi_in: float, transfer_capital_in: float, distiller_capital_in: float, source_conditions_in: bool, target_cpi_in: float    ) -> ModuleResult[Fuel_Processing_CostOutput]:
        """Execute calculation.

        Args:
            distiller_installation_in: distiller_installation_in input
            cleanup_capital_in: cleanup_capital_in input
            exponent_in: exponent_in input
            enabled_in: enabled_in input
            containment_installation_in: containment_installation_in input
            price_multiplier_in: price_multiplier_in input
            inventory_enabled_in: inventory_enabled_in input
            cleanup_installation_in: cleanup_installation_in input
            flow_in: flow_in input
            legacy_cost_in: legacy_cost_in input
            containment_capital_in: containment_capital_in input
            n_mod_in: n_mod_in input
            distiller_cpi_in: distiller_cpi_in input
            capacity_margin_in: capacity_margin_in input
            cleanup_cpi_in: cleanup_cpi_in input
            transfer_installation_in: transfer_installation_in input
            transfer_cpi_in: transfer_cpi_in input
            reference_flow_in: reference_flow_in input
            containment_cpi_in: containment_cpi_in input
            transfer_capital_in: transfer_capital_in input
            distiller_capital_in: distiller_capital_in input
            source_conditions_in: source_conditions_in input
            target_cpi_in: target_cpi_in input

        Returns:
            Module result with Fuel_Processing_CostOutput (containment_installation, cost, transfer_capital, cleanup_reference_installation, cleanup_capital, new_total, containment_capital, containment_reference_installation, scaling_factor, distiller_installation, cleanup_reference_capital, distiller_capital, capacity_kg_s, transfer_reference_installation, plant_capacity_kg_s, distiller_reference_capital, installation_total, defined_flag, flow_ratio, cleanup_installation, equipment_total, flow_kg_s, module_total, distiller_reference_installation, transfer_reference_capital, transfer_installation, containment_reference_capital)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(distiller_installation_in, cleanup_capital_in, exponent_in, enabled_in, containment_installation_in, price_multiplier_in, inventory_enabled_in, cleanup_installation_in, flow_in, legacy_cost_in, containment_capital_in, n_mod_in, distiller_cpi_in, capacity_margin_in, cleanup_cpi_in, transfer_installation_in, transfer_cpi_in, reference_flow_in, containment_cpi_in, transfer_capital_in, distiller_capital_in, source_conditions_in, target_cpi_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_fuel_cycle.fuel_processing_cost_impl import (
            run_fuel_processing_cost,
        )

        # Execute implementation - returns tuple of values
        containment_installation, cost, transfer_capital, cleanup_reference_installation, cleanup_capital, new_total, containment_capital, containment_reference_installation, scaling_factor, distiller_installation, cleanup_reference_capital, distiller_capital, capacity_kg_s, transfer_reference_installation, plant_capacity_kg_s, distiller_reference_capital, installation_total, defined_flag, flow_ratio, cleanup_installation, equipment_total, flow_kg_s, module_total, distiller_reference_installation, transfer_reference_capital, transfer_installation, containment_reference_capital = run_fuel_processing_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Fuel_Processing_CostOutput(
                containment_installation=containment_installation,
                cost=cost,
                transfer_capital=transfer_capital,
                cleanup_reference_installation=cleanup_reference_installation,
                cleanup_capital=cleanup_capital,
                new_total=new_total,
                containment_capital=containment_capital,
                containment_reference_installation=containment_reference_installation,
                scaling_factor=scaling_factor,
                distiller_installation=distiller_installation,
                cleanup_reference_capital=cleanup_reference_capital,
                distiller_capital=distiller_capital,
                capacity_kg_s=capacity_kg_s,
                transfer_reference_installation=transfer_reference_installation,
                plant_capacity_kg_s=plant_capacity_kg_s,
                distiller_reference_capital=distiller_reference_capital,
                installation_total=installation_total,
                defined_flag=defined_flag,
                flow_ratio=flow_ratio,
                cleanup_installation=cleanup_installation,
                equipment_total=equipment_total,
                flow_kg_s=flow_kg_s,
                module_total=module_total,
                distiller_reference_installation=distiller_reference_installation,
                transfer_reference_capital=transfer_reference_capital,
                transfer_installation=transfer_installation,
                containment_reference_capital=containment_reference_capital,
            )
        )
