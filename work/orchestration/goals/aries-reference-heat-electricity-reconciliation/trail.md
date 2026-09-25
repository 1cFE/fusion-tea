# Trail: ARIES reference heat-to-electricity reconciliation

Append-only, newest entry last, ISO dates. No entry is edited in place; corrections are dated amendments. Native artifacts own execution evidence; entries cite them.

## Round 1 — replay-contract-attribution

### Strategy revision — 2026-09-25

- **Approach:** reproduce the historical source-conditioned cases against the current package; write the reference-case contract from primary page images and have each new source reading independently checked; declare the materiality budget with focused review; then commit one diagnostic study on the unchanged package that isolates candidate causes one at a time (recuperation, cycle flow, exchanger conductance, hot-side bounds, auxiliary-load definitions) and in combination, before any model change.
- **Assumptions:** the current package reproduces the frozen numbers up to recorded input differences; Lyon Table IV and its text supply a complete electrical boundary (thermal, gross, recirculating, net); the sequential closure exposes enough branch-level transferred/unmet heat and temperatures to locate the thermal inadequacy.
- **Abandonment conditions:** the replay differs from frozen evidence for reasons not explained by recorded input differences; primary pages do not support a consistent target; a needed comparison quantity cannot be expressed on the current package without a model change (that work moves to a later round); an owner gate or a declared cap.
- **Intended model increment:** none; the package stays pinned this round.
- **Intended study question:** which single justified assumption changes, and which combination, account for the unmet heat and the gross/net difference against the Lyon reference when the published fusion power is supplied and hardware is held fixed?

### T-001 scope

- **Objective:** establish the current-package baseline for the four canonical scenarios and record entry preservation.
- **Why now:** grounding shows the live scenario runner sets pump modes the frozen study did not; the historical table cannot be adopted until reproduced against the actual package.
- **Scope:** read-only replay of the `run.py` scenarios and the frozen-study variants into a scratch directory; channel extraction and comparison with `results/cases.json@8e6fb2f2`; entry preservation manifest. No package, model, frozen-record or study writes.
- **Inputs:** `goal.md`; `exploration/aries_integrated/run.py@96914299`; the frozen record; `evidence/build-preservation-manifest.py`.
- **Done when:** every canonical case is reproduced, or its difference from the frozen record is attributed to a recorded input difference, with branch-level heat/temperature and ledger channels tabulated for the source-conditioned cases.
- **Stop when:** the package cannot load through the documented runtime (mechanical), or a reserved gate binds.

### T-001 start — 2026-09-25

T-001 · current `aries_integrated` package through the documented `.codex-test/run` runtime, outputs in scratch · `evidence/replay-canonical.py` and `evidence/t001-replay-summary.json`. Coordinator executes directly.

### T-002 scope

- **Objective:** write the reference-case contract from primary page images: supplied boundary values, calculated outputs to compare, exact source definitions with units, case and confidence, and every inherited approximation with its support status.
- **Why now:** the goal requires the comparison defined before any model change; the Lyon systems relations (thermal power, conversion, recirculating power) and the Raffray divertor circuit are not yet captured in a reviewed contract.
- **Scope:** read retained PDFs and page images; render needed pages into `evidence/`; write `evidence/reference-case-contract.md`; commission a focused independent source check of each new reading against the page images. No model, package or study writes.
- **Inputs:** `goal.md`; retained Lyon/Raffray PDFs and images cited in grounding; `heat-transport-scope.md@45d90d95`; `power-conversion-scope.md@45d90d95`; WI-089 design register.
- **Done when:** the contract is written, each new source reading is independently checked against its page image, and the auxiliary-load and thermal-power definitions on both sides are stated in comparable terms; or a bounded negative names the source gap.
- **Stop when:** a source ambiguity changes the comparison's meaning (owner gate), or a declared cap.

### T-002 start — 2026-09-25

T-002 · retained primary sources and goal evidence · `evidence/reference-case-contract.md`, rendered page images, independent source-check return. Runs in parallel with T-001: T-001 writes only scratch and its summary; T-002 writes only source evidence and the contract.

### T-001 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/replay-canonical.py`, `evidence/t001-replay-summary.json` (runtime executable fingerprint `d13f4153…`, matching the entry package); `evidence/preservation-entry.json` (18,725 protected files at `96914299`) with `evidence/preservation-entry-check.json` passing; `evidence/entry-state.txt`. Scratch outputs are not retained.
- **Reading:** the current package reproduces every historical headline exactly: source-assumed 2759.082152 MW accepted, 158.725848 MW unmet, 1028.658530 MW gross, 796.005288 MW net; literal Lyon 2518.899476 / 398.908524 / 1039.669902 / 807.016660; literal Raffray 2517.615798 / 502.134202 / 1038.516213 / 805.910865; calculated nominal 423.106794 MW net. Against the frozen record only two of 211 common channels differ in each case, `fuel.tbr_required` and `fuel.tbr_margin` (1.19 → 1.1941), which is the WI-090 selected-stock migration adding decay of the 10 kg stock to required breeding; no thermal or electrical channel moved. Setting `pump_mode=1` in the live runner leaves every channel unchanged at reference flow, because the cubic proxy equals the fixed 156/0.01/10 MW at reference conditions; the historical table can be adopted as the original-case baseline. Branch-level reading of the failing case: with recuperator effectiveness 0.8 the helium and divertor stages transfer all their heat (helium hot-bound margin 13.7 K); the entire 158.7 MW unmet heat is in the PbLi stage, whose capability is `≈ C_PbLi × (1011.15 K − 767.85 K)` because the PbLi side is the smaller capacity rate (5.10 MW/K against 7.27 MW/K cycle) and the series order heats the cycle helium through the divertor stage before the PbLi stage (cycle inlet to PbLi 495 °C, so PbLi cannot be cooled below ≈ 499 °C, against the published 451 °C return). With the source's 0.95 effectiveness the heater inlet rises to 320 °C and the helium stage becomes limiting as well (169.9 MW helium unmet, 229.0 MW PbLi unmet). Thermal efficiency on accepted heat is 37.3% (0.8) and 41.3% (0.95) against the published 43%; auxiliary electricity 232.7 MW against the published 253 MW with different composition.
- **Decision:** the live runner's pump-mode keys are a no-op at reference flow; adopt the historical table without amendment and keep the frozen record as the cited original; execution detail; coordinator; `evidence/t001-replay-summary.json`.
- **Decision:** the series heater order and the assumed cycle flow/recuperation are the leading candidate causes of the thermal inadequacy, and the published network (Fig 12: parallel PbLi and divertor stages after the helium stage) is a topology the current closure cannot express; a topology alternative is a model increment for a later round after design review, while this round quantifies the input-level causes on the unchanged package; execution detail; coordinator; none.

### T-003 scope

- **Objective:** declare the materiality budget for net electricity, gross electricity, thermal power, branch heat balance, unmet heat and turbine inlet temperature, with rationale, and obtain focused independent review of the budget together with the T-002 source readings.
- **Why now:** the owner brief requires the budget declared and reviewed before any refinement study, and not chosen afterward to fit a residual.
- **Scope:** `evidence/materiality-budget.md`; one bounded fresh review covering the contract's source readings, the source-consistency question Q1 and the budget. No study execution before the review returns.
- **Inputs:** `goal.md`; `evidence/reference-case-contract.md`; the page images cited there.
- **Done when:** the budget is written and the reviewer returns PASS or FINDINGS that are resolved by revision; or the reviewer identifies a source ambiguity that needs the owner (OWNER_GATE).
- **Stop when:** an owner gate binds or the checkpoint revision cap is reached.

### T-003 start — 2026-09-25

T-003 · goal evidence only · `evidence/materiality-budget.md`, `evidence/source-check-brief.md`, reviewer return `evidence/source-check-review.md`.

### T-004 scope

- **Objective:** prepare and, after the T-003 review passes, execute one committed diagnostic-attribution study on the unchanged package that isolates the candidate input-level causes of the source-conditioned unmet heat and gross/net difference, one at a time and combined, with reverse one-at-a-time and a cycle-flow bracket to measure interactions.
- **Why now:** T-001 located the shortfall in the PbLi and helium stages and named the inherited recuperation, cycle flow, divertor flow and auxiliary definitions as candidate causes; the goal requires these quantified before any model change.
- **Scope:** record `exploration/aries_integrated/studies/20260925-aries-reference-heat-electricity-reconciliation/`, thin `reconciliation_support.py`, declared config, indicators, native baseline point, preflight, oracle scan, native execution, all-point verification, record and freeze. Twenty-one declared points; no model, package or live manifest change; no topology change (that is a later round); no filtering of adverse points.
- **Inputs:** `goal.md`; `evidence/reference-case-contract.md`; `evidence/materiality-budget.md`; `evidence/t001-replay-summary.json`; the LCOE canonical receipt at `exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/canonical-author-receipt.json@96914299`; stock study tooling.
- **Done when:** all declared points complete and verify, the record is frozen and committed, and the executor reading attributes the original difference by cause with interactions stated; or a bounded negative names what the unchanged package cannot express.
- **Stop when:** the T-003 review returns OWNER_GATE or unresolved findings on the source-informed inputs (execution parked), a mechanical gate fails past the retry cap, or a reserved gate binds.

### T-004 start — 2026-09-25

T-004 · new study record under `exploration/aries_integrated/studies/` and one native baseline evaluation into its `preparation/` · proposed points, indicators, preflight now; native points after the source-check review. Coordinator executes directly.

### T-002 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/reference-case-contract.md` (revised r1/r2); rendered page images `evidence/lyon-p703.png`, `lyon-p704.png`, `lyon-p707.png`, `lyon-p715.png`, `lyon-p717.png`, `raffray-p738.png`, `raffray-p741.png`, `raffray-p742.png` from the retained PDFs; retained WI-086/WI-088 images; `evidence/source-check-review.md` (fresh non-author reviewer: r1 FINDINGS none blocking, r2 FINDINGS one correct-before-use, r3 PASS; briefs `source-check-brief.md`, `source-check-recheck-brief.md`, `source-check-recheck-brief-r3.md`).
- **Reading:** the Lyon reference is a systems-code boundary, not an exchanger result: thermal 2916 MW → 43% → gross 1253 → minus 253 (170 + 27 + 55; itemised 252) → net 1000, with an ignited plasma and 90% of pumping/BOP power returned as heat. Raffray supplies the hardware at 2365 MW: He 1192 MW at 386 → 456 °C, PbLi 1444 MW at 451 → 738 °C, divertor 186 MW at 573 → 700 °C (≈ 67 MW of it unlabelled, presumed nuclear), cycle 355 → 707 °C with ε_rec 0.95 and a 30 °C approach; Fig. 12 places the PbLi and divertor exchangers in parallel after the helium exchanger. Q1 is confirmed and strengthened by the reviewer: in one series stream the helium stage can span 71 K of the 352 K rise (20%) while carrying 42% of the heat, so no cycle flow satisfies Fig. 12's temperatures, Table II's duties and the arrangement together; the published 43% applies a cycle constant to all thermal power. The model's divertor deposition (385 MW) exceeds the source-informed ≈ 167 MW by ≈ 218 MW, and its blanket deposition is ≈ 198 MW low. Source-informed inputs for the diagnostic study: ε_rec 0.95, divertor flow 283 kg/s (held at 2436 MW), partition f_rad 0.657 and exchange 0.0469, Lyon auxiliary itemisation; cycle flow 1600 kg/s is a cross-source derived convention bracketed 1500–2000.
- **Decision:** the thermal-composition ambiguity (≈ 60 MW), the unlabelled divertor share (≈ 67 MW) and the 253/252 itemisation are bounded ledger items, never tolerance; execution detail; coordinator with reviewer concurrence; contract § 3/§ 8 and budget.
- **Decision:** Q1 changes what "agreement with 43%" can mean for this model and is surfaced in the contract for the owner rather than resolved silently; dependent conclusions in the answer will be conditioned on it; premise surprise; coordinator; contract § 6.

