package aries_constituent_inventory {
    private import ScalarValues::*;
    private import sector_constituent_inventory::*;
    part full {
        doc /* Reference FS/He blanket region, not the SiC alternative. Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Lyon Table II p706. Basis: source recipe and coverage, independently supplied midpoint-area basis; AGENT normalized area scenario. Tapered 0.25m is a source endpoint sensitivity, not an inferred mean. Last Updated: 2026-09-21. */
        attribute midpoint_area_basis : Real = 1.0;
        attribute coverage : Real = 0.654;
        attribute thickness : Real = 0.543;
        attribute helium_fraction : Real = 0.08;
        calc layer : 'Covered Layer Volume' {
            in area_basis_in = midpoint_area_basis;
            in coverage_in = coverage;
            in thickness_in = thickness;
        }
        attribute region_volume : Real = layer.volume;
        part lipb {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II full recipe, lipb; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.79;
            attribute material_density : Real = 8897;
            attribute component_rate : Real = 17.1;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = full.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        part sic_insert {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II full recipe, sic_insert; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.07;
            attribute material_density : Real = 3200;
            attribute component_rate : Real = 101;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = full.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        part ferritic_steel {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II full recipe, ferritic_steel; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.06;
            attribute material_density : Real = 7800;
            attribute component_rate : Real = 103;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = full.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        calc recipe : 'Three Constituent Recipe Summary' {
            in region_volume_in = region_volume;
            in unquantified_fraction_in = helium_fraction;
            in fraction_1_in = lipb.volume_fraction;
            in mass_1_in = lipb.known_mass;
            in price_1_in = lipb.source_price_subtotal;
            in fraction_2_in = sic_insert.volume_fraction;
            in mass_2_in = sic_insert.known_mass;
            in price_2_in = sic_insert.source_price_subtotal;
            in fraction_3_in = ferritic_steel.volume_fraction;
            in mass_3_in = ferritic_steel.known_mass;
            in price_3_in = ferritic_steel.source_price_subtotal;
        }
        attribute known_mass : Real = recipe.known_mass;
        attribute source_price_subtotal : Real = recipe.source_price_subtotal;
        attribute unquantified_helium_volume : Real = recipe.unquantified_volume;
    }
    part behind_divertor {
        doc /* Reference FS/He blanket region, not the SiC alternative. Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Lyon Table II p706. Basis: source recipe and coverage, independently supplied midpoint-area basis; AGENT normalized area scenario. Tapered 0.25m is a source endpoint sensitivity, not an inferred mean. Last Updated: 2026-09-21. */
        attribute midpoint_area_basis : Real = 1.0;
        attribute coverage : Real = 0.106;
        attribute thickness : Real = 0.35;
        attribute helium_fraction : Real = 0.08;
        calc layer : 'Covered Layer Volume' {
            in area_basis_in = midpoint_area_basis;
            in coverage_in = coverage;
            in thickness_in = thickness;
        }
        attribute region_volume : Real = layer.volume;
        part lipb {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II behind_divertor recipe, lipb; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.75;
            attribute material_density : Real = 8897;
            attribute component_rate : Real = 17.1;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = behind_divertor.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        part sic_insert {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II behind_divertor recipe, sic_insert; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.09;
            attribute material_density : Real = 3200;
            attribute component_rate : Real = 101;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = behind_divertor.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        part ferritic_steel {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II behind_divertor recipe, ferritic_steel; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.08;
            attribute material_density : Real = 7800;
            attribute component_rate : Real = 103;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = behind_divertor.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        calc recipe : 'Three Constituent Recipe Summary' {
            in region_volume_in = region_volume;
            in unquantified_fraction_in = helium_fraction;
            in fraction_1_in = lipb.volume_fraction;
            in mass_1_in = lipb.known_mass;
            in price_1_in = lipb.source_price_subtotal;
            in fraction_2_in = sic_insert.volume_fraction;
            in mass_2_in = sic_insert.known_mass;
            in price_2_in = sic_insert.source_price_subtotal;
            in fraction_3_in = ferritic_steel.volume_fraction;
            in mass_3_in = ferritic_steel.known_mass;
            in price_3_in = ferritic_steel.source_price_subtotal;
        }
        attribute known_mass : Real = recipe.known_mass;
        attribute source_price_subtotal : Real = recipe.source_price_subtotal;
        attribute unquantified_helium_volume : Real = recipe.unquantified_volume;
    }
    part tapered {
        doc /* Reference FS/He blanket region, not the SiC alternative. Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Lyon Table II p706. Basis: source recipe and coverage, independently supplied midpoint-area basis; AGENT normalized area scenario. Tapered 0.25m is a source endpoint sensitivity, not an inferred mean. Last Updated: 2026-09-21. */
        attribute midpoint_area_basis : Real = 1.0;
        attribute coverage : Real = 0.24;
        attribute thickness : Real = 0.25;
        attribute helium_fraction : Real = 0.08;
        calc layer : 'Covered Layer Volume' {
            in area_basis_in = midpoint_area_basis;
            in coverage_in = coverage;
            in thickness_in = thickness;
        }
        attribute region_volume : Real = layer.volume;
        part lipb {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II tapered recipe, lipb; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.76;
            attribute material_density : Real = 8897;
            attribute component_rate : Real = 17.1;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = tapered.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        part sic_insert {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II tapered recipe, sic_insert; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.08;
            attribute material_density : Real = 3200;
            attribute component_rate : Real = 101;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = tapered.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        part ferritic_steel {
            doc /* Source: work/active/WI-084_aries-sector-constituent-inventory/evidence/lyon-p706.png. Ref: Table II tapered recipe, ferritic_steel; volume fraction, kg/m3 density, complex-machined-shape USD2004/kg rate. Basis: supplied constituent, partial component subtotal; LiPb account scope is separate from blanket installation. Last Updated: 2026-09-21. */
            attribute volume_fraction : Real = 0.08;
            attribute material_density : Real = 7800;
            attribute component_rate : Real = 103;
            calc inventory : 'Constituent Inventory' {
                in region_volume_in = tapered.region_volume;
                in fraction_in = volume_fraction;
                in density_in = material_density;
                in unit_price_in = component_rate;
            }
            attribute constituent_volume : Real = inventory.constituent_volume;
            attribute known_mass : Real = inventory.known_mass;
            attribute source_price_subtotal : Real = inventory.source_price_subtotal;
        }
        calc recipe : 'Three Constituent Recipe Summary' {
            in region_volume_in = region_volume;
            in unquantified_fraction_in = helium_fraction;
            in fraction_1_in = lipb.volume_fraction;
            in mass_1_in = lipb.known_mass;
            in price_1_in = lipb.source_price_subtotal;
            in fraction_2_in = sic_insert.volume_fraction;
            in mass_2_in = sic_insert.known_mass;
            in price_2_in = sic_insert.source_price_subtotal;
            in fraction_3_in = ferritic_steel.volume_fraction;
            in mass_3_in = ferritic_steel.known_mass;
            in price_3_in = ferritic_steel.source_price_subtotal;
        }
        attribute known_mass : Real = recipe.known_mass;
        attribute source_price_subtotal : Real = recipe.source_price_subtotal;
        attribute unquantified_helium_volume : Real = recipe.unquantified_volume;
    }
    part reference_blanket_subset {
        doc /* Sum of three modeled blanket layer regions only. Unknown helium mass and price remain unquantified. Excludes first wall, divertor hardware, back walls, shields and manifolds. Source: work/active/WI-084_aries-sector-constituent-inventory/spec.md. Reference: supplied normalized geometry and partial-inventory contract. Last Updated: 2026-09-21. */
        calc totals : 'Three Sector Inventory Sum' {
            in coverage_1_in = full.coverage;
            in coverage_2_in = behind_divertor.coverage;
            in coverage_3_in = tapered.coverage;
            in volume_1_in = full.region_volume;
            in mass_1_in = full.known_mass;
            in price_1_in = full.source_price_subtotal;
            in unquantified_volume_1_in = full.unquantified_helium_volume;
            in volume_2_in = behind_divertor.region_volume;
            in mass_2_in = behind_divertor.known_mass;
            in price_2_in = behind_divertor.source_price_subtotal;
            in unquantified_volume_2_in = behind_divertor.unquantified_helium_volume;
            in volume_3_in = tapered.region_volume;
            in mass_3_in = tapered.known_mass;
            in price_3_in = tapered.source_price_subtotal;
            in unquantified_volume_3_in = tapered.unquantified_helium_volume;
        }
    }
}
