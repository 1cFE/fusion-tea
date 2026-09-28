from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from heat_tea.modules.dual_circuit_heat_accounting.coolant_branch_heat import Coolant_Branch_HeatModule
from heat_tea.modules.dual_circuit_heat_accounting.dual_circuit_heat_ledger import Dual_Circuit_Heat_LedgerModule
from heat_tea.modules.mfe_viability.offered_capacity_screen import Offered_Capacity_ScreenModule
from heat_tea.modules.aries_dual_blanket_heat.inter_coolant_exchange.absent_boundary_exchange_mw import absent_boundary_exchange_mwModule
from heat_tea.modules.aries_dual_blanket_heat.heliumcapacityokconstraintmodule import HeliumCapacityOkConstraintModule
from heat_tea.modules.aries_dual_blanket_heat.pblicapacityokconstraintmodule import PbliCapacityOkConstraintModule
from heat_tea.modules.constraints.constraintreportaggregatormodule import ConstraintReportAggregatorModule

from heat_tea.schemas.constraint_types import ConstraintEvaluation as ConstraintEvaluation, ConstraintReport as ConstraintReport
from heat_tea.schemas.dual_blanket_heat_params import DualBlanketHeatParams as DualBlanketHeatParams

from heat_tea.primitives import Float


def create_heat_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            HeliumCapacityOkConstraintModule,            PbliCapacityOkConstraintModule,            absent_boundary_exchange_mwModule,            ConstraintReportAggregatorModule,            Coolant_Branch_HeatModule,            Dual_Circuit_Heat_LedgerModule,            Offered_Capacity_ScreenModule,        ],
        module_type_override={            HeliumCapacityOkConstraintModule: "aries_dual_blanket_heat.HeliumCapacityOkConstraintModule",            PbliCapacityOkConstraintModule: "aries_dual_blanket_heat.PbliCapacityOkConstraintModule",            absent_boundary_exchange_mwModule: "aries_dual_blanket_heat.inter_coolant_exchange.absent_boundary_exchange_mwModule",            ConstraintReportAggregatorModule: "constraints.ConstraintReportAggregatorModule",            Coolant_Branch_HeatModule: "dual_circuit_heat_accounting.Coolant_Branch_HeatModule",            Dual_Circuit_Heat_LedgerModule: "dual_circuit_heat_accounting.Dual_Circuit_Heat_LedgerModule",            Offered_Capacity_ScreenModule: "mfe_viability.Offered_Capacity_ScreenModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    DualBlanketHeatParams,    ConstraintEvaluation,    ConstraintReport,    Float,]
