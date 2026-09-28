from simkit.core.registry_builder import create_registry
from simkit.core.pipeline_registry import PipelineModuleRegistry

from budget_tea.modules.mfe_account_costs.n_1cfe_form_lcoe import n_1cfe_Form_LCOEModule
from budget_tea.modules.source_budget_accounting.budget_period_allocation import Budget_Period_AllocationModule
from budget_tea.modules.source_budget_accounting.disjoint_capital_budget import Disjoint_Capital_BudgetModule

from budget_tea.schemas.source_budget_params import SourceBudgetParams as SourceBudgetParams

from budget_tea.primitives import Float


def create_budget_tea_registry() -> PipelineModuleRegistry:
    """Create registry for all modules using auto-introspection.

    Pure auto-registration pattern:
    - All modules (single-output and multi-output) use create_registry()
    - TEAx introspection handles RootModel[T] and BaseModel fields correctly

    ADR-003: Uses module_type_override to register modules with namespaced
    module types (e.g., "fusionphysics_powerbalance.AlphaNeutronSplitModule")
    while keeping Python class names unchanged (e.g., "AlphaNeutronSplitModule").
    """
    return create_registry(
        [            n_1cfe_Form_LCOEModule,            Budget_Period_AllocationModule,            Disjoint_Capital_BudgetModule,        ],
        module_type_override={            n_1cfe_Form_LCOEModule: "mfe_account_costs.n_1cfe_Form_LCOEModule",            Budget_Period_AllocationModule: "source_budget_accounting.Budget_Period_AllocationModule",            Disjoint_Capital_BudgetModule: "source_budget_accounting.Disjoint_Capital_BudgetModule",        },
    )


# Custom schema types for TEAx pipeline registration
# Use with: execute_pipeline(..., custom_schema_types=CUSTOM_SCHEMA_TYPES)
CUSTOM_SCHEMA_TYPES = [    SourceBudgetParams,    Float,]
