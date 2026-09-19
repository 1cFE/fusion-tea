# Fresh final review and R10.P grade

**Verdict: PASS. R10.P = 2; target P2 met.** Reviewed 2026-09-19 by fresh non-author session `/root/fuel_final_grade`, against the closed Round 1 result and corrected draft answer. The calculations support a conditional estimate for the represented fuel-system boundary. They do not qualify complete plant inventory, obtainable startup fuel or self-sufficiency. Formal goal closure remains owner-held.

## Unchanged-rubric cell record

| Field | Assessment |
|---|---|
| cell_id | R10.P |
| rubric_version | `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d`, generic P ladder, scoring rules and Row 10 |
| model_version | `956444b5d440238857911a0406e6d3f51ddcbf2e` |
| score | 2 |
| anchor_satisfied | “Tritium inventory, startup requirement, and processing throughput forward-computed, verified” |
| model_evidence | `models/library/analyses/mfe_fuel_cycle.sysml:93`; `models/library/structure/mfe_plant_systems.sysml:472`; seven bound stock occurrences starting at `:502`; `models/designs/generic_mfe/mfe_plant.sysml:103`; stellarator activation/scenarios at `models/designs/stellarator_09/stellarator_plant.sysml:1405` |
| runtime_evidence | Normative manual implementation `work/active/WI-069_fuel-inventory-and-startup/seeds/fuel_inventory_impl.py:17`, matching generated implementation; native `evidence/integration/integration_return.json`; study `results/package_identity.json`, baseline and all-point comparisons |
| study_evidence | `exploration/stellarator_e2e/studies/20260919-fuel-inventory-and-startup/@3529f6c8b070641f6c12a3632a3241ddb536decf`: `record.md`, `report.md`, `results/points.csv`, `results/native-cases.json`, retained SQLite store, independent scan and verification |
| why_not_next | The full calendar-dependent self-sufficiency feasibility coupling and physical fuel-system limits required for R10.P3 are not established; a running breeding screen and diagnostic annual supply balance do not establish that closure. |
| grader | `/root/fuel_final_grade`, fresh session without inherited author conversation; authored no reviewed model, oracle, study, source review or rubric |

The generic P2 evidence test is met for all three governing quantities. Residence, recovery and reserve inputs can be declared scenario assumptions at this level when their source basis and limits are explicit. Requiring qualified reactor-specific process hardware would raise the target beyond its unchanged forward-calculation test. Conversely, throughput alone would not earn this grade. No R10.S or other row is regraded here.

## Scientific and numerical checks

The original-image [source/design review](source-design-review.md) and [mathematical review](math-precheck.md) remain valid for the implemented boundary. Their source scenarios, combined cleanup/separation topology, deterministic return-delay approximation, plasma prefill and conservative decay argument are unchanged. I reused those original-source checks rather than claiming a new PDF inspection. I independently read the declared equations, final normative implementation, oracle interval integration, canonical stock bindings and generated plasma/calendar dependencies.

Exhaust stock uses unburned inlet flow before the permanent recovery loss. Both breeding stages use gross production; extraction loss applies once at the outlet. Plasma stock integrates the density profile. Feed, plasma, buffer and reserve are prefilled once; the cumulative supply deficit fills the initially empty processor while breeding fills its own stages. The decay allowance bounds decay of both the initial purchase and the allowance itself, with abstract replenishment access. This is coherent nominal accounting, not an exact decaying transport model.

I independently integrated the piecewise constant startup withdrawal in kg across return-time intervals for all 26 retained cases. Every maximum and prefill-plus-reserve total matched the native result. I also checked flow conservation and calendar throughput identities at every case, and joined all 1,820 new-output values in `points.csv` exactly to the 70 native output channels per case. Reference results are 2.380405 kg working stock, 2.037548 kg reserve, 4.417953 kg represented total, 4.398468 kg initial supply before decay, 0.001656 kg decay allowance and 4.400124 kg conservative startup supply. Running processor demand is 7.742681 kg T/day or 12.911794 kg D+T/day; annual T processing is 2,551.320892 kg. Annual decay replacement is 0.248386 kg. The maintained and passive-shutdown policies remain distinct.

I independently rejoined the retained oracle scan to all native cases and rechecked 23,556 scalar comparisons and 650 predicate comparisons. All pass. Classification comes from the model contract, because native serialized Boolean flags are numeric carriers: 914 numeric outputs plus 14 Boolean outputs are exported; the map covers 892 numeric plus 14 Boolean channels, leaving 22 inherited numeric outputs unmapped. All 70 new channels are mapped. No case passes all plant predicates. The reference failures are divertor heat, reference conductor current, conservative breeding and winding-pack fit. The finite list spans 1.091110–10.530596 kg represented stock and 1.086605–10.514651 kg conservative startup supply; these are scenario extrema, not uncertainty bounds.

