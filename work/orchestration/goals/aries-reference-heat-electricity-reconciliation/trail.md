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
