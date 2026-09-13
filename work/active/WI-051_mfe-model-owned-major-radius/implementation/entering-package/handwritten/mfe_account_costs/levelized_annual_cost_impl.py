"""Auto-generated implementation for Levelized_Annual_Cost.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_account_costs.sysml:670

SysML Expressions:
    disc_pow_n = (1.0 + interest_rate) ** operational_years_in
    crf = interest_rate * disc_pow_n / (disc_pow_n - 1.0)
    a1 = annual_cost * (1.0 + inflation_rate_in) ** project_time
    pv = a1 * (1.0 - ((1.0 + inflation_rate_in) / (1.0 + interest_rate)) ** operational_years_in) / (interest_rate - inflation_rate_in)
    levelized = crf * pv
    
Documentation:
Levelized (growing-annuity) annual cost -- the shared CAS71/CAS80
wrapper:

  crf = i*(1+i)^n / ((1+i)^n - 1)
  a1  = annual_cost * (1+g)^Tc
  pv  = a1 * (1 - ((1+g)/(1+i))^n) / (i - g)
  levelized = crf * pv

A real annual stream escalating at g from the first operating year is
present-valued over n operating years at discount rate i, then
annuitized by CRF. `project_time` Tc is the construction period that
escalates the stream to its first operating year -- at NOAK that is
`construction_time` alone (1cfe adds licensing_time only when FOAK,
costs.py:41-44), so Tc = 8 at both the design and handshake points.

Used TWICE by the plant (MR-3, one def two usages): with
annual_cost = the unlevelized annual O&M -> CAS71, and with
annual_cost = the raw annual DT fuel cost -> CAS80.

Flat-Real (+ - * / **) -- Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:13-50 (levelized_annual_cost); economics.py:6-10 (CRF);
costs.py:41-44 (_total_project_time, NOAK omits licensing_time)
*Basis**: Growing-annuity present value annuitized by the capital recovery factor
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_account_costs.levelized_annual_cost import Levelized_Annual_CostInput


def run_levelized_annual_cost(inputs: Levelized_Annual_CostInput) -> tuple[float, float]:
    """Execute Levelized_Annual_Cost calculation.

Levelized (growing-annuity) annual cost -- the shared CAS71/CAS80
wrapper:

  crf = i*(1+i)^n / ((1+i)^n - 1)
  a1  = annual_cost * (1+g)^Tc
  pv  = a1 * (1 - ((1+g)/(1+i))^n) / (i - g)
  levelized = crf * pv

A real annual stream escalating at g from the first operating year is
present-valued over n operating years at discount rate i, then
annuitized by CRF. `project_time` Tc is the construction period that
escalates the stream to its first operating year -- at NOAK that is
`construction_time` alone (1cfe adds licensing_time only when FOAK,
costs.py:41-44), so Tc = 8 at both the design and handshake points.

Used TWICE by the plant (MR-3, one def two usages): with
annual_cost = the unlevelized annual O&M -> CAS71, and with
annual_cost = the raw annual DT fuel cost -> CAS80.

Flat-Real (+ - * / **) -- Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:13-50 (levelized_annual_cost); economics.py:6-10 (CRF);
costs.py:41-44 (_total_project_time, NOAK omits licensing_time)
*Basis**: Growing-annuity present value annuitized by the capital recovery factor

SysML Source: root-0/analyses/mfe_account_costs.sysml:670

SysML Expressions:
    disc_pow_n = (1.0 + interest_rate) ** operational_years_in
    crf = interest_rate * disc_pow_n / (disc_pow_n - 1.0)
    a1 = annual_cost * (1.0 + inflation_rate_in) ** project_time
    pv = a1 * (1.0 - ((1.0 + inflation_rate_in) / (1.0 + interest_rate)) ** operational_years_in) / (interest_rate - inflation_rate_in)
    levelized = crf * pv
    
Documentation:
Levelized (growing-annuity) annual cost -- the shared CAS71/CAS80
wrapper:

  crf = i*(1+i)^n / ((1+i)^n - 1)
  a1  = annual_cost * (1+g)^Tc
  pv  = a1 * (1 - ((1+g)/(1+i))^n) / (i - g)
  levelized = crf * pv

A real annual stream escalating at g from the first operating year is
present-valued over n operating years at discount rate i, then
annuitized by CRF. `project_time` Tc is the construction period that
escalates the stream to its first operating year -- at NOAK that is
`construction_time` alone (1cfe adds licensing_time only when FOAK,
costs.py:41-44), so Tc = 8 at both the design and handshake points.

Used TWICE by the plant (MR-3, one def two usages): with
annual_cost = the unlevelized annual O&M -> CAS71, and with
annual_cost = the raw annual DT fuel cost -> CAS80.

Flat-Real (+ - * / **) -- Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:13-50 (levelized_annual_cost); economics.py:6-10 (CRF);
costs.py:41-44 (_total_project_time, NOAK omits licensing_time)
*Basis**: Growing-annuity present value annuitized by the capital recovery factor

Args:
    inputs: Input parameters validated against Levelized_Annual_CostInput schema

Returns:
    tuple[float, ...]: (levelized, crf)

Example:
    >>> inputs = Levelized_Annual_CostInput(...)
    >>> levelized, crf = run_levelized_annual_cost(inputs)
    """
    disc_pow_n = ((1.0 + inputs.interest_rate) ** inputs.operational_years_in)
    a1 = (inputs.annual_cost * ((1.0 + inputs.inflation_rate_in) ** inputs.project_time))
    pv = ((a1 * (1.0 - (((1.0 + inputs.inflation_rate_in) / (1.0 + inputs.interest_rate)) ** inputs.operational_years_in))) / (inputs.interest_rate - inputs.inflation_rate_in))
    crf = ((inputs.interest_rate * disc_pow_n) / (disc_pow_n - 1.0))
    return (
        (crf * pv),  # levelized
        crf,
    )
