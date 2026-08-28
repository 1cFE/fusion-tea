# Spec Review: GSTH Item 5 — Research-to-Model Round Proof

**Spec:** `.project/active/goal-research-model-proof/spec.md`
**Contract:** `claude-pack/commands/_my_spec.md`
**Review File:** `.project/active/goal-research-model-proof/spec-review.md`
**Date:** 2026-08-27

---

## Reality Check

**Sound.** The spec is about the right work item, and it covers epic § Item 5's scope, out-of-scope, and all six success criteria without narrowing or widening them. Every path and pinned commit I spot-checked resolves and says what the spec claims: the epic at `83d6fc6c`, the runbook at `1d43dc5b`, the seam guide at `9637f1b7`, DI-008 and the WI-031 research doc at `ffa5c54c`, the study record at `881d4448`, the discovery log at `e891b23a`. Discovery row `20260821-power-cycle-ab#3` exists and reads as quoted. `mfe_power_balance.sysml:119,135` are exactly the two lines where `p_pump_in` enters. `CURRENT_WORK.md` really does name "the `p_pump` re-source item" in the Phase 4 next-up list. The Align rulings are carried faithfully.

The faults are not directional. They are three places where a requirement pair can squeeze the run toward a dishonest result, one physics claim that is imprecise at exactly the decision point it governs, one surfaced tension that is under-surfaced, and a handful of provenance tags that overstate their authority. Verdict is **Revise**.

---

## Audit

### Lens 1 — Faithfulness

**L1-1 · Direct claim (must-fix):** R-A6's invariant says the `p_pump` change "moves every arm of both committed A/B studies equally." That is true of the *input* and false of the *effect*, and the difference is the whole question R-E1 has to answer. `rec_frac = recirculating / p_et` (`mfe_power_balance.sysml:135,143-144`), and `p_et` differs across the power-cycle arms by construction (η 0.333 → 0.47). The record already shows unequal rec_frac at the same grid point — 0.94 / 0.79 / 0.68 by arm — and unequal fence positions: `recirc_ok` is violated at R ≤ 8.0 m (paper), ≤ 6.5 (upstream), ≤ 5.5 (both η 0.47 arms) (`record.md@881d4448:56,92`). An equal +60–190 MW addition to the recirculating sum therefore moves each arm's fence by a *different* amount and can flip feasible regions unevenly. DI-008's own "moves every arm equally" is about the input being cycle-independent (DI-007), not about verdicts. As written, R-A6 hands the round a premise that reads as "comparison meaning is preserved by construction," which is the exact conclusion R-E1 vs R-E3 is supposed to be decided on evidence. The invariant needs to state the equal-input / unequal-verdict distinction explicitly.

**L1-2 · Direct claim (must-fix, small):** R-A7 is tagged `[NEED] [OWNER 2026-08-27, conflict surfaced at Align]`. `align.md:10-12` records the owner accepting the *removal* from Run-Study Item 6 Phase 4's close list. It does not record any owner statement about **where that removal gets written down**. The removal is `[NEED]`; the obligation to record it where a Phase 4 operator will read it is the spec agent's inference. Split the requirement or retag the recording half `[INFERRED]`.

**L1-3 · Direct claim (must-fix, small):** R-C3 is tagged `[NEED] [OWNER 2026-08-25; cap value inherited from GOAL_RUNBOOK@1d43dc5b § Limits]` and then bolds **"The cap is 2 revisions (3 submissions)"**. The owner-stated part (epic:49, `[OWNER 2026-08-25]`) is "the author revises until the checkpoint passes or its declared cap produces an owner-visible stop" — it names a cap, not a number. The number 2 is the runbook *default*, and the runbook explicitly says "A goal may declare tighter or looser values, and the declared value wins" (`GOAL_RUNBOOK.md:232`). Tagging the number `[NEED]` promotes an inherited default to owner-settled and forecloses a choice the runbook deliberately leaves open. The stop-never-releases half is genuinely `[NEED]`+`[INHERITED]`; the number is `[INHERITED]`.

