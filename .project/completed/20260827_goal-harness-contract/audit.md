# Audit: Lean Goal Contract and Operator Runbook

**Verdict:** Needs Work — two cheap prose/frontmatter defects, on an otherwise strong build
**Audited:** 2026-08-25
**Branch:** `feat/run-study-first-consumer`
**Commit:** `21c46dc5` (audit brief at `687b617d`)
**Auditor:** fresh session; did not implement this item

---

## The Point

The approved concept-design defines a goal layer above the native workflows — a grounded question, one revisable strategy, one bounded task at a time, a round that ends in a mandatory result and a review by a fresh agent who did not do the work. None of it existed on disk. The rulings that shape it lived only in shaping files, the repository had no home where an architecture decision belongs, one ruling actively contradicted live project guidance (`CLAUDE.md:73`), and five textual homes still said the study executor was the sole writer of the discovery log — with twenty-two rows sitting in that log, six `unrouted`, and no consumer.

The bar is the owner's, stated verbatim: "I just want really good documentation and clean patterns so that it can be easily operated and managed by a human," operable by someone who "shouldn't have to be me (who built this and therefore is mostly familiar)." Every downstream epic item — the cold-grounding proof, the resume proof, the closure proof — reads this item's contract as its input. Until the contract is written down, nothing after it can be tested.

## Summary

The build is substantially complete and unusually well made. All seven phases landed, all six spec success criteria are met on their own terms, the 256-test suite is green, the six amendment edits reach all five homes, the append-as-update guarantee is now a real test rather than a docstring, and `GOAL_RUNBOOK.md` reads at the referent's bar. Provenance was preserved faithfully — grades are copied verbatim from the design's Recorded Rulings table, the mixed-grade records write the split, and nothing was invented.

Two defects control the verdict, and both are prose-sized. **ADR-005's frontmatter and index row grade an owner-originated decision as agent-grade**, telling a scanning reader to re-derive an owner ruling — the exact failure the register's own README and ADR-007 name. **"Fresh" is the load-bearing word of two gates and the contract never says what an agent does when it needs a fresh reviewer and cannot delegate** — the owner's criterion is "the critic is never the author's session," which is stronger than the runbook's "did not do the work." Neither defect invalidates anything built. Both are fixable in under an hour.

## Product Judgment

**Is this the right piece of work?** Yes, and it is built at the right altitude. The item produces exactly what the epic said it should — records, conventions, documentation, templates, and consistency tests — and nothing more. No executable goal-agent code, no hardening machinery, no mirrored PM state. The reverse check found no orphan scope.

**Product-lens ledger gate: BLOCKED** (`audit-F1`, `audit-F2`), appended at `.project/active/goal-harness-contract/product-lens.md`. The six prior blocks in that ledger are all resolved by citation (spec-F1/F2/F3, design-F1/F2/F3/F4 → `Gate: CLEAR` at the spec and design revision hops). The epic's own Product-Lens gate reads CLEAR and is unaffected. This audit-hop block is the only live one.

Both blocked findings were verified independently against the sources rather than taken on the lens's word:

- **`audit-F1` is confirmed.** `.project/adr/005-review-topology.md:5` reads `grade: "[AGENT] inference; owner may override"` and `INDEX.md:11` renders the same, while the record's own § Decision at `:20` carries a second, explicitly `[OWNER 2026-08-25]` decision — the pre-execution checkpoint placement. The register's README states the rule it breaks: "Write the split; do not round it to the stronger half" (`README.md:45`) — and this rounds to the *weaker* half, the direction that loses owner authority. ADR-004 and ADR-007 both carry splits; ADR-007's own § Rationale names this failure by name. The implement stage recorded the choice honestly as a Phase 1 deviation (`plan.md:577`), reasoning that the frontmatter should stay the copied grade. That reasoning was right for the topology half and predates the owner half being added to the body; it was not re-checked afterward. **This is a capture-fidelity rule 1 violation** (preserve the grade across every hop) on the two surfaces built for scanning.

