# Design Review: Lean Goal Contract and Operator Runbook

**Design:** `.project/active/goal-harness-contract/design.md`
**Spec:** `.project/active/goal-harness-contract/spec.md`
**Review File:** `.project/active/goal-harness-contract/design-review.md`
**Date:** 2026-08-25
**Reviewer:** fresh session; did not author the design

---

## The Point

Item 1 puts the goal layer on disk so someone who did not build it can operate it. The owner's bar is verbatim: "I just want really good documentation and clean patterns so that it can be easily operated and managed by a human," run by an operator who "shouldn't have to be me (who built this and therefore is mostly familiar)" (`.project/concepts/goal-driven-model-development-harness.md` § Owner's Words). That ladders to the epic's critical success factor — a non-builder resumes and completes a real goal round from the goal directory and native records alone, every touched study finding dispositioned, no completed native work repeated.

Four obligations follow. Seven approved decisions become live records carrying their recorded grades, and the live guidance one of them contradicts (`CLAUDE.md:73`) is amended. Three lean files get conventions detailed enough that current goal state is derivable without mirroring native stage state. Five textual homes that forbid a goal round from appending a disposition row are amended so no touched finding returns `unrouted`. And one shared `GOAL_RUNBOOK.md` describes the same artifacts, gates, returns, and reviews for a human and an agent. All under the owner's lean-first rule: no hardening mechanism without a recorded observed failure of the prose-and-native-facts route.

Items 4–6 test exactly these documents. They are the reason a silent omission here is expensive.

---

## Fundamental Assessment

**Sound — with two omissions that must be closed before implementation.**

This is the right piece of work and the right approach. "Documents with fixed shapes, not a program" is the correct read of the lean-first ruling, and the design carries it consistently: the contract is enforced by heading shape, replay comes from git plus native artifacts, and the only genuinely new surface (the ADR register) is new because nothing occupies that slot. I looked hard for a control-plane mechanism entering by the back door and did not find one. Neither structural smell fires: the writer-ownership change moves an invariant, but it says so loudly across six edits, an ADR, and a test, rather than silently.

I verified the two claims the brief said to verify rather than take:

- **`adr.sh` stays inside the boundary.** It mints an id, copies a template, appends an index row. It touches nothing in the goal loop and decides no authority question. It is a filing helper for a document register, not goal-agent machinery. D4's scope addition past the spec's `[INFERRED]` deliverable list is legitimate — it re-derives against the epic's own Current State, and I confirmed the wording: "no project ADR directory **or filing mechanism** exists yet" (`epic_goal_strategy_task_harness.md:111`). The design records the addition in the open rather than burying it.
- **D8's digest re-derivation holds, for tracked artifacts.** The function-based split is real: a citation digest is read by a person; the barred digest is compared by a procedure to decide whether work is still authorized. I6 makes the boundary a stated rule. For repository-tracked evidence there is no genuine collision and nothing needed parking. See M2 for the evidence class the mechanism does not cover.

What is wrong is narrower and specific: two `[INHERITED]` spec requirements have no design home at all, and one of them — external mutation voiding task authority — is the single place where the hardening boundary and the contract genuinely rub. That is the case the spec attached a surfacing duty to, and the design neither designs it nor surfaces it.

Verdict is **Revise**, not Rework. The foundation is right; the gaps are additive.

---

## Dimensional Review

### 1. Spec Compliance
**Assessment:** Concerns

I walked every `[NEED]` / `[HARD]` / `[INHERITED]` item in the spec against the design. Most land cleanly, including the ones that are easy to lose: the checkpoint's cap **and** its owner-visible stop ("Hitting the checkpoint cap does not permit execution" — § Default limits), the post-execution audit obligation placed inside `RoundReview`, the owner's "path and digest" term surviving into edit 6, the seven grades copied per-record rather than flattened, and the five-home amendment reaching all five.

Two silent omissions (C1, C2 below) and four dropped clauses (n2).

