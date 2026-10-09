package mfe_cooling_accounts {
    private import ScalarValues::*;

    calc def 'Cooling Scenario Guard' {
        doc /* Validate supported scenario choices before using zero dormant outputs.
        Both modes must be finite and exactly zero or one. If either mode is one,
        equipment_enabled_in must be true; otherwise raise ValueError. Return the
        validated cost_mode_in and energy_mode_in unchanged. False/zero/zero is the
        generic dormant scenario. Manual completion supplies the explicit guards.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Implementation review control-domain correction; Basis: scenario validity. */
        in attribute equipment_enabled_in : Boolean;
        in attribute cost_mode_in : Real;
        in attribute energy_mode_in : Real;
        out attribute cost_mode : Real;
        out attribute energy_mode : Real;
    }

    calc def 'Cooling Account Selection' {
        doc /* Select independently sized cooling accounts or the retained legacy
        allowance. Cost mode and secondary energy mode are binary scenario inputs
        (0 or 1), not continuous blending controls. Each energy selector applies
        to both electricity and recovered shaft heat. Primary IHX duty remains
        upstream of secondary work, avoiding a feedback edge. New equipment
        amounts are plant-total for the supported single-module scenario.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Account boundaries; Intermediate equipment and energy; Corrective review details
        Basis: explicit accounting identities, independent of equipment price models.
        */
        in attribute cost_mode_in : Real;
        in attribute legacy_cost_in : Real;
        in attribute equipment_cost_in : Real;
        in attribute delivered_in : Real;
        in attribute replacements_in : Real;
        in attribute consumables_in : Real;
        out attribute cost : Real = (1.0 - cost_mode_in) * legacy_cost_in + cost_mode_in * equipment_cost_in;
        out attribute shipping_exclusion : Real = cost_mode_in * delivered_in;
        out attribute replacement_annual : Real = cost_mode_in * replacements_in;
        out attribute consumables_annual : Real = cost_mode_in * consumables_in;
    }

    calc def 'Cooling Energy Addition' {
        doc /* Add intermediate pump electricity and recovered shaft work together.
        This producer has no cost inputs: the legacy cost reads plant net power,
        so combining its inputs with this producer would create a dependency cycle.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Corrective review details; Basis: separate acyclic energy ownership. */
        in attribute secondary_mode_in : Real;
        in attribute primary_electric_in : Real;
        in attribute primary_recovered_in : Real;
        in attribute salt_electric_in : Real;
        in attribute salt_shaft_in : Real;
        out attribute electric_total : Real = primary_electric_in + secondary_mode_in * salt_electric_in;
        out attribute recovered_total : Real = primary_recovered_in + secondary_mode_in * salt_shaft_in;
    }

    calc def 'Cooling Annual Addition' {
        doc /* Add new cooling annual expenses to their distinct existing owners.
        Routine service labor remains in inherited O&M; cooling consumable make-up
        enters before the existing annual-cost levelization. Dated cooling major
        replacements are already annualized and enter CAS72 after that calculation.
        Source: work/active/WI-067_installed-cooling-equipment-costs/combined-design.md
        Ref: Lifecycle; models/library/analyses/mfe_lifecycle.sysml (annualized replacement convention)
        Basis: sum each annual expense once before its existing consumer.
        */
        in attribute existing_om_in : Real;
        in attribute cooling_consumables_in : Real;
        in attribute existing_replacements_in : Real;
        in attribute cooling_replacements_in : Real;
        out attribute annual_om : Real = existing_om_in + cooling_consumables_in;
        out attribute cas72_total : Real = existing_replacements_in + cooling_replacements_in;
    }
}
