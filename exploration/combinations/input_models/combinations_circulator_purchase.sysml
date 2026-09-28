package combinations_circulator_purchase {
    doc /*
    C-5: the ARIES selected-purchase law ('Selected Inventory Purchase' on a 'Selected Equipment' leaf) applied to the
    Stellaris helium circulator at a re-selected shaft rating, with the ARIES capacity screen against the Stellaris demand.
    Existing definitions only. Capital follows the selected rating, never the demand (MR-7).
    **Source**: work/active/WI-093_combination-assemblies/design.md § 5 **Reference**: map row E1
    **Basis**: [INHERITED: Stellaris baseline] reference quantity helium_design_shaft_MW 6.26003337158886 MW and reference cost
    primary_circulators_cost 442,174,444.749 USD at the design point (work/analysis/model-evaluation-diagnostics/baseline.json);
    the linear law is the ARIES E4 assumption; [ASSUMED] selected rating 8 MW. **Last Updated**: 2026-09-26
    */
    private import ScalarValues::*;
    private import costed_component::*;
    private import integrated_equipment_parts::*;
    private import integrated_equipment_costs::*;
    private import mfe_viability::*;

    part circulator_purchase {
        doc /* Root occurrence of the combinations_circulator_purchase assembly (the generator renders output aliases by part path, so each assembly needs its own root part; the Stellaris nesting shape). */
        part circulator_equipment : 'Selected Equipment' {
            doc /* Selected shaft rating is the chosen quantity; capital is calculated from it through the linear law; mode 0 (linear, not fixed budget). */
            :>> cas_code = "22.2";
            attribute selected_rating : Real = 8.0;
            attribute reference_quantity : Real = 6.26003337158886;
            attribute reference_cost : Real = 442174444.74911624;
            attribute price_factor : Real = 1.0;
            attribute estimate_mode : Real = 0.0;
            calc purchase : 'Selected Inventory Purchase' {
                in quantity_in = selected_rating;
                in reference_quantity_in = reference_quantity;
                in reference_cost_in = reference_cost;
                in price_factor_in = price_factor;
                in mode_in = estimate_mode;
            }
            attribute inventory_quantity : Real = purchase.purchased_quantity;
            attribute quantity_ratio : Real = purchase.quantity_ratio;
            attribute estimated_cost : Real = purchase.capital;
            attribute cost_extrapolated : Real = purchase.extrapolated;
            :>> capital_cost = purchase.capital;
        }
        part circulator_capacity {
            doc /* The selected rating against the Stellaris circulator shaft demand at the design point. **Basis**: demand [INHERITED: Stellaris baseline circulator_shaft_MW 6.26003337158886 MW], supplied here as a literal because the Stellaris loop is not assembled in C-5. */
            attribute demand : Real = 6.26003337158886;
            attribute assumed_supported : Boolean = true;
            attribute scenario_applicable : Boolean = true;
            attribute demand_available : Boolean = true;
            calc evaluate : 'Offered Capacity Screen' {
                in rating_in = circulator_equipment.selected_rating;
                in demand_in = demand;
                in applicable_in = scenario_applicable;
                in conditions_supported_in = assumed_supported;
                in demand_available_in = demand_available;
            }
            attribute margin : Real = evaluate.margin;
            attribute evaluation_defined : Real = evaluate.evaluation_defined;
            assert constraint capacity_ok : 'Offered Equipment Capacity' {
                in defined_in = evaluation_defined;
                in margin_in = margin;
            }
        }
    }
}
