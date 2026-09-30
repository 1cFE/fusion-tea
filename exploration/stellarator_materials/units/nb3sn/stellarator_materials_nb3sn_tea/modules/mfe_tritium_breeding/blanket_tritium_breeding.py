"""Blanket_Tritium_BreedingModule Module Wrapper

TEAx module for Blanket_Tritium_Breeding calculation.

Continuous-energy-transport response interpolation for an explicitly fixed material/source scenario. The supported lever is breeder thickness [m]; all other geometry inputs [m, except dimensionless kappa] are applicability guards. Fixed enrichment and material/source metadata belong to the immutable response-data manifest, not free public inputs. The typed manual implementation checks finite inputs, the released table domain and every fixed geometry coordinate; no extrapolation or clamping. Table release and independent withheld validation are prerequisites for implementation completion.
Outputs are Li6/Li7 production and total tritium atoms per emitted fusion neutron, total Monte Carlo standard error, interpolation allowance, numerical lower estimate and defined_flag (exactly 0 or 1). The statistical multiplier and allowance are declared in the released manifest. The lower estimate is not a physical confidence bound. Unsupported inputs return zero numerical carriers and defined_flag=0; those carriers are undefined, not physical zero breeding or proof of deficit. Shaped-stellarator bias and physical scenario uncertainties remain separate.
*Source**: work/active/WI-066_computed-tritium-breeding/spec.md
*Reference**: work/active/WI-066_computed-tritium-breeding/design.md; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
*Last Updated**: 2026-09-18

Inputs:
    - vessel_t_in: vessel_t_in parameter
    - reflector_t_in: reflector_t_in parameter
    - firstwall_t_in: firstwall_t_in parameter
    - vacuum_t_in: vacuum_t_in parameter
    - kappa_in: kappa_in parameter
    - structure_t_in: structure_t_in parameter
    - blanket_t_in: blanket_t_in parameter
    - R_in: R_in parameter
    - gap1_t_in: gap1_t_in parameter
    - a_in: a_in parameter
    - ht_shield_t_in: ht_shield_t_in parameter

Outputs:
    - interpolation_allowance: interpolation_allowance result
    - tbr_lower: tbr_lower result
    - defined_flag: defined_flag result
    - tbr_li6: tbr_li6 result
    - tbr_std_error: tbr_std_error result
    - tbr_li7: tbr_li7 result
    - tbr_mean: tbr_mean result

SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:4

SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_tritium_breeding/blanket_tritium_breeding_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.blanket_tritium_breeding_output import Blanket_Tritium_BreedingOutput


class Blanket_Tritium_BreedingInput(BaseModel):
    """Input model for Blanket_Tritium_BreedingModule.

    Attributes:
        vessel_t_in: vessel_t_in input
        reflector_t_in: reflector_t_in input
        firstwall_t_in: firstwall_t_in input
        vacuum_t_in: vacuum_t_in input
        kappa_in: kappa_in input
        structure_t_in: structure_t_in input
        blanket_t_in: blanket_t_in input
        R_in: R_in input
        gap1_t_in: gap1_t_in input
        a_in: a_in input
        ht_shield_t_in: ht_shield_t_in input
    """
    vessel_t_in: float = Field(..., description="vessel_t_in input")
    reflector_t_in: float = Field(..., description="reflector_t_in input")
    firstwall_t_in: float = Field(..., description="firstwall_t_in input")
    vacuum_t_in: float = Field(..., description="vacuum_t_in input")
    kappa_in: float = Field(..., description="kappa_in input")
    structure_t_in: float = Field(..., description="structure_t_in input")
    blanket_t_in: float = Field(..., description="blanket_t_in input")
    R_in: float = Field(..., description="R_in input")
    gap1_t_in: float = Field(..., description="gap1_t_in input")
    a_in: float = Field(..., description="a_in input")
    ht_shield_t_in: float = Field(..., description="ht_shield_t_in input")


class Blanket_Tritium_BreedingModule(ModuleBase[Blanket_Tritium_BreedingInput, Blanket_Tritium_BreedingOutput]):
    """TEAx module for Blanket_Tritium_Breeding calculation.

Continuous-energy-transport response interpolation for an explicitly fixed material/source scenario. The supported lever is breeder thickness [m]; all other geometry inputs [m, except dimensionless kappa] are applicability guards. Fixed enrichment and material/source metadata belong to the immutable response-data manifest, not free public inputs. The typed manual implementation checks finite inputs, the released table domain and every fixed geometry coordinate; no extrapolation or clamping. Table release and independent withheld validation are prerequisites for implementation completion.
Outputs are Li6/Li7 production and total tritium atoms per emitted fusion neutron, total Monte Carlo standard error, interpolation allowance, numerical lower estimate and defined_flag (exactly 0 or 1). The statistical multiplier and allowance are declared in the released manifest. The lower estimate is not a physical confidence bound. Unsupported inputs return zero numerical carriers and defined_flag=0; those carriers are undefined, not physical zero breeding or proof of deficit. Shaped-stellarator bias and physical scenario uncertainties remain separate.
*Source**: work/active/WI-066_computed-tritium-breeding/spec.md
*Reference**: work/active/WI-066_computed-tritium-breeding/design.md; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
*Last Updated**: 2026-09-18