Provenance handling is faithful in the direction that matters most. The design treats the `[INFERRED]` digest reconciliation as challengeable-by-re-derivation and re-derives it (D8) rather than inheriting it as settled — correct under the settled rule. The `[REFERENT]` bar is carried at its stated force: § Research Findings analyzes the referent's actual shape (49 unwrapped lines, graded input bullets, dated stage log) and Implementation Notes binds the runbook to it. Neither hardened into a required form nor softened into a vibe.

Spec Open Questions: all eight are settled. The weakest is "what a revision iteration looks like" (n5).

### 2. Pattern Consistency
**Assessment:** Concerns

The design composes with what exists rather than paralleling it: `run-study` keeps the study contract, both PM systems keep their operations, `pytest` under `tests/` keeps drift detection in the same doc-consistency style as `test_no_retired_identifiers.py` and `test_record_template.py` (both verified present). D6's reasoning — a human copying a template should copy a file, and should not reach into `.claude/` for their own working files — is right.

But two of the design's statements about the repo's own conventions are false, and one of them is a decision's stated rejection reason (M3).

### 3. Abstraction Quality
**Assessment:** Pass

Five surfaces, one question each, joined only by citation. Nothing here is a wrapper. The one thing I pushed on — whether `.project/adr/` earns a fourth register — survives: `modeling_project/ARCHITECTURE.md:3` states its own charter as model-package decomposition, and I confirmed AD-001 through AD-007 are all live in that file and are all SysML typing, library layout, and calc-def shape. Extending it would have put orchestration decisions under a modeling charter on the wrong side of CLAUDE.md's two-system rule. D1 is correct, and D3's handling of the stray `exploration/phase_1a/ADR-001_csv-source-of-truth.md` (named in the index as prior art, not renumbered) is the cheap right answer.

D5's sequencing is real, not ceremonial: align ruling 3 has Item 2 filing into this home "once it exists," Item 2 is running now, and a partial register would make Item 2 file against a convention that then changes.

### 4. Duplication Avoidance
**Assessment:** Pass

D9 splits the tests by subject specifically to avoid a second parser of the discovery-log table — the right instinct, and the reason given is the drift the tests exist to catch. "The runbook cites; it does not restate" is stated and consistently applied (the ADR records hold the reasons; the runbook names them).

### 5. Data Structure Clarity
**Assessment:** Concerns

The trail entry shapes are explicit and countable, which is what makes a fresh reader able to tell a complete entry from a partial one. Good.

The weak structure is the discovery log's row kind. I8 makes kind **positional** with no column marking it, and I9 forbids adding one because `tests/study/test_records.py:60` reads `Record` at index 3 (verified: `line.split("|")[3]`, and index 3 is `Record` given the leading empty cell). Positional kind works — `<study-id>#<n>` ids are study-scoped, so a later first sighting under an existing id is impossible — but the invariant now lives in convention and reader discipline instead of in the schema, and the shipped tests check it only weakly (M5). Add to that the readability cost: a disposition row lands at the file end, dozens of rows from its sighting (n4).

### 6. Route Safety
**Assessment:** Pass

No routing surface in the usual sense. The analogue — who may write where — is explicit and closed: the goal round's only write outside its own directory is the joined disposition row, the administrator stays read-only, and edit 5 states all three writers in one sentence. No catch-all.

### 7. Bets & Decisions Integrity
**Assessment:** Concerns

B1–B4 are genuine claims about reality with stated failure consequences, and B1 is honest about the fact that being wrong is the designed route to the hardening path — at the cost of Items 4–6. That is the right way to state it. B3 is the load-bearing one and I agree it is likely true (see Fundamental Assessment).

**The hidden bet.** The design bets that a fresh reviewer, reading prose, will notice that a referenced native work item changed outside an active goal task — because nothing else can notice it, and the only mechanism that could is barred. That bet is never stated, because the requirement it belongs to (C1) was dropped.

**A decision resting on a false premise.** D7 rejects a slash command because "every file in `.claude/commands/` is an agentic-mbse symlink." It is not: `.claude/commands/manage-concept.md` is a real fusion-tea file. See M3.

### 8. Reader Comprehension
**Assessment:** Pass

