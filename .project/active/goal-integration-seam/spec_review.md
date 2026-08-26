# Spec Review: Verified Package Integration Seam (GSTH Item 3)

**Spec:** `.project/active/goal-integration-seam/spec.md`
**Contract:** `~/.claude/commands/_my_spec.md`
**Review File:** `.project/active/goal-integration-seam/spec_review.md`
**Date:** 2026-08-26
**Reviewer:** fresh stage session (did not author the spec)

---

## Reality Check

**Sound.** The spec is about the right work item, the Problem section frames the real gap (a proven sequence that lives in two plans and is not callable), and the two-return-class contract is a faithful and useful sharpening of epic Item 3's Objective. Requirements A–G map cleanly onto epic Scope 1–4, Out of Scope, and Deliverables, with no orphan requirement and nothing from the hardening-path prohibition sneaking in. Design would not be pointed at the wrong thing.

It would, however, be pointed at three things that are not true or not decidable. All three sit inside R-B1 / R-D1 — the requirements the spec itself grades `[HARD]` and calls "the contract."

---

## Audit

### Lens 1 — Faithfulness

**L1-1 · Direct claim (must-fix):** R-B1 gate 1 says the toolchain pin check verifies that "the installed sysml-codegen **and teax** revisions are the pinned ones," and names `tests/test_dependency_provenance.py` as the producer. That test does not check teax. It pins three packages — `agentic-mbse`, `sysml-codegen`, `1costingfe` — via `pyproject.toml`/lock assertions and installed `__version__` reads (`tests/test_dependency_provenance.py:18-28,54-100`). Teax is not a pinned dependency at all; it is a working checkout reached through the `STOP_PARSER_TEAX_ROOT` env var, and nothing in `tests/` or `scripts/study/` asserts its git revision. The only teax pin check that has ever run is a hand-typed line in the migration plan's environment block: `git -C "$STOP_PARSER_TEAX_ROOT" rev-parse --short HEAD → 744745f, or stop` (`.project/completed/20260821_stellarator-model-migration/plan.md:47`). The gap is corroborated from the other side by the defect the spec itself cites: `verify.py:456` falls back to `"unrecorded"` precisely because stock teax exposes no `__version__` (`DISCOVERY_LOG.md` `20260821-power-cycle-ab#8`).

This is load-bearing twice over. R-B1 forbids reimplementing a gate and R-B2 forbids editing `scripts/study/` — so a design agent that reads R-B1.1 literally, goes looking for the teax half in the named producer, and does not find it has no legal move. It will either drop half of gate 1 silently or write a new check and break R-B1. R-C2 ("an installed toolchain revision differs from its pin") rests on the same false premise. The spec needs to say plainly which producer owns the teax revision check, or record that none exists and say what the seam does about it.

**L1-2 · Direct claim (must-fix):** R-B1 presents its eight-step order as authoritative "as proven by the manual referents," and R-B4 makes that order the contract. Steps 4 and 5 are not what the referent did, and step 4's census half is not proven at all.

- The spec orders **model-family spine (4) → census/snapshot recapture (5)**. The migration plan recaptures the snapshot in Phase 2 step 3 (`:203`) and only then runs the family-spine test in Phase 2's validation block (`:212`). That is 5 before 4.
- The spec's step 4 includes "census exact." The exact census check did not exist during Phase 2 — Phase 1 built a three-test subset (`:96`, Phase 1 Completion `:488`), and the full 13-test family spine with the MFE census fixture was grown in **Phase 4** (`:349-351`, Phase 4 Completion `:554`), i.e. *after* the Phase 3 manifest re-pin, preflight, and verify. The referent therefore proves the opposite placement for the census.

That Phase 4 placement was driven by the migration item's own scope (promoting source into `models/`), not by an integration-ordering rule — which is exactly why "as proven by the manual referents" is the wrong provenance claim to hang a `[HARD]` grade on. Either fix the order to match the referent, or keep the order the spec wants and re-grade the parts the referent does not prove as `[INFERRED]` with the reasoning stated. Under R-B4 as written, design has no license to reorder.

**L1-3 · Direct claim (must-fix):** The Problem section's motivating example overstates itself, and R-C9 leans on the overstatement. The spec says Item 6's Phase 2 opened with eleven red tests "because a scaffold commit added a `magnet_capital` objective to the manifest without re-pinning the fixtures" — that part is accurate (`run-study-first-consumer/plan.md:305`). The next sentence is not: "Nothing checked the manifest against the package until a study run tripped over it." Something did check. The known-answer fixtures *are* that check, and they were red at session start, before any study ran. The real lesson is narrower and still supports the item: the check existed but fired nowhere near the commit that broke it, and only when a human happened to run the suite. R-C9 then repeats the inflated version ("caught only when a study tripped over it") as its rationale. Fix the claim; the requirement survives it.

