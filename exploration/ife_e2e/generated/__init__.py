from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from ife_tea.modules.fusion_cycle.recirculating_power_fraction import Recirculating_Power_FractionModule
from ife_tea.modules.hif_economics.meier_coe import Meier_COEModule
from ife_tea.modules.hif_economics.meier_hif_driver_cost import Meier_HIF_Driver_CostModule
from ife_tea.modules.hif_economics.meier_reactor_cost import Meier_Reactor_CostModule
from ife_tea.modules.hif_economics.meier_total_capital_cost import Meier_Total_Capital_CostModule
from ife_tea.modules.ife_lcoe.ife_lcoe import IFE_LCOEModule
from ife_tea.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule
from ife_tea.modules.hif_plant_pkg.hifplantviabilityconstraintmodule import HifPlantViabilityConstraintModule

from ife_tea.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
from ife_tea.schemas.hif_plant_params import HifPlantParams as HifPlantParams
from ife_tea.schemas.ife_plant_params import IfePlantParams as IfePlantParams
from ife_tea.schemas.system_design import SystemDesign as SystemDesign

from ife_tea.primitives import Float


def create_ife_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            ConstraintReportAggregatorModule,            Recirculating_Power_FractionModule,            Meier_COEModule,            Meier_HIF_Driver_CostModule,            Meier_Reactor_CostModule,            Meier_Total_Capital_CostModule,            HifPlantViabilityConstraintModule,            IFE_LCOEModule,        ],
        module_type_override={            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            Recirculating_Power_FractionModule: "fusion_cycle.Recirculating_Power_FractionModule",            Meier_COEModule: "hif_economics.Meier_COEModule",            Meier_HIF_Driver_CostModule: "hif_economics.Meier_HIF_Driver_CostModule",            Meier_Reactor_CostModule: "hif_economics.Meier_Reactor_CostModule",            Meier_Total_Capital_CostModule: "hif_economics.Meier_Total_Capital_CostModule",            HifPlantViabilityConstraintModule: "hif_plant_pkg.HifPlantViabilityConstraintModule",            IFE_LCOEModule: "ife_lcoe.IFE_LCOEModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    HifPlantParams,    IfePlantParams,    SystemDesign,    ConstraintEvaluation,    ConstraintReport,    Float,]
