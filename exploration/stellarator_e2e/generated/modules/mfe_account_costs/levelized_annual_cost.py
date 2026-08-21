"""Levelized_Annual_CostModule Module Wrapper

TEAx module for Levelized_Annual_Cost calculation.

Levelized (growing-annuity) annual cost — the shared CAS71/CAS80
wrapper:

  crf = i*(1+i)^n / ((1+i)^n - 1)
  a1  = annual_cost * (1+g)^Tc
  pv  = a1 * (1 - ((1+g)/(1+i))^n) / (i - g)
  levelized = crf * pv

A real annual stream escalating at g from the first operating year is
present-valued over n operating years at discount rate i, then
annuitized by CRF. `project_time` Tc is the construction period that
escalates the stream to its first operating year — at NOAK that is
`construction_time` alone (1cfe adds licensing_time only when FOAK,
costs.py:41-44), so Tc = 8 at both the design and handshake points.

Used TWICE by the plant (MR-3, one def two usages): with
annual_cost = the unlevelized annual O&M -> CAS71, and with
annual_cost = the raw annual DT fuel cost -> CAS80.

Flat-Real (+ - * / **) — Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:13-50 (levelized_annual_cost); economics.py:6-10 (CRF);
costs.py:41-44 (_total_project_time, NOAK omits licensing_time)
*Basis**: Growing-annuity present value annuitized by the capital recovery factor

Inputs:
    - annual_cost: annual_cost parameter
    - interest_rate: interest_rate parameter
    - inflation_rate: inflation_rate parameter
    - operational_years: operational_years parameter
    - project_time: project_time parameter

Outputs:
    - crf: crf result
    - levelized: levelized result

SysML Source: root-0/analyses/mfe_account_costs.sysml:628

SysML Source: root-0/analyses/mfe_account_costs.sysml:628

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/levelized_annual_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.levelized_annual_cost_output import Levelized_Annual_CostOutput


class Levelized_Annual_CostInput(BaseModel):
    """Input model for Levelized_Annual_CostModule.

    Attributes:
        annual_cost: annual_cost input
        interest_rate: interest_rate input
        inflation_rate: inflation_rate input
        operational_years: operational_years input
        project_time: project_time input
    """
    annual_cost: float = Field(..., description="annual_cost input")
    interest_rate: float = Field(..., description="interest_rate input")
    inflation_rate: float = Field(..., description="inflation_rate input")
    operational_years: float = Field(..., description="operational_years input")
    project_time: float = Field(..., description="project_time input")


class Levelized_Annual_CostModule(ModuleBase[Levelized_Annual_CostInput, Levelized_Annual_CostOutput]):
    """TEAx module for Levelized_Annual_Cost calculation.

Levelized (growing-annuity) annual cost — the shared CAS71/CAS80
wrapper:

  crf = i*(1+i)^n / ((1+i)^n - 1)
  a1  = annual_cost * (1+g)^Tc
  pv  = a1 * (1 - ((1+g)/(1+i))^n) / (i - g)
  levelized = crf * pv

A real annual stream escalating at g from the first operating year is
present-valued over n operating years at discount rate i, then
annuitized by CRF. `project_time` Tc is the construction period that
escalates the stream to its first operating year — at NOAK that is
`construction_time` alone (1cfe adds licensing_time only when FOAK,
costs.py:41-44), so Tc = 8 at both the design and handshake points.

Used TWICE by the plant (MR-3, one def two usages): with
annual_cost = the unlevelized annual O&M -> CAS71, and with
annual_cost = the raw annual DT fuel cost -> CAS80.

Flat-Real (+ - * / **) — Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:13-50 (levelized_annual_cost); economics.py:6-10 (CRF);
costs.py:41-44 (_total_project_time, NOAK omits licensing_time)
*Basis**: Growing-annuity present value annuitized by the capital recovery factor

Inputs:
    - annual_cost: annual_cost parameter
    - interest_rate: interest_rate parameter
    - inflation_rate: inflation_rate parameter
    - operational_years: operational_years parameter
    - project_time: project_time parameter

Outputs:
    - crf: crf result
    - levelized: levelized result

SysML Source: root-0/analyses/mfe_account_costs.sysml:628

    SysML Source: root-0/analyses/mfe_account_costs.sysml:628

    Calculation Specification:
        disc_pow_n = (1.0 + interest_rate) ** operational_years
        crf = interest_rate * disc_pow_n / (disc_pow_n - 1.0)
        a1 = annual_cost * (1.0 + inflation_rate) ** project_time
        pv = a1 * (1.0 - ((1.0 + inflation_rate) / (1.0 + interest_rate)) ** operational_years) / (interest_rate - inflation_rate)
        levelized = crf * pv
        
Documentation:
Levelized (growing-annuity) annual cost — the shared CAS71/CAS80
wrapper:

  crf = i*(1+i)^n / ((1+i)^n - 1)
  a1  = annual_cost * (1+g)^Tc
  pv  = a1 * (1 - ((1+g)/(1+i))^n) / (i - g)
  levelized = crf * pv

A real annual stream escalating at g from the first operating year is
present-valued over n operating years at discount rate i, then
annuitized by CRF. `project_time` Tc is the construction period that
escalates the stream to its first operating year — at NOAK that is
`construction_time` alone (1cfe adds licensing_time only when FOAK,
costs.py:41-44), so Tc = 8 at both the design and handshake points.

Used TWICE by the plant (MR-3, one def two usages): with
annual_cost = the unlevelized annual O&M -> CAS71, and with
annual_cost = the raw annual DT fuel cost -> CAS80.

Flat-Real (+ - * / **) — Rung A, lowers to generated arithmetic.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
*Ref**: economics.py:13-50 (levelized_annual_cost); economics.py:6-10 (CRF);
costs.py:41-44 (_total_project_time, NOAK omits licensing_time)
*Basis**: Growing-annuity present value annuitized by the capital recovery factor

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.levelized_annual_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts crf, levelized fields to separate channels.
    """

    name: str = "Levelized_Annual_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, annual_cost: float, interest_rate: float, inflation_rate: float, operational_years: float, project_time: float    ) -> Levelized_Annual_CostInput:
        """Validate inputs and fill defaults.

        Args:
            annual_cost: annual_cost input
            interest_rate: interest_rate input
            inflation_rate: inflation_rate input
            operational_years: operational_years input
            project_time: project_time input

        Returns:
            Validated input model
        """
        return Levelized_Annual_CostInput(annual_cost=annual_cost, interest_rate=interest_rate, inflation_rate=inflation_rate, operational_years=operational_years, project_time=project_time)

    def run(
        self, annual_cost: float, interest_rate: float, inflation_rate: float, operational_years: float, project_time: float    ) -> ModuleResult[Levelized_Annual_CostOutput]:
        """Execute calculation.

        Args:
            annual_cost: annual_cost input
            interest_rate: interest_rate input
            inflation_rate: inflation_rate input
            operational_years: operational_years input
            project_time: project_time input

        Returns:
            Module result with Levelized_Annual_CostOutput (crf, levelized)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(annual_cost, interest_rate, inflation_rate, operational_years, project_time)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.levelized_annual_cost_impl import (
            run_levelized_annual_cost,
        )

        # Execute implementation - returns tuple of values
        crf, levelized = run_levelized_annual_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Levelized_Annual_CostOutput(
                crf=crf,
                levelized=levelized,
            )
        )