**L1-4 · Direct claim (advisory):** The `SYSIDE_LICENSE_KEY` citation is off by two lines. The spec cites `run-study-first-consumer/plan.md:308` in two places (§ two return classes, and via the product-lens trail); the actual line is `:306`. `:305` (eleven red tests) is correct. Small, but this spec asks downstream readers to trust line-level cites.

**L1-5 · Direct claim (advisory, in the spec's favour):** R-A6's refused-vs-could-not-run distinction is already producer-native for the largest gate, and the spec does not say so. `preflight.py run_gates` emits a per-gate `DID_NOT_RUN` status distinct from `FAIL`, with the blocking condition named in the result (`scripts/study/preflight.py:368-370, 375-424`). The Open Question asks "how 'could not run' is detected per producer" as if it were open everywhere. Citing this precedent would stop design from inventing a detection scheme for the gate that already has one, and would give it the shape to match for the others.

**Capture-fidelity structure — checked, mostly clean.** Every `[INHERITED]` cites a source. `[OWNER, epic § Hardening rule]` in R-F2 resolves to `epic_goal_strategy_task_harness.md:74` and the paraphrase is faithful. The two align.md-derived requirements (R-F3, R-F4) are honestly marked `AGENT-grade orchestrator reading` rather than promoted to owner grade. No verbatim quote is claimed anywhere, so there is nothing to falsify. The Non-Goal on the calc-then-compare parser follows Law 3's decision-record form rather than prohibition-mode phrasing. The § Ordering note is a genuine Law 4 surfacing. The one grade problem is L1-2: `[HARD]` over an ordering that is an agent reading of two plans.

### Lens 2 — Problem & Approach

**L2-1 · If-then tradeoff (advisory):** The Non-Goals boundary note — "executing the baseline point and any probe run that the gates themselves require is *inside* the seam" — is `[INFERRED]`, agent-grade, and sitting in a section where every other bullet is owner-ratified `[INHERITED: epic Item 3]`. The reasoning is right (a study is a declared question with axes, arms, a record, and findings; running a gate's own input is none of those) and the note states its own alternative, which is the correct Law 4 posture. But the force is easy to misread at skim: a downstream reader sees a Non-Goals bullet and treats it as settled. **If** the owner has any doubt about the seam executing a baseline point, this belongs above the fold as an owner question rather than as a boundary note inside Non-Goals. **If** the owner is content with the agent reading, the note should say plainly that it is an agent call awaiting ratification, not just that an alternative reading exists.

**L2-2 · Question to the user (advisory):** R-A4 makes the seam callable standalone by an operator at a terminal, graded `[INFERRED]` from the epic's route-equivalence row. That row is about *Item 6* proving hand and agent routes reach the same end state — it is not obviously a requirement that *this* seam ship a human entry surface. Sizing consequence: a standalone operator surface plus SC6's non-builder documentation is a meaningful chunk of the 8h execute estimate. Is the operator-callable path a first-build requirement, or is "a goal task can call it, and a human can call the same thing however a goal task does" enough?

### Lens 3 — Pipeline Risk

**L3-1 · Direct claim (must-fix):** R-B4, R-C1, and R-D1/SC3 cannot all hold unless an assumption the spec never states is true. R-B4 says no gate is skipped because a prior run passed it — so a second invocation re-runs R-B1.2, regeneration in place. R-C1 makes a non-git-clean package tree a `BLOCKER`. Therefore the re-run returns `CANDIDATE` naming the same identity (spec line 37, R-D1) **only if** regeneration under the pinned toolchain is byte-deterministic against an already-regenerated tree. If it is not, the second run dirties the tree, R-C1 fires, and the seam returns `BLOCKER` — which technically satisfies SC3's weaker wording ("does not produce a second conflicting candidate identity") while flatly contradicting the spec's own prose that a re-run "returns `CANDIDATE` naming the **same** identity … which is what makes the seam safe to call twice."

The migration plan gives evidence the assumption holds (`--smart-regen --preserve-handwritten` reported `Preserved: 10, Regenerated: 0`, both normative impls byte-identical, `:511`) but that was a first regeneration onto a repaired tree, not a re-run onto its own output. Design cannot resolve this by choosing: it either re-runs regeneration or it does not, and R-B4 currently forbids the second. Say which, and state the determinism assumption as an assumption.

**L3-2 · Question to the user (advisory):** R-A2 says a `BLOCKER` "names the gate involved" — singular — and R-B4 says the seam stops at the first refusal. But `preflight.py gates` deliberately does not stop: it runs all six checks and reports every one, passed or failed or `DID_NOT_RUN`, in a single document (`preflight.py:333-435`, docstring "Every gate appears in the result, whatever happened"). So one producer can refuse on several sub-gates at once. Does the seam's `BLOCKER` name the producer (preflight) and cite its document, or name a sub-gate? R-B3's cite-by-path rule points at the first answer, but R-A2's singular phrasing reads like the second. One clarifying sentence closes it.

**L3-3 · Direct claim (advisory):** SC4 has no test shape behind it. R-G1 enumerates three fixtures — success, gate failure, identity stability — inherited from epic Deliverables, and none of them is "the candidate is accepted by the stock study route with no seam-specific accommodation." Open Question 5 then defers *whether the seam demonstrates SC4 at all* to design. So a success criterion the epic marks as a checkbox currently has neither a requirement nor an owner. The epic has the same gap, so this is not a fidelity failure — but it is a criterion nobody will be able to tick at audit. Either add the shape to R-G1 or say explicitly that SC4 is verified by Item 6, not here.

**L3-4 · Question to the user (advisory):** SC6 has no stated evidence form. "A non-builder walks the seam's operator documentation and can, from it alone, assemble an integration request…" — who is the non-builder, and what gets recorded as proof? This is not pedantry: the sibling seam's audit marked its two documentation-and-walkthrough criteria **not met** (`CURRENT_WORK.md`, Item 2 audit 2026-08-26, SC7/SC9), and the fix pass had to satisfy them via "regression tests plus the auditor's walk." Naming that shape now — a fresh-session agent walk, recorded where — costs one sentence and prevents the same audit round-trip.

**Deferral accuracy — checked, clean.** The eight Open Questions are genuinely design-stage. The three orchestrator readings are correctly labelled `[AGENT]` deferrals rather than settled items. The "pending native repair" marker question is honestly parked as an epic-close debt rather than smuggled into scope. Nothing in the spec is stated as settled that the owner did not decide, except the R-B1 ordering grade already covered in L1-2.

### Lens 4 — Hygiene

**L4-1 · Rewrite request:** § F lists R-F1, R-F2, R-F3, **R-F5**, R-F4. The out-of-order insertion is a visible artifact of the product-lens fix pass. Renumber or reorder.

### Lens 5 — Reader Comprehension

No findings. The two-return-class table up front, the refused/could-not-run paragraph, and the ordering note each lead with the point and put the mechanism after. A tired engineer can skim this once and know the contract. The § Ordering note in particular is the right way to surface a premise conflict — plain statement, evidence, and an explicit "do not treat the shorthand as a constraint."

---

## Engagement Summary

**Overall take:** The contract is right and the shape is right — this is a stronger spec than its sibling was at the same stage, and the two-return-class framing plus R-A6 will save the goal layer real trouble. But the one requirement graded `[HARD]` and declared "the contract" contains a producer that does not do what the spec says it does, an order the cited referent did not run, and an idempotency claim that depends on an unstated determinism assumption. Those three would each stop a design session cold or, worse, get guessed past.

**Here's what I need you to weigh in on:**

1. **[L1-1]** There is no automated teax revision pin check anywhere in the repo — `tests/test_dependency_provenance.py` pins sysml-codegen, agentic-mbse, and 1costingfe only, and teax has no `__version__` to read. Decide whether the seam's gate 1 drops the teax half with that recorded, wraps the migration plan's manual `git rev-parse` against a recorded SHA, or files the missing check upstream. R-B1.1 and R-C2 both need rewriting either way.
2. **[L1-2]** R-B1's steps 4 and 5 are inverted relative to the migration plan, and the exact-census check the spec puts at step 4 actually ran in Phase 4, after preflight and verify. Confirm the order you want, and let the parts the referent does not prove carry `[INFERRED]` rather than `[HARD]`.
3. **[L3-1]** A re-run re-runs regeneration (R-B4), and a dirtied tree is a `BLOCKER` (R-C1) — so "safe to call twice" rests on regeneration being byte-deterministic onto its own output. Confirm that assumption and state it, or exempt regeneration from R-B4's no-skip rule.
4. **[L1-3]** The Problem section's Item 6 example says nothing checked until a study tripped over it. The fixtures were the check and they were red at session start. The honest version — the check fired far from the commit that broke it — still motivates the item; R-C9 should stop repeating the inflated one.
5. **[L2-2, L3-4]** Two scope questions worth one line each: is a standalone human entry surface a first-build requirement (R-A4), and what counts as evidence for SC6's non-builder walk, given the sibling audit failed on exactly that criterion shape?
6. **[L1-5]** Free win: `preflight.py` already emits a per-gate `DID_NOT_RUN` distinct from `FAIL`. Cite it under R-A6 so design matches the existing shape instead of inventing one.

---

## Resolutions

*(Empty — non-interactive stage session. To be filled by the owner or the orchestrator, keyed by finding ID, before the spec agent incorporates.)*

---

**Verdict:** **Revise** — the work item is sound and the contract shape is right; three must-fix defects sit inside R-B1 / R-D1.

**Must-fix (blocks design):** L1-1, L1-2, L1-3, L3-1.
**Advisory:** L1-4, L1-5, L2-1, L2-2, L3-2, L3-3, L3-4, L4-1.

**Next Steps:** Record resolutions above, then return to the spec-agent session (or re-run `/_my_spec`) pointed at this file. The reviewer does not edit the spec.
