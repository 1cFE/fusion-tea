"""Matched_Pair_ComparisonModule Module Wrapper

TEAx module for Matched_Pair_Comparison calculation.

Compares the two supplied windings at one duty. rankable = all_pass_nb3sn*all_pass_rebco, where each all_pass = acceptance_pass*fit_pass*cu_pass*steel_pass*capacity_pass (acceptance_pass already requires a supported status); pair_status = status_nb3sn when both statuses are supported (non-zero), else 0; cost_difference = annualized_rebco - annualized_nb3sn; breakeven_rebco_price_per_m = rebco_price_per_m - cost_difference/(crf*rebco_element_length); breakeven_rebco_price_per_kAm = breakeven_rebco_price_per_m/(rebco_ic_tape_op/1000), per kA*m of tape critical current at the operating field and conductor temperature. Break-even prices are reported for every pair but are meaningful only when rankable = 1. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.8 (D2, D7); contract sections 7-8. **Basis**: [AGENT] cost is linear in the REBCO price per metre, so the break-even price follows from recorded outputs. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/matched_pair_comparison_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - crf_in: crf_in parameter
    - status_nb3sn_in: status_nb3sn_in parameter
    - rebco_element_length_in: rebco_element_length_in parameter
    - annualized_rebco_in: annualized_rebco_in parameter
    - annualized_nb3sn_in: annualized_nb3sn_in parameter
    - status_rebco_in: status_rebco_in parameter
    - rebco_price_per_m_in: rebco_price_per_m_in parameter
    - all_pass_nb3sn_in: all_pass_nb3sn_in parameter
    - all_pass_rebco_in: all_pass_rebco_in parameter
    - rebco_ic_tape_op_in: rebco_ic_tape_op_in parameter

Outputs:
    - breakeven_rebco_price_per_m: breakeven_rebco_price_per_m result
    - breakeven_rebco_price_per_kAm: breakeven_rebco_price_per_kAm result
    - pair_status: pair_status result
    - cost_difference: cost_difference result
    - rankable: rankable result

SysML Source: root-0/magnet_conductor_alternatives.sysml:247

SysML Source: root-0/magnet_conductor_alternatives.sysml:247

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/magnet_conductor_alternatives/matched_pair_comparison_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.primitives import Float
from magnet_materials_tea.schemas.matched_pair_comparison_output import Matched_Pair_ComparisonOutput


class Matched_Pair_ComparisonInput(BaseModel):
    """Input model for Matched_Pair_ComparisonModule.

    Attributes:
        crf_in: crf_in input
        status_nb3sn_in: status_nb3sn_in input
        rebco_element_length_in: rebco_element_length_in input
        annualized_rebco_in: annualized_rebco_in input
        annualized_nb3sn_in: annualized_nb3sn_in input
        status_rebco_in: status_rebco_in input
        rebco_price_per_m_in: rebco_price_per_m_in input
        all_pass_nb3sn_in: all_pass_nb3sn_in input
        all_pass_rebco_in: all_pass_rebco_in input
        rebco_ic_tape_op_in: rebco_ic_tape_op_in input
    """
    crf_in: float = Field(..., description="crf_in input")
    status_nb3sn_in: float = Field(..., description="status_nb3sn_in input")
    rebco_element_length_in: float = Field(..., description="rebco_element_length_in input")
    annualized_rebco_in: float = Field(..., description="annualized_rebco_in input")
    annualized_nb3sn_in: float = Field(..., description="annualized_nb3sn_in input")
    status_rebco_in: float = Field(..., description="status_rebco_in input")
    rebco_price_per_m_in: float = Field(..., description="rebco_price_per_m_in input")
    all_pass_nb3sn_in: float = Field(..., description="all_pass_nb3sn_in input")
    all_pass_rebco_in: float = Field(..., description="all_pass_rebco_in input")
    rebco_ic_tape_op_in: float = Field(..., description="rebco_ic_tape_op_in input")


class Matched_Pair_ComparisonModule(ModuleBase[Matched_Pair_ComparisonInput, Matched_Pair_ComparisonOutput]):
    """TEAx module for Matched_Pair_Comparison calculation.

