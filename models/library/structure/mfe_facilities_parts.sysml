package mfe_facilities_parts {
    private import ScalarValues::*;
    private import costed_component::*;
    private import mfe_facilities::*;
    part def 'Facility Building' :> 'Costed Component' {
        doc /* Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Physical civil occurrence with its own quantities and cost. */
        :>> cas_code = "21";
        attribute enabled : Boolean;
        attribute clear_length : Real;
        attribute clear_width : Real;
        attribute clear_height : Real;
        attribute clear_area : Real;
        attribute gross_area : Real;
        attribute air_volume : Real;
        attribute sub_concrete : Real;
        attribute super_concrete : Real;
        attribute sub_formwork : Real;
        attribute super_formwork : Real;
        attribute sub_rebar : Real;
        attribute super_rebar : Real;
        attribute sub_concrete_rate : Real;
        attribute sub_formwork_rate : Real;
        attribute sub_rebar_rate : Real;
        attribute super_concrete_rate : Real;
        attribute super_formwork_rate : Real;
        attribute super_rebar_rate : Real;
        attribute civil_cpi_ratio : Real;
        attribute civil_rate_multiplier : Real;
        attribute tonne_interpretation_kg : Real;
        calc civil : 'Facility Civil Cost' {
            in enabled_in = enabled;
            in sub_concrete_in = sub_concrete;
            in super_concrete_in = super_concrete;
            in sub_formwork_in = sub_formwork;
            in super_formwork_in = super_formwork;
            in sub_rebar_in = sub_rebar;
            in super_rebar_in = super_rebar;
            in sub_concrete_rate_in = sub_concrete_rate;
            in sub_formwork_rate_in = sub_formwork_rate;
            in sub_rebar_rate_in = sub_rebar_rate;
            in super_concrete_rate_in = super_concrete_rate;
            in super_formwork_rate_in = super_formwork_rate;
            in super_rebar_rate_in = super_rebar_rate;
            in civil_cpi_ratio_in = civil_cpi_ratio;
            in civil_rate_multiplier_in = civil_rate_multiplier;
            in tonne_interpretation_kg_in = tonne_interpretation_kg;
        }
        :>> capital_cost = civil.cost_2025;
    }
    part def 'Facility Service Account' :> 'Costed Component' {
        doc /* Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Separately identified services or inherited site allowance. */
        :>> cas_code = "21";
    }
}
