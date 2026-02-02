from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from solar_battery.modules.solarbatterylibrary.allocationcostcalc import AllocationCostCalcModule
from solar_battery.modules.solarbatterylibrary.annualizedfinancialcalc import AnnualizedFinancialCalcModule
from solar_battery.modules.solarbatterylibrary.annualizedfuelcalc import AnnualizedFuelCalcModule
from solar_battery.modules.solarbatterylibrary.annualizedomcalc import AnnualizedOMCalcModule
from solar_battery.modules.solarbatterylibrary.arrayboscostcalc import ArrayBOSCostCalcModule
from solar_battery.modules.solarbatterylibrary.batteryboscostcalc import BatteryBOSCostCalcModule
from solar_battery.modules.solarbatterylibrary.batterypackcostcalc import BatteryPackCostCalcModule
from solar_battery.modules.solarbatterylibrary.electricalpanelcostcalc import ElectricalPanelCostCalcModule
from solar_battery.modules.solarbatterylibrary.energyproductioncalc import EnergyProductionCalcModule
from solar_battery.modules.solarbatterylibrary.hybridinvertercostcalc import HybridInverterCostCalcModule
from solar_battery.modules.solarbatterylibrary.invertercostcalc import InverterCostCalcModule
from solar_battery.modules.solarbatterylibrary.lcoecalc import LCOECalcModule
from solar_battery.modules.solarbatterylibrary.permittingcostcalc import PermittingCostCalcModule
from solar_battery.modules.solarbatterylibrary.pvmodulecostcalc import PVModuleCostCalcModule
from solar_battery.modules.solarbatterylibrary.rackingcostcalc import RackingCostCalcModule

# Hand-written module
from solar_battery.modules.component_cost_evaluator import (
    ComponentCostEvaluator,
    CostEvaluatorResult,
)

from solar_battery.schemas.design_params import DesignParams as DesignParams
from solar_battery.schemas.library_params import LibraryParams as LibraryParams
from solar_battery.schemas.pipeline_config import PipelineConfig

from solar_battery.primitives import Float


def create_solar_battery_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Includes both codegen-generated modules and the hand-written
    ComponentCostEvaluator module for the hybrid pipeline.
    """
    return create_registry(
        [
            ComponentCostEvaluator,
            PVModuleCostCalcModule,
            InverterCostCalcModule,
            ArrayBOSCostCalcModule,
            BatteryPackCostCalcModule,
            HybridInverterCostCalcModule,
            BatteryBOSCostCalcModule,
            RackingCostCalcModule,
            ElectricalPanelCostCalcModule,
            PermittingCostCalcModule,
            AllocationCostCalcModule,
            EnergyProductionCalcModule,
            AnnualizedOMCalcModule,
            AnnualizedFuelCalcModule,
            AnnualizedFinancialCalcModule,
            LCOECalcModule,
        ],
        module_type_override={
            ComponentCostEvaluator: "ComponentCostEvaluator",
            PVModuleCostCalcModule: "solarbatterylibrary.PVModuleCostCalcModule",
            InverterCostCalcModule: "solarbatterylibrary.InverterCostCalcModule",
            ArrayBOSCostCalcModule: "solarbatterylibrary.ArrayBOSCostCalcModule",
            BatteryPackCostCalcModule: "solarbatterylibrary.BatteryPackCostCalcModule",
            HybridInverterCostCalcModule: "solarbatterylibrary.HybridInverterCostCalcModule",
            BatteryBOSCostCalcModule: "solarbatterylibrary.BatteryBOSCostCalcModule",
            RackingCostCalcModule: "solarbatterylibrary.RackingCostCalcModule",
            ElectricalPanelCostCalcModule: "solarbatterylibrary.ElectricalPanelCostCalcModule",
            PermittingCostCalcModule: "solarbatterylibrary.PermittingCostCalcModule",
            AllocationCostCalcModule: "solarbatterylibrary.AllocationCostCalcModule",
            EnergyProductionCalcModule: "solarbatterylibrary.EnergyProductionCalcModule",
            AnnualizedOMCalcModule: "solarbatterylibrary.AnnualizedOMCalcModule",
            AnnualizedFuelCalcModule: "solarbatterylibrary.AnnualizedFuelCalcModule",
            AnnualizedFinancialCalcModule: "solarbatterylibrary.AnnualizedFinancialCalcModule",
            LCOECalcModule: "solarbatterylibrary.LCOECalcModule",
        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [
    LibraryParams,
    DesignParams,
    PipelineConfig,
    CostEvaluatorResult,
    Float,
]