**L1-4 · Direct claim (must-fix, small):** Success criterion 8 is tagged `[INHERITED: epic § Success Criteria, last item]`, but the epic's last criterion (epic:58) is only the second half: "First-build scope contains no control-plane mechanism from the hardening path unless the epic records the observed run failure that promotes it." The first clause — "Every prose failure the run hits is recorded" — is not in the epic; it is R-H2, which the spec itself tags `[INFERRED]`. The criterion carries an inferred obligation under an inherited tag. This also makes the section's lead sentence ("The six epic criteria, plus two this item adds") not quite match the list, where the eighth item claims inheritance.

**L1-5 · Direct claim (must-fix, small):** Related Artifacts cites `.project/active/goal-research-model-proof/product-lens.md` as a product-lens artifact. It does not exist — the directory holds `align.md`, `briefs/`, and `spec.md`. Either the lens was not run, or the reference is aspirational; a cited artifact that isn't on disk is the kind of thing the audit will trip on later.

**L1-6 · Verified, no action:** the remaining provenance grades hold up. R-A1/R-A2/R-A4 map to `align.md:7-17` rulings (a)/(b)/(c). R-G1 maps to `align.md:20-22`. R-H1 maps to epic:74 `[OWNER]`. R-C1 maps to epic:49 `[OWNER 2026-08-25]`. R-D5's citation of Item 2 R-C3 is exact, quote and owner date included (`.project/completed/20260827_goal-research-seam/spec.md:88`). The Non-Goal on `cryo-volume-basis` is backed by a real owner close (`e891b23a`). The `[OWNER-VERBATIM]` quote in the Problem section appears at `goal-driven-model-development-harness.md:33` word for word. No `[INFERRED]` item is marked settled anywhere.

### Lens 2 — Problem & Approach

**L2-1 · Question to the user (must-fix):** **Can this round honestly "discover" a prerequisite it was grounded on?** R-A1 grounds the goal on the `p_pump` re-source need, citing DI-008 and a discovery row whose own text already says "re-sourcing is a separate modeling item." R-B1 then makes the round's first task a bounded modeling objective on `p_pump`, and R-B2 insists `PREREQUISITE` be a return, never a prediction. But the grounding evidence *is* the prerequisite, spelled out. A model task pointed at `p_pump` with DI-008 in its evidence set cannot fail to return `PREREQUISITE`; it is restating its inputs. That is a staged discovery, and criterion 1 ("a **real** `PREREQUISITE`") would be technically met by machinery that proves nothing.

This is not fatal — a genuine version exists — but it depends on how the goal question is framed at grounding, which is reserved gate (a) and therefore yours. The question to settle: **what is the bounded modeling objective, such that its prerequisite is a finding rather than a restatement?** One shape that works: ground the goal on the *decision* ("does the stellarator package's recirculating power basis survive a sourced circulator figure, and do the A/B conclusions survive with it?"), and make task 1 the model change itself — attempt to re-base `p_pump` from repository-native sources, and let it return `PREREQUISITE` when the only citable authority is an un-ingested PDF. There the prerequisite is discovered by the attempt. The spec should say what would distinguish the two, and `verification_record.md` should be required to show it (R-H2).

**L2-2 · If-then tradeoff (advisory):** The spec's bet is that one round on one need proves the whole `model → research → model` sequence. That holds **if** the seam returns `REGISTERED` and the follow-up modeling task actually lands. It is much weaker **if** the round ends at an owner gate or an operator queue — which, given L3-1 and L3-2 below, is the more likely outcome. The spec is honest that non-positive closes are valid, but it does not say what the *item* is worth if the sequence's second half never executes. Worth a sentence: does the item still ship, or does it open round 2 (Open Question 2)? Right now that judgment is deferred to design without the criterion it should be judged against.

**L2-3 · Advisory:** Sizing looks right at the epic's 8h execute, with one caveat — R-E1/R-E2 leave open whether the follow-up modeling work item is carried through implement (Open Question 3). If it is, this is not an 8h item. Design should be told to bound it, not just scope it.

### Lens 3 — Pipeline Risk

