from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from aries_integrated.modules.dual_circuit_heat_accounting.coolant_branch_heat import Coolant_Branch_HeatModule
from aries_integrated.modules.ideal_gas_brayton_components.fixed_outlet_conditioning import Fixed_Outlet_ConditioningModule
from aries_integrated.modules.ideal_gas_brayton_components.fractional_pressure_loss import Fractional_Pressure_LossModule
from aries_integrated.modules.ideal_gas_brayton_components.ideal_gas_compressor import Ideal_Gas_CompressorModule
from aries_integrated.modules.ideal_gas_brayton_components.ideal_gas_expander import Ideal_Gas_ExpanderModule
from aries_integrated.modules.integrated_heat_electricity.fusion_source_selector import Fusion_Source_SelectorModule
from aries_integrated.modules.integrated_heat_electricity.heat_driven_closure import Heat_Driven_ClosureModule
from aries_integrated.modules.integrated_heat_electricity.integrated_heat_source import Integrated_Heat_SourceModule
from aries_integrated.modules.integrated_heat_electricity.integrated_plant_ledger import Integrated_Plant_LedgerModule
from aries_integrated.modules.integrated_heat_electricity.passive_recuperator import Passive_RecuperatorModule
from aries_integrated.modules.integrated_heat_electricity.plant_electrical_balance import Plant_Electrical_BalanceModule
from aries_integrated.modules.mfe_fuel_cycle.fuel_cycle_flows import Fuel_Cycle_FlowsModule
from aries_integrated.modules.mfe_plasma_scaling.volume_averaged_beta import Volume_Averaged_BetaModule
from aries_integrated.modules.mfe_viability.offered_capacity_screen import Offered_Capacity_ScreenModule
from aries_integrated.modules.radial_density_profile.radial_density_profile import Radial_Density_ProfileModule
from aries_integrated.modules.supplied_profile_plasma.supplied_profile_plasma import Supplied_Profile_PlasmaModule
from aries_integrated.modules.aries_cs_plasma_integration.plasma.edge_density import edge_densityModule
from aries_integrated.modules.aries_integrated_plant.compressorcapacitycapacityokconstraintmodule import CompressorCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.divertorcapacitycapacityokconstraintmodule import DivertorCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.fuelcapacitycapacityokconstraintmodule import FuelCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.generatorcapacitycapacityokconstraintmodule import GeneratorCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.hecapacitycapacityokconstraintmodule import HeCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.pblicapacitycapacityokconstraintmodule import PbliCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.plantledgerbalancesokconstraintmodule import PlantLedgerBalancesOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.plantledgerheatremovalokconstraintmodule import PlantLedgerHeatRemovalOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.rejectioncapacitycapacityokconstraintmodule import RejectionCapacityCapacityOkConstraintModule
from aries_integrated.modules.aries_integrated_plant.turbinecapacitycapacityokconstraintmodule import TurbineCapacityCapacityOkConstraintModule
from aries_integrated.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule

from aries_integrated.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
from aries_integrated.schemas.mfe_plasma_scaling_params import MfePlasmaScalingParams as MfePlasmaScalingParams
from aries_integrated.schemas.plant_params import PlantParams as PlantParams
from aries_integrated.schemas.plasma_integration_params import PlasmaIntegrationParams as PlasmaIntegrationParams

from aries_integrated.primitives import Float


