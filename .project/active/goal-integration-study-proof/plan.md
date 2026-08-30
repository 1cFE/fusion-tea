# Implementation Plan: GSTH Item 6 — Integration-to-Study Closure and Route Equivalence

**Status:** Draft
**Created:** 2026-08-29
**Last Updated:** 2026-08-29
**Branch:** `feat/wi033-p-pump-rebase` (owner-ruled: one PR ships WI-033 + Item 6)

## Source Documents

- **Spec (Align deltas):** `.project/active/goal-integration-study-proof/spec.md`
- **Governing spec:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 6 — Scope 1–5, Success Criteria 1–7, Out of Scope
- **No `design.md`** — owner-ruled lean shape (spec § Align ruling 6). The one real design question, route-equivalence isolation, is **Phase 6 § Isolation design** below.
- **The loop this round follows:** `work/orchestration/GOAL_RUNBOOK.md`
- **Why the layer is shaped this way:** `.project/adr/001`–`007`; the integrate seam's own decision is `.project/adr/009-integration-is-a-fixed-point-proof.md`
- **Seam operator guides:** `docs/integration_seam_operator_guide.md`, `.claude/skills/run-study/SKILL.md` + `runbook.md`, `modeling_project/STUDY_POLICY.md`

## The Point

A discovery row has been open since 2026-08-22: `p_pump` = 1.0 MW is ~130–195× below what helium-primary circulator evidence supports (`20260821-power-cycle-ab#3`). Goal `p-pump-basis` answered the *basis* question — 6 % of thermal power, ≈195 MW at the baseline geometry — and the owner ruled the value in. WI-033 landed it in the model. But the row's own last sentence is still open: **"where the `recirc_ok` fence moves and what LCOE does still need a package run."** No study has run against a package carrying 195 MW, because no package carries it: the model says 195.0 and every committed package says 1.0.

That gap is not an accident, and closing it is what this item is for. The `integrate` seam exists precisely to answer "is there one study-ready candidate for this audited model change?" It has never been run live by a goal round. So this item does two jobs at once:

1. **Answer the domain question.** Regenerate the package on the audited model, get one verified pin, run one bounded study against that exact pin, read it from the record alone, and close the round on whatever the reading says.
2. **Prove the harness.** This is the first end-to-end trip through `integrate → study.execute → study.read → dispositions → fresh review`, and the first time the goal layer's two operating routes — a hand operator following the runbook, and a goal agent — are checked against the same contract.

If a tired engineer reads one paragraph of this file, it is the previous two. Everything below is sequencing.

## Implementation Strategy

**Phasing rationale.** The riskiest thing here is not the study; it is whether the package can be brought to a state the seam will call a `CANDIDATE` at all. Phase 1 does that first and does it in the honest order: run the seam on the tree as it stands, get its designed refusal on the record, discharge the refusal, re-run, and only then move. Everything downstream — study, reading, findings, close, runbook flip, route comparison — is worthless if Phase 1 returns a blocker, and Phase 1 finishing tells us within one session whether the item is deliverable.

**Critical path.**

```
P0 ground goal + open round  →  P1 BLOCKER → regenerate/commit → CANDIDATE + battery green
                             →  P2 one committed study at that pin
                             →  P3 fresh administrator reading
                             →  P4 dispositions, learning, fresh RoundReview, round closes
                             →  P5 runbook integrate row flip   →  P6 route equivalence
                             →  P7 epic evidence + regressions  →  P8 verification record
```

P5–P7 have no ordering dependency on each other beyond P5 needing the seam to have run live and P6 needing the round's kept evidence, so they may be interleaved if a session boundary makes that convenient.

**First proof point.** Phase 1's second seam invocation returning `class: "CANDIDATE"` with exit 0. Until that JSON exists, nothing else in the item can start.

**Overall validation approach.** Each phase names its own check and its commit point. Full regressions run once, at Phase 7. `uv run` for everything Python; validation via `uv run agentic-mbse validate models/`, never bare `syside check`.

### Two standing constraints on every phase

- **Cite, don't mirror.** Goal artifacts (`goal.md`, `trail.md`, `learnings.md`) cite native state by `<path>@<sha>` and say what it *meant*; they never restate a work item's status, a study's numbers, or a spec's requirements (GOAL_RUNBOOK § What this is; ADR-006).
- **The regeneration fence is inverted now.** WI-033 deferred package regeneration to this item, so Item 6 **is** the authorized regeneration. Committed prior study records stay reproducible at their own pins — **do not touch any directory under `exploration/stellarator_e2e/studies/2026*`**. Their pins will no longer match the live package after Phase 1; that is expected, and each record carries its own snapshot and fingerprints.

