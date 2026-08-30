# Changelog

Historical record of completed work.

---

## [2026-08-30] - Epic: Goal Strategy and Task Harness

**Type**: Epic (GSTH — 6 items)
**Duration**: 7 days (epic created 2026-08-23 → closed 2026-08-30; items closed 2026-08-27 → 2026-08-30)

### Summary
Research, modeling, package generation, and study procedures worked separately, with no durable layer owning why one should follow another, and the research and integration seams still depended on documented hand patterns. This epic built the lean goal layer — `goal.md`/`trail.md`/`learnings.md` per goal plus the shared `work/orchestration/GOAL_RUNBOOK.md` — repaired both seams as native callable returns, and proved the joins live: cold grounding, ungrounded rejection, and mid-task resume (Item 4); a research-to-model round where the owner's pre-execution checkpoint bound and released for the first time (Item 5); and integration-to-study closure with hand and goal-agent routes byte-identical on native identity (Item 6). All eleven epic success criteria are ticked at close; the three declared limits are recorded in the epic evidence, not worked around.

### Deliverables
- `.project/completed/20260830_epic_goal_strategy_task_harness.md` — the epic record (criteria ticked with per-criterion evidence pointer, product-lens gate CLEAR)
- Item archives: `20260827_goal-harness-contract/`, `20260827_goal-research-seam/`, `20260827_goal-integration-seam/`, `20260827_goal-cold-pickup-proof/`, `20260828_goal-research-model-proof/`, `20260830_goal-integration-study-proof/`
- `work/orchestration/GOAL_RUNBOOK.md` with every seam row native; `scripts/research_seam.py` + `scripts/source_registry.py` (research seam); the integrate seam + `docs/integration_seam_operator_guide.md`
- Three goals grounded and closed under the contract: `work/orchestration/goals/cryo-volume-basis/`, `p-pump-basis/`, `p-pump-fence/`
- ADR-0008 (source identity), ADR-0009 (integration fixed-point proof), ADR-0010 (oracle mirrors audited bindings); product ledger entry 0001; WI-033 landed, WI-034 minted

### Lessons Learned
- The recurring discovery was the stale-expectation class: five hand-maintained expectations of package output (manifest headline, independent oracle, two test fixture sets, annex prose) surfaced one at a time across the round. Accepted as learning L-001 (`work/orchestration/goals/p-pump-fence/learnings.md`), deliberately not promoted to machinery per the epic's hardening rule.
- Route equivalence earned its keep by failing first: the guide was not hand-reproducible from a fresh checkout (`close-F1`), and the honest resolution — repair the guide/env contract, then a fresh guide-only re-run — proved more than a clean first pass would have. Record: Item 6 `product-lens.md` resolution block, `route_equivalence.md`.
- Lean-first held across all six items: no control-plane mechanism was promoted; four hardening candidates are recorded with fix homes (`epic_evidence.md` § 4), and the three declared limits are stated rather than worked around (§ 3).
- Register renames need a repo-wide reference sweep: the four-digit ADR migration updated `tests/orchestration` but missed a `tests/study` consumer of the old filename/index format, caught at the pre-PR battery (fixed `e64d2136`).

---

## [2026-08-30] - Goal Harness Item 6: Integration-to-Study Closure and Route Equivalence

**Type**: Item (Goal Strategy and Task Harness epic, Item 6 — the epic-verdict deliverable)
**Duration**: 2 days (spec 2026-08-29 → close 2026-08-30)

### Summary
The goal loop's back half had never run: no round had consumed the native `integrate` return, promoted a pin, committed a study against it, and closed on the reading — and the documented human and goal-agent routes had never been compared. This item did all of it live, under a real successor goal (`p-pump-fence`) grounded on the open tail of discovery row `20260821-power-cycle-ab#3`. The seam refused four times for four designed reasons before returning one CANDIDATE; the 906-point study moved the `recirc_ok` fence from a 32-point corner to a 184-point band and put LCOE +21.0 % at baseline, with a 42-point net-negative region disclosed as an evaluability bound; a fresh administrator read the committed record alone; a checkpoint critic refused once and passed the revision; a fresh RoundReview upheld the answer; the owner closed the goal. Route equivalence came back byte-identical on native identity — and the product-lens close gate then blocked on the one over-claim in the evidence, which was resolved the honest way: repair the guide/env contract, re-run the hand integration from documentation alone, amend the evidence to the failure-then-repair story.

### Deliverables
- `20260830_goal-integration-study-proof/` — spec (lean shape), plan (9 phases), audit (POSITIVE), `epic_evidence.md` (all 7 epic criteria + criterion 8 mapped), `route_equivalence.md` + hand synthesis, `verification_record.md`, `product-lens.md` (BLOCK → CLEAR), 21 stage briefs
- `exploration/stellarator_e2e/studies/20260829-p-pump-fence/` — committed study record, fresh-administrator synthesis, addendum with re-derived artifacts
- `work/orchestration/goals/p-pump-fence/` — goal closed by owner ruling; trail with five seam returns kept as evidence; four accepted learnings
- Seven joined `DISCOVERY_LOG.md` disposition rows; **WI-034** minted (CAS10 land-term guard); `GOAL_RUNBOOK.md` `integrate` row flipped native; `docs/integration_seam_operator_guide.md` secondary-checkout contract

### Notes
- The stale-expectation class was the round's recurring discovery: five hand-maintained expectations of package output (manifest headline, independent oracle, two test fixture sets, annex prose), found one at a time by gate 8, the battery, and a human read — accepted as learning L-001, not promoted to machinery.
- The oracle carry (`p_pump` 1.0 → 195.0 in `verify_stellaris.py`) was an explicit owner override of a written prohibition; ADR candidate pending owner yes/no at close.
- Hardening verdict: nothing promoted. F-1/F-2 (fresh-checkout reproducibility) fixed at close as documentation; F-3/F-4 recorded with fix homes.

