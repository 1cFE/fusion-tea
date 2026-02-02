from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from chain_spike.modules.chainspikelibrary.areacalc import AreaCalcModule
from chain_spike.modules.chainspikelibrary.costcalc import CostCalcModule
from chain_spike.modules.chainspikelibrary.summarycalc import SummaryCalcModule

from chain_spike.schemas.design_params import DesignParams as DesignParams

from chain_spike.primitives import Float


def create_chain_spike_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            AreaCalcModule,            CostCalcModule,            SummaryCalcModule,        ],
        module_type_override={            AreaCalcModule: "chainspikelibrary.AreaCalcModule",            CostCalcModule: "chainspikelibrary.CostCalcModule",            SummaryCalcModule: "chainspikelibrary.SummaryCalcModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    DesignParams,    Float,]
