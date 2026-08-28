# Audit: GSTH Item 5 — Research-to-Model Round Proof

**Verdict:** POSITIVE — five findings, none of which overturns a verdict in the record
**Audited:** 2026-08-28
**Branch:** `feat/goal-research-model-proof`
**Commit:** `eef3865c` (working tree clean; base `e44498d4`)

---

## The Point

The goal layer is supposed to let a modeling question be pursued across rounds under a contract:
a bounded task runs against native evidence, a fresh critic reviews the reading before anything
downstream executes, every touched finding gets a disposition, and a fresh reviewer closes the
round without the round agent grading itself. Item 5 asks whether that contract actually holds
when it is run live, on a real open question — `p_pump` = 1.0 MW in the committed A/B study —
rather than on a rehearsal. The deliverable is not a model change. It is a proof, and the
`verification_record.md` is the thing being certified.

The honest-outcome discipline is the load-bearing part. A proof item that grades itself after
the fact proves nothing, so the item declared in advance which criteria each possible outcome
would cover (`covering-branches.md`, committed at `e02ce403` before any session ran) and let
`git log` carry the ancestry.

## Summary

The record holds. I re-ran all nine criterion rows, both ordering predicates, and all ten
invariant checks against disk — including the Invariant 2 tool-input sweep over 174 tool calls
across eight transcripts — and every number the record pastes reproduces exactly. The
covering-branch discipline is real, not retrofitted: I read the `covering-branches.md` blob at
`e02ce403` and the branch the round closed on was declared there, with the same covers /
non-exercised split the record grades against. The owner-ruling chain traces to real commits with
verbatim text. The hardening verdict survives my own whole-diff read plus a sweep wider than the
one the plan specifies.

What I found is a layer of citation and bookkeeping defects in the item's own records — the same
defect class the round's fresh reviewer caught as its Finding 1, now appearing inside the record
that reports it. None changes a verdict. Three of them are in artifacts the record itself
presents as settled, which is why they are worth fixing before close rather than noting and
moving on.

## Product Judgment

**Is this the right piece of work?** Yes, and the strongest evidence for that is what the item
declined to do. The round could have manufactured a research need to light up criteria 3, 4 and
7. It didn't: T-001 found the repository could answer the question, returned `COMPLETE`, and the
item graded itself against a branch row written the day before (`covering-branches.md:32`,
`R-B3`). An item that proves less because the honest path proved less is the correct behavior for
a proof item, and it is what the goal layer exists to make possible.

**One thing a reader of the epic must not miss, stated as a limit rather than a block.** The item
is titled "research-to-model" and the research half never ran. The Item 2 seam was not invoked
(criterion 3), no work item was minted (criterion 4), and the runbook `research` row is still
stale (criterion 7). Criterion 1 was retired by owner ruling. So four of nine criteria carry no
live evidence, and what Item 5 actually proves is the *model → critic → disposition → review*
spine, not the seam. The record says this plainly in every relevant row, and the owner ruled the
retirement — so this is disclosure working, not concealment. But the epic's Item 5 heading should
not be read as "the seam is proven."

**Product-lens ledger gate: NOT RUN.** `product-lens.md` does not exist. The spec has cited it as
a Related Artifact since drafting; `spec-review.md:30` (finding **L1-5**) flagged the dangling
reference as "the kind of thing the audit will trip on later," and it now has. The record lists
it correctly under § Still owed. This audit does not clear that gate — see Certification.

**Structural smells:** none fired. The item ships no code. The full diff vs `e44498d4` is 58
files, all prose: the item directory, three new goal files, two appended `DISCOVERY_LOG.md` rows,
and one line of `CURRENT_WORK.md`. There is no function, no test, and no tool to be god-shaped,
leaky, or silently-falling-back.

## Findings

### Plan completion

