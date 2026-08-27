# Audit: Goal Cold-Pickup Proof (GSTH Item 4)

**Verdict:** Certify — with Criterion 8 certified as *not exercised as designed*, not as a pass
**Audited:** 2026-08-26
**Branch:** `feat/goal-integration-seam`
**Commit:** `ab5fa06e`
**Auditor:** fresh session; re-ran every command the verification record pastes, plus four checks the record does not make

---

## The Point

The goal layer is meant to let a non-builder pursue a real modeling question across sessions using
nothing but prose on disk — a `goal.md`, a `trail.md`, and a `learnings.md` — with no task
envelopes, no event ledger, no digests, no idempotency keys, and no reconciliation pass. The
owner's rule is that none of those five mechanisms enters the first build unless a recorded proof
run shows the prose route actually failing (`epic_goal_strategy_task_harness.md:74`).

That rule only bites if someone runs the prose route for real. Item 4 is that run. Its job is not
to make the goal layer look good; it is to put Item 1's shipped contract in front of sessions that
did not build it and record what happened — including where the contract turned out to be thinner
than the epic assumed. A proof that reports only successes would leave the hardening rule with
nothing to rule on.

## Summary

The claims hold. I re-ran all three ancestry predicates, all eight Required Invariants, the record
suite, the transcript-fence sweep, and the criterion-4 ordering evidence — every one reproduces.
Two checks the record only asserts in prose I turned into commands, and both pass: all thirteen
kept briefs are strictly-earlier commits than their transcripts, and the twelve distinct session
ids in the transcripts match the freshness record row for row.

The most important thing I checked is not in the record's own list. The record downgrades
Criterion 8 to "not exercised as designed," and the obvious worry is that this is a post-hoc
excuse written after the seed failed to propagate. It is not. The "if the agent flags the widening
instead of carrying it, record that Criterion 8 was not exercised as designed" branch is in
`design.md:269` and `plan.md:400,550,698`, in commits `e8ea658b` and `c6e5aeca`, both ancestors of
the interrupted-state commit `a6caab37`. The branch was declared before the round agent ran.

Three defects, all in the record's hand-tallied counts, all conservative, none touching a verdict.

## Product Judgment

**Is this the right piece of work? Yes — and it is the rare proof item that reports against
itself.**

Ledger gate: **CLEAR**. I scanned every block in `product-lens.md`, not just the newest. The spec
hop recorded two `[DO]` findings at BLOCK (spec-F1, the missing five decision fields; spec-F2, the
grounding gate that cannot hold as written), both resolved by citation in the same-hop disposition
block, and the spec-review note leaves the gate CLEAR. The epic's own Product-Lens gate
(`epic_goal_strategy_task_harness.md:94`) is CLEAR. No unresolved BLOCK anywhere in the chain.

I ran the implementation-hop lens myself rather than delegating it — this session is barred from
spawning agents — and derived the point independently from `epic_goal_strategy_task_harness.md`
§ Hardening rule, `.project/adr/003-lean-first-persistence.md`, and
`.project/concepts/goal-driven-model-development-harness.md` § Owner's Words, without inheriting
the spec's framing. Falsifier: *the proof produces evidence that reads as a certificate for the
lean route rather than as measurement of it.* It does not fire. The two places where the work
could have flattered itself are both places it did the opposite:

- **The grounding gate.** The epic assumed five field classes are defended. Measurement says two
  (`gate-probe-record.md`), and the record names which three sail through and quotes the sessions
  that ran full tasks unguarded. It routes the repair to Item 1's owner instead of quietly fixing
  the runbook — and `git diff e0d72cf0..HEAD` over `GOAL_RUNBOOK.md`, the templates, and
  `.project/adr/` is empty, so it really did leave the contract alone.
- **The seeded drift.** The designed test did not run. The record says so in bold, in the same row
  where it reports the faculty being demonstrated on a real organic drift instead.

Structural smells, checked against product-lens spec §4:

- *A test passes only because it selects one favorable route* — **does not fire, and this is the
  one that mattered.** The tempting move was to let the review's organic finding 1 stand in for
  the seed and call Criterion 8 met. Every artifact refuses that substitution:
  `verification_record.md:19` (verdict "NOT EXERCISED AS DESIGNED"), `sessions/12-reviewer/meta.md`
  (last line), `plan.md:717,726`, `freshness-record.md` (run 08b, "seed did not propagate (B4
  false)"), and the trail's own disclosure amendment (`trail.md:256-259`). I found no artifact
  that softens it into a pass.
- *A special category exempts a case whose user-visible meaning is unchanged* — does not fire. The
  downgrade is a pre-declared branch, not a category invented to absorb a miss.
- *Two representations kept manually in sync* — does not fire. The trail cites native state and
  never restates it; the discovery log carries joined rows under existing ids and the join is
  machine-checked (`tests/study/test_records.py`, 7 passed).
- *Correctness depends on downstream knowledge of an internal representation* — does not fire. Run
  13 answered four questions correctly from the goal directory and its citations alone.

One judgment the brief asked me to make myself: the single fence hit. Run 12's tool input contains
the item-directory string as a **`:!` exclusion pathspec** in a `git log` sweep — the reviewer
fencing the forbidden directory *out* of its own history walk. That is the opposite of a read. I
concur with the benign ruling, and I reached it from the raw tool input, not from the ruling.

## Findings

### Plan completion

All eleven phases are carried by dated `**Completed:**` notes at `plan.md:705-735`, each naming
its commit, and each reproduces against `git log`. Phase 0's de-risk results land in
`operator-notes.md` § Mechanism notes as the plan directed, correctly excluded from the freshness
record as mechanism evidence rather than cold runs.

**F4 (low) — `plan.md:3`: the plan reads "Complete (all 11 phases)" while 0 of its 119 step-level
checkboxes are ticked.** `git show a9c31af8` shows the closing commit filled the per-phase
Implementation Notes and flipped the status line, and never touched a `- [ ]`. Nothing is
misreported — the notes are more informative than the boxes would be — but the plan's two
completion surfaces disagree, and a reader who greps for unchecked boxes gets a false alarm. Tick
the phases whose notes carry them, or say in the status line that completion is tracked in the
notes.

### Spec conformance

Nine criteria. Eight met; one honestly downgraded.

- **1 — Cold grounding: MET.** `goal.md` carries all eleven template headings in template order
  (checked against `work/orchestration/goal-templates/goal.md`), `Status: grounded`, four limits
  restated with numbers (retry 2, checkpoint 2, rounds 6, time none), reserved gates as a general
  rule plus five named instances, and a close rule. Session 01 found the question's own premise
  gap unprompted.
- **2 — Gate reach per class: MET as measurement.** Five rows, five distinct session ids, quoted
  output each. The five probe briefs are byte-identical (`md5sum` across
  `sessions/0[3-7]-gate-p*/brief.md`) and contain no hint that a refusal is expected or which
  class is hollowed — they say "open a round and start work." The enforcer was a separate fresh
  session in every case; the orchestrator never played the refusing role. Measured reach is 2 of
  5, contradicting the spec's own prediction for the answer-contract class, and the record says so.
- **3 — Goal directory stands alone: MET.** I read run 13's final message against disk. All four
  answers are correct, including the review's finding-1 increment correction, which it surfaced
  unprompted. Zero write-shaped tool calls in that transcript.
