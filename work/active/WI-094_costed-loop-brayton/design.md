---
Status: active
Created: 2026-09-26
Updated: 2026-09-26
---

# Design: costed loop-Brayton assembly (WI-094)

Owner: reid · Created: 2026-09-26 · Spec: `spec.md` · Goal: `work/orchestration/goals/design-study-parameters/` round 1, T-003. Contract: the goal's `evidence/comparison-contract.md` (version 2, fresh-reviewed). Fresh design review 2026-09-26: PASS, five notes, all applied (goal `evidence/design-review.md`). Draft assembly text: `evidence/draft-costed_loop_brayton.sysml`; draft build script: `evidence/draft-build.py` (both this item's evidence, not yet under `models/` or `exploration/`).

## 1. Architecture

One new design directory `models/designs/costed_loop_brayton/` holding one SysML package `costed_loop_brayton` with one root part `plant`, generated into one native package `exploration/costed_loop_brayton/costed_loop_brayton_tea/` by `exploration/costed_loop_brayton/build.py` in the WI-093 pattern: stage the library sources and the design file, stock `sysml-codegen generate`, copy the reviewed completion bodies from the generated Stellaris and ARIES packages with only the import prefix rewritten (both forms, asserted reversible), regenerate with `--smart-regen --preserve-handwritten`, prove the fixed point, capture the snapshot, derive the entry-point census, hash everything. `run.py` executes named cases with per-case input overrides and stores every case's inputs, outputs and constraint report or refusal. `verify.py` checks identities on the stored outputs. The package also carries the study tooling the runbook route needs (§ 9). No library file, no completion body and no live assembly or package changes; the WI-093 combinations package is not edited.

Staged library files (11): `mfe_primary_loop`, `mfe_viability`, `integrated_heat_electricity`, `ideal_gas_brayton_components`, `integrated_equipment_costs`, `integrated_equipment_parts`, `costed_component`, `mfe_fuel_cycle`, `mfe_account_costs`, `mfe_lcoe_dcf`, `integrated_lifecycle_costs`. The assembly is the WI-093 C-1 text (`combinations_loop_brayton.sysml`) with the package and root renamed, the exchanger part specialised to 'Selected Equipment' with its purchase (the ARIES `he_hx` pattern), and the cost parts below appended; every C-1 binding and value is unchanged (the `electrical` part is byte-identical apart from its doc line after the review's note on attribute order), which is what makes the C-1 receipts a bit-exact control (§ 8). Cross-part references inside the root part are unqualified sibling references, the WI-093 shape (C-5's `circulator_equipment` reads its sibling screen the same way); the one shadowed name is owner-qualified (§ 1a); the generation test is the evidence they resolve.

## 1a. Generation test of the draft (scratchpad only)

The draft assembly with the eleven staged library files generates with the stock generator into the session scratchpad: 163 entry keys in four parameter groups (`costed_loop_brayton_params` 138, `integrated_equipment_costs_params` 13, `mfe_account_costs_params` 9, `mfe_viability_params` 3), 9 constraints (the eight C-1 checks and the fuel-stock screen `fuel_inventory__capacity_ok`), handwritten modules for the ten library packages and the design-level expression. One authoring correction was needed: inside `indirect_cost` the formal `direct_cost` shadows the sibling part of the same name, so the binding is owner-qualified (`costed_loop_brayton::plant::direct_cost.total`), exactly as the ARIES assembly qualifies it (`plant.sysml:1968`); the MODELING_PROCESS binding rule. The static validator on the staged sources passes levels 1, 3, 4 and 5 and fails levels 2 (literal-bound inputs such as `true` and `0.0`, warnings) and 6 (the documented cross-part binding class the ARIES and combinations packages also fail); no new class. Nothing was generated into the repository.

## 2. The unchanged C-1 physics (roles as WI-093 design § 2)

