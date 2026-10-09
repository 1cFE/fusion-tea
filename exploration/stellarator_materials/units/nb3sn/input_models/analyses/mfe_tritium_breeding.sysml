package mfe_tritium_breeding {
    private import ScalarValues::*;

    calc def 'Blanket Tritium Breeding' {
        doc /* Continuous-energy-transport response interpolation for an explicitly fixed material/source scenario. The supported lever is breeder thickness [m]; all other geometry inputs [m, except dimensionless kappa] are applicability guards. Fixed enrichment and material/source metadata belong to the immutable response-data manifest, not free public inputs. The typed manual implementation checks finite inputs, the released table domain and every fixed geometry coordinate; no extrapolation or clamping. Table release and independent withheld validation are prerequisites for implementation completion.
        Outputs are Li6/Li7 production and total tritium atoms per emitted fusion neutron, total Monte Carlo standard error, interpolation allowance, numerical lower estimate and defined_flag (exactly 0 or 1). The statistical multiplier and allowance are declared in the released manifest. The lower estimate is not a physical confidence bound. Unsupported inputs return zero numerical carriers and defined_flag=0; those carriers are undefined, not physical zero breeding or proof of deficit. Shaped-stellarator bias and physical scenario uncertainties remain separate.
        **Source**: work/active/WI-066_computed-tritium-breeding/spec.md
        **Reference**: work/active/WI-066_computed-tritium-breeding/design.md; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
        **Last Updated**: 2026-09-18 */
        in attribute blanket_t_in : Real;
        in attribute R_in : Real;
        in attribute a_in : Real;
        in attribute kappa_in : Real;
        in attribute vacuum_t_in : Real;
        in attribute firstwall_t_in : Real;
        in attribute reflector_t_in : Real;
        in attribute ht_shield_t_in : Real;
        in attribute structure_t_in : Real;
        in attribute gap1_t_in : Real;
        in attribute vessel_t_in : Real;
        out attribute tbr_li6 : Real;
        out attribute tbr_li7 : Real;
        out attribute tbr_mean : Real;
        out attribute tbr_std_error : Real;
        out attribute interpolation_allowance : Real;
        out attribute tbr_lower : Real;
        out attribute defined_flag : Real;
    }

    calc def 'Tritium Breeding Adequacy' {
        doc /* Conditional fuel-account adequacy. Typed manual completion validates finite quantities; positive burn rate; burn fraction and extraction efficiency in (0,1]; exhaust recovery in [0,1]; nonnegative decay constant, inventory, growth and loss; positive finite design/fuel requirements; and the exact applicability flag. required_tbr=max(tbr_floor_in,tbr_required_in), without adding the same reserve twice. design_margin=tbr_mean_in-tbr_floor_in; fuel_margin=tbr_mean_in-tbr_required_in; numerical_margin=tbr_lower_in-required_tbr. Production=tbr_mean_in*burn_rate_in; extracted_supply=eta_extract_in*production; extraction_loss=(1-eta_extract_in)*production; recycle_loss=loss_rate_in; decay=lambda_T_in*I_total_in; stock_growth=G_stock_in; balance=extracted_supply-burn_rate_in-recycle_loss-decay-stock_growth [all rates atoms/s]. Extraction acts on breeder supply only. Check finite intermediates, consistency of required breeding with its source account, and nonnegative physical production.
        defined_flag is exactly 0 or 1. It marks all breeding-derived outputs together. Invalid applicability or account inputs fail the screen even if a malformed requirement is nonpositive. A valid requirement may remain reported when breeding is undefined, but breeding-derived numerical carriers are zero and are not physical margins, lower bounds or deficits. Raw Fuel Cycle Flows margin has this same applicability condition in a transport-driven instance. The retained 0.99 exhaust recovery is a conditional cost-derived reading, not isotope-recovery evidence; unity extraction and zero inventory/growth remain optimistic explicit assumptions.
        **Source**: work/active/WI-066_computed-tritium-breeding/spec.md
        **Reference**: models/library/analyses/mfe_fuel_cycle.sysml; work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md
        **Last Updated**: 2026-09-18 */
        in attribute tbr_mean_in : Real;
        in attribute tbr_lower_in : Real;
        in attribute defined_in : Real;
        in attribute tbr_floor_in : Real;
        in attribute tbr_required_in : Real;
        in attribute burn_rate_in : Real;
        in attribute loss_rate_in : Real;
        in attribute eta_extract_in : Real;
        in attribute lambda_T_in : Real;
        in attribute I_total_in : Real;
        in attribute G_stock_in : Real;
        in attribute burn_fraction_in : Real;
        in attribute t_recycle_in : Real;
        out attribute required_tbr : Real;
        out attribute design_margin : Real;
        out attribute fuel_margin : Real;
        out attribute numerical_margin : Real;
        out attribute production_rate : Real;
        out attribute extracted_supply_rate : Real;
        out attribute extraction_loss_rate : Real;
        out attribute recycle_loss_rate : Real;
        out attribute decay_rate : Real;
        out attribute stock_growth_rate : Real;
        out attribute balance_rate : Real;
        out attribute defined_flag : Real;
    }

    constraint def 'Computed TBR Adequacy' {
        doc /* Valid conditional fuel account and transport applicability plus numerical lower breeding at least the stricter of design floor and fuel requirement. Numerical uncertainty is not a physical qualification bound. **Source**: work/active/WI-066_computed-tritium-breeding/spec.md **Reference**: work/orchestration/goals/computed-tritium-breeding/evidence/round2/benchmark-and-interface-review.md **Last Updated**: 2026-09-18 */
        in attribute defined_in : Real;
        in attribute numerical_margin_in : Real;
        defined_in >= 1.0 and numerical_margin_in >= 0.0
    }
}