**L3-1 · Direct claim (must-fix):** **Success criterion 3 does not admit `OPERATOR_QUEUE`, and `OPERATOR_QUEUE` is the likeliest return.** The criterion reads: "The Item 2 seam returns registered MR-4-citable evidence **or an honest strategy blocker**." But R-D6 and the "Not a criterion, deliberately" paragraph both name `OPERATOR_QUEUE` as a valid real result, and R-D3 forbids re-grading the seam's native class. So an `OPERATOR_QUEUE` return leaves criterion 3 unmet under a spec that elsewhere calls it a legitimate outcome — and the run's two escapes are both prohibited: hand-fetch and register the PDF (violates R-D1's "no hand-written registry step anywhere in the path"), or read the queue as a blocker (violates R-D3).

This is not hypothetical. DI-008's strongest primary — Moscato et al., SOFT 2018, WPBOP-CPR(18) 20276 — is recorded as "open PDF, **not ingested**" (`KNOWLEDGE.md@ffa5c54c` DI-008), which is precisely the guide's `OPERATOR_QUEUE` shape: "a named candidate blocked on something only a person can resolve" (`research_seam_operator_guide.md:165`). The criterion needs to name all the seam's honest returns, or say explicitly which ones leave it unmet and why that is acceptable.

**L3-2 · Direct claim (must-fix):** **The honest-outcome list omits the owner gate.** The "Not a criterion, deliberately" paragraph names three valid non-positive closes: seam queue, bounded negative, premise moved. It does not name the fourth, which R-A4 and R-E2 make near-certain — the round parks at a reserved gate (minting/advancing the work item, or amending DI-008) and the owner has not ruled by close. Under the list as written, that outcome reads as "criterion 4 failed" rather than "the round closed at a declared gate." Add it, or state plainly that an unresolved gate is a failure of the item.

**L3-3 · Rewrite request (must-fix — R-C2 needs an owner ruling, not an italicised note):** The spec is right on the merits and wrong on the volume. The runbook's trigger is "after a study reading produces proposed dispositions" (`GOAL_RUNBOOK.md:140`); this round reads a committed record. The spec's reading — that the checkpoint's purpose is catching a misread before follow-up compounds, so a reading of committed study evidence satisfies it — is defensible, and epic § Item 5's own criterion drops the word "study" ("a fresh critic reviews **the reading** and proposed dispositions"). But the epic's **owner-graded** criterion (epic:49, `[OWNER 2026-08-25]`) says "reviews the **study** reading," and the owner's verbatim words behind it start with "Study > Analysis > Dispositions Plan" (`goal-driven-model-development-harness.md:33`). So the spec is re-reading an owner-graded phrase inside an `[INFERRED]` requirement, and then building section C on the result without parking anything. That is exactly the shape capture-fidelity Law 4 says not to resolve silently, and the owner was in the room this morning.

The consequence is epic-level, not cosmetic: if the narrow reading is right, Item 5's checkpoint rehearses the criterion but does not prove it, and Item 6's scope contains no separate checkpoint requirement — so nothing proves it. Raise this to an Open Question addressed to the owner (or a surfaced-conflict block), park the dependent conclusion, and note that under the narrow reading the runbook sentence is what gets amended.

**L3-4 · Question to the user (advisory):** R-D5 forbids minting a DI and R-A4 makes amending DI-008 a reserved gate. But the positive path (R-E1) needs an MR-4-citable basis for the new `p_pump` value. DI-008 already carries the band (2–6 %, ~60–190 MW) and its authority, so a newly registered source arguably lets the modeling item cite the registered source directly, no DI amendment needed. Is that the intended route? If instead the model change is expected to cite an amended DI-008, the round hits a reserved gate before criterion 4 can be met, and L3-2 becomes load-bearing. Design will guess if the spec doesn't say.

**L3-5 · Direct claim (must-fix, small):** R-G2 retires the WI-031 hand-pattern bullet with the `research` row, but the flip leaves two neighbouring sentences false. `GOAL_RUNBOOK.md:260` reads "**Two seams are not repaired yet**, and a goal round may not silently absorb either repair," and :264 closes with "The repairs have their own owners and their own failure contracts." After the flip only `integrate` is unrepaired. R-G1/R-G2 as written would ship a runbook whose lead-in contradicts its own table. Name the surrounding prose as in scope.

**L3-6 · Advisory (verifiability):** Two criteria can't be checked against disk as stated. Criterion 8's first clause — "every prose failure the run hits is recorded" — is unfalsifiable from the artifact side; an auditor can verify that recorded failures are real, never that none went unrecorded. Criterion 7's "the change is made after the live round exercised the seam, not before" *is* verifiable, but only by commit ordering, which the criterion doesn't say. Say how each is checked, or restate criterion 8's first clause as the positive obligation it really is (R-H2's record).

