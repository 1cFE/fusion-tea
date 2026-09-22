package sector_constituent_inventory {
    private import ScalarValues::*;
    calc def 'Covered Layer Volume' {
        doc /* volume = area_basis_in * coverage_in * thickness_in. Units m2, dimensionless and m yield m3. Inputs finite nonnegative; coverage in [0,1]. Reject nonfinite outputs. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21. */
        in attribute area_basis_in : Real;
        in attribute coverage_in : Real;
        in attribute thickness_in : Real;
        out attribute volume : Real;
    }
    calc def 'Constituent Inventory' {
        doc /* constituent_volume = region_volume_in * fraction_in; known_mass = constituent_volume * density_in; source_price_subtotal = known_mass * unit_price_in. Units m3, kg/m3 and source-year dollars/kg yield kg and source-year dollars. Finite nonnegative inputs, fraction in [0,1], density strictly positive. Reject nonfinite outputs. A missing density or price is not zero; an unquantified constituent is represented outside this calculation. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21. */
        in attribute region_volume_in : Real;
        in attribute fraction_in : Real;
        in attribute density_in : Real;
        in attribute unit_price_in : Real;
        out attribute constituent_volume : Real;
        out attribute known_mass : Real;
        out attribute source_price_subtotal : Real;
    }
    calc def 'Three Constituent Recipe Summary' {
        doc /* represented_fraction = fraction_1_in + fraction_2_in + fraction_3_in; unquantified_volume = region_volume_in * unquantified_fraction_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in. Units m3, kg and same-source-year dollars; no currency conversion. Finite nonnegative inputs, each fraction in [0,1]; sum of represented and unquantified fractions must equal one within 1e-12, an arithmetic closure tolerance. Check closure even at zero volume. Reject nonfinite outputs. Three explicitly represented material children plus an unquantified-volume complement; their mass and price coverage remain partial. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21. */
        in attribute region_volume_in : Real;
        in attribute fraction_1_in : Real;
        in attribute fraction_2_in : Real;
        in attribute fraction_3_in : Real;
        in attribute unquantified_fraction_in : Real;
        in attribute mass_1_in : Real;
        in attribute mass_2_in : Real;
        in attribute mass_3_in : Real;
        in attribute price_1_in : Real;
        in attribute price_2_in : Real;
        in attribute price_3_in : Real;
        out attribute represented_fraction : Real;
        out attribute unquantified_volume : Real;
        out attribute known_mass : Real;
        out attribute source_price_subtotal : Real;
    }
    calc def 'Three Sector Inventory Sum' {
        doc /* The three supplied lateral coverages must each lie in [0,1] and sum to one within 1e-12, including zero-volume cases. Refuse inconsistent supplied partitions; never normalize them. This establishes arithmetic partition closure, not geometric nonoverlap qualification. */
        doc /* volume = volume_1_in + volume_2_in + volume_3_in; known_mass = mass_1_in + mass_2_in + mass_3_in; source_price_subtotal = price_1_in + price_2_in + price_3_in; unquantified_volume = unquantified_volume_1_in + unquantified_volume_2_in + unquantified_volume_3_in. Inputs and outputs finite nonnegative. Units m3, kg and same-source-year dollars; no currency conversion. Sums three nonoverlapping lateral layer occurrences, not arbitrary stacked area fractions. Partial source-price sum is not installed capital. Guarded typed completion implements these equations through the native route. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: geometry/material identities and three-child aggregation contract. Last Updated: 2026-09-21. */
        in attribute volume_1_in : Real;
        in attribute volume_2_in : Real;
        in attribute volume_3_in : Real;
        in attribute coverage_1_in : Real;
        in attribute coverage_2_in : Real;
        in attribute coverage_3_in : Real;
        in attribute mass_1_in : Real;
        in attribute mass_2_in : Real;
        in attribute mass_3_in : Real;
        in attribute price_1_in : Real;
        in attribute price_2_in : Real;
        in attribute price_3_in : Real;
        in attribute unquantified_volume_1_in : Real;
        in attribute unquantified_volume_2_in : Real;
        in attribute unquantified_volume_3_in : Real;
        out attribute volume : Real;
        out attribute known_mass : Real;
        out attribute source_price_subtotal : Real;
        out attribute unquantified_volume : Real;
    }
}
