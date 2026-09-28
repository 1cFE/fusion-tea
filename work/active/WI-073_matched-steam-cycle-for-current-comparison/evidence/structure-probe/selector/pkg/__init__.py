from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from probe_selector.modules.probe.legacy import LegacyModule
from probe_selector.modules.probe.match import MatchModule
from probe_selector.modules.probe.sink import SinkModule
from probe_selector.modules.probe.turbine.property_value import property_valueModule

from probe_selector.schemas.probe_params import ProbeParams as ProbeParams

from probe_selector.primitives import Float


def create_probe_selector_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            LegacyModule,            MatchModule,            SinkModule,            property_valueModule,        ],
        module_type_override={            LegacyModule: "probe.LegacyModule",            MatchModule: "probe.MatchModule",            SinkModule: "probe.SinkModule",            property_valueModule: "probe.turbine.property_valueModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    ProbeParams,    Float,]