### Lessons Learned
[TODO: Add lessons learned]

---

## [2026-08-28] - Goal Harness Item 5: Research-to-Model Round Proof

**Type**: Item (Goal Strategy and Task Harness epic, Item 5)
**Duration**: 2 days (spec 2026-08-27 → close 2026-08-28)

### Summary
The goal layer had never run the sequence it exists for, and the owner's central requirement — that criticism sits before work compounds on a misread — had never bound on a live round. This item ran one, on a real open question rather than a rehearsal: `p_pump` = 1.0 MW in two committed A/B studies, roughly 100× below admissible helium-primary circulator figures, with the discovery row still open and DI-008's strongest primary not ingested. Eight cold sessions grounded the goal at `work/orchestration/goals/p-pump-basis/`, ran a bounded task, put the reading and the proposed dispositions through a fresh critic that refused and then released, appended joined disposition rows, closed through a `RoundResult`, and had a fresh reviewer close the round. What it proves is the **model → critic → disposition → review** spine. It does **not** prove the research half: `T-001` came back `COMPLETE` because the repository could answer the question, so the Item 2 seam was never invoked, no work item was minted during the round, and the runbook `research` row is still stale. Four of nine criteria therefore carry no live evidence — three non-exercised under a covering branch declared before the round opened (`covering-branches.md@e02ce403`), one retired by owner ruling — and the record says so in every row rather than manufacturing a research need to light them up. The goal was closed by owner ruling with the answer written and sourced (1.0 MW is not defensible; ~4–6 % of thermal power, ~130–195 MW at the baseline point), and the model change routed to **WI-033** in the modeling PM.

### Deliverables
- `20260828_goal-research-model-proof/verification_record.md` — the proof report: all nine criterion rows settled against disk, both ordering predicates as git-ancestry checks, ten pasted invariant outputs, and a § Failures section with eight entries covering every point the prose route was ambiguous, misread, or failed
- `covering-branches.md` — the four possible outcomes and which criteria each covers, committed at `e02ce403` before the round opened, amended at `08af1532`; both ancestors of the outcome commit `71d2abe8`
- `sessions/` — eight kept cold-session transcripts with their input briefs, plus `freshness-record.md` and `operator-notes.md`
- Workflow record: `{align,spec,spec-review,design,design-review,plan,audit,product-lens}.md` and the stage briefs
- `work/orchestration/goals/p-pump-basis/{goal,trail,learnings}.md` — the second live goal, kept as goal-layer state, closed by owner ruling
- Two joined `DISCOVERY_LOG.md` disposition rows appended under existing ids `#3` and `#5`; DI-008 corrected to a divertor-relative floor; WI-033 minted
- `.project/adr/003-lean-first-persistence.md` § Amendment 2026-08-28 — the second hardening measurement recorded against the decision it tests

### Notes
- Audited 2026-08-28, verdict **POSITIVE**. The auditor re-ran all nine criterion rows, both ancestry predicates, and all ten invariant checks against disk — including the fence sweep over 174 tool calls across eight transcripts, all clean — and every figure in the record reproduced exactly. Five findings, all citation and bookkeeping defects in the item's own records, all fixed the same day (`c389afc1`) as objectively verifiable corrections with the verification recorded; no re-audit, per the pipeline rule.
- **Honest scope, stated in the epic.** Item 5 does not discharge the research-seam half. The epic's Item 5 criteria 1, 3 and 4 stay `[ ]` with their dispositions named, and Item 6's Current State now says plainly that no research return exists and that `GOAL_RUNBOOK.md:256`/`:264` still route a research disposition to the pre-seam hand pattern. Whichever item next runs the seam live owes both.
- **Hardening verdict: nothing promoted.** Eight recorded failures, every one caught by a cold session, the fresh reviewer, the operator, or the audit trail. The item contains no code at all. Two things the run added over Item 4's measurement: the trail carried an owner-visible critic-versus-author disagreement without an in-place edit, and a three-step mid-run sandbox degradation was absorbed by stopping cleanly and saying why.
- **The negative result is the valuable one.** Criterion 1's bet — that a bounded task would discover a prerequisite blind — measured false, and the cause generalizes: a need selected *because* it is documented carries its own answer in the evidence pointers the grounding step must walk. Retired by owner ruling, with the measurement kept as the item's finding rather than discarded.
- Product-lens gate **CLEAR** at close (run at close rather than at spec, which `spec-review.md:30` had flagged); two findings, both dispositioned in the same hop. No product ledger exists in this repository (`.project/product/`, `product.sh` absent), so the promise scan filed nothing — gap noted, not worked around, as in the Item 2/3/4 closes.

### Lessons Learned
[TODO: Add lessons learned]

---

## [2026-08-27] - Goal Harness Item 2: Native Research Acquisition and Registration Seam

**Type**: Item (Goal Strategy and Task Harness epic, Item 2)
**Duration**: 2 days (spec 2026-08-25 → close 2026-08-27)

### Summary
Research was the one hop in the model-development loop with no callable boundary. Modeling has the `work/` PM, generation has sysml-codegen, studies have the run-study skill; research had a reading command, an extraction primitive, and a Zotero-shaped registry writer, with nothing joining them. The loop had already run this hop by hand once — WI-031 registered two URL sources through shell steps and hand-written `SOURCE_INDEX.md` blocks, leaving `MANIFEST.jsonl` untouched because it had no slot for a non-Zotero source. This item builds the missing boundary at the producer: a bounded request goes in, exactly one of four returns comes out, every registered source is MR-4-citable by repo-relative path with provenance to re-fetch and verify it, and the ARIES-CS hold-out is checked in code before any byte is written.

