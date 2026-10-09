"""Tritium_Breeding_AdequacyModule Module Wrapper

TEAx module for Tritium_Breeding_Adequacy calculation.

Conditional fuel-account adequacy. Typed manual completion validates finite quantities; positive burn rate; burn fraction and extraction efficiency in (0,1]; exhaust recovery in [0,1]; nonnegative decay constant, inventory, growth and loss; positive finite design/fuel requirements; and the exact applicability flag. required_tbr=max(tbr_floor_in,tbr_required_in), without adding the same reserve twice. design_margin=tbr_mean_in-tbr_floor_in; fuel_margin=tbr_mean_in-tbr_required_in; numerical_margin=tbr_lower_in-required_tbr. Production=tbr_mean_in*burn_rate_in; extracted_supply=eta_extract_in*production; extraction_loss=(1-eta_extract_in)*production; recycle_loss=loss_rate_in; decay=lambda_T_in*I_total_in; stock_growth=G_stock_in; balance=extracted_supply-burn_rate_in-recycle_loss-decay-stock_growth [all rates atoms/s]. Extraction acts on breeder supply only. Check finite intermediates, consistency of required breeding with its source account, and nonnegative physical production.
defined_flag is exactly 0 or 1. It marks all breeding-derived outputs together. Invalid applicability or account inputs fail the screen even if a malformed requirement is nonpositive. A valid requirement may remain reported when breeding is undefined, but breeding-derived numerical carriers are zero and are not physical margins, lower bounds or deficits. Raw Fuel Cycle Flows margin has this same applicability condition in a transport-driven instance. The retained 0.99 exhaust recovery is a conditional cost-derived reading, not isotope-recovery evidence; unity extraction and zero inventory/growth remain optimistic explicit assumptions.
*Source**: work/active/WI-066_computed-tritium-breeding/spec.md
*Reference**: models/library/analyses/mfe_fuel_cycle.sysml; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
*Last Updated**: 2026-09-18

Inputs:
    - loss_rate_in: loss_rate_in parameter
    - I_total_in: I_total_in parameter
    - eta_extract_in: eta_extract_in parameter
    - burn_rate_in: burn_rate_in parameter
    - tbr_lower_in: tbr_lower_in parameter
    - defined_in: defined_in parameter
    - tbr_floor_in: tbr_floor_in parameter
    - G_stock_in: G_stock_in parameter
    - lambda_T_in: lambda_T_in parameter
    - tbr_mean_in: tbr_mean_in parameter
    - t_recycle_in: t_recycle_in parameter
    - tbr_required_in: tbr_required_in parameter
    - burn_fraction_in: burn_fraction_in parameter

Outputs:
    - design_margin: design_margin result
    - decay_rate: decay_rate result
    - fuel_margin: fuel_margin result
    - extracted_supply_rate: extracted_supply_rate result
    - recycle_loss_rate: recycle_loss_rate result
    - defined_flag: defined_flag result
    - required_tbr: required_tbr result
    - balance_rate: balance_rate result
    - extraction_loss_rate: extraction_loss_rate result
    - stock_growth_rate: stock_growth_rate result
    - numerical_margin: numerical_margin result
    - production_rate: production_rate result

SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:30

SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:30

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_tritium_breeding/tritium_breeding_adequacy_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.tritium_breeding_adequacy_output import Tritium_Breeding_AdequacyOutput


class Tritium_Breeding_AdequacyInput(BaseModel):
    """Input model for Tritium_Breeding_AdequacyModule.

    Attributes:
        loss_rate_in: loss_rate_in input
        I_total_in: I_total_in input
        eta_extract_in: eta_extract_in input
        burn_rate_in: burn_rate_in input
        tbr_lower_in: tbr_lower_in input
        defined_in: defined_in input
        tbr_floor_in: tbr_floor_in input
        G_stock_in: G_stock_in input
        lambda_T_in: lambda_T_in input
        tbr_mean_in: tbr_mean_in input
        t_recycle_in: t_recycle_in input
        tbr_required_in: tbr_required_in input
        burn_fraction_in: burn_fraction_in input
    """
    loss_rate_in: float = Field(..., description="loss_rate_in input")
    I_total_in: float = Field(..., description="I_total_in input")
    eta_extract_in: float = Field(..., description="eta_extract_in input")
    burn_rate_in: float = Field(..., description="burn_rate_in input")
    tbr_lower_in: float = Field(..., description="tbr_lower_in input")
    defined_in: float = Field(..., description="defined_in input")
    tbr_floor_in: float = Field(..., description="tbr_floor_in input")
    G_stock_in: float = Field(..., description="G_stock_in input")
    lambda_T_in: float = Field(..., description="lambda_T_in input")
    tbr_mean_in: float = Field(..., description="tbr_mean_in input")
    t_recycle_in: float = Field(..., description="t_recycle_in input")
    tbr_required_in: float = Field(..., description="tbr_required_in input")
    burn_fraction_in: float = Field(..., description="burn_fraction_in input")


class Tritium_Breeding_AdequacyModule(ModuleBase[Tritium_Breeding_AdequacyInput, Tritium_Breeding_AdequacyOutput]):
    """TEAx module for Tritium_Breeding_Adequacy calculation.