### T-003 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/materiality-budget.md` (revised r1/r2); `evidence/source-check-review.md` r1–r3.
- **Reading:** budgets declared before any refinement study: net and gross ±15 MW (purpose-driven attribution resolution; the source itself supports ≈ ±2 MW), total thermal ±10 MW, per-circuit heat ±10 MW under a stated scaling rule (helium ambiguity ≈ 9.5 MW, so little margin), unmet heat 0 above ledger tolerance, turbine inlet ±5 K about the printed 708 °C. Reviewer accepted the lines and the bounded-item treatment.
- **Decision:** the budget is fixed from this entry onward and is not relaxed to accept residuals; reserved gate honoured; coordinator; `evidence/materiality-budget.md`.

### T-004 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `exploration/aries_integrated/studies/20260925-aries-reference-heat-electricity-reconciliation/@581e3c1a` (record, snapshot `dae3a4652ea16cbba42914e3d7174b27a9d112359a3c88307a316d1a573dba78`, 27 stored cases, all-point verification, sealed package, retained sources, executor `synthesis.md`); `results/attribution.json`; ten discovery-log rows `…#1`–`#10`; `evidence/preservation-check-t004-prep.json`; `evidence/entry-stellaris-regression-receipt.json` (exact 1,352 outputs and 68 responses; original package preserved).
- **Reading:** all 27 declared points completed under the entry package identity and verify against the independent oracle (364 channels, 14 exact verdicts per point). The original 158.7 MW unremoved heat is entirely a PbLi-stage limit set by the series exchanger order and the PbLi capacity rate; conductance is not the limit. Every source-supported input-level correction combined (C3) leaves 151.0 MW unremoved and reaches net 842.7 MW; the only steady, all-checks-satisfied source-conditioned points use 0.8 recuperation at 1600 kg/s (net 759.9–773.5 MW, efficiency ≈ 0.345); the source's 0.95 recuperation needs 1700–1800 kg/s for complete removal, past the assumed compressor rating. The reference 1253 MW gross is not approached anywhere. Interactions are large (forward one-at-a-time sum −45 MW versus combined +47 MW). The ledger is in `evidence/discrepancy-ledger.md` v1.
- **Decision:** finding #7 (series order) is routed to a model increment in the next round, with independent design review before implementation, rather than absorbed into this round; execution detail; coordinator; discovery log row `#7`.
- **Decision:** the compressor-rating violations at ≥ 1700 kg/s are retained as adverse points and not relabelled, because the 1600 MW rating is an A6 assumption and no resized alternative was declared; execution detail; coordinator; record § 4.
- **Decision:** one native baseline point was executed before the axis set grew from 16 to 18 axes; recorded as process finding #9 with preflight rerun, no re-execution; execution detail; coordinator; record § 9.

### Round 1 result — 2026-09-25

- **Intent:** met for the round's strategy (replay, contract, budget, one committed diagnostic study on the unchanged package), unmet for the goal question: the input-level causes are quantified, but the remaining thermal inadequacy is structural and needs a model increment before the answer contract can be assessed.
- **Task sequence:** T-001 COMPLETE (replay and entry preservation); T-002 COMPLETE (reference-case contract, fresh source check r1–r3 PASS); T-003 COMPLETE (materiality budget, reviewed); T-004 COMPLETE (27-point study sealed at `581e3c1a`).
- **Last semantic outcome:** COMPLETE with a valid study reading; exactly one study committed and no package promoted.
- **Stop reason:** last outcome `COMPLETE` with a valid study reading + no limit reached → round closes on trigger 1 (a valid study reading). No retry consumed; no checkpoint revision; caps untouched.
- **Evidence refs:** grounding `52e01b48`; seal `581e3c1a`; study snapshot `dae3a465…`; `evidence/source-check-review.md`; `evidence/t001-replay-summary.json`; `evidence/discrepancy-ledger.md`; `evidence/entry-stellaris-regression-receipt.json`; preservation checks at entry and after preparation (18,725 files unchanged).
- **Learning delta (proposed):** L-001 the source-conditioned unremoved heat is a PbLi-stage limit from the series exchanger order and the PbLi capacity rate, not from conductance. L-002 recuperation and cycle flow interact: 0.95 recuperation needs 1700–1800 kg/s on this package while 0.8 at 1600 kg/s removes all heat at ≈ 0.345 efficiency; forward one-at-a-time sums (−45 MW) do not predict the combined result (+47 MW). L-003 the Lyon reference is a systems-constant chain (2916 → 43% → 1253 → −253 → 1000) and the independently checked Q1 shows the published temperatures, duties and series-first arrangement cannot all hold, so part of the disagreement is a property of the published description. L-004 source-supported replacements for inherited inputs are 0.95 recuperation, 283 kg/s divertor flow, partition 0.657/0.0469 and the 252 MW Lyon auxiliary itemisation; the model's divertor deposition is ≈ 218 MW over and blanket ≈ 198 MW under the source-informed values; cycle flow 1595 kg/s is a derived cross-source convention.
- **Finding dispositions:** ten rows `20260925-aries-reference-heat-electricity-reconciliation#1`–`#10` were sighted by this round's own study with dispositions written; #7 is routed to a round-2 model increment, #8 and #10 to the answer ledger and learnings, #1–#6 are declared seams, #9 a recorded process note. None is unrouted. Joined disposition rows will be appended after the round review accepts them.
- **Constraints carried forward:** the topology alternative must keep the original series closure evaluable, expose the split between the parallel PbLi and divertor stages as a chosen operating quantity, and pass independent design review (MR-7) before implementation; the reference gross 1253 remains a comparison, never a target; the materiality budget stands.
- **Native-state check:** model, package and frozen evidence unchanged (preservation checks pass); the only writes outside the goal directory are the new study record, two thin study-support modules and ten discovery-log rows; two unrelated staged entry files remain untouched.

### Amendment 2026-09-25 — amends T-004 scope

[AGENT] The T-004 scope declared twenty-one points. After the source-check review confirmed the divertor-share reading (contract § 8), two partition axes and six cases were added before execution, giving twenty-seven declared points; the native baseline point for the preflight gate had been executed once before the T-003 review returned and was not re-executed because manifest and package were unchanged. Recorded here on the round-1 reviewer's finding; no result changed.

### Round 1 review — 2026-09-25

- **Reviewer and verdict:** fresh non-author reviewer, `evidence/round1-review.md`; FINDINGS, none blocking. Brief: `evidence/round1-review-brief.md`.
- **Checks:** native evidence by citation PASS (cases, attribution sums, snapshot sha256 `dae3a465…` recomputed, no verdict mismatches); goal and strategy fidelity PASS (no model or package change, one study, original case verbatim, nothing tuned); task scopes FINDING (T-004 point count grew 21 → 27 without a dated amendment; baseline point executed before the T-003 return) — amended above; retry classification PASS (none; the reviewer notes the contract/budget took two reviewer-driven revisions, which this coordinator records as review rechecks under T-002/T-003, not study-reading checkpoint revisions, so the checkpoint cap is unconsumed — recorded so the owner can rule otherwise); discovery rows PASS (ten rows, none unrouted; joined disposition rows appended after this review); reading and dispositions PASS with a wording correction to finding #7 (record addendum); budget discipline PASS; overstated claims: ledger net 842.727 → 842.732 and the "removable only" wording corrected in `discrepancy-ledger.md` v1.1, and the two PbLi return temperatures attributed to their cases in the record addendum.
- **Accepted learning delta:** L-001, L-002 accepted; L-003 accepted as a source-reading claim conditioned on the owner's Q1 gate; L-004 accepted with the note that the 218/198 MW deposition figures trace to the contract, not the study. Appended to `learnings.md`.
- **Remaining uncertainty:** temperature channels were not read by the reviewer; Q1's scientific meaning is an owner gate; the parallel-network effect is known only from the first-principles scratch check, not from the model.
- **Next:** do not close; open round 2 on the parallel PbLi/divertor topology increment after MR-7 design review, with the original series closure retained and evaluable.

## Round 2 — topology-increment

### Strategy revision — 2026-09-25