### Deliverables
- `scripts/source_registry.py` — the single write door into `knowledge/`: capture into staging, provenance verification, dedupe, a fixed commit ladder under a lock with exact rollback, receipts, two index-writer profiles, and `verify` (0 faults / 3 legacy on the current repo)
- `scripts/holdout_guard.py` — parses both §3 barred lists of `knowledge/holdout/aries-cs/PROTOCOL.md` and fails closed on a bad parse; no waiver exists in code
- `scripts/research_seam.py` — bounded request, request-key negatives, run record, and the four return classes computed from receipts and triage log rather than agent claims
- `.claude/commands/research-acquire.md` and `docs/research_seam_operator_guide.md` — the acquisition protocol and operator documentation (SC9)
- `scripts/zotero_ingest.py` / `zotero_lib.py` extended; both Zotero paths are now callers of `register`, and the local-PDF path finally writes its manifest row
- `tests/research/` — 150 tests, offline against a loopback HTTP fixture and a generated PDF, running the real extraction subprocess
- `.project/adr/008-source-identity-raw-bytes-sha256.md` — the R-F2 decision, filed 2026-08-25 into Item 1's register
- Workflow record: `20260827_goal-research-seam/{align,spec,spec-review,design,design-review,plan,audit,product-lens}.md` and the stage briefs

### Notes
- Audited 2026-08-26, verdict **Needs Work**, two HIGH findings, both real and both reproduced by the auditor: the staging sweep deleted every in-flight registration's working directory outside the commit lock, and a candidate blocked at triage (a paywall — the spec's own first-named reason to queue) could not reach `OPERATOR_QUEUE`, so the documented sequence closed the run `BOUNDED_NEGATIVE` and wrote a durable negative that then blocked its own request.
- Fix pass complete the same day (`9637f1b7`), all eight findings addressed: the sweep is now lock-held and age-thresholded with each attempt owning its own staging directory; `close` reads the queue from triage failures as well as receipts; design D7 amended and D13 corrected against the spec's class table, which is the authority. Regression tests reproduce both audited failures. 150 tests green, all nine success criteria marked.
- **The hold-out invariant did not change owners.** `--holdout-ack` was deleted at design review; there is no override in code, and the human exception path stays PROTOCOL §6, outside this seam. Extending the protocol with a machine-readable exception was surfaced as an owner question, not resolved.
- Two breaking-ish operator changes: `zotero_ingest.py --local-pdf` now requires `--use-for` / `--validation` / `--caveat`, and index blocks insert before `## How Sources Are Used` — a missing anchor raises instead of appending at end.
- Two `agentic-mbse` defects were filed upstream rather than worked around (`PM-APPROVE-RESEARCH-EMPTY-INSIGHTS`, `EXTRACT-PROVENANCE-HOOK`); the entries sit uncommitted in that repository for the owner's commit. Carried in `.project/CURRENT_WORK.md` § Housekeeping owed.
- Product-lens gate CLEAR at both levels; the epic's `epic-plan-F1`/`F2` are FIXED and land in other items. No product ledger exists in this repository (`.project/product/`, `product.sh` absent), so the promise scan filed nothing — gap noted, not worked around.
- Closed on owner authorization 2026-08-27 under the one-PR ship ruling, with the audit verdict superseded by the orchestrator-verified fix pass rather than by a re-audit.

### Lessons Learned
[TODO: Add lessons learned]

---

## [2026-08-27] - Goal Harness Item 4: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof

**Type**: Item
**Duration**: 2 days (spec 2026-08-26 → close 2026-08-27)

### Summary
Item 1 shipped the lean goal contract — the runbook, the three templates, the `run-goal` skill, and ADRs 001–007 — and every file in it was written by the person who designed the layer. No session that was not that person's had ever used it: `work/orchestration/goals/` did not exist, no goal had been grounded, no round opened, no round reviewed. Three bets carried the epic's critical path untested, and the owner's hardening rule made a recorded proof run the only admissible evidence in either direction. This item is that run. It is a proof, not a build: thirteen kept cold sessions across twelve fresh agents grounded a real goal at `work/orchestration/goals/cryo-volume-basis/`, probed the grounding gate one field class at a time, took a real mid-task process kill and resumed it from disk, closed a bounded round, reviewed it fresh, and had a standalone reader answer four questions from the goal directory alone. Its output includes the places the prose failed.

### Deliverables
- Workflow record: `20260827_goal-cold-pickup-proof/{spec,spec-review,design,design-review,plan,audit,product-lens,align}.md` and the stage briefs
- `verification_record.md` — the proof report: three ancestry predicates, eight Required Invariant checks, and a § Failures section enumerating every point where the prose route was ambiguous, misread, or failed
- `sessions/` — fifteen kept cold-session transcripts with their input briefs, the evidence the proof rests on; `probes/`, `gate-probe-record.md`, `seed-record.md`, `freshness-record.md`, `interruption-state.md`, `operator-notes.md`
- Four re-runnable auditor scripts (`audit-c4-order.py`, `audit-fence-sweep.py`, `audit-brief-ordering.py`, `audit-reader-and-writes.py`)
- `work/orchestration/goals/cryo-volume-basis/{goal,trail,learnings}.md` — the first live goal, kept as product, closed by owner ruling R3 (`e891b23a`) with WI-032 archived to `work/completed/20260827_WI-032_cold-volume-basis/`
- `.project/adr/003-lean-first-persistence.md` § Amendment 2026-08-27 — the hardening measurement recorded against the decision it tested