- **`audit-F2` is confirmed, and its stronger half is the owner's own words.** `.project/concepts/goal-driven-model-development-harness.md:47` (`[OWNER]`, SC 5) reads "The critic is never the author's session." `GOAL_RUNBOOK.md` says only "a fresh agent who did not do the work" (`:11`, `:113`, `:129`). Those are not the same rule — the owner's names a session boundary, the runbook's names a work boundary, and an agent can satisfy the second while violating the first. Worse, the runbook's instruction at `:113` is "**hand** the reading and its proposed dispositions to a fresh agent," and `SKILL.md:12` gives the round agent `allowed-tools: Bash, Read, Write, Edit, Glob, Grep` — no delegation. So a goal agent that reaches the owner's own checkpoint gate has no defined next move, and no document supplies the prose alternative (a recorded stop that hands back to the operator). `SKILL.md:28-30` further tells the reader "The runbook says what 'fresh' means at each place it matters," which overstates what the runbook actually says. The builder knows to open a second session; that is precisely the operator the owner said this must not require.

No structural smell from the rubric fired. The writer-ownership change moves an invariant, but it does so across six edits, an ADR, and a test rather than silently; and the goal round writing into the study producer's log is the owner's own ruling with the producer's contract amended to match, not a consumer compensating around a producer guarantee. The lens recorded four lower-severity smells, dispositioned under § Code integrity below.

**Neither block is a rethink.** They are a frontmatter line plus an index cell, and two or three sentences of runbook prose. The work itself is sound.

## Findings

### Plan completion

All seven phases verified complete against reality. 73 of 74 checkboxes marked; the artifacts they claim exist, exist, and are not stubs.

- **The one unchecked box is resolved.** `plan.md:237` ("Confirm `SKILL.md` states no rule the runbook owns") stayed unchecked because Phase 7's manual check found a defect and staged rather than applied the fix. The fix landed in `21c46dc5`: the staged edit at `staging/skill-edit-1.md` matches the live file exactly (`diff` clean apart from the intended two-line replacement), and the duplicated sentence "An agent never fills two of these roles for the same round" is gone. **Verified and now marked.**
- **The staging content was applied faithfully.** `staging/dot-claude/skills/run-goal/SKILL.md` differs from `.claude/skills/run-goal/SKILL.md` only at line 28, by exactly the replacement `staging/skill-edit-1.md` specifies. The runbook edits 1–4 described in `staging/runbook-edits-1-4.md` match the committed diff. Nothing was dropped or paraphrased in the slicing.
- **The claim attached to that fix is inaccurate, though.** `plan.md:685` and `staging/skill-edit-1.md` both say the removed sentence "is the only such sentence in the file." It is not. `SKILL.md:42` restates `GOAL_RUNBOOK.md:72` nearly verbatim (how to tell whether a round is open), and `SKILL.md:46` restates `GOAL_RUNBOOK.md:35` ("the headings are the contract"). The manual check that produced the claim was `grep -nE 'must|never|always|at most|only when'`, which cannot see restatements phrased as description. Low severity — both duplicated rules are correct and neither is likely to drift — but the check is weaker than the claim it supports.
- No placeholder code, no TODOs, no stubs found in any deliverable.

### Spec conformance

| SC | Status | Evidence |
|---|---|---|
| SC1 — decisions live, provenance-graded, cited | **Met with a defect** | Seven records at `.project/adr/`, grades copied verbatim from `goal-strategy-task-harness-design.md:221-227` (checked row by row; all seven match, including the three split grades). `GOAL_RUNBOOK.md:240-246` cites all seven by relative path, all resolving from `work/orchestration/`. `CLAUDE.md:73-75` and `006-goal-evidence-seam.md:42` cite each other. **But `audit-F1`:** ADR-005's frontmatter and index row are not provenance-graded correctly. Checkbox left unmarked. |
| SC2 — three lean files sufficient to derive goal state | **Met** | `goal.md` ten headings in fixed order; `trail.md` eight entry headings in occurrence order with the two rules a writer breaks first stated in place; `learnings.md` five-field entry shape. "Is round N open?" is answerable from headings alone (`GOAL_RUNBOOK.md:72`), with nothing maintained. Three heading tests guard the order. |
| SC3 — checkpoint and `RoundReview` distinct in timing and responsibility | **Met** | `GOAL_RUNBOOK.md:150-161` — one table, six rows, differing in *when*, *over what*, *asks*, *reviewer*, *on failure*, and *loops?*. ADR-005:22 states the same distinction. The cap is present and stops work rather than releasing it (`:121`, `:195`). |
| SC4 — five homes agree on writer ownership and joined rows | **Met** | Read all five independently. `runbook.md:221-224` (sole writer scoped to first sightings), `:273-275` (the goal append is not an administrator act), `:295-306` (one row per finding *sighting*, plus the positional-kind and newest-row-wins reading rule), `DISCOVERY_LOG.md:3` (writer rule, cardinality rule, and the corrected authority citation — it had wrongly cited `runbook.md § DISCOVERY_LOG.md`, which carries no writer rule; now cites step 14). Six parametrized cases guard them with negative lookaheads rather than bare substrings. |
| SC5 — one document for human and agent alike | **Met with a defect** | No section forks by operator kind; the skill is a door, not a second copy. **But `audit-F2`:** the shared document leaves the agent path undefined at the checkpoint gate. Checkbox marked — the criterion as written ("describes the same artifacts, gates, returns, and reviews") is satisfied; the gap is that one gate is under-described for both paths, which the Product Judgment carries. |
| SC6 — tests pass; no hardening mechanism | **Met** | `uv run python -m pytest tests/study tests/orchestration -q` → **256 passed, 43 skipped**, run by this audit. § Non-Goals walked item by item: no envelope files, no event ledger, no authority digests, no idempotency keys, no effect queries, no reconciliation, no denser per-stage events, no concurrent runs, no unattended dispatch, no stale-authority guard. The runbook's only mention of that machinery is the sentence declaring it absent and on the hardening path (`:20`, `:173`). No executable goal-agent code. Nothing touched under `scripts/zotero_*`, research surfaces, or `knowledge/` (verified by `git diff --name-only` across all seven commits — empty). |