Compares the two supplied windings at one duty. rankable = all_pass_nb3sn*all_pass_rebco, where each all_pass = acceptance_pass*fit_pass*cu_pass*steel_pass*capacity_pass (acceptance_pass already requires a supported status); pair_status = status_nb3sn when both statuses are supported (non-zero), else 0; cost_difference = annualized_rebco - annualized_nb3sn; breakeven_rebco_price_per_m = rebco_price_per_m - cost_difference/(crf*rebco_element_length); breakeven_rebco_price_per_kAm = breakeven_rebco_price_per_m/(rebco_ic_tape_op/1000), per kA*m of tape critical current at the operating field and conductor temperature. Break-even prices are reported for every pair but are meaningful only when rankable = 1. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.8 (D2, D7); contract sections 7-8. **Basis**: [AGENT] cost is linear in the REBCO price per metre, so the break-even price follows from recorded outputs. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/matched_pair_comparison_impl.py. **Last Updated**: 2026-09-29

Inputs:
    - crf_in: crf_in parameter
    - status_nb3sn_in: status_nb3sn_in parameter
    - rebco_element_length_in: rebco_element_length_in parameter
    - annualized_rebco_in: annualized_rebco_in parameter
    - annualized_nb3sn_in: annualized_nb3sn_in parameter
    - status_rebco_in: status_rebco_in parameter
    - rebco_price_per_m_in: rebco_price_per_m_in parameter
    - all_pass_nb3sn_in: all_pass_nb3sn_in parameter
    - all_pass_rebco_in: all_pass_rebco_in parameter
    - rebco_ic_tape_op_in: rebco_ic_tape_op_in parameter

Outputs:
    - breakeven_rebco_price_per_m: breakeven_rebco_price_per_m result
    - breakeven_rebco_price_per_kAm: breakeven_rebco_price_per_kAm result
    - pair_status: pair_status result
    - cost_difference: cost_difference result
    - rankable: rankable result

SysML Source: root-0/magnet_conductor_alternatives.sysml:247

    SysML Source: root-0/magnet_conductor_alternatives.sysml:247

    Calculation Specification:
        annualized_nb3sn_in = 0.0
        annualized_rebco_in = 0.0
        all_pass_nb3sn_in = 0.0
        all_pass_rebco_in = 0.0
        status_nb3sn_in = 0.0
        status_rebco_in = 0.0
        rebco_element_length_in = 1.0
        rebco_price_per_m_in = 0.0
        rebco_ic_tape_op_in = 1.0
        crf_in = 1.0
        