**L3-7 · Advisory:** Open Question 4 (declare a covering branch before the run) is the right instinct and Item 4's precedent is real — the epic explicitly leans on "the covering branch was declared before the run" to dispose criterion 5 (epic:338). Given L3-1 and L3-2, this stops being a nice-to-have: without a pre-declared branch list, an `OPERATOR_QUEUE` or a gate park will be re-read after the fact as a failed criterion. Consider promoting it from Open Question to a requirement, or at least from "recommended" to "required unless design records why not."

### Lens 4 — Hygiene

**L4-1 · Rewrite request (advisory):** The Problem's third paragraph carries seven pinned citations in one block and is the hardest thing in the spec to read once. It's doing real work — it is the evidence that the need is live — but the reader has to hold four artifacts in their head to get one claim ("the modeling work is real, the source gap under it is real, and the row is still open"). Lead with that sentence, then the evidence.

### Lens 5 — Reader Comprehension

No findings. The spec states its bets plainly, the honest-outcome paragraph is unmissable and correctly placed, and a tired reader would come away knowing what the round is and what could stop it. Section C's R-C2 is the one place where a decision hides inside prose (see L3-3), and that's filed there rather than here.

---

## Engagement Summary

**Overall take:** This is a strong spec — faithful to the epic, faithful to your Align rulings, and every pinned citation I checked resolves and says what it claims. It fails in three narrow but load-bearing places, all of the same kind: a requirement pair that pushes the run toward a dishonest answer when the honest one arrives. The most likely research return (`OPERATOR_QUEUE`, because DI-008's best primary is an un-ingested PDF) is not admitted by the criterion that would judge it, and the two ways out are both explicitly prohibited elsewhere in the spec. Revise, not rework.

**Here's what I need you to weigh in on:**

1. **[L3-1]** Success criterion 3 admits "registered evidence or an honest strategy blocker" — but an `OPERATOR_QUEUE` is neither, and it's the return DI-008's un-ingested PDF most likely produces. Should the criterion name all four seam returns, or do you want the queue to count as unmet?
2. **[L3-3]** The runbook says the critic fires "after a study reading"; this round reads a committed record. The spec resolves that itself, in an `[INFERRED]` requirement. Your 2026-08-25 criterion says "study reading," and your own words behind it start with "Study >". Do you want the broad reading (this checkpoint proves the criterion) or the narrow one (it rehearses it, and the runbook sentence gets amended)? Item 6 has no checkpoint of its own, so under the narrow reading nothing proves it.
3. **[L2-1]** The goal is grounded on the `p_pump` prerequisite, and then the round is asked to *discover* it. What bounded modeling objective makes that a real discovery rather than a restatement of the grounding evidence? This lands on reserved gate (a), the goal question, so it's yours before design.
4. **[L1-1]** R-A6 tells the round that the `p_pump` change "moves every arm equally." The input is equal; the effect is not — `rec_frac` is already 0.94 / 0.79 / 0.68 by arm and the fences sit at different R. As written it pre-answers the "does comparison meaning survive" question the round exists to decide.
5. **[L3-2]** The honest-outcome list is missing the outcome your own reserved gates make likeliest: the round parks at a gate and closes unresolved. Valid close, or item failure?
6. **[L3-5]** Flipping the `research` row leaves the runbook saying "Two seams are not repaired yet." Bring the surrounding prose into R-G1/R-G2's scope.
7. **[L1-2, L1-3, L1-4, L1-5]** Four small provenance/reference fixes: R-A7's recording obligation is inferred not owner-stated; R-C3's cap *number* is an inherited default the runbook lets a goal override, not a `[NEED]`; criterion 8's first clause isn't in the epic it cites; and `product-lens.md` is cited but doesn't exist.

---

## Resolutions

*(Empty — to be filled as findings are resolved. The reviewer does not edit the spec.)*

---

**Verdict:** Revise
**Next Steps:** Record resolutions above, then re-run `/_my_spec` (or return to the spec-agent session) pointed at this review. L3-3 and L2-1 want owner answers before design starts; the rest can be resolved by the spec agent against recorded decisions.
