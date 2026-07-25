from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from stellarator_tea.modules.mfe_account_costs.annual_cost_rollup import Annual_Cost_RollupModule
from stellarator_tea.modules.mfe_account_costs.annual_om_cost import Annual_OM_CostModule
from stellarator_tea.modules.mfe_account_costs.aux_cooling_cost import Aux_Cooling_CostModule
from stellarator_tea.modules.mfe_account_costs.blanket_cost import Blanket_CostModule
from stellarator_tea.modules.mfe_account_costs.buildings_cost import Buildings_CostModule
from stellarator_tea.modules.mfe_account_costs.contingency_cost import Contingency_CostModule
from stellarator_tea.modules.mfe_account_costs.coolant_cost import Coolant_CostModule
from stellarator_tea.modules.mfe_account_costs.divertor_cost import Divertor_CostModule
from stellarator_tea.modules.mfe_account_costs.dt_fuel_cost import DT_Fuel_CostModule
from stellarator_tea.modules.mfe_account_costs.heating_cost import Heating_CostModule
from stellarator_tea.modules.mfe_account_costs.idc_closed_form_cost import IDC_Closed_Form_CostModule
from stellarator_tea.modules.mfe_account_costs.indirect_cost import Indirect_CostModule
from stellarator_tea.modules.mfe_account_costs.installation_labor_cost import Installation_Labor_CostModule
from stellarator_tea.modules.mfe_account_costs.levelized_annual_cost import Levelized_Annual_CostModule
from stellarator_tea.modules.mfe_account_costs.levelized_replacement_cost import Levelized_Replacement_CostModule
from stellarator_tea.modules.mfe_account_costs.linear_power_cost import Linear_Power_CostModule
from stellarator_tea.modules.mfe_account_costs.n_1cfe_form_capital_charge import n_1cfe_Form_Capital_ChargeModule
from stellarator_tea.modules.mfe_account_costs.n_1cfe_form_lcoe import n_1cfe_Form_LCOEModule
from stellarator_tea.modules.mfe_account_costs.plant_power_law_cost import Plant_Power_Law_CostModule
from stellarator_tea.modules.mfe_account_costs.power_supplies_cost import Power_Supplies_CostModule
from stellarator_tea.modules.mfe_account_costs.preconstruction_cost import Preconstruction_CostModule
from stellarator_tea.modules.mfe_account_costs.remote_handling_cost import Remote_Handling_CostModule
from stellarator_tea.modules.mfe_account_costs.shield_cost import Shield_CostModule
from stellarator_tea.modules.mfe_account_costs.structure_cost import Structure_CostModule
from stellarator_tea.modules.mfe_account_costs.supplementary_cost import Supplementary_CostModule
from stellarator_tea.modules.mfe_account_costs.vessel_cost import Vessel_CostModule
from stellarator_tea.modules.mfe_cryo_plant.cryoplant_electrical_power import Cryoplant_Electrical_PowerModule
from stellarator_tea.modules.mfe_lcoe_dcf.lcoe_dcf import LCOE_DCFModule
from stellarator_tea.modules.mfe_magnet_cost.magnet_coil_cost import Magnet_Coil_CostModule
from stellarator_tea.modules.mfe_plasma_scaling.dt_fusion_power import DT_Fusion_PowerModule
from stellarator_tea.modules.mfe_plasma_scaling.mfe_radial_build import MFE_Radial_BuildModule
from stellarator_tea.modules.mfe_plasma_scaling.neutron_wall_load import Neutron_Wall_LoadModule
from stellarator_tea.modules.mfe_plasma_scaling.plasma_geometry import Plasma_GeometryModule
from stellarator_tea.modules.mfe_power_balance.mfe_power_balance_calc import MFE_Power_Balance_CalcModule
from stellarator_tea.modules.stellarator_09.stellaris.bop_capital import bop_capitalModule
from stellarator_tea.modules.stellarator_09.stellaris.cas20_capital import cas20_capitalModule
from stellarator_tea.modules.stellarator_09.stellaris.cas22_capital import cas22_capitalModule
from stellarator_tea.modules.stellarator_09.stellaris.cas23_to_28_capital import cas23_to_28_capitalModule
from stellarator_tea.modules.stellarator_09.stellaris.cas2x_pre_contingency import cas2x_pre_contingencyModule
from stellarator_tea.modules.stellarator_09.stellaris.overnight_capital import overnight_capitalModule
from stellarator_tea.modules.stellarator_09.stellaris.powercore_capital import powercore_capitalModule
from stellarator_tea.modules.stellarator_09.stellaris.reactor_equipment_subtotal import reactor_equipment_subtotalModule
from stellarator_tea.modules.stellarator_09.stellaris.replacement_cost_per_event import replacement_cost_per_eventModule
from stellarator_tea.modules.stellarator_09.stellaris.total_capital import total_capitalModule
from stellarator_tea.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule
from stellarator_tea.modules.stellarator_09.stellarisbetaokconstraintmodule import StellarisBetaOkConstraintModule
from stellarator_tea.modules.stellarator_09.stellarisnetpositiveconstraintmodule import StellarisNetPositiveConstraintModule
from stellarator_tea.modules.stellarator_09.stellarisrecircokconstraintmodule import StellarisRecircOkConstraintModule
from stellarator_tea.modules.stellarator_09.stellaristbrokconstraintmodule import StellarisTbrOkConstraintModule
from stellarator_tea.modules.stellarator_09.stellariswallloadokconstraintmodule import StellarisWallLoadOkConstraintModule

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
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
        [            ConstraintReportAggregatorModule,            Annual_Cost_RollupModule,            Annual_OM_CostModule,            Aux_Cooling_CostModule,            Blanket_CostModule,            Buildings_CostModule,            Contingency_CostModule,            Coolant_CostModule,            DT_Fuel_CostModule,            Divertor_CostModule,            Heating_CostModule,            IDC_Closed_Form_CostModule,            Indirect_CostModule,            Installation_Labor_CostModule,            Levelized_Annual_CostModule,            Levelized_Replacement_CostModule,            Linear_Power_CostModule,            Plant_Power_Law_CostModule,            Power_Supplies_CostModule,            Preconstruction_CostModule,            Remote_Handling_CostModule,            Shield_CostModule,            Structure_CostModule,            Supplementary_CostModule,            Vessel_CostModule,            n_1cfe_Form_Capital_ChargeModule,            n_1cfe_Form_LCOEModule,            Cryoplant_Electrical_PowerModule,            LCOE_DCFModule,            Magnet_Coil_CostModule,            DT_Fusion_PowerModule,            MFE_Radial_BuildModule,            Neutron_Wall_LoadModule,            Plasma_GeometryModule,            MFE_Power_Balance_CalcModule,            StellarisBetaOkConstraintModule,            StellarisNetPositiveConstraintModule,            StellarisRecircOkConstraintModule,            StellarisTbrOkConstraintModule,            StellarisWallLoadOkConstraintModule,            bop_capitalModule,            cas20_capitalModule,            cas22_capitalModule,            cas23_to_28_capitalModule,            cas2x_pre_contingencyModule,            overnight_capitalModule,            powercore_capitalModule,            reactor_equipment_subtotalModule,            replacement_cost_per_eventModule,            total_capitalModule,        ],
        module_type_override={            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            Annual_Cost_RollupModule: "mfe_account_costs.Annual_Cost_RollupModule",            Annual_OM_CostModule: "mfe_account_costs.Annual_OM_CostModule",            Aux_Cooling_CostModule: "mfe_account_costs.Aux_Cooling_CostModule",            Blanket_CostModule: "mfe_account_costs.Blanket_CostModule",            Buildings_CostModule: "mfe_account_costs.Buildings_CostModule",            Contingency_CostModule: "mfe_account_costs.Contingency_CostModule",            Coolant_CostModule: "mfe_account_costs.Coolant_CostModule",            DT_Fuel_CostModule: "mfe_account_costs.DT_Fuel_CostModule",            Divertor_CostModule: "mfe_account_costs.Divertor_CostModule",            Heating_CostModule: "mfe_account_costs.Heating_CostModule",            IDC_Closed_Form_CostModule: "mfe_account_costs.IDC_Closed_Form_CostModule",            Indirect_CostModule: "mfe_account_costs.Indirect_CostModule",            Installation_Labor_CostModule: "mfe_account_costs.Installation_Labor_CostModule",            Levelized_Annual_CostModule: "mfe_account_costs.Levelized_Annual_CostModule",            Levelized_Replacement_CostModule: "mfe_account_costs.Levelized_Replacement_CostModule",            Linear_Power_CostModule: "mfe_account_costs.Linear_Power_CostModule",            Plant_Power_Law_CostModule: "mfe_account_costs.Plant_Power_Law_CostModule",            Power_Supplies_CostModule: "mfe_account_costs.Power_Supplies_CostModule",            Preconstruction_CostModule: "mfe_account_costs.Preconstruction_CostModule",            Remote_Handling_CostModule: "mfe_account_costs.Remote_Handling_CostModule",            Shield_CostModule: "mfe_account_costs.Shield_CostModule",            Structure_CostModule: "mfe_account_costs.Structure_CostModule",            Supplementary_CostModule: "mfe_account_costs.Supplementary_CostModule",            Vessel_CostModule: "mfe_account_costs.Vessel_CostModule",            n_1cfe_Form_Capital_ChargeModule: "mfe_account_costs.n_1cfe_Form_Capital_ChargeModule",            n_1cfe_Form_LCOEModule: "mfe_account_costs.n_1cfe_Form_LCOEModule",            Cryoplant_Electrical_PowerModule: "mfe_cryo_plant.Cryoplant_Electrical_PowerModule",            LCOE_DCFModule: "mfe_lcoe_dcf.LCOE_DCFModule",            Magnet_Coil_CostModule: "mfe_magnet_cost.Magnet_Coil_CostModule",            DT_Fusion_PowerModule: "mfe_plasma_scaling.DT_Fusion_PowerModule",            MFE_Radial_BuildModule: "mfe_plasma_scaling.MFE_Radial_BuildModule",            Neutron_Wall_LoadModule: "mfe_plasma_scaling.Neutron_Wall_LoadModule",            Plasma_GeometryModule: "mfe_plasma_scaling.Plasma_GeometryModule",            MFE_Power_Balance_CalcModule: "mfe_power_balance.MFE_Power_Balance_CalcModule",            StellarisBetaOkConstraintModule: "stellarator_09.StellarisBetaOkConstraintModule",            StellarisNetPositiveConstraintModule: "stellarator_09.StellarisNetPositiveConstraintModule",            StellarisRecircOkConstraintModule: "stellarator_09.StellarisRecircOkConstraintModule",            StellarisTbrOkConstraintModule: "stellarator_09.StellarisTbrOkConstraintModule",            StellarisWallLoadOkConstraintModule: "stellarator_09.StellarisWallLoadOkConstraintModule",            bop_capitalModule: "stellarator_09.stellaris.bop_capitalModule",            cas20_capitalModule: "stellarator_09.stellaris.cas20_capitalModule",            cas22_capitalModule: "stellarator_09.stellaris.cas22_capitalModule",            cas23_to_28_capitalModule: "stellarator_09.stellaris.cas23_to_28_capitalModule",            cas2x_pre_contingencyModule: "stellarator_09.stellaris.cas2x_pre_contingencyModule",            overnight_capitalModule: "stellarator_09.stellaris.overnight_capitalModule",            powercore_capitalModule: "stellarator_09.stellaris.powercore_capitalModule",            reactor_equipment_subtotalModule: "stellarator_09.stellaris.reactor_equipment_subtotalModule",            replacement_cost_per_eventModule: "stellarator_09.stellaris.replacement_cost_per_eventModule",            total_capitalModule: "stellarator_09.stellaris.total_capitalModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    MfePlantParams,    StellaratorPlantParams,    SystemDesign,    ConstraintEvaluation,    ConstraintReport,    Float,]
