# Verification Record — GSTH Item 6: Integration-to-Study Closure and Route Equivalence

**Date:** 2026-08-29
**Branch:** `feat/wi033-p-pump-rebase`
**Item directory:** `.project/active/goal-integration-study-proof/`
**Status:** implemented; audit not yet run; push, PR and item close are owner-held.

## 1. Commit chain

43 commits, `45b61e1e` (the spec) through `f0cc7ada` (the Phase-8 brief), in branch order.

**Ancestry verified, not assumed.** `git merge-base --is-ancestor` was run over each of the 42 consecutive pairs and every pair returned ancestor → descendant. `git log --merges` over the same range returns **zero** merge commits. The branch is a linear chain; no commit below is reachable except through the one above it.

| # | Label | SHA | Content |
|---|---|---|---|
| 1 | C-SPEC | `45b61e1e` | Lean shape opened; the six Align rulings recorded; successor goal ruled `[OWNER 2026-08-29]` |
| 2 | C-EPIC | `5e026531` | Epic Item 6 current-state amendment — WI-033 discharges the Item-5-gap lines `[OWNER 2026-08-29]` |
| 3 | C-PLAN | `68ea5f23` | The nine-phase plan; blocker-first integrate; worktree-isolated route equivalence; D1–D3 |
| 4 | C-BRIEF-1 | `4ac33d95` | Round agent launched on P0–P1; grounding wording agent-drafted, adopted verbatim by owner ruling |
| 5 | C-GOAL | `67c4ff45` | Successor goal grounded, round 1 opened, T-001 designed refusal, T-002 opened |
| 6 | C-REGEN | `8099217b` | Package regenerated on WI-033's model; snapshot recaptured; manifest re-pinned; six fixtures re-derived |
| 7 | C-BRIEF-2 | `31a7ec01` | Resumer launched on P1c–P1d — interruption resume from native facts |
| 8 | C-PIN-HL | `cc249b89` | Manifest `baseline.headline.value` re-pinned, 275.264 → 333.067 |
| 9 | C-BRIEF-3 | `b2185b09` | Resume 2 — headline re-pin ruled in scope |
| 10 | C-ORACLE | `2f0f5133` | `p_pump` carried to the independent oracle, 1.0 → 195.0 `[OWNER 2026-08-29]` |
| 11 | C-BRIEF-4 | `71a72dc3` | Resume 3 — oracle carry authorized, T-003 opened |
| 12 | C-TRAIL-1 | `b962ae91` | T-002 returns `PREREQUISITE` across its full arc; T-003 opened; runs 3–5 evidence |
| 13 | C-PIN-EXP | `6e05c12f` | The last two pre-WI-033 expectation sets re-pinned — nine anchors + `PINNED_LCOE` |
| 14 | C-BRIEF-5 | `e3d17387` | Resume 4 — re-pins landed |
| 15 | C-P1 | `02a086b0` | Phase 1 close; battery green at 344 passed; T-003 `COMPLETE`; candidate `20c2c364` pinned |
| 16 | C-BRIEF-6 | `dfb6d314` | Resume 5 — Phase 2 to the framing gate |
| 17 | C-PREP | `8ced8ca5` | T-004 opened; axes declared; indicators run; framing held for the owner |
| 18 | C-ANNEX | `0534c77b` | ANNEX baseline-pin prose re-stated at the live headline |
| 19 | C-BRIEF-7 | `068a9103` | Resume 6 — framing ruled `[OWNER 2026-08-29]`, execute 948 points |
| 20 | C-BRIEF-8 | `98ac72e0` | Resume 7 — evaluability bound ruled per comparand precedent |
| 21 | C-STUDY | `611bc87a` | The study record `20260829-p-pump-fence` — fence located at 195 MW, LCOE +21.0 % |
| 22 | C-BRIEF-9 | `4c962557` | Phase 3 fresh administrator staged |
| 23 | C-SYNTH | `47fb5cb5` | Fresh administrator's synthesis — answered; fence unbounded in R |
| 24 | C-BRIEF-10 | `1f7cbaad` | Resume 8 — Phase 4a reading and proposed dispositions |
| 25 | C-READ | `309519e3` | Reading `ANSWERED`; dispositions and learning delta proposed, held at the checkpoint |
| 26 | C-BRIEF-11 | `a278d7ad` | Phase 4 checkpoint critic staged |
| 27 | C-CHK-1 | `df3d9947` | Checkpoint C-001.r1 `REFUSED` — three blocking findings, four corrections |
| 28 | C-BRIEF-12 | `1150cf12` | Resume 9 — revision r2, addendum-first sequencing |
| 29 | C-ADD | `7cb6a48d` | r2 submission; the record addendum and its three artifacts landed |
| 30 | C-BRIEF-13 | `2a920e99` | Checkpoint r2 verdict requested |
| 31 | C-CHK-2 | `91cdb4ad` | Checkpoint C-001.r2 `PASS` — dispositions released |
| 32 | C-BRIEF-14 | `745bf8b3` | Resume 10 — land dispositions, close round 1 |
| 33 | C-BRIEF-15 | `650a5791` | Fresh `RoundReview` staged |
| 34 | C-ROUND | `e7e9e8ca` | Round 1 result; seven disposition rows landed |
| 35 | C-REVIEW | `4bf5d709` | Round 1 review — `FINDINGS`, answer stands, L-001…L-004 accepted with corrections |
| 36 | C-FLIP | `c4c7d723` | `GOAL_RUNBOOK.md` `integrate` row flipped native |
| 37 | C-BRIEF-16 | `a5e97a09` | Hand-operator route staged — isolated worktree |
| 38 | C-CLOSE | `5d740688` | Goal closed by owner ruling; annex edit ratified; CAS10 guard minted as WI-034 |
| 39 | C-ROUTE | `cb417e5e` | Route equivalence — same contract on five dimensions, identical native identity, F-1…F-4 |
| 40 | C-BRIEF-17 | `24730a95` | Resume 11 — Phase 7 |
| 41 | C-EVID | `58b80929` | Epic evidence — all seven criteria plus criterion 8 mapped, full battery green |
| 42 | C-BRIEF-18 | `0635d53f` | Resume 12 — Phase 8 |
| 43 | C-BRIEF-19 | `f0cc7ada` | Phase 8 brief, second part |