### Notes
- Audited 2026-08-26, verdict **Certify** — with Criterion 8 certified as *not exercised as designed, not as a pass*. Eight of nine spec criteria met. The seeded drift was neutralized at the writer, and the audit confirmed the branch covering that outcome was declared in `design.md:269` and `plan.md` before the round agent ran (ancestry-checked). The review did catch a real organic drift, so the faculty is demonstrated; the designed test is not.
- Findings F1–F4 (conservative hand-tally slips in `verification_record.md`) fixed; the audit's one unreachable check — the external `~/goal-proof-logs/` cross-check — closed post-audit in `41b2fcc6`: fifteen log directories, one per enumerated run plus two Phase 0 mechanism checks, no unenumerated run.
- **Hardening verdict: no mechanism promoted.** Ten recorded prose failures, every one caught by a cold session, the fresh review, or the operator. Two table rows were exercised directly and neither triggered; the idempotency row stays untested rather than passed, because the resume was attended. Recorded as a dated amendment on ADR-003 at close.
- Two *written-rule* repairs, distinct from machinery, went to the owner and were taken into Item 1: the grounding gate's measured reach of 2 of 5 field classes (three sessions ran full tasks unguarded and none noticed), and the `GOAL_RUNBOOK.md:234` vs `:244` contradiction. The five-class rule was promoted into the runbook on the probe record (`4a8de283`).
- Epic Item 4 criteria 1 and 5 closed 2026-08-27 by owner ruling; the audit-time state of both is kept verbatim in the epic. Product-lens gate CLEAR — two `BLOCK` findings at the spec hop (the missing five decision fields, the grounding gate that could not hold as written), both resolved by citation in the same-hop disposition and re-checked at the implementation hop; parent epic gate CLEAR.
- Item 1's contract was left untouched by the run itself: `git diff` over `GOAL_RUNBOOK.md`, `goal-templates/`, and `.project/adr/` across the run is empty. The runbook amendment and the ADR-003 amendment are owner-authorized post-run acts, dated in place.
- No product ledger exists in this repository (`.project/product/`, `product.sh` absent), so the promise scan filed nothing. Gap noted, not worked around.

### Lessons Learned
[TODO: Add lessons learned]

## [2026-08-27] - Goal Harness Item 3: Verified Package Integration Seam

**Type**: Item
**Duration**: 2 days (spec 2026-08-26 → close 2026-08-27)

### Summary
Integration is the hop between an audited model change and a study that can run against it. Every gate that hop needs already existed and already failed closed — `sysml-codegen generate`, the model-family spine suite, `manifest.py`, `preflight.py`, `verify.py`, `identity.py`, and the dependency-provenance suite. What did not exist was a boundary that owned them together: the sequence lived in two work-item plans and a pile of shell commands, and neither was callable. The cost had already been paid once, when a scaffold commit changed a manifest without re-pinning the fixtures and Run-Study Item 6's Phase 2 opened with eleven red tests. This item built that boundary. `scripts/integrate.py` runs the ten gates in the producers' own order, stops at the first non-pass, and returns one verified study-ready candidate identity or one named blocker — never both, never a caveated candidate. The blocker says whether a gate *refused* or *could not run*, because the goal layer's retry rule reads that distinction and a round closes or continues on it.

### Deliverables
- Workflow record: `20260827_goal-integration-seam/{spec,spec_review,design,design_review,plan,audit,product-lens,align}.md`, two spike findings, and the stage briefs
- `scripts/integrate.py` — the seam CLI, ten producer-owned gates, two return classes, two modes, fourteen `condition` slugs closed at the constructor
- `docs/integration_seam_operator_guide.md` — the operator surface, including the `condition` → goal-class mapping and the stated coverage boundaries
- `.project/adr/009-integration-is-a-fixed-point-proof.md` — the prove-don't-perform decision
- Nine test modules under `tests/study/test_integrate_*.py`, including six real refusals driven from real producers and no mocks in the gate path
- Six `.project/backlog/BACKLOG.md` § Flagged rows routing each producer shortfall back to its own home

### Notes
- Audited 2026-08-26, verdict **POSITIVE — Certify**; spec SC1–SC6 all met. SC6's operator-guide walk was performed from the shipped guide alone, end to end, with zero source reads.
- Six non-blocking findings (reporting, coverage and documentation) fixed the same day in `2a9707df`, chiefly finding 1: the gate that stopped the sequence was recorded `not reached` even when it had run and refused. It now carries its own `fail` / `did not run` verdict per design D4, and the refusal tests pin that row rather than stepping over it.
- Product-lens gate **CLEAR** — four `BLOCK` findings raised across the spec and design passes, all four resolved by citation and re-checked against the shipped code at close. Parent epic gate CLEAR.
- Regression gate `pytest tests/models tests/study tests/test_dependency_provenance.py` — **395 passed, 14 skipped, 0 failed**. R-B2 frozen-producer diff over `scripts/study/`, `tests/models/` and `tests/test_dependency_provenance.py` empty.
- Two coverage boundaries are stated rather than closed: gate 5's refusal path has no hermetic driver, and `manifest.assert_read_set_covered` has no caller anywhere in the repository. Both are named in the guide, disclosed at runtime in gate 6's own passing detail, and filed.
- The three sealed wheels that `tests/test_dependency_provenance.py` pins now live at `/home/reid/1cfe/stop-parser-sealed-wheels/`; run anything in this area as `uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python -m pytest ...`.

### Lessons Learned
[TODO: Add lessons learned]

## [2026-08-27] - Goal Harness Item 1: Lean Goal Contract and Operator Runbook

**Type**: Item
**Duration**: 2 days (spec 2026-08-25 → close 2026-08-27)

