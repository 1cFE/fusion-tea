package combinations_lumped_fit {
    doc /*
    C-4: the three ARIES branch outlet temperatures into the Stellaris lumped efficiency law ('Power Cycle Efficiency',
    Kovari 2016 Table 4 helium-primary Rankine fit) with its 'Cycle Fit Domain' constraint. Existing definitions only.
    Each branch is read alone; no combining rule across branches is asserted (map row H8 records that as new behavior).
    **Source**: work/active/WI-093_combination-assemblies/design.md § 4 **Reference**: map rows H6, H7
    **Basis**: [INHERITED: ARIES] hot limits 729.15 / 973.15 / 1011.15 K (plant.sysml:249-257); [INHERITED: Stellaris] fit
    coefficients, approach and domain (stellarator_plant.sysml:816-831). **Last Updated**: 2026-09-26
    */
    private import ScalarValues::*;
    private import mfe_power_cycle::*;
    private import mfe_viability::*;

    part lumped_fit {
        doc /* Root occurrence of the combinations_lumped_fit assembly (the generator renders output aliases by part path, so each assembly needs its own root part; the Stellaris nesting shape). */
        part he_fit {
            doc /* Blanket-helium branch at its ARIES outlet limit. T2 = 729.15 − 20 − 273.15 = 436 °C, inside [384, 642]. */
            attribute T_hot : Real = 729.15;
            attribute dT_approach : Real = 20.0;
            attribute a_fit : Real = 0.1802;
            attribute b_fit : Real = 0.7823;
            attribute T_offset_fit : Real = 273.0;
            attribute T2_min : Real = 384.0;
            attribute T2_max : Real = 642.0;
            attribute delta_eta : Real = 0.0;
            attribute cycle_live : Real = 1.0;
            attribute eta_th_direct : Real = 0.0;
            calc cycle : 'Power Cycle Efficiency' {
                in T_hot_in = T_hot;
                in dT_approach_in = dT_approach;
                in a_fit_in = a_fit;
                in b_fit_in = b_fit;
                in T_offset_fit_in = T_offset_fit;
                in T2_min_in = T2_min;
                in T2_max_in = T2_max;
                in delta_eta_in = delta_eta;
                in cycle_live_in = cycle_live;
                in eta_th_direct_in = eta_th_direct;
            }
            attribute T2_C : Real = cycle.T2_C;
            attribute eta_fit : Real = cycle.eta_fit;
            attribute eta_th : Real = cycle.eta_th;
            attribute margin_low : Real = cycle.margin_low;
            attribute margin_high : Real = cycle.margin_high;
            attribute domain_product : Real = cycle.domain_product;
            assert constraint domain_ok : 'Cycle Fit Domain' {
                in domain_product_in = domain_product;
            }
        }
        part divertor_fit {
            doc /* Divertor-helium branch at its ARIES outlet limit. T2 = 680 °C, above T2_max: the constraint reads violated and the value is published unclamped. */
            attribute T_hot : Real = 973.15;
            attribute dT_approach : Real = 20.0;
            attribute a_fit : Real = 0.1802;
            attribute b_fit : Real = 0.7823;
            attribute T_offset_fit : Real = 273.0;
            attribute T2_min : Real = 384.0;
            attribute T2_max : Real = 642.0;
            attribute delta_eta : Real = 0.0;
            attribute cycle_live : Real = 1.0;
            attribute eta_th_direct : Real = 0.0;
            calc cycle : 'Power Cycle Efficiency' {
                in T_hot_in = T_hot;
                in dT_approach_in = dT_approach;
                in a_fit_in = a_fit;
                in b_fit_in = b_fit;
                in T_offset_fit_in = T_offset_fit;
                in T2_min_in = T2_min;
                in T2_max_in = T2_max;
                in delta_eta_in = delta_eta;
                in cycle_live_in = cycle_live;
                in eta_th_direct_in = eta_th_direct;
            }
            attribute T2_C : Real = cycle.T2_C;
            attribute eta_fit : Real = cycle.eta_fit;
            attribute eta_th : Real = cycle.eta_th;
            attribute margin_low : Real = cycle.margin_low;
            attribute margin_high : Real = cycle.margin_high;
            attribute domain_product : Real = cycle.domain_product;
            assert constraint domain_ok : 'Cycle Fit Domain' {
                in domain_product_in = domain_product;
            }
        }
        part pbli_fit {
            doc /* PbLi branch at its ARIES outlet limit. T2 = 718 °C, above T2_max: violated, published unclamped. */
            attribute T_hot : Real = 1011.15;
            attribute dT_approach : Real = 20.0;
            attribute a_fit : Real = 0.1802;
            attribute b_fit : Real = 0.7823;
            attribute T_offset_fit : Real = 273.0;
            attribute T2_min : Real = 384.0;
            attribute T2_max : Real = 642.0;
            attribute delta_eta : Real = 0.0;
            attribute cycle_live : Real = 1.0;
            attribute eta_th_direct : Real = 0.0;
            calc cycle : 'Power Cycle Efficiency' {
                in T_hot_in = T_hot;
                in dT_approach_in = dT_approach;
                in a_fit_in = a_fit;
                in b_fit_in = b_fit;
                in T_offset_fit_in = T_offset_fit;
                in T2_min_in = T2_min;
                in T2_max_in = T2_max;
                in delta_eta_in = delta_eta;
                in cycle_live_in = cycle_live;
                in eta_th_direct_in = eta_th_direct;
            }
            attribute T2_C : Real = cycle.T2_C;
            attribute eta_fit : Real = cycle.eta_fit;
            attribute eta_th : Real = cycle.eta_th;
            attribute margin_low : Real = cycle.margin_low;
            attribute margin_high : Real = cycle.margin_high;
            attribute domain_product : Real = cycle.domain_product;
            assert constraint domain_ok : 'Cycle Fit Domain' {
                in domain_product_in = domain_product;
            }
        }
    }
}
