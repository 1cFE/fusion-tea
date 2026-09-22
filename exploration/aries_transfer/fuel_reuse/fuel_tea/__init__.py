from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from fuel_tea.modules.mfe_fuel_cycle.fuel_cycle_flows import Fuel_Cycle_FlowsModule
from fuel_tea.modules.mfe_viability.offered_capacity_screen import Offered_Capacity_ScreenModule
from fuel_tea.modules.aries_fuel_reuse.processingcapacityokconstraintmodule import ProcessingCapacityOkConstraintModule
from fuel_tea.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule

from fuel_tea.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
from fuel_tea.schemas.fuel_reuse_params import FuelReuseParams as FuelReuseParams
from fuel_tea.schemas.mfe_fuel_cycle_params import MfeFuelCycleParams as MfeFuelCycleParams



def create_fuel_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            ProcessingCapacityOkConstraintModule,            ConstraintReportAggregatorModule,            Fuel_Cycle_FlowsModule,            Offered_Capacity_ScreenModule,        ],
        module_type_override={            ProcessingCapacityOkConstraintModule: "aries_fuel_reuse.ProcessingCapacityOkConstraintModule",            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            Fuel_Cycle_FlowsModule: "mfe_fuel_cycle.Fuel_Cycle_FlowsModule",            Offered_Capacity_ScreenModule: "mfe_viability.Offered_Capacity_ScreenModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    FuelReuseParams,    MfeFuelCycleParams,    ConstraintEvaluation,    ConstraintReport,]
