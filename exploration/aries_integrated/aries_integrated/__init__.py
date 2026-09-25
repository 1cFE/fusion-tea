from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from aries_integrated.modules.dual_circuit_heat_accounting.coolant_branch_heat import Coolant_Branch_HeatModule
from aries_integrated.modules.ideal_gas_brayton_components.fixed_outlet_conditioning import Fixed_Outlet_ConditioningModule
from aries_integrated.modules.ideal_gas_brayton_components.fractional_pressure_loss import Fractional_Pressure_LossModule
from aries_integrated.modules.ideal_gas_brayton_components.ideal_gas_compressor import Ideal_Gas_CompressorModule
from aries_integrated.modules.ideal_gas_brayton_components.ideal_gas_expander import Ideal_Gas_ExpanderModule
from aries_integrated.modules.integrated_equipment_costs.annual_selected_fuel import Annual_Selected_FuelModule
from aries_integrated.modules.integrated_equipment_costs.comparison_difference import Comparison_DifferenceModule
from aries_integrated.modules.integrated_equipment_costs.eight_amount_sum import Eight_Amount_SumModule
from aries_integrated.modules.integrated_equipment_costs.equipment_cost_ledger import Equipment_Cost_LedgerModule
from aries_integrated.modules.integrated_equipment_costs.exchanger_area_conductance import Exchanger_Area_ConductanceModule
from aries_integrated.modules.integrated_equipment_costs.replacement_events import Replacement_EventsModule
from aries_integrated.modules.integrated_equipment_costs.scaled_amount import Scaled_AmountModule
from aries_integrated.modules.integrated_equipment_costs.selected_flow_pump import Selected_Flow_PumpModule
from aries_integrated.modules.integrated_equipment_costs.selected_inventory_purchase import Selected_Inventory_PurchaseModule
from aries_integrated.modules.integrated_equipment_costs.selected_stock_atoms import Selected_Stock_AtomsModule
from aries_integrated.modules.integrated_heat_electricity.fusion_source_selector import Fusion_Source_SelectorModule
from aries_integrated.modules.integrated_heat_electricity.integrated_heat_source import Integrated_Heat_SourceModule
from aries_integrated.modules.integrated_heat_electricity.integrated_plant_ledger import Integrated_Plant_LedgerModule
from aries_integrated.modules.integrated_heat_electricity.network_heat_driven_closure import Network_Heat_Driven_ClosureModule
from aries_integrated.modules.integrated_heat_electricity.passive_recuperator import Passive_RecuperatorModule
from aries_integrated.modules.integrated_heat_electricity.plant_electrical_balance import Plant_Electrical_BalanceModule
from aries_integrated.modules.integrated_lifecycle_costs.already_financed_duration import Already_Financed_DurationModule
from aries_integrated.modules.integrated_lifecycle_costs.lifecycle_cashflow_accounts import Lifecycle_Cashflow_AccountsModule
from aries_integrated.modules.integrated_lifecycle_costs.supplied_annual_energy import Supplied_Annual_EnergyModule
from aries_integrated.modules.mfe_account_costs.annual_om_cost import Annual_OM_CostModule
from aries_integrated.modules.mfe_account_costs.contingency_cost import Contingency_CostModule
from aries_integrated.modules.mfe_account_costs.dt_fuel_cost import DT_Fuel_CostModule
from aries_integrated.modules.mfe_account_costs.indirect_cost import Indirect_CostModule
from aries_integrated.modules.mfe_account_costs.levelized_annual_cost import Levelized_Annual_CostModule
from aries_integrated.modules.mfe_account_costs.supplied_purchase_cost import Supplied_Purchase_CostModule
from aries_integrated.modules.mfe_fuel_cycle.fuel_cycle_flows import Fuel_Cycle_FlowsModule
from aries_integrated.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFModule
from aries_integrated.modules.mfe_plasma_scaling.volume_averaged_beta import Volume_Averaged_BetaModule
from aries_integrated.modules.mfe_viability.offered_capacity_screen import Offered_Capacity_ScreenModule
from aries_integrated.modules.radial_density_profile.radial_density_profile import Radial_Density_ProfileModule
from aries_integrated.modules.source_budget_accounting.disjoint_capital_budget import Disjoint_Capital_BudgetModule
from aries_integrated.modules.supplied_profile_plasma.supplied_profile_plasma import Supplied_Profile_PlasmaModule
from aries_integrated.modules.aries_cs_plasma_integration.plasma.edge_density import edge_densityModule
from aries_integrated.modules.aries_integrated_plant.compressorcapacitycapacityokconstraintmodule import CompressorCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.divertorcapacitycapacityokconstraintmodule import DivertorCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.divertorpumpcapacityokconstraintmodule import DivertorPumpCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.fuelcapacitycapacityokconstraintmodule import FuelCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.fuelinventorycapacityokconstraintmodule import FuelInventoryCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.generatorcapacitycapacityokconstraintmodule import GeneratorCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.hecapacitycapacityokconstraintmodule import HeCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.hepumpcapacityokconstraintmodule import HePumpCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.pblicapacitycapacityokconstraintmodule import PbliCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.pblipumpcapacityokconstraintmodule import PbliPumpCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.plantledgerbalancesokconstraintmodule import PlantLedgerBalancesOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.plantledgerheatremovalokconstraintmodule import PlantLedgerHeatRemovalOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.rejectioncapacitycapacityokconstraintmodule import RejectionCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.turbinecapacitycapacityokconstraintmodule import TurbineCapacityCapacityOkConstraintModule
from aries_integrated.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule

