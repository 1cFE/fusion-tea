from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from costed_loop_brayton_tea.modules.ideal_gas_brayton_components.fixed_outlet_conditioning import Fixed_Outlet_ConditioningModule
from costed_loop_brayton_tea.modules.ideal_gas_brayton_components.fractional_pressure_loss import Fractional_Pressure_LossModule
from costed_loop_brayton_tea.modules.ideal_gas_brayton_components.ideal_gas_compressor import Ideal_Gas_CompressorModule
from costed_loop_brayton_tea.modules.ideal_gas_brayton_components.ideal_gas_expander import Ideal_Gas_ExpanderModule
from costed_loop_brayton_tea.modules.integrated_equipment_costs.annual_selected_fuel import Annual_Selected_FuelModule
from costed_loop_brayton_tea.modules.integrated_equipment_costs.eight_amount_sum import Eight_Amount_SumModule
from costed_loop_brayton_tea.modules.integrated_equipment_costs.equipment_cost_ledger import Equipment_Cost_LedgerModule
from costed_loop_brayton_tea.modules.integrated_equipment_costs.exchanger_area_conductance import Exchanger_Area_ConductanceModule
from costed_loop_brayton_tea.modules.integrated_equipment_costs.replacement_events import Replacement_EventsModule
from costed_loop_brayton_tea.modules.integrated_equipment_costs.scaled_amount import Scaled_AmountModule
from costed_loop_brayton_tea.modules.integrated_equipment_costs.selected_inventory_purchase import Selected_Inventory_PurchaseModule
from costed_loop_brayton_tea.modules.integrated_equipment_costs.selected_stock_atoms import Selected_Stock_AtomsModule
from costed_loop_brayton_tea.modules.integrated_heat_electricity.network_heat_driven_closure import Network_Heat_Driven_ClosureModule
from costed_loop_brayton_tea.modules.integrated_heat_electricity.passive_recuperator import Passive_RecuperatorModule
from costed_loop_brayton_tea.modules.integrated_heat_electricity.plant_electrical_balance import Plant_Electrical_BalanceModule
from costed_loop_brayton_tea.modules.integrated_lifecycle_costs.lifecycle_cashflow_accounts import Lifecycle_Cashflow_AccountsModule
from costed_loop_brayton_tea.modules.mfe_account_costs.annual_om_cost import Annual_OM_CostModule
from costed_loop_brayton_tea.modules.mfe_account_costs.contingency_cost import Contingency_CostModule
from costed_loop_brayton_tea.modules.mfe_account_costs.dt_fuel_cost import DT_Fuel_CostModule
from costed_loop_brayton_tea.modules.mfe_account_costs.indirect_cost import Indirect_CostModule
from costed_loop_brayton_tea.modules.mfe_account_costs.levelized_annual_cost import Levelized_Annual_CostModule
from costed_loop_brayton_tea.modules.mfe_account_costs.supplied_purchase_cost import Supplied_Purchase_CostModule
from costed_loop_brayton_tea.modules.mfe_fuel_cycle.fuel_cycle_flows import Fuel_Cycle_FlowsModule
from costed_loop_brayton_tea.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFModule
from costed_loop_brayton_tea.modules.mfe_primary_loop.primary_coolant_loop import Primary_Coolant_LoopModule
from costed_loop_brayton_tea.modules.mfe_viability.offered_capacity_screen import Offered_Capacity_ScreenModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plant.rejection_capacity.rejected_heat import rejected_heatModule
from costed_loop_brayton_tea.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plantchecksheatremovalokconstraintmodule import PlantChecksHeatRemovalOkConstraintModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plantchecksloopcapacityokconstraintmodule import PlantChecksLoopCapacityOkConstraintModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plantchecksnetpositiveconstraintmodule import PlantChecksNetPositiveConstraintModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plantcompressorcapacitycapacityokconstraintmodule import PlantCompressorCapacityCapacityOkConstraintModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plantfuelinventorycapacityokconstraintmodule import PlantFuelInventoryCapacityOkConstraintModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plantgeneratorcapacitycapacityokconstraintmodule import PlantGeneratorCapacityCapacityOkConstraintModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.planthecapacitycapacityokconstraintmodule import PlantHeCapacityCapacityOkConstraintModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plantrejectioncapacitycapacityokconstraintmodule import PlantRejectionCapacityCapacityOkConstraintModule
from costed_loop_brayton_tea.modules.costed_loop_brayton.plantturbinecapacitycapacityokconstraintmodule import PlantTurbineCapacityCapacityOkConstraintModule

from costed_loop_brayton_tea.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
from costed_loop_brayton_tea.schemas.costed_loop_brayton_params import CostedLoopBraytonParams as CostedLoopBraytonParams
from costed_loop_brayton_tea.schemas.integrated_equipment_costs_params import IntegratedEquipmentCostsParams as IntegratedEquipmentCostsParams
from costed_loop_brayton_tea.schemas.mfe_account_costs_params import MfeAccountCostsParams as MfeAccountCostsParams
from costed_loop_brayton_tea.schemas.mfe_viability_params import MfeViabilityParams as MfeViabilityParams

from costed_loop_brayton_tea.primitives import Float