§ Core Concept gives the mental model before any mechanism — documents with fixed shapes, enforced by shape not machinery, replayable because git plus native artifacts already carry history. A reader can skim this once and come away with the system, the bets, and the decisions. Terms are anchored where they are coined. The one place the prose runs ahead of the reader is § Section conventions' code block, which is dense — but it is a reference table, and that is the right form for it.

One internal inconsistency: § Core Concept says the item "amends five sentences" in `run-study`, while § Amendment text plan is six edits (five homes, six edits, one of which fixes an authority citation). Cosmetic, but it is the kind of number a reader anchors on.

---

## Issues by Severity

### Critical

- **C1 · "External mutation voids authority" has no design home — and its only mechanism is barred.** `spec.md:74` carries it as `[INHERITED]`: "If a referenced native work item changes outside an active goal task, the task loses authority; re-ground or close the round before more work." It appears nowhere in the design — not in I1–I12, not in the trail entry kinds, not in the runbook's section list, not in Non-Goals. This is not a clause dropped in passing. Noticing that a cited artifact changed since it was cited is *exactly* a stale-authority check, which § Non-Goals and I6 bar ("no goal procedure compares a cited digest"). So the design has an inherited requirement whose natural implementation is the mechanism it just outlawed, and it neither designs the prose alternative nor surfaces the tension. The spec attached an explicit surfacing duty to this seam and it went unexercised. **Fix:** give the requirement a prose home — a `RoundReview` check ("did any cited native artifact move outside its task?"), a runbook paragraph on re-grounding, and an invariant — or, if design concludes the prose route cannot carry it, surface the collision to the owner and park the dependent choice, exactly as `spec.md:42` instructs.

- **C2 · Round-closure conditions are never designed.** `spec.md:64` `[INHERITED]`: a round has at most one promoted pin and at most one committed study; a valid study reading — including adverse or inconclusive — closes it; it also closes on strategy blocker, changed comparison meaning, owner gate, declared limit, or answered goal, and may close with neither pin nor study. In the design, these appear only inside a table cell justifying why there is no task cap (`design.md:176`: "Already bounded by one pin, one study, and mandatory close after a valid reading"). § Component Overview lists a runbook section called "closing a round," but the design never says what closes one. SC2's bar is that a fresh reader can *derive current goal state* from the files — and "is this round still open?" is the first question they will ask. **Fix:** state the one-pin/one-study bound and the six close triggers as an invariant plus a runbook section, at the same grain the design gives the entry headings.

### Major

- **M1 · I6 is claimed testable and no test tests it.** § Validation's SC6 mapping reads "all tests green + § Non-Goals held, with I6 as the testable form of the hardening boundary," but none of `test_goal_contract.py`'s four tests touches I6. Either add an assertion (the runbook and templates contain no procedure comparing a cited digest — a phrase check at the same altitude as test 1) or drop "testable" and hold I6 in manual verification honestly.

- **M2 · `<path>@<commit-sha>` pins nothing for untracked evidence.** For tracked files a path plus a commit sha resolves to a unique blob, and D8's "zero new mechanism" claim holds. It does not hold for the evidence class the owner's "for mutable evidence, a digest" term most plausibly targets: study stores under `exploration/stellarator_e2e/studies/<id>/_work/` are gitignored (`run-study-first-consumer/plan.md:244`), and R2-synced research binaries are gitignored by design (`CLAUDE.md` § Research Artifact Sync). A goal round citing one of those writes a citation that pins nothing and silently looks identical to one that does. **Fix:** say which evidence classes the citation form covers and what an operator writes for the rest — naming the gap is enough; inventing a digest scheme for untracked files would cross the boundary.

- **M3 · D7's rejection reason is factually wrong, and so is the research finding behind it.** D7 rejects a slash command because "every file in `.claude/commands/` is an agentic-mbse symlink; a fusion-tea command there is tool-owned territory and gets clobbered." `.claude/commands/manage-concept.md` is a real 17 KB fusion-tea file sitting in that directory today. The same error appears at `design.md:42`: "every other entry in `.claude/skills/` is a symlink into `~/1cfe/agentic-mbse`" — `browser-inspect/`, `concept-research-navigation/`, and `html-explainer/` are all real local directories. The *conclusion* (a thin skill, matching the run-study precedent, one document two doors) survives on its other grounds and I would keep it. The stated reason has to change, because a design decision's recorded reasoning is what a future agent re-derives against.

