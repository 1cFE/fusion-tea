# Current processing flows and cost boundaries

## Finding

The verified running fuel-flow interface exists. The live processing capital account still follows net electric power, so it does not meet the throughput-cost target. No model change has been made in this assessment.

## Exact producer and checked version

WI-069 owns `Fuel Inventory` in models/library/analyses/mfe_fuel_cycle.sysml:93, its typed implementation under exploration/stellarator_e2e/generated/handwritten/mfe_fuel_cycle/, and its wiring in models/library/structure/mfe_plant_systems.sysml:472. The audited producer commit is 956444b5d440238857911a0406e6d3f51ddcbf2e. The model trees, generated package and independent oracle/adapter are unchanged at entry 86333b0de799e2332c01d489d400f8028bdb6d87; inspect_entry.py checks those paths against the audited commit. The retained native study is exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/@3529f6c8. Its original integration fingerprint is e19b63a03be3a00ebd5cec4ce4ed06a082f5bb7ed89b736aed06feaea8d1e319.

Fresh command `.codex-test/run python -m pytest tests/models/test_fuel_inventory.py tests/models/test_fuel_inventory_oracle.py -q` passes 144 tests, with 13 serialization warnings. The second file includes native off-reference comparisons and independent conservation/time-domain checks. See entering-fuel-tests.log. This is targeted verification, not a complete plant regression run. The upstream static L2/L6 limitations remain disclosed in the upstream audit.

## Capacity contract

Let B be the computed T-atom burn rate and f the single-pass burn fraction. The upstream producer calculates injected flow B/f and exhaust flow U=B/f−B. Recovery acts once at the processor outlet, so cost capacity must not use recovered flow rU in place of inlet U. The cost model will consume outputs rather than repeat these balances.

All outputs below are per fusion module; the current instance has one. Prefix: `stellarator_09__stellaris__fuel_cycle__inventory__`.

| Output | Meaning | Retained reference value | Applicability |
|---|---|---:|---|
| `exhaust_kg_day` | T mass entering combined cleanup/separation per running day | 7.7426808959 kg T/day | Not total isotope or gas mass |
| `dt_processor_kg_day` | Combined D+T mass entering that processor per running day | 12.9117940450 kg D+T/day | Equal isotope atom rates; excludes helium, impurities and carriers |
| `production_kg_s` | Gross T produced by breeding | 5.6507700102e-6 kg T/s | Not PbLi circulation or extraction-equipment gas flow |
| `extracted_kg_s` | Usable T after extraction loss | 5.6507700102e-6 kg T/s | Equals production only in the current unity-efficiency case |
| `startup_conservative_kg` | Conditional initial external stock, including decay allowance | 4.4001242157 kg T | Inventory, not processing capacity |
| `defined_flag` | Upstream physical interpretation flag | 1 | Production-dependent quantities cannot be interpreted at flag 0 |

The exact inventory interface is work/orchestration/goals/fuel-inventory-and-startup/evidence/throughput-interface.md. Annual amounts and calendar-average flow must not size running equipment. A conversion to molecular flow must state the atom-to-molecule convention; a conversion to standard gas volume must state reference pressure and temperature. No total-gas composition, impurity load, product purity, process pressure, redundancy or design margin is established by these flow outputs.

## Process and account map

This maps current ownership and candidate costing boundaries. It does not select a new technology or claim that every listed function has a supported price.

| Function | Current model representation | Existing price/account | Consequence for new processing estimate |
|---|---|---|---|
| Exhaust cleanup and isotope separation | Combined `exhaust_processor` stock at U, with declared residence time and one outlet recovery loss | Broad C220500 fuel handling | Primary throughput-cost candidate; source must support actual feed convention and combined scope |
| Purification | Included only functionally in combined cleanup; no separately specified process | No separately priced train | Do not add an independent purification cost if aggregate source already includes it |
| Storage and delivery | Working/reserve stock and feed-equipment stock; storage policy and residence assumptions | Broad C220500 may overlap; separate fuel building is civil scope | Source must distinguish storage equipment from fuel commodity and building |
| Blanket release and extraction | Breeder-zone and extraction stocks, gross/usable T rates | No individually identified extraction price | T mass alone does not size PbLi handling; price only with an applicable extraction basis |
| Fueling hardware | Feed-equipment stock represents injection residence, not a hardware design | No separately traceable complete fueling equipment price established | Require explicit aggregate inclusion or disclose omission |
| Torus vacuum pumping | Separate `Vacuum Pumping` part and gas-load calculation | Vessel shell is priced; no separately sized pumping-train price in that part | Do not equate processor flow with a purchased vacuum system; disclose present price incompleteness |
| Fuel-processing/storage building | WI-068 `fuel_building` and controlled ventilation | Facilities/civil account in CAS21 | Exclude building/HVAC scope from new equipment price, or subtract overlap explicitly |
| Safety and containment | No complete independently priced tritium safety train; C220500 is labeled processing plus containment | Broad legacy account plus building ventilation | Replacing C220500 retires its full allowance; missing containment scope cannot be claimed retained implicitly |
| Recurring fuel purchases | Reaction-priced D and Li-6 with burn/recovery correction | CAS80; $550,716.18 raw annual baseline | Separate from process capital; does not purchase annual circulating T throughput |
| Startup stock purchase | Separate power-scaled allowance | CAS50 startup base $40 million per 1000 MW net | Not yet driven by computed startup inventory; keep separate and disclose proxy rather than include again in process capital |

The actual fuel-building instance has a provisional 30×20×8 m equipment envelope (models/designs/stellarator_09/stellarator_plant.sysml:1556), with civil/ventilation costing under WI-068. These dimensions do not qualify processing equipment. Earlier proposal tables are not a substitute for this implemented value.

## Existing capital path and overlap checks

`Fuel Cycle.fuel_handling` in models/library/structure/mfe_plant_systems.sysml:560 invokes `Plant Power-Law Cost`: C220500 = $120,000,000 × (n_mod × p_net / 1000 MW)^0.7. The instance source is 1costingFE costing_constants.yaml and cas22.py; its label is “DT tritium processing + containment.” The retained native reference is $120,746,472.20. Neither its exponent nor reference price can be transferred automatically to a throughput law.

The cost exposes through `fuel_handling_cost` to models/designs/generic_mfe/mfe_plant.sysml:500 and is added once into CAS22, then CAS20, indirect costs, supplementary cost and the two LCOE calculations. A replacement must enter this existing summand or explicitly retire it. The current generic installation-labor base is power-core plus remote-handling capital (same file:463), so it does not automatically install fuel-processing equipment. Existing aggregate shipping/tax/insurance and indirect charges do respond to this account; any source-installed estimate needs a scope comparison against those charges.

CAS50's startup allowance remains separate (mfe_account_costs.sysml:652); CAS80 flows through `cas80_calc` (generic plant:650). Current LCOE is $273.454649/MWh for the lifecycle form and $268.288850/MWh for the separate 1costingFE form. These are retained upstream results, not a new study or complete-cost assertion. See entering-evidence.json for exact values and provenance.

## What remains unresolved before implementation

An applicable source must provide the process scope, reference capacity convention and composition, price/currency/year, installed versus purchased treatment, supported scaling or modular replication, scale applicability and redundancy. The existing architecture supports a combined exhaust processor, but its unspecified technology and gas composition may require a material owner decision. Neither an unrelated power proxy nor an inventory-driven source can satisfy the throughput criterion by renaming its input.