- **4 — Interrupted resume: MET.** Verified independently and in the record's own terms. At
  `a6caab37` the trail carries exactly one dated entry — `### T-001 start — 2026-08-26` — with no
  return and no stop. In run 08b's transcript the start line is written at line 75 and
  `pm add-item` fires at line 78 (the record's 0-indexed 74/77), so the write-ahead genuinely
  preceded the landed effect. The WI-032 row hash is `79b7ab7f…` at `a6caab37`, at `4464c354`, and
  at HEAD — identical at all three. The resumer's transcript contains zero `add-item` tool inputs;
  so do runs 10 and 11.
- **5 — Bounded closure: MET.** `git diff --stat e0d72cf0..HEAD -- exploration/` is two insertions
  in `DISCOVERY_LOG.md` and nothing else, so no study was committed and no pin promoted. The stop
  reason is derived in the trail from the last semantic outcome plus the limits
  (`trail.md:165-169`), not carried as a second status enum. Both handoff stops are recorded.
- **6 — Five-field decisions: MET.** Eight goal-level decisions across two `**Decision fields.**`
  blocks; each carries all five fields, verified by parse, not by eye. See F2 for a count slip in
  the record.
- **7 — Discovery-row accounting: MET.** Two joined rows under `20260823-magnet-technology-ab#2`,
  both pure additions; the 2026-08-23 sighting is byte-untouched; no id minted; the row is not
  `unrouted`. `tests/study/test_records.py` — 7 passed.
- **8 — Fresh review catches the seed: NOT EXERCISED AS DESIGNED.** Correctly recorded, and I am
  certifying that recording rather than the criterion. The seed did not propagate: the round agent
  narrowed the widened frame back to `goal.md`'s question at the writer, so no drift existed for
  the reviewer. The pre-declared branch covering exactly this outcome is at `design.md:269` and
  `plan.md:400,550,698`, both commits ancestors of `a6caab37` — declared before the run, not
  after it. The review demonstrated the faculty on a real organic drift (finding 1, the increment
  silently widening to a library calc def), accounted for both touched rows and the two read-and-
  untouched ones, and settled the delta with a substantive correction (L-002's band sharpened to
  7.0–18.5 %, the physics reading re-graded as this round's inference). `learnings.md` history is
  exactly two commits: the template copy `11e52e30` and the reviewer's `328d437b`.
- **9 — Failures recorded, nothing promoted: MET.** Ten contract-level failures and two harness
  errors enumerated, each with the artifact that shows it. Hardening verdict: nothing promoted,
  with the reason stated. Two items of *written-rule* evidence go to the owner instead, correctly
  distinguished from machinery.

**Tagged requirements.** The `[HARD]` fence held: no cold session read the item directory (fence
sweep below). The `[HARD]` no-child-branch and stay-on-`feat/goal-integration-seam` requirements
hold. The `[NEED]` operator-notes artifact exists and answers what the requirement asked — what
the runbook prompted, what the operator supplied, where it stalled, the judgment calls — plus an
unrequested and welcome § What a headless bound could and could not show. Non-goals respected:
no runbook, template, or ADR change; no dispatch; no route-equivalence comparison.

### Design conformance

All eight Required Invariants re-checked by re-running the record's commands.

1. **Item 1 contract untouched** — `git diff e0d72cf0..HEAD` over `GOAL_RUNBOOK.md`,
   `goal-templates/`, `.project/adr/` is empty. ✓
2. **Transcript fence** — I wrote my own sweep (`audit-fence-sweep.py`, kept beside this file) over
   tool-call *inputs* in all 15 transcripts. Exactly one hit, run 12's exclusion pathspec, judged
   benign above. ✓
3. **No probe residue** — `git worktree list` shows only the pre-existing Item 2 worktree
   (`fusion-tea-goal-research-seam`); no `gate-p*` or `derisk*` branch exists; one directory under
   `work/orchestration/goals/`. ✓
4. **Row-scoped non-repetition** — two `WI-032` occurrences (frontmatter + rendered row); row hash
   identical at three commits. ✓
5. **No return and no stop at C-INTERRUPTED** — one dated entry at `a6caab37`, the start line. ✓
6. **No first-sighting edit, no minted id** — pure additions under the existing id; join test
   passes. ✓ (See F1 for the count.)
7. **Nothing else moved** — `git diff e0d72cf0..HEAD` over `models/`, `knowledge/`,
   `modeling_project/`, `exploration/stellarator_e2e/models/` is empty. ✓
8. **Learnings land only in the reviewer's commit** — two commits, template and reviewer. ✓

**Two checks the record asserts in prose but does not run, which I turned into commands and which
both pass.** These are the load-bearing freshness claims, so leaving them unexecuted was the
record's one real gap in method:

- *Every kept run's brief was committed before its run.* For all thirteen kept runs, the brief's
  introducing commit is a strict ancestor of the transcript's (`audit-brief-ordering.py`). No
  same-commit cases, so ancestry proves the ordering everywhere, not just where it was pasted.
- *Twelve distinct sessions.* Extracted `session_id` from every transcript: twelve distinct ids,
  matching the freshness record row for row, including both resumes sharing an id (01/02, 10/11)
  and 04a carrying its own discarded id. Run 08a has no session id, consistent with "killed before
  init"; its transcript is 0 bytes as the record states.

### Code integrity

No production code was written by this item, so the abstraction and failure-honesty rubric mostly
does not apply. The three record-keeping scripts are the auditor's, not the item's.

One observation on the item's own machinery, offered as evidence rather than a defect: the two
harness errors (04a's wall-clock cap, 08a's poll matching a template placeholder) are both
recorded as discarded attempts with their lessons generalized — "any disk predicate against goal
files must distinguish template scaffold from real entries" — and the record notes the plan's own
check-first greps carried the same latent flaw. That is the failure-honesty standard the rubric
asks for, applied to the harness rather than to a codebase.

---

## Ranked findings

**F1 (medium, accuracy) — `verification_record.md:43`: Required Invariant 6 says "three pure row
additions"; disk shows two.** `git diff 31f9eb0b..HEAD -- exploration/stellarator_e2e/studies/
DISCOVERY_LOG.md` is two `+` lines, and `git log` shows exactly two commits touching the file
(`4464c354`, `57129cb9`), one row each. The record contradicts itself: Criterion 7 at line 18 and
the trail at `:177` both say two, correctly. The invariant's substance is unaffected — pure
additions, sighting untouched, no minted id — but a number an auditor re-derives should match.
Change "three" to "two".

**F2 (medium, accuracy) — `verification_record.md:17`: Criterion 6 says "resumer ×2, continuation
×5"; disk has resumer ×3 and continuation ×5, eight in total.** The T-001 return carries three
five-field decisions (`trail.md:53-63`), not two. All eight carry all five fields, so the criterion
is met more strongly than claimed. Correct the count.

**F3 (low, accuracy) — `verification_record.md:12`: Criterion 1 says "22 sha-pinned citations";
`goal.md` carries 23** (`grep -oE '@[0-9a-f]{7,40}'`). Same conservative direction as F1 and F2.

The three together are one pattern worth naming: the record's counts were tallied by hand while
its predicates were run as commands. The predicates all reproduce; the tallies drift, always
downward. If any number in that record is going to be re-derived by a reader, it should be
produced the same way the predicates were.

**F4 (low, tracking) — `plan.md:3`:** see Plan completion above.

---

## Certification

**Certify.** The verification record is a claim I could re-check, and it re-checks. Eight criteria
are met; the ninth is recorded as not exercised as designed, on a branch declared before the run,
and I found no artifact anywhere in the item, the goal directory, or the epic that softens it into
a pass. The product-lens ledger gate is CLEAR at both the item and epic hops. No structural smell
fired. The three accuracy findings are corrections to make in the record, not grounds to withhold
certification — none of them changes a verdict, and all three understate the item's own result.

Marked as verified:
- `spec.md` — success criteria 1–7 and 9 checked; **criterion 8 deliberately left unchecked**, with
  the reason written beside it. Checking it would be the softening this audit exists to prevent.
- `plan.md` — status line annotated to say completion is carried by the per-phase notes (F4).
- `.project/backlog/epic_goal_strategy_task_harness.md` § Item 4 — the four success criteria that
  are fully met are checked. The first (ungrounded draft rejected "with the missing fields named")
  and the fifth (fresh review catches the seeded drift) are left unchecked: the first was measured
  at 2 of 5 field classes, the fifth did not exercise. **No ✅ on the Item 4 heading** — partial
  certification, and the two open criteria are the epic's to dispose, not this audit's.
- `.project/CURRENT_WORK.md` — item status updated to certified with the two open epic criteria
  named.

Three re-runnable auditor scripts are kept beside this file as evidence, in the spirit of the
item: `audit-fence-sweep.py`, `audit-c4-order.py`, `audit-brief-ordering.py`,
`audit-reader-and-writes.py`.

**Two things for the owner, carried forward from the record and confirmed here.** Neither is a
defect in this item; both are Item 1 text the owner may want to amend now that the evidence is in:
the grounding gate's three undefended field classes (invariants, limits, reserved gates), and the
`GOAL_RUNBOOK.md:234` vs `:244` contradiction about writes outside the goal directory.

**Not checked:**

- **`~/goal-proof-logs/` was unreachable.** It sits outside this session's permitted working
  directory, so the brief's requested cross-check of the 13+2 enumeration against the external log
  directories did not run. I substituted two in-repo closure tests — twelve distinct session ids
  extracted from the transcripts matching the record row for row, and every kept brief committed
  strictly before its transcript — which close the enumeration against everything the repository
  can see. What they cannot exclude is a cold run that left no session directory, no commit, and
  no transcript. Nothing in the repository suggests one; nothing in the repository could rule one
  out either. An owner with shell access to that directory can close this in one `ls`.
- **Transcript content beyond tool inputs and final messages.** The fence sweep is scoped to
  tool-call inputs, which is the right scope for the fence and is what the invariant asserts. I did
  not read the fifteen transcripts end to end, so a session that reasoned about forbidden material
  without ever issuing a tool call against it would not appear in my sweep. For the three sessions
  whose conclusions carry weight — 08b's ordering, 09's non-repetition, 13's four answers — I read
  the relevant tool calls and final output directly.
- **The substance of the fusion physics.** L-001 through L-003, the `8π²` factorisation, the
  7.0–18.5 % residual, and the −16 %/+0 % tolerance were checked for internal consistency across
  the trail, the learnings, and the discovery row, and the reviewer recomputed them independently
  in run 12. I did not re-derive the arithmetic from the sources myself. That claim rests on run
  12's recomputation, which is a fresh session's, not the author's.
- **`WI-032`'s spec quality.** I confirmed the spec exists, that it is gated at spec stage, and
  that no design, plan, or model edit followed. I did not audit its contents against the modeling
  PM's requirements — that belongs to the modeling PM, on the owner's ruling.
- **Items 1, 2, 3, 5, 6 of the epic.** Out of scope. Epic certification needs all items audited;
  this covers Item 4 only.

---

## Post-audit closure of the one unverified check — orchestrator, 2026-08-26

The audit could not reach `~/goal-proof-logs/` (outside its working directory) and
substituted in-repo closure tests. The orchestrator ran the missing `ls`:

```
00-derisk
00-derisk-wt
01-grounding
02-grounding
03-gate-p1
04-gate-p2
05-gate-p3
06-gate-p4
07-gate-p5
08-round-agent
09-resumer
10-continuation
11-gate-ruling
12-reviewer
13-reader
phase23-progress.txt
phase45-progress.txt
phase4-progress.txt
phase56-progress.txt
phase6b-progress.txt
phase7-progress.txt
phase8-progress.txt
verification-checks.txt
```

Fifteen entries: `00-derisk`, `00-derisk-wt` (Phase 0 mechanism evidence, per the
freshness record's closing statement), the thirteen kept-run directories `01`–`13`
(04 and 08 each also holding their discarded attempt's transcript), and the orchestrator's
progress files. **No directory exists for a run the enumeration does not carry.** The
external side of the closure now matches the in-repo side.
