"""Explicit literal or inferred FPY/calendar allocation; guards all consumer inputs."""
import math
AUTO_IMPLEMENTED = False

def run_budget_period_allocation(inputs):
    from budget_tea.schemas.budget_period_allocation_output import Budget_Period_AllocationOutput
    for name,value in inputs.model_dump().items():
        if not math.isfinite(value):raise ValueError(name+' must be finite')
    if inputs.capital_budget_in<0 or inputs.replacement_budget_in<0:raise ValueError('budget costs must be nonnegative')
    if inputs.selected_period_in<=0:raise ValueError('selected period must be positive')
    if inputs.net_power_in<=0:raise ValueError('net power must be positive')
    if not 0<inputs.availability_in<=1:raise ValueError('availability must be in (0,1]')
    if inputs.period_mode_in not in (0.,1.):raise ValueError('period mode must be zero or one')
    period=inputs.selected_period_in if inputs.period_mode_in==0 else inputs.selected_period_in/inputs.availability_in
    capital=inputs.capital_budget_in/period
    replacement=inputs.replacement_budget_in/period
    # Exact downstream formula grouping, with fixed single-module and excluded-scope channels.
    energy=((8760.0*inputs.net_power_in)*1.0)*inputs.availability_in
    lifetime=energy*period
    result=dict(annual_capital=capital,annual_replacement=replacement,partial_annual_cost=capital+replacement,comparison_period=period,annual_energy=energy,lifetime_energy=lifetime,validated_net_power=inputs.net_power_in,validated_availability=inputs.availability_in,module_count=1.0,excluded_annual_channel=0.0)
    if not all(math.isfinite(v) for v in result.values()):raise ValueError('nonfinite allocated budget or energy')
    if energy<=0 or lifetime<=0:raise ValueError('annual and lifetime energy must be positive')
    if not math.isfinite(((capital+replacement)+0.0)/energy):raise ValueError('nonfinite partial cost quotient')
    return tuple(result[name] for name in Budget_Period_AllocationOutput.model_fields)
