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
    - nbi_per_mw: nbi_per_mw parameter
    - p_nbi: p_nbi parameter
    - icrf_per_mw: icrf_per_mw parameter
    - p_icrf: p_icrf parameter
    - ecrh_per_mw: ecrh_per_mw parameter
    - p_ecrh: p_ecrh parameter
    - lhcd_per_mw: lhcd_per_mw parameter
    - p_lhcd: p_lhcd parameter

Outputs:
    - cost: cost result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:196

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:196

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_account_costs/heating_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Heating_CostInput(BaseModel):
    """Input model for Heating_CostModule.

    Attributes:
        nbi_per_mw: nbi_per_mw input
        p_nbi: p_nbi input
        icrf_per_mw: icrf_per_mw input
        p_icrf: p_icrf input
        ecrh_per_mw: ecrh_per_mw input
        p_ecrh: p_ecrh input
        lhcd_per_mw: lhcd_per_mw input
        p_lhcd: p_lhcd input
    """
    nbi_per_mw: float = Field(..., description="nbi_per_mw input")
    p_nbi: float = Field(..., description="p_nbi input")
    icrf_per_mw: float = Field(..., description="icrf_per_mw input")
    p_icrf: float = Field(..., description="p_icrf input")
    ecrh_per_mw: float = Field(..., description="ecrh_per_mw input")
    p_ecrh: float = Field(..., description="p_ecrh input")
    lhcd_per_mw: float = Field(..., description="lhcd_per_mw input")
    p_lhcd: float = Field(..., description="p_lhcd input")


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
    - nbi_per_mw: nbi_per_mw parameter
    - p_nbi: p_nbi parameter
    - icrf_per_mw: icrf_per_mw parameter
    - p_icrf: p_icrf parameter
    - ecrh_per_mw: ecrh_per_mw parameter
    - p_ecrh: p_ecrh parameter
    - lhcd_per_mw: lhcd_per_mw parameter
    - p_lhcd: p_lhcd parameter

Outputs:
    - cost: cost result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:196

    SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_account_costs.sysml:196

    Calculation Specification:
        cost = nbi_per_mw * p_nbi + icrf_per_mw * p_icrf + ecrh_per_mw * p_ecrh + lhcd_per_mw * p_lhcd
        
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
        self, nbi_per_mw: float, p_nbi: float, icrf_per_mw: float, p_icrf: float, ecrh_per_mw: float, p_ecrh: float, lhcd_per_mw: float, p_lhcd: float    ) -> Heating_CostInput:
        """Validate inputs and fill defaults.

        Args:
            nbi_per_mw: nbi_per_mw input
            p_nbi: p_nbi input
            icrf_per_mw: icrf_per_mw input
            p_icrf: p_icrf input
            ecrh_per_mw: ecrh_per_mw input
            p_ecrh: p_ecrh input
            lhcd_per_mw: lhcd_per_mw input
            p_lhcd: p_lhcd input

        Returns:
            Validated input model
        """
        return Heating_CostInput(nbi_per_mw=nbi_per_mw, p_nbi=p_nbi, icrf_per_mw=icrf_per_mw, p_icrf=p_icrf, ecrh_per_mw=ecrh_per_mw, p_ecrh=p_ecrh, lhcd_per_mw=lhcd_per_mw, p_lhcd=p_lhcd)

    def run(
        self, nbi_per_mw: float, p_nbi: float, icrf_per_mw: float, p_icrf: float, ecrh_per_mw: float, p_ecrh: float, lhcd_per_mw: float, p_lhcd: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            nbi_per_mw: nbi_per_mw input
            p_nbi: p_nbi input
            icrf_per_mw: icrf_per_mw input
            p_icrf: p_icrf input
            ecrh_per_mw: ecrh_per_mw input
            p_ecrh: p_ecrh input
            lhcd_per_mw: lhcd_per_mw input
            p_lhcd: p_lhcd input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(nbi_per_mw, p_nbi, icrf_per_mw, p_icrf, ecrh_per_mw, p_ecrh, lhcd_per_mw, p_lhcd)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_account_costs.heating_cost_impl import (
            run_heating_cost,
        )

        # Execute implementation - returns single value
        cost = run_heating_cost(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(cost))
