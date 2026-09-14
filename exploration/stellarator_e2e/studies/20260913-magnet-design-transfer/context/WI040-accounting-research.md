# WI-040 winding-pack accounting research

Date: 2026-09-13 (local; native run stamped 2026-09-14 UTC). Consumer: REQ-040-02 / WI-040. Author: fresh clean reader `/root/accounting_research`. Scope: accounting form and manufacturing estimate, not material prices/densities or model implementation.

## Result

Native outcome: **REGISTERED**. Run and receipts: `knowledge/research/requests/runs/REQ-040-02/20260914T042427532598/`; exact result: `return.json`. Three sources registered. BLS direct access returned HTTP 403 and remains in the native operator queue; the Federal Reserve's accessible republication supplies the needed annual CPI values, so that queue does not block this recommendation. The three-capture budget is spent. No bounded negative was written.

[AGENT] Replace the unsplit tape-cost multiplier with **tape procurement + separately sized non-tape procurement + a separate winding-operation estimate**. Estimate winding operations from composite-conductor metres multiplied by the historical PROCESS winding rate, converted to a declared common dollar year and multiplied by an explicit transfer factor. Keep the old 6.65 calculation as a named comparison. This is an independently sourced accounting form with a disclosed transferred manufacturing estimate; it does not recover the historical multiplier's content.

## Registered evidence

