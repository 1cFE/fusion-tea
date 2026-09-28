# Final independent review and R10.S grade

**PASS. R10.S = 2, meeting the unchanged target.** [AGENT] The selected processing account now follows verified operating D+T exhaust through an applicable, explicitly conditional source relationship into plant capital and both electricity-cost outputs. The frozen study demonstrates that chain under actual demand changes and separates it from price, capacity-margin and expenditure-date assumptions. No case demonstrates whole-plant feasibility. Formal goal closure remains the owner's decision.

Reviewer: `/root/source_review`, 2026-09-19; non-author of the model, oracle, study and rubric. This review reuses the original-source, price, controls, design and implementation reviews at their recorded scopes, and independently checks the newly frozen study and its interpretation. The immutable record was not edited.

## Grade record and exact identities

| Field | Assessment |
|---|---|
| `cell_id` | `R10.S` |
| `rubric_version` | `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d` |
| `model_version` | `2a50d3ec40e587af25beadaa9bd26c305b9ac11d` |
| `score` | `2` |
| `anchor_satisfied` | “Processing-plant cost follows computed throughput with source basis” |
| `why_not_next` | The four historical rows share an aggregate throughput law; processing subsystems are not independently sized subaccounts as required for S3. |
| Study commit | `2bae7fb7ffc204ca95e3daec16a349a5d7870f1b` |
| Snapshot SHA256 | `2dc662da935c99eefbe9ea127fba354cc1b3b0f3db0fd0f0b97034244fc2d069` |
| Executable fingerprint | `3e3bf467fd98ad927cf12409f1c36807b92e9e8eaa4fd598a2fcd79c00ae698f` |
| Semantic fingerprint | `37ca31ff0412f56a67301fa4e714b1dba2e74df6788348ce97dd5ee64d98d62f` |
| Indicator-input digest | `50c9d4b9b3bf16fdb00e5c726011f2b434bfa0ba8970569795372a12364c312b` |
| Recorded and reproduced TEAx revision | `8d877460ac4f6f264561d916e40c1708adb13397` |

Model evidence is the [processing definition](../../../../../models/library/analyses/mfe_fuel_cycle.sysml:258), [public inlet and selected account](../../../../../models/library/structure/mfe_plant_systems.sysml:459), [costed processing occurrence](../../../../../models/library/structure/mfe_plant_systems.sysml:523), [producer bindings](../../../../../models/library/structure/mfe_plant_systems.sysml:596), [CAS22 rollup](../../../../../models/designs/generic_mfe/mfe_plant.sysml:509) and [installation freight exclusion](../../../../../models/designs/generic_mfe/mfe_plant.sysml:578), at the model commit above. The primary [implementation audit](../../../../active/WI-070_throughput-based-fuel-processing-costs/audit.md) records the independently checked source-to-runtime chain and exact package hashes. Final study evidence is [the frozen report](../../../../../exploration/stellarator_e2e/studies/20260919-throughput-based-fuel-processing-costs/report.md), [record](../../../../../exploration/stellarator_e2e/studies/20260919-throughput-based-fuel-processing-costs/record.md), native stores and all-point verification at the study commit above. No R10.P regrade is made here.

## What was independently checked

The reviewer read the unchanged rubric's Row 10 anchors and grading protocol; the owner contract; study record, report and executor synthesis; snapshot and producer identity; full native cases; point table; scalar/predicate coverage; axis fan-out, indicators, rulings and window release; integration receipt; findings; attempt-1 rejection evidence; and cold-reproduction code and store. Earlier independent reviews establish source interpretation and engineering transfer rather than relying on source registration alone.

- **Frozen custody:** 542 distinct snapshot path/hash references, including the separately referenced indicator output, match both disk and committed bytes. This counting convention includes more than the artifact-array summary. Snapshot SHA256 remains unchanged. Package/model/TEAx identities join to the audited candidate and integration receipt.
- **Raw evidence joins:** All 20 retained cases join their exact eight-key proposals, candidate IDs and point-table rows. Seven hundred selected scalar/verdict CSV-to-native joins pass. Both the frozen native store and the author's external cold store match all 19,120 retained scalar outputs against the raw case artifact; all 20 assessments reject whole-plant feasibility. These are store/reproduction checks, not independent physical validation.
- **Fresh frozen execution:** The reviewer used the recorded cold route and copied frozen package/tools, selecting reference, burn-0.025, margin-1.5 and legacy-reference. All **3,824 native scalar comparisons** and their predicate comparisons pass. The external sample did not load the live model. Its receipt is [final-review/frozen-sample.json](final-review/frozen-sample.json), with the script and runtime log alongside it.
- **Study verification:** The committed independent arithmetic receipt passes **18,680 mapped scalar comparisons and 500 predicate comparisons** across all 20 points. All new processing and freight outputs are mapped. There are 934 unique mapped channels, including 14 Boolean outputs; the 22 inherited unmapped numeric channels remain explicitly named. The author's complete 20-case cold receipt was checked against its actual store rather than accepted solely from its summary.
- **Axis and attribution:** All eight single-key axes match their declared direct consumers in the frozen pipeline; no undeclared sibling tie was found. All five matched new/legacy pairs preserve 915 raw outputs outside the changed processing/financial path and identical physical verdicts. Independent charge identities reproduce every reported matched capital delta. Detailed receipts are [record-checks.json](final-review/record-checks.json), [store-checks.json](final-review/store-checks.json) and [attribution-checks.json](final-review/attribution-checks.json).

