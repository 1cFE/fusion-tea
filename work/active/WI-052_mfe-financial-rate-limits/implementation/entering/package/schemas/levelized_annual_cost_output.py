from pydantic import Field
from simkit.config.schema import MultiOutput

class Levelized_Annual_CostOutput(MultiOutput):
    """Multi-output container for Levelized_Annual_Cost.

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

SysML Source: root-0/analyses/mfe_account_costs.sysml:672
    """
    levelized: float = Field(description="levelized output")
    crf: float = Field(description="crf output")