def create_costed_loop_brayton_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            ConstraintReportAggregatorModule,            PlantChecksHeatRemovalOkConstraintModule,            PlantChecksLoopCapacityOkConstraintModule,            PlantChecksNetPositiveConstraintModule,            PlantCompressorCapacityCapacityOkConstraintModule,            PlantFuelInventoryCapacityOkConstraintModule,            PlantGeneratorCapacityCapacityOkConstraintModule,            PlantHeCapacityCapacityOkConstraintModule,            PlantRejectionCapacityCapacityOkConstraintModule,            PlantTurbineCapacityCapacityOkConstraintModule,            rejected_heatModule,            Fixed_Outlet_ConditioningModule,            Fractional_Pressure_LossModule,            Ideal_Gas_CompressorModule,            Ideal_Gas_ExpanderModule,            Annual_Selected_FuelModule,            Eight_Amount_SumModule,            Equipment_Cost_LedgerModule,            Exchanger_Area_ConductanceModule,            Replacement_EventsModule,            Scaled_AmountModule,            Selected_Inventory_PurchaseModule,            Selected_Stock_AtomsModule,            Network_Heat_Driven_ClosureModule,            Passive_RecuperatorModule,            Plant_Electrical_BalanceModule,            Lifecycle_Cashflow_AccountsModule,            Annual_OM_CostModule,            Contingency_CostModule,            DT_Fuel_CostModule,            Indirect_CostModule,            Levelized_Annual_CostModule,            Supplied_Purchase_CostModule,            Fuel_Cycle_FlowsModule,            LCOE_DCFModule,            Primary_Coolant_LoopModule,            Offered_Capacity_ScreenModule,        ],
        module_type_override={            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            PlantChecksHeatRemovalOkConstraintModule: "costed_loop_brayton.PlantChecksHeatRemovalOkConstraintModule",            PlantChecksLoopCapacityOkConstraintModule: "costed_loop_brayton.PlantChecksLoopCapacityOkConstraintModule",            PlantChecksNetPositiveConstraintModule: "costed_loop_brayton.PlantChecksNetPositiveConstraintModule",            PlantCompressorCapacityCapacityOkConstraintModule: "costed_loop_brayton.PlantCompressorCapacityCapacityOkConstraintModule",            PlantFuelInventoryCapacityOkConstraintModule: "costed_loop_brayton.PlantFuelInventoryCapacityOkConstraintModule",            PlantGeneratorCapacityCapacityOkConstraintModule: "costed_loop_brayton.PlantGeneratorCapacityCapacityOkConstraintModule",            PlantHeCapacityCapacityOkConstraintModule: "costed_loop_brayton.PlantHeCapacityCapacityOkConstraintModule",            PlantRejectionCapacityCapacityOkConstraintModule: "costed_loop_brayton.PlantRejectionCapacityCapacityOkConstraintModule",            PlantTurbineCapacityCapacityOkConstraintModule: "costed_loop_brayton.PlantTurbineCapacityCapacityOkConstraintModule",            rejected_heatModule: "costed_loop_brayton.plant.rejection_capacity.rejected_heatModule",            Fixed_Outlet_ConditioningModule: "ideal_gas_brayton_components.Fixed_Outlet_ConditioningModule",            Fractional_Pressure_LossModule: "ideal_gas_brayton_components.Fractional_Pressure_LossModule",            Ideal_Gas_CompressorModule: "ideal_gas_brayton_components.Ideal_Gas_CompressorModule",            Ideal_Gas_ExpanderModule: "ideal_gas_brayton_components.Ideal_Gas_ExpanderModule",            Annual_Selected_FuelModule: "integrated_equipment_costs.Annual_Selected_FuelModule",            Eight_Amount_SumModule: "integrated_equipment_costs.Eight_Amount_SumModule",            Equipment_Cost_LedgerModule: "integrated_equipment_costs.Equipment_Cost_LedgerModule",            Exchanger_Area_ConductanceModule: "integrated_equipment_costs.Exchanger_Area_ConductanceModule",            Replacement_EventsModule: "integrated_equipment_costs.Replacement_EventsModule",            Scaled_AmountModule: "integrated_equipment_costs.Scaled_AmountModule",            Selected_Inventory_PurchaseModule: "integrated_equipment_costs.Selected_Inventory_PurchaseModule",            Selected_Stock_AtomsModule: "integrated_equipment_costs.Selected_Stock_AtomsModule",            Network_Heat_Driven_ClosureModule: "integrated_heat_electricity.Network_Heat_Driven_ClosureModule",            Passive_RecuperatorModule: "integrated_heat_electricity.Passive_RecuperatorModule",            Plant_Electrical_BalanceModule: "integrated_heat_electricity.Plant_Electrical_BalanceModule",            Lifecycle_Cashflow_AccountsModule: "integrated_lifecycle_costs.Lifecycle_Cashflow_AccountsModule",            Annual_OM_CostModule: "mfe_account_costs.Annual_OM_CostModule",            Contingency_CostModule: "mfe_account_costs.Contingency_CostModule",            DT_Fuel_CostModule: "mfe_account_costs.DT_Fuel_CostModule",            Indirect_CostModule: "mfe_account_costs.Indirect_CostModule",            Levelized_Annual_CostModule: "mfe_account_costs.Levelized_Annual_CostModule",            Supplied_Purchase_CostModule: "mfe_account_costs.Supplied_Purchase_CostModule",            Fuel_Cycle_FlowsModule: "mfe_fuel_cycle.Fuel_Cycle_FlowsModule",            LCOE_DCFModule: "mfe_lcoe_dcf.LCOE_DCFModule",            Primary_Coolant_LoopModule: "mfe_primary_loop.Primary_Coolant_LoopModule",            Offered_Capacity_ScreenModule: "mfe_viability.Offered_Capacity_ScreenModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    CostedLoopBraytonParams,    IntegratedEquipmentCostsParams,    MfeAccountCostsParams,    MfeViabilityParams,    ConstraintEvaluation,    ConstraintReport,    Float,]
