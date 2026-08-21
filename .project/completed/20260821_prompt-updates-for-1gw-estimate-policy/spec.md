# Spec: Prompt Updates for the 1 GWe Estimate Policy

**Status:** Complete (Phases 1–5 verified 2026-06-06 — clean converging run on concept 24, iter-1 FAIL → iter-2 PASS)
**Owner:** Reid W
**Created:** 2026-06-06 10:40 PDT
**Complexity:** MEDIUM
**Branch:** TBD (currently on `feat/concept-explorer-omit-list`)

---

## Work Item Summary

The concept-analysis pipeline's prompts (analysis, model-setup, review, assessment, and their shared config) carry a stale and silently inconsistent story about what a relative cost override (`M * generic.costs.X`) means at the 1 GWe headline projection. The recent override-semantics investigation and the 2026-06-06 policy doc fix the conceptual story: every concept's headline is a **replicated** 1 GWe fleet of `N` real `P_native` modules, and override semantics depend on which of three **cost classes** (Shared / Per-unit / Power-proportional) an account belongs to. This work item updates the agent-facing prompts to teach that policy: class-aware override semantics, the modular-fleet rationale baseline (replacing the implicit "conventional 1 GWe plant" baseline), and the corresponding review/assessment checks.

## Why This Matters Now

A separate research thread proved that the analysis and model-setup agents have been writing relative overrides under a hidden mismatch: the *value* anchors to a per-module quantity (Class S/U inside the library) while the *rationale* invokes a "conventional 1 GWe plant" baseline (the monolithic interpretation we explicitly do **not** use). The reviewer can't catch it because the review prompt has no class-aware check and no notion of the modular vs monolithic baseline distinction. Every concept analysis re-run from here on will keep cementing the inconsistency into the corpus unless the prompts that drive the agents change first. The policy doc exists; the prompts need to inherit it.

## Key Bets / Constraints

- **Bet:** One invariant sentence — `account = M × library_fleet_cost(account)`, always — plus a class table that explains *why* the fleet cost is what it is (and dictates per-module-vs-whole-plant authoring shape) is enough to fix authoring behavior. We do **not** want three per-class multiplier rules; that is the cognitive load that produced the original drift. We do **not** need a typed helper or a code-level guardrail yet.
- **Bet:** The reviewer/assessor can catch the policy violation if it knows (a) the three cost classes, (b) that the rationale baseline must be "library default for a modular fleet of this device," and (c) that "conventional 1 GWe plant" framing in rationale is a finding.
- **Constraint:** The 1 GWe headline path stays `run_native_and_1gw(..., noak=True)` (replicated). No monolithic mode is introduced. Prompts must explicitly say so — not just imply it.
- **Constraint:** Override authoring shape stays the same six-field dict and the same two relative patterns (`generic.costs.<rollup>` vs `generic.cas22_detail["..."]`). We are changing *what the value means* and *what the rationale baseline is*, not the storage syntax.
- **Non-goal:** Library-side changes. The Class-S "buildings are charged once at module-scale floor" question (1cFE/1costingfe site-sizing) is out of scope for this work item.
- **Non-goal:** Re-authoring existing concept `model_setup.py` files. A follow-up may sweep them; this spec is prompts-only.
- **Non-goal:** Touching the prompts owned by Stage 0 (research/dossier/synthesis) — only the concept-analysis pipeline prompts that the policy actually changes.

---

## Business Goals

### Why This Matters
The headline LCOE number is the only cross-concept comparable the project produces. Its credibility rests on every concept's override registry being authored against the same, named baseline. Today the named baseline drifts silently per concept depending on whether the analyst (and the agent) were thinking modular or monolithic when they wrote the rationale. The policy doc resolves the question — modular always — and the prompts are how that decision reaches the agents.

### Success Criteria
- [ ] An analysis or model-setup agent reading the updated prompts can answer "what does `0.70 * generic.costs.cas21` mean for the 1 GWe headline?" with the single invariant — "70% of the library's 1 GWe fleet CAS21" — without invoking a per-class rule.
- [ ] A review agent reading the updated prompts will flag any rationale that invokes a "conventional 1 GWe plant" (monolithic) baseline as a finding.
- [ ] The inline example in `model_setup_costingfe.md` no longer carries an A-vs-B ambiguous rationale ("30% reduction vs library default" with no scale frame). It states the modular-fleet frame explicitly.
- [ ] A spot-check re-run of one previously-affected concept (e.g. 24-dense-plasma-focus) produces a rationale that names the modular-fleet baseline and a value whose class semantics match the policy.

