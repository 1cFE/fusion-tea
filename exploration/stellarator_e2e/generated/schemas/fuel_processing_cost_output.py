from pydantic import Field
from simkit.config.schema import MultiOutput

class Fuel_Processing_CostOutput(MultiOutput):
    """Multi-output container for Fuel_Processing_Cost.

Conditional conventional D+T exhaust processing, four subsystem rows and direct installation.
Source: knowledge/sources/bartlit_1983_tsta_subsystem_costs_original_osti_paper/output.md, Table II and Section III; knowledge/sources/etr_iter_systems_code_ornl_fedc_87_7_1988/output.md, fuel-processing relation.
Reference: work/active/WI-070_throughput-based-fuel-processing-costs/design.md and evidence/account-reconciliation.md; reviewed price and transfer records in goal evidence.
Basis: near-equimolar D/T, source-like impurities, cleaned feed below 1 ppm noncondensibles, atmospheric cryogenic separation and 20 K refrigeration. Conditional 99 percent functional recovery is inherited, not established by this price. CPI is purchasing power, not current procurement. Per-module running inlet, identical independent trains times module count; no shared discount or certified capacity. Source-like conditions are declared, not measured. Included local controls belong exclusively to C220500. Limited purchased containment; no full building, storage, blanket extraction, added specialized fuel instrumentation or source installation design/inspection claim.

SysML Source: root-0/analyses/mfe_fuel_cycle.sysml:258
    """
    containment_installation: float = Field(description="containment_installation output")
    cost: float = Field(description="cost output")
    transfer_capital: float = Field(description="transfer_capital output")
    cleanup_reference_installation: float = Field(description="cleanup_reference_installation output")
    cleanup_capital: float = Field(description="cleanup_capital output")
    new_total: float = Field(description="new_total output")
    containment_capital: float = Field(description="containment_capital output")
    containment_reference_installation: float = Field(description="containment_reference_installation output")
    scaling_factor: float = Field(description="scaling_factor output")
    distiller_installation: float = Field(description="distiller_installation output")
    cleanup_reference_capital: float = Field(description="cleanup_reference_capital output")
    distiller_capital: float = Field(description="distiller_capital output")
    capacity_kg_s: float = Field(description="capacity_kg_s output")
    transfer_reference_installation: float = Field(description="transfer_reference_installation output")
    plant_capacity_kg_s: float = Field(description="plant_capacity_kg_s output")
    distiller_reference_capital: float = Field(description="distiller_reference_capital output")
    installation_total: float = Field(description="installation_total output")
    defined_flag: float = Field(description="defined_flag output")
    flow_ratio: float = Field(description="flow_ratio output")
    cleanup_installation: float = Field(description="cleanup_installation output")
    equipment_total: float = Field(description="equipment_total output")
    flow_kg_s: float = Field(description="flow_kg_s output")
    module_total: float = Field(description="module_total output")
    distiller_reference_installation: float = Field(description="distiller_reference_installation output")
    transfer_reference_capital: float = Field(description="transfer_reference_capital output")
    transfer_installation: float = Field(description="transfer_installation output")
    containment_reference_capital: float = Field(description="containment_reference_capital output")