**Tagged requirements.** The `[HARD]` requirement (`spec.md:88`) — that the accidental set-comparison pass becomes a stated guarantee — is met and is the strongest single piece of work in the item. `_ids_in_record` and `_ids_in_log` are extracted to module level, the real test calls them unchanged, the fixture test uses the same helpers rather than a second parser, and the docstrings say plainly that returning a set is load-bearing. The recorded red-check found it turns **three** tests red, not one, because the live records already exercise the multiplicity.

**Non-goals respected.** Nothing out of scope was built.

### Design conformance

Implementation follows design rev 2. Components are where the design placed them; invariants I1–I15 have homes; the three caps (2 / 2 / 6) are the design's numbers, restated in the goal template so nothing is inherited silently.

- **The one design deviation is recorded honestly and is the better reading.** `plan.md:661` — the design's test-5 sentence asked that the runbook *and the three templates* carry I6's and I13's sentences; the implementation asserts them on the runbook only and applies the no-crossing scan to all four. Requiring one rule in four homes is the duplication the design otherwise forbids. Agreed.
- **The `005` deviation is recorded but wrong on its merits.** `plan.md:577` explains why the frontmatter grade stayed `[AGENT]`. The record's *body* correctly carries the owner half with its own grade and source, so nothing was invented — but the frontmatter and index are the scanning surfaces, and they now under-grade. This is `audit-F1`.
- The "five surfaces" table omitting the `run-goal` skill is **not** a deviation: `design.md:156` specifies that table, and D7 frames the skill as a door rather than a surface.

### Code integrity

No slop and no failure-honesty problems. The tests are the only code, and they are careful: every assertion carries a comment naming the obligation it guards, the absent-clause checks use negative lookaheads (because "one row per finding" is a prefix of its own replacement and a substring check would pass forever), and three mutation checks were run and reverted — a reword noise check, an injected barred instruction, and the restored retired clause. `adr.sh` is small, `set -euo pipefail`, and fails loudly on a missing index table rather than silently appending.

Four lower-severity smells, all confirmed:

- **Two dead cross-references inside the register's own § Affected seams.** `.project/adr/002-round-boundary.md:32` and `.project/adr/005-review-topology.md:40` both cite `GOAL_RUNBOOK.md` "§ The fresh `RoundReview`". The section is called "The fresh review." Affected seams is the list someone edits against, so a dead pointer there costs more than it looks. Should change to the live heading.
- **`adr.sh new` defaults to the weaker grade.** `.project/scripts/adr.sh:28` hardcodes `` `[AGENT]` `` in the minted index row and `template.md:5` does the same. `README.md:57` says to fill the grade in by hand, but the default sits on the path of least resistance in the direction that loses owner authority — and the register's very first owner-graded record already came out under-graded. Should default to a placeholder that cannot be left as-is (`[GRADE]`, or `<copy from source>`).
- **`ADR-00X` already means something else in committed modeling artifacts.** `work/completed/20260303_WI-008_hif-concept-instantiation/design.md:49-107` uses "ADR-002" for a modeling calc-placement decision (`AD-002`). The README's prior-art paragraph handles the `exploration/phase_1a/ADR-001` stray but not this looser usage, so "ADR-002" now resolves to two decisions depending on which directory the reader came from. Should get one sentence in the prior-art paragraph.
- **The register is invisible from the two files that route readers to homes** (`audit-F3`, NOTE). `CLAUDE.md` § Project Structure lists `.project/` as active / backlog / completed / EPIC_GUIDE / epic_template with no `adr/`, and `modeling_project/ARCHITECTURE.md` never mentions `.project/adr/` at all — so the `ADR-NNN` vs `AD-XXX` split is asserted only in the file a modeling agent does not read. Mitigating: the `CLAUDE.md` tree already omitted `.project/concepts/` and `.project/research/` before this item. One line in each file.

**Auto-memory check.** No previously rejected pattern appears. In particular `feedback_no_fallbacks` holds — the runbook offers no default or family-average anywhere; where evidence is missing it says "unpinned; no native digest" rather than inventing one.

---

## Item 6 non-interference — clean

Verified independently, because the two items share `runbook.md`:

- **The four pending sentences' homes are untouched.** The item's runbook diff is 14 insertions and 5 deletions, confined to step 14 (`:221-224`), the administrator paragraph (`:273-275`), and § `DISCOVERY_LOG.md` (`:295-306`). Steps 5, 6, 7, and 9 and the study-definition convention are byte-identical. Disjoint — the collision stop correctly did not fire.
- **The discovery log lost no rows.** 22 finding rows before `007d9488^` and 22 now; only line 3 changed. (The plan's "24, unchanged" and the audit brief's "24 rows" are both counting `grep -c '^|'`, which includes the header and separator lines. Same file, two counting conventions — no discrepancy.) Six columns in order in both schema tables.
- `tests/study` green: 232 passed, 43 skipped, within the 256 total.

## Deviations — all recorded honestly, none hiding a gap

| Deviation | Recorded at | Assessment |
|---|---|---|
| Test-5 scope narrowed from design to plan stencil | `plan.md:661` | Honest, reasoned, and the better reading. No gap. |
| Skill de-duplication found late, staged not applied | `plan.md:685` | Honest about severity and about leaving the box unchecked. The fix landed faithfully. The attached claim "the only such sentence" is over-stated (see Plan completion) — an over-claim, not a hidden gap. |
| Commit slicing by the orchestrator after the permission wall | `plan.md:609`, `:628`, `:644` | Fully disclosed, including which commits are whose. Staging matches disk exactly. No gap. |
| ADR-005 records the checkpoint beyond the Recorded Rulings row | `plan.md:577` | The addition itself is right — filing the topology without the checkpoint would contradict the runbook. The frontmatter grade that came with it is `audit-F1`. |
| `test_register_is_coherent` globs and filters instead of the stencil's glob | `plan.md:577` | Trivial, and the explicit filter is more readable. No gap. |

## The runbook at the owner's bar — cold read

Read `GOAL_RUNBOOK.md` end to end as a non-builder against `work/orchestration/handshake-lcoe-construction.md`. **It holds.** Every procedural section answers what to do, what to write, where it goes, and who checks it; the vocabularies are fixed and used exactly; rules are cited to their record rather than restated; there is no hedging. Grounding a goal and running a round are both followable from this file alone.

Four things a stranger stumbles on, ranked. The first is `audit-F2` and is a defect; the rest become Item 4 pre-reads unless Item 4 finds them worse than they look.

1. **No path to the study runbook.** § The native seams tells an operator to invoke `study.execute` with "pin, question, protocol rulings" and `study.read` with "committed record only", and gives no path to `.claude/skills/run-study/runbook.md`. The document says "the study runbook" once, in prose, at `:13`, unpathed. This is the one cross-layer document a goal operator needs most, and the runbook cites the ADRs, the templates, and WI-031 by path but not this. **Moderate** — cheap to fix, one path.
2. **"Pin" is never defined.** Used as the round's central bound at `:55` ("at most one promoted pin"), again at `:197`, `:223`, `:224`, and in the `goal.md` template's § Invariants. A non-builder cannot tell what a pin is or what promoting one means, and the round bound is stated in terms of it. **Moderate** — a one-line gloss plus a pointer to where the study layer defines it.
3. **"The current manual integration pattern" has no path.** `:230` names it as the interim hand pattern for the `integrate` seam. The `research` seam next to it cites WI-031 by full path; this one cites nothing, and no such document exists in the repo. A stranger told to use a pattern they cannot find will improvise, which is exactly the silent absorption the same paragraph forbids. **Moderate** — either a path, or an explicit "there is no written pattern; this is a `PREREQUISITE` return until Item 3."
4. **No worked example anywhere.** The referent is a run record and this is a procedure, so the genre difference is real and was reasoned about. Still, the templates plus the runbook give a stranger no filled-in round to read. **Low** — Item 4's own output becomes that example, which may be the right sequencing.

