# Replacement comparison approval packet

[AGENT] **Recommendation: adopt this exact candidate for the agreed comparison, carrying the limitations below. Technical preparation and independent actual-archive reproduction are complete.** [OWNER] Adoption/publication and formal goal closure were authorized and completed on 2026-09-20; reveal remains separately owner-held. See [publication record](../../../../.project/active/aries-comparison-preparation/replacement-r3/publication.md).

Candidate archive: `.project/active/aries-comparison-preparation/current-readiness/candidate-archives/20260920-matched-cycle/comparison-freeze.tar.gz`. SHA256: `34526b8b4587a306453a1f01fa73e6803e4eddf04c3ae0d0f3e647b69a9dbd19`. It contains 1,047 files and is 5,692,124 bytes. Two independent builder invocations produced identical bytes; see `evidence/round2/archive-build-custody.json`. Adjacent `freeze-record.json` records the index hash and full candidate identity.

Scientific source checkpoint: `3093d1676d33fbb1e1677797f352c643de309d32`; reviewed coding/oracle base: `5fc805015609d8cdc47f00b2f6e16866af6233a2`. Semantic fingerprint: `989f6a4492157969ba4777347ab588f18547a5077161172be586e41310ad41a1`. Executable fingerprint: `7a9d297dbd8961b9e1dc15656360933d38871d93ee727e3173f7d73a171fa61f`. Runtime prerequisites and exact external identities are in the archived `runtime-requirements.json`; reproducibility requires that licensed runtime. Every finite local execution dependency is included; the base-only dependency map is empty.

## What the replacement changes

The replacement uses the current integrated stellarator and its reviewed steam-cycle calculation. The preserved r2 archive remains byte-for-byte unchanged. The candidate supplies updated input/output mappings, all current engineering checks, cost and power accounts, source and input-selection rules, retained validation receipts, explicit limitations and a deterministic reproduction procedure.

The previous 480°C conversion-fit argument described turbine inlet but was derived directly from 500°C helium, bypassing the 465°C salt supply. The new calculation uses actual salt heat and water properties, finite heat-transfer requirements, calculated feedwater heating, staged expansion/reheat, condensation and explicit steam/cooling-water pumps. It retains helium and salt technology and temperatures. The selected cycle states and performance factors are reviewed engineering assumptions, not measurements or owner-originated numbers.

## What stays unchanged

Derived-quantity agreement remains the inclusive ratio band [1/3,3]; component-cost agreement remains [0.5,2]. LCOE supports interpretation. The C220107 lineage exception remains excluded or footnoted. The existing source/input-selection policy, selected-forward controls, supplied-versus-calculated roles, missing/incompatible reference handling and immutable first-result requirements remain in force. No ARIES paper or excluded concept was opened during this work.

## Model results and limitations

At unchanged raw-default inputs, gross efficiency changes from 41.1357% to 36.8926%, exported electricity from 1008.898406 to 850.065301MW, and model LCOE from 271.584320 to 318.737170USD/MWh. Heat admitted and primary pumping are unchanged. Explicit steam and cooling-water pumps consume 9.706961 and 13.023180MW. These are corrected calculations under declared new cycle assumptions; they were not tuned to preserve old LCOE.

The preserved selected comparison controls produce 844.321933MW net electricity, 19.061495billionUSD overnight cost, 341.057865USD/MWh model LCOE and 334.542638USD/MWh comparison-convention LCOE. The fixed Table5-conditioned control is separate. Each passes 1,050 independent scalar/status comparisons, 28 exact predicate comparisons and 53 power/cost identities. Supplied quantities receive no independent prediction credit.

The same four engineering failures remain in both candidate cases: divertor heat, breeding adequacy, conductor current and winding-pack fit. A separate zero cooling-water temperature-gap test retains its failed physical check. Incompatible and invalid calculations retain their raw refusals. Numerical-comparison tolerances never change these engineering limits.

The first ARIES report must disclose unqualified steam-generator/reheater and cooling-water installed cost/capacity, conditional cooling-water site assumptions, possible overlap between explicit pumps and the retained 3% auxiliary allowance, simplified cycle loss/property assumptions, mixed-year money and source-transfer/reliability limits. Static validation remains non-clean: ten L2 warnings and 1328 L6 findings, with scoped dispositions against the tested execution path. Passing the executable checks does not certify unrelated static behavior, a feasible reactor or complete installed cost.

The two exact-boundary conductor discrepancies were traced to floating-point operation order. Independently reviewed tolerances apply only to the demonstrated scalar fixture comparisons. Raw negative margins and strict engineering verdicts remain unchanged. The old failed receipts and the numerical-policy review are retained; rounding a printed value to zero cannot turn a failure into a pass.

## Verification and depth

The omitted manifest input-file coverage check now verifies 511 inputs in 11 input files and 13 opened artifacts, and rejects uncovered or outside-package reads. All 1,050 numeric/status channels have independent calculation or explicitly labeled input/alias checks; the earlier 22 missing channels no longer lack numerical coverage. Native integration passed all ten gates without changing generated bytes. Fresh independent regrading finds all 23 scored depth targets met, with three not-applicable cells.

Full regression is complete: **3,585 passed, zero failures, zero errors, 14 ordinary skips and two strict expected historical incompatibilities**, accounting for all 3,601 collected cases. All 34 earlier failures/errors now pass. All 120 captured source/data hashes remain unchanged. The skips are 13 unused foundation/example fixtures and one absent historical proof-of-life database. The historical CLI success assertions retain exact refusal guards; the current adapter uses the complete current interface. Fresh independent WI-073 audit passes R1–R7. Evidence: coding `regression-evidence/cycle-migration/final-full-reconciliation.json`, `final-summary.md`, both final XML/logs, native WI-073 `audit.md`, and this goal’s `evidence/round2/cycle-regression-contract-review.md`. Actual-archive reproduction now passes; see the independent review below.

## Independent archive reproduction

[Fresh independent review](evidence/round2/archive-review/review.md) passes for the exact archive hash above. The reviewer restored all 1,047 files without borrowing working-tree sources, verified the recorded runtime and source assets, and passed **190 restored tests with zero failures, errors or skips**. Fresh selected-forward and Table5 executions each reproduce all 1,050 outputs, 28 predicates, 53 account identities and 276 export rows exactly. All five archived databases pass immutable integrity checks; the four candidate cases have exact result/refusal joins.

Two reviewer rebuilds match the archive byte-for-byte. A corrupted copy is rejected. An explicitly synthetic first-report exercise with the actual archive verifies twelve artifact joins, refuses a second original and preserves the original through a linked correction. Neither operating result register was created. The review's initial database-join helper confused adapter and native attempt identifiers; the corrected check and initial failed log are both retained. No candidate change was required.

The archived README and validation summary correctly describe archive review as an external gate. This external packet and review discharge it without modifying the reviewed archive. The exact predecessor r2 SHA256 remains `fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21`.

## Owner decision and remaining gate

[OWNER] The exact candidate above is adopted and published as r3; the goal is formally closed on 2026-09-20. The external publication record preserves the owner's exact instruction and verifies byte equality. All stated limitations and comparison criteria remain unchanged.

Separate owner authorization of ARIES reveal under `knowledge/holdout/aries-cs/PROTOCOL.md` remains required. The sole operating first-result register will be `.project/active/aries-comparison-preparation/current-readiness/revealed-results/`; it remains absent. An adverse first result remains immutable, and conditioned/corrected reports link back to it.

No merge or push is part of this publication.