| Source | Citable repository path | What it establishes |
|---|---|---|
| [UKAEA PROCESS original cost implementation](https://ukaea.github.io/PROCESS/source/reference/process/models/costs/costs/) | `knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md` | `acc2221`, lines 4307–4433: separate conductor, winding, case, intercoil structure, gravity support terms. Lines 4346–4381 separate superconductor/copper from sheath/fixed additions. Lines 4384–4396 calculate winding cost from conductor metres and a winding rate. |
| [UKAEA PROCESS cost-variable definitions](https://ukaea.github.io/PROCESS/source/reference/process/data_structure/cost_variables/) | `knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md` | Lines 37–44 and 1215 identify the original model as 1990 dollars. Lines 2724–2731 give `ucwindtf = 480.0`, cost of TF superconductor windings in dollars/metre. Lines 917–944 distinguish fixed cable cost and steel conduit/sheath cost. |
| [Federal Reserve Bank of Minneapolis annual CPI table](https://www.minneapolisfed.org/about-us/monetary-policy/inflation-calculator/consumer-price-index-1913-) | `knowledge/sources/federal_reserve_bank_of_minneapolis_annual_consumer_price/output.md` | Lines 11–15 give the dollar-year conversion and annual-average table. Lines 556–560 give 1990 CPI 130.7; lines 801–805 give 2025 CPI 321.9. Lines 808–815 give an explicitly estimated 2026 CPI of 334.4, based on the change from second quarter 2025 to second quarter 2026. |

The native registry owns ingestion and records source/extraction hashes in each receipt. Captured HTML and extraction were checked against each other for the accounting equations and selected coefficient/CPI values. These are HTML/code sources, so no PDF table extraction is involved.

## Why the current factor is insufficient

[INHERITED: `work/completed/20260901_WI-035_magnet-closure/design.md`, D4 and Risk 4] The live formula multiplies winding ampere-metres by tape price and 6.65. D4 recomposes 6.65 from an appropriated copper fabrication factor 3.5 and nonplanar factor 1.9; Risk 4 explicitly calls that content mapping contestable. Neither passage supplies a procurement/manufacturing split. Current implementation: `models/library/analyses/mfe_magnet_cost.sysml`, `Winding Pack Cost`.

Adding independently priced copper/steel/solder/helium to that whole factor would leave unknown overlap. Subtracting their price from the factor to preserve the old total would merely fit the old total. Neither operation establishes an engineering manufacturing cost.

## Recommended equation and boundaries

[AGENT] Use the following scoped estimate, with each subtotal separately visible:

```text
K = n_coils * I_coil_A_turn * f_set * circumference_m / 1000  [kA m]
L_turn = 1000 * K / I_operating_turn_A                      [m]
C_tape = K * tape_price_per_kAm                           [project-year dollars]
C_non_tape = sum(mass_i * procurement_price_i)             [project-year dollars]
C_winding = L_turn * 480 * (CPI_project_year / 130.7) * f_transfer
C_wp_estimate = C_tape + C_non_tape + C_winding
```

The PROCESS length multiplier is `n_tf_coils * len_tf_coil * n_tf_coil_turns`, directly visible at source lines 4388–4390. It counts composite conductor turns, not the sum of individual tape lengths inside a turn. The division by operating turn current is a dimensional derivation for this project's ampere-metre representation. It assumes a common operating turn current across the coil set; variable currents require a summed coil-by-coil length or a justified effective current. A published maximum current is not an observed mean operating current.

[AGENT] A 50 kA operating-current assumption can give a runnable initial estimate if separately cited to the admitted Stellaris maximum by the implementation reader. At fixed ampere-metres it gives the shortest winding length allowed by that current ceiling. Lower current increases winding cost. This reader did not reverify that Stellaris source datum; the coordinator identified it as source prose. Keep its assumption grade when adopting it.

[AGENT] Use **estimated 2026 purchasing power** for an initial nominal estimate alongside the coordinator's identified 2026-era procurement inputs: `334.4 / 130.7 = 2.558530986993114`, giving 1228.0948737566948 dollars/metre before the transfer factor. The captured source explicitly labels 334.4 an estimate based on second-quarter changes; it is not a final annual 2026 observation. A completed-year alternative is 2025: `321.9 / 130.7 = 2.462892119357307`, giving 1182.1882172915073 dollars/metre. Preserve both as sensitivity choices. Source capture occurred 2026-09-14 UTC, or 2026-09-13 local time. CPI is a general purchasing-power proxy, not a specialized coil-manufacturing escalation index. This convention does not establish whole-plant price-year consistency or normalize all inherited material prices; the material research worker owns their dates and nominal-price limitations.

[AGENT] Use the inherited 1.9 only as an explicit **transfer assumption**, if continuity with the existing nonplanar allowance is desired. This investigation did not independently establish 1.9 from a clean NCSX procurement/manufacturing source. It must not be called a validated universal stellarator penalty. Keep the rate and factor separately settable. Setting the transfer factor to 1 defines the historical TF-winding reference, not a proven stellarator lower bound.

The rate is documented as a winding cost, not specifically a labor-only wage rate. Do not rename it labor cost or assert that it includes all insulation, joints, testing, tooling, cooling fabrication and integration. These coverage uncertainties remain part of the transferred estimate.

[AGENT] Do not add PROCESS's `cconshtf = 75 dollars/metre`: its stated scope is steel conduit/sheath, which overlaps the proposed explicit non-tape steel account. Do not also add its copper or superconductor costs when procurement is already separately sized. PROCESS's `cconfix = 80 dollars/metre` is a separate fixed superconducting-cable cost. Its applicability to the proposed REBCO winding construction and tape procurement scope is unresolved. The selected narrow winding-operation estimate excludes that term; this is a disclosed scope limitation, not a claim that cable manufacture is free. If cable manufacture is later included, establish its material/process boundary first.

Keep coil casings, intercoil supports, cryoplant and other magnet equipment in their existing separate accounts. The new winding estimate does not certify their completeness.

## Numerical illustration and sensitivity

[EXAMPLE; AGENT] Using the inherited WI-035 `K = 1.608e7 kA m` solely to illustrate the new equation, an assumed 50 kA turn current gives 321600 conductor metres. At the CPI-adjusted estimated-2026 rate, winding operations are $394.955 million with factor 1, or $750.415 million with factor 1.9. The completed-2025-year alternative gives $380.192 million and $722.364 million respectively. These are equation evaluations, not procurement quotes and not calibration targets. They were not chosen to reproduce the old $5.3466 billion winding-pack total.

[AGENT] The smallest useful study varies the winding-rate multiplier at 0.5, 1 and 2 times the selected transferred rate and operating turn current at 25, 40 and 50 kA, holding ampere-metres/material masses fixed for an accounting-only comparison. These are exploratory scenarios, not confidence bounds. Then vary winding-pack side/volume through the actual model to expose independent material growth. A tape-price-only perturbation must change tape procurement and leave winding operations unchanged; a non-tape volume perturbation must change that procurement and leave the fixed-length operation term unchanged; a current-at-fixed-ampere-metres perturbation must change operation cost inversely with turn current. Those separations test whether the replacement has actually removed the hidden tape-price-dependent fabrication assumption.

## Authority and limits

- Source-established: PROCESS's additive account structure, composite-conductor winding length, 480 dollars/metre historical coefficient, 1990-dollar model basis, and annual CPI values.
- Derived: the ampere-metres/current length identity, CPI ratio and illustrative arithmetic.
- Agent assumptions: transfer to nonplanar REBCO windings, CPI as manufacturing escalation proxy, a common effective turn current, and use of inherited 1.9 as an explicit transfer factor.
- Unresolved engineering scope: manufacturing process coverage beyond winding, construction-specific fixed cabling expense, actual operating turn current, yield/scrap/rework/tooling and production-learning behavior. This report supports a scoped engineering estimate, not a validated complete factory cost.

No domain insight was approved or minted. No model, test, generated package, specification or goal-trail file was changed by this reader.

## Clean-room handling

Read the protocol and the committed clean-reader brief before fetching. Never opened the previously contaminated external account-justification document, sealed PDFs, or barred sources. Each fetched PROCESS/CPI candidate was screened with boolean-only checks for quarantine identifiers before reading; all three keeper screens were clear, and native registration's holdout checks accepted them. Search snippets were used for discovery only. No quarantined design/cost datum entered this research report. Boolean term checks are not a blanket guarantee of provenance; the inspected keeper contents support the narrow accounting claims above without reactor-design comparison data.
