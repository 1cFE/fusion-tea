"""Heating_CostModule Module Wrapper

TEAx module for Heating_Cost calculation.

CAS22.1.4 Supplementary heating & current drive cost, steady-state MFE.
Sum of per-method installed power times per-MW cost:

  cost = nbi_per_mw*p_nbi + icrf_per_mw*p_icrf
       + ecrh_per_mw*p_ecrh + lhcd_per_mw*p_lhcd

All per-MW rates and delivered powers are the concept heating mix
(WI-011). Per-MW rates are ITER-procurement-calibrated in the source.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:454-459 (c220104 steady-state)
*Basis**: Linear per-method heating capital; MFE analogue of IFE ignition

Inputs:
    - icrf_per_mw: icrf_per_mw parameter
    - p_nbi_in: p_nbi_in parameter
    - ecrh_per_mw: ecrh_per_mw parameter
    - p_lhcd_in: p_lhcd_in parameter
    - p_ecrh_in: p_ecrh_in parameter
    - p_icrf_in: p_icrf_in parameter
    - nbi_per_mw: nbi_per_mw parameter
    - lhcd_per_mw: lhcd_per_mw parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:196

SysML Source: root-0/analyses/mfe_account_costs.sysml:196

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/heating_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Heating_CostInput(BaseModel):
    """Input model for Heating_CostModule.

    Attributes:
        icrf_per_mw: icrf_per_mw input
        p_nbi_in: p_nbi_in input
        ecrh_per_mw: ecrh_per_mw input
        p_lhcd_in: p_lhcd_in input
        p_ecrh_in: p_ecrh_in input
        p_icrf_in: p_icrf_in input
        nbi_per_mw: nbi_per_mw input
        lhcd_per_mw: lhcd_per_mw input
    """
    icrf_per_mw: float = Field(..., description="icrf_per_mw input")
    p_nbi_in: float = Field(..., description="p_nbi_in input")
    ecrh_per_mw: float = Field(..., description="ecrh_per_mw input")
    p_lhcd_in: float = Field(..., description="p_lhcd_in input")
    p_ecrh_in: float = Field(..., description="p_ecrh_in input")
    p_icrf_in: float = Field(..., description="p_icrf_in input")
    nbi_per_mw: float = Field(..., description="nbi_per_mw input")
    lhcd_per_mw: float = Field(..., description="lhcd_per_mw input")


class Heating_CostModule(ModuleBase[Heating_CostInput, Float]):
    """TEAx module for Heating_Cost calculation.

CAS22.1.4 Supplementary heating & current drive cost, steady-state MFE.
Sum of per-method installed power times per-MW cost:

  cost = nbi_per_mw*p_nbi + icrf_per_mw*p_icrf
       + ecrh_per_mw*p_ecrh + lhcd_per_mw*p_lhcd

All per-MW rates and delivered powers are the concept heating mix
(WI-011). Per-MW rates are ITER-procurement-calibrated in the source.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:454-459 (c220104 steady-state)
*Basis**: Linear per-method heating capital; MFE analogue of IFE ignition

Inputs:
    - icrf_per_mw: icrf_per_mw parameter
    - p_nbi_in: p_nbi_in parameter
    - ecrh_per_mw: ecrh_per_mw parameter
    - p_lhcd_in: p_lhcd_in parameter
    - p_ecrh_in: p_ecrh_in parameter
    - p_icrf_in: p_icrf_in parameter
    - nbi_per_mw: nbi_per_mw parameter
    - lhcd_per_mw: lhcd_per_mw parameter

Outputs:
    - cost: cost result

SysML Source: root-0/analyses/mfe_account_costs.sysml:196

    SysML Source: root-0/analyses/mfe_account_costs.sysml:196

    Calculation Specification:
        cost = nbi_per_mw * p_nbi_in + icrf_per_mw * p_icrf_in + ecrh_per_mw * p_ecrh_in + lhcd_per_mw * p_lhcd_in
        
Documentation:
CAS22.1.4 Supplementary heating & current drive cost, steady-state MFE.
Sum of per-method installed power times per-MW cost:

  cost = nbi_per_mw*p_nbi + icrf_per_mw*p_icrf
       + ecrh_per_mw*p_ecrh + lhcd_per_mw*p_lhcd

All per-MW rates and delivered powers are the concept heating mix
(WI-011). Per-MW rates are ITER-procurement-calibrated in the source.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/cas22.py
*Ref**: cas22.py:454-459 (c220104 steady-state)
*Basis**: Linear per-method heating capital; MFE analogue of IFE ignition

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_account_costs.heating_cost_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Heating_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, icrf_per_mw: float, p_nbi_in: float, ecrh_per_mw: float, p_lhcd_in: float, p_ecrh_in: float, p_icrf_in: float, nbi_per_mw: float, lhcd_per_mw: float    ) -> Heating_CostInput:
        """Validate inputs and fill defaults.

        Args:
            icrf_per_mw: icrf_per_mw input
            p_nbi_in: p_nbi_in input
            ecrh_per_mw: ecrh_per_mw input
            p_lhcd_in: p_lhcd_in input
            p_ecrh_in: p_ecrh_in input
            p_icrf_in: p_icrf_in input
            nbi_per_mw: nbi_per_mw input
            lhcd_per_mw: lhcd_per_mw input

        Returns:
            Validated input model
        """
        return Heating_CostInput(icrf_per_mw=icrf_per_mw, p_nbi_in=p_nbi_in, ecrh_per_mw=ecrh_per_mw, p_lhcd_in=p_lhcd_in, p_ecrh_in=p_ecrh_in, p_icrf_in=p_icrf_in, nbi_per_mw=nbi_per_mw, lhcd_per_mw=lhcd_per_mw)

    def run(
        self, icrf_per_mw: float, p_nbi_in: float, ecrh_per_mw: float, p_lhcd_in: float, p_ecrh_in: float, p_icrf_in: float, nbi_per_mw: float, lhcd_per_mw: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            icrf_per_mw: icrf_per_mw input
            p_nbi_in: p_nbi_in input
            ecrh_per_mw: ecrh_per_mw input
            p_lhcd_in: p_lhcd_in input
            p_ecrh_in: p_ecrh_in input
            p_icrf_in: p_icrf_in input
            nbi_per_mw: nbi_per_mw input
            lhcd_per_mw: lhcd_per_mw input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(icrf_per_mw, p_nbi_in, ecrh_per_mw, p_lhcd_in, p_ecrh_in, p_icrf_in, nbi_per_mw, lhcd_per_mw)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.heating_cost_impl import (
            run_heating_cost,
        )

        # Execute implementation - returns single value
        cost = run_heating_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