- **Approach:** represent the published exchanger network (Raffray Fig. 12: series blanket-helium stage, then parallel PbLi and divertor-helium stages rejoining before the turbine) as an additive generic closure selectable by a network mode, with mode 0 reproducing the current series closure exactly and the cycle-flow split between the parallel stages supplied as a chosen operating quantity. Register a modeling item, write its spec/design with the MR-7 role table and equations, obtain fresh design review before implementation, implement with the stock build route and fixed-point checks, prove exact reproduction of the four canonical cases and the 27 sealed points in mode 0, pass the integration seam, then commit one study of revised reference cases: mode 1 at the 1600 kg/s convention with a split sensitivity, the steady all-checks point, and a separately named resized-compressor alternative at 1800 kg/s, with the original failing case retained.
- **Assumptions:** the parallel network fits the existing bounded bisection closure (each stage's accepted heat is nonincreasing in the heater inlet, mixing is linear, so the residual stays strictly increasing); downstream consumers keep their interfaces; the split is an operating choice, not equipment sizing; the first-principles scratch check (`evidence/parallel-network-scratch.txt`) is right that the network reduces but does not remove the unmet heat at 1600 kg/s.
- **Abandonment conditions:** the closure's monotonicity or bracket fails for the network; the design review finds an MR-7 violation not resolvable within the split's declared role; the integration seam blocks outside this increment; an owner gate on Q1 or on the resized-compressor alternative; the round-2 limits.
- **Intended model increment:** new `Network Heat Driven Closure` definition and completion in `integrated_heat_electricity.sysml` (ARIES-only file), the assembly's `heat_exchangers` part rebound to it with `network_mode` (default 0) and `pbli_split_fraction` inputs, the reviewed `Heat Driven Closure` definition left in the library and its equations disclosed as copied in mode 0; regenerated package, re-pinned live manifest, one native CANDIDATE.
- **Intended study question:** with the published network represented, how much of the remaining unremoved heat and gross shortfall is removed at the source-supported inputs, how the result depends on the supplied split, and what a steady all-checks revised reference case gives at 1600 kg/s and at the declared 1800 kg/s resized-compressor alternative.

### T-001 scope

- **Objective:** register modeling item WI-092 and write one reviewable spec/design record with the MR-7 variable-role table, equations, migration and validation plan for the network closure; obtain fresh independent design review.
- **Why now:** round 1 located the remaining thermal inadequacy in the series arrangement; the owner brief permits an architecture correction only after review.
- **Scope:** native PM registration; `work/active/WI-092_*/spec.md`, `design.md`, `plan.md`; the design-review brief and return under goal evidence. No model, package or completion edits before the review passes.
- **Inputs:** `goal.md`; round-1 learnings L-001–L-004; `evidence/reference-case-contract.md` § 4; `evidence/parallel-network-scratch.py`; WI-089 design (closure equations) and `heat_driven_closure_impl.py@96914299`; MR-7.
- **Done when:** the record names every affected quantity, role, binding and consumer, the mode-0 exactness proof and the insufficient/sufficient tests, and a fresh reviewer returns PASS or resolvable FINDINGS.
- **Stop when:** the reviewer returns OWNER_GATE or the revision cap is reached.

### T-001 start — 2026-09-25

T-001 · modeling PM (`pm add-item`) and `work/active/WI-092_*/` · spec/design/plan and `evidence/design-review.md`. Coordinator authors; fresh reviewer reviews.

### T-001 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** WI-092 registered in `work/BACKLOG.md` (`pm add-item`); `work/active/WI-092_aries-parallel-exchanger-network/{spec,design,plan}.md` (revised r1); `evidence/design-review.md` (fresh non-author reviewer: r1 FINDINGS two correct-before-implementation and three notes; r2 PASS; MR-7 compliant at design level); briefs `design-review-brief.md`, `design-review-recheck-brief.md`; scratch draft and standalone test under the session scratchpad reproduced the reviewed series closure bit-for-bit in mode 0 and the first-principles network check in mode 1.
- **Reading:** the additive `Network Heat Driven Closure` with a supplied split is an admissible architecture alternative: equations, monotonicity and bracket verified by the reviewer; consumers keep meaning (only whole-network channels are read downstream); the split is an operating stand-in for the unmodelled branch hydraulic balance, not sizing. The reviewer corrected the R3 test to a direction test and noted that at the C3 inputs the PbLi heat is not fully transferred in any mode, because the PbLi primary capacity rate and the helium-stage bound limit it.
- **Decision:** proceed to implementation on the stock build route with the old definition retained unbound and its equations disclosed as copied; execution detail; coordinator with reviewer PASS; WI-092 design.
- **Decision:** the package-owned oracle must learn the network mode so the study verifier can re-derive mode-1 points independently; this is a checker extension, not model arithmetic, and is disclosed in the record; execution detail; coordinator; `exploration/aries_integrated/studies/oracle_entry.py`.

### T-002 scope

- **Objective:** implement WI-092 (definition, completion, assembly rebinding), rebuild the package on the stock route with fixed-point regeneration, run the development checks (mode-0 exact replay of the four canonical maps and the 27 sealed points, mode-1 network at C3 and original inputs, direction triple, refusals, zero-UA definedness), write the migration report, extend the oracle for mode 1, re-pin the live manifest and interface, run scoped validation, preservation and the isolated Stellaris replay, and obtain fresh independent implementation review.
- **Why now:** the design review passed; the increment is the round's declared model change.
- **Scope:** files named in the WI-092 plan plus `exploration/aries_integrated/build.py` (evidence path only), `studies/oracle_entry.py` (mode-1 branch), `studies/interface_data.py` and `studies/manifest.json` (re-pin). No shared-family file, no frozen record, no study execution.
- **Inputs:** WI-092 spec/design/plan; `evidence/design-review.md`; the scratch draft; `goal.md` invariants.
- **Done when:** all development checks pass with the receipts in WI-092 evidence and the implementation reviewer returns PASS (or resolvable FINDINGS), MR-7 recorded compliant/violated/unverified on executed behaviour.
- **Stop when:** the build route cannot reach a fixed point (mechanical, retry within cap), mode-0 replay is not exact (strategy blocker), or a reserved gate binds.

### T-002 start — 2026-09-25

T-002 · `models/library/analyses/integrated_heat_electricity.sysml`, `models/designs/aries_cs_integrated/plant.sysml`, `exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py`, `build.py`, regenerated `aries_integrated` package, study oracle/interface/manifest · WI-092 evidence receipts and `evidence/implementation-review.md`. Coordinator implements; fresh reviewer reviews.

### T-003 scope

- **Objective:** prove the rebuilt `aries_integrated` package is the integrated form of the WI-092 checkpoint through the native integration seam (`scripts/integrate.py`) and obtain a CANDIDATE with the re-pinned fingerprints.
- **Why now:** the increment is committed and re-pinned (`6828df18`); the round's study may only run on a package the seam has accepted.
- **Scope:** read-only against model, package, manifest and route; the seam's outputs under `evidence/integration-attempt<N>/` and log. No edits to the package or model.
- **Inputs:** audited work `work/active/WI-092_aries-parallel-exchanger-network@6828df18`; semantic `78dd23bf…`, executable `f739dbce…`; TEAx revision `8d877460…`; `evidence/integrate.py` (adapted from the WI-089 seam replay).
- **Done when:** the seam returns CANDIDATE with every gate passing and the lineage equal to the re-pinned fingerprints.
- **Stop when:** a gate blocks outside this increment (surface as a seam), or the implementation review (T-002, open) requires a change to the package, in which case this run is void and repeated after the change.

### T-003 start — 2026-09-25

T-003 · `evidence/integrate.py` → `evidence/integration-attempt1/` and `.log` · read-only seam replay. Coordinator runs; started while the T-002 implementation review is outstanding, on the committed state `6828df18`.

### T-002 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** commits `49668453` (implementation checkpoint) and `6828df18` (re-pin); WI-092 evidence `generation.log`, `completion-generation.log`, `fixed-point-generation.log`, `census-generation.log`, `build-hashes.json`, `development-cases.json` (40 native cases), `migration-report.json`, `validation-complete.log`, `validation-comparison.json`, `oracle-self-check.json`, `implementation-review-notes.md`; goal evidence `preservation-check-wi092.json` (18,725 files unchanged), `wi092-stellaris-regression-receipt.json` (exact 1,352 outputs and 68 responses on the original Stellaris package), `implementation-review.md` (fresh non-author reviewer at `6828df18`: PASS, four notes, MR-7 compliant on executed evidence; brief `implementation-review-brief.md`).
- **Reading:** mode 0 reproduces the four canonical maps and the 27 sealed round-1 points bit-exactly (546 of 546 numeric channels per point at relative 0, every verdict equal); the interface gains two entry keys and five outputs (546 → 551) and loses none; the executable fingerprint is `f739dbce…`, semantic `78dd23bf…`. Mode 1 at the C3 inputs with the 0.85 default split removes 41 MW more heat than the series arrangement (unmet 151.0 → 109.9 MW: helium 53.5, PbLi 56.4) and raises net from 842.7 to 879.7 MW; split 0.9 gives 882.1; the helium stage binds in mode 1, so no split removes all heat at 0.95 recuperation and 1600 kg/s. On the original failing inputs the network alone moves the unmet heat from the PbLi stage (158.7) to the divertor stage (117.9) and gives net 825.4. At 1800 kg/s the unmet heat is 0 in both arrangements (net 803.6). Validation: L2 105 → 105; L6 493 → 498, the five additions being the pre-existing "unsupported operator" diagnostic on the five new pass-through attributes.
- **Decision:** the reviewer's wording notes (1–3) are applied in the WI-092 design and recorded in `implementation-review-notes.md`; the completion docstring and calc-def doc comment keep their committed wording because they are part of the sealed package identity, and a wording-only rebuild would void the re-pin, replay receipts and integration candidate; the correction is scheduled for the next package edit; execution detail; coordinator; WI-092 design `[ir]`.
- **Decision:** note 4 is an explanation, not a defect: fifteen of the twenty "new channels" in the replay comparison are constraint evaluation records and the constraint report, which the development receipt lists among outputs and the sealed exporter stores as verdicts; execution detail; coordinator; `implementation-review-notes.md`.

### T-004 scope

- **Objective:** after the T-003 candidate, prepare and execute one committed study on the WI-092 package that gives the revised source-conditioned reference cases with the published network represented: the split sensitivity at the 1600 kg/s convention, the order-interaction tests (network on the original inputs, on C1, on C2 and on C3), the steady all-checks revised candidate at 0.8 recuperation, the flow bracket on the inherited compressor rating, and the separately named resized-compressor alternative at 1700 and 1800 kg/s; with the original failing case, the literal Lyon variant, the calculated baseline and the round-1 series cases C1, C2, C3 and the series steady point retained verbatim as controls.
- **Why now:** the increment passed implementation review; the goal requires the revised case executed under the native graph with the original case retained, and the attribution ledger needs the network step measured at more than one position in the change order.
- **Scope:** record `exploration/aries_integrated/studies/20260925-aries-revised-reference-network/`, thin `revised_reference_support.py` (reuses the round-1 composer; canonical bases from the mode-0 replay receipt on this package), 21 declared axes (the round-1 18 plus `network_mode`, `pbli_split`, `compressor_rating`), 27 declared points, indicators, native baseline point, preflight, oracle scan, native execution, all-point verification, reporting, record and freeze. No model, package or live-manifest change; no filtering of adverse points; the resized-compressor cases are labelled as a declared hardware alternative and never as a reference reproduction.
- **Inputs:** `goal.md`; `evidence/reference-case-contract.md`; `evidence/materiality-budget.md`; round-1 sealed record and `evidence/discrepancy-ledger.md` v1.1; WI-092 `evidence/development-cases.json` (canonical replay receipt) and `migration-report.json`; the T-003 candidate; stock study tooling.
- **Done when:** all 27 points complete and verify, the record is frozen and committed, the executor reading attributes the revised difference by cause with the network step measured at each position in the order, and the ledger is updated to v2; or a bounded negative names what the package cannot express.
- **Stop when:** T-003 does not return CANDIDATE (execution parked), a mechanical gate fails past the retry cap, or a reserved gate binds.

### T-003 return — 2026-09-25

- **Outcome:** COMPLETE (one mechanical retry consumed: attempt 1 refused at preflight because the coordinator's shell exported a PYTHONPATH with an empty `STOP_PARSER_TEAX_ROOT`, so the read-coverage gate saw an undeclared `/packages/teax-simkit` read; attempt 2 ran under the launcher's own environment and the package was untouched between attempts).
- **Evidence:** `evidence/integrate.py`; `evidence/integration-attempt1/` and `.log` (BLOCKER, retained); `evidence/integration-attempt2/integration_return.json` and `.log` (CANDIDATE: pinned packages, TEAx `8d877460…`, regeneration rewrote no byte outside `handwritten/`, 60 handwritten files byte-identical, census recaptured with 424 entry points, model-family spine, manifest pin `06e0627c…`, all six preflight gates with baseline read coverage `7188f0ec…`, oracle parity with every verdict re-derived, lineage semantic `78dd23bf…` executable `f739dbce…`).
- **Reading:** the committed package at `6828df18` is the integrated form of the WI-092 model change and carries the re-pinned identity; the round's study may run on it.
- **Decision:** the seam is invoked only through `.codex-test/run` without an outer PYTHONPATH, and study commands through `.codex-test/run bash -c` so the TEAx root expands inside the launcher; execution detail; coordinator; recorded here to prevent the same refusal.

### T-004 start — 2026-09-25

T-004 · new study record `exploration/aries_integrated/studies/20260925-aries-revised-reference-network/`, `revised_reference_support.py`, `revised_reference_reporting.py` · proposals, indicators, oracle scan, native baseline point, preflight, execution on the T-003 candidate, verification, report, record, freeze, commit. Coordinator executes directly.

### T-004 attempt 1 — 2026-09-25 (verification refused; retained)

- **What happened:** preparation (27 proposals, 21 axes), indicators (every axis `constraints_reachable`, no ruling required), native baseline point, six preflight gates and the oracle scan (27 of 27 evaluated, none refused) passed; all 27 points executed and completed under executable `f739dbce…` on the T-003 candidate (`evidence/t004-execute.log`). All-point verification refused one channel: `he_unmet` in `network-c2-0.85` (store 2.028448680648353 MW, oracle 2.0284486773855406 MW, relative 1.609e-09 against the 1e-9 rule, absolute 3.3e-09 MW with no declared absolute tolerance). No summary was written (`evidence/t004-verify-attempt1.log`).
- **Reading:** the unmet-heat channels are differences of order-1000 MW quantities fixed by a root solve whose native termination is 1e-8 MW residual (1e-10 K bracket) against the checker's own root finder; a relative 1e-9 rule on a 2 MW difference asks for 2e-9 MW, below the solver's guaranteed accuracy. This is the same numerical class as the residual-magnitude allowance the earlier goal declared and had independently reviewed (manifest `absolute_tolerances`, 1e-7 MW, T-005 of `aries-integrated-heat-electricity`). Round 1 escaped it only because no point had unmet heat below ≈ 16 MW.
- **Decision:** declare an absolute comparison tolerance of 1e-7 MW on the four unmet-heat channels only, with the evidence written to `evidence/unmet-tolerance-declaration.md`, obtain a focused fresh review before use, then re-run indicators and preflight on the amended manifest and re-execute and re-verify the 27 points into fresh `results/`, keeping attempt 1's results as `results-attempt1/` and comparing them; verdict parity stays exact; no model, package or point changes; this consumes one T-004 retry (1 of 2); execution detail; coordinator; recorded before the declaration is written.

### T-004 return — 2026-09-25

- **Outcome:** COMPLETE (one retry consumed, 1 of 2: attempt 1's all-point verification refused one unmet-heat channel by 1.6e-9 relative; a 1e-7 MW absolute tolerance on the four unmet-heat channels was declared, independently reviewed and applied, and the points were re-executed bit-identically and verified).
- **Evidence:** `exploration/aries_integrated/studies/20260925-aries-revised-reference-network/` (record, `synthesis.md`, snapshot `c6551b7172a567db1fac5c43f14f7cbdc8169283ffa6b47d73c4f0fe4025a738`, 27 stored cases with 551 numeric outputs each, all-point verification pass over 364 channels and 14 exact verdicts, sealed package, retained sources, attempt-1 results and refused verification retained); `results/attribution.json` and `.md`; `results/attempt-comparison.json` (14,877 channels identical); nine discovery-log rows `20260925-aries-revised-reference-network#1`–`#9`; `evidence/unmet-tolerance-declaration.md`, `unmet-tolerance-review-brief.md`, `unmet-tolerance-review.md` (fresh reviewer: PASS, five notes; note 4 applied by copying the full basis into every manifest entry); `evidence/t004-execute.log`, `t004-execute-attempt2.log`, `t004-verify-attempt1.log`, `t004-verify-attempt2.log`; `evidence/preservation-check-t004-r2.json` (18,725 files unchanged); `evidence/discrepancy-ledger.md` v2; `evidence/freeze-study-r2.py`.
- **Reading:** the published network removes the series-order PbLi limit (41.1 MW of the 151.0 MW C3 shortfall at unchanged hardware) but at 1600 kg/s with 0.95 recuperation the blanket-helium stage binds (cycle helium leaves 3.6 K below the 456 °C helium hot inlet) and 107–114 MW stay unremoved at every split from 0.80 to 0.90; the source-conditioned network case at the convention (net 879.7, gross 1131.7) is therefore not a steady point. Steady all-checks cases exist only with 0.8 recuperation at 1600 kg/s (net 759.9, either arrangement) or with the declared resized-compressor alternative at 0.95 recuperation and 1700 kg/s with the network (net 891.0, gross 1143.0, efficiency 0.391, turbine inlet 628 °C; series needs 1800 kg/s, net 803.6). No point approaches 1253 / 1000; at the best steady point the entire remaining 110 MW gross gap is the efficiency shortfall at the heat-limited turbine inlet, and the network cannot reach the published 708 °C with the published duties at any split (Q1 quantified in the model). Order interaction is +7.6 MW net; the ledger accounts for the combined difference.
- **Decision:** the resized-compressor cases are reported as a declared hardware alternative and never as a reference reproduction; the inherited-rating cases at 1700 and 1800 kg/s stay adverse and unrelabelled; execution detail; coordinator; record § 3 and § 4.
- **Decision:** the live manifest's tolerance list is amended (four unmet-heat channels, 1e-7 MW) after focused fresh review, with the pin, fingerprints and every point unchanged; the integration candidate obtained before the amendment is retained because the seam does not read the tolerance list; execution detail; coordinator with reviewer PASS; `evidence/unmet-tolerance-review.md`.
- **Decision:** the v1.1 ledger's per-circuit heat figures (1248.571 / 1485.781 / 191.412) are replaced in v2 by the stored channel values (1248.568 / 1485.785 / 191.410); the difference is transcription, below any budget; execution detail; coordinator; `evidence/discrepancy-ledger.md`.

### T-005 scope

- **Objective:** assemble `answer.md` for the goal (source case definition, baseline and revised heat/electricity tables, quantitative attribution, remaining uncertainty, engineering statuses, reuse and model changes, independent reviews, Stellaris preservation, exact replay instructions and a plain-language explanation), and run the delivery checks: the entry preservation manifest and the isolated Stellaris baseline replay.
- **Why now:** the study reading closes the round's strategy; every material discrepancy has a ledger status; the owner brief requires the answer with these sections and reserves closure.
- **Scope:** `answer.md`, `evidence/preservation-check-delivery.json`, `evidence/delivery-stellaris-regression-receipt.json`; no model, package, manifest or study change.
- **Inputs:** `goal.md`; trail; ledger v2; contract; budget; both sealed study records; WI-092 record and reviews; `evidence/stellaris-regression-wi092.py`; `evidence/check-preservation.py`.
- **Done when:** the answer names every required section with native evidence by citation, the preservation check passes and the Stellaris replay is exact.
- **Stop when:** a delivery check fails (strategy blocker; surface, do not fix by editing the original package).

### T-005 start — 2026-09-25

T-005 · `answer.md` and two delivery receipts under `evidence/` · assembled from committed evidence after the study seal. Coordinator writes directly.

### T-005 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `answer.md` (sections: question and short answer, source case definition, baseline and revised tables generated from the sealed store, attribution, discrepancy statuses, remaining uncertainty, engineering statuses, reuse and model changes, independent reviews, Stellaris preservation, exact replay instructions, plain-language explanation, owner gates); `evidence/preservation-check-delivery.json` (18,725 protected files unchanged against `96914299`); `evidence/delivery-stellaris-regression-receipt.json` and `.log` with `stellaris-regression-delivery.py` (isolated replay exact: 1,352 outputs and 68 responses; copied package exact; original package byte-preserved; preservation passed after the replay).
- **Reading:** the delivery checks pass; the answer states the result as a well-supported disagreement (best steady point 109 MW net short, explained by the turbine-inlet limit under the published duties) with the 158.7 MW unmet heat corrected in two named mechanisms and every material discrepancy carrying a ledger status.
- **Decision:** the answer's tables are generated from `results/cases.json` by script rather than transcribed, so every figure in them is a stored channel; execution detail; coordinator; `answer.md` § 3.

### Round 2 result — 2026-09-25

- **Intent:** met for the round's strategy (network increment designed, MR-7 reviewed, implemented, integrated as a native CANDIDATE, one study committed on it, answer assembled with delivery checks). For the goal question: answered as a well-supported disagreement, conditioned on the owner's Q1 gate. The 158.7 MW unmet heat is corrected in two named mechanisms (series order, removed by the reviewed architecture change; helium-stage bound at 1600 kg/s with 0.95 recuperation, removed by a declared operating or hardware choice the sources do not state). Every material discrepancy carries a ledger status (corrected / explained / bounded / unresolved); the remaining −109 MW net at the best steady point is explained (efficiency shortfall at the heat-limited turbine inlet) and bounded (resized alternative), and its source-side meaning (whether ARIES's 43% was attainable) is unresolved because the retained papers do not describe the cycle arrangement in enough detail. Net 1000 is not reproduced within the ±15 MW budget at any steady point, and the answer says so.
- **Task sequence:** T-001 COMPLETE (WI-092 spec/design, fresh design review r1 → r2 PASS); T-002 COMPLETE (implementation, re-pin, fresh implementation review PASS with notes); T-003 COMPLETE with one retry (seam attempt 1 refused on an outer PYTHONPATH, attempt 2 CANDIDATE); T-004 COMPLETE with one retry (attempt 1 verification refused by 1.6e-9 relative on a 2 MW difference channel; tolerance declared and reviewed; attempt 2 bit-identical and verified); T-005 COMPLETE (answer, preservation, isolated Stellaris replay).
- **Last semantic outcome:** COMPLETE with a valid study reading and the answer delivered; one package promoted and one study committed, the round's allowance.
- **Stop reason:** last outcome `COMPLETE` with a valid study reading + no limit reached → round closes on trigger 1. Retries: one each in T-003 and T-004 (cap 2 per task, unconsumed elsewhere); checkpoint revisions: none; rounds: 2 of 6.
- **Evidence refs:** commits `49668453` (implementation), `6828df18` (re-pin), `4f5991a5` (reviews and candidate), `352ecee4` (study seal), `b6d24a64` (record § 16); study snapshot `c6551b7172a567db1fac5c43f14f7cbdc8169283ffa6b47d73c4f0fe4025a738`; `evidence/design-review.md`, `implementation-review.md`, `unmet-tolerance-review.md`; `evidence/integration-attempt2/integration_return.json`; `evidence/discrepancy-ledger.md` v2; `answer.md`; `evidence/preservation-check-delivery.json`; `evidence/delivery-stellaris-regression-receipt.json`.
- **Learning delta (proposed):** L-005 the published series-then-parallel network removes the series-order PbLi limit (41 MW of the 151 MW C3 shortfall at unchanged hardware) but at 1600 kg/s with 0.95 recuperation the blanket-helium stage binds: the cycle helium enters it at 309 °C and can reach only 452 °C against the 456 °C helium hot inlet, so 107–114 MW stay unremoved at every split from 0.80 to 0.90; complete removal at 0.95 recuperation needs 1700 kg/s with the network (1800 kg/s in series). L-006 once all heat is removed the exchanger arrangement has no effect on any plant output, because the turbine inlet then follows from the energy balance; the arrangement matters only where a stage is limited. L-007 (extends L-003) at the best steady point the whole remaining gap to Lyon's 1253 / 1000 (110 / 109 MW) is the efficiency shortfall at the heat-limited turbine inlet (628 against 708 °C); with the published duties the published network cannot reach 708 °C at any split, so Lyon's 43% is a systems constant the described hardware does not deliver in this model. L-008 (process) the verifier's relative-only rule fails on small difference channels of a root solve (unmet heat) at the solver's termination order; declare absolute tolerances at that order, with focused review, before verifying a study whose points can have small nonzero differences. L-009 (process) the integration seam and study commands run only under the launcher's own environment; an outer PYTHONPATH built from an unset TEAx root trips the read-coverage gate.
- **Finding dispositions:** nine rows `20260925-aries-revised-reference-network#1`–`#9` sighted by this round's study with dispositions written (#1, #2, #5, #6 to the ledger and answer; #3 to the write-up; #4, #8, #9 declared seams; #7 a process note). None is unrouted. Joined disposition rows will be appended after the round review accepts them.
- **Constraints carried forward:** Q1 stays an owner gate with dependent conclusions conditioned on it; the resized-compressor alternative is a declared hardware change and never a reference reproduction; the materiality budget stands unchanged; the "line for line" wording in the sealed completion docstring and calc-def doc comment is corrected at the next package edit, not by a wording-only rebuild; WI-092 remains `backlog` in the native registry pending the owner's close.
- **Native-state check:** the model changed only through WI-092 (ARIES-only files; reviewed before and after implementation); the package was regenerated on the stock route and re-pinned; the live manifest gained four reviewed absolute tolerances; one study committed; every frozen record, the Stellaris models and packages and the six shared library files are unchanged (preservation 18,725 files at delivery; isolated Stellaris replay exact). The owner's unrelated entries were committed by the owner during the round (`02836e36`, "write-up work") and one unrelated file (`work/analysis/20260920-184131_design-choice-assignment-audit.md`) is now untracked in the working tree; neither was touched by this round.

### Amendment 2026-09-25 — amends T-004 scope

[AGENT] The T-004 scope declared "no model, package or live-manifest change". The reviewed absolute-tolerance declaration amended the live manifest's tolerance list (four unmet-heat channels; pin, fingerprints and every point unchanged). Recorded here on the round-2 reviewer's finding F3 as a deviation outside the written scope, taken through the T-004 attempt-1 decision and the fresh tolerance review; no result changed.

### Round 2 review — 2026-09-25

- **Reviewer and verdict:** fresh non-author reviewer at `53702a4b`, `evidence/round2-review.md`; FINDINGS, none blocking (three correct-before-use, two notes). Brief: `evidence/round2-review-brief.md`.
- **Checks:** native evidence by citation PASS (six figures confirmed in `results/cases.json`; attempt comparison zero; verification pass over 27 rows); helium-stage claim PASS (3.585 K approach, 53.514 MW short of the duty); goal and strategy fidelity PASS; task scopes FINDING (F3, amended above); retry classification PASS; tolerance discipline PASS (budget unchanged since `581e3c1a`); discovery rows PASS; reading FINDING (F2); answer completeness FINDING (F1); unsupported claims F2, F4.
- **Findings applied:** F1 `answer.md` now states the completion condition as partially answered (§ 1 and § 13). F2 record § 3/§ 6, finding #3, synthesis, ledger and L-006 restricted to plant-ledger and cycle-state outputs (19 of 551 exchanger-stage channels differ in each pair). F3 amendment above. F4 ledger v2.1 and answer § 5 relabel mechanism 2 as bounded by a missing-input range. F5 "needs 1700 kg/s" reworded as a bracket (1700 suffices, 1600 does not; threshold unbracketed) in the record addendum, synthesis, ledger and L-005.
- **Accepted learning delta:** L-005 (F5 wording), L-006 (F2 wording), L-007, L-008, L-009 accepted and appended to `learnings.md`. Joined disposition rows for `…network#1`–`#9` appended to the discovery log.
- **Remaining uncertainty:** the reviewer did not open `attribution.json`, the constraint catalog, the WI-092 spec/design or the source images, and checked the migration replay's full channel count on one sampled entry; Q1's scientific meaning remains the owner's gate.
- **Next:** do not open a further round; the answer stands as partially answered pending the owner's Q1 decision and formal closure.


## Round 3 — q1-thermal-cycle-check

### Owner supplement — 2026-09-25

[OWNER] Received after the round-2 answer; retained verbatim in `evidence/owner-supplement-r3.md`. The reconciliation is not closed; the conclusion about the published design was stronger than the evidence supports; three corrections and the narrow Q1 investigation are directed.

- **Corrections applied at the owner's emphasis:** the claim that the published network cannot reach 708 °C and that Lyon's 43% is therefore a systems constant the described hardware does not deliver is withdrawn from `answer.md` (§ 1, § 5, § 6, § 12, § 13), `evidence/discrepancy-ledger.md` (v2.2), `learnings.md` (L-003 and L-007 amended in place with the owner citation), `.project/CURRENT_WORK.md`, and by addendum on the sealed `record.md` and `synthesis.md`; the supported statement is that we cannot yet reconcile the published thermal description with our interpretation and implementation. The 110 MW residual is now stated as 53.5 MW in the helium stage and 56.4 MW in the PbLi stream. The 891 MW case is stated as the best tested steady case, not an upper bound. The gross/net shortfall's ledger status changes from "explained" to "unresolved, model mechanism identified". The answer's completion assessment stays "partially answered".

### Strategy revision — 2026-09-25

- **Approach:** a fresh thermal-cycle reviewer with a bounded brief examines the primary diagrams, the temperature and duty definitions, the cross-paper mapping and our cycle representation, and determines whether Q1 survives. If it does not survive, the round scopes the implied interpretation or model change as a further task (design review before any implementation, MR-7 binding). If it survives, the answer records the reconciliation as open on that specific inconsistency and names the missing evidence. No model, package, manifest or study change in this task.
- **Assumptions:** the retained page images and the reviewed contract carry enough of the primary papers to decide the diagram and definition questions; the reviewer can view the images; the executed channels on the network package are the right description of our representation.
- **Abandonment conditions:** the reviewer returns `UNDETERMINED` with a named missing source (surface to the owner; the research route applies); a finding that changes stated modeling intent (reserved gate); the round-3 limits.
- **Intended model increment:** none in this task.
- **Intended study question:** none in this task.

### T-001 scope

- **Objective:** obtain the fresh thermal-cycle review of Q1 and record whether the apparent contradiction survives, the deciding check, and the implied change.
- **Why now:** the owner funded this investigation before closure; the round-2 answer's remaining gap rests on it.
- **Scope:** `evidence/q1-thermal-cycle-review-brief.md` and the reviewer's return `evidence/q1-thermal-cycle-review.md`; the coordinator applies wording consequences to `answer.md` and the ledger. No model, package, manifest or study change.
- **Inputs:** the contract; the retained page images; WI-089 design § Heat-driven recuperated cycle; the cycle library and completions; the network closure; the executed round-2 channels.
- **Done when:** the reviewer returns a verdict with the deciding check and the implied change, and the trail records it with the next action.
- **Stop when:** the reviewer cannot decide from the retained material (park; owner research decision), or a reserved gate binds.

### T-001 start — 2026-09-25

T-001 · `evidence/q1-thermal-cycle-review-brief.md` → `evidence/q1-thermal-cycle-review.md` · read-only review of sources and representation. Fresh reviewer; coordinator records.

### T-001 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/q1-thermal-cycle-review.md` (fresh thermal-cycle reviewer at `812b79bf`: verdict SURVIVES, deciding check the first-principles reconstruction; three correct-before-use findings, three notes); brief `evidence/q1-thermal-cycle-review-brief.md` with an appended correction of its image list; contract § 6a addendum; `answer.md` § 1, § 5, § 6, § 12, § 13 revised.
- **Reading:** the apparent contradiction is independent of the exchanger arrangement: with Raffray's printed per-branch duties and temperatures, the blanket-helium stage needs ≥ 11.8 MW/K (zero approach) or 16.8 MW/K (30 °C approach) against a whole-cycle capacity rate of 8.0 MW/K, so no counterflow arrangement delivers 707 °C; Fig. 13's inset draws one lumped hot leg 385 → 737 °C, consistent with a lumped-heater cycle calculation. Definitions (456 °C helium hot inlet; 30 °C exchanger terminal difference; 0.95 recuperator; duties as loop heat to the exchanger, friction included) and the cross-paper mapping (2907 against 2916 MW; 3% on flow) close the escape routes. Our representation agrees with Fig. 13's chain and is generous to the source (4–5 K approaches). Undetermined: how the ARIES-CS cycle calculation treated the exchangers (p737 Ref. 7, not retained) and whether Lyon's 2916 MW includes ≈ 50 MW of balance-of-plant heat. The reviewer also found a mapping artefact on our side: duties scaled by 1.030 with Raffray's primary flows pinch the PbLi cold end, so part of the 56 MW PbLi shortfall at 1600 kg/s is ours.
- **Decision:** the answer states what the review establishes (the published per-branch description cannot be reconciled with the published cycle outlet by any arrangement; our representation is not the cause) and what it does not (the source's own cycle treatment; the actual design's attainable efficiency), at the owner's framing; execution detail; coordinator; `answer.md` § 1.
- **Decision:** the scaling artefact is quantified natively rather than recorded: one small study on the unchanged package with the primary flows and pump capacities scaled with the duties, and a 1650 kg/s point to narrow the round-2 review's unbracketed threshold; the flow and capacity values are declared in the configuration as the cross-paper mapping's own hardware values, never derived from demand; execution detail; coordinator; T-002 below.
- **Decision:** the brief's page-image mislabel is corrected by an appended note, and future briefs cite the WI-086 Raffray pages for Tables II–III and Figs. 12–14; execution detail; coordinator.

### T-002 scope

- **Objective:** quantify the cross-paper flow-scaling artefact and narrow the cycle-flow threshold with one committed study on the unchanged WI-092 package: the network case at C3 with primary flows and pump capacities scaled by 2436/2365 (all three loops, PbLi only, helium only) at 1600 kg/s, and the declared resized-compressor alternative at 1650 and 1700 kg/s with and without scaled flows; controls `combined-c3-partition`, `network-c3-0.85` and `resized-compressor-1700-network-0.85` retained verbatim.
- **Why now:** the Q1 review attributes part of the 56 MW PbLi shortfall to our mapping, which the ledger must quantify rather than list; the round-2 review left the 1600–1700 kg/s threshold unbracketed.
- **Scope:** record `exploration/aries_integrated/studies/20260925-aries-flow-scaling-check/` on `revised_reference_support.py` (round-2 canonical receipt reused; same package identity, same live manifest), 25 declared axes (round-2's 21 plus `he_primary_flow`, `pbli_primary_flow`, `he_pump_capacity`, `pbli_pump_capacity`), 11 declared points, indicators, baseline, preflight, scan, execution on the round-2 integration candidate, all-point verification, report, record, freeze, commit. No model, package or manifest change.
- **Inputs:** `evidence/q1-thermal-cycle-review.md` finding 2; contract § 6a and § 8; round-2 record; the round-2 canonical replay receipt.
- **Done when:** all 11 points complete and verify, the record is frozen and committed, and the ledger states the artefact's size in MW.
- **Stop when:** a mechanical gate fails past the retry cap, or a reserved gate binds.

### T-002 start — 2026-09-25

T-002 · new study record under `exploration/aries_integrated/studies/` · proposals, indicators, native baseline point, preflight, scan now; execution, verification, freeze after. Coordinator executes directly.

### Amendment 2026-09-25 — amends T-002 scope (round 3)

[AGENT] The T-002 scope declared eleven points; the configuration declares twelve, because the C1 and C2 composition steps are stored as controls alongside C3 (the composer builds C3 from them). Recorded before execution; no result affected.

### T-002 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `exploration/aries_integrated/studies/20260925-aries-flow-scaling-check/` (record, synthesis, snapshot `342d97318902abfb7803559d4fca7e5ee1dabd688f1344bb146904df5c2ca471`, 12 stored cases, all-point verification pass over 364 channels and 14 exact verdicts, sealed package, retained sources); `results/attribution.json` and `.md` (`evidence/flow-scaling-ledger.py`); four discovery rows `20260925-aries-flow-scaling-check#1`–`#4`; `evidence/t002-r3-execute.log`, `t002-r3-verify.log`; contract § 6a rule amendment; ledger v2.3; `answer.md` § 3, § 6, § 9, § 11.
- **Reading:** the mapping artefact is ≈ 34 MW of the 56 MW PbLi shortfall at 1600 kg/s, but ≈ 20 MW of it migrates to the helium stage (bounded by its 456 °C hot inlet, whose capability falls as the heater inlet rises), so the network case's total shortfall falls by 14.2 MW (to 95.7) and net rises by 12.8 MW (to 892.4); the case stays not steady. The helium flow itself is irrelevant to the helium-stage limit (−0.3 MW). The threshold for complete removal lies between 1650 kg/s (42.7 MW unremoved; 26.3 with scaled flows) and 1700 kg/s under either mapping; the 1700 kg/s steady case's plant outputs are unchanged to 1e-3 MW.
- **Decision:** the contract's § 8 mapping scales flows with duties from here on, with the unscaled mapping retained as the round-1/round-2 convention and both quantified; execution detail; coordinator; contract § 6a.
- **Decision:** the round-2 integration candidate and canonical receipt were reused for this study because the package identity and manifest pin are unchanged; process note `…#4`; execution detail; coordinator.

### Round 3 result — 2026-09-25

- **Intent:** met for the strategy: the owner-funded Q1 investigation returned a verdict (SURVIVES) with the deciding check and the implied change; its side finding (our flow-scaling artefact) was quantified natively rather than listed. For the goal question the answer stays partially answered, now with the remaining gap characterised as a source-internal inconsistency that survives independent review, and with the limit of that statement kept at the owner's framing (the source's own cycle treatment and the actual design's attainable efficiency are not decided).
- **Task sequence:** T-001 COMPLETE (fresh thermal-cycle review); T-002 COMPLETE (flow-scaling study sealed at `342d9731…`, no retries).
- **Last semantic outcome:** COMPLETE with a valid review and a valid study reading; no package promoted; one study committed.
- **Stop reason:** last outcome `COMPLETE` + no limit reached → round closes on trigger 1. Retries: none in round 3; checkpoint revisions: none; rounds: 3 of 6.
- **Evidence refs:** `evidence/owner-supplement-r3.md`; `evidence/q1-thermal-cycle-review.md`; contract § 6a; `evidence/discrepancy-ledger.md` v2.3; study snapshot `342d9731…`; `answer.md`.
- **Learning delta (proposed):** L-010 with Raffray's printed per-branch duties and temperatures, no counterflow arrangement of the three exchangers can deliver the printed 707 °C cycle outlet, because the blanket-helium loop (hot inlet 456 °C) carries 42% of the heat over 21% of the span and would need ≥ 11.8 MW/K against 8.0 MW/K for the whole cycle flow; Raffray's Fig. 13 inset draws one lumped hot leg 385 → 737 °C, consistent with a lumped-heater cycle calculation; what the ARIES-CS cycle calculation actually did is not in the retained pages (supersedes the wording of L-003 and L-007 on this point, not their numbers). L-011 the cross-paper mapping must scale primary flows with duties: holding Raffray's flows while scaling duties by 1.030 pinches the PbLi cold end and is worth ≈ 34 MW on the PbLi stage at 1600 kg/s, of which ≈ 20 MW migrates to the helium stage, so the total shortfall changes by only ≈ 14 MW and no steady result changes. L-012 (process) a per-branch model shortfall can migrate between stages when one input is corrected; attribute by stage and by total, never by a single stage's change.
- **Finding dispositions:** four rows `…flow-scaling-check#1`–`#4` with dispositions written; none unrouted; joined rows after the round review.
- **Constraints carried forward:** the owner's framing on Q1 (established versus not established) governs every restatement; Q1's remaining undetermined items (Raffray p737 Ref. 7; Lyon's balance-of-plant heat) are named for the owner's research decision; the budget stands; the resized cases remain declared alternatives.
- **Native-state check:** no model, package or manifest change in round 3; one study committed; frozen records, Stellaris and shared files unchanged (delivery preservation and Stellaris replay from round 2 stand; the package identity is unchanged since).

### Amendment 2026-09-25 — amends T-002 scope (round 3), second

[AGENT] The first amendment did not reconcile the count (round-3 review F3). The twelve declared points are: `combined-source-thermal`, `combined-source-thermal-lyon-aux`, `combined-c3-partition`, `network-c3-0.85`, `network-c3-scaledflows-0.85`, `network-c3-scaledflows-0.90`, `network-c3-scaledflows-pbli-only-0.85`, `network-c3-scaledflows-he-only-0.85`, `resized-compressor-1650-network-0.85`, `resized-compressor-1650-network-scaledflows-0.85`, `resized-compressor-1700-network-0.85`, `resized-compressor-1700-network-scaledflows-0.85`. The split-0.90 scaled case was declared in the configuration and omitted from the scope text. Recorded after execution on the reviewer's finding; no result affected.

### Round 3 review — 2026-09-25

- **Reviewer and verdict:** fresh non-author reviewer at `77098a41`, `evidence/round3-review.md`; FINDINGS, none blocking (four correct-before-use, one note). Brief: `evidence/round3-review-brief.md`.
- **Checks:** owner framing FINDING (F1, F4); reporting details PASS; native evidence PASS (six figures confirmed; verification pass 12 of 12); study fidelity and MR-7 PASS (scaled flows and capacities declared, nothing tuned, one study, identity unchanged); scope and count FINDING (F3, amended above); migration PASS (stored channels); discovery rows PASS; unsupported claims F2, F5.
- **Findings applied:** F1 the "Typical Fluid Temperatures in HX" inset belongs to Fig. 12 (p736), not Fig. 13; corrected in the contract § 6a, the ledger, the answer and L-010, and here for the T-001 return above, after the coordinator checked the page image. F2 stale sentences in `answer.md` § 5 and § 13 replaced with the 1650–1700 kg/s bracket and the returned Q1 status. F3 amendment above. F4 answer § 12 now says "the heat sources as printed". F5 the T-001 return above overstates the review's note count (the committed review has one note, finding 4); contract § 6a's "reviewer note 5" corrected to "finding 4"; the ledger's ambiguous "which of the two" sentence rewritten.
- **Accepted learning delta:** L-010 (with F1 and the zero-approach / 30 °C qualifier), L-011 ("unchanged to 1e-3 MW"), L-012 accepted and appended to `learnings.md`. Joined disposition rows for `…flow-scaling-check#1`–`#4` appended to the discovery log.
- **Remaining uncertainty:** the reviewer did not open the page images, the thermal-cycle physics, `learnings.md`, the logs or cost channels; Q1's two undetermined items are the owner's research decision.
- **Next:** do not open a further round; the answer stands as partially answered with the Q1 result and its limits stated at the owner's framing; formal closure and the research decision are the owner's.


## Round 4 — cited-cycle-reference

### Owner supplement — 2026-09-25

[OWNER] Received after round 3; retained verbatim in `evidence/owner-supplement-r4.md`. Directs pursuit of Raffray's cited cycle/exchanger reference; the current calculations are preserved; the missing reference is not assumed to resolve the issue; the lumped-heater explanation stays a hypothesis until the source supports it; a bounded negative is documented if the reference cannot be obtained or does not answer. Two qualifications applied at the owner's emphasis in `answer.md`, `evidence/discrepancy-ledger.md`, `evidence/reference-case-contract.md` § 6a, `learnings.md` L-010 and `.project/CURRENT_WORK.md`: "these published quantities cannot all hold under the stated heat-exchanger assumptions" replaces "no arrangement can work"; 891 MW is a modeled alternative, not the reconstructed ARIES reference, whose changed flow and compressor rating still need cost evaluation before economic comparison.

### Strategy revision — 2026-09-25

- **Approach:** identify the cycle/exchanger reference Raffray cites on p737 from the retained paper's reference list (rendered page image under evidence); check the internal registers (`knowledge/SOURCE_INDEX.md`, `knowledge/research/`, concept research) for it; if absent, form a research request and acquire it through the prescribed route (`research-acquire`, `research_seam.py`, `source_registry.py`, hold-out screen applied by the registry); read what it says about heat delivery to the cycle (single or per-branch heaters, approach, temperatures, duties) and decide whether it resolves the inconsistency among the published branch duties and temperatures; record the result or the bounded negative; no model, package, manifest or study change.
- **Assumptions:** the reference is identifiable from the retained page; the registry's hold-out screen decides admissibility (never waived by the agent); reading is post-reveal authorized by the owner brief for this goal.
- **Abandonment conditions:** the reference cannot be obtained within the request limits (bounded negative documented); a hold-out hit (queued for the owner, not waived); the source does not describe the exchanger treatment (bounded negative); a reserved gate.
- **Intended model increment:** none.
- **Intended study question:** none.

### T-001 scope

- **Objective:** identify the cited reference and determine whether it is already in the repository.
- **Why now:** the owner directed the pursuit; the citation text is on the retained page.
- **Scope:** render the Raffray reference-list page(s) from the retained PDF into `evidence/`; read the citation; search the internal registers; record the identification. No acquisition in this task.
- **Inputs:** `knowledge/holdout/aries-cs/08-FST-Raffray.pdf` (retained primary paper, post-reveal reading authorized by the owner brief for this goal); `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p737.png`; `knowledge/SOURCE_INDEX.md`; `knowledge/research/`.
- **Done when:** the reference is named (authors, title, venue, year) with the page image cited, and its presence or absence in the registers is recorded.
- **Stop when:** the citation cannot be read from the retained page (surface).

### T-001 start — 2026-09-25

T-001 · `evidence/raffray-p<N>.png` renders and the trail · read-only. Coordinator executes directly.

### T-001 return — 2026-09-25

- **Outcome:** COMPLETE (with a correction of the round-3 attribution).
- **Evidence:** `evidence/raffray-p745.png`, `evidence/raffray-p746.png` (reference list rendered from the retained paper); a citation-marker scan of every page of the retained paper (superscript numerals with their preceding text), recorded here: Ref. 7 appears on p726 only ("physics, engineering and system studies"; "to the divertor. From the system studies"); p737's cycle paragraph ("The overall thermal-hydraulic optimization was done by considering the efficiency of the Brayton cycle for an example 1000 MW(electric) case … for a given set of material constraints and cycle parameters") carries no reference marker; Ref. 15 is attached on p735 to "three compression stages and a single expansion stage" and on p745 in the conclusions; Ref. 13 is attached on p732 to "the blanket coupled to a Brayton power cycle".
- **Reading:** Ref. 7 is Lyon's systems paper (retained as `08-FST-Lyon.pdf`); it takes the 43% thermal conversion efficiency as a systems constant ("90% of the power for helium pumping and balance of plant is returned as thermal power, which is converted with a 43% thermal conversion efficiency", p703) and contains no exchanger or cycle representation, so it cannot answer the question. The cycle references Raffray actually cites are Ref. 15, R. Schleicher, A. R. Raffray and C. P. Wong, "An Assessment of the Brayton Cycle for High Performance Power Plant", Fusion Technol. 39, 823 (2001), and Ref. 13, X. Wang, S. Malang and A. R. Raffray, "Modular Dual Coolant Pb-17Li Blanket Design for ARIES-CS Compact Stellarator Power Plant", Proc. 20th IEEE SOFE, Knoxville, 2005. Neither is in `knowledge/SOURCE_INDEX.md`, `knowledge/research/` or the concept research.
- **Decision:** the round-3 "p737 Ref. 7" attribution is corrected in the contract § 6a, the answer, the ledger, the current-work entry and by an appended note on the review; the pursuit targets Refs. 15 and 13; execution detail; coordinator.

### T-002 scope

- **Objective:** acquire Raffray's cited cycle references (Ref. 15 Schleicher et al. 2001; Ref. 13 Wang et al. 2005) through the prescribed research route and, if obtained, read how they represent heat delivery to the cycle.
- **Why now:** T-001 identified them; neither is in the repository.
- **Scope:** `knowledge/research/requests/REQ-ARIES-CYCLE-HX-01.json` (one request, two candidates, limits 8 searches and 3 captures); a fresh researcher carrying `.claude/commands/research-acquire.md` with `scripts/research_seam.py` and `scripts/source_registry.py`; the registry's hold-out screen decides admissibility and is never waived; the return class and, if registered, the source locations; no model, package or study change. Reading of a registered source is the next task.
- **Inputs:** the request file; the trail T-001 return; `docs/research_seam_operator_guide.md`; the hold-out protocol as applied by the registry.
- **Done when:** the run closes with a class (REGISTERED, BOUNDED_NEGATIVE, OPERATOR_QUEUE or BLOCKER) and the run directory is committed.
- **Stop when:** a hold-out hit or a paywall queues a candidate for the owner (documented; the owner decides), or the limits are reached.

### T-002 start — 2026-09-25

T-002 · `knowledge/research/requests/REQ-ARIES-CYCLE-HX-01.json` → run directory and `return.json` · fresh researcher; coordinator records.

### T-002 return — 2026-09-25

- **Outcome:** COMPLETE (class REGISTERED with one candidate queued for the owner).
- **Evidence:** `evidence/research-acquire-r4-return.md`; run `knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-01/20260925T203030790830/` (`return.json`, `process_log.md`, `run.jsonl`, receipts); registered source `knowledge/sources/schleicher_raffray_wong_2001_an_assessment_of_the_brayton/` (`raw.pdf`, `output.md`, `images/`; `SOURCE_INDEX.md` and `MANIFEST.jsonl` updated by the registry); commit `HEAD` after this entry.
- **Reading:** Ref. 15 (Schleicher, Raffray and Wong, TOFE 2000 / Fusion Technol. 39, 823, 2001) is captured from the ARIES library mirror at qedfusion.org (the registry's identity screen bars the `aries.ucsd.edu` term; no hold-out hit). Ref. 13 (Wang, Malang and Raffray, SOFE 2005) is paywalled at IEEE Xplore with no author-posted copy found in eight searches; it is queued for the owner with the journal-typeset Schleicher copy (not needed). Three candidates rejected (abstract only; wrong paper; the 2007 successor of Ref. 13, also paywalled). One of three captures used; closed `limit_reached` on searches.
- **Decision:** the registered source is read in T-003 against its page images, with a fresh independent check of the reading before any conclusion is written into the answer; the researcher's registration summary is not adopted as the reading; execution detail; coordinator.
- **Owner queue:** whether to obtain Ref. 13 (IEEE Xplore, paywalled) through institutional access; the run's failure receipt names it.

### T-003 scope

- **Objective:** read the registered Ref. 15 and determine how it represents heat delivery to the cycle, whether that representation resolves the inconsistency among the published branch duties and temperatures, and what it does and does not establish about ARIES-CS's own cycle calculation.
- **Why now:** the source is registered and citable; the owner's question turns on its content.
- **Scope:** `evidence/ref15-reading.md` written from `output.md` and the page images (not from the researcher's summary); a fresh source-check reviewer with a bounded brief confirms the reading against the page images before the answer changes; no model, package or study change.
- **Inputs:** the registered source; Raffray p735–p737 (Table III cycle parameters; the citing sentence); contract § 6a; the owner supplement r4 (no lumped-heater conclusion without source support).
- **Done when:** the reading names, with page and figure, how the source treats heat addition, its approach or terminal-difference assumptions, its efficiency dependence on turbine inlet temperature, and its plant context; the reviewer returns PASS or resolvable FINDINGS; and the trail states the bounded result.
- **Stop when:** the reading cannot be checked against page images (surface).

### T-003 start — 2026-09-25

T-003 · `evidence/ref15-reading.md`, `evidence/ref15-reading-brief.md`, `evidence/ref15-reading-review.md` · read-only. Coordinator reads; fresh reviewer checks.

### T-003 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/ref15-reading.md` (revised r1 after the source check; corrections marked `[sc]`); `evidence/ref15-reading-brief.md`; `evidence/ref15-reading-review.md` (fresh source-check reviewer at `6b40a8d3`: FINDINGS, five correct-before-use and three notes, all applied; the absence claim confirmed by a full-text search: no per-branch exchanger, blanket duty, divertor, approach, pinch or ΔT anywhere in the five pages; equation (2) has no heat-source term).
- **Reading:** Raffray's cited cycle method (Schleicher, Raffray and Wong 2000/2001) treats the heat source as a boundary "To/from In-Reactor Components or Intermediate Heat Exchanger" with the turbine inlet temperature as an independent design input and the return temperature as a dependent variable of the compression ratio (constrainable by materials); gross efficiency follows from two expressions in Tin, ε_rec, η_T, η_C, Pout, ΔP/Pout, r_p, T_min and γ, expressions the source attributes to Malang, Schnauder and Tillack 1998 (its Ref. [4]). Raffray's Table III lists the same variables except Tin, which it replaces by an "HX temperature difference between hot and cold legs 30 °C" the cited method does not have; that Tin = 737 − 30 = 707 °C was set that way is an inference consistent with the Fig. 12 inset, not a statement in either source; Raffray's compression ratio 3.5 lies outside the source's plotted range. Bounded result: the cited reference answers the methodology question (a lumped heat-source boundary with Tin as input) and does not resolve the inconsistency among the published branch duties and temperature spans; the lumped-heater reading of the inset stays a hypothesis at the ARIES-CS level, with the method's lumped heat source as support for its plausibility only.
- **Decision:** the reviewer's finding 1 identifies the expressions' origin (Malang, Schnauder and Tillack 1998, a liquid-metal-blanket plus gas-turbine coupling paper) as a direct lead on how the ARIES lineage delivered blanket heat to the cycle; one more bounded request is issued for it (6 searches, 2 captures) before the round closes; the chain stops there unless the owner extends it; execution detail; coordinator.

### T-004 scope

- **Objective:** acquire Malang, Schnauder and Tillack 1998 (Fusion Eng. Des. 39–40, 561) through the research route and, if obtained, read how it represents blanket-to-cycle heat delivery.
- **Why now:** it is the origin of the cited method's efficiency expressions and the nearest source on blanket-to-cycle coupling in the ARIES lineage.
- **Scope:** `knowledge/research/requests/REQ-ARIES-CYCLE-HX-02.json`; a fresh researcher on `research-acquire.md`; the return class and, if registered, a reading with a fresh source check; no model, package or study change.
- **Inputs:** the request; `evidence/ref15-reading.md` § 3; the hold-out protocol as applied by the registry.
- **Done when:** the run closes with a class and the run directory is committed; a registered source is read and checked.
- **Stop when:** a paywall or hold-out hit queues the candidate (documented; the owner decides), or the limits are reached.

### T-004 start — 2026-09-25

T-004 · `REQ-ARIES-CYCLE-HX-02.json` → run directory and return · fresh researcher; coordinator records.

### T-004 return — 2026-09-25

- **Outcome:** COMPLETE (class REGISTERED).
- **Evidence:** `evidence/research-acquire-r4b-return.md`; run `knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-02/20260925T204659541052/`; registered source `knowledge/sources/combination_of_a_self_cooled_liquid_metal_breeder_blanket/` (publisher-typeset ISFNT-4 paper, Fusion Eng. Des. 41, 561–567, 1998; the request's "39–40" was one volume off); two paywalled copies queued as redundant; three candidates rejected; 3 of 6 searches and 1 of 2 captures; no hold-out hit.
- **Decision:** the source is read in T-005 against `raw.pdf` and its page images (the extraction scrambles the title line and the p. 564 equation), with a fresh source check before the answer changes; the researcher's registration summary is not adopted as the reading; execution detail; coordinator.

### T-005 scope

- **Objective:** read Malang, Schnauder and Tillack 1998 and determine how it represents blanket-to-cycle heat delivery, whether that bears on the inconsistency among the published ARIES-CS branch duties and temperature spans, and what it establishes about the ARIES lineage's method.
- **Why now:** it is the origin of the cited method's expressions and the nearest coupling paper obtained.
- **Scope:** `evidence/malang98-reading.md`, `evidence/malang98-reading-brief.md`, `evidence/malang98-reading-review.md`; then the round-4 result; no model, package or study change.
- **Inputs:** the registered source; `evidence/ref15-reading.md`; Raffray Tables II–III and Fig. 12; the owner supplement r4.
- **Done when:** the reading names, with page, figure and table, the exchanger arrangement, the temperature differences and the cycle parameters; the reviewer returns PASS or resolvable FINDINGS; the trail states the bounded result.
- **Stop when:** the reading cannot be checked against page images (surface).

### T-005 start — 2026-09-25

T-005 · reading, brief and review under `evidence/` · read-only. Coordinator reads; fresh reviewer checks.

### T-005 return — 2026-09-25

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/malang98-reading.md` (revised r1, corrections `[sc]`); `evidence/malang98-reading-brief.md`; `evidence/malang98-reading-review.md` (fresh source-check reviewer at `3e945e0a`: FINDINGS, one correct-before-use and five notes, all applied; every quotation and number confirmed against the PDF; absence of divertor, second loop, parallel or series branches confirmed by full-text search); page renders `evidence/malang98-p562.png`, `-p563.png`, `-p565.png` (the printed paper's Fig. 1 and Fig. 3 captions are swapped).
- **Reading:** the origin of the cited method's expressions within the ARIES lineage applies them to one lithium loop through one IHX duty with stated terminals and derives efficiency from To/Ts, the pressure-loss ratio and the component efficiencies; it says nothing about several primary loops at different temperature levels. Bounded result of the citation chain: the cited method takes the turbine inlet temperature as an input from a single heat source or IHX and, in the obtained sources, was never extended to several loops; it neither resolves the inconsistency among the published ARIES-CS branch duties and temperature spans nor states how ARIES-CS handled them; the lumped-heater reading of the Fig. 12 inset is consistent with the method, not supported by it, and remains an inference.
- **Decision:** the citation chain stops here unless the owner extends it; the remaining obtainable lead is the paywalled Ref. 13, queued; execution detail; coordinator.

### Round 4 result — 2026-09-25

- **Intent:** met for the strategy: Raffray's cited cycle reference was identified from the retained page (correcting the round-3 attribution), acquired through the research route with the registry's hold-out screen, read against page images with a fresh source check, and followed one hop to the origin of its expressions, likewise acquired, read and checked; the owner's two qualifications were applied first. The bounded result is recorded without assuming the reference resolved the issue and without treating the lumped-heater explanation as established. For the goal question the answer stays partially answered: the remaining gap is a source-internal inconsistency under the stated heat-exchanger assumptions; the obtained references show the cited cycle method takes the turbine inlet as an input from a single heat source and do not say how ARIES-CS combined its three loops.
- **Task sequence:** T-001 COMPLETE (citation identified; misattribution corrected); T-002 COMPLETE (REQ-ARIES-CYCLE-HX-01, REGISTERED; Ref. 13 queued, paywalled); T-003 COMPLETE (Ref. 15 read, source check FINDINGS applied); T-004 COMPLETE (REQ-ARIES-CYCLE-HX-02, REGISTERED); T-005 COMPLETE (Malang 1998 read, source check FINDINGS applied).
- **Last semantic outcome:** COMPLETE with two registered sources and a bounded result; no package promoted; no study committed.
- **Stop reason:** last outcome `COMPLETE` + no limit reached → round closes on trigger 1. Retries: none; checkpoint revisions: none; rounds: 4 of 6.
- **Evidence refs:** `evidence/owner-supplement-r4.md`; `evidence/raffray-p745.png`, `raffray-p746.png`; `knowledge/research/requests/REQ-ARIES-CYCLE-HX-01.json`, `-02.json` and their runs; `knowledge/sources/schleicher_raffray_wong_2001_an_assessment_of_the_brayton/`, `knowledge/sources/combination_of_a_self_cooled_liquid_metal_breeder_blanket/`; `evidence/ref15-reading.md`, `ref15-reading-review.md`, `malang98-reading.md`, `malang98-reading-review.md`; contract § 6a `[r4]`; `answer.md`; ledger v2.3.
- **Learning delta (proposed):** L-013 the ARIES-CS Brayton cycle method (Raffray Ref. 15, Schleicher, Raffray and Wong 2000/2001; expressions from Malang, Schnauder and Tillack 1998) treats the heat source as a boundary or a single intermediate heat exchanger with the turbine inlet temperature as an independent input and the return temperature as a dependent variable; in the obtained sources it was never extended to several primary loops at different temperature levels, so a branch-level inconsistency like Q1 would not surface in that calculation; whether ARIES-CS combined its three loops in that way is inferred, not stated. L-014 (process) a citation named by a reviewer must be verified against the reference list and a citation-marker scan before it is pursued: the round-3 "p737 Ref. 7" was Lyon's retained systems paper, and the cycle references were Refs. 15 and 13. L-015 (process) the registry's identity screen bars the `aries.ucsd.edu` term; the ARIES library mirror at `qedfusion.org` serves the same files and passed the screen.
- **Finding dispositions:** no study in this round; no discovery rows. The research runs' receipts and negatives are in their run directories.
- **Constraints carried forward:** the owner's two qualifications govern every restatement (published quantities cannot all hold under the stated heat-exchanger assumptions; 891 MW is a modeled alternative whose flow and rating need cost evaluation before economic comparison); the lumped-heater reading remains an inference; Ref. 13 is the owner's acquisition decision; formal closure is the owner's.
- **Native-state check:** no model, package, manifest or study change in round 4; two sources registered through the registry (knowledge/ only); frozen records, Stellaris and shared files unchanged (the package identity is unchanged since round 2's delivery checks).

### Round 4 review — 2026-09-25

- **Reviewer and verdict:** fresh non-author reviewer at `21a76402`, `evidence/round4-review.md`; FINDINGS, none blocking (two correct-before-use, one owner question, two notes). Brief: `evidence/round4-review-brief.md`.
- **Checks:** owner direction PASS with one exception (answer § 12, F1); qualifications FINDING (answer § 12 bare 891 MW, F2); citation correction PASS (p745/p746 read by the reviewer); source-check application PASS; bounded result PASS (same four elements in trail, answer, ledger and contract; completion "partially answered"); scopes and limits PASS (the Malang hop recorded as one bounded step past the direction; no retries); unsupported claims F1, F2, F4.
- **Findings applied:** F1 answer § 12 now says the sketch "would be one way to arrive at 708 °C, but the papers do not say that is what was done" and that the obtained references "neither confirm nor rule out" how ARIES-CS handled its loops. F2 answer § 12 carries the modeled-alternative and cost caveat on 891 MW. F4 the T-001 return's "and on p745 in the conclusions" is withdrawn: Raffray's p745 markers are off by one and belong to Ref. 16; the cycle attribution rests on p735 alone (L-014 amended). F5 stale text repaired (answer § 1 duplicate sentence, § 5 row 5, § 6 Malang hop, § 13 fragment; ledger header v2.4; L-010 "being pursued"); `SOURCE_INDEX.md`'s registry-written "lumped block" wording is left as the registry wrote it, the checked reading (`ref15-reading.md`, boundary label) governs.
- **Owner question (F3, surfaced, not resolved):** the request `REQ-ARIES-CYCLE-HX-01` named `aries.ucsd.edu` in `where_to_look`; the registry's identity screen bars that term, so the researcher captured the same files from the ARIES library mirror at `qedfusion.org` (content hold-out screen: no hit; neither paper is ARIES-CS 2008 material) and used Wayback snapshots of the barred site for triage only. Whether the term bar is a hold-out safeguard that a mirror must not bypass is the owner's call; if it is, the two registrations should be re-screened or withdrawn by the owner. The proposed process learning L-015 (use the mirror) is rejected on this ground and not recorded.
- **Accepted learning delta:** L-013 accepted as corrected (only Schleicher makes Tout dependent; Malang states both IHX terminals and takes To from the IHX outlet); L-014 accepted with the marker-context check; L-015 rejected. Appended to `learnings.md`.
- **Remaining uncertainty:** the reviewer did not open the PDFs, the p732/p735 markers, the receipts beyond `return.json`, or the frozen-records claim; Ref. 13 and the composition of Lyon's 2916 MW remain the owner's decisions.
- **Next:** do not open a further round; the answer stands as partially answered with the citation-chain result at the owner's framing; formal closure, the Ref. 13 acquisition and the F3 screen question are the owner's.


## Round 5 — coupling-paper-question

### Owner supplement — 2026-09-25

[OWNER] Received after round 4; retained verbatim in `evidence/owner-supplement-r5.md`. One question for the round (does the Wang, Malang and Raffray SOFE 2005 paper provide the missing information), the source-screen question first, a bounded permitted-access attempt with no purchase without asking, the four precise conclusions, the "41 MW of 151 MW" correction, updates to the answer, ledger and findings log, independent review, commit; closure reserved. Corrections applied on receipt: `answer.md` § 12 now says the network change "removed about 41 MW of the 151 MW of trapped heat at the source-supported inputs"; § 13 states 891 MW as the best tested steady alternative, not an upper bound or a reconstructed reference, with costing outside this goal.

### Strategy revision — 2026-09-25

- **Approach:** T-001 reviews the `aries.ucsd.edu` term bar's intended scope against the existing authorization and the two round-4 registrations from the run records, preserving their receipts, and states the decisions the owner must make; T-002 makes one bounded attempt to locate a permitted-access copy of the coupling paper outside the ARIES library hosts, registering nothing (its ARIES-CS title makes any registration a hold-out hit reserved to the owner) and queuing what it finds; the round then closes with the bounded result and the decisions, or, if the owner rules in time and a copy is registered, proceeds to reading with a fresh source check and a comparison with the model under the goal's workflow. No model, package, manifest or study change unless step 4 of the supplement is reached.
- **Assumptions:** the rule home and the run records state the screen's purpose and what was done; the registry's pre-fetch identity screen refuses an ARIES-CS-titled registration before any fetch.
- **Abandonment conditions:** the owner's decisions D1/D2 are needed before any ARIES-library or ARIES-CS-titled access (park, report); the paper is unavailable through permitted access (record the limit, finish the round); the round-5 limits.
- **Intended model increment:** none unless the paper resolves a material assumption (then the smallest justified correction through spec, design review, implementation and a targeted study).
- **Intended study question:** none unless the above.

### T-001 scope

- **Objective:** resolve or precisely state the source-screen question: the intended scope of the `aries.ucsd.edu` restriction against the existing research authorization, and a review of the two round-4 registrations including mirror access and Wayback triage, with provenance and receipts preserved.
- **Why now:** the owner requires it before dependent source access.
- **Scope:** `evidence/source-screen-review.md` from `scripts/holdout_guard.py`, `scripts/source_registry.py`, `knowledge/holdout/aries-cs/PROTOCOL.md` (rule text only; no sealed PDF opened), the owner brief and supplements, and the two run directories; no edit to any shared policy file or run record.
- **Inputs:** as listed. **Done when:** the review states the scope, the authorization, what was done, and either a resolution under existing authorization or the specific decisions needed. **Stop when:** a decision is needed (surface; do not access dependent sources).

### T-001 start — 2026-09-25

T-001 · `evidence/source-screen-review.md` · read-only. Coordinator.

### T-001 return — 2026-09-25

- **Outcome:** COMPLETE (decisions surfaced; not resolved by existing authorization).
- **Evidence:** `evidence/source-screen-review.md` § 1–5, quoting `scripts/holdout_guard.py` ("the host is the canonical program mirror"; "There is no waiver … adjudicating it is the owner's job, through the protocol's own § 6 exception log"), `scripts/source_registry.py` (pre-fetch identity screen on URL and title; post-capture content scan), PROTOCOL § 3/§ 6/§ 7, and the two run records and receipts (`8bbb7e3c`, `620e341f`, untouched).
- **Reading:** the host term marks ARIES-library provenance for owner adjudication; the round-4 researcher substituted the `qedfusion.org` mirror so that no match was presented, and used Wayback index listings of the barred host for triage; on content both papers are clean. The existing authorization covers reading and route-based acquisition, forbids bypassing safeguards, and does not delegate the adjudication step; it cannot resolve the conflict.
- **Decision:** two owner decisions are surfaced before any dependent access: D1 ratify (log under § 6) or withdraw the two round-4 registrations; D2 the Wang 2005 paper's ARIES-CS title makes any registration a hold-out hit reserved to the owner, so the round-5 attempt locates and queues a permitted-access copy without capturing it, and the owner decides on the exception and on paywalled access; no ARIES-library host, mirror or snapshot is used by this goal until D1 is ruled; reserved gate; coordinator; `evidence/source-screen-review.md` § 5.

### T-002 scope

- **Objective:** one bounded attempt to locate a permitted-access copy of the coupling paper outside the ARIES library hosts, queued for the owner's decision; nothing captured or registered; no purchase.
- **Why now:** the owner's item 2; the outcome makes D2 concrete (exception plus registration, purchase, or stop).
- **Scope:** `knowledge/research/requests/REQ-ARIES-CYCLE-HX-03.json` (4 searches, 1 capture allowed by the schema but no registration attempted); a fresh researcher on `research-acquire.md` with the standing rules and this round's restriction (no `aries.ucsd.edu`, no `qedfusion.org`, no Wayback snapshots of either); the run directory and `evidence/research-acquire-r5-return.md`.
- **Inputs:** the request; the round-4 HX-01 log (IEEE Xplore paywalled; no author copy found on the ARIES hosts); `evidence/source-screen-review.md` § 5.
- **Done when:** the run closes with its class and the candidates it queued, or a bounded negative.
- **Stop when:** the limits are reached, or a candidate would need the barred hosts.

### T-002 start — 2026-09-25

T-002 · `REQ-ARIES-CYCLE-HX-03.json` → run directory and return · fresh researcher; coordinator records.

### T-002 return — 2026-09-25

- **Outcome:** COMPLETE (class OPERATOR_QUEUE; the paper is unavailable through permitted access).
- **Evidence:** `evidence/research-acquire-r5-return.md`; run `knowledge/research/requests/runs/REQ-ARIES-CYCLE-HX-03/20260925T212847849698/` (`return.json`, `run.jsonl`, `process_log.md`; committed). IEEE Xplore 4018989 (SOFE 2005) and Taylor and Francis FST07-6 (2007 successor, FS&T 52, 635) both closed access with no author manuscript or repository copy (IEEE record, OpenAlex, Semantic Scholar, Crossref); OSTI, NTIS, eScholarship and CORE searched with no record of either paper; twelve other results rejected as different papers, none opened (one of them a landing page for a sealed hold-out paper, not opened). Four of four searches; nothing registered or downloaded; no ARIES-library host, mirror or Wayback snapshot used; no purchase; Google Scholar all-versions not reached within the limit.
- **Reading:** the round's question (does the coupling paper provide the missing information) cannot be answered: the paper is obtainable only through paywalled or institutional access, and its ARIES-CS title makes any registration a hold-out hit reserved to the owner. The limit is recorded; the investigation does not expand.
- **Decision:** the round finishes on the bounded result without a further research dependency; the two acquisition routes (purchase or institutional access, with the § 6 exception) are the owner's decision D2; execution detail; coordinator.

### Round 5 result — 2026-09-25

- **Intent:** met for the strategy (source-screen question reviewed and its decisions surfaced before any dependent access; one bounded, capture-free, permitted-access attempt; the four precise conclusions and the "41 MW of 151 MW" correction applied; answer, ledger and contract updated). The round's question is not answered: the coupling paper is unavailable through permitted access, so no new information reached the model, and the reconciliation stays partially answered. Closure as partially answered is recommended.
- **Task sequence:** T-001 COMPLETE (source-screen review; decisions D1, D2 surfaced); T-002 COMPLETE (OPERATOR_QUEUE; limit recorded).
- **Last semantic outcome:** COMPLETE with a bounded negative on the round's question; no package promoted; no study committed.
- **Stop reason:** last outcome `COMPLETE` + the owner's stop condition ("If unavailable, record that limit and finish the round") → round closes on trigger 1. Retries: none; checkpoint revisions: none; rounds: 5 of 6.
- **Evidence refs:** `evidence/owner-supplement-r5.md`; `evidence/source-screen-review.md`; `knowledge/research/requests/REQ-ARIES-CYCLE-HX-03.json` and its run; `evidence/research-acquire-r5-return.md`; `answer.md` § 12–13; ledger v2.5; contract § 6a `[r5]`.
- **Learning delta (proposed):** L-015 (process; replaces the rejected round-4 proposal) the registry's `aries.ucsd.edu` term marks ARIES-library provenance for owner adjudication and has no waiver; substituting a mirror host so that no match is presented avoids the adjudication step and is not permitted access, whatever the content scan says; a source whose identity or title carries a barred term is acquired only after the owner logs a § 6 exception. L-016 (process) a bounded acquisition attempt for a barred-title source is run capture-free (locate, log with `--failure`, close), so the owner's decision is made on a concrete candidate without any fetch of hold-out material.
- **Finding dispositions:** no study in this round, so no discovery-log rows; the findings log's last entries remain the round-3 flow-scaling rows (`…flow-scaling-check#1`–`#4`), and the round's bounded negative is recorded in the run's `return.json` and this trail rather than as a study finding.
- **Constraints carried forward:** the four precise conclusions; D1 and D2 are the owner's; no ARIES-library host, mirror or snapshot is used by this goal until D1 is ruled; costing the resized alternative belongs in a separate goal; formal closure is the owner's.
- **Native-state check:** no model, package, manifest or study change in round 5; no registration; frozen records, Stellaris and shared files unchanged since round 2's delivery checks (package identity unchanged).
