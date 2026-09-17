# Trail: Bounded feasibility and design-point transfer

## Round 1 — fixed-assumption-local-search

### Strategy revision — 2026-09-16

- **Approach:** Reuse frozen rejections to locate coupled constraint conflicts, then refine a small supported geometry/current/accommodation search with explicit integer cooling requirements and transfer checks.
- **Assumptions:** Entering package dependencies and independently reviewed original equations remain applicable only within their documented conditional scope.
- **Abandonment conditions:** Unsupported physical improvement, changed comparison meaning, unresolved owner gate or declared evaluation budget.
- **Intended model increment:** None initially; expose current model limits rather than invent dependencies.
- **Intended study question:** Is there a sampled combined pass under fixed default assumptions, and what do smaller/reference/larger cases establish about conditional transfer?

### T-001 scope

- **Objective:** Define the meaningful bounded search and current transfer inventory.
- **Why now:** Prior frozen cases isolate interacting field, fit, burn, divertor and cooling constraints without establishing global infeasibility.
- **Scope:** Read clean existing evidence, inspect current dependencies, write pre-execution protocol and transfer contract draft; no model changes or new scientific equations.
- **Inputs:** `goal.md` and its grounding evidence at entering HEAD.
- **Done when:** Variables/bounds/budget/responses/stopping rules and evidence reuse are explicit, with unsupported transfer claims identified.
- **Stop when:** Unsupported dependency or scientific premise conflict blocks justified framing.

### T-001 start — 2026-09-16

T-001 · current package and frozen study evidence · `evidence/search-protocol.md` and `transfer-contract.md`.

### Parallel scope — 2026-09-16

[AGENT] A bounded transfer-inventory worker may run alongside coordinator search framing: both read unchanged package evidence; neither changes equations or another's files. Worker owns only `transfer-contract.md` and `evidence/transfer-inventory.md`. Coordinator owns trail, goal, search protocol and execution. Results integrate sequentially before final conclusions.

### T-001 return — 2026-09-16

- **Outcome:** COMPLETE.
- **Evidence:** `evidence/search-protocol.md`, study `protocol.md`, `axes.json`, `indicators.json` and `reviews/preexecution-check.md` (unpinned; no native digest).
- **Reading:** Six supported design choices have represented constraint paths. Search can proceed under fixed performance, engineered geometry bounds and explicitly incomplete accommodation economics. Transfer inventory is independently scoped and continues alongside execution.
- **Decision:** Coupled previous rejections warrant bounded refinement; authorize the stated protocol without changing scientific assumptions; execution detail; coordinator; new study directory and protocol.

### T-002 scope

- **Objective:** Execute a bounded native search and explain joint constraint outcomes with transfer checks.
- **Why now:** T-001 established supported inputs and pre-execution limits.
- **Scope:** One unchanged package, one native study, at most 500 oracle coordinates and 80 native cases including baseline; all failures retained.
- **Inputs:** `goal.md`, `evidence/search-protocol.md`, current study protocol and captured preparation.
- **Done when:** Frozen native/oracle-verified results establish a sampled pass/neighborhood or informative bounded rejection and reference/smaller/larger responses.
- **Stop when:** Declared budget, mechanical failure past cap, unsupported premise or owner gate.

### T-002 start — 2026-09-16

T-002 · `exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer/` · committed native study and bounded synthesis.

### T-002 return — 2026-09-16

- **Outcome:** MECHANICAL_FAILURE.
- **Evidence:** Baseline invocation failed before evaluation with missing `simkit`; `/tmp/bounded-baseline.log` (unpinned; no native digest).
- **Reading:** Scientific inputs unchanged. The prior study's runtime-command.md supplies the required sealed TEAx import path.
- **Decision:** Retry the identical baseline with the documented runtime import path; execution detail; coordinator; invocation only.

### T-002 start — 2026-09-16

Retry 1 of 2; task, inputs, scope and meaning identical. Operational correction: use `PYTHONPATH=.:/home/reid/1cfe/teax/packages/teax-simkit STUDY_REQUIRE_TEAX=1 .codex-test/run python ...`, as in the preceding frozen study.

### T-002 return — 2026-09-16

