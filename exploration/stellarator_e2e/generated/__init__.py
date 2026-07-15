from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from stellarator_tea.modules.mfe_account_costs.blanket_cost import Blanket_CostModule
from stellarator_tea.modules.mfe_account_costs.contingency_cost import Contingency_CostModule
from stellarator_tea.modules.mfe_account_costs.divertor_cost import Divertor_CostModule
from stellarator_tea.modules.mfe_account_costs.heating_cost import Heating_CostModule
from stellarator_tea.modules.mfe_account_costs.indirect_cost import Indirect_CostModule
from stellarator_tea.modules.mfe_account_costs.linear_power_cost import Linear_Power_CostModule
from stellarator_tea.modules.mfe_account_costs.power_supplies_cost import Power_Supplies_CostModule
from stellarator_tea.modules.mfe_account_costs.shield_cost import Shield_CostModule
from stellarator_tea.modules.mfe_account_costs.structure_cost import Structure_CostModule
from stellarator_tea.modules.mfe_account_costs.vessel_cost import Vessel_CostModule
from stellarator_tea.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFModule
from stellarator_tea.modules.mfe_magnet_cost.magnet_coil_cost import Magnet_Coil_CostModule
from stellarator_tea.modules.mfe_plasma_scaling.dt_fusion_power import DT_Fusion_PowerModule
from stellarator_tea.modules.mfe_plasma_scaling.neutron_wall_load import Neutron_Wall_LoadModule
from stellarator_tea.modules.mfe_plasma_scaling.plasma_geometry import Plasma_GeometryModule
from stellarator_tea.modules.mfe_power_balance.mfe_power_balance_calc import MFE_Power_Balance_CalcModule

from stellarator_tea.schemas.mfe_plant_params import MfePlantParams as MfePlantParams
from stellarator_tea.schemas.stellarator_plant_params import StellaratorPlantParams as StellaratorPlantParams
from stellarator_tea.schemas.system_design import SystemDesign as SystemDesign

from stellarator_tea.primitives import Float


def create_stellarator_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            Blanket_CostModule,            Contingency_CostModule,            Divertor_CostModule,            Heating_CostModule,            Indirect_CostModule,            Linear_Power_CostModule,            Power_Supplies_CostModule,            Shield_CostModule,            Structure_CostModule,            Vessel_CostModule,            LCOE_DCFModule,            Magnet_Coil_CostModule,            DT_Fusion_PowerModule,            Neutron_Wall_LoadModule,            Plasma_GeometryModule,            MFE_Power_Balance_CalcModule,        ],
        module_type_override={            Blanket_CostModule: "mfe_account_costs.Blanket_CostModule",            Contingency_CostModule: "mfe_account_costs.Contingency_CostModule",            Divertor_CostModule: "mfe_account_costs.Divertor_CostModule",            Heating_CostModule: "mfe_account_costs.Heating_CostModule",            Indirect_CostModule: "mfe_account_costs.Indirect_CostModule",            Linear_Power_CostModule: "mfe_account_costs.Linear_Power_CostModule",            Power_Supplies_CostModule: "mfe_account_costs.Power_Supplies_CostModule",            Shield_CostModule: "mfe_account_costs.Shield_CostModule",            Structure_CostModule: "mfe_account_costs.Structure_CostModule",            Vessel_CostModule: "mfe_account_costs.Vessel_CostModule",            LCOE_DCFModule: "mfe_lcoe_dcf.LCOE_DCFModule",            Magnet_Coil_CostModule: "mfe_magnet_cost.Magnet_Coil_CostModule",            DT_Fusion_PowerModule: "mfe_plasma_scaling.DT_Fusion_PowerModule",            Neutron_Wall_LoadModule: "mfe_plasma_scaling.Neutron_Wall_LoadModule",            Plasma_GeometryModule: "mfe_plasma_scaling.Plasma_GeometryModule",            MFE_Power_Balance_CalcModule: "mfe_power_balance.MFE_Power_Balance_CalcModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    MfePlantParams,    StellaratorPlantParams,    SystemDesign,    Float,]
