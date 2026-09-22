from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from brayton_tea.modules.ideal_gas_brayton_components.brayton_cycle_ledger import Brayton_Cycle_LedgerModule
from brayton_tea.modules.ideal_gas_brayton_components.equal_capacity_recuperator import Equal_Capacity_RecuperatorModule
from brayton_tea.modules.ideal_gas_brayton_components.fixed_outlet_conditioning import Fixed_Outlet_ConditioningModule
from brayton_tea.modules.ideal_gas_brayton_components.fractional_pressure_loss import Fractional_Pressure_LossModule
from brayton_tea.modules.ideal_gas_brayton_components.ideal_gas_compressor import Ideal_Gas_CompressorModule
from brayton_tea.modules.ideal_gas_brayton_components.ideal_gas_expander import Ideal_Gas_ExpanderModule
from brayton_tea.modules.mfe_viability.offered_capacity_screen import Offered_Capacity_ScreenModule
from brayton_tea.modules.aries_nominal_brayton.compressorcapacitycapacityokconstraintmodule import CompressorCapacityCapacityOkConstraintModule
from brayton_tea.modules.aries_nominal_brayton.heatercapacitycapacityokconstraintmodule import HeaterCapacityCapacityOkConstraintModule
from brayton_tea.modules.aries_nominal_brayton.rejectioncapacitycapacityokconstraintmodule import RejectionCapacityCapacityOkConstraintModule
from brayton_tea.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule

from brayton_tea.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
from brayton_tea.schemas.nominal_brayton_params import NominalBraytonParams as NominalBraytonParams

from brayton_tea.primitives import Float


def create_brayton_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            CompressorCapacityCapacityOkConstraintModule,            HeaterCapacityCapacityOkConstraintModule,            RejectionCapacityCapacityOkConstraintModule,            ConstraintReportAggregatorModule,            Brayton_Cycle_LedgerModule,            Equal_Capacity_RecuperatorModule,            Fixed_Outlet_ConditioningModule,            Fractional_Pressure_LossModule,            Ideal_Gas_CompressorModule,            Ideal_Gas_ExpanderModule,            Offered_Capacity_ScreenModule,        ],
        module_type_override={            CompressorCapacityCapacityOkConstraintModule: "aries_nominal_brayton.CompressorCapacityCapacityOkConstraintModule",            HeaterCapacityCapacityOkConstraintModule: "aries_nominal_brayton.HeaterCapacityCapacityOkConstraintModule",            RejectionCapacityCapacityOkConstraintModule: "aries_nominal_brayton.RejectionCapacityCapacityOkConstraintModule",            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            Brayton_Cycle_LedgerModule: "ideal_gas_brayton_components.Brayton_Cycle_LedgerModule",            Equal_Capacity_RecuperatorModule: "ideal_gas_brayton_components.Equal_Capacity_RecuperatorModule",            Fixed_Outlet_ConditioningModule: "ideal_gas_brayton_components.Fixed_Outlet_ConditioningModule",            Fractional_Pressure_LossModule: "ideal_gas_brayton_components.Fractional_Pressure_LossModule",            Ideal_Gas_CompressorModule: "ideal_gas_brayton_components.Ideal_Gas_CompressorModule",            Ideal_Gas_ExpanderModule: "ideal_gas_brayton_components.Ideal_Gas_ExpanderModule",            Offered_Capacity_ScreenModule: "mfe_viability.Offered_Capacity_ScreenModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    NominalBraytonParams,    ConstraintEvaluation,    ConstraintReport,    Float,]