- **M4 · The `[HARD]` constraint's second consequence has no operator-facing home.** `spec.md:90` names it: a goal-appended row whose `Record` cell cites an id **not** in that record's § 15 fails `test_findings_join_the_discovery_log` for that record. The design handles this only inside its own new test's assertion. Nothing in `GOAL_RUNBOOK.md`, the templates, or I7 tells an operator the rule: a goal round may append only under an id a committed record already carries, and a finding the goal round discovers itself is not a discovery-log row. I7 presupposes touched rows, so the case is undefined rather than forbidden — and Items 5 and 6 will hit it. **Fix:** one sentence in the runbook and a clause on I7 saying where a goal-originated finding goes instead.

- **M5 · The joined-row guarantee is documented, not enforced.** The spec's ask was that the set-comparison accident become a stated guarantee. The design's answer is a docstring correction plus four assertions, none of which fails if someone rewrites `in_log` from a set comprehension to a list — which is the exact edit that kills append-as-update. Two of the four assertions are also near-tautological ("the extra rows follow the first in file order," "none of them is the earliest row for that id"). **Fix:** assert the multiplicity intent directly — that an id carrying more than one row still joins, i.e. the record↔log join is over *distinct* ids by design and a duplicate row is legal — so a future "cleanup" of the comparison breaks a test rather than a comment.

- **M6 · Item 6's pending-sentence list is read loosely.** The design's disjointness conclusion is right, but the basis is shakier than stated. `#6`/`#10`/`#11` are study-scoped ids and **both** studies have a `#10`: study 2's is the preflight re-run with home runbook step 6 (`plan.md:335`), which is the one the design names; study 1's is the oracle-operands artifact, and `plan.md:309` says its "runbook sentence lands at Phase 4" too. So there may be four pending sentences, not three. Separately, Phase 4's own § Changes Required (`plan.md:224-227`) carries **no** runbook-sentence checkbox at all — the pending sentences exist only as Implementation-Notes prose, so no authoritative list exists to check against. None of this breaks disjointness (edits 1–4 touch step 14, the administrator section, and § `DISCOVERY_LOG.md`; the pending homes are steps 5/6/7/9 and the store convention). **Fix:** have the re-check instruction name the two-study id ambiguity, and check Phase 4's *notes*, not just its checklist.

### Minor

