from pydantic import Field
from simkit.config.schema import MultiOutput

class Tritium_Breeding_AdequacyOutput(MultiOutput):
    """Multi-output container for Tritium_Breeding_Adequacy.

Conditional fuel-account adequacy. Typed manual completion validates finite quantities; positive burn rate; burn fraction and extraction efficiency in (0,1]; exhaust recovery in [0,1]; nonnegative decay constant, inventory, growth and loss; positive finite design/fuel requirements; and the exact applicability flag. required_tbr=max(tbr_floor_in,tbr_required_in), without adding the same reserve twice. design_margin=tbr_mean_in-tbr_floor_in; fuel_margin=tbr_mean_in-tbr_required_in; numerical_margin=tbr_lower_in-required_tbr. Production=tbr_mean_in*burn_rate_in; extracted_supply=eta_extract_in*production; extraction_loss=(1-eta_extract_in)*production; recycle_loss=loss_rate_in; decay=lambda_T_in*I_total_in; stock_growth=G_stock_in; balance=extracted_supply-burn_rate_in-recycle_loss-decay-stock_growth [all rates atoms/s]. Extraction acts on breeder supply only. Check finite intermediates, consistency of required breeding with its source account, and nonnegative physical production.
defined_flag is exactly 0 or 1. It marks all breeding-derived outputs together. Invalid applicability or account inputs fail the screen even if a malformed requirement is nonpositive. A valid requirement may remain reported when breeding is undefined, but breeding-derived numerical carriers are zero and are not physical margins, lower bounds or deficits. Raw Fuel Cycle Flows margin has this same applicability condition in a transport-driven instance. The retained 0.99 exhaust recovery is a conditional cost-derived reading, not isotope-recovery evidence; unity extraction and zero inventory/growth remain optimistic explicit assumptions.
*Source**: work/active/WI-066_computed-tritium-breeding/spec.md
*Reference**: models/library/analyses/mfe_fuel_cycle.sysml; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
*Last Updated**: 2026-09-18

SysML Source: root-0/analyses/mfe_tritium_breeding.sysml:30
    """
    design_margin: float = Field(description="design_margin output")
    decay_rate: float = Field(description="decay_rate output")
    fuel_margin: float = Field(description="fuel_margin output")
    extracted_supply_rate: float = Field(description="extracted_supply_rate output")
    recycle_loss_rate: float = Field(description="recycle_loss_rate output")
    defined_flag: float = Field(description="defined_flag output")
    required_tbr: float = Field(description="required_tbr output")
    balance_rate: float = Field(description="balance_rate output")
    extraction_loss_rate: float = Field(description="extraction_loss_rate output")
    stock_growth_rate: float = Field(description="stock_growth_rate output")
    numerical_margin: float = Field(description="numerical_margin output")
    production_rate: float = Field(description="production_rate output")