Inputs:
    - vessel_t_in: vessel_t_in parameter
    - reflector_t_in: reflector_t_in parameter
    - firstwall_t_in: firstwall_t_in parameter
    - vacuum_t_in: vacuum_t_in parameter
    - kappa_in: kappa_in parameter
    - structure_t_in: structure_t_in parameter
    - blanket_t_in: blanket_t_in parameter
    - R_in: R_in parameter
    - gap1_t_in: gap1_t_in parameter
    - a_in: a_in parameter
    - ht_shield_t_in: ht_shield_t_in parameter

Outputs:
    - interpolation_allowance: interpolation_allowance result
    - tbr_lower: tbr_lower result
    - defined_flag: defined_flag result
    - tbr_li6: tbr_li6 result
    - tbr_std_error: tbr_std_error result
    - tbr_li7: tbr_li7 result
    - tbr_mean: tbr_mean result

SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:4

    SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:4

    Calculation Specification:
        See documentation:
Continuous-energy-transport response interpolation for an explicitly fixed material/source scenario. The supported lever is breeder thickness [m]; all other geometry inputs [m, except dimensionless kappa] are applicability guards. Fixed enrichment and material/source metadata belong to the immutable response-data manifest, not free public inputs. The typed manual implementation checks finite inputs, the released table domain and every fixed geometry coordinate; no extrapolation or clamping. Table release and independent withheld validation are prerequisites for implementation completion.
Outputs are Li6/Li7 production and total tritium atoms per emitted fusion neutron, total Monte Carlo standard error, interpolation allowance, numerical lower estimate and defined_flag (exactly 0 or 1). The statistical multiplier and allowance are declared in the released manifest. The lower estimate is not a physical confidence bound. Unsupported inputs return zero numerical carriers and defined_flag=0; those carriers are undefined, not physical zero breeding or proof of deficit. Shaped-stellarator bias and physical scenario uncertainties remain separate.
*Source**: work/active/WI-066_computed-tritium-breeding/spec.md
*Reference**: work/active/WI-066_computed-tritium-breeding/design.md; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
*Last Updated**: 2026-09-18

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_tritium_breeding.blanket_tritium_breeding_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts interpolation_allowance, tbr_lower, defined_flag, tbr_li6, tbr_std_error, tbr_li7, tbr_mean fields to separate channels.
    """

    name: str = "Blanket_Tritium_BreedingModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, vessel_t_in: float, reflector_t_in: float, firstwall_t_in: float, vacuum_t_in: float, kappa_in: float, structure_t_in: float, blanket_t_in: float, R_in: float, gap1_t_in: float, a_in: float, ht_shield_t_in: float    ) -> Blanket_Tritium_BreedingInput:
        """Validate inputs and fill defaults.

        Args:
            vessel_t_in: vessel_t_in input
            reflector_t_in: reflector_t_in input
            firstwall_t_in: firstwall_t_in input
            vacuum_t_in: vacuum_t_in input
            kappa_in: kappa_in input
            structure_t_in: structure_t_in input
            blanket_t_in: blanket_t_in input
            R_in: R_in input
            gap1_t_in: gap1_t_in input
            a_in: a_in input
            ht_shield_t_in: ht_shield_t_in input

        Returns:
            Validated input model
        """
        return Blanket_Tritium_BreedingInput(vessel_t_in=vessel_t_in, reflector_t_in=reflector_t_in, firstwall_t_in=firstwall_t_in, vacuum_t_in=vacuum_t_in, kappa_in=kappa_in, structure_t_in=structure_t_in, blanket_t_in=blanket_t_in, R_in=R_in, gap1_t_in=gap1_t_in, a_in=a_in, ht_shield_t_in=ht_shield_t_in)

    def run(
        self, vessel_t_in: float, reflector_t_in: float, firstwall_t_in: float, vacuum_t_in: float, kappa_in: float, structure_t_in: float, blanket_t_in: float, R_in: float, gap1_t_in: float, a_in: float, ht_shield_t_in: float    ) -> ModuleResult[Blanket_Tritium_BreedingOutput]:
        """Execute calculation.

        Args:
            vessel_t_in: vessel_t_in input
            reflector_t_in: reflector_t_in input
            firstwall_t_in: firstwall_t_in input
            vacuum_t_in: vacuum_t_in input
            kappa_in: kappa_in input
            structure_t_in: structure_t_in input
            blanket_t_in: blanket_t_in input
            R_in: R_in input
            gap1_t_in: gap1_t_in input
            a_in: a_in input
            ht_shield_t_in: ht_shield_t_in input

        Returns:
            Module result with Blanket_Tritium_BreedingOutput (interpolation_allowance, tbr_lower, defined_flag, tbr_li6, tbr_std_error, tbr_li7, tbr_mean)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(vessel_t_in, reflector_t_in, firstwall_t_in, vacuum_t_in, kappa_in, structure_t_in, blanket_t_in, R_in, gap1_t_in, a_in, ht_shield_t_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_tritium_breeding.blanket_tritium_breeding_impl import (
            run_blanket_tritium_breeding,
        )

        # Execute implementation - returns tuple of values
        interpolation_allowance, tbr_lower, defined_flag, tbr_li6, tbr_std_error, tbr_li7, tbr_mean = run_blanket_tritium_breeding(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Blanket_Tritium_BreedingOutput(
                interpolation_allowance=interpolation_allowance,
                tbr_lower=tbr_lower,
                defined_flag=defined_flag,
                tbr_li6=tbr_li6,
                tbr_std_error=tbr_std_error,
                tbr_li7=tbr_li7,
                tbr_mean=tbr_mean,
            )
        )