def create_aries_integrated_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            edge_densityModule,            CompressorCapacityCapacityOkConstraintModule,            DivertorCapacityCapacityOkConstraintModule,            FuelCapacityCapacityOkConstraintModule,            GeneratorCapacityCapacityOkConstraintModule,            HeCapacityCapacityOkConstraintModule,            PbliCapacityCapacityOkConstraintModule,            PlantLedgerBalancesOkConstraintModule,            PlantLedgerHeatRemovalOkConstraintModule,            RejectionCapacityCapacityOkConstraintModule,            TurbineCapacityCapacityOkConstraintModule,            ConstraintReportAggregatorModule,            Coolant_Branch_HeatModule,            Fixed_Outlet_ConditioningModule,            Fractional_Pressure_LossModule,            Ideal_Gas_CompressorModule,            Ideal_Gas_ExpanderModule,            Fusion_Source_SelectorModule,            Heat_Driven_ClosureModule,            Integrated_Heat_SourceModule,            Integrated_Plant_LedgerModule,            Passive_RecuperatorModule,            Plant_Electrical_BalanceModule,            Fuel_Cycle_FlowsModule,            Volume_Averaged_BetaModule,            Offered_Capacity_ScreenModule,            Radial_Density_ProfileModule,            Supplied_Profile_PlasmaModule,        ],
        module_type_override={            edge_densityModule: "aries_cs_plasma_integration.plasma.edge_densityModule",            CompressorCapacityCapacityOkConstraintModule: "aries_integrated_plant.CompressorCapacityCapacityOkConstraintModule",            DivertorCapacityCapacityOkConstraintModule: "aries_integrated_plant.DivertorCapacityCapacityOkConstraintModule",            FuelCapacityCapacityOkConstraintModule: "aries_integrated_plant.FuelCapacityCapacityOkConstraintModule",            GeneratorCapacityCapacityOkConstraintModule: "aries_integrated_plant.GeneratorCapacityCapacityOkConstraintModule",            HeCapacityCapacityOkConstraintModule: "aries_integrated_plant.HeCapacityCapacityOkConstraintModule",            PbliCapacityCapacityOkConstraintModule: "aries_integrated_plant.PbliCapacityCapacityOkConstraintModule",            PlantLedgerBalancesOkConstraintModule: "aries_integrated_plant.PlantLedgerBalancesOkConstraintModule",            PlantLedgerHeatRemovalOkConstraintModule: "aries_integrated_plant.PlantLedgerHeatRemovalOkConstraintModule",            RejectionCapacityCapacityOkConstraintModule: "aries_integrated_plant.RejectionCapacityCapacityOkConstraintModule",            TurbineCapacityCapacityOkConstraintModule: "aries_integrated_plant.TurbineCapacityCapacityOkConstraintModule",            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            Coolant_Branch_HeatModule: "dual_circuit_heat_accounting.Coolant_Branch_HeatModule",            Fixed_Outlet_ConditioningModule: "ideal_gas_brayton_components.Fixed_Outlet_ConditioningModule",            Fractional_Pressure_LossModule: "ideal_gas_brayton_components.Fractional_Pressure_LossModule",            Ideal_Gas_CompressorModule: "ideal_gas_brayton_components.Ideal_Gas_CompressorModule",            Ideal_Gas_ExpanderModule: "ideal_gas_brayton_components.Ideal_Gas_ExpanderModule",            Fusion_Source_SelectorModule: "integrated_heat_electricity.Fusion_Source_SelectorModule",            Heat_Driven_ClosureModule: "integrated_heat_electricity.Heat_Driven_ClosureModule",            Integrated_Heat_SourceModule: "integrated_heat_electricity.Integrated_Heat_SourceModule",            Integrated_Plant_LedgerModule: "integrated_heat_electricity.Integrated_Plant_LedgerModule",            Passive_RecuperatorModule: "integrated_heat_electricity.Passive_RecuperatorModule",            Plant_Electrical_BalanceModule: "integrated_heat_electricity.Plant_Electrical_BalanceModule",            Fuel_Cycle_FlowsModule: "mfe_fuel_cycle.Fuel_Cycle_FlowsModule",            Volume_Averaged_BetaModule: "mfe_plasma_scaling.Volume_Averaged_BetaModule",            Offered_Capacity_ScreenModule: "mfe_viability.Offered_Capacity_ScreenModule",            Radial_Density_ProfileModule: "radial_density_profile.Radial_Density_ProfileModule",            Supplied_Profile_PlasmaModule: "supplied_profile_plasma.Supplied_Profile_PlasmaModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    MfePlasmaScalingParams,    PlantParams,    PlasmaIntegrationParams,    ConstraintEvaluation,    ConstraintReport,    Float,]
