from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from e2e_attr_expr_v5.modules.e2eattrexprlibrary.annualizedcostcalc import AnnualizedCostCalcModule
from e2e_attr_expr_v5.modules.e2eattrexprlibrary.componentcostcalc import ComponentCostCalcModule
from e2e_attr_expr_v5.modules.e2eattrexprlibrary.energycalc import EnergyCalcModule
from e2e_attr_expr_v5.modules.e2eattrexprlibrary.simplelcoecalc import SimpleLCOECalcModule
from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.annual_om import annual_omModule
from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.area import areaModule
from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.power_kw import power_kwModule
from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.power_mw import power_mwModule
from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.surface_cost import surface_costModule
from e2e_attr_expr_v5.modules.e2eattrexprdesign.e2e_plant.volume import volumeModule

from e2e_attr_expr_v5.schemas.design_params import DesignParams as DesignParams

from e2e_attr_expr_v5.primitives import Float


def create_e2e_attr_expr_v5_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            annual_omModule,            areaModule,            power_kwModule,            power_mwModule,            surface_costModule,            volumeModule,            AnnualizedCostCalcModule,            ComponentCostCalcModule,            EnergyCalcModule,            SimpleLCOECalcModule,        ],
        module_type_override={            annual_omModule: "e2eattrexprdesign.e2e_plant.annual_omModule",            areaModule: "e2eattrexprdesign.e2e_plant.areaModule",            power_kwModule: "e2eattrexprdesign.e2e_plant.power_kwModule",            power_mwModule: "e2eattrexprdesign.e2e_plant.power_mwModule",            surface_costModule: "e2eattrexprdesign.e2e_plant.surface_costModule",            volumeModule: "e2eattrexprdesign.e2e_plant.volumeModule",            AnnualizedCostCalcModule: "e2eattrexprlibrary.AnnualizedCostCalcModule",            ComponentCostCalcModule: "e2eattrexprlibrary.ComponentCostCalcModule",            EnergyCalcModule: "e2eattrexprlibrary.EnergyCalcModule",            SimpleLCOECalcModule: "e2eattrexprlibrary.SimpleLCOECalcModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    DesignParams,    Float,]