### Summary
The approved concept-design defined a goal layer above the native workflows — a grounded question, one revisable strategy, one bounded task at a time, a round ending in a mandatory result and a review by a fresh agent. None of it existed on disk: seven approved rulings lived only in shaping files, the repository had no home where an architecture decision belongs, one ruling contradicted live project guidance at `CLAUDE.md:73`, and five textual homes still made the study executor the sole writer of the discovery log. This item wrote the contract down. It created `.project/adr/` and filed the seven decisions with their recorded provenance grades, amended CLAUDE.md's evidence seam, defined the three-file lean artifact contract with its decision/task/round conventions, aligned all five writer-ownership homes on joined `<study-id>#<n>` disposition rows, and wrote the operator runbook that every downstream epic item reads as its input.

### Deliverables
- Workflow record: `20260827_goal-harness-contract/{spec,spec-review,design,design-review,plan,audit,product-lens,align}.md`
- `.project/adr/` — `README.md`, `INDEX.md`, `template.md`, records `001`–`007`, and `.project/scripts/adr.sh`
- `work/orchestration/GOAL_RUNBOOK.md` and the `goal.md` / `trail.md` / `learnings.md` templates
- `.claude/skills/run-goal/SKILL.md` — the fusion-tea-owned goal-agent door
- `CLAUDE.md` evidence-seam amendment; six writer-ownership edits across `.claude/skills/run-study/runbook.md` and `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`
- Contract and documentation tests under `tests/orchestration/`, including the append-as-update guarantee and the register-coherence check