- **Outcome:** BOUNDED_NEGATIVE.
- **Evidence:** `exploration/stellarator_e2e/studies/20260916-bounded-feasibility-transfer/record.md@a16e7256` and frozen native results; executor synthesis at the same directory (new synthesis currently unpinned; no native digest); `evidence/transfer-checks.json@a16e7256`.
- **Reading:** The declared search found no combined pass; informative simultaneous deficits and numerical transfer responses are established within held assumptions. Unsupported field evaluations, invalid heat accounts and absent equipment pricing stay separate. Current transfer receipt satisfies the requested small design-point checks; comparison preparation remains as named in readiness.md.
- **Decision:** Repeated local field/heat/wall tradeoffs and adequate finite coverage support the declared stopping rule at 201 calls rather than budget exhaustion; execution detail; coordinator; study/window-selection and answer.md. No global conclusion or changed criterion.
- **Decision:** Matched transverse inputs change only fit and matched loop inputs preserve magnet/divertor heat while altering pumping; retain missing physical/accounting dependencies in the transfer contract; execution detail; coordinator; evidence/transfer-checks.json and transfer-contract.md.

### Round 1 result — 2026-09-16

- **Intent:** Met on the owner's accepted bounded-negative path; transfer contract and necessary-only readiness assessment delivered.
- **Task sequence:** T-001 COMPLETE; T-002 MECHANICAL_FAILURE before evaluation, identical documented import-path retry, then BOUNDED_NEGATIVE.
- **Last semantic outcome:** BOUNDED_NEGATIVE with a valid native study reading.
- **Stop reason:** Valid study reading plus the protocol's adequate-local-rejection stopping rule → round closes. No feasible neighborhood is claimed; no future task list is opened.
- **Evidence refs:** Frozen study `a16e7256`, answer.md, transfer-contract.md, readiness.md and transfer-checks.json; final amendments and synthesis await custody commit.
- **Learning delta:** Proposed L-001: current/fit/loop closure leaves coupled field/heat/wall deficits in the finite default sample. Proposed L-002: numerical off-reference response and fixed-point comparability are distinct from feasible operation and qualified configuration/technology transfer. Proposed L-003: unchanged transverse cost and loop installed-price omissions prohibit economic ranking despite a hydraulic or fit response.
- **Finding dispositions:** Five current study IDs #1–#5 and 42 prior touched IDs are routed in evidence/finding-dispositions.md, new-findings.json and prior-findings-map.json. Final acceptance and joined preservation rows await independent coverage. No semantic follow-up executes from those dispositions.

### Round 1 review — 2026-09-16

- **Reviewer:** Fresh non-author `/root/reviewer`, continuing valid framing coverage; evidence/final-review.md and final-review-checks.json (unpinned; no native digest until final custody commit).
- **Verdict:** FINDINGS.
- **Checks:** Independent review passes 228 frozen hashes, 234 committed files, 72 evidence records, 71 store joins, 16,046 fresh scalar comparisons, 1,420 oracle predicates, 1,420 native-operand predicates, full 201-call replay and 354 coupled identities. Five new and 42 prior finding dispositions checked. L-001–L-003 are substantively accepted subject to scope correction. Native package/source evidence remains unchanged.
- **Finding:** Nine first-refinement oracle-only points have current below the declared 12 MA-turn lower bound. None was native-selected and none passes. The frozen protocol/window claims of universal bound compliance are false for those rows. This is a protocol deviation, not newly authorized coverage.
- **Next:** Closed round remains closed. Open a bounded correction round to retain and identify the exceptions, correct coverage counts and claims, and obtain the same reviewer's diff check. No model rerun or retroactive bound expansion.

## Round 2 — correct-search-coverage

### Strategy revision — 2026-09-16

- **Approach:** Correct the scope account using retained coordinates; preserve all frozen numerical evidence and separate nine out-of-protocol oracle diagnostics from the declared-window result.
- **Assumptions:** Independent all-point replay and custody coverage remain valid because no inputs, outputs, predicates or package equations change.
- **Abandonment conditions:** Correction changes a scientific outcome, evidence cannot support the classification, or an owner-held premise must change.
- **Intended model increment:** None.
- **Intended study question:** No new study. Correct the account of the existing study's executed coverage.

### T-003 scope