## 2. Spec Align rulings — check and result

| Ruling | Check run | Result |
|---|---|---|
| **1. Ground a new successor goal on `20260821-power-cycle-ab#3`'s open tail; `p-pump-basis` stays closed** | Read `work/orchestration/goals/p-pump-fence/goal.md` § Question and § Grounding evidence; `git diff --stat` over `work/orchestration/goals/p-pump-basis/` across the branch | **Met.** The goal is grounded on that row's open tail and cites it. `p-pump-basis` is byte-unchanged across all 43 commits — zero lines. |
| **2. Item 6 runs on `feat/wi033-p-pump-rebase`; its integrate run regenerates and commits the package; one PR ships WI-033 + Item 6; the 21 designed reds go green before the final gate** | Branch identity; the commit chain in § 1; the Phase-1 battery at `02a086b0` and the Phase-7 battery in `epic_evidence.md` § 1 | **Met, under plan D2's reading.** All 43 commits are on this branch. The package was regenerated and committed (`8099217b`) and the seam proved the fixed point (`evidence/integration-run-5/`). The 21 reds are green: 344 passed at Phase 1, 574 passed / 14 skipped at Phase 7. The PR itself is owner-held (§ 5). |
| **3. Item 6's discharged Current State lines amended by a dated note citing WI-033; original lines kept** | Read `.project/backlog/epic_goal_strategy_task_harness.md` § Item 6 | **Met** at `5e026531`. The **Amendment 2026-08-29** paragraph sits below the original ❌ lines, which are unedited. |
| **4. Four reserved gates: goal grounding wording; goal close ruling; push/PR/merge; any ruling an adverse or inconclusive reading requests** | `goal.md` § Reserved gates; the trail's owner-marked entries | **Met.** Grounding wording: agent-drafted, adopted verbatim by owner ruling ("use your drafts") at `4ac33d95` — a recorded deviation from ruling 1's owner-originated intent (§ 4). Goal closed by owner ruling at `5d740688`. Push/PR/merge not done (§ 5). The fourth gate did not fire — the reading was `ANSWERED`, neither adverse nor inconclusive — and is recorded as not-fired rather than as satisfied. |
| **5. Route-equivalence human route follows `GOAL_RUNBOOK.md` step by step; isolation design is the plan's one real design question** | `.project/active/goal-integration-study-proof/route_equivalence.md` § Isolation design | **Met, with a declared limit.** Hand session `ab39378e` in an isolated worktree detached at `c4c7d723`; zero commits either tree; main tree clean at exit. `study.execute` fixture-substituted — the declared limit (§ 4). |
| **6. Lean shape: spec → plan → implement → audit; no `design.md`; no spec_review or design_review** | Directory listing of the item dir | **Met.** No `design.md` exists; the isolation design lives in `plan.md` § Phase 6. No review artifacts were produced at spec or design stage; the round's own mechanisms carried the criticism (§ 3, criterion 4). |