---

## Certification

**Not certified.** The product-lens ledger gate is BLOCKED on `audit-F1` and `audit-F2`, both verified independently against their sources. Under the audit contract an unresolved owner/`[HARD]` contradiction forbids Certify regardless of the rubric, and `audit-F1` is a capture-fidelity violation on an owner-originated decision while `audit-F2` leaves an owner-named gate without a defined move on the agent path.

**Gaps ranked by severity:**

1. **`audit-F2` — the agent path has no move at the checkpoint gate** (`GOAL_RUNBOOK.md:113`, `SKILL.md:12`, `:28-30`). Prose fix only, no dispatch: define "fresh" once against the owner's wording (`.project/concepts/goal-driven-model-development-harness.md:47` — "The critic is never the author's session"), say per gate who obtains the reviewer on each path, and give the agent path its recorded stop that hands back to the operator when it cannot. Then either back `SKILL.md:28-30`'s claim or delete it. Building a way to *start* a session is dispatch and stays barred by ADR-003.
2. **`audit-F1` — ADR-005 under-grades an owner decision** (`.project/adr/005-review-topology.md:5`, `INDEX.md:11`). Two lines: `grade: "[AGENT] review topology, owner may override; [OWNER] 2026-08-25 pre-execution checkpoint"`, and the matching index cell. The body already says it.
3. **Three uncited pointers in the runbook** — the study runbook path, the "pin" gloss, the manual integration pattern (§ cold read, items 1–3).
4. **Two dead § Affected seams cross-references** — `002-round-boundary.md:32` and `005-review-topology.md:40` cite a heading that does not exist.
5. **`adr.sh` and `template.md` default to `[AGENT]`** — flip the default to a placeholder that cannot be left as-is.
6. **`audit-F3` — the register is unlisted in `CLAUDE.md`'s tree and unmentioned in `modeling_project/ARCHITECTURE.md`.** One line each.
7. **`SKILL.md:42` and `:46` still restate runbook rules**, and `plan.md:685`'s "only such sentence" claim does not hold. Lowest severity; both restatements are correct as written.

**What I marked:** spec success criteria SC2–SC6 checked (verified independently, each to a named artifact or test). SC1 left unchecked pending `audit-F1`. `plan.md:237` checked — the underlying fix landed and was verified against staging. The epic item heading is **not** marked ✅ and its success checkboxes are left as-is; the epic's own Product-Lens gate is unaffected and still reads CLEAR.

**Not checked:**

- **Runtime behaviour of anything.** Every test in this item checks documents. Whether a goal agent actually appends a legal disposition row, actually stops at the cap, or actually refrains from comparing a digest is unverified here and unverifiable by these tests — Item 4 and Item 5 are the proofs, and the implementation says so plainly rather than claiming otherwise.
- **Whether a real stranger can operate the runbook.** I read it cold as a non-builder, but I read it with the spec, design, and concept files already in context. Item 4's cold-grounding proof is the real test. Per `design.md#potential-risks` and `plan.md:503`, any finding Item 4 raises against the runbook is an **Item 1 defect**, not an Item 4 one.
- **`tests/models`.** Needs the SYSIDE environment and is not touched by this item; not run.
- **The ADR bodies' claims against their upstream reviews line by line.** I verified all seven *grades* against `goal-strategy-task-harness-design.md:221-227`, read 003–007 in full, and spot-read 001–002's § Decision. I did not re-derive each record's Rationale and Rejected alternatives against the two design-review files.
- **Item 2's parallel worktree.** Whether the research-seam item has filed into this register, and whether its records collide with `001-007`, was not checked.
- **`adr.sh supersede` end to end.** The implement stage exercised and reverted it; I did not re-run it.
