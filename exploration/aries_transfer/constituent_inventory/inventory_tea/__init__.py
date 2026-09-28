from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from inventory_tea.modules.sector_constituent_inventory.constituent_inventory import Constituent_InventoryModule
from inventory_tea.modules.sector_constituent_inventory.covered_layer_volume import Covered_Layer_VolumeModule
from inventory_tea.modules.sector_constituent_inventory.three_constituent_recipe_summary import Three_Constituent_Recipe_SummaryModule
from inventory_tea.modules.sector_constituent_inventory.three_sector_inventory_sum import Three_Sector_Inventory_SumModule

from inventory_tea.schemas.constituent_inventory_params import ConstituentInventoryParams as ConstituentInventoryParams

from inventory_tea.primitives import Float


def create_inventory_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            Constituent_InventoryModule,            Covered_Layer_VolumeModule,            Three_Constituent_Recipe_SummaryModule,            Three_Sector_Inventory_SumModule,        ],
        module_type_override={            Constituent_InventoryModule: "sector_constituent_inventory.Constituent_InventoryModule",            Covered_Layer_VolumeModule: "sector_constituent_inventory.Covered_Layer_VolumeModule",            Three_Constituent_Recipe_SummaryModule: "sector_constituent_inventory.Three_Constituent_Recipe_SummaryModule",            Three_Sector_Inventory_SumModule: "sector_constituent_inventory.Three_Sector_Inventory_SumModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    ConstituentInventoryParams,    Float,]
