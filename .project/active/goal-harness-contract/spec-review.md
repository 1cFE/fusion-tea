# Spec Review: Lean Goal Contract and Operator Runbook

**Spec:** `.project/active/goal-harness-contract/spec.md`
**Contract:** `~/.claude/commands/_my_spec.md`
**Review File:** `.project/active/goal-harness-contract/spec-review.md`
**Date:** 2026-08-25
**Reviewer:** fresh session; did not author the spec

---

## Reality Check

**Sound.** The spec is about the right work item, the Problem section is accurate on every claim I could check, and the four epic scope groups are all present. I re-derived the load-bearing citations independently and they hold: `CLAUDE.md:73` carries "**CRITICAL: Do not cross-reference between them.**"; `runbook.md:221` says "The executor is the sole writer of the log."; `runbook.md:270` says "An administrator does not append to `DISCOVERY_LOG.md`"; the log header at `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3` says "Only a study's executor appends rows"; the log has exactly 22 rows and 6 are `unrouted`; `work/orchestration/handshake-lcoe-construction.md` exists; Item 6's pending findings `#6`, `#10`, `#11` are real and are recorded as Phase 4 runbook sentences in `.project/active/run-study-first-consumer/plan.md:309,323`.

The hardening boundary is clean in the direction the brief worried about most: I found no envelope, ledger, idempotency, reconciliation, concurrency, or dispatch mechanism smuggled into any requirement, and the owner-required evidence-citation digest survives at `spec.md:41`. Checkpoint-vs-`RoundReview` separation is stated explicitly and unambiguously at `spec.md:58`.

What needs work is narrower and mostly about one thing: the discovery-log amendment is scoped to the *sole-writer* sentence, and the writer change is not the only rule the joined-row design breaks.

---

## Audit

### Lens 1 — Faithfulness

**L1-1 · Direct claim:** *An agent inference is wearing an owner grade at `spec.md:42`.* The requirement reads `[NEED]` `[OWNER]` — "The evidence-citation digest above is **not** barred by the hardening rule. The hardening table's barred row is *authority* digests." The owner never said that. What the owner said, in review 1 § Resolutions P2/M4 (`goal-strategy-task-harness-design-review.md:209`), is a flat list: "The envelope YAML, event ledger, **digests**, idempotency keys, and reconciliation remain in the concept as the *hardening path*." The word "authority" is not the owner's — it comes from `goal-strategy-task-harness-design.md:186`, a row in an agent-authored table written under the owner's ruling. So the reconciliation between the two owner rulings is a defensible *inference from agent-authored text*, and it is graded `[OWNER]`.

The same narrowing is repeated twice more under owner grade: `spec.md:88` lists "authority/envelope digests" where the owner said "digests", and `spec.md:92` restates the reconciliation as settled — both inside a Non-Goals section headed `[OWNER]` at `:86`.

