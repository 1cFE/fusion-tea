# Current-role and definedness overlay

[AGENT] This overlay implements the independently reviewed requirement that unavailable outputs never become predictions. The coordinator released implementation on 2026-09-20 after native coverage exposed a completed case with undefined breeding. Independent implementation acceptance must check these joins.

Historical `manifest.json` bytes and criteria remain unchanged. `v1/current-overlay.json` records the exact current producer substitutions and output flags. Casing and support mass rows now read independently supplied `magnet__casing__m_casing` and `magnet__m_support`; their roles are held or supplied. Source: WI-074 interface migration and `models/library/cost_structure/mfe_power_core.sysml`. All current predicate verdicts join their contract evaluation channels. A false verdict is a reported failed check, not an absent prediction.

| Export row | Required current output flags | Reason |
|---|---|---|
| `achieved_tbr` | `blanket__breeding__defined_flag` | Unsupported fixed-geometry response-table inputs produce undefined zero carriers. |
| `required_tbr` | `fuel_cycle__inventory__defined_flag` | The live fuel requirement consumes total inventory for decay; production-dependent total inventory is undefined when breeding is undefined. |
| `tbr_margin` | Both preceding flags | The raw margin uses available breeding and the inventory-dependent requirement. |
| `fuel_handling` | `fuel_cycle__processing_cost__defined_flag` | The selected processing cost has its own source/applicability flag, separate from inventory or breeding. |
| `turbine__matched_cycle__main_UA_MW_K` | `turbine__matched_cycle__main_UA_available` | A zero UA carrier with unavailable heat-transfer state is not an available conductance prediction. |
| `turbine__matched_cycle__reheat_UA_MW_K` | `turbine__matched_cycle__reheat_UA_available` | Same rule for reheater conductance. |

All keys use `stellarator_09__stellaris__`. Flags must be present, scalar Boolean/numeric and exactly one for availability. Zero makes the prediction undefined; missing or malformed flags make it unknown. The raw numeric carrier and raw flags remain available as diagnostics. Flag quantities themselves remain reported so the source limitation stays visible. Ordinary independent arithmetic, including annual purchased fuel, is not suppressed merely because breeding is unavailable.

Primary model contracts: `models/library/analyses/mfe_tritium_breeding.sysml:6` and `:32`; `models/library/analyses/mfe_fuel_cycle.sysml:120`; `models/library/analyses/mfe_matched_steam_cycle.sysml:90`; `models/library/analyses/mfe_account_costs.sysml:810`. Exact flags and bindings are checked against the generated contract and current outputs. These flags establish only the implemented model's available calculation domain, not physical validation or a wider source-transfer qualification.