The [implementation audit](../../../../active/WI-069_fuel-inventory-and-startup/audit.md) supplies additional independent domain, hand-case, profile-quadrature, decay and off-reference evidence. I inspected the relevant test construction and final logs: 75 author tests and 195 affected oracle tests pass. Its 700 off-reference comparisons and strict 70-output baseline are reused with the matching final executable identity. The earlier 218-test battery predates final arithmetic guards and is not represented as a final full-suite run. Retained failures and their repairs remain visible. Static validation remains failed at inherited L2/L6 diagnostics and three explicitly classified new EXPOSE diagnostics; runtime binding evidence does not turn those static errors into passes.

## Identity and evidence custody

The native integration return accepts the reviewed candidate with semantic fingerprint `1d97071e32b40888ef206f0c403250a28a9ecfad7e921797546f0a3ddcc0c1ef`, executable fingerprint `e19b63a03be3a00ebd5cec4ce4ed06a082f5bb7ed89b736aed06feaea8d1e319` and pin `9aaca3257606b22dd48d92b0074ee4076836e5b0fefd9b593369aa0915c4f1c2`. All ten integration gates pass within their stated coverage. The manifest gate explicitly does not check read-set coverage; the generic verifier's unrecorded teax revision is qualified by the snapshot and integration's recorded revision.

I checked all 38 model and 367 package hashes from the implementation audit, 448 snapshot-listed preparation/review/execution/definition artifact hashes, and the snapshot SHA256 `bcaf7f5723775c2e030be9635b0c3096bab43189b97ac5b3f94dd0cd6cae821a`. The model, package, twins and normative seed tree have no diff from the audited candidate; the frozen study has no diff from its study commit. The retained SQLite integrity check returns `ok`, contains 26 completed cases, and its case inputs and failed assessment headlines join to the exported native cases. The existing store-backup receipt supplies complete row-equality evidence. I checked all 17 numbered record sections and reused the coordinator's three passing native record tests. This is verification of existing custody, not a new packaging mechanism or a claimed cold reproduction.

The task's committed changes do not change the holdout or the inspected historical comparison paths. The quarantine protocol was read before evidence inspection; no barred source, excluded concept or sealed PDF was opened. Pre-existing unrelated edits are outside this review and are not attributed to this goal.

## Round 1 and learning dispositions

T-001 established the source/accounting basis, T-002 implemented and independently audited the released contract, and T-003 integrated one candidate and executed one finite study. These returns match their recorded scopes and the owner's nine required results. The two retained verification failures are mechanical: one count assertion excluded Boolean outputs; one input join distinguished integers from equivalent floats. Their repaired code changes neither physical values nor case selection. No second native execution, hidden case removal or semantic retry is inferred.

Accept all four study finding dispositions in record §15 and the proposed Round 1 learning delta:

| Finding | Reviewed disposition |
|---|---|
| `20260919-fuel-inventory-and-startup#1` | Accept conditional source/process scope. Equipment, reliability and obtainable-supply couplings remain unresolved; do not interpret graph reachability as qualified performance. |
| `20260919-fuel-inventory-and-startup#2` | Accept distinct working stock, startup purchase and recurring makeup channels. The verified delay and fill accounting explains their difference. |
| `20260919-fuel-inventory-and-startup#3` | Accept the named isotope-specific running and calendar costing interface, including its applicability and per-module limits. |
| `20260919-fuel-inventory-and-startup#4` | Accept preservation of every failed plant screen and the limits on self-sufficiency interpretation. |

The accepted claims now appear in the goal's `learnings.md:5`; `trail.md:99` records this review and its corrections. I checked the four joined `declared seam` dispositions at `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:710`. All four findings have a durable destination and preserve the conditional scope. No dependent semantic implementation follows within the P2 goal. The updated answer cites this grade. The frozen study and audited model/package remain unchanged after these administrative joins.

## Corrections and recommendation

Two factual findings were corrected by the coordinator and rechecked before this verdict. The current WI-069 audit now states the exact 892 numeric plus 14 Boolean mapping and 22 unmapped numeric channels. The frozen study's copied audit retains its historical erroneous eight-unmapped statement; the final schema census and this review supersede that count. The draft answer's required-breeding value was corrected to 1.191670: both native fuel and adequacy channels give 1.1916699222592924. Neither correction changed the model or frozen evidence.

Recommend owner closure on the reviewed P2 answer; the accepted learnings and joined discovery references have landed. Unsupported retention, permeation, bypass, detritiation, actual PbLi residence, reserve reliability, supply procurement and physical startup delivery remain material limits of the conditional estimate. They do not erase the verified P2 calculations and do not confer P3. This review does not close the goal, authorize reveal, replace the frozen comparison, or authorize merge/push.