- **n1 · Test 1's absent-phrase check is a substring of its own replacement.** "One row per finding" is a prefix of "One row per finding sighting," so a naive must-be-absent assertion fails against the corrected text. The design's "as a bare phrase" hedge signals awareness but is not implementable as written. Needs a negative lookahead or a whole-clause match.
- **n2 · Four `[INHERITED]` clauses dropped.** `StrategyRevision` "contains no future task list" (`spec.md:59`); `PREREQUISITE` "is discovered as a return, never predicted in scope" (`:62`); the stop reason is "derived from the last outcome plus limits, not maintained as a second enum" (`:65`); `RoundReview` "never resumes the closed round" (`:66`). Each is one clause in a template or invariant. The third is load-bearing against exactly the kind of second-enum drift the lean rule exists to prevent.
- **n3 · D4's premise is unverifiable from here.** The claim that `/_my_design` instructs filing with `.project/scripts/adr.sh new <slug>` sits in a file outside this session's readable working directory, so I could not check it. Everything else supporting D4 does check out (`epic:111`'s "filing mechanism"; `.project/scripts/` holds only `get-metadata.sh`; `.project/adr/` is absent). Worth a second pair of eyes before shipping a script on that basis.
- **n4 · Append-as-update costs the log its scannability.** A disposition row lands at the file end, dozens of rows from its sighting, and the log is already 22 rows over two records. The runbook should tell a reader to scan for the id rather than trust the first row they hit.
- **n5 · "What a revision iteration looks like" is answered only by a counter.** Spec Open Question 8 asks for it; the design gives "revision N of 2" inside the checkpoint entry and stops. It does not say whether each submission appends a new `Checkpoint C-00N` entry or amends the existing one, which matters because I4 forbids editing entries in place.
- **n6 · Five sentences vs. six edits.** § Core Concept says "this item amends five sentences" in `run-study`; § Amendment text plan is six edits (four in `runbook.md`, one in the log header, one in CLAUDE.md). Five *homes*, six edits. Pick one number.

---

## What I checked

Live-tree verifications behind the findings above:

- `runbook.md:221` "The executor is the sole writer of the log." ✓ · `:270` "An administrator does not append to `DISCOVERY_LOG.md`" ✓ · `:290-292` "one row per finding, never a second copy of the finding's account" ✓ · `:294-296` six-column schema table, order `Date | Kind | Record | Finding | Disposition | Home` ✓ · `DISCOVERY_LOG.md:3` carries both the cardinality clause and the sole-writer clause, and mis-attributes the writer rule to `runbook.md § DISCOVERY_LOG.md` ✓ (edit 5's fix is correct) · `CLAUDE.md:73` "**CRITICAL: Do not cross-reference between them.**" followed by exactly the two sentences edit 6 preserves ✓
- `tests/study/test_records.py:60` reads `line.split("|")[3]` and index 3 is `Record` ✓ (I9 correct) · `:41` compares sets ✓ · the log is currently non-decreasing by `Date`, so the design's global newest-last assertion passes on today's file ✓
- `pyproject.toml` sets no `testpaths`, so a new `tests/orchestration/` is collected without config changes ✓ · `tests/study/test_no_retired_identifiers.py` and `test_record_template.py` exist and are the precedent the design claims ✓
- `.project/adr/` absent ✓ · `.project/scripts/` holds only `get-metadata.sh` ✓ · `exploration/phase_1a/ADR-001_csv-source-of-truth.md` exists ✓ · `modeling_project/ARCHITECTURE.md:3` charter quote exact, AD-001–AD-007 all live and all model-scoped ✓
- `work/orchestration/handshake-lcoe-construction.md` is 49 lines ✓ · epic `:111` "no project ADR directory or filing mechanism exists yet" ✓ · align ruling 3 (Item 2 files "once it exists") ✓
- `.claude/commands/manage-concept.md` is a regular file, not a symlink ✗ (M3) · `.claude/skills/browser-inspect`, `concept-research-navigation`, `html-explainer` are regular directories ✗ (M3)
- `run-study-first-consumer/plan.md:309` (study 1 `#10`, `#11`), `:323` (study 2 `#10`, `#6`), `:335` (`#10` home = runbook step 6), `:224-227` (Phase 4 checklist, no runbook sentences) — M6

**Process note.** The command's Stage 0 step 4 calls for spawning a subagent to run the product-lens. This session carries a standing instruction not to invoke the Agent tool unless the user asked for it, so I ran the lens myself against the same sources and appended the verdict block to `product-lens.md` in the ledger format. The result is one reviewer's lens rather than an independent one — worth knowing when weighing the gate.

---

## Recommendations

1. **Close C1.** Give "external mutation voids authority" a prose home, or surface the I6 collision to the owner and park it. This is the finding I would not ship without.
2. **Close C2.** State the round-closure rule and the one-pin/one-study bound where a fresh reader will find them.
3. **Fix M3's stated reasons** (keep both conclusions) and pick up n2's four dropped clauses — both are cheap and both protect future re-derivation.
4. **Decide M1 and M5 together**: what the tests actually guarantee versus what the design claims they guarantee. Either strengthen the assertions or soften the claims.
5. **M2 and M4** each need one sentence in `GOAL_RUNBOOK.md`, not new mechanism.
6. **M6**: sharpen the re-check instruction to name the two-study id ambiguity and to read Phase 4's notes, not just its checklist.

---

## Resolutions

[To be filled during Stage 4. One entry per resolved issue — this is what the design agent reads to incorporate the review.]

---

**Overall:** **Revise**

**Next Steps:** Record resolutions above, then re-run `/_my_design` (or return to the design-agent session) pointed at this review to incorporate. The reviewer does not edit the design.