## 3. Epic § Item 6 success criteria — check and result

| # | Criterion | Check run | Result |
|---|---|---|---|
| 1 | Exactly one study-ready pin and fingerprint; the study executes against that exact contract | Read `work/orchestration/goals/p-pump-fence/evidence/integration-run-5/integration_return.json` for `class`, `exit_code`, gate list and the candidate block; compared its pin and both fingerprints against `exploration/stellarator_e2e/studies/20260829-p-pump-fence/snapshot.json` | **Met.** `CANDIDATE`, exit 0, ten gates pass. Pin `20c2c364d6c79592b87e8d467b0a4c29a2695fe89c3a5a83e247dfd7a7d758d6`; semantic `f08daa7b1bcc62f838d33821646b676548c14edd535cb3b4482fd358bbfaed2e`; executable `f97f084818723224bdd7f604a63e1941dadeb3e99af0cca3c9c6d30280d312f0`. The snapshot names all three. Gate 6 confirms the pin is the manifest's own value. One pin promoted; no second. |
| 2 | One committed record passes verification and yields a fresh administrator reading; an adverse or inconclusive reading closes the round without self-repair | Read `20260829-p-pump-fence/results/verification_summary.json`; confirmed the administrator's session id and record-only scope in `synthesis.md`; read trail `### T-004 return` and `### T-005 return` | **Met.** Verification `pass`: 48 rows stratified across all four observed verdict combinations, 10 channels at 1e-9, worst deviation 6.3463e-16, zero verdict mismatches, `not_independently_verified` empty. Administrator session `885bf5c5`, record-directory-only, `47fb5cb5`. The conditional did not fire (reading `ANSWERED`); nothing was self-repaired — the two open limits were routed, not fixed. |
| 3 | Every touched/new finding has a joined disposition with status and changed/next reference; no touched row remains `unrouted` | `git diff --numstat` over `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` at the disposition commit; `pytest tests/study/test_records.py` | **Met.** Seven joined rows under existing ids only; 7 insertions, 0 deletions, so no prior row was edited. `10 passed` including `test_findings_join_the_discovery_log`. The two rows whose Home column reads `unrouted` are ruled at trail `### Checkpoint C-001.r2` finding 2: ADR-004's clause governs the disposition class, not the log's Home column, and both dispositions are classed `model fix`. |
| 4 | `RoundReview` accounts for the pre-execution critic, task scopes/returns, comparison meaning, findings and learning before a next strategy is written | Read trail `### Round 1 review — 2026-08-29`; checked `learnings.md`'s append timing against the review commit | **Met.** Fresh session `88437945`, verdict `FINDINGS`, answer upheld. It accounted for the pre-execution critique (checkpoint C-001, both revisions), every task scope and return, the cross-pin comparison meaning, the seven dispositions and the four-claim delta — correcting L-001, L-003 and L-004 and catching an over-claim in the round result's own honesty statement. Learnings landed only after acceptance, at `4bf5d709`. No successor strategy was written; the goal closed instead. |
| 5 | Human and goal-agent routes meet the same artifact/native-state contract without duplicate side effects | Read `route_equivalence.md` §§ Isolation design, five-dimension table, Divergences, Findings | **Met, with a declared limit.** Same contract on artifact set, gates and reviewer-visible evidence; **identical** on native end states and return classes, with byte-identical pin and both fingerprints from an independent hand `integrate`. No duplicate external effects: zero commits either tree, no second promoted pin, no second committed study. Limit: `study.execute` fixture-substituted; study-runbook steps 7–15 not walked by hand. |
| 6 | Item-level and project-defined regressions pass; the epic proof report maps every criterion to evidence | Ran the plan's full § Regression Stencil; read `epic_evidence.md` §§ 1–2 | **Met.** Canonical battery 574 passed / 14 skipped, exit 0 (reference shape 570/14 — +4 passed, skips unchanged, the 21 reds green). `tests/models` 48 passed / 13 skipped with the 13 spine tests confirmed passing separately; the 13 skips are pre-existing template and foundation-library skips. `tests/research` 150 passed. `validate models/` L1 clean over 22 files, L2 the 12 known WARNs (exit 1 is the designed L2 stop). `source_registry.py verify` 0 faults, 3 known legacy. `epic_evidence.md` § 2 maps all eight criteria to resolving paths. |
| 7 | No hardening-path mechanism is present unless its promoting failure is recorded and owner-visible | Read `epic_evidence.md` § 5, which enumerates the eight things this item added and asks the ADR-003 question of each | **Met.** None of the eight is control-plane machinery. The one mechanism added — the evaluability pre-screen in the study's own `study.py` — is study-local, keeps policy at the call site, discloses its boundary as a result, and hardens no path. Four promoting failures are recorded and owner-visible (F-1, F-2, the stale-expectation class, the record-contract gap) and **none was built on**. No promotion requested. |
| 8 (spec) | `epic_evidence.md` states plainly that the research seam's request/return bookkeeper has never run end to end | Read `epic_evidence.md` § 3 | **Met.** Stated first among the honest limits: `scripts/research_seam.py`'s open → log → close has not been exercised by any round, this one included; the WI-033 flip evidence covers the seam's write door only; this round did not force a research disposition to exercise it. The same section states the parallel limit — `assert_read_set_covered` has never run at gate 6, reported not-run by the three of five invocations that reached that gate. |

