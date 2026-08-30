# Product-Lens Ledger — goal-integration-study-proof (GSTH Item 6)

Append-only. One block per run; a changed gate is a new dated block. Resolution is by citation of a finding id, never by recency.

## close — 2026-08-30 — rev `d6b7b400`

Epic: GSTH (`.project/backlog/epic_goal_strategy_task_harness.md` § Item 6)

**Execution note.** This run was performed inline because the session's collaboration rules did not authorize spawning the product-lens subagent. The canonical product-lens spec was read directly, and its oracle-first order was followed: the durable product sources below were read before this item's work.

**Point (re-derived):** A non-builder must be able to operate the goal loop from the repository's documentation, through the same native seams and judgment gates as the goal agent, while native workflows keep ownership of their technical state. For this item, the proof must carry one exact candidate through study and reviewed finding closure, then show that the documented human and goal-agent routes meet the same operable contract without adding hardening machinery that no recorded failure earned. [source: `.project/concepts/goal-driven-model-development-harness.md:22-24,30-33,43-50`; `.project/backlog/epic_goal_strategy_task_harness.md:46-58,431-481`; `work/orchestration/GOAL_RUNBOOK.md:9-20,138-181,250-267`; `.project/adr/003-lean-first-persistence.md`; grade: owner for human operability, criticism, resume, and lean-first scope; agent/ratified for the Item 6 decomposition and exact equivalence dimensions]

**Falsifier:** A fresh non-builder follows the documented integration route from an isolated checkout and either cannot run the documented command or receives a semantic blocker for an unchanged toolchain, while the goal-agent route returns `CANDIDATE` for that same package and lineage.

### Findings

- **close-F1 [DON'T] — the close evidence declares route equivalence met after the falsifier occurred.** The hand route's first usable integration result required bypassing the guide's copy-paste `uv run` invocation and calling the sealed interpreter directly. Before that correction, the checkout-local `STOP_PARSER_WHEEL_TARGET` mismatch was reported as `toolchain-drift`; the unchanged operator guide maps that condition to `STRATEGY_BLOCKER`, so a reader following the documented contract would close the round on a strategy failure even though the wheels and candidate had not changed. `route_equivalence.md` states both failures and says the written pattern is not hand-reproducible from a fresh checkout, but `epic_evidence.md` criterion 5 still reads **met** and its proof-chain conclusion says two operators proved the same contract. This contradicts the owner's requirement that a non-builder can operate the loop from clean documentation. — `.project/concepts/goal-driven-model-development-harness.md:22-24,50`; `.project/active/goal-integration-study-proof/route_equivalence.md:25-42`; `.project/active/goal-integration-study-proof/epic_evidence.md:99-107,124-133,162-166`; `docs/integration_seam_operator_guide.md:23-45,69-97,197-216` (owner for the product obligation; agent/ratified for the route-equivalence criterion) — **disposition: BLOCK** (expected: either repair the environment/guide contract and re-run the isolated hand integration without an undocumented correction, then append a block resolving `close-F1`; or obtain an owner disposition narrowing what “same operable contract” means and amend the criterion/evidence accordingly)

### Reverse check

**CLEAR.** The study record, five kept integration returns, goal trail, critic and review entries, joined discovery rows, route comparison, proof report, and verification record each trace to an Item 6 criterion or to evidence a fresh reviewer needs. The four hardening candidates are recorded observations, not unauthorized mechanisms. No orphan product work found.

### Fired smells

- **A consumer compensates for something the producer or platform claims to guarantee** and **a test passes only because it selects one route or interpretation** both fire on `close-F1`: the hand consumer supplied an interpreter/environment correction absent from the documented route, then the report selected the corrected run to declare equivalence while leaving the documented semantic misclassification in place.
- **Two representations must be manually kept synchronized** fires on the five stale expectation artifacts recorded in `epic_evidence.md:135-143`. It does not add a close finding: this proof exposed the class, accepted it as learning L-001, and correctly left promotion to ADR-003's owner-visible hardening path.
- **A special category exempts a case whose user-visible meaning is unchanged** fires on the 42 `p_net <= 0` points excluded as unevaluable before `net_positive` could report violated. The item disclosed the manufactured clean sheet and the owner routed the producer defect to WI-034 at `5d740688`; that is a visible disposition, not a hidden exemption.

### Gate

**BLOCKED (`close-F1`).** The earlier epic-plan product-lens block remains historically CLEAR for its two planning findings, but it does not resolve this item-local close finding. Item close and any epic claim that route equivalence is proved remain blocked until a later ledger block cites `close-F1` with an authorized resolution.

## close — 2026-08-30 — rev `f3249f7c` (resolution block)

Resolves:
- **close-F1: FIXED** — authority: the finding's own first expected remedy (repair the environment/guide contract and re-run the isolated hand integration without an undocumented correction). Basis: `f3249f7c` adds the checkout-kind carve-out to the guide's `toolchain-drift` row, documents the sealed-interpreter pattern in a new § Running from a second checkout or worktree, and scopes the always-`uv` exception in CLAUDE.md; a fresh guide-only operator (session `0d76b3a4`, brief `briefs/hand-rerun-f1.md`) then re-ran the isolated integration from a clean worktree following **only the committed guide**: exit 0, `CANDIDATE`, pin `20c2c364d6c7…`, all ten gates pass, verdict verbatim "Guide alone sufficed. No undocumented correction at any step." The evidence over-claim is amended in `epic_evidence.md` (criterion 5, § 4 F-1/F-2 rows, § 6 conclusion) to tell the failure-then-repair story rather than a clean pass.

Gate: **CLEAR**