### Decisions made here, recorded loudly

Spec § Align ruling 4 makes everything outside the four reserved gates execution detail, decided and recorded. Three decisions:

**D1 — The regeneration is performed under this coding-PM item; no new modeling work item is minted.**
ADR-009 says a regeneration-gate refusal is "the modeling item's unfinished work." WI-033 is closed and archived, and the owner's routing ruling (spec § Align ruling 2) put the regeneration on this branch under Item 6. Reopening WI-033 or minting a WI-034 to hold four mechanical commands would add a PM lifecycle to a step the owner already assigned here. *Alternative rejected:* mint a modeling work item for the regeneration — correct by the letter of ADR-009's "referent item" sentence, but the referent item is closed by owner ruling and this item is its owner-named successor.

**D2 — "Regenerates and commits the package through the seam" is read as: regenerate natively, commit, then the seam proves it.**
Spec § Align ruling 2's phrasing, read literally, would have the seam perform and commit. ADR-009 bars both (`spec.md` R-F1, R-C6), and changing it needs an owner ruling. The reading above is the only one consistent with the seam as built and delivers exactly the owner's stated outcome — a regenerated, committed package with a verified pin. Surfaced here rather than resolved silently (capture-fidelity law 4). If the owner meant the other thing, that is a seam contract change and a new item.

**D3 — Inside the round, the plan names only the first task.**
GOAL_RUNBOOK § Opening a round and ADR-001 bar a forward task list in a strategy: "if you can predict all the tasks, the strategy is a plan." This plan sequences *the item's* obligations, not the round's task list. It names `T-001` and the obligations each subsequent step owes; which tasks follow is chosen by the round agent from the evidence in hand. Where a phase below says "the round then owes X," that is an obligation, not a pre-authorized task.

---

## Phase 0: Ground the successor goal and open round 1

### Goal
A grounded successor goal on the open tail of `20260821-power-cycle-ab#3`, round 1 open with one strategy revision, and `T-001`'s scope written before any work.

### Assumption Under Test
That the open tail is a groundable question — that `goal.md` can be filled in all five field classes without hollow fields, and that the grounding evidence in the repository does not already answer it.

### Reserved gate — owner wording
`§ Question` and `§ Answered when` are **the owner's own sentences** `[OWNER 2026-08-29]`, collected before the round opens. The orchestrator carries them in. **Do not draft them and do not paraphrase.** If they have not arrived, this phase stops and nothing downstream starts.

### Verification Stencil (satisfy this before opening the round)
```
Read work/orchestration/goals/<new-slug>/goal.md and check five field classes:
  grounding evidence  — non-empty, paths resolve, Status is not `draft`
  answer contract     — § Answered when, owner's words, two readers would agree
  invariants          — what a comparison must preserve
  limits              — retry cap, checkpoint cap, round limit, restated explicitly
  reserved gates      — the four from spec § Align ruling 4
Any hollow class → refuse to open the round and name the class (GOAL_RUNBOOK § Grounding a goal).
```

### Changes Required
- [x] Create `work/orchestration/goals/<new-slug>/` from `work/orchestration/goal-templates/` (`goal.md`, `trail.md`, `learnings.md`). The headings are the contract; copy, do not invent.
- [x] `goal.md`: owner's § Question and § Answered when verbatim. Grounding evidence cites `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` row `#3` (2026-08-28 disposition), `work/orchestration/goals/p-pump-basis/` (closed; its § "Constraints carried into round 2" informs the invariants), `work/completed/20260828_WI-033_p-pump-rebase/verification_record.md@83ccd8f9`. Limits restated explicitly, never inherited silently.
- [x] `goal.md` § Reserved gates: the four from spec § Align ruling 4, plus the study layer's own § 4 axis ruling (below).
- [x] `trail.md`: `## Round 1 — <strategy-slug>` + `### Strategy revision — 2026-08-29`. Carries approach, assumptions, abandon conditions, the intended model increment, the intended study question. **No future task list.**
- [x] `trail.md`: `### T-001 scope` — six lines, before any work. Objective: is there one study-ready candidate for the stellarator package on WI-033's audited model change?

### Validation
- [x] Five-class grounding check above passes; record it in the trail.
- [x] `p-pump-basis` untouched — `git diff --stat` shows zero lines under `work/orchestration/goals/p-pump-basis/`.
- [x] Round-open test: the `## Round 1` section carries a `### Strategy revision` and no `### Round 1 result`.