Conditional fuel-account adequacy. Typed manual completion validates finite quantities; positive burn rate; burn fraction and extraction efficiency in (0,1]; exhaust recovery in [0,1]; nonnegative decay constant, inventory, growth and loss; positive finite design/fuel requirements; and the exact applicability flag. required_tbr=max(tbr_floor_in,tbr_required_in), without adding the same reserve twice. design_margin=tbr_mean_in-tbr_floor_in; fuel_margin=tbr_mean_in-tbr_required_in; numerical_margin=tbr_lower_in-required_tbr. Production=tbr_mean_in*burn_rate_in; extracted_supply=eta_extract_in*production; extraction_loss=(1-eta_extract_in)*production; recycle_loss=loss_rate_in; decay=lambda_T_in*I_total_in; stock_growth=G_stock_in; balance=extracted_supply-burn_rate_in-recycle_loss-decay-stock_growth [all rates atoms/s]. Extraction acts on breeder supply only. Check finite intermediates, consistency of required breeding with its source account, and nonnegative physical production.
defined_flag is exactly 0 or 1. It marks all breeding-derived outputs together. Invalid applicability or account inputs fail the screen even if a malformed requirement is nonpositive. A valid requirement may remain reported when breeding is undefined, but breeding-derived numerical carriers are zero and are not physical margins, lower bounds or deficits. Raw Fuel Cycle Flows margin has this same applicability condition in a transport-driven instance. The retained 0.99 exhaust recovery is a conditional cost-derived reading, not isotope-recovery evidence; unity extraction and zero inventory/growth remain optimistic explicit assumptions.
*Source**: work/active/WI-066_computed-tritium-breeding/spec.md
*Reference**: models/library/analyses/mfe_fuel_cycle.sysml; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
*Last Updated**: 2026-09-18

Inputs:
    - loss_rate_in: loss_rate_in parameter
    - I_total_in: I_total_in parameter
    - eta_extract_in: eta_extract_in parameter
    - burn_rate_in: burn_rate_in parameter
    - tbr_lower_in: tbr_lower_in parameter
    - defined_in: defined_in parameter
    - tbr_floor_in: tbr_floor_in parameter
    - G_stock_in: G_stock_in parameter
    - lambda_T_in: lambda_T_in parameter
    - tbr_mean_in: tbr_mean_in parameter
    - t_recycle_in: t_recycle_in parameter
    - tbr_required_in: tbr_required_in parameter
    - burn_fraction_in: burn_fraction_in parameter

Outputs:
    - design_margin: design_margin result
    - decay_rate: decay_rate result
    - fuel_margin: fuel_margin result
    - extracted_supply_rate: extracted_supply_rate result
    - recycle_loss_rate: recycle_loss_rate result
    - defined_flag: defined_flag result
    - required_tbr: required_tbr result
    - balance_rate: balance_rate result
    - extraction_loss_rate: extraction_loss_rate result
    - stock_growth_rate: stock_growth_rate result
    - numerical_margin: numerical_margin result
    - production_rate: production_rate result

SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:30

    SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:30

    Calculation Specification:
        See documentation:
Conditional fuel-account adequacy. Typed manual completion validates finite quantities; positive burn rate; burn fraction and extraction efficiency in (0,1]; exhaust recovery in [0,1]; nonnegative decay constant, inventory, growth and loss; positive finite design/fuel requirements; and the exact applicability flag. required_tbr=max(tbr_floor_in,tbr_required_in), without adding the same reserve twice. design_margin=tbr_mean_in-tbr_floor_in; fuel_margin=tbr_mean_in-tbr_required_in; numerical_margin=tbr_lower_in-required_tbr. Production=tbr_mean_in*burn_rate_in; extracted_supply=eta_extract_in*production; extraction_loss=(1-eta_extract_in)*production; recycle_loss=loss_rate_in; decay=lambda_T_in*I_total_in; stock_growth=G_stock_in; balance=extracted_supply-burn_rate_in-recycle_loss-decay-stock_growth [all rates atoms/s]. Extraction acts on breeder supply only. Check finite intermediates, consistency of required breeding with its source account, and nonnegative physical production.
defined_flag is exactly 0 or 1. It marks all breeding-derived outputs together. Invalid applicability or account inputs fail the screen even if a malformed requirement is nonpositive. A valid requirement may remain reported when breeding is undefined, but breeding-derived numerical carriers are zero and are not physical margins, lower bounds or deficits. Raw Fuel Cycle Flows margin has this same applicability condition in a transport-driven instance. The retained 0.99 exhaust recovery is a conditional cost-derived reading, not isotope-recovery evidence; unity extraction and zero inventory/growth remain optimistic explicit assumptions.
*Source**: work/active/WI-066_computed-tritium-breeding/spec.md
*Reference**: models/library/analyses/mfe_fuel_cycle.sysml; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
*Last Updated**: 2026-09-18

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_tritium_breeding.tritium_breeding_adequacy_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts design_margin, decay_rate, fuel_margin, extracted_supply_rate, recycle_loss_rate, defined_flag, required_tbr, balance_rate, extraction_loss_rate, stock_growth_rate, numerical_margin, production_rate fields to separate channels.
    """

    name: str = "Tritium_Breeding_AdequacyModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, loss_rate_in: float, I_total_in: float, eta_extract_in: float, burn_rate_in: float, tbr_lower_in: float, defined_in: float, tbr_floor_in: float, G_stock_in: float, lambda_T_in: float, tbr_mean_in: float, t_recycle_in: float, tbr_required_in: float, burn_fraction_in: float    ) -> Tritium_Breeding_AdequacyInput:
        """Validate inputs and fill defaults.

        Args:
            loss_rate_in: loss_rate_in input
            I_total_in: I_total_in input
            eta_extract_in: eta_extract_in input
            burn_rate_in: burn_rate_in input
            tbr_lower_in: tbr_lower_in input
            defined_in: defined_in input
            tbr_floor_in: tbr_floor_in input
            G_stock_in: G_stock_in input
            lambda_T_in: lambda_T_in input
            tbr_mean_in: tbr_mean_in input
            t_recycle_in: t_recycle_in input
            tbr_required_in: tbr_required_in input
            burn_fraction_in: burn_fraction_in input

        Returns:
            Validated input model
        """
        return Tritium_Breeding_AdequacyInput(loss_rate_in=loss_rate_in, I_total_in=I_total_in, eta_extract_in=eta_extract_in, burn_rate_in=burn_rate_in, tbr_lower_in=tbr_lower_in, defined_in=defined_in, tbr_floor_in=tbr_floor_in, G_stock_in=G_stock_in, lambda_T_in=lambda_T_in, tbr_mean_in=tbr_mean_in, t_recycle_in=t_recycle_in, tbr_required_in=tbr_required_in, burn_fraction_in=burn_fraction_in)

    def run(
        self, loss_rate_in: float, I_total_in: float, eta_extract_in: float, burn_rate_in: float, tbr_lower_in: float, defined_in: float, tbr_floor_in: float, G_stock_in: float, lambda_T_in: float, tbr_mean_in: float, t_recycle_in: float, tbr_required_in: float, burn_fraction_in: float    ) -> ModuleResult[Tritium_Breeding_AdequacyOutput]:
        """Execute calculation.

        Args:
            loss_rate_in: loss_rate_in input
            I_total_in: I_total_in input
            eta_extract_in: eta_extract_in input
            burn_rate_in: burn_rate_in input
            tbr_lower_in: tbr_lower_in input
            defined_in: defined_in input
            tbr_floor_in: tbr_floor_in input
            G_stock_in: G_stock_in input
            lambda_T_in: lambda_T_in input
            tbr_mean_in: tbr_mean_in input
            t_recycle_in: t_recycle_in input
            tbr_required_in: tbr_required_in input
            burn_fraction_in: burn_fraction_in input

        Returns:
            Module result with Tritium_Breeding_AdequacyOutput (design_margin, decay_rate, fuel_margin, extracted_supply_rate, recycle_loss_rate, defined_flag, required_tbr, balance_rate, extraction_loss_rate, stock_growth_rate, numerical_margin, production_rate)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(loss_rate_in, I_total_in, eta_extract_in, burn_rate_in, tbr_lower_in, defined_in, tbr_floor_in, G_stock_in, lambda_T_in, tbr_mean_in, t_recycle_in, tbr_required_in, burn_fraction_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_tritium_breeding.tritium_breeding_adequacy_impl import (
            run_tritium_breeding_adequacy,
        )

        # Execute implementation - returns tuple of values
        design_margin, decay_rate, fuel_margin, extracted_supply_rate, recycle_loss_rate, defined_flag, required_tbr, balance_rate, extraction_loss_rate, stock_growth_rate, numerical_margin, production_rate = run_tritium_breeding_adequacy(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Tritium_Breeding_AdequacyOutput(
                design_margin=design_margin,
                decay_rate=decay_rate,
                fuel_margin=fuel_margin,
                extracted_supply_rate=extracted_supply_rate,
                recycle_loss_rate=recycle_loss_rate,
                defined_flag=defined_flag,
                required_tbr=required_tbr,
                balance_rate=balance_rate,
                extraction_loss_rate=extraction_loss_rate,
                stock_growth_rate=stock_growth_rate,
                numerical_margin=numerical_margin,
                production_rate=production_rate,
            )
        )
