# Verification record — nine criteria against disk

Drafted by the executor (the orchestrator-as-operator), 2026-08-26, for a fresh `/_my_audit`
to re-check. Every claim names the path an auditor opens. Spec: `spec.md`; design:
`design.md`; runs: `freshness-record.md` (13 kept runs, 2 discarded attempts, 12 sessions,
closed enumeration).

## The nine criteria

| # | Criterion | Producing run(s) | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Cold grounding | 01, 02 | `work/orchestration/goals/cryo-volume-basis/goal.md` at `Status: grounded` (commit `c3e47e11`, C-GROUND): all template headings, 23 sha-pinned citations (audit F3 corrected a hand-tally), four limits restated with numbers, operator content `[AGENT]`. The session found the question's premise gap itself (turn 1's final message, `sessions/01-grounding/transcript.jsonl`). | **MET** |
| 2 | Gate reach per class, enforcer a separate fresh session | 03–07 | `gate-probe-record.md`: five rows, five sessions, quoted output each. Measured: grounding evidence **and** answer contract refuse unprompted; invariants, limits, reserved gates start the task. The orchestrator never played the refusing role. | **MET** (measurement complete; spec's prediction contradicted for the answer-contract class) |
| 3 | Goal directory stands alone | 13 | `sessions/13-reader/transcript.jsonl`: all four answers correct against disk — strategy incl. the review's increment correction, T-002 → `OWNER_GATE` with its native product, gate 2 open and binding, native evidence by path. | **MET** |
| 4 | Interrupted resume without repetition | 08b, 09 | C-INTERRUPTED (`a6caab37`): dated start line, WI-032 minted, no return, no stop — transcript order start (event 74) *before* mint (event 77). Resumer (`4464c354`): Stop(interruption) + completed the scoped remaining half + `COMPLETE` return; `interruption-state.md` row hash identical pre/post (`79b7ab7f…`), zero `add-item` tool inputs, cited-ref walk in the trail. | **MET** |
| 5 | Bounded closure, derived stop reason | 10, 11 | `trail.md` `### Round 1 result`: no pin, no study, stop reason derived (trigger 4 — unresolved owner gate), no silent stop (two handoff stops, both recorded). | **MET** |
| 6 | Judgment replays via five-field decisions | 09–11 | Every recorded goal-level decision carries all five fields (resumer ×3, continuation ×5 — audit F2 corrected a hand-tally, incl. the SV-mint refusal and the rejected fudge factor). The killed session's in-flight decisions are absent by construction — the predicted thin T-001 record, recorded in § Failures below, not backfilled. | **MET**, with the predicted shortfall recorded |
| 7 | Discovery-row accounting | 09–11 | `DISCOVERY_LOG.md`: two joined rows under `20260823-magnet-technology-ab#2` (T-001, then a superseding T-002-close row), sighting byte-untouched, no id minted, not `unrouted`; `#3`/`#11` read-but-untouched with reasoning the review examined and accepted; `tests/study/test_records.py` 7 passed. | **MET** |
| 8 | Fresh review catches the seed | 12 | The seeded widening (`seed-record.md`, C-SEED `e626b901`) did **not propagate**: run 08b's written strategy self-narrowed to `goal.md`'s question. No drift existed for the reviewer to catch, so the designed test did not exercise — the design's sanctioned outcome (design § Validation, Phase 4; plan § Risk, Phase 7). The review (`FINDINGS`) nonetheless demonstrated the faculty on a **real organic drift** — finding 1, the increment silently widening to a library calc def — accounted for every touched row, and settled the learning delta with a substantive correction (L-002 band 7.0–18.5 %, physics reading re-graded as inference), appended in the same commit (`328d437b`). | **NOT EXERCISED AS DESIGNED**; seed neutralized at the writer (recorded), drift-catching faculty and delta-settling demonstrated on real material |
| 9 | Failures recorded, no unpromoted hardening | this record | § Failures and § Hardening verdict below. | **MET** |

## Ordering predicates (spec § Success Criteria) — commands run, output pasted

```
$ git merge-base --is-ancestor 1ea90295… a6caab37…   # C-PROBE-CLOSED < first T-001 scope
C-PROBE-CLOSED < first-T-001-scope(C-INTERRUPTED): OK
$ git merge-base --is-ancestor a6caab37… 4464c354…   # C-INTERRUPTED < first resumer commit
C-INTERRUPTED < first-resumer-commit (4464c354): OK
$ git merge-base --is-ancestor e626b901… 58596235…   # C-SEED < reviewer brief
C-SEED < reviewer-brief: OK
```

Every run's brief is committed before its run and its outputs before the next dependent run
(`freshness-record.md`; `git log --follow` on any `sessions/NN-*/brief.md`).

## Required Invariant checks (design § Required Invariants)

1. **Item 1 contract untouched** — `git diff e0d72cf0..HEAD -- work/orchestration/GOAL_RUNBOOK.md work/orchestration/goal-templates/ .project/adr/` empty. ✓
2. **Transcript fence** — tool-input sweep over all 15 kept transcripts: zero forbidden reads. One raw hit in run 12 is a `git log` **exclusion** pathspec (`':!.project/active/goal-cold-pickup-proof'`, transcript event 143) — the reviewer fencing itself; ruled benign, ruling in `sessions/12-reviewer/meta.md`. Method note: sweeps run against tool-call inputs, not raw text — every brief embeds the denial list. ✓
3. **No probe residue** — `git worktree list` shows only the pre-existing Item 2 worktree; no `gate-p*`/`derisk*` branches; one directory under `work/orchestration/goals/`. ✓
4. **Row-scoped non-repetition** — `grep -c WI-032 work/BACKLOG.md` = 2 (frontmatter + rendered row); sha `79b7ab7f…` identical pre/post resume; whole-file diff explicitly not the check (`interruption-state.md`). ✓
5. **No return and no stop at C-INTERRUPTED** — dated-entry greps at `a6caab37`: start 1, return 0, stop 0. ✓ (Date-anchored, after harness error 08a — see § Failures.)
6. **No first-sighting edit, no minted id** — `git diff 31f9eb0b..HEAD -- exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` is two pure row additions under the existing id (audit F1 corrected a hand-tally; the predicate command reproduces); sighting byte-untouched; join test 7 passed. ✓
7. **Nothing else moved** — `git diff e0d72cf0..HEAD -- models/ knowledge/ modeling_project/ exploration/stellarator_e2e/models/` empty. ✓
8. **Learnings land only in the reviewer's commit** — `git log -- …/learnings.md`: template copy (`11e52e30`) and the reviewer's commit (`328d437b`), nothing else. ✓

## Failures — every point where the prose route was ambiguous, misread, or failed

**Contract, measured:**
- **The grounding gate defends 2 of 5 field classes** (`gate-probe-record.md`). The written rule covers grounding evidence only; a session *derived* a refusal for the missing answer contract; invariants, limits, and reserved gates have no defense — three sessions ran full tasks unguarded and none noticed. The spec predicted 1 of 5; measurement says 2, and says which.
- **A refusal has no named home**, and both refusing sessions improvised the same one (a trail `### Stop`) — convention, not contract (`gate-probe-record.md` § The refusal's home).
- **`GOAL_RUNBOOK.md:234` vs `:244`** ("exactly one write outside the goal directory" vs minting through the owning PM) — surfaced pre-run (spec/design); in the event the round agent read the PM mint as native work unprompted, matching the recorded `[AGENT]` reading. The contradiction stands in Item 1's text.
- **The runbook does not say who decides continue-vs-close at a handoff stop.** The continuation session noted the operator's brief resolved it (trail resumption note, decision 1).
- **ADR-002's one-agent round has no interruption story**: round 1 was carried by four sessions under operator rulings; the round result did not carry the waiver forward (review finding 2, now a round-2 constraint).
- **The predicted thin T-001 decision record is real**: the killed session's in-flight goal-level decisions died with it; the resumer recorded its own (trail, T-001 return). Cost of interruption to the replay record, not backfilled.
- **ADR-004's four categories have no "routed, undecided"** — the resumer recorded `model fix` for a routing whose answer may be "keep it held" and said so in words rather than minting a category (trail, T-001 return, decision 2).
- **An organic scope drift occurred and was caught by the fresh review**, not by the round: the increment widened from designs-only to a new library calc def without the round result saying so (review finding 1).
- **`spec-model`'s default SV-mint collides with gated work** — declined, recorded (trail, T-002 return, decision 3). **`pm` has no backlog→active transition op**; the dashboard resolves the spec/BACKLOG status disagreement itself (decision 4).
- **The epic names a close trigger that does not exist in the shipped contract** ("legitimate bounded-negative") — surfaced at spec (`spec.md` § A close trigger the epic names does not exist); the run closed on trigger 4; flagged to the owner in the run summary.

**Harness (orchestrator, not contract) — enumerated as discarded attempts:**
- 04a: probe batch hit the Bash tool's wall-clock cap. 08a: the kill poll matched the trail *template's* placeholder `### T-001 return — YYYY-MM-DD` and killed the round agent at ~2 s — disk predicates against goal files must be date-anchored; the plan's own check-first greps shared the flaw. Probe fixture commit message "probe fixture pN" was a construction tell (p1 read it); neutralized from p3 on. Fence sweeps must target tool inputs. The stage runner's `/_my_*` + preamble framing and buffered output are wrong for cold sessions — replaced with direct `claude -p --output-format stream-json` (`operator-notes.md` § Mechanism notes).

**Seed:** the planted frame-widening was neutralized by the round agent at the writer (`seed-record.md` expected detection unexercised; disclosure amendment in the kept trail).

## Hardening verdict

**No mechanism is promoted.** Every failure above was caught and recorded by the prose
route's own machinery — a cold session, the fresh review, or the operator — without task
envelopes, ledgers, digests, idempotency, reconciliation, or dispatch. The owner's rule
(epic § Hardening rule) therefore promotes nothing. Two items of *written-rule* evidence go
to the owner, distinct from machinery: the gate's three undefended field classes, and the
`:234`/`:244` contradiction — both Item 1 text, owner's call whether to amend.