**Commit point (orchestrator):** `goal(<slug>): ground successor goal, open round 1, T-001 scope`

**What We Know Works After This Phase:** the goal authorizes tasks; the round is open; the first task's scope is on the record before its first side effect.

---

## Phase 1: Integrate — blocker, discharge, candidate

### Goal
Exactly one `CANDIDATE` pin and both fingerprints for the stellarator package on WI-033's model, with the seam's refusal branch demonstrated live on the way there, and the pre_pr's 21 designed battery reds green.

### Assumption Under Test
That the seam's refusal is exactly what ADR-009 designed (`package-not-integrated` at gate 2) and nothing else is stale — and that a native regenerate/recapture/re-pin makes the package a fixed point of the whole ten-gate sequence.

### Test Stencil (the seam is the test; run it first, unchanged)
```bash
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env \
  python scripts/integrate.py \
    --audited-work work/completed/20260828_WI-033_p-pump-rebase@83ccd8f9 \
    --models-root  exploration/stellarator_e2e/models \
    --package      exploration/stellarator_e2e/pkg/stellarator_tea \
    --manifest     exploration/stellarator_e2e/studies/manifest.json \
    --groups       tests/study/data/axes.known_answers.json \
    --census-file  tests/models/data/mfe_census.json \
    --expected-semantic-fingerprint   <contracts/model_contract.json semantic_fingerprint> \
    --expected-executable-fingerprint <contracts/package_contract.json executable_fingerprint> \
    --expected-teax-revision          $(git -C "$STOP_PARSER_TEAX_ROOT" rev-parse HEAD) \
    --route-sys-path exploration/stellarator_e2e/studies \
    --route-module study_route --route-callable execute_baseline \
    --out-dir /tmp/integration-run-1
# Expect exit 1, BLOCKER, blocker.condition == "package-not-integrated" (gate 2, regeneration).
# Exit 2 is a seam defect, NOT a result about the package — read seam_traceback.txt and stop.
```
Full invocation, every flag's provenance, and the blocker-condition table: `docs/integration_seam_operator_guide.md`. All six `STOP_PARSER_*` variables must be exported or the sweep at gate 0 refuses before any producer runs.

### Changes Required

**1a — Run the seam on the tree as it stands.**
- [x] Invoke as above; keep `integration_return.json` as evidence.
- [x] Confirm the blocker is gate 2 `package-not-integrated` naming `sysml-codegen generate` and no earlier gate. An earlier-gate blocker means something *other* than the known divergence is stale — stop, name it, and treat it as a new finding.
- [x] `trail.md`: `### T-001 return` = `PREREQUISITE`, naming the seam's blocker condition, with the five decision fields. Per ADR-009 § Consequences a regeneration-gate refusal is a prerequisite, **not** a strategy blocker. Then `### T-002 scope` for the discharge (D3: this is the task the evidence chose, written after the return).

**1b — Discharge the prerequisite: regenerate, recapture, re-pin, commit.**
- [x] Regenerate in place, per `exploration/stellarator_e2e/studies/AFTER_MIGRATION_RECORD.md` § 1 and the flags gate 2 uses:
      `uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten`
- [x] Recapture `exploration/stellarator_e2e/stellarator.snapshot.json` (`capture_instance_graph_snapshot`, as `scripts/integrate.py:1070` invokes it).
- [x] Re-pin `exploration/stellarator_e2e/studies/manifest.json` — `fingerprints.recorded_provenance.{semantic,executable}_fingerprint` and `fingerprints.indicator_inputs.digest`.
- [x] Confirm the two handwritten implementations survive byte-identical (`dt_fusion_power_impl.py`, `levelized_replacement_cost_impl.py`); `--preserve-handwritten` is what gate 3 checks.
- [x] **Re-derive, never patch, the six known-answer fixtures** — `tests/study/data/{availability,interest_rate,R,R+tie,a,B}.expected.json` and `EXPECTED_SEMANTIC_FINGERPRINT` in `tests/study/test_known_answers.py:20`. That file's own docstring states the rule: derived from the new package, never edited to match. `test_fixture_binding` fails first and says so. **This is the regression the pre_pr gate could not see** — the 21 reds were the integrate suite against a stale package; re-deriving the package moves the known-answer values too, because `p_pump` feeds `rec_frac` → `p_net` → LCOE.
- [x] Check `tests/models/data/mfe_census.json` — WI-033 already re-derived it at `18a5ce86`; confirm it still matches, do not re-derive twice.
- [x] Commit the regenerated package, snapshot, manifest and re-derived fixtures together.