### Priority
P1 — blocks the next round of concept analyses from cementing the wrong baseline. Not blocking any current PR.

---

## Problem Statement

### Current State
- `model_setup_costingfe.md` Rule 5 (lines ~269–328) describes the two relative-override storage patterns but is silent on (a) the three cost classes, (b) what the multiplier means at the headline by class, and (c) the modular-fleet rationale baseline. The inline example at L141–147 anchors `C220101` to `generic.costs.cas21` (mixes a U-account value with an S-account anchor) and frames the rationale as "vs library default" with no scale frame.
- `model_setup_costingfe.md:133–137` glosses `generic` as "the library's bare answer for a reactor this size, and the reference a relative override is written against" — silent on `_scale_overrides`, the rescale ratio, and the resulting headline meaning by class.
- `output_template.md` Section 5b (lines ~136–151) shows the YAML schema and says relative `value` references `generic.costs.cas21`, but doesn't tell the analysis agent what the multiplier *means* at the headline. The agent writes the value in one frame and the rationale in another.
- `config/account_walkthrough.md` defines the per-account discovery loop but is silent on class semantics — the agent decides yes/no per account without ever being told that "yes" means different things for CAS21 (S), C220103 (U), and CAS24 (P).
- `review.md` Section 4 and `config/assessment_checklist.md` Section 5 check the three-forward shape and numerical plausibility, but have no check on (a) rationale-baseline framing or (b) value↔class consistency.
- `config/analysis_goals.md` and `config/quality_standards.md` set up override accountability but do not mention the replicate-always architecture or the modular-fleet baseline.

### Desired Outcome
The five agent-facing prompts (analysis_v2, model_setup_costingfe, output_template, review, assessment) and the three shared configs (analysis_goals, quality_standards, account_walkthrough, assessment_checklist) carry one consistent story:
1. The 1 GWe headline is **always** the replicated fleet (`run_native_and_1gw`, `noak=True`). Monolithic is not an option.
2. The headline invariant is single and class-free: `account = M × (library's 1 GWe fleet cost for that account)`, always. `M` is "the fraction of the library's fleet answer you believe this concept should pay."
3. The three cost classes — **S** (Shared, charged once), **U** (Per-unit, ×n_mod with NOAK learning), **P** (Power-proportional, scales with plant power) — explain *why* the fleet cost is what it is and dictate the **authoring shape** (per-module M$ for sub-accounts, whole-plant M$ for top-level rollups). The class is comprehension, not a per-class multiplier rule.
4. Every relative override's rationale must be authored against the **modular-fleet baseline** ("library's default for a fleet of this device at 1 GWe") — never against a "conventional 1 GWe plant" (monolithic) baseline.
4. The reviewer and the assessor each carry one explicit check that catches the modular-baseline violation.

---

## Scope

### In Scope
- `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md` — Rule 5 expansion, `generic` gloss update, inline example fix.
- `exploration/concept_analysis/prompt_templates/output_template.md` — Section 5b schema gloss.
- `exploration/concept_analysis/prompt_templates/analysis_v2.md` — pointer to the class story for the override walkthrough.
- `exploration/concept_analysis/prompt_templates/review.md` — new check under "Two-Knob Projection & Model Integrity" (or rename) for rationale-baseline framing and value↔class consistency.
- `exploration/concept_analysis/prompt_templates/assessment.md` and `config/assessment_checklist.md` — corresponding finding criteria.
- `exploration/concept_analysis/prompt_templates/config/account_walkthrough.md` — mention the class table and where it lives.
- `exploration/concept_analysis/prompt_templates/config/analysis_goals.md` and `config/quality_standards.md` — one-paragraph orientation that the headline is the replicated 1 GWe fleet and that rationale must share that frame.
- The class table itself: decide whether it lives in one of the existing prompts or in a new shared snippet (e.g. `config/cost_class_table.md`) that other prompts `{{@include}}`.