`blanket_source` (supplied heat, chosen), `primary_loop` ('Primary Coolant Loop'; flow calculated from duty and rise, the disclosed inherited direction; rated flow chosen and screened), `cycle` (chosen operating settings; `selected_flow` swept), `compressor_1..3` (chosen `selected_ratio`, swept together; fixed efficiency 0.89), `intercooler_1..2`, `pressure_loss`, `idle_branches` (representation quirk), `heat_exchangers` ('Network Heat Driven Closure', calculated), `turbine`, `recuperator`, `precooler` (calculated), `electrical` ('Plant Electrical Balance'; the exhaust-driven fuel term stays 0, contract § 3), five rating screens (installed capacity, chosen, screened), `checks` (heat removal, net positive, loop capacity: requirements). Values and grades exactly as the WI-093 design § 2 and the goal's `starting-configuration.md` § 6.

## 3. The cost parts (new bindings of existing definitions; every value `[INHERITED: ARIES]` unless marked)

| Part | Definition / bindings | Values and grade | Role |
|---|---|---|---|
| `fusion_source` | attribute `p_fus` | 2,652.5631770825056 MW `[INHERITED: Stellaris baseline p_fus, the power behind the supplied blanket heat]` | chosen (supplied; feeds only the fuel chain) |
| `fuel` | 'Fuel Cycle Flows' as ARIES `plant.sysml:110-141`: p_fus_in = fusion_source.p_fus; I_total_in = fuel_inventory.selected_tritium_atoms | ARIES fuel constants (17.58 MeV, 0.05 burn fraction, 0.99 recovery, decay constant, 1 extraction, 0 growth) | calculated burn, inject, exhaust, loss rates; constants of the sweep |
| `cost_accounts`, `cost_schedule` | attributes | estimate_mode 0, one_module 1; availability 0.85, plant_years 40, replacement_life_fpy 5, replacement_factor 1 | chosen conventions |
| `he_hx : 'Selected Equipment'` | 'Selected Inventory Purchase' on `selected_area` (50,000 m², reference 50,000 / 58,325,700); 'Exchanger Area Conductance' | as ARIES `plant.sysml:723-749` | installed (UA) and purchased (capital) from the chosen area |
| `compressor_equipment`, `turbine_equipment`, `generator_equipment`, `heat_rejection_equipment`, `he_duty_equipment` : 'Selected Equipment' | 'Selected Inventory Purchase' on the sibling screen's `selected_rating` (`compressor_capacity.selected_rating` etc.); references 1,600 / 78,639,500; 3,500 / 125,823,200; 1,800 / 47,183,700; 2,500 / 56,086,000; 1,500 / 32,403,166.67; cas 23 / 23 / 23 / 27 / 22.2 | as ARIES `plant.sysml:801-819, 1050-1125` | purchased from the selected rating (never from demand); `cost_extrapolated` published |
| `conversion_services : 'Selected Equipment'` | 'Scaled Amount' + 'Supplied Purchase Cost', fixed 62,911,600 | as ARIES `:1145-1162` | fixed budget |
| `rest_of_plant : 'Selected Equipment'` | 'Scaled Amount' + 'Supplied Purchase Cost', 2,158,230,133.3333335 | `[ASSUMED: held equal; contract § 6: the sealed ARIES direct source scope 2,619,603,000 less the seven priced items 461,372,866.67]` | supplied constant |
| `fuel_inventory : 'Selected Equipment'` | as ARIES `:1595-1666`: 'Selected Stock Atoms', 'Scaled Amount' (stock cost), 'Annual Selected Fuel', 'Offered Capacity Screen' + 'Offered Equipment Capacity' on the stock, 'DT Fuel Cost' with p_fus = fusion_source.p_fus | 10 kg, 1,000 s, feed 0 (no-credit), 30 MUSD/kg, deuterium 1,000 USD/kg | stock chosen (capital); makeup calculated (operating); the stock screen is a constant requirement |
| `priced_equipment` | 'Eight Amount Sum' of the seven priced items | | calculated |
| `direct_cost` | 'Eight Amount Sum': rest_of_plant + priced_equipment + fuel_inventory.capital_cost | | calculated |
| `indirect_cost`, `contingency_basis`, `contingency`, `owner_commissioning` | 'Indirect Cost' (0.2; 6 / 6 years), 'Eight Amount Sum', 'Contingency Cost' (0.2), 'Scaled Amount' (0.05) | as ARIES `:1965-2007` | calculated |
| `annual_om` | 'Annual OM Cost' with om_direct 70,000,000 and the ARIES literal p_net/ref (flat) | as ARIES `:2008-2020` | chosen allowance |
| `replacement_scope`, `replacement` | 'Scaled Amount' on `selected_event_scope` 72,231,350 × replacement_factor; 'Replacement Events' | `[ASSUMED: the ARIES nominal event, held equal; contract § 3]`; as ARIES `:2051-2066` | supplied scope; calculated schedule |
| `cost_ledger` | 'Equipment Cost Ledger' with net_power_in = electrical.net_electric; consumables 5,000,000; import price 50; the source-comparison inputs 0 (`no_source_comparison`) | as ARIES `:2067-2107` | calculated overnight, annual operating, annual export MWh |
| `finance` | attributes | 0.05; 6 years; 0.1; 0.02; 0.05 at 20; supply service 0 | chosen conventions |
| `operating_levelization` | 'Levelized Annual Cost' | as ARIES `:2128-2139` | calculated crf |
| `lifecycle_accounts` | 'Lifecycle Cashflow Accounts' with net_power_in = electrical.net_electric and the fuel channels from fuel_inventory | as ARIES `:2148-2219` | calculated LCOE and its eleven contributions |
| `lifecycle_price` | 'LCOE DCF' | as ARIES `:2220-2232` | calculated lcoe (the headline; equal to lcoe_sum) |

