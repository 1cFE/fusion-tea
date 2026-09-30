from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from magnet_materials_tea.modules.magnet_conductor_alternatives.magnet_cold_stage_load import Magnet_Cold_Stage_LoadModule
from magnet_materials_tea.modules.magnet_conductor_alternatives.matched_pair_comparison import Matched_Pair_ComparisonModule
from magnet_materials_tea.modules.magnet_conductor_alternatives.nb3sn_cable_critical_surface import Nb3Sn_Cable_Critical_SurfaceModule
from magnet_materials_tea.modules.magnet_conductor_alternatives.rebco_cable_critical_surface import REBCO_Cable_Critical_SurfaceModule
from magnet_materials_tea.modules.magnet_conductor_alternatives.staged_refrigeration_screen import Staged_Refrigeration_ScreenModule
from magnet_materials_tea.modules.magnet_conductor_alternatives.subsystem_annualized_cost import Subsystem_Annualized_CostModule
from magnet_materials_tea.modules.magnet_conductor_alternatives.winding_inventory_and_cost import Winding_Inventory_and_CostModule
from magnet_materials_tea.modules.magnet_conductor_alternatives.winding_turn_area_screen import Winding_Turn_Area_ScreenModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.duty.turn_current import turn_currentModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.nb3sn.all_pass import all_passModule as Nb3sn_all_passModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.nb3sn.eps_min import eps_minModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.nb3sn.k_a import k_aModule as Nb3sn_k_aModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.nb3sn.k_d import k_dModule as Nb3sn_k_dModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.nb3sn.k_g import k_gModule as Nb3sn_k_gModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.nb3sn.k_i import k_iModule as Nb3sn_k_iModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.rebco.all_pass import all_passModule as Rebco_all_passModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.rebco.k_a import k_aModule as Rebco_k_aModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.rebco.k_d import k_dModule as Rebco_k_dModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.rebco.k_g import k_gModule as Rebco_k_gModule
from magnet_materials_tea.modules.magnet_subsystem.subsystem.rebco.k_i import k_iModule as Rebco_k_iModule
from magnet_materials_tea.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemnb3snacceptanceokconstraintmodule import SubsystemNb3snAcceptanceOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemnb3sncapacityokconstraintmodule import SubsystemNb3snCapacityOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemnb3sncopperokconstraintmodule import SubsystemNb3snCopperOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemnb3snfitokconstraintmodule import SubsystemNb3snFitOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemnb3snsteelokconstraintmodule import SubsystemNb3snSteelOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemrebcoacceptanceokconstraintmodule import SubsystemRebcoAcceptanceOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemrebcocapacityokconstraintmodule import SubsystemRebcoCapacityOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemrebcocopperokconstraintmodule import SubsystemRebcoCopperOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemrebcofitokconstraintmodule import SubsystemRebcoFitOkConstraintModule
from magnet_materials_tea.modules.magnet_subsystem.subsystemrebcosteelokconstraintmodule import SubsystemRebcoSteelOkConstraintModule

from magnet_materials_tea.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
from magnet_materials_tea.schemas.magnet_conductor_alternatives_params import MagnetConductorAlternativesParams as MagnetConductorAlternativesParams
from magnet_materials_tea.schemas.magnet_subsystem_params import MagnetSubsystemParams as MagnetSubsystemParams

from magnet_materials_tea.primitives import Float


