"""Volume_Averaged_BetaModule Module Wrapper

TEAx module for Volume_Averaged_Beta calculation.

Volume-averaged thermal plasma beta [1] from the plant's one
volume-averaged thermal pressure and the axis-averaged field (WI-030;
WI-042: reads <p> instead of recomputing it).

  beta = 2 * mu0 * <p> / B^2

<p> [Pa] is 'Plasma Sustainment'.p_avg -- the pressure average over
the source's own profile rules (power-law fuel and temperature
profiles, the helium ash on the fusion-rate profile by Eq. A.5
pointwise, electrons by quasi-neutrality), the same integral that
gives W_th = 3/2 <p> V there. One pressure integral, two consumers:
beta * B^2 * 1.5 * V / (2 mu0) = W_th to float precision, always.
Thermal only: fast-particle pressure is excluded.

Before WI-042 this calc carried a second copy of the pressure average
in closed form, Sigma_s n_s0 T_s0 / (1 + alpha_n,s + alpha_T) over
power-law profiles with the ash at the fuel exponent and the electrons
at a bound exponent; that form is now exactly the no-ash special case
the sustainment calc reduces to (its DORMANT CASE), and is not an
executable path here.

Concept-agnostic: every MFE instance carries the sustainment chain
(WI-037), so every instance has a <p> to read; B enters the physics
here, not only the magnet cost (mfe_magnet_cost.sysml).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: tokamak.py:36-40 (MU_0 1.25663706127e-6 -- this calc keeps the
model's 1.25663706212e-6 from mfe_magnet_cost.sysml:41, 7e-10 apart);
tokamak.py:117-126 (compute_beta_N: electron + ion pressure over B^2
-- NOTE its mu0*n_e*(T_e + n_i T_i)/B^2 is half the standard
2*mu0*p/B^2 used here); images/page_009_table_0.png (Table 5: vol.
av. beta 2.76 % / 2.81 %, the cross-check -- with the caveat of goal
stored-energy-basis L-002: the printed 2.76 % is inconsistent with
the printed W at the only field the paper names, 9.0 T; from the
one <p> the model reads 2.53 % at point A, thermal)
*Basis**: beta = 2*mu0*<p>/B^2 with <p> the volume-averaged thermal
pressure of all species over the source's profile rules; MFE-generic

Inputs:
    - mu0: mu0 parameter
    - B_in: B_in parameter
    - p_avg_in: p_avg_in parameter

Outputs:
    - beta: beta result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:351

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:351

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/volume_averaged_beta_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Volume_Averaged_BetaInput(BaseModel):
    """Input model for Volume_Averaged_BetaModule.

    Attributes:
        mu0: mu0 input
        B_in: B_in input
        p_avg_in: p_avg_in input
    """
    mu0: float = Field(..., description="mu0 input")
    B_in: float = Field(..., description="B_in input")
    p_avg_in: float = Field(..., description="p_avg_in input")


class Volume_Averaged_BetaModule(ModuleBase[Volume_Averaged_BetaInput, Float]):
    """TEAx module for Volume_Averaged_Beta calculation.

Volume-averaged thermal plasma beta [1] from the plant's one
volume-averaged thermal pressure and the axis-averaged field (WI-030;
WI-042: reads <p> instead of recomputing it).

  beta = 2 * mu0 * <p> / B^2

<p> [Pa] is 'Plasma Sustainment'.p_avg -- the pressure average over
the source's own profile rules (power-law fuel and temperature
profiles, the helium ash on the fusion-rate profile by Eq. A.5
pointwise, electrons by quasi-neutrality), the same integral that
gives W_th = 3/2 <p> V there. One pressure integral, two consumers:
beta * B^2 * 1.5 * V / (2 mu0) = W_th to float precision, always.
Thermal only: fast-particle pressure is excluded.

Before WI-042 this calc carried a second copy of the pressure average
in closed form, Sigma_s n_s0 T_s0 / (1 + alpha_n,s + alpha_T) over
power-law profiles with the ash at the fuel exponent and the electrons
at a bound exponent; that form is now exactly the no-ash special case
the sustainment calc reduces to (its DORMANT CASE), and is not an
executable path here.