## 4. Deviations, each with its authorizing ruling

| Deviation | Authorizing ruling | Note |
|---|---|---|
| **D1** — the regeneration runs under this coding-PM item; no new modeling work item minted for it | Spec § Align ruling 2 (owner routing) plus plan § D1 | ADR-009 calls a regeneration-gate refusal the modeling item's unfinished work, but the referent item WI-033 is closed by owner ruling and the owner named this item its successor. |
| **D2** — "regenerates and commits the package through the seam" read as: regenerate natively, commit, then the seam proves it | Plan § D2, surfaced not resolved silently (capture-fidelity law 4) | ADR-009 bars the seam from performing or committing. The reading delivers the owner's stated outcome and is the only one consistent with the seam as built. |
| **D3** — the plan names only the round's first task | Plan § D3, ADR-001, `GOAL_RUNBOOK.md` § Opening a round | A forward task list in a strategy would make it a plan. T-002…T-005 were each chosen from the evidence in hand. |
| **The oracle carry** — `verify_stellaris.py` edited despite `oracle_entry.py`'s written prohibition | `[OWNER 2026-08-29]`, on the round agent's recommendation, at `2f0f5133` | The round agent stopped rather than override on its own authority. The override is recorded in the commit, in a comment in the file, and in trail `### T-003 scope`. Reserved tier. |
| **The framing set** — search on `R` and `a`, one arm; `availability` and `discount_rate` declined; the comparand's window adopted in place of the step-7 scan | `[OWNER 2026-08-29]` "approved" / "decline those" / "adopted", recorded in `20260829-p-pump-fence/record.md` § 2 before any point ran | The window substitution was surfaced as a real substitution and ruled as one, not passed off as a detail. |
| **The evaluability bound** — 42 points pre-screened out on oracle `p_net > 0` | **Orchestrator tier, execution detail** — not an owner ruling. Stated honestly here because the record's § 2 table says the same. | Grounded in committed precedent: `20260823-magnet-technology-ab/record.md:224-226` established the pattern for that study's density floor. The round agent proposed it and stopped; the orchestrator ruled it in on that precedent. |
| **The goal close set** — goal closed, annex edit ratified, CAS10 guard minted as WI-034 | `[OWNER 2026-08-29]` at `5d740688`; `goal.md` § Close rule reserves closing to the owner | The fresh review recommended; it did not close. |
| **Orchestrator-performed commits** | The round's standing no-commit rule for stage agents | Every commit in § 1 was the orchestrator's. Stage agents made working-tree writes only. Five are data commits the stage agent recommended and did not make: `8099217b`, `cc249b89`, `2f0f5133`, `6e05c12f`, `0534c77b`. |
| **The 600-second timeout interruption and three-session resume** | `GOAL_RUNBOOK.md` § interruption — an invocation with no return is resumed from native artifacts | The round agent's session timed out after `### T-002 start`. Three fresh sessions resumed from native facts, briefed at `briefs/implement-p1-resume.md`, `-2.md`, `-3.md`, `-4.md`. Work completed but unrecorded was found already committed at `8099217b`. No prior trail entry was edited; T-002's single return covers the whole arc. Recorded in `epic_evidence.md` § 4 as a passed stress, not a defect. |
| **The harness kill of the first hand-route launch** | none needed — an environment incident | The hand route's first `integrate` was killed mid-run by a harness fault and relaunched clean with identical results. Named as an environment incident in `route_equivalence.md` § header so it is not read as route evidence. |
| **Lean shape — no `design.md`** | Spec § Align ruling 6 `[OWNER 2026-08-29]` | Deviation from the epic's deliverables list. The one real design question, route-equivalence isolation, lives in `plan.md` § Phase 6. |
| **Goal-question provenance — agent-drafted, owner-adopted** | Owner ruling 2026-08-29 ("use your drafts") | Spec Align ruling 1 intended § Question and § Answered when as the owner's own sentences; they are agent drafts the owner adopted verbatim. `goal.md` grades them honestly (`[AGENT] (adopted verbatim by owner ruling, 2026-08-29)`) with the challenge-path consequence stated. Omission from this record found by the item audit (F-1). |
| **Lean shape — briefs are the stage-instruction record** | The item's orchestrated run shape | `.project/active/goal-integration-study-proof/briefs/` holds twenty stage briefs (the twentieth is the audit's own, staged before the record was authored), each committed before its stage ran. They are how a later reader sees what each stage was told, in place of the review artifacts the lean shape omits. |
| **`set -a` substitution in the Phase-7 stencil** | none — a harness constraint, recorded rather than worked around | This session's tool harness refuses `set -a`. The same variables were supplied via `uv run --env-file`, which produces what the stencil's validation line asks for. Stated in `epic_evidence.md` § 1 and `plan.md` § Phase 7 Completion. |
| **`### T-005 scope` and `### T-005 start` written after the task ran** | none — a sequencing defect, recorded not backdated | The round owed a scope before the administer pass and did not write one. Surfaced by the round agent itself and flagged to the checkpoint critic. |