**1c — Re-run the seam.**
- [x] Same invocation, fresh `--out-dir`, with the *new* expected fingerprints. Expect exit 0, `class: "CANDIDATE"`.
- [ ] Record the pin and both fingerprints in `trail.md` as `### T-002 return` = `COMPLETE`, citing `integration_return.json`. **Exactly one** candidate — a second promoted pin is out of scope.

**1d — Turn the battery green.**
- [ ] `uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python -m pytest tests/study` — the 13 failures and 8 errors in `tests/study/test_integrate_*` from `.project/reports/2026-08-28-pre-pr-wi033-p-pump-rebase.md` must be green.

### Validation
**Automated:**
- [x] `integration_return.json` from 1a: exit 1, gate 2. From 1c: exit 0, `CANDIDATE`.
- [x] `uv run agentic-mbse validate models/` → L1 clean; L2 = the 12 known pre-existing placeholder-binding WARNs, count and locations unchanged.
- [ ] `tests/study` green, including the 21 formerly-red integrate tests and `test_known_answers.py`.

**Manual:**
- [x] `git diff --stat` shows zero lines under `exploration/stellarator_e2e/studies/2026*` — prior committed records untouched.
- [x] The candidate's `pin` is the manifest's own value, not a newly minted number (`tests/study/test_integrate_success.py:68` is the same assertion).

**What We Know Works After This Phase:** the seam runs live, refuses correctly, and returns one verified study-ready identity; the branch's known red set is green.

**Commit points (orchestrator):** (i) regeneration + snapshot + manifest + re-derived fixtures; (ii) the trail entries and the kept seam returns.

---

## Phase 2: Execute one bounded study against that exact pin

### Goal
One committed study record, run against the Phase 1 candidate contract and nothing else, answering the open tail: where the `recirc_ok` fence moves and what LCOE does at `p_pump` = 195 MW.

### Assumption Under Test
That the axes that move the fence still resist at the new pin, and that a bounded study can say where the fence went relative to `20260821-power-cycle-ab`'s answer.

### Owner touchpoint (native study gate, not a new reserved gate)
`runbook.md` step 4 requires the **user's ruling on the framing before any point runs**, and `SKILL.md` § Three roles makes the user the one who rules on any axis the model turns out not to resist. Sequence it: indicators (step 3) run, framing argued (step 4), owner rules, *then* points run. An unruled framing stops the phase.

### Test Stencil (the runbook's own gates are the test)
```
step 2  declare each candidate axis as a qualified entry-key group
step 3  run indicators for every proposed axis, including declined ones
step 4  argue the framing → OWNER RULING → only then
step 6  preflight gates, 6 of 6
step 9  every point through the stock teax lifecycle
step 10 verify a sample against the package-owned oracle
```
Re-run the gates after any declaration change — `20260823-magnet-technology-ab#10` is the row that bought that rule.

### Changes Required
- [ ] `trail.md`: `### T-00N scope` and `### T-00N start` before the first side effect.
- [ ] Invoke `/run-study` in **execute** mode. Mint the study id per `runbook.md § Naming`; record path `exploration/stellarator_e2e/studies/<study-id>/`.
- [ ] The store goes **beside** the record directory, not inside it (`20260821-power-cycle-ab#11`). The baseline executor's work directory likewise (`20260823-magnet-technology-ab#9`).
- [ ] `points.csv` carries `case_id` (`20260823-magnet-technology-ab#6`).
- [ ] Emit the unrecorded predicate operands (`rec_frac`, `p_net`) as a labelled `results/` artifact before verification (`20260821-power-cycle-ab#10`) — the fence question is exactly the one this artifact answers.
- [ ] A headline landing within one grid step of the fence is re-evaluated across the sourced range of every held value it depends on, and the margin stated (`20260823-magnet-technology-ab#11`).
- [ ] Executor registers findings and appends **first-sighting** discovery-log rows (runbook step 14). The round appends disposition rows later, in Phase 4.

### Validation
- [ ] Preflight 6/6; step 10 oracle sample verification passes.
- [ ] The record's `snapshot.json` names the Phase 1 pin and both fingerprints — the same contract the candidate named. Any mismatch is a stop, not a note.
- [ ] Record passes `uv run python -m pytest tests/study/test_records.py` (including `test_findings_join_the_discovery_log`).
- [ ] Exactly one committed study this round.

**What We Know Works After This Phase:** a study ran against the exact candidate contract and its record is committed and independently readable.

**Commit point (orchestrator):** the record directory + discovery-log sighting rows + trail entries.