Concept-agnostic: every MFE instance carries the sustainment chain
(WI-037), so every instance has a <p> to read; B enters the physics
here, not only the magnet cost (mfe_magnet_cost.sysml).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: tokamak.py:36-40 (MU_0 1.25663706127e-6 -- this calc keeps the
model's 1.25663706212e-6 from mfe_magnet_cost.sysml:41, 7e-10 apart);
tokamak.py:117-126 (compute_beta_N: electron + ion pressure over B^2
-- NOTE its mu0*n_e*(T_e + n_i T_i)/B^2 is half the standard
2*mu0*p/B^2 used here); images/page_009_table_0.png (Table 5: vol.
av. beta 2.76 % / 2.81 %, the cross-check -- with the caveat of goal
stored-energy-basis L-002: the printed 2.76 % is inconsistent with
the printed W at the only field the paper names, 9.0 T; from the
one <p> the model reads 2.53 % at point A, thermal)
*Basis**: beta = 2*mu0*<p>/B^2 with <p> the volume-averaged thermal
pressure of all species over the source's profile rules; MFE-generic

Inputs:
    - mu0: mu0 parameter
    - B_in: B_in parameter
    - p_avg_in: p_avg_in parameter

Outputs:
    - beta: beta result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:351

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:351

    Calculation Specification:
        mu0 = 1.25663706212e-06
        beta = 2.0 * mu0 * p_avg_in / B_in ** 2
        
Documentation:
Volume-averaged thermal plasma beta [1] from the plant's one
volume-averaged thermal pressure and the axis-averaged field (WI-030;
WI-042: reads <p> instead of recomputing it).

  beta = 2 * mu0 * <p> / B^2

<p> [Pa] is 'Plasma Sustainment'.p_avg -- the pressure average over
the source's own profile rules (power-law fuel and temperature
profiles, the helium ash on the fusion-rate profile by Eq. A.5
pointwise, electrons by quasi-neutrality), the same integral that
gives W_th = 3/2 <p> V there. One pressure integral, two consumers:
beta * B^2 * 1.5 * V / (2 mu0) = W_th to float precision, always.
Thermal only: fast-particle pressure is excluded.

Before WI-042 this calc carried a second copy of the pressure average
in closed form, Sigma_s n_s0 T_s0 / (1 + alpha_n,s + alpha_T) over
power-law profiles with the ash at the fuel exponent and the electrons
at a bound exponent; that form is now exactly the no-ash special case
the sustainment calc reduces to (its DORMANT CASE), and is not an
executable path here.

Concept-agnostic: every MFE instance carries the sustainment chain
(WI-037), so every instance has a <p> to read; B enters the physics
here, not only the magnet cost (mfe_magnet_cost.sysml).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: tokamak.py:36-40 (MU_0 1.25663706127e-6 -- this calc keeps the
model's 1.25663706212e-6 from mfe_magnet_cost.sysml:41, 7e-10 apart);
tokamak.py:117-126 (compute_beta_N: electron + ion pressure over B^2
-- NOTE its mu0*n_e*(T_e + n_i T_i)/B^2 is half the standard
2*mu0*p/B^2 used here); images/page_009_table_0.png (Table 5: vol.
av. beta 2.76 % / 2.81 %, the cross-check -- with the caveat of goal
stored-energy-basis L-002: the printed 2.76 % is inconsistent with
the printed W at the only field the paper names, 9.0 T; from the
one <p> the model reads 2.53 % at point A, thermal)
*Basis**: beta = 2*mu0*<p>/B^2 with <p> the volume-averaged thermal
pressure of all species over the source's profile rules; MFE-generic

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.volume_averaged_beta_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Volume_Averaged_BetaModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, mu0: float, B_in: float, p_avg_in: float    ) -> Volume_Averaged_BetaInput:
        """Validate inputs and fill defaults.

        Args:
            mu0: mu0 input
            B_in: B_in input
            p_avg_in: p_avg_in input

        Returns:
            Validated input model
        """
        return Volume_Averaged_BetaInput(mu0=mu0, B_in=B_in, p_avg_in=p_avg_in)

    def run(
        self, mu0: float, B_in: float, p_avg_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            mu0: mu0 input
            B_in: B_in input
            p_avg_in: p_avg_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(mu0, B_in, p_avg_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.volume_averaged_beta_impl import (
            run_volume_averaged_beta,
        )

        # Execute implementation - returns single value
        beta = run_volume_averaged_beta(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(beta))