### Out of Scope
- Library-side changes to `1costingfe` (Class-S site-sizing, override surface for CAS40/CAS70, etc.).
- A typed override helper (`relative_override("CAS21", 0.05, class="S", baseline="modular")`).
- Sweeping existing concept `model_setup.py` files to re-anchor rationales. (Tracked as a follow-up.)
- Any change to the three-forward contract validator or `model_setup_helpers.py`.
- Stage 0 prompts (research, dossier, synthesis) and the explorer-side prompts.

### Edge Cases & Considerations
- Some accounts straddle classes (the policy doc lists CAS22 rollup, CAS30/50/60 as Class C — "blend"). The prompt language has to handle this without over-specifying — most likely by mapping every overridable account explicitly and listing the blend cases by name.
- Class S accounts (CAS40, CAS70 today) are not currently overridable (1cFE/1costingfe#106). The prompt should still teach the class so analysts know *why* they can't override them, and so a future surface lands on prepared ground.
- The two existing "inverted" concepts (12-levitated-dipole at 1.34×, 17a-laser-icf-hybrid at 1.25×) were authored under interpretation B in the old prompts. Under the new policy the multiplier still means "fraction of the library's modular-fleet answer," so a >1 multiplier is a legitimate "this concept is more expensive than the library default for this account in the fleet frame." The prompt needs to make that legible without endorsing the prior B-framing.
- The native LCOE column in `print_cas_breakdown` remains diagnostic-only. The prompt should already say this somewhere; the policy doesn't change the column itself, but the reviewer must not treat native ≠ headline as a finding.

---

## Requirement Selection Notes

The normative section captures only what the prompts must say or check after this work item lands. Tone, ordering, and how to phrase the class table are left to design. Whether the class table is duplicated inline or extracted to a shared include is a design decision. The exact wording of the rationale-baseline check is a design decision.

---

## Requirements

### Functional Requirements

1. **FR-1**: The model-setup prompt MUST teach the three cost classes (S / U / P), enumerate which canonical accounts fall in each, and state what `n_mod` does to each class at the headline.
2. **FR-2**: The model-setup prompt MUST state the single invariant: at the headline, `account = M × (library's 1 GWe fleet cost for that account)`, for every class, with no exceptions. `M` is "the fraction of the library's fleet answer you believe this concept should pay." The class is **not** a per-class multiplier rule — it explains why the fleet cost is what it is (shared-once vs replicated vs power-scaled) and dictates the **authoring shape** (per-module M$ for sub-accounts, whole-plant M$ for top-level rollups).
3. **FR-3**: The model-setup prompt MUST instruct the author to write the override rationale against the **modular-fleet baseline** ("the library's default for a fleet of this device at 1 GWe") and MUST NOT use a "conventional 1 GWe plant" / monolithic baseline. The rationale answers "why M is what it is" against that one named baseline.
4. **FR-4**: The model-setup prompt's inline relative-override example MUST be class-consistent (the value anchor matches the example's account) and its rationale MUST be in the modular-fleet frame.
5. **FR-5**: The `generic` gloss in the model-setup prompt MUST explain that `generic` is both the writing frame for relative overrides and the rescale reference, and MUST point to where the rescale logic lives (`1costingfe/src/costingfe/model.py:_scale_overrides`).
6. **FR-6**: The analysis output template's Section 5b gloss MUST mirror the multiplier-meaning-by-class statement (FR-2) and the modular-fleet baseline rule (FR-3), so the analysis agent and the model-setup agent share the same authoring frame.
7. **FR-7**: The per-account walkthrough config MUST reference the class table and instruct the agent to identify each account's class as part of the yes/no decision.
8. **FR-8**: The review prompt MUST include an explicit check that every enabled relative override's rationale is in the modular-fleet frame (not the monolithic frame), and that the value's anchor matches the account's class.
9. **FR-9**: The assessment checklist MUST include the corresponding finding criterion (one bullet, addressed under Override Discipline or a renamed area).
10. **FR-10**: The analysis_goals and quality_standards configs MUST carry one short orientation paragraph stating that the headline is the replicated 1 GWe fleet (not a monolithic 1 GWe machine) and that override values and rationales share that frame.
11. **FR-11**: The class table (the canonical S / U / P breakdown with the account list) MUST appear in at least one prompt the model-setup agent and the analysis agent both read, and the review/assessment prompts MUST be able to reference it.

### Non-Functional Requirements