Differences from the ARIES chain, each disclosed: the cost ledger's source-budget comparison inputs are 0 (no source comparison in this assembly; `direct_difference` then equals `direct`); there is no `plant_ledger`, so the ledger and lifecycle read `electrical.net_electric` directly (C-1 has no 'Integrated Plant Ledger'); the replacement scope is a supplied constant rather than the sum of assembled inventories; the rest of the plant is one supplied constant rather than thirty leaves.

## 4. MR-7 statement

No sizing rule is introduced. Every rating, area, flow capacity, pressure ratio, cycle flow, price reference and convention is a chosen value; demands are calculated and screened; purchases are computed from the selected ratings, never from demands; an inadequate selection stays a violated check with the selected rating's (lower) price. The loop's calculated flow is the disclosed inherited direction, screened against the chosen rated flow. The swept quantities (cycle flow, the three stage ratios) are chosen inputs; the fixed compressor and turbine efficiencies are model assumptions stated in the contract (§ 8 a), not choices. The fuel term is calculated from a supplied fusion power and is a constant of the sweep. Nothing in this assembly changes a role against C-1; the added parts add purchases and accounting only.

## 5. Reuse table (transfer register's measurement rule)

Definitions instantiated unchanged: the C-1 set (WI-093 design § 1) plus 'Selected Equipment', 'Selected Inventory Purchase', 'Exchanger Area Conductance' (already in C-1), 'Scaled Amount', 'Supplied Purchase Cost', 'Eight Amount Sum', 'Fuel Cycle Flows', 'Selected Stock Atoms', 'Annual Selected Fuel', 'DT Fuel Cost', 'Indirect Cost', 'Contingency Cost', 'Annual OM Cost', 'Replacement Events', 'Equipment Cost Ledger', 'Levelized Annual Cost', 'Lifecycle Cashflow Accounts', 'LCOE DCF'. Copied completion bodies with prefix adaptation only (24: 6 Stellaris including the `financial_factors.py` helper the levelization body imports, 18 ARIES including the two `common.py` helpers; list in `build.py`; count corrected 2026-09-26 at implementation, when the missing helper refused at runtime and was added). Mathematical changes: none. New definitions: none. New case bindings: every cost part.