### Notes
- Audited 2026-08-25, verdict **Needs Work** on two prose-sized defects; both fixed the same day (`audit-F1` ADR-005's split grade restored on frontmatter and index; `audit-F2` § What "fresh" means, stating the owner's session boundary and the agent's recorded handoff stop). Product-lens gate CLEAR.
- Amended 2026-08-27 by owner ruling on Item 4's proof-run evidence (`4a8de283`): the grounding gate now refuses on all five field classes, and the discovery-log sentence is scoped to the goal layer's own pen. Both amendments are dated in place with their evidence cited.
- `tests/study tests/orchestration` — 287 passed, 84 skipped, re-run at close.
- The runtime half of the contract is proved by epic Items 4–6, not here; any finding those runs raise against the runbook is an Item 1 defect.

### Lessons Learned
[TODO: Add lessons learned]

## [2026-08-21] - Stellarator Model Migration

**Type**: Item
**Duration**: 1 day

### Summary
Regenerated and sealed the stellarator package at runtime contract 2.0.0 so it executes on stock teax without the frozen-era adapter or injected glue. Preserved numerical identity across the baseline, 948-point radius grid, and 19-point availability sweep; closed the CAS27 verification gap; promoted the MFE sources into the canonical model tree; and made every evidence-producing command fail closed.

### Deliverables
- Archived workflow record: `20260821_stellarator-model-migration/{spec,design,plan,audit,product-lens}.md`
- Sealed stellarator package, stock study route, re-pinned manifest, and `AFTER_MIGRATION_RECORD.md`
- Canonical MFE model sources plus the 506-row `models/stellarator_migration_ledger.md`
- Two-family generation, census, mutation, stock-route, and fail-closed publication regression tests
- Retired primary era adapter and recorded temporary codegen workarounds in the local and upstream backlogs

### Lessons Learned
[TODO: Add lessons learned]

## [2026-08-21] - Bulk Archival: April–August Work Items and Six Epics

**Type**: Housekeeping
**Duration**: 1 session (on `feat/stellarator-model-migration`)

### Summary
Cleared the `.project/active/` backlog of everything finished or dead since the last archival on 2026-04-11: 56 item directories and 6 epic files moved to `completed/` under the `20260821_` prefix, 3 empty untracked directories deleted. Every item was checked against `main` (claimed commits reachable, deliverables present) before moving. Live path references (code, tests, skills, knowledge docs, kept epics) were rewritten to the new locations; historical records (`.project/completed|reports|research`, `work/completed|analysis|orchestration`, `archive/`) were left as written. `BACKLOG.md` and `CURRENT_WORK.md` were purged down to live work. `active/` now holds 5 directories.

### Epics Archived
- **Knowledge Database Integration** — Complete (Items 1–3, 5; Item 4 abandoned, superseded by IFE source ingestion).
- **Concept Analysis v2** — Complete (Item 2 visuals superseded by the concept explorer). Never had a BACKLOG row.
- **Explorer UX v2** — Complete (all 5 items, 2026-04-06). Never had a BACKLOG row.
- **Source Extraction Fix & Re-extraction** — Abandoned. Never decomposed; the cleanup goals were delivered by `source-replacement` + `orig-md-research`. The original table-quality complaint (`11-magnetic-mirror` arXiv 2411.06644 Table 3) was never addressed.
- **Ontology v3 Migration** — Complete (Items 1–4 merged via PRs #15/#16/#19/#20; Item 5 superseded by the rework's full regeneration; Item 6 discharged here).
- **Concept-Analysis Pipeline Rework** — Complete in substance (PR #44, regen PRs #46/#48; Items 2–3 superseded by the prototype; Item 12 aspirational). **Open**: Item 5's per-row verification gate on `design_point.csv` was never signed (`verified_by` blank on 33/33 rows) — recorded as a BACKLOG Flagged row for the owner.

### Items Archived — complete (52)
- Analysis pipeline, April: `cleanup-feedback-flag` (2055cdb3), `costingfe-scaled-overrides` (PR #9), `feedback-dispatch-symmetry` (150d5721), `manifest-elimination` (bdc55c59), `model-feedback-starvation` (PR #8), `parameter-metadata-generation` (6345555), `power-standardization` (PR #6; α=0.6 approach later replaced by scaled overrides), `staleness-propagation-fix` (PR #10), `template-nesting-bug` (PR #8), `concept-capex-ranked-bars` (87d540d4).
- Down-select and scoring, May: `concept-downselect-merge` (PR #17), `concept-research-17-split` (PR #18), `scoring-v3-rewrite` (PRs #19–#26, #28/#29), `scoring-v2-component-modularity-slice` and `scoring-v2-modularity-slice` (shipped, then replaced by v3 P2), `gap-check-source-index` (PR #32).
- Concept-analysis rework, May–June: `concept-rework-prototype`, `costingfe-library-preconditions`, `concept-rework-tables` (Phases A–D; E/F gate unsigned), `concept-rework-pipeline-glue`, `concept-rework-helpers-validators`, `concept-rework-three-forward-contract`, `concept-rework-prompt-templates`, `concept-rework-model-critic` (Phase 5 archived-concept simulation never run; tool is in production use), `concept-rework-explorer-pilot` (Phases 1–2; 3–5 overtaken by the June bulk regen), `concept-rework-bulk-regeneration`, `prompt-updates-for-1gw-estimate-policy` (860adf93), `concept-explorer-omit-list` (4b098c9e).
- Ontology v3: `ontology-v3-merge`, `ontology-v3-close-gaps`, `ontology-v3-design-decisions` (PR #16).
- Explorer, June: `explorer-rework-unblock` (PR #49), `explorer-extractor-resilience` (PR #50), `explorer-slider-override-semantics` and `explorer-override-inspection` (PR #52), `explorer-identity-spine` (PR #58), `explorer-ontology-matrix` (PR #59), `explorer-cost-landscape` (PR #64), `explorer-model-setup-path-normalization` (PR #82), `explorer-web-hosting` (PR #97; operator runbook now at `20260821_explorer-web-hosting/RUNBOOK.md`), `compute-oom-debounce-and-quantize` (PR #98), `portfolio-audit-stage` (PR #63), `model-setup-feedback-timeout` (ticket, resolved 70b6fbe1).
- Stellarator demo and run-study, July–August: `aries-cs-holdout` (barred/admissible lists — pointer updated in `knowledge/holdout/aries-cs/PROTOCOL.md`), `demo-anchor-acceptance-spec` (ratified bars, still govern demo Item 7), `demo-proof-of-life`, `run-study-reachability-spike`, `run-study-contract`, `run-study-indicators`, `run-study-quality-tools`, `run-study-cold-pickup`, `stellarator-demo-landing` (PR #104).

### Items Archived — abandoned or superseded (4)
- `batch-pipeline-run` — plan never started; every step calls `stage1-all`, deleted 2026-04-13, and all 41 concepts have since been regenerated.
- `costingfe-two-knob-projection` — draft spec re-specced the next day as `costingfe-library-preconditions`.
- `eta_th-double-count-fix` — implemented on `fix/eta-th-double-count`, PR #31 closed unmerged ("Fixed in 1costingFE yamls instead"); remote branch deletable.
- `explorer-rework-enrich` — never started; the surviving ideas live in Explorer UX v3 (D2/D3/C2).

### Deleted (empty, untracked)
- `1gw-override-cohort-rerun/`, `relative-override-semantics-prompt-fix/`, `server-recompute-param-drops/`.

### BACKLOG.md rows dropped (verified done or moot on `main`)
- Refresh synthesis.md for 13 concepts — done (8598403c).
- Concept 20a capital-side coupling and concept 09 dual-site availability — both `model_setup.py` files were regenerated under the three-forward contract; the suspected overrides no longer exist.
- Non-D-T availability policy and the DEFAULT-label audit script — the rework moved availability and defaults into the 1costingfe library (`lib/model_setup_helpers.py:61`, `validate_model_setup_contract`); `canonical_availability` survives only for `standardize_availability.py`.
- Refresh deployed Score Explorer after PR #33 — done (`docs/` mirrors `tools/score_explorer/` byte-for-byte).
- Ideas "MFE concept modeling" and "Cross-concept comparison tooling" — delivered by the stellarator demo and the explorer.

### Remaining Active
- `stellarator-model-migration` — live; needs work after the 2026-08-21 audit.
- `run-analysis-cli-step-semantics` — paused spec, real bug.
- `traceability-system`, `loop-dry-run-symmetry` — paused; gaps still open.
- `demo-study-parameterization-policy` — the run-study skill's rulebook, stays until RUN-STUDY Item 6.

---

## [2026-04-11] - Pipeline Hardening, Explorer Merge, Source Cleanup

**Type**: Feature + robustness (8 work items + 2 deletions)
**Duration**: ~1 week on `design-space-explore`

### Summary
Pipeline-hardening closed a class of silent-corruption and transient-error failures that had been killing `stage1-all --all` runs and required manual re-runs. In parallel, output validation, feedback routing, concept-landscape context, and .orig.md re-sourcing landed as independent correctness fixes. The concept explorer (from `ralph/concept-explorer`) was merged into the analysis pipeline branch, and Phase 1a source replacement was closed out. The combined effect: `batch-pipeline-run` can now safely proceed against all concepts.

### Items Archived
- `pipeline-hardening` — Validated invocation, transient-error retry, state integrity across `loop.py`/`run_analysis.py`/`research.py`. Deleted legacy `step_runner` surface. 7 phases, audit passed clean. Commit 9d9605a.
- `output-validation-retry` — `invoke_claude_validated()` wrapper with regex-based verdict/section validators; retry-via-resume on malformed output. Commit 46afb62.
- `concept-landscape-context` — Injected cross-concept catalog into analysis prompts so agents can name verifiable nearest neighbors; simplified vestigial status codes (`D`/`M` → `iterating`). Commits 244e160, 0ab9dc0.
- `orig-md-research` — Re-sourced 21 NO-verdict `.orig.md` Haiku-paraphrased files against real HTML sources and deleted originals. Commit a8c489a.
- `feedback-routing-fix` — Added finding categories so assessment findings targeting model code reach `model_setup.py` directly instead of being laundered through analysis prose. Commit 73f6994.
- `explorer-merge` — Merged `ralph/concept-explorer` (FastAPI 4-page explorer, 140+ tests) into `design-space-explore`. Commit d8cb8ce and follow-ups.
- `source-replacement` — Phase 1a source replacement effort, coupled with `orig-md-research`. Triage report, plan, and plan-completion preserved for reference.
- `common-output-interface` — Picked up a lingering prior-session archival (staged rename to `completed/20260407_common-output-interface/` that was never committed). Plan marked Complete as of 2026-04-07.

### Deleted (not archived)
- `extraction-interface-gap/` — Empty orphan directory, never committed.
- `step-runner-validation-retry/` — Untracked spec only. Superseded by pipeline-hardening Phase 5, which explicitly deleted the legacy `step_runner` surface the spec targeted.

### Remaining Active
- `batch-pipeline-run` — Not started; unblocked now that pipeline is hardened
- `loop-dry-run-symmetry` — Small follow-up from pipeline-hardening audit (spec only)
- `traceability-system` — Still on hold awaiting prioritization

---

## [2026-04-05] - Analysis Pipeline Bulk Archival

**Type**: Housekeeping
**Duration**: 1 session

### Summary
Archived 13 completed work items from the analysis pipeline development phase. The pipeline (`run_analysis.py` + `lib/` modules) is fully operational with iterative analysis, autonomous source acquisition, cross-concept memory, PROCEED/REVISE review verdicts, and concept management tooling.

### Items Archived
- `automated-concept-analysis` — Core analysis pipeline with gap-check/analyze/approve workflows and Claude invocation. All 5 phases complete.
- `autonomous-source-acquisition` — WebSearch/WebFetch research step for automated data gap resolution. Live-tested.
- `checkpoint-test-concept17` — End-to-end validation on concept 17a with replaced sources. 6/8 spot checks passed.
- `concept-research-skill` — Consolidated research docs into README.md + `concept-research-navigation` skill.
- `constraint-atms-spike` — ATMS constraint propagation prototype for design space exploration.
- `iterative-analysis-loop` — Multi-pass analysis with config extraction, modal prompts, and convergence tracking.
- `manage-concept-agent` — Interactive `/manage-concept` command for concept vetting and comparison.
- `refactor-final-stages` — Rescoped review/synthesize/approve to PROCEED/REVISE verdicts with kick-back.
- `refactor-run-analysis` — Extracted `run_analysis.py` (2306→1380 lines) into 9 `lib/` modules.
- `refactor-stage1-loop` — `iter-N/` directory layout, `--resume` support, verdict.json tracking, migration.
- `research-artifact-sync` — R2 binary sync + migration to `knowledge/concept_research/`.
- `shared-memory-system` — Cross-concept tagged memory (concept/family/universal) loaded into analysis prompts.
- `source-addition` — `add-source` and `update-analysis` commands for incremental source addition.

### Remaining Active
- `orig-md-research` — Re-sourcing NO-verdict `.orig.md` files (3/21 processed)
- `source-replacement` — Coupled to above; extraction complete, cleanup remains
- `traceability-system` — Spec/design/plan written, awaiting prioritization

---

## [2026-03-29] - Concept Taxonomy & Interactive Explorer

**Type**: Feature (4 work items, 2 superseded)
**Duration**: 1 day

### Summary
Built taxonomy visualizer for all 38 fusion concepts: Pydantic data models, pairwise similarity engine (4-dimension decomposition + classical MDS), 7 API endpoints, and interactive frontend with tree view, Plotly constellation scatter, taxonomy cards, and Cytoscape neighborhood graph.

Neighborhood graph went through two failed iterations (procedural add/remove causing re-renders) before landing on a proper model-view architecture (GraphModel built once, GraphView toggles visibility).

### Items Archived
- `concept-taxonomy-and-similarity` — Foundation: data models, similarity engine, API, tree/constellation/cards. Complete.
- `graph-model-rewrite` — Model-view rewrite of neighborhood graph. Complete.
- `taxonomy-viz-redesign` — Intermediate attempt, superseded by graph-model-rewrite.
- `taxonomy-viz-polish` — Intermediate attempt, superseded by graph-model-rewrite.

### Deliverables
- `exploration/concept_explorer/taxonomy_models.py` — Pydantic models with typed enums
- `exploration/concept_explorer/similarity.py` — Pairwise similarity + MDS + diversity-aware bridges
- `exploration/concept_explorer/seed_registry.py` — Canonical JSON registry seeded from table_v2.csv
- Frontend: `taxonomy.js`, `taxonomy_card.js`, `neighborhood_graph.js`, `constellation.js`, `tree_view.js`
- 140+ tests (54 new for taxonomy/similarity)

---

## [2026-03-06] - Project Cleanup & Archival

**Type**: Housekeeping
**Duration**: 1 session

### Summary
Comprehensive review and archival of all active work items and backlog epics. Project infrastructure phase is complete; modeling work continues under the modeling PM system.

### Items Archived
- `extraction-pipeline-integration` — Script modernized for v4 pipeline, 6 sources re-extracted. Infrastructure proven.
- `extraction-validation` — v4 pipeline validated against 6-source corpus. Verdict: proceed.
- `project-reframing` — Massive scope change from CATF-MFE to broad comparative investigation. 8 phases complete.
- `ife-source-ingestion` — 5 IFE sources ingested into knowledge/sources/. SOURCE_INDEX updated.
- `ife-domain-research` — Domain insights produced from IFE literature review.
- `ife-modeling-epic-setup` — *Completed for demo purposes.* Set up IFE Cost Modeling epic (WI-006/007/008) in modeling PM.
- `ife-cost-model-full-workflow` — *Completed for demo purposes.* Meta-orchestrator for IFE modeling workflow demo. All 3 WIs (WI-006/007/008) completed successfully.
- `visualization-demo` — Section 8 of workflow explainer populated with structural view, calc flow, and parameter table.

### Items Abandoned
- `first-corpus-ingestion` — Superseded by `ife-source-ingestion` which ingested 5 IFE-focused sources.

### Epics Archived
- **Visualization POC Sprint** — Complete (all 5 items delivered 2026-01-19)
- **Cost Modeling Patterns De-Risking** — Complete. Learnings from coffee maker and solar+battery models handed off to sysml-codegen; all changes implemented upstream.
- **End-to-End Pipeline De-Risking** — Complete. Solar+battery LCOE pipeline proven end-to-end. Codegen enhancements (Item 6: nested CalcUsage discovery) in open PR.
- **Full Workflow Demo** — Complete. Interactive HTML explainer shipped; IFE modeling demo delivered through modeling PM.

### Remaining Active
- `traceability-system` — Spec + plan written, ready for implementation when prioritized.
- Knowledge DB Integration epic — Kept (infrastructure works, ready to scale).

---

## [2026-01-18] - Visualization POC Sprint (EPIC-001)

**Type**: Epic (5 items)
**Duration**: 2 days (estimated: 5 days)

### Summary
End-to-end proof-of-concept: SysML model → structural extraction → Cytoscape.js interactive web diagram with cost coloring, tree layout, expand/collapse, and PNG export.

### Items Closed
- `golden-reference-cytoscape-poc` — Hand-written JSON + Cytoscape demo de-risking rendering
- `extraction-implementation` — `extract_structural_view()` producing ViewResult data structures
- `end-to-end-pipeline` — `to_cytoscape()`, `to_dot()` converters + CLI entry point
- `visualization-options` — Inside-box labels, tree layout, %-of-parent cost coloring
- `cost-annotations` — Cost attribute extraction + cost-based node styling
- `web-integration` — FastAPI server: model path → extraction → interactive diagram

### Deliverables
- `proof_of_concept/web/` — FastAPI server + Cytoscape frontend
- Extraction pipeline with format converters
- 23+ tests passing

---

## [2026-01-26] - Costed Component Interface

**Type**: Item (Cost Patterns De-Risking epic)
**Duration**: 1 day

### Summary
Production-ready `'Costed Component'` interface with type-safe `CASCategory` enum containing all PyFECONS CAS codes. Foundation for all cost modeling.

### Deliverables
- `models/library/foundation/costing/` — Costed Component interface + CAS enum

---

## [2026-02-01] - Codegen Chain Spike

**Type**: Item (End-to-End Pipeline De-Risking epic)
**Duration**: ~2 days

### Summary
Validated that sysml-codegen handles CalcUsage dependency chains. GO verdict — extraction pipeline's chain binding support works end-to-end. Revisit confirmed 3 runtime gaps fixed upstream.

### Deliverables
- Spike models in `models/tests/codegen_chain_spike/`
- Findings and fix plan documented

---

## [2026-02-09] - Solar+Battery End-to-End Pipeline

**Type**: Epic (6 items, 5 complete, 1 deferred)
**Duration**: ~10 days

### Summary
Full LCOE pipeline proof: SysML model → codegen → calc implementations → ComponentCostEvaluator → LCOE verification. Solar+battery plant model produces $288.68/MWh within 1% tolerance.

### Items Closed
- `solar-battery-sysml-model` — Full SysML model (3 hierarchy levels, 9 leaf parts, 15 calc defs)
- `solar-battery-cost-evaluation` — Cost evaluation script + JSON entry points, all 10 tests passing
- `hybrid-pipeline-e2e` — Complete pipeline: codegen → calcs → evaluator → LCOE verified
- `gap1-default-value-debug` — Root cause: path filter mismatch. Fix plan for upstream repos.

### Deferred
- Item 6 (Codegen nested CalcUsage discovery) — upstream enhancement, not blocking

### Deliverables
- `models/tests/solar_battery/` — Complete SysML model + expected outputs
- Pipeline YAML, registry, integration tests
- 28 pipeline tests + 10 regression tests passing

---

## [2026-02-09] - Knowledge Database Integration (KNOW-DB Items 1-3)

**Type**: Epic (partial — Items 1-3 of 5)
**Duration**: ~3 days

### Summary
Built git-authoritative Zotero ingestion pipeline: API de-risk → single-source E2E → batch automation → manifest-based diffing. 6 fusion sources ingested.

### Items Closed
- `knowledge-database-integration` — Items 1-2: Zotero API de-risk + single-source pipeline
- `zotero-ingestion-script` — Item 3: Batch ingestion with --dry-run, --local-pdf
- `ingestion-workflow-v2` — Manifest diffing replaces tag-based queue

### Deliverables
- `scripts/zotero_ingest.py` — Batch ingestion automation
- `scripts/zotero_lib.py` — Shared Zotero API helpers
- `knowledge/MANIFEST.jsonl` — Git-side source tracking
- 6 sources in `knowledge/sources/`

---

## [2026-01-12] - Cost Evaluation Script (Archived)

**Type**: Item (Cost Patterns De-Risking epic)
**Status**: Never started — superseded by `solar-battery-cost-evaluation`

### Summary
Spec and design drafted for coffee maker cost evaluation script. Work was superseded when the solar+battery model became the primary evaluation target.

---