- The prompts MUST stay coherent with the existing three-forward contract language; no contradictions introduced.
- The prompt edits SHOULD prefer targeted insertions over wholesale rewrites — the existing prompts have a lot of working language that this work item is not trying to disturb.

---

## Acceptance Criteria

### Core Functionality
- [ ] `model_setup_costingfe.md` carries the class table (or includes it from a shared snippet), the multiplier-meaning-by-class statement, the modular-fleet baseline rule, and a class-consistent inline example.
- [ ] `output_template.md` Section 5b carries the multiplier-meaning-by-class statement and the modular-fleet baseline rule.
- [ ] `account_walkthrough.md` instructs the agent to identify each account's class.
- [ ] `review.md` and `assessment_checklist.md` carry the rationale-baseline check.
- [ ] `analysis_goals.md` and `quality_standards.md` carry the "headline is the replicated 1 GWe fleet" orientation paragraph.
- [ ] A model-setup re-run on 24-dense-plasma-focus (or any sub-1 GWe relative-override concept) produces rationales in the modular-fleet frame, and a subsequent review pass would PROCEED on the rationale-baseline check.

### Quality & Integration
- [ ] No contradictions introduced with the existing three-forward contract, the six-field override shape, or the strict-kwarg validator language.
- [ ] Wording is consistent across the five touched prompts and the four touched configs (one named baseline, one named class taxonomy).
- [ ] Existing prompt-template-driven CLI flows continue to render without template errors (variable interpolation, includes).

---

## Next-Stage Handoff

**Settled in this spec:**
- The policy itself is fixed (modular-always, three classes, modular-fleet baseline). Prompts inherit it.
- The set of files touched is fixed (see Scope > In Scope).
- The class taxonomy comes from the policy doc — S / U / P — and the account list in the policy doc is the authoritative starting point.

**Design must figure out:**
- Whether to extract the class table to a new shared snippet (e.g. `config/cost_class_table.md`) or duplicate it in the model-setup and output-template prompts.
- The exact phrasing of the invariant sentence and how to position it relative to the class table — the invariant leads, the class table supports. The risk to avoid is letting the class table read as three separate multiplier rules.
- How the class table communicates authoring shape (per-module vs whole-plant M$) without slipping back into per-class multiplier framing — likely a single "authoring shape" column rather than a "what M means" column.
- How to handle Class C ("blend") accounts in the prompt language — name them out, or fold into Class P with a caveat.
- Whether the "rationale-baseline framing" check sits inside the existing Review Section 4 ("Two-Knob Projection & Model Integrity") or warrants a new Section 6 ("Override Frame Coherence").
- Whether the agent-facing class table needs the monolithic-vs-modular contrast called out, or just the modular semantics (the policy doc has both; the prompts may not need both).

**Watch-outs for design:**
- The model-setup prompt is already long. Insertions should be tight; consider a shared include for the class table to avoid duplicating ~30 lines into two prompts.
- The phrase "conventional 1 GWe plant" appears in several existing concept analyses' rationale text and in the prior research doc; the new prompt language should describe what wrong looks like clearly enough that an agent reading an old rationale flags it.
- The inline example fix (FR-4) is constrained by the existing Rule 5 storage-shape rule (top-level `cas21` vs sub-account `C220103`). The example must respect both rules simultaneously — pick a top-level Class U account or a sub-account Class U with the correct anchor.
- The reviewer's check (FR-8) needs a way to distinguish "rationale in modular frame" from "rationale in monolithic frame" without false-flagging concepts where the analyst correctly invokes a 1 GWe comparable that happens to be a monolithic plant in the literature (e.g. ARC, STEP). Design should pin down the wording.

---

## Related Artifacts

- **Policy doc:** `.project/reports/2026-06-06-1gw-estimate-policy.md`
- **Research (accurate):** `.project/research/20260606-093951_override-scaling-semantics-by-account-class.md`
- **Research (prior, partially superseded):** `.project/research/20260605-145424_relative-override-double-discount.md`
- **Affected prompts:** `exploration/concept_analysis/prompt_templates/{analysis_v2,model_setup_costingfe,output_template,review,assessment}.md` and `config/{analysis_goals,quality_standards,account_walkthrough,assessment_checklist}.md`
- **Design:** `.project/active/prompt-updates-for-1gw-estimate-policy/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