def create_magnet_materials_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            ConstraintReportAggregatorModule,            Magnet_Cold_Stage_LoadModule,            Matched_Pair_ComparisonModule,            Nb3Sn_Cable_Critical_SurfaceModule,            REBCO_Cable_Critical_SurfaceModule,            Staged_Refrigeration_ScreenModule,            Subsystem_Annualized_CostModule,            Winding_Inventory_and_CostModule,            Winding_Turn_Area_ScreenModule,            SubsystemNb3snAcceptanceOkConstraintModule,            SubsystemNb3snCapacityOkConstraintModule,            SubsystemNb3snCopperOkConstraintModule,            SubsystemNb3snFitOkConstraintModule,            SubsystemNb3snSteelOkConstraintModule,            SubsystemRebcoAcceptanceOkConstraintModule,            SubsystemRebcoCapacityOkConstraintModule,            SubsystemRebcoCopperOkConstraintModule,            SubsystemRebcoFitOkConstraintModule,            SubsystemRebcoSteelOkConstraintModule,            turn_currentModule,            Nb3sn_all_passModule,            eps_minModule,            Nb3sn_k_aModule,            Nb3sn_k_dModule,            Nb3sn_k_gModule,            Nb3sn_k_iModule,            Rebco_all_passModule,            Rebco_k_aModule,            Rebco_k_dModule,            Rebco_k_gModule,            Rebco_k_iModule,        ],
        module_type_override={            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            Magnet_Cold_Stage_LoadModule: "magnet_conductor_alternatives.Magnet_Cold_Stage_LoadModule",            Matched_Pair_ComparisonModule: "magnet_conductor_alternatives.Matched_Pair_ComparisonModule",            Nb3Sn_Cable_Critical_SurfaceModule: "magnet_conductor_alternatives.Nb3Sn_Cable_Critical_SurfaceModule",            REBCO_Cable_Critical_SurfaceModule: "magnet_conductor_alternatives.REBCO_Cable_Critical_SurfaceModule",            Staged_Refrigeration_ScreenModule: "magnet_conductor_alternatives.Staged_Refrigeration_ScreenModule",            Subsystem_Annualized_CostModule: "magnet_conductor_alternatives.Subsystem_Annualized_CostModule",            Winding_Inventory_and_CostModule: "magnet_conductor_alternatives.Winding_Inventory_and_CostModule",            Winding_Turn_Area_ScreenModule: "magnet_conductor_alternatives.Winding_Turn_Area_ScreenModule",            SubsystemNb3snAcceptanceOkConstraintModule: "magnet_subsystem.SubsystemNb3snAcceptanceOkConstraintModule",            SubsystemNb3snCapacityOkConstraintModule: "magnet_subsystem.SubsystemNb3snCapacityOkConstraintModule",            SubsystemNb3snCopperOkConstraintModule: "magnet_subsystem.SubsystemNb3snCopperOkConstraintModule",            SubsystemNb3snFitOkConstraintModule: "magnet_subsystem.SubsystemNb3snFitOkConstraintModule",            SubsystemNb3snSteelOkConstraintModule: "magnet_subsystem.SubsystemNb3snSteelOkConstraintModule",            SubsystemRebcoAcceptanceOkConstraintModule: "magnet_subsystem.SubsystemRebcoAcceptanceOkConstraintModule",            SubsystemRebcoCapacityOkConstraintModule: "magnet_subsystem.SubsystemRebcoCapacityOkConstraintModule",            SubsystemRebcoCopperOkConstraintModule: "magnet_subsystem.SubsystemRebcoCopperOkConstraintModule",            SubsystemRebcoFitOkConstraintModule: "magnet_subsystem.SubsystemRebcoFitOkConstraintModule",            SubsystemRebcoSteelOkConstraintModule: "magnet_subsystem.SubsystemRebcoSteelOkConstraintModule",            turn_currentModule: "magnet_subsystem.subsystem.duty.turn_currentModule",            Nb3sn_all_passModule: "magnet_subsystem.subsystem.nb3sn.all_passModule",            eps_minModule: "magnet_subsystem.subsystem.nb3sn.eps_minModule",            Nb3sn_k_aModule: "magnet_subsystem.subsystem.nb3sn.k_aModule",            Nb3sn_k_dModule: "magnet_subsystem.subsystem.nb3sn.k_dModule",            Nb3sn_k_gModule: "magnet_subsystem.subsystem.nb3sn.k_gModule",            Nb3sn_k_iModule: "magnet_subsystem.subsystem.nb3sn.k_iModule",            Rebco_all_passModule: "magnet_subsystem.subsystem.rebco.all_passModule",            Rebco_k_aModule: "magnet_subsystem.subsystem.rebco.k_aModule",            Rebco_k_dModule: "magnet_subsystem.subsystem.rebco.k_dModule",            Rebco_k_gModule: "magnet_subsystem.subsystem.rebco.k_gModule",            Rebco_k_iModule: "magnet_subsystem.subsystem.rebco.k_iModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    MagnetConductorAlternativesParams,    MagnetSubsystemParams,    ConstraintEvaluation,    ConstraintReport,    Float,]
