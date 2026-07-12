from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from exp_toy_tea.modules.exp_toy.boschhalereactivity import BoschHaleReactivityModule
from exp_toy_tea.modules.exp_toy.expcontrol import ExpControlModule
from exp_toy_tea.modules.exp_toy.gaindoublings import GainDoublingsModule

from exp_toy_tea.schemas.exp_toy_params import ExpToyParams as ExpToyParams

from exp_toy_tea.primitives import Float


def create_exp_toy_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            BoschHaleReactivityModule,            ExpControlModule,            GainDoublingsModule,        ],
        module_type_override={            BoschHaleReactivityModule: "exp_toy.BoschHaleReactivityModule",            ExpControlModule: "exp_toy.ExpControlModule",            GainDoublingsModule: "exp_toy.GainDoublingsModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    ExpToyParams,    Float,]