---

## Phase 3: Administer — a fresh session reads the record and nothing else

### Goal
`synthesis.md` and findings produced by a session that did not execute the study, reading only the committed record directory.

### Assumption Under Test
That the record is self-sufficient: a reader with no memory of the run can recover what was asked, what was assumed, what came out, and what none of it supports.

### Fresh is a session boundary, not a work boundary
GOAL_RUNBOOK § What "fresh" means, quoting the owner: *the critic is never the author's session.* An agent cannot start a session. If the fresh session is not available, write the handoff stop (`### Stop`, kind `handoff`) and **stop** — do not administer your own execution.

### Verification Stencil
```
The administrator reads ONLY exploration/stellarator_e2e/studies/<study-id>/.
A fact not in the record is reported as MISSING, never recovered from elsewhere.
The administrator writes synthesis.md and appends NO discovery-log rows.
```

### Changes Required
- [ ] Fresh session, `/run-study` **administer** mode, record path given, confirmed to be a record directory before being read as one.
- [ ] `synthesis.md` in the record directory.
- [ ] `trail.md`: the reading's `### T-00N return` with its outcome class and the goal-level reading of the evidence. **An adverse or inconclusive reading is a real result** — it closes the round and is not repaired inside it (epic Scope 2; spec § Align ruling 4).

### Validation
- [ ] The administrator's session is demonstrably not the executor's — say which session did what, in the trail.
- [ ] `synthesis.md` cites nothing outside the record directory.
- [ ] No discovery-log row was written by the administrator.

**What We Know Works After This Phase:** the record/synthesis seam holds across a real session boundary.

**Commit point (orchestrator):** `synthesis.md` + trail return.

---

## Phase 4: Close the round — dispositions, checkpoint, learning, fresh review

### Goal
Every touched or new discovery row carries a joined disposition; the learning delta is proposed and accepted; a fresh `RoundReview` verdict is on the record; the round closes on the reading whatever it says.

### Assumption Under Test
That the disposition rules survive a round whose evidence touches a row (`#3`) that a previous goal already marked "final for goal `p-pump-basis`" — the row is final *for that goal*, and this round's evidence is new.

### Two distinct checks — do not merge them
| | Pre-execution checkpoint | Round review |
|---|---|---|
| When | After the reading proposes dispositions, **before any semantic follow-up executes** | After the round result is written |
| Reviewer | Fresh non-author, lightweight | Fresh non-author, thorough |
| On failure | Author revises, up to **2 revisions**; then `### Stop` kind `cap` — the cap **stops** work, it never releases it (ADR-005) | `FINDINGS` or `OWNER_GATE`; the round stays closed |

If no semantic follow-up task is proposed, say so explicitly in the trail rather than skipping the checkpoint silently.

### Changes Required
- [ ] `### Checkpoint C-00N.rK` for each submission — never amend a prior `rK`.
- [ ] Append disposition rows to `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` under **existing** ids only. **Never mint an id** — a row under an unknown id breaks the join and fails `test_findings_join_the_discovery_log`. Read the newest matching row for an id, not the first (the first is the sighting).
- [ ] Every touched/new row gets `model fix | research | declared seam | upstream filing` + status + responsible task/owner + what changed or the concrete next reference. **No touched row returns `unrouted`** (ADR-004).
- [ ] `### Round 1 result — YYYY-MM-DD`: intent met/unmet, task sequence, last semantic outcome, **derived** stop reason, evidence refs, proposed learning delta, finding dispositions.
- [ ] Fresh session writes `### Round 1 review` — verdict `PASS | FINDINGS | OWNER_GATE`, over: native evidence by citation, goal/strategy fidelity, every recorded task scope, retry classification, every touched discovery row, external mutation of cited artifacts, the learning delta, constraints carried forward.
- [ ] Accepted learning delta appended to `learnings.md` — there and nowhere else.

### Validation
- [ ] Walk every cited ref: it resolves and says what the trail claims (§ When a cited artifact moves). Any ref that moved outside its task → `### Stop`, kind `external mutation`.
- [ ] `uv run python -m pytest tests/study/test_records.py` still green after the log append.
- [ ] Round is closed: `## Round 1` carries a `### Round 1 result`.
- [ ] Goal close itself is **owner-held** — the review recommends; it does not close. Ditto any ruling an adverse reading requests.

**What We Know Works After This Phase:** the round semantics, disposition join, and review topology hold on a live round with a real study behind them.

**Commit point (orchestrator):** trail result + review, `learnings.md`, discovery-log disposition rows.

---