from aries_integrated.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
from aries_integrated.schemas.integrated_equipment_costs_params import IntegratedEquipmentCostsParams as IntegratedEquipmentCostsParams
from aries_integrated.schemas.mfe_account_costs_params import MfeAccountCostsParams as MfeAccountCostsParams
from aries_integrated.schemas.mfe_plasma_scaling_params import MfePlasmaScalingParams as MfePlasmaScalingParams
from aries_integrated.schemas.mfe_viability_params import MfeViabilityParams as MfeViabilityParams
from aries_integrated.schemas.plant_params import PlantParams as PlantParams
from aries_integrated.schemas.plasma_integration_params import PlasmaIntegrationParams as PlasmaIntegrationParams

from aries_integrated.primitives import Float


def create_aries_integrated_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            edge_densityModule,            CompressorCapacityCapacityOkConstraintModule,            DivertorCapacityCapacityOkConstraintModule,            DivertorPumpCapacityOkConstraintModule,            FuelCapacityCapacityOkConstraintModule,            FuelInventoryCapacityOkConstraintModule,            GeneratorCapacityCapacityOkConstraintModule,            HeCapacityCapacityOkConstraintModule,            HePumpCapacityOkConstraintModule,            PbliCapacityCapacityOkConstraintModule,            PbliPumpCapacityOkConstraintModule,            PlantLedgerBalancesOkConstraintModule,            PlantLedgerHeatRemovalOkConstraintModule,            RejectionCapacityCapacityOkConstraintModule,            TurbineCapacityCapacityOkConstraintModule,            ConstraintReportAggregatorModule,            Coolant_Branch_HeatModule,            Fixed_Outlet_ConditioningModule,            Fractional_Pressure_LossModule,            Ideal_Gas_CompressorModule,            Ideal_Gas_ExpanderModule,            Annual_Selected_FuelModule,            Comparison_DifferenceModule,            Eight_Amount_SumModule,            Equipment_Cost_LedgerModule,            Exchanger_Area_ConductanceModule,            Replacement_EventsModule,            Scaled_AmountModule,            Selected_Flow_PumpModule,            Selected_Inventory_PurchaseModule,            Selected_Stock_AtomsModule,            Fusion_Source_SelectorModule,            Integrated_Heat_SourceModule,            Integrated_Plant_LedgerModule,            Network_Heat_Driven_ClosureModule,            Passive_RecuperatorModule,            Plant_Electrical_BalanceModule,            Already_Financed_DurationModule,            Lifecycle_Cashflow_AccountsModule,            Supplied_Annual_EnergyModule,            Annual_OM_CostModule,            Contingency_CostModule,            DT_Fuel_CostModule,            Indirect_CostModule,            Levelized_Annual_CostModule,            Supplied_Purchase_CostModule,            Fuel_Cycle_FlowsModule,            LCOE_DCFModule,            Volume_Averaged_BetaModule,            Offered_Capacity_ScreenModule,            Radial_Density_ProfileModule,            Disjoint_Capital_BudgetModule,            Supplied_Profile_PlasmaModule,        ],
        module_type_override={            edge_densityModule: "aries_cs_plasma_integration.plasma.edge_densityModule",            CompressorCapacityCapacityOkConstraintModule: "aries_integrated_plant.CompressorCapacityCapacityOkConstraintModule",            DivertorCapacityCapacityOkConstraintModule: "aries_integrated_plant.DivertorCapacityCapacityOkConstraintModule",            DivertorPumpCapacityOkConstraintModule: "aries_integrated_plant.DivertorPumpCapacityOkConstraintModule",            FuelCapacityCapacityOkConstraintModule: "aries_integrated_plant.FuelCapacityCapacityOkConstraintModule",            FuelInventoryCapacityOkConstraintModule: "aries_integrated_plant.FuelInventoryCapacityOkConstraintModule",            GeneratorCapacityCapacityOkConstraintModule: "aries_integrated_plant.GeneratorCapacityCapacityOkConstraintModule",            HeCapacityCapacityOkConstraintModule: "aries_integrated_plant.HeCapacityCapacityOkConstraintModule",            HePumpCapacityOkConstraintModule: "aries_integrated_plant.HePumpCapacityOkConstraintModule",            PbliCapacityCapacityOkConstraintModule: "aries_integrated_plant.PbliCapacityCapacityOkConstraintModule",            PbliPumpCapacityOkConstraintModule: "aries_integrated_plant.PbliPumpCapacityOkConstraintModule",            PlantLedgerBalancesOkConstraintModule: "aries_integrated_plant.PlantLedgerBalancesOkConstraintModule",            PlantLedgerHeatRemovalOkConstraintModule: "aries_integrated_plant.PlantLedgerHeatRemovalOkConstraintModule",            RejectionCapacityCapacityOkConstraintModule: "aries_integrated_plant.RejectionCapacityCapacityOkConstraintModule",            TurbineCapacityCapacityOkConstraintModule: "aries_integrated_plant.TurbineCapacityCapacityOkConstraintModule",            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            Coolant_Branch_HeatModule: "dual_circuit_heat_accounting.Coolant_Branch_HeatModule",            Fixed_Outlet_ConditioningModule: "ideal_gas_brayton_components.Fixed_Outlet_ConditioningModule",            Fractional_Pressure_LossModule: "ideal_gas_brayton_components.Fractional_Pressure_LossModule",            Ideal_Gas_CompressorModule: "ideal_gas_brayton_components.Ideal_Gas_CompressorModule",            Ideal_Gas_ExpanderModule: "ideal_gas_brayton_components.Ideal_Gas_ExpanderModule",            Annual_Selected_FuelModule: "integrated_equipment_costs.Annual_Selected_FuelModule",            Comparison_DifferenceModule: "integrated_equipment_costs.Comparison_DifferenceModule",            Eight_Amount_SumModule: "integrated_equipment_costs.Eight_Amount_SumModule",            Equipment_Cost_LedgerModule: "integrated_equipment_costs.Equipment_Cost_LedgerModule",            Exchanger_Area_ConductanceModule: "integrated_equipment_costs.Exchanger_Area_ConductanceModule",            Replacement_EventsModule: "integrated_equipment_costs.Replacement_EventsModule",            Scaled_AmountModule: "integrated_equipment_costs.Scaled_AmountModule",            Selected_Flow_PumpModule: "integrated_equipment_costs.Selected_Flow_PumpModule",            Selected_Inventory_PurchaseModule: "integrated_equipment_costs.Selected_Inventory_PurchaseModule",            Selected_Stock_AtomsModule: "integrated_equipment_costs.Selected_Stock_AtomsModule",            Fusion_Source_SelectorModule: "integrated_heat_electricity.Fusion_Source_SelectorModule",            Integrated_Heat_SourceModule: "integrated_heat_electricity.Integrated_Heat_SourceModule",            Integrated_Plant_LedgerModule: "integrated_heat_electricity.Integrated_Plant_LedgerModule",            Network_Heat_Driven_ClosureModule: "integrated_heat_electricity.Network_Heat_Driven_ClosureModule",            Passive_RecuperatorModule: "integrated_heat_electricity.Passive_RecuperatorModule",            Plant_Electrical_BalanceModule: "integrated_heat_electricity.Plant_Electrical_BalanceModule",            Already_Financed_DurationModule: "integrated_lifecycle_costs.Already_Financed_DurationModule",            Lifecycle_Cashflow_AccountsModule: "integrated_lifecycle_costs.Lifecycle_Cashflow_AccountsModule",            Supplied_Annual_EnergyModule: "integrated_lifecycle_costs.Supplied_Annual_EnergyModule",            Annual_OM_CostModule: "mfe_account_costs.Annual_OM_CostModule",            Contingency_CostModule: "mfe_account_costs.Contingency_CostModule",            DT_Fuel_CostModule: "mfe_account_costs.DT_Fuel_CostModule",            Indirect_CostModule: "mfe_account_costs.Indirect_CostModule",            Levelized_Annual_CostModule: "mfe_account_costs.Levelized_Annual_CostModule",            Supplied_Purchase_CostModule: "mfe_account_costs.Supplied_Purchase_CostModule",            Fuel_Cycle_FlowsModule: "mfe_fuel_cycle.Fuel_Cycle_FlowsModule",            LCOE_DCFModule: "mfe_lcoe_dcf.LCOE_DCFModule",            Volume_Averaged_BetaModule: "mfe_plasma_scaling.Volume_Averaged_BetaModule",            Offered_Capacity_ScreenModule: "mfe_viability.Offered_Capacity_ScreenModule",            Radial_Density_ProfileModule: "radial_density_profile.Radial_Density_ProfileModule",            Disjoint_Capital_BudgetModule: "source_budget_accounting.Disjoint_Capital_BudgetModule",            Supplied_Profile_PlasmaModule: "supplied_profile_plasma.Supplied_Profile_PlasmaModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    IntegratedEquipmentCostsParams,    MfeAccountCostsParams,    MfePlasmaScalingParams,    MfeViabilityParams,    PlantParams,    PlasmaIntegrationParams,    ConstraintEvaluation,    ConstraintReport,    Float,]