All phases through Phase 13 are executed and their artifacts are on disk. The two phases the plan
gates on a seam run (the `T-002` execution phase, and Phase 11's runbook flip) correctly did not
run — `plan.md:925` makes both conditional on the seam having run, and it did not.

**Finding 1 — `operator-notes.md` ships with skeleton text and three headings that were never
filled.** `operator-notes.md:7` still reads "*Not yet populated.*" in a file whose own header
says it was "Written at Phase 12 from the kept transcripts." Three headings carry no body:
`:9` (what the runbook prompted for unprompted), `:11` (where the exchange stalled), and `:17`
(the Invariant-3 narrowing). The first two have content, but it is at `:53` and `:54` under
"Post-run notes" — so the file reads as unfinished when it is merely re-homed. `:17` has no
content anywhere in the file; the material exists at `plan.md:94` and was never carried across.
**Fix:** delete `:7`, fold `:53`/`:54` under their own headings or delete the empty ones, and
either write `:17` or strike it.

**Finding 2 — `operator-notes.md:45` is stale and contradicts two other records.** It reads
"**Status: authorized, not yet exercised.** No cold run has used it." Both
`verification_record.md:59` ("exercised from session 02 on") and `freshness-record.md:26` ("the
transcripts were teed in-repo per the authorized deviation") say the opposite, and the eight
committed transcripts are the evidence. The line was true when written at authorization time and
was never updated at Phase 12. **Fix:** update the status line to record that it was exercised
for sessions 02–08 and that the transcripts landed complete and well-formed, which was the
confirmation `:45` asked the first user to make.

### Spec conformance

I re-ran every row rather than reading the record's summary of it. Criterion numbering follows
`spec.md` § Success Criteria.

| # | Record's verdict | My re-run |
|---|---|---|
| 1 | Retired `[OWNER 2026-08-28]` | **Confirmed.** Ruling is real and at a real commit: `briefs/implement_resume_gate_a.md@c8362239` Ruling 1, and `c8362239` is an ancestor of the session-02 brief `0e69a043`. `trail.md` § T-001 scope / § T-001 return exist and T-001 ran as a bounded task |
| 2 | MET — bound and released | **Confirmed at the session ids.** Author `a94a3ddd` (sessions 03/05/07, the last two labelled resumes); critics `832ac26a` (04) and `2a8ee4ea` (04b), both distinct and both new. Ordering holds: `C-001.r2` passed at `b209766c`, dispositions landed at `2b9ee81e`, and `b209766c` precedes it in `git log`. Trail lines `:134` and `:307` resolve as cited |
| 3 | Non-exercised under the declared branch | **Confirmed, and the branch predates the round** — see § Covering-branch discipline. No seam artifacts exist; `knowledge/` diff vs base is empty; `source_registry.py verify` → `0 fault(s), 3 legacy entry(ies)`, matching the record verbatim. No hand-written registry step either |
| 4 | Non-exercised, same branch | **Confirmed.** `work/` is untouched in the diff vs base. `p_pump` is still `1.0` at `models/designs/stellarator_09/stellarator_plant.sysml:502` and the exploration twin is identical. Gates 2/3/4 were referred, not decided |
| 5 | MET | **Confirmed.** Two appended `DISCOVERY_LOG.md` rows under existing ids `#3` and `#5` at `2b9ee81e`; removed-line count is 0; `tests/study/test_records.py` → **7 passed**. `learnings.md` has exactly two commits, the template at `e02ce403` and the reviewer's append at `104a68b5` — the R-F4 claim ("appended only in the reviewer's commit") holds |
| 6 | MET | **Confirmed.** `trail.md:457` is `### Round 1 review — 2026-08-28`, verdict `FINDINGS`. Reviewer session `cbc65841` appears in no other `meta.md`. Goal `Status` is still `grounded`, not closed — the review recommends and does not rule. No PM state mirrored |
| 7 | Non-exercised | **Confirmed.** `git diff e44498d4..HEAD -- '*GOAL_RUNBOOK.md'` → 0 lines. The stale row stands, recorded at § Failures 1 |
| 8 | MET | **Substantially confirmed, with a ninth entry owed** — see Finding 3. All eight entries resolve: every sha they name (`8f731fa7`, `b8a791ce`, `71d2abe8`, `71244a3b`, `104a68b5`) exists and carries the change described |
| 9 | MET | **Confirmed, and I widened the check** — see § Hardening verdict below |

**Ordering predicates.** Invariant 4: `git merge-base --is-ancestor e02ce403 71d2abe8` → OK, and
`08af1532 → 71d2abe8` → OK. Both re-run by me. Invariant 5 is correctly non-exercised: no seam
run, no flip, nothing to order.

**Non-goals respected.** The spec bars building anything new. Nothing executable entered the diff.

### Design conformance

**Covering-branch discipline — the central check, and it holds.** I did not take the record's
summary. I read `covering-branches.md` as it stood at `e02ce403`:

- The branch "T-001 returns `COMPLETE`" was **already there**, at line 36 of that blob, declaring
  Covers = 2, 5, 6, 8, 9 and non-exercised = 1, 3, 4.
- At HEAD the same row is line 32, reworded to "The repository answers it," with criterion 1
  dropped from the non-exercised cell because it was separately retired.
- The covers / non-exercised split the record grades against is therefore **identical to the
  pre-round declaration**, criterion 1 aside. The outcome was declared before it existed, and the
  run was graded against the declaration rather than excused after the fact.

Criteria 3, 4 and 7 are each graded to that row, not ad hoc: 3 and 4 to the branch's
non-exercised cell, 7 to the file's stated rule that criterion 7 tracks the seam *run* and goes
non-exercised on branches where the seam never ran (`covering-branches.md:40`).

**One in-place edit, authorized and disclosed.** `08af1532` rewrote Table 1 in place — criterion 1
stripped from every Covers cell and one row's label reworded. The file's own line 42 forbids
editing the table to accommodate an outcome; this edit was not that. It applied an owner ruling
retiring a criterion, it is recorded in § Amendment 2026-08-28 with the authority named, and the
ancestry claim survives. **But** § Amendment's phrase "the tables above are otherwise as declared
at C-COVER" understates it — an auditor reading only HEAD cannot see that the table changed. The
amendment should say plainly that the Covers cells were edited and the `COMPLETE` row reworded,
so the diff is not the only place that fact lives. This is the root of Finding 3.

**Owner-ruling chain — clean.** `goal.md:19` § Question is byte-identical to Ruling 3 in
`briefs/implement_resume_gate_a.md:35-36`, graded `[OWNER 2026-08-28]`, and the ruling's commit
`c8362239` precedes the session-02 brief that carried it in. Gates (a)–(c) from `align.md` were
each held by the owner, not decided by an agent: gate (a) is Ruling 3, gate (b) is unopened (no
`work/` mutation exists on disk), gate (c) is unexercised (the goal is not closed). The
grounding session's own `[AGENT]` grading is scrupulous — `goal.md:5` states explicitly that
nothing the operator said is `[OWNER]`, and § Close rule at `:164` self-identifies as the
operator's, not the owner's.

**Append-only discipline — holds across the trail.** The only removed lines anywhere under
`work/orchestration/goals/p-pump-basis/` across all 43 commits are template placeholder lines
being replaced at first fill. No trail entry was edited after the fact. The one correction to a
closed entry is `trail.md:543`, a proper `### Amendment` written by the reviewer session in its
own commit `104a68b5` — the runbook's prescribed shape, and the reviewer's own pen rather than
the operator's.

### Code integrity

No code. The item's whole diff is prose plus two data rows.

**Hardening verdict — survives a wider sweep than the record ran.** The plan's Invariant 10 greps
only `-- $ITEM`, which excludes the goal directory the round actually wrote. I ran the keyword
sweep over `work/`, `exploration/` and `CURRENT_WORK.md` as well: three hits, all prose — "not
reconciled inside this goal" and two uses of "digest" in the sense of ADR-006's `path@sha`
citation convention, which predates this item. I then read the full diff. **There is no
mechanism.** Nothing promoted, and the verdict holds under a check stricter than the one that
produced it.

**Finding 4 — the record's Invariant 10 output line misdescribes where the hits are.**
`verification_record.md:45` says "hits only in prose quoting the rule (spec, review, ADR list)."
Counting added lines per file, there are 55 hits and **38 of them are in session transcripts**
(03, 04, 08, 01 lead), not in the three artifacts named. They are benign — agents reading and
discussing the epic's hardening rule — but the record names a hit set narrower than the one its
own command returns, so an auditor re-running it gets a different answer than the row predicts.
**Fix:** say "spec, design, review, plan, and the session transcripts that read the rule," or
paste the per-file count.

**Finding 5 — a check-scope gap, no violation behind it.** Invariant 10 as written cannot see the
goal directory. I closed the gap myself and it is clean, so nothing is owed on this run. But the
check should be scoped `$BASE..HEAD` with no path filter for the next item that uses it, or its
row should state the scope limit.

---

## The ninth failure

The brief asked whether § Failures' eight entries are all of them. They are not. The strongest
candidate, and the one I would number ninth, is a defect of exactly the class the round's own
reviewer caught:

**Finding 3 — a load-bearing citation in the verification record does not resolve at the sha it
names.** `verification_record.md:14` settles criterion 3 on `covering-branches.md:32@e02ce403`,
quoting the branch as "The repository answers it." At `e02ce403`, **line 32 is the
`OPERATOR_QUEUE` row**. The `COMPLETE` branch is at line 36 of that blob and its wording is "No
prerequisite (T-001 returns `COMPLETE`)". The line/sha pair the record offers as proof of the
honest-outcome test points at the wrong row of the right table. `:80` repeats the composite
claim without the line number and is fine.

Why this is the ninth entry and not a typo. § Failures 8 records precisely this — a citation off
by two lines, load-bearing, repeated unchecked by both checkpoints, caught only by a fresh
reader. The record then commits the same error in its own single most important citation: the one
an auditor opens first to check that the outcome was declared before the run. **The substance
survives** — I opened the blob and the branch was declared, with the same covers set — which is
why this is a finding and not a failed criterion. But the record's own § Failures 8 argues that
"the conclusion is unaffected" is not a reason to leave a citation wrong.

**Fix:** cite `covering-branches.md:36@e02ce403` for the declaration and `:32@HEAD` for the
current wording, and add a § Failures 9 recording that the pattern recurred inside the record
itself.

**Two smaller items that belong with it:**

- **`freshness-record.md:26` says "twelve session entries" and then enumerates nine** (01, 02,
  03, 04, 04b, 05, 07, 08 kept, plus 05a never-run). The table has nine rows. `verification_record.md:36`
  independently says eight sessions plus 05a. The commit message at `6f1f5d70` repeats "twelve."
  A completeness statement whose own count is wrong is the one sentence in that file that has to
  be right.
- **`verification_record.md:88` and `plan.md:1138` cite "spec review A9"** for the product-lens
  obligation. `spec-review.md` contains no "A9" — zero occurrences, and it uses no A-prefixed
  labels at all. The finding is **L1-5** (`spec-review.md:30`, carried at `:86` item 7).

---

## Certification

**What I verified myself, not from the record:** all nine criterion rows against disk; both
ancestry predicates re-run; all ten invariant checks re-run, with the Invariant 2 fence sweep
executed over all eight transcripts (174 tool calls, all CLEAN); `source_registry.py verify`
(0 faults, 3 legacy); `tests/study/test_records.py` (7 passed); `tests/study` (261 passed, 84
skipped) — every figure matching the record to the digit; the `covering-branches.md` blob at
`e02ce403` read directly; the owner-ruling commits opened and compared verbatim against
`goal.md`; the whole item diff read for hardening mechanism plus an extended sweep beyond the
item directory; append-only discipline checked by removed-line scan across all 43 commits;
`p_pump` confirmed unchanged in both model homes; working tree confirmed clean.

**Verdict: POSITIVE.** The proof stands. The record's claims are honest, its evidence resolves,
its declared branch predates its outcome, and its hardening verdict survives a stricter check
than the one that produced it. The five findings are record-quality defects in artifacts the item
presents as settled. Findings 3 (with its two companions) and 1–2 should be repaired before
close, because they are cheap and because a proof item's records are its whole deliverable.
Findings 4–5 can be repaired in the record or carried as notes to the next item that reuses the
battery.

**This audit does not clear the product-lens gate.** `product-lens.md` does not exist. Under the
audit command's own rule, item certification at close requires that ledger entry; it remains
owed, as `verification_record.md:87` already says.

**Not checked:**

- **The product lens was not run.** No ledger entry was produced or appended, so no product-lens
  BLOCK/CLEAR/DISPOSED disposition exists for this item. The Product Judgment above is my own,
  derived from the spec, the epic's Item 5 framing, and the durable records — it is not a
  substitute for the lens.
- **The domain substance of the round's answer.** I did not re-derive the power balance, the
  4–6 % range, the ~130–195 MW figures, the nine cost accounts, or the ARIES-ACT divertor-relative
  reading. The fresh reviewer recomputed all of it independently (`trail.md:465-494`); I audited
  the record of that work, not the physics.
- **Session transcript content.** I swept all eight for fence violations against tool-call inputs
  and read `meta.md` for identity. I did not read the transcripts end to end, so I cannot say
  whether a session reasoned its way somewhere the briefs did not authorize by means other than a
  tool call.
- **The epic-level assembly.** This is a work-item audit. Whether Items 1–5 together discharge the
  epic's intent — in particular, that the `research` seam is still unproven after an item named
  for it — is an epic-scope question and is not settled here.
- **`close` and `pre_pr`, and the three goal-close rulings** in `### Round 1 review`, plus the two
  `goal.md` § Amendments the review recommends. All owner-held and outside this audit by the
  brief's terms.
- **Whether § Failures is now complete.** I found a ninth and two companions. Criterion 8 is
  written as a positive obligation — the record exists and its entries resolve — and I verified it
  on those terms. Neither the record nor this audit can claim nothing went unrecorded.