## Phase 5: Flip the runbook's `integrate` row — after the seam ran live, not before

### Goal
`work/orchestration/GOAL_RUNBOOK.md` § The native seams describes the repaired `integrate` seam, with the `research` row byte-untouched.

### Assumption Under Test
That the flip rests on live evidence. Phase 1 supplies it: a real `BLOCKER` and a real `CANDIDATE` from `scripts/integrate.py` on this branch. **Do not run this phase before Phase 1c returns a candidate.**

### The recipe
Mirror `git show 9f0019e8` (C-FLIP, the `research` row flip) exactly in shape. Four edits, no more:
1. The `integrate` row loses `— **pending native repair**` and gains the native return classes.
2. `GOAL_RUNBOOK.md:262` — "One seam — `integrate` — is not repaired yet…" goes; the paragraph's whole premise is now false.
3. `GOAL_RUNBOOK.md:265` — the `integrate` bullet's "no native tracked procedure … no written pattern to follow" becomes the seam pointers: `scripts/integrate.py`, ADR-009, `docs/integration_seam_operator_guide.md`.
4. `:267` — the "may not silently absorb" closing paragraph, now that neither seam is pending.

### Changes Required
- [ ] Edit the four locations above.
- [ ] Assert the `research` row and its bullet are **byte-untouched** — the mirror of WI-033's R-G1 guard. Verify with a targeted diff, not by eye.
- [ ] `.project/adr/` needs no new record; ADR-009 already decides the seam.

### Validation
- [ ] `git show <flip-sha> -- work/orchestration/GOAL_RUNBOOK.md` shows only the four edits.
- [ ] `uv run python -m pytest tests/orchestration` green.
- [ ] Grep confirms no `pending native repair` string remains in the file.

**What We Know Works After This Phase:** the runbook's seam table matches the repository, on evidence rather than on intent.

**Commit point (orchestrator):** `flip(GSTH-6): runbook integrate row goes native`

---

## Phase 6: Route equivalence — hand operator vs goal agent

### Goal
`.project/active/goal-integration-study-proof/route_equivalence.md`: the same documented contract exercised through both routes, compared on artifact set, native end states, gates, return classes, and reviewer-visible evidence — with no duplicate external effects.

### Assumption Under Test
That `GOAL_RUNBOOK.md` is genuinely one document for both operators — that a hand operator following it step by step lands the same contract as the agent route did, without the runbook needing agent-specific or human-specific carve-outs.

### Isolation design

This is the item's one real design question (spec § Align ruling 5). The design:

**Where the hand route runs.** A scratch git worktree of this branch at the round's closing commit, created parallel to the repo as `../fusion-tea-route-equiv` (project worktree convention). Every hand-route write — goal files, discovery-log rows, seam out-dirs — lands there. Nothing is committed to `feat/wi033-p-pump-rebase` from it. The worktree is removed after the comparison; `route_equivalence.md` is the only thing that survives, in the main tree.

**What each seam does on the hand route, and why:**

| Seam | Hand route | Why it is safe |
|---|---|---|
| `research` | Not invoked | No research disposition arises; research registration is explicitly out of scope. |
| `model` | Not invoked | WI-033 is closed; both routes cite the same audited item. |
| `integrate` | **Invoked for real**, `--out-dir` outside the package, inside the worktree | ADR-009 § Consequences: "the return is safe to call twice: a re-run on unchanged inputs returns the prior identity or a blocker, never a second conflicting identity." The seam performs nothing and commits nothing. This is **not** a second promoted pin — it is the *same* pin, returned again, and returning the same pin is the point of the comparison. |
| `study.execute` | **Fixture-substituted** — the agent route's committed record stands in | A second execution would be a second committed study (barred), a duplicated multi-hour external effect, and a second store. This substitution is the comparison's **declared limit** and is stated as such in the report. |
| `study.read` | **Run for real** by hand, off that committed record | The seam's own contract is "committed record only," so a hand administrator reading the agent route's record is a faithful exercise, not a shortcut. |

**Why fixture-substituting `study.execute` does not hollow out the check.** What the equivalence is about is whether the two operators reach the same *contract* — same pin, same gates passed, same return classes, same artifacts a reviewer can act on. The sweep's arithmetic is not route-dependent; the runbook obligations around it are, and those (declare axes, run indicators, argue framing, preflight, name the record path) are exercised by hand against the same pin with the points step stopped at the gate. State plainly in the report what was and was not replayed.