## 5. Owner-held remainder

None of the following is this item's to do, and none of it has been done.

- **Push, PR and merge.** Reserved gate 4. One PR ships WI-033 + Item 6 on `feat/wi033-p-pump-rebase` (spec § Align ruling 2, pre_pr option (a)). Nothing has been pushed and no PR exists. `/_my_pre_pr` is the branch gate and runs after close.
- **Closing the coding-PM item `goal-integration-study-proof`.** It stays in `.project/active/`. The audit runs first; `/_my_close` archives it on the owner's word.
- **Epic close-out.** Whether Item 6 completing closes the GSTH epic, and what its remaining items need, is the epic's question and not this record's.
- **WI-034.** Minted to the modeling backlog at `5d740688` on the owner's close ruling, carrying the CAS10 land-term guard from `20260829-p-pump-fence#1` and `20260823-magnet-technology-ab#1`. It is **backlog, not this item's work** — no spec, no design, no model edit was made against it here.
- **The four recorded hardening candidates.** F-1 (the operator guide's `toolchain-drift` row needs a checkout-kind carve-out), F-2 (the sealed environment is not reachable via `uv run` from a second checkout), the stale-expectation class (an expectation-coverage checker), and the record-contract gap (a numbers-to-artifacts check at runbook step 13). All recorded and owner-visible in `epic_evidence.md` § 4; none built, per epic SC 7.

## 6. What a reader should not conclude from this record

- **That the fence is bounded.** At a ≤ 0.85 the `recirc_ok` fence runs past the adopted window's largest R. The study locates how far it moved, not where it ends.
- **That +21.0 % is attributable to `p_pump` by the study record alone.** The record's § 12 says it is not. The attribution is licensed at the goal layer by the audited single delta — `git log ffa5c54c..8099217b~1` over `generated/` is empty, and `8099217b`'s own diff over `generated/` is `p_pump` in two files plus two provenance line numbers and the two contract fingerprints.
- **That the hand route reproduced the study.** It reproduced the declarations and every step-1–6 deposit. The 906 points were fixture-substituted.