This matters beyond bookkeeping. Under the settled rule, an `[OWNER]` item is challenged by asking the owner; an `[INFERRED]` one is challenged by re-deriving it. If design finds the collision is real, the current grade tells it a false story about who it has to go back to. Regrade the reconciliation `[INFERRED]` (keeping the surface-don't-resolve-silently instruction, which is the right call) and mark the Non-Goals narrowing as the inference it is. The digest *term itself* at `:41` is owner-verbatim and correctly graded — that half is right, and I verified the quote.

**L1-2 · Question to the user:** *Is `handshake-lcoe-construction.md` the bar you have to match, or an example of the kind?* `spec.md:77` marks it `[REFERENT]` — under capture-fidelity that means binding, the bar to match, not an illustration. I could not find you saying that. The epic calls it a "proven prose referent" in Required Reading (`epic_goal_strategy_task_harness.md:120`) and says it "proves that graded inputs, owner gates, and a prose stage log can carry multi-session work" (`:109`) — agent-authored framing. `align.md` doesn't mention it. The product-lens ledger records the `[REFERENT]` marking as "authority: owner", but the only owner statements on record from 2026-08-25 are align.md's four rulings, and this isn't among them. The force matters: a 13 KB binding referent for `GOAL_RUNBOOK.md` is a materially bigger deliverable than a 13 KB illustration of the register.

**L1-3 · Direct claim (clean):** everything else I sampled traces. The checkpoint `[NEED]`s at `:58`/`:59` match the epic's `[OWNER 2026-08-25]` success criterion (`epic:49`) and the concept's SC 5 ("loop with their critic until it passes or a declared cap is hit") and SC 7 ("no run ends silently") word for word. The writer-ownership `[NEED]` at `:69` matches review 1 C1 (`review:206`) and review 2 `mi1`'s three-site list (`review-2:136`). Both `[OWNER-VERBATIM]` quotes at `:77` match `goal-driven-model-development-harness.md:22` and `:24` exactly. The align rulings at `:71`, `:79`, `:80` match `align.md:7,9`. The seven ADR provenance grades at `:40` match the design's rulings table (`design.md:219-227`) row for row, including the Lean-First split and the Supersession split. `:60`'s handling of the homeless post-execution audit critic is honest — it names the placement as `[AGENT]` and owner-overridable rather than quietly asserting it.

### Lens 2 — Problem & Approach

**L2-1 · Question to the user:** *Is 8 hours of execution real for this?* The epic budgets 1.5 days (spec 1h, design 2h, plan 1h, execute 8h). The execute half is: invent an ADR convention from scratch, file seven records with their reasons/seams/rejected alternatives, write section conventions for three prose file types, write the templates, write `GOAL_RUNBOOK.md` to a handshake-grade bar, amend CLAUDE.md, amend three (see L3-1: five) textual homes across two files, and write contract tests. If the answer is "it'll overrun, that's fine," nothing changes. If the estimate is load-bearing, the natural cut is records-and-amendments first (SC 1, 4) and runbook-plus-templates second (SC 2, 3, 5) — Item 4 needs both, so it's a sequencing question, not a scope one.

**L2-2 · If-then tradeoff:** *The ADR-home open question is missing its prior art.* `spec.md:103` defers path, naming, template, and numbering to design as if the field were empty, on the strength of the design's "no project ADR directory exists (0 entries)". That's true as stated but incomplete: `modeling_project/ARCHITECTURE.md` already carries seven decision records under an `AD-XXX` convention, and `exploration/phase_1a/ADR-001_csv-source-of-truth.md` is a stray one-off in the older style. **If** the intent is one repository decision-record convention, design should be told to weigh extending `AD-XXX` before minting a third form; **if** orchestration decisions are deliberately a separate register from modeling decisions, say that, because the design's Prior Art line already noticed AD-001–AD-007 and passed over them without a reason. Related and more urgent: align ruling 3 has Item 2 filing into this home "once it exists," and Item 2 is running *now* in a parallel worktree. The spec records that as a coordination note; it is closer to a live scheduling dependency.

**L2-3 · Question to the user:** *The one control you added has the latest proof in the epic.* The pre-execution disposition checkpoint is the owner-originated addition (`epic-plan-F2`), and Item 1 contracts it in prose only. Its first live exercise is Item 5, which sits behind Items 2 and 4. Item 4 — the cold-pickup proof, and the first time a non-builder touches this contract — never runs the checkpoint. Should Item 1's deliverable include one worked example of the checkpoint (verdict shape, revision iteration, cap-hit stop) that Item 4 can dry-run against an existing `unrouted` row? Arguing the other side: that's a proof, and proofs belong to Items 4–6. But the cheapest version is a template, which is squarely this item's job.

### Lens 3 — Pipeline Risk

**L3-1 · Direct claim (must-fix):** *The three-home list is the wrong list. Joined disposition rows break a rule that lives in two more places.* The spec's writer-ownership requirement (`spec.md:69`) and success criterion 4 (`:31`) name three homes, all carrying the *sole-writer* sentence. But the change the owner ruled — a goal round **appends** a disposition row joined by `<study-id>#<n>` — also breaks the log's cardinality rule, which lives in two homes the spec never names:

- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:3` — "**One row per finding**; the finding's account lives in its record's § 15 and is never copied here."
- `.claude/skills/run-study/runbook.md:290-292` (§ `DISCOVERY_LOG.md`) — "An append-only index, newest row last — **one row per finding**, never a second copy of the finding's account." The schema table at `:294-296` is likewise one row per finding, with a single `Disposition` and `Home` cell.

SC 4 as written requires the homes to agree "on writer ownership **and joined `<study-id>#<n>` disposition rows**." With the amendment scoped to writer ownership only, they cannot: the executor's first-sighting row and the goal round's disposition row are two rows for one finding, which the header and the schema section both forbid. There's a second, deeper ambiguity underneath it that design will hit immediately and the spec should settle or explicitly defer: does the goal round **append a new row**, or **amend the existing row's `Disposition`/`Home` cells**? The design says "appends disposition rows" (`design.md:170`), the epic success criterion says "receives a joined `<study-id>#<n>` disposition update" (`epic:53`) — append and update are different edits to a file whose header says append-only and one-row-per-finding.

**L3-2 · Direct claim:** *A live contract test already guards this file and the spec doesn't know about it.* `tests/study/test_records.py:41-64` (`test_findings_join_the_discovery_log`) asserts that, for each committed record, the set of `<record>#<n>` ids in its § 15 equals the set found in the log's `Record` column. Two consequences the spec should name as constraints rather than let design discover:

- The comparison is set-based, so a duplicate joined row for an existing id passes today. That is luck, not design — and it's the single fact that decides whether "append a row" is even viable without rewriting the test.
- A goal-appended row whose `Record` cell cites an id **not** in that record's § 15 fails the test for that record. If a round's evidence touches a finding and the goal wants to record a disposition under a new id, this test blocks it.

`spec.md:106` defers "the shape and home of the consistency tests" to design as if the field were empty. There is an existing test on exactly this surface; it belongs in the spec as an existing-system constraint (`[HARD]`), not as an open question.

**L3-3 · Direct claim:** *Success criterion 1 has no matching requirement.* SC 1 (`spec.md:28`) is three-part: the decisions must be live, provenance-graded, **and cited by the runbook and affected project guidance**. The § Architecture records requirements cover "live" (filing) and "provenance-graded" (grades preserved) and cover one guidance surface (the Goal Evidence Seam record naming `CLAUDE.md:73`). Nothing anywhere obliges `GOAL_RUNBOOK.md` to cite the ADRs — § Operating surface at `:75-78` says what the runbook must describe, never that it must cite the decisions it rests on. As written, an implementer can satisfy every requirement and miss a third of SC 1.

**L3-4 · Rewrite request:** *`spec.md:71` describes an obligation that doesn't exist yet.* It says Item 6's findings `#6`, `#10`, `#11` "must survive these edits intact." They are not in the runbook to survive — they are *pending* sentences that Phase 4 will land later (`run-study-first-consumer/plan.md:309,323`). The requirement's second sentence gets it right ("must not clobber or pre-empt them"). Ask the spec agent to make the first sentence say the same thing: this item edits the shared runbook first, and its edits must leave room for Phase 4's three pending sentences rather than pre-empting or contradicting them.

**L3-5 · Rewrite request (minor):** `spec.md:81` illustrates the contract tests with a concrete example ("a test asserting the three writer-ownership homes agree, and that the templates exist and parse") while `:106` defers test shape entirely to design. Either mark the example as illustrative of the *altitude* (lightweight consistency, not goal-agent machinery — which is clearly the point being made) or drop the specifics. As it stands the two lines pull against each other.

### Lens 4 — Hygiene

**L4-1 · Direct claim:** The discovery-log header's authority citation is already wrong and will be copied forward. `DISCOVERY_LOG.md:3` attributes "Only a study's executor appends rows" to "`.claude/skills/run-study/runbook.md § DISCOVERY_LOG.md`". That section (`runbook.md:288-299`) contains no writer rule — the sole-writer sentence is in step 14 at `:221`. Worth fixing in the same pass, since the amendment touches both.

### Lens 5 — Reader Comprehension

**L5-1 · Rewrite request:** § Lean artifact contract is seventeen compressed bullets whose labels are coined terms the spec never unpacks — "Six-value task return", "Five decision fields", "Write-ahead start", "Round limits". Each bullet is dense enough to need a second read, and the section opens straight into them with only a one-line statement of the directory layout. A reader who has read the concept-design will follow it; a reader who hasn't (the operator this whole item exists for) will not. Ask for two or three sentences at the top of the section framing what the three files are *for* — what `goal.md` fixes, what `trail.md` accumulates, what `learnings.md` carries across rounds — before the enumeration starts. The bullets themselves are fine and shouldn't grow.

---

## Engagement Summary

**Overall take:** The spec is faithful where it's hardest — the seven provenance grades are preserved individually rather than flattened, the owner's digest term survives, the checkpoint's cap-and-owner-visible-stop is captured, and nothing from the hardening path is smuggled in. Two things need fixing before this is a safe design contract: one owner grade sits on an agent inference, and the discovery-log amendment is scoped to the wrong set of textual homes — the joined-row change breaks a "one row per finding" rule in two places the spec never names, with a live test sitting on the same file.

**Here's what I need you to weigh in on:**

1. **[L3-1]** The discovery-log amendment. Joined disposition rows contradict "one row per finding" at `DISCOVERY_LOG.md:3` and `runbook.md:290-292` — two homes beyond the three the spec lists. And it's still open whether the goal round *appends a row* or *amends the existing row's cells*. Decide the append-vs-amend question, or file it explicitly as a design question; either way the home list has to grow to five.
2. **[L1-1]** The digest reconciliation at `spec.md:42` is graded `[OWNER]` but you never said it. Your P2/M4 words bar "digests" flatly; "authority digests" is the design table's wording. Regrade to `[INFERRED]` (keeping the surface-it-don't-resolve-it instruction), or tell me it is your ruling and it stays `[OWNER]`.
3. **[L3-2]** `tests/study/test_records.py:41` already guards the log's record↔row join. It happens to tolerate a duplicate joined row because it compares sets. That accident is currently the only reason "append a row" works at all — it should be a named constraint in the spec, not a discovery design makes on day one.
4. **[L1-2]** Is `handshake-lcoe-construction.md` the bar `GOAL_RUNBOOK.md` must match, or an illustration of the register? The spec marks it binding on agent authority. This changes how big the runbook deliverable is.
5. **[L3-3]** Success criterion 1 requires the decisions be "cited by the runbook"; no requirement says so. Add one, or trim the criterion.
6. **[L2-1, L2-3]** Sizing and proof timing. 8 hours covers an ADR convention, seven records, three sets of section conventions, templates, a handshake-grade runbook, four file amendments, and tests. And the checkpoint you added is contracted here but first exercised in Item 5, behind Item 2 — worth deciding whether Item 1 ships a worked checkpoint example that Item 4 can dry-run.

---

## Resolutions

*(To be filled in as findings are resolved. Keyed by finding ID; the spec agent reads this section to incorporate the review. The reviewer does not edit the spec.)*

---

**Verdict:** **Revise**

The work item is right and most of the capture is good. L3-1, L1-1, L3-2, and L3-3 are must-fix; L1-2 and L2-1/L2-3 are owner decisions; L3-4, L3-5, L4-1, L5-1 are cheap.

**Next Steps:** Record resolutions above, then re-run `/_my_spec` (or return to the spec-agent session) pointed at this review to incorporate. The reviewer does not edit the spec.