### Comparison Stencil
```
For each dimension, record: agent route | hand route | same contract? (textual identity NOT required)

1. Required artifact set   goal.md / trail.md / learnings.md / discovery rows /
                           seam return / study record / synthesis
2. Native end states       package, manifest, model, work items — unchanged by the hand route;
                           no second pin, no second committed record
3. Gates                   grounding five-class check; owner framing ruling;
                           pre-execution checkpoint; fresh RoundReview
4. Return classes          each T-00N outcome; seam CANDIDATE/BLOCKER; the reading's class
5. Reviewer-visible        could a fresh reviewer reach the same verdict from each route's
   evidence                artifacts alone?
```

### Changes Required
- [ ] Create the worktree; confirm it is at the round's closing commit.
- [ ] Hand operator walks `GOAL_RUNBOOK.md` from § Grounding a goal through § The fresh review. Owner supervises at checkpoints (§ Align ruling 5).
- [ ] Write `route_equivalence.md`: the five-dimension table, every divergence with its reason, the declared limit above, and any place the runbook needed an operator-kind carve-out (that would be a finding worth recording).
- [ ] Remove the worktree; confirm the main tree is unchanged by it.

### Validation
- [ ] `git status` and `git log` on the branch show **zero** commits and zero working-tree changes originating in the worktree.
- [ ] `exploration/stellarator_e2e/studies/` in the main tree holds exactly one new record directory (Phase 2's).
- [ ] The hand route's `integration_return.json` names the **same** pin and fingerprints as Phase 1c's.
- [ ] Every divergence in the report has a stated reason; "textual identity is not required" is honored, not used as cover.

**What We Know Works After This Phase:** one runbook, two operators, one contract — or a named place where that is not true.

**Commit point (orchestrator):** `route_equivalence.md`.

---

## Phase 7: Epic evidence and full regressions

### Goal
`.project/active/goal-integration-study-proof/epic_evidence.md` — every epic success criterion mapped to evidence, honest limits included — plus the project-defined regression suite green.

### Assumption Under Test
That the proof chain closes, and that where it does not, the gap is stated rather than papered over.

### The honest limit — state it plainly, do not bury it
Spec success criterion 8, carried from WI-033's verification record § 4 `[OWNER 2026-08-28]`: **the research seam's request/return bookkeeper (`scripts/research_seam.py` open → log → close) has never run end-to-end.** The WI-033 flip evidence covers the seam's *write door* (`scripts/source_registry.py`) only. This round does **not** force a research disposition just to exercise the bookkeeper. Write it as its own line in `epic_evidence.md`, not as a footnote.

### Regression Stencil
```bash
# Canonical battery — both env files
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env \
  python -m pytest tests/models tests/study tests/research tests/orchestration \
                   tests/test_dependency_provenance.py

# Model-family spines, environment exported (the .env does not export SYSIDE_LICENSE_KEY itself)
set -a; source ~/1cfe/agentic-mbse/.env; set +a
uv run python -m pytest tests/models

uv run python -m pytest tests/research
uv run agentic-mbse validate models/
uv run python scripts/source_registry.py verify   # expect 0 faults, 3 known legacy
```
Reference shape: 570 passed / 14 skipped / 0 failed at the 2026-08-28 gate, before the 21 integrate reds appeared. Any red that is not explained is a stop.

### Changes Required
- [ ] Run every command above; quote outputs verbatim in `epic_evidence.md`.
- [ ] Map each of the seven epic § Item 6 success criteria to its evidence path/commit, plus spec criterion 8.
- [ ] Epic Success Criterion 7 — "no hardening-path mechanism is present unless its promoting failure is recorded and owner-visible": walk what this item added and confirm none of it is control-plane machinery (ADR-003). If Phase 6 or the round surfaced a real failure that would justify hardening, record the failure; do not build on it.
- [ ] Record any observed failure worth later hardening, with its evidence.

### Validation
- [ ] Canonical battery exit 0.
- [ ] `tests/models` green with the environment sourced (13 spine tests included).
- [ ] Every epic criterion row cites a path or commit that resolves.

**Commit point (orchestrator):** `epic_evidence.md` + any fixture updates the regressions required.

---

## Phase 8: Verification record and audit prep

### Goal
`.project/active/goal-integration-study-proof/verification_record.md` — the commit chain, each success criterion with its check and result, deviations, and what remains owner-held.

### Changes Required
- [ ] Commit table (commit → SHA → content), in branch order, mirroring WI-033's record shape.
- [ ] Each spec/epic success criterion: the check run and the result, with paths.
- [ ] Deviations, each with the ruling that authorized it — including D1, D2, D3 from § Decisions above.
- [ ] Owner-held remainder, stated as such: goal close ruling; any ruling an adverse reading requested; push, PR, merge; `pm close-item` / archive of native work.
- [ ] Update `.project/CURRENT_WORK.md`.

### Validation
- [ ] Every SHA in the table resolves; ancestry is linear (`git merge-base --is-ancestor` over each predecessor).
- [ ] Every criterion row has a check and a result — no row reads "see above."
- [ ] Fresh-session audit (`/_my_audit`) after the record is written.

**Commit point (orchestrator):** verification record + `CURRENT_WORK.md`.

---

## Environment Setup

See CLAUDE.md and `docs/integration_seam_operator_guide.md § The environment`. Two things bite:

- `~/1cfe/agentic-mbse/.env` **does not export** `SYSIDE_LICENSE_KEY` — use `set -a; source …; set +a` for `tests/models`, or the two `--env-file` flags on `uv run`.
- The three sealed wheels live outside the repository at `/home/reid/1cfe/stop-parser-sealed-wheels/`. A gate-1a hash mismatch is usually a wrong path, not toolchain drift — check with `sha256sum` against `tests/test_dependency_provenance.py::WHEEL_HASHES` before reading it as a real refusal.

---

## Risk Management

| Risk | Phase | Mitigation |
|---|---|---|
| Regeneration is not byte-deterministic, so no `CANDIDATE` ever appears | P1 | Determinism was measured — `.project/completed/20260827_goal-integration-seam/spike_regen_determinism.md`. If it fails anyway, that is a real blocker and the round closes on it; it is not repaired here. |
| The re-derived known-answer fixtures get *patched* to match instead of re-derived | P1b | `test_known_answers.py` docstring states the rule and `test_fixture_binding` fails first. Re-derive from the new package; never hand-edit a value. |
| The seam exits 2 (seam defect) and gets read as a package result | P1 | Exit 2 is explicitly not a judgment. Read `seam_traceback.txt`, stop, and file it. |
| The study's framing is never ruled on and points run anyway | P2 | Runbook step 4 is a hard gate; the owner touchpoint is sequenced before step 9. |
| A fresh session is unavailable at P3 or P4 | P3, P4 | Write the `### Stop` handoff and stop. An agent may not review a round it authored any part of, and the cap never releases work. |
| The hand route duplicates an external effect | P6 | Worktree isolation; `study.execute` fixture-substituted; verified by the zero-commit / one-record checks. |
| An adverse study reading is treated as something to fix | P3, P4 | It closes the round. Follow-up is next round's, and any ruling it requests is owner-held. |
| Goal artifacts drift into mirroring native state | all | Cite `<path>@<sha>` and say what it meant; ADR-006. |

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 0 Completion
**Completed:** 2026-08-29, committed `67c4ff45`.

**Actual Changes:**
- Created `work/orchestration/goals/p-pump-fence/` from `work/orchestration/goal-templates/` — `goal.md`, `trail.md`, `learnings.md`, headings copied not invented.
- `goal.md` grounded: twelve cited artifacts as `<path>@<sha>`, four explicit limits, the four owner Align-ruling reserved gates plus the study layer's framing gate.
- `trail.md`: `## Round 1 — integrate-then-fence`, the grounding check, `### Strategy revision — 2026-08-29` (blocker-first, four assumptions, four abandonment conditions, no model increment, no future task list), `### T-001 scope`.

**Issues:**
- A premise conflict was surfaced rather than resolved: `GOAL_RUNBOOK.md@9f0019e8` § The native seams still marks `integrate` "pending native repair" and says not to improvise a pattern, while the repository now holds `scripts/integrate.py`, ADR-009 and an operator guide. Recorded in the trail's grounding check. Resolved *for this round only* by the owner's routing ruling; the runbook row stays as written until Phase 5 flips it on this round's evidence.

**Deviations:**
- § Question and § Answered when were agent-drafted and adopted verbatim by the owner ("use your drafts"), not owner-originated as the phase's reserved gate anticipated. Graded `[AGENT] (adopted verbatim by owner ruling, 2026-08-29)` in `goal.md` and flagged in the trail as weaker provenance than the predecessor goal's contract. The phase did not stop, because the gate's purpose — that the contract is the owner's and not the agent's to reinterpret — is met by the adoption.

### Phase 1 Completion

### Phase 2 Completion

### Phase 3 Completion

### Phase 4 Completion

### Phase 5 Completion

### Phase 6 Completion

### Phase 7 Completion

### Phase 8 Completion

---

**Status**: Draft → In Progress → Complete