SQLite inspection initially created empty WAL/shared-memory sidecars despite read-only mode. The reviewer removed only those review-created sidecars after closing connections and continued with immutable read mode. The indexed database and snapshot hashes stayed unchanged; existing unrelated scratch symlinks were preserved.

## Engineering result and limits

The source driver is **12.911794 kg D+T per running day**, before recovery, not tritium-only mass, carrier-gas flow or annual throughput. The baseline four-row estimate is **$22.786229 million**, comprising $20.443420 million equipment and $2.342810 million direct installation in 2025 CPI purchasing power. At identical physical inputs, replacing the full $120.746472 million legacy allowance changes total capital by **−$141.271204 million**, headline LCOE by **−$1.870330/MWh**, and comparison-form LCOE by **−$1.829920/MWh**. Source direct installation and its CAS29 contingency are excluded from freight; no hidden legacy residual remains.

Burn fraction 0.025–0.10 produces 26.503156–6.116113 kg D+T/day and $28.272601–$18.210385 million process capital. Burn also changes existing recurring fuel, so the total LCOE response cannot all be assigned to processing. Matched legacy controls correctly isolate that distinction. Physical recovery changes losses and breeding adequacy while pre-loss processing capacity remains fixed; the distinct recurring-price recovery input remains held. Density changes native power and multiple plant systems; only matched account comparisons isolate the method effect. Downtime changes annual amounts and utilization, not running processing capacity.

Price multipliers scale the historical estimate; margin scales capacity under the published exponent; expenditure-date changes affect only the containment row and downstream costs. None provides a procurement confidence interval, demonstrated reliability benefit or preferred operating choice. Every study point retains at least one failed plant predicate, and no source-applicability declaration is presented as a physical qualification constraint.

The accepted engineering transfer joins the ORNL reactor-oriented cost method, original TSTA expenditure/scope evidence and larger conventional reactor-process design evidence. Owner adoption authorizes that conditional scenario; it does not measure impurities, certify cleanup/recovery or establish commercial performance. Limited containment, missing storage, blanket extraction/conditioning, complete fueling/safety systems, installation design, OPEX and replacements remain unpriced or incomplete as stated. CAS50 startup remains its old proxy; computed startup stock is not bought a second time. Package-local controls and the retained supervisory C220700 allowance have explicit separate ownership; the latter's unchanged coefficient remains uncalibrated to that residual scope. These qualifications are compatible with S2 and do not establish S3.

## Round assurance and dispositions

**Round 2 passes.** T-003 implementation and its non-author audit, T-005 exact-pin native integration and T-004 study execution form a joined evidence chain. The initial admission failure and one authorized numeric-representation retry remain visible. All 20 intended physical/monetary points were retained, including failed plant cases. The retry changes JSON representation of false to 0.0, not model semantics or the scientific window. The frozen record appropriately does not claim that the relocated first attempt is cold-reproducible.

| Proposed disposition | Review |
|---|---|
| Findings #1–4: margin, price, date and method selection have no constraint response | ACCEPT. Keep separate sensitivity-only qualification limits. No reliability, market-price, optimal-margin or physical-superiority conclusion follows. |
| Finding #5: burn attribution and distinct physical/recurring recovery inputs | ACCEPT. Preserve matched-control attribution and the current interface limitation. No new coupling or changed loss assumption is authorized. |
| Finding #6: all sampled points retain plant failures | ACCEPT. Retain failed points and decline feasible-optimum, complete-plant and self-sufficiency claims. |
| Finding #7: Boolean proposal admission | ACCEPT as resolved for this execution. Preserve original rejection evidence and the unchanged shared-route allowlist limitation for possible future tooling work. |

The proposed learning delta follows the observed evidence. These dispositions authorize no new scientific implementation, optimized setting, source premise, ARIES reveal, replacement freeze or formal closure.

Native integration passed all ten gates but explicitly omitted manifest read-set coverage; indicator checking does not close that omission. Static validation remains failed: ten inherited L2 identities and three added L6 EXPOSE-dot diagnostics beyond the existing residue. Actual generated execution checks those new bindings, without converting the static result to PASS. Serializer warnings and shared source/transport assumptions remain disclosed. No evidence-integrity finding changes the R10.S2 grade; no open corrective action blocks the coordinator's final answer. Owner-held closure remains separate.
