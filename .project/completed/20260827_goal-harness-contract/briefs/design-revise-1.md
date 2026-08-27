Orchestrator feedback — independent design review returned Revise (`.project/active/goal-harness-contract/design-review.md`; read it in full, and the lens block appended to `product-lens.md`). Apply these dispositions and revise design.md:

**Must-fix:**

- **C1 (external mutation voids authority).** Design it. Direction to test, not to copy: the spec's rule is judgment-read, not procedure-compared — the resumer and `RoundReview` verify cited refs as part of reading the trail, and a cited work item changed outside the active task produces a recorded stop + re-ground/close, a human-legible rule like the rest of the contract. If that survives your re-derivation, I6 and C1 don't collide (same person-vs-procedure split as D8). If you find they genuinely do collide, STOP and surface to me — do not design around it silently. Either way the invariant, its trail entry, and its runbook sentence need homes.
- **C2 (round closure).** Give the one-pin/one-study bound and all six close triggers a designed home: how a round opens and closes in `trail.md`, and how a fresh reader answers "is this round open?" from the file alone.
- **M1**: either add a lightweight test asserting I6's checkable content or stop calling I6 "the testable form" — no overclaiming either way.
- **M2**: say what the evidence digest is for untracked evidence (gitignored study stores, R2 binaries). Lean direction: cite the hashes native records already carry (study records, MANIFEST.jsonl) rather than minting new digest machinery; if a class of evidence has no native hash, say so plainly.
- **M3**: correct the two false rejection reasons (`.claude/commands/manage-concept.md` is real, same for the skills claim). Conclusions may stand on the surviving reasons.
- **M4**: define the goal-discovered-finding case, don't leave it undefined. Owner-ruled writer split says first sightings are executor-written — so presumably a goal agent never mints finding ids and a joined row must cite an existing `<study-id>#<n>`; state the rule where an operator will meet it.
- **M5**: make the joined-row guarantee a failing test, not a docstring — a fixture with a duplicate-id joined row that must be accepted, so rewriting `in_log` set→list breaks the suite visibly.
- **M6**: re-verify the pending-findings list against `run-study-first-consumer/plan.md` precisely (both studies have a #10; possibly four sentences, and Phase 4's checklist names none) and restate disjointness against the corrected list.

**Nits:** fix all — especially restore the four dropped `[INHERITED]` clauses (no-future-task-list, PREREQUISITE-never-predicted, stop-reason-not-a-second-enum, review-never-resumes); also the test-1 prefix trap, D4 premise wording, revision-entry append semantics, five-vs-six count.

Then resolve the product-lens gate: append a resolution block dispositioning design-F1/design-F2 with the authority basis, per the ledger's convention.

Finish with the revised design at the same path. ARTIFACT line when done.
