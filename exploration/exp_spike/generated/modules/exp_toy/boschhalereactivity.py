"""BoschHaleReactivityModule Module Wrapper

TEAx module for BoschHaleReactivity calculation.

Bosch-Hale-flavored DT reactivity shape:
    sigma_v = C * exp(-B / T^(1/3)) / T^(2/3)
(NRL-formulary-style approximation, valid ~10s of keV; toy
coefficients, physically shaped so success is meaningful).
Out-of-envelope: contains an inline invocation of Exp.

Inputs:
    - t_kev: t_kev parameter
    - c_coeff: c_coeff parameter
    - b_gamow: b_gamow parameter

Outputs:
    - sigma_v: sigma_v result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:39

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:39

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/exp_toy/boschhalereactivity_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exp_toy_tea.primitives import Float


class BoschHaleReactivityInput(BaseModel):
    """Input model for BoschHaleReactivityModule.

    Attributes:
        t_kev: t_kev input
        c_coeff: c_coeff input
        b_gamow: b_gamow input
    """
    t_kev: float = Field(..., description="t_kev input")
    c_coeff: float = Field(..., description="c_coeff input")
    b_gamow: float = Field(..., description="b_gamow input")


class BoschHaleReactivityModule(ModuleBase[BoschHaleReactivityInput, Float]):
    """TEAx module for BoschHaleReactivity calculation.

Bosch-Hale-flavored DT reactivity shape:
    sigma_v = C * exp(-B / T^(1/3)) / T^(2/3)
(NRL-formulary-style approximation, valid ~10s of keV; toy
coefficients, physically shaped so success is meaningful).
Out-of-envelope: contains an inline invocation of Exp.

Inputs:
    - t_kev: t_kev parameter
    - c_coeff: c_coeff parameter
    - b_gamow: b_gamow parameter

Outputs:
    - sigma_v: sigma_v result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:39

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/exp_spike/models/exp_toy.sysml:39

    Calculation Specification:
        sigma_v = c_coeff * Exp(-(b_gamow) / t_kev ** LiteralRationalEvaluation() / LiteralRationalEvaluation()) / t_kev ** LiteralRationalEvaluation() / LiteralRationalEvaluation()
        
Documentation:
Bosch-Hale-flavored DT reactivity shape:
    sigma_v = C * exp(-B / T^(1/3)) / T^(2/3)
(NRL-formulary-style approximation, valid ~10s of keV; toy
coefficients, physically shaped so success is meaningful).
Out-of-envelope: contains an inline invocation of Exp.

    IMPLEMENTATION: See exp_toy_tea.handwritten.exp_toy.boschhalereactivity_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "BoschHaleReactivityModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, t_kev: float, c_coeff: float, b_gamow: float    ) -> BoschHaleReactivityInput:
        """Validate inputs and fill defaults.

        Args:
            t_kev: t_kev input
            c_coeff: c_coeff input
            b_gamow: b_gamow input

        Returns:
            Validated input model
        """
        return BoschHaleReactivityInput(t_kev=t_kev, c_coeff=c_coeff, b_gamow=b_gamow)

    def run(
        self, t_kev: float, c_coeff: float, b_gamow: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            t_kev: t_kev input
            c_coeff: c_coeff input
            b_gamow: b_gamow input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(t_kev, c_coeff, b_gamow)

        # Import handwritten implementation
        from exp_toy_tea.handwritten.exp_toy.boschhalereactivity_impl import (
            run_boschhalereactivity,
        )

        # Execute implementation - returns single value
        sigma_v = run_boschhalereactivity(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(sigma_v))