Documentation:
Compares the two supplied windings at one duty. rankable = all_pass_nb3sn*all_pass_rebco, where each all_pass = acceptance_pass*fit_pass*cu_pass*steel_pass*capacity_pass (acceptance_pass already requires a supported status); pair_status = status_nb3sn when both statuses are supported (non-zero), else 0; cost_difference = annualized_rebco - annualized_nb3sn; breakeven_rebco_price_per_m = rebco_price_per_m - cost_difference/(crf*rebco_element_length); breakeven_rebco_price_per_kAm = breakeven_rebco_price_per_m/(rebco_ic_tape_op/1000), per kA*m of tape critical current at the operating field and conductor temperature. Break-even prices are reported for every pair but are meaningful only when rankable = 1. **Source**: work/active/WI-099_magnet-conductor-alternatives/design.md **Reference**: section 2.8 (D2, D7); contract sections 7-8. **Basis**: [AGENT] cost is linear in the REBCO price per metre, so the break-even price follows from recorded outputs. Body: exploration/magnet_materials/bodies/magnet_conductor_alternatives/matched_pair_comparison_impl.py. **Last Updated**: 2026-09-29

    IMPLEMENTATION: See magnet_materials_tea.handwritten.magnet_conductor_alternatives.matched_pair_comparison_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts breakeven_rebco_price_per_m, breakeven_rebco_price_per_kAm, pair_status, cost_difference, rankable fields to separate channels.
    """

    name: str = "Matched_Pair_ComparisonModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, crf_in: float, status_nb3sn_in: float, rebco_element_length_in: float, annualized_rebco_in: float, annualized_nb3sn_in: float, status_rebco_in: float, rebco_price_per_m_in: float, all_pass_nb3sn_in: float, all_pass_rebco_in: float, rebco_ic_tape_op_in: float    ) -> Matched_Pair_ComparisonInput:
        """Validate inputs and fill defaults.

        Args:
            crf_in: crf_in input
            status_nb3sn_in: status_nb3sn_in input
            rebco_element_length_in: rebco_element_length_in input
            annualized_rebco_in: annualized_rebco_in input
            annualized_nb3sn_in: annualized_nb3sn_in input
            status_rebco_in: status_rebco_in input
            rebco_price_per_m_in: rebco_price_per_m_in input
            all_pass_nb3sn_in: all_pass_nb3sn_in input
            all_pass_rebco_in: all_pass_rebco_in input
            rebco_ic_tape_op_in: rebco_ic_tape_op_in input

        Returns:
            Validated input model
        """
        return Matched_Pair_ComparisonInput(crf_in=crf_in, status_nb3sn_in=status_nb3sn_in, rebco_element_length_in=rebco_element_length_in, annualized_rebco_in=annualized_rebco_in, annualized_nb3sn_in=annualized_nb3sn_in, status_rebco_in=status_rebco_in, rebco_price_per_m_in=rebco_price_per_m_in, all_pass_nb3sn_in=all_pass_nb3sn_in, all_pass_rebco_in=all_pass_rebco_in, rebco_ic_tape_op_in=rebco_ic_tape_op_in)

    def run(
        self, crf_in: float, status_nb3sn_in: float, rebco_element_length_in: float, annualized_rebco_in: float, annualized_nb3sn_in: float, status_rebco_in: float, rebco_price_per_m_in: float, all_pass_nb3sn_in: float, all_pass_rebco_in: float, rebco_ic_tape_op_in: float    ) -> ModuleResult[Matched_Pair_ComparisonOutput]:
        """Execute calculation.

        Args:
            crf_in: crf_in input
            status_nb3sn_in: status_nb3sn_in input
            rebco_element_length_in: rebco_element_length_in input
            annualized_rebco_in: annualized_rebco_in input
            annualized_nb3sn_in: annualized_nb3sn_in input
            status_rebco_in: status_rebco_in input
            rebco_price_per_m_in: rebco_price_per_m_in input
            all_pass_nb3sn_in: all_pass_nb3sn_in input
            all_pass_rebco_in: all_pass_rebco_in input
            rebco_ic_tape_op_in: rebco_ic_tape_op_in input

        Returns:
            Module result with Matched_Pair_ComparisonOutput (breakeven_rebco_price_per_m, breakeven_rebco_price_per_kAm, pair_status, cost_difference, rankable)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(crf_in, status_nb3sn_in, rebco_element_length_in, annualized_rebco_in, annualized_nb3sn_in, status_rebco_in, rebco_price_per_m_in, all_pass_nb3sn_in, all_pass_rebco_in, rebco_ic_tape_op_in)

        # Import handwritten implementation
        from magnet_materials_tea.handwritten.magnet_conductor_alternatives.matched_pair_comparison_impl import (
            run_matched_pair_comparison,
        )

        # Execute implementation - returns tuple of values
        breakeven_rebco_price_per_m, breakeven_rebco_price_per_kAm, pair_status, cost_difference, rankable = run_matched_pair_comparison(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Matched_Pair_ComparisonOutput(
                breakeven_rebco_price_per_m=breakeven_rebco_price_per_m,
                breakeven_rebco_price_per_kAm=breakeven_rebco_price_per_kAm,
                pair_status=pair_status,
                cost_difference=cost_difference,
                rankable=rankable,
            )
        )
