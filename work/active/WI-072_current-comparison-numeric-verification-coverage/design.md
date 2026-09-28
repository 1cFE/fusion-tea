# Verification mapping design correction

[AGENT] Implements fresh review F4; this is an exact proposed inventory, not a current-output baseline. Prefix for every native suffix is `stellarator_09__stellaris__`. The left column is the new independent result name; the middle column is an existing independently computed oracle local/expression; the right column is the native producer suffix.

| New oracle name | Independent expected expression | Native producer |
|---|---|---|
| coverage_annual_total | annual_om | cas70_calc__annual_total |
| coverage_cas70 | cas70_annual | cas70_calc__cas70 |
| coverage_cas71_crf | crf_71 | cas71_calc__crf |
| coverage_cas71_levelized | cas71_annual | cas71_calc__levelized |
| coverage_cas80_crf | crf_71 | cas80_calc__crf |
| coverage_cas80_levelized | cas80_annual | cas80_calc__levelized |
| coverage_cooling_cost_mode | p['cooling_cost_mode'] after existing finite/binary guard | heat_transport__cooling_guard__cost_mode |
| coverage_cooling_energy_mode | p['cooling_energy_mode'] after existing finite/binary guard | heat_transport__cooling_guard__energy_mode |
| coverage_cooling_consumables | p['cooling_cost_mode'] * cooling['consumables_annual'] | heat_transport__cooling_selection__consumables_annual |
| coverage_cooling_replacements | p['cooling_cost_mode'] * cooling['replacement_annual'] | heat_transport__cooling_selection__replacement_annual |
| coverage_cooling_shipping | p['cooling_cost_mode'] * cooling['delivered_total'] | heat_transport__cooling_selection__shipping_exclusion |
| coverage_coil_length | c_coil | magnet__coil_length__c_coil |
| coverage_wp_side | wp_side | magnet__wp_sizing__wp_side |
| coverage_cold_volume | vol_cold_total | magnet__wp_volume__vol_cold_total |
| coverage_blanket_volume | blanket_vol | rb__blanket_vol |
| coverage_outer_radius | lt_shield_or | rb__outer_radius |
| coverage_coil_inner_radius | r_coil | rb__r_coil |
| coverage_shield_volume | shield_vol | rb__shield_vol |
| coverage_structure_volume | structure_vol | rb__structure_vol |
| coverage_vessel_volume | vessel_vol | rb__vessel_vol |
| coverage_wall_area | wall_area | rb__wall_area |
| coverage_replacement_event | replacement_cost_per_event | replacement_cost_per_event__replacement_cost_per_event |

[AGENT] Remove only the duplicate map key `fuel_handling`; retain that independent result and assert equality to `processing_cost`. Existing legacy fuel handling remains mapped. Require exact equality between the complete native numeric-output key set and independent returned mapped keys, and uniqueness of native producer values in the mapping. No values captured from execution are expected values. The proposed mapping names above are verified against the actual pipeline plus existing independent locals during review.

## Branch and numerical evidence

[AGENT] Use six bounded current-native validation points: current manifest baseline; cost mode0/energy1; cost1/energy0; cost0/energy0 with equipment disabled; zero discount; permitted major radius13m with other inputs fixed. These are implementation checks, not a design search or independent optimization study. If an input fails an existing domain requirement, preserve the failure and use a separately justified compatible input only for the unmet test obligation. Every executed row retains all authored verdicts and compares independent numeric quantities; no feasibility prerequisite.

[AGENT] In disabled mode, verify zero selected cooling annual/shipping effects while native equipment diagnostics follow their actual disabled behavior. Separate invalid-mode cases require explicit rejection for values outside{0,1}, and selecting effects on disabled equipment must refuse. For both CRF producer channels, independently compute `1 / sum((1+r)**(-year) for year in range(1,31))` at default r=.07 and r=0. Compare relative1e-12/absolute1e-14, justified by double-precision finite30-term accumulation and scale≈.03–.08; this is not a physical limit. Broader native/oracle comparisons retain established quantity-specific tolerances. No new tolerance applies to conductor predicates or raw margins.

[AGENT] The native item owns oracle exposure and new coverage test; the coding repair worker owns historical-compatibility/route tests. Subsequent cycle outputs must join full coverage before final integration. Any new cycle equation needs its separate source/design review, not automatic acceptance through this mapping plan.

## Newly executed domain finding — 2026-09-19

[AGENT] The first coverage run passed nine checks but cooling equipment disabled with facilities still live failed native evaluation: `cooling_helium_count must be positive`. The compatible disabled scenario must also disable facilities and its cost/capacity modes. The second run verifies all six compatible full-output cases plus invalid oracle modes, but reveals that the independent oracle still accepts cooling-off/facilities-live while native refuses it. Raw logs are retained. Proposed bounded repair: independently enforce the existing active-facility cooling-inventory requirement in the oracle and keep a dedicated native/oracle refusal test. This adds no physical acceptance limit and changes no supported comparison scenario; it closes a domain-parity omission. Fresh reviewer disposition is requested before that guard change.