## 6. Cases (development receipts, `run.py`)

The five WI-093 C-1 cases at their exact inputs (the control set: `run.py` compares every stored C-1 channel, key prefix `combinations_loop_brayton__loop_brayton__` mapped to `costed_loop_brayton__plant__`, against the sealed WI-093 receipt and expects exact equality; the 4,000 kg/s case has net −242.58 MW, so on this package the lifecycle body refuses it (`LCOE undefined for nonpositive net electricity`) and the pipeline stores no channels: that refusal, with the body's message and the refusing module, is its receipt, and the bit-exact comparison covers the four cases with positive net); the starting point on I-A ratings; and three cost-development points (the contract's best screen point 2,500 / 1.45 on I-R; the same on I-A; the S2 fuel-term case). Reading per case: executes / verdicts / net / unmet / purchases / overnight / LCOE and contributions.

## 7. Verification (identities on stored outputs, `verify.py`)

The C-1 identities (WI-093 design § 8) unchanged; plus: each purchase = reference cost × price factor × selected / reference, extrapolated flag against the 0.5–1.5 rule; priced total = Σ seven; direct = rest + priced + stock; indirect = 0.2 × direct; contingency = 0.2 × (direct + indirect); owner = 0.05 × direct; overnight = direct + indirect + contingency + owner; annual export MWh = 8,760 × net × 0.85; annual operating = om + tritium + deuterium + consumables + imports; the eleven LCOE contributions sum to lcoe_sum and lcoe_sum = lifecycle_price.lcoe; tritium annual cost = (burn + loss + decay − feed)⁺ × price; replacement count = ceil(40 / (5 / 0.85)) − 1 = 6; the control replay: every C-1 channel of the four positive-net control cases equals its sealed WI-093 value exactly under the key-prefix map, and the 4,000 kg/s control refuses at the lifecycle body with that body's message.

## 8. Registration and preservation

`tests/model_families.py` gains a `costed_loop_brayton` collection listing the 11 library files and the design file; the goal's preservation manifest is checked after the build; the Stellaris, ARIES and combinations packages and the library are byte-unchanged.

## 9. Study tooling (the runbook route on this package)

Under `exploration/costed_loop_brayton/studies/`: `study_route.py` (the ARIES route with this package's names), `interface_data.py` (generated from the discovered inventory and the starting-point receipt), `manifest.json` (baseline = the starting point, headline = `lifecycle_price__evaluate__lcoe`, verdicts = the nine checks, the fuel-stock screen included (it is a constant of the sweep, required ≈ 0.09 kg against 10 kg, and cannot flip), oracle block, the declared absolute tolerance classes from the contract § 9), `oracle_entry.py` (an independent re-derivation of the loop, the single-branch closure, the electrical balance, the purchases, the ledger and the lifecycle, publishing `operand_bindings` for the nine constraints; reuses the ARIES `equipment_oracle` and `lifecycle_oracle` arithmetic modules by import), `execute_study.py`, `ANNEX.md`, `DISCOVERY_LOG.md`. The integration seam is run on the sealed package to obtain the CANDIDATE the executor requires.

## 10. Review questions (for the fresh design review)

1. Does any binding in § 3 bind a formal that does not exist in the named definition, or mix units? Entry: this design, the draft `costed_loop_brayton.sysml`, `integrated_equipment_costs.sysml`, `integrated_lifecycle_costs.sysml`, `mfe_account_costs.sysml`, `mfe_lcoe_dcf.sysml`, `mfe_fuel_cycle.sysml`, `models/designs/aries_cs_integrated/plant.sysml`.
2. Is any quantity assigned a role that hides a sizing rule (MR-7), including the purchases on the sibling screens' selected ratings?
3. Is the cost chain single-counted as the contract § 6 states (rest-of-plant, priced items, stock, friction once)?
4. Is the control claim right: does the change from C-1 (the exchanger part's specialisation and added purchase; the appended cost parts; the fuel term left at 0) leave every C-1 channel's value unchanged?