- **Objective:** Resolve the independent review's bound-compliance finding faithfully.
- **Why now:** Round 1 review identified nine unapproved below-bound oracle coordinates despite the frozen window statement.
- **Scope:** Add a native-record erratum/classification receipt, correct goal answer/readiness/transfer citations, preserve frozen data, and recheck the correction. No new scientific evaluation, changed bound or acceptance limit.
- **Inputs:** goal.md; evidence/final-review.md and final-review-checks.json; frozen study at a16e7256.
- **Done when:** Exact nine exceptions, corrected denominators and unchanged native conclusions are independently checked; dispositions and learnings reflect the corrected scope.
- **Stop when:** Unresolved evidence discrepancy or owner-held change in scientific meaning.

### T-003 start — 2026-09-16

T-003 · frozen study reading and goal interpretation · native coverage erratum plus corrected answer and reviewer diff check.

### T-003 return — 2026-09-16

- **Outcome:** COMPLETE.
- **Evidence:** Native study coverage-erratum.md and coverage-erratum.json; appended record correction; corrected synthesis, goal answer/readiness/transfer contract. Frozen inputs/results/snapshot unchanged.
- **Reading:** Declared-window/control coverage is 191 unique coordinates: 185 evaluated and six refused. Nine below-bound oracle-only diagnostics remain separately visible. None entered the 71 native cases; no numerical or transfer conclusion changes. The raw 201-call/200-coordinate record is preserved.
- **Decision:** Independent evidence of unapproved current excursions requires explicit scope correction rather than retroactive bounds; execution detail correcting a protocol error; coordinator; native erratum and named interpretation documents. No new scientific assumption or owner gate.

### Round 2 result — 2026-09-16

- **Intent:** Met: correction deposited without changing frozen data or claiming unauthorized coverage.
- **Task sequence:** T-003 COMPLETE; no scientific re-execution, new pin or new study.
- **Last semantic outcome:** COMPLETE.
- **Stop reason:** Corrected answer contract fulfilled → goal answered, subject to the same reviewer's correction check and owner-held formal close.
- **Evidence refs:** Frozen study a16e7256 plus current coverage erratum and goal interpretation edits (unpinned; no native digest until final custody commit).
- **Learning delta:** L-001–L-003 from Round 1 retain their substance with the corrected declared-window scope. The protocol deviation is recorded in the erratum; no compensating new process requirement is invented.
- **Finding dispositions:** Current #1 gains the exact coverage correction; #2–#5 and 42 prior dispositions preserve accepted routing. Joined append-only rows follow final independent acceptance.

### Round 2 review — 2026-09-16

- **Reviewer:** Fresh continuing non-author `/root/reviewer`; evidence/round2-review.md.
- **Verdict:** PASS.
- **Checks:** Exact nine exception IDs/inputs/verdicts, corrected 192 planned/control calls and 191 unique coordinates (185 evaluated, six refused), unchanged 71 native cases, all 228 frozen artifact hashes and original snapshot bytes, append-only record correction and corrected answer/synthesis/readiness verified. Reuses Round 1 all-point numerical/custody evidence and original framing/source coverage.
- **Learning delta:** L-001–L-003 accepted with corrected finite-sample scope; appended to learnings.md below this assurance boundary.
- **Finding dispositions:** Corrected current #1, remaining #2–#5 and 42 prior dispositions accepted. Coordinator publishes joined preservation/correction rows without scientific follow-up. No prior first sighting is edited.
- **Next:** Technical objective answered. Owner-held formal goal close recommended on the bounded-negative/conditional-transfer outcome; reveal remains separate. No further technical correction required.

## Goal close — 2026-09-16

- **Authority:** [OWNER-VERBATIM] “ok please close the goal”.
- **Decision:** Close `bounded-feasibility-transfer` on the reviewed answer and corrected coverage at `53338f04`, retaining the frozen numerical study at `a16e7256` and independent Round 2 PASS at `53338f04`.
- **Outcome:** Bounded negative feasibility result, conditional design-point transfer contract and remaining pre-reveal preparation accepted as the completed goal outcome. No global infeasibility or technology qualification is inferred; the nine-point protocol correction remains explicit.
- **Recorded changes:** Goal status, answer closure note and project context updated. Administrative closure requires no new round, study or model change. ARIES remains sealed.
