# Implementation Plan: Prompt Updates for the 1 GWe Estimate Policy

**Status:** Draft
**Created:** 2026-06-06
**Last Updated:** 2026-06-06

## Source Documents

- **Spec:** `.project/active/prompt-updates-for-1gw-estimate-policy/spec.md` — requirements (FR-1…FR-11), in-scope file list, design must-figure-outs.
- **Policy reference:** `.project/reports/2026-06-06-1gw-estimate-policy.md` — the canonical source for the invariant, the class taxonomy, and the modular-fleet baseline.
- **Mechanics reference:** `.project/research/20260606-093951_override-scaling-semantics-by-account-class.md` — the step-by-step trace; cite for `_scale_overrides` mechanics in the `generic` gloss.
- **No `design.md`** — the spec + policy doc carry the design content for a prompts-only change.

## Implementation Strategy

**Phasing Rationale:** Author the shared snippet first (Phase 1) — every other edit either includes it or references its terms, so the wording risk lives there. Then move outward by audience: model-setup agent (Phase 2, the prompt that produces the artifact with the bug), analysis-side prompts (Phase 3, the prompt that proposes the override), reviewer/assessor (Phase 4, the prompt that catches violations). Phase 5 is the only real validation — a fresh concept run.

**Critical Path:** Snippet → model-setup prompt → fresh concept run. The other phases are necessary for closing the loop but the snippet + model-setup edit is where the policy lands in agent behavior.

**First Proof Point:** Phase 1's snippet read in isolation answers "what does `0.70 * generic.costs.cas21` mean for the headline?" with the single invariant. If the snippet doesn't, no downstream prompt will recover.

**Overall Validation Approach:**
- No automated tests — these are prompt-template edits.
- Static verification per phase: render the template (catch `{{@include}}` / variable errors), grep for forbidden phrases ("conventional 1 GWe plant" in the rationale framing), spot-read.
- Real validation is Phase 5: run a previously-affected concept fresh through the pipeline and inspect outputs against the policy.

---

## Phase 1: Author the shared policy snippet

### Goal
Produce one canonical fragment that carries the invariant sentence, the S/U/P class table (with an authoring-shape column, not a multiplier-meaning column), the modular-fleet baseline definition, and the "what wrong looks like" examples. Every downstream prompt either `{{@include}}`s it or quotes its terms verbatim.

### Assumption Under Test
That a single invariant — `account = M × library_fleet_cost(account)` — plus a comprehension-only class table is teachable in one snippet without re-fracturing into three per-class multiplier rules.

### Snippet stencil (write this first)
```markdown
# Override semantics and the 1 GWe headline

## The invariant
At the 1 GWe headline, for every account in every class:

    account = M × (library's 1 GWe fleet cost for that account)

`M` is the fraction of the library's fleet answer you believe this concept
should pay. That is the whole rule. The classes below explain *why* the fleet
cost is what it is and dictate the **authoring shape** (per-module M$ vs
whole-plant M$). They do NOT introduce per-class multiplier rules.

## The fleet architecture (read once)
The headline is always the replicated fleet ...

## Cost classes — what they explain
| Class | What replication does | Authoring shape for relative overrides | Accounts |
|---|---|---|---|
| S — Shared | charged once across the fleet | whole-plant M$ (top-level rollup) | CAS10, CAS21, CAS28, CAS40, CAS70 |
| U — Per-unit | ×n_mod with NOAK learning | per-module M$ (sub-account in cas22_detail) | C2201xx, CAS80 |
| P — Power-proportional | scales with plant power | whole-plant M$ (top-level rollup) | CAS23–27, C2202xx–C2207xx |

## The rationale baseline
Every relative override's rationale is authored against ONE named baseline:
"the library's default for a fleet of this device at 1 GWe."
Never "a conventional 1 GWe plant" / monolithic baseline ...

## What wrong looks like
- Value-vs-rationale frame mismatch: ...
- Monolithic baseline in rationale: ...
```

### Changes Required

**Reference:** `spec.md` FR-2, FR-3, FR-11; policy doc Part 2 (knobs), Part 3 (classes), Part 4 (rules).

- [x] Create `exploration/concept_analysis/prompt_templates/config/override_semantics.md` (name chosen: `override_semantics.md`).
- [x] Confirm the prompt template engine resolves `{{@config/override_semantics.md}}` the same way it resolves the existing `{{@config/analysis_goals.md}}` etc. (verify by reading whichever renderer handles the existing includes). — `templating.py:fill_template` resolves `{{@rel}}` against `TEMPLATES_DIR` (= `prompt_templates/`) in a **single, non-recursive** pass; `loop.py:628` calls it with the default `templates_dir` for model-setup too. **Nested includes do NOT work** — the snippet must not itself contain `{{@...}}`, and Phase 3's "include from analysis_goals" option is replaced by duplication.
- [x] Snippet content: invariant sentence (one paragraph); fleet-architecture paragraph; class table with **authoring shape** column (not "what M means"); rationale-baseline definition; 2–3 "what wrong looks like" examples; one-line pointer to `_scale_overrides` in `1costingfe/src/costingfe/model.py` for readers who want the mechanics.
- [x] No per-class multiplier statements. Discipline test: if you can remove the class table without weakening the invariant, the invariant is doing the right work — keep the table for the authoring-shape decision only.

### Validation

**Static:**
- [x] Read the snippet cold. Answer "what does `0.70 * generic.costs.cas21` mean?" using only the invariant. — answered: 70% of the library's 1 GWe fleet CAS21.
- [x] Grep the snippet for "conventional 1 GWe" — appears only in negative/what-wrong contexts (the FR-3 prohibition + the examples), never as the endorsed baseline.
- [x] Class table has no "multiplier means" column. Columns: class, why the fleet cost is what it is, authoring shape, accounts (the accounts column matches the Phase-1 stencil).

**What We Know Works After This Phase:** A canonical fragment exists that downstream prompts can include. The invariant is stated once, in one place.

---

## Phase 2: Update the model-setup prompt

### Goal
The model-setup agent reads the snippet, fixes the `generic` gloss to point at `_scale_overrides`, and works from an inline example whose value-anchor matches the example's account and whose rationale is in the modular-fleet frame.

### Assumption Under Test
That fixing the model-setup prompt is enough to shift agent authoring behavior on the next concept run — i.e. that the snippet + a corrected inline example + a fixed `generic` gloss collectively close the gap that produced the original drift.

### Edit stencil (write this first)
- The `generic` gloss (current L133–137) becomes: "`generic` is the library's overrides-off forward at `P_native`. It is both the writing frame for relative overrides and the reference the framework rescales against at projection time (see `_scale_overrides` in `1costingfe/src/costingfe/model.py`). Under the invariant above, the headline value lands on `M × library_fleet_cost(account)` regardless of class."
- Rule 5 (current L269–328) gains: an `{{@include}}` of the snippet near the top, plus the existing storage-shape paragraph reframed as "authoring shape — pick the one that matches your account's class."
- The inline example (current L141–147) gets rewritten: either a Class-U sub-account with `generic.cas22_detail["C220101"]` (per-module M$) or a Class-S/P top-level with `generic.costs.cas21` (whole-plant M$). Rationale in the modular-fleet frame.

### Changes Required

**Reference:** `spec.md` FR-1, FR-2, FR-3, FR-4, FR-5.

- [x] `model_setup_costingfe.md` §2b — rewrote the `generic` gloss: `generic` is the overrides-off forward at P_native, both the writing frame AND the `_scale_overrides` rescale reference; headline lands on `M × fleet_cost` regardless of class.
- [x] `model_setup_costingfe.md` inline example — replaced with the **Class-U sub-account** shape: `{"account": "C220101", "value": 0.70 * generic.cas22_detail["C220101"], ...}`, rationale in the modular-fleet frame ("70% of the library's per-module C220101 … fleet pays 0.70 × n_mod × per-module … NOT a conventional 1 GWe plant"). This directly fixes the documented bug (C220101 was anchored to `generic.costs.cas21`).
- [x] `model_setup_costingfe.md` Rule 5 — inserted `{{@config/override_semantics.md}}` after the Rule 5 opening paragraph; reframed the two-pattern block as "pick the shape that matches your account's storage shape (the authoring-shape column)"; **fixed the top-level example** from the mismatched `C220101 → generic.costs.cas21` to `CAS24 → generic.costs.cas24` (account matches anchor).
- [x] Grepped for "conventional"/"monolithic"/"vs library default". Only two hits: the inline-example prohibition (correct) and an unrelated efficiency-override note in Rule 6 ("library default" = efficiency default, not a baseline frame) — left as-is.

### Validation

**Static:**
- [x] Rendered `model_setup_costingfe.md` via `fill_template` with minimal vars: include resolves (no `CONFIG FILE NOT FOUND`), invariant text present, no leftover `{{@config` token.
- [x] Grep for "conventional 1 GWe" / "monolithic" — appears only in the snippet's prohibition/what-wrong text and the inline-example rationale's prohibition.
- [x] Read the inline example cold: value-anchor (`generic.cas22_detail["C220101"]`) matches the account's Class-U storage shape; rationale names the modular-fleet baseline.

**What We Know Works After This Phase:** The model-setup agent's next run is reading the policy. Behavior change is unverified until Phase 5.

---

## Phase 3: Update the analysis-side prompts

### Goal
The analysis agent reads the same policy when proposing overrides in `analysis.md` Section 5b. The per-account walkthrough names the class as part of the yes/no decision. Orientation paragraphs in the shared configs frame the headline as the replicated fleet.

### Assumption Under Test
That the upstream (analysis-time) override proposals carry the right rationale frame, so the model-setup agent isn't forced to retrofit a baseline that wasn't in the analysis to begin with.

### Edit stencil
- `output_template.md` §5b (current L130–151): include the snippet (or a condensed reference to it) just before the YAML stencil; rewrite the "Relative `value` expressions reference …" paragraph to state the invariant and the modular-fleet baseline.
- `account_walkthrough.md`: add one bullet to the per-account decision — "identify the account's class (S / U / P) from the snippet table; this dictates whether your override value is a per-module M$ or a whole-plant M$."
- `analysis_v2.md`: one-line pointer added to the override-discovery section that says "for the override semantics and rationale baseline, see {{@config/override_semantics.md}}."
- `analysis_goals.md`: one-paragraph orientation that the headline is the replicated 1 GWe fleet and rationale baselines share that frame.
- `quality_standards.md`: same orientation paragraph (or `{{@include}}` from analysis_goals if the engine supports nesting).

### Changes Required

**Reference:** `spec.md` FR-6, FR-7, FR-10.

- [x] `output_template.md` §5b — **condensed inline** statement (NOT an include): `output_template.md` is read raw by the agent (`output_template_path`), never `fill_template`'d, so a `{{@}}` include would render as literal text. Wrote the invariant + modular-fleet baseline + S/U/P gloss inline and pointed to the embedded policy.
- [x] `config/account_walkthrough.md` — added a "identify the account's cost class first (S/U/P)" step to the per-account decision; it points to the class table (this file is itself `{{@}}`-included into `analysis_v2.md`, and the full snippet renders just above it in the same prompt).
- [x] `analysis_v2.md` — **deviation from plan:** carries the FULL `{{@config/override_semantics.md}}` include in the Override Candidate Discovery section (not just a pointer), because `output_template.md` can't host the include (raw-read). This is where the analysis agent actually reads the policy; satisfies FR-11 (both agents read the class table: analysis via this include, model-setup via Rule 5).
- [x] `config/analysis_goals.md` — added the "headline is the replicated 1 GWe fleet" orientation paragraph.
- [x] `config/quality_standards.md` — added the same orientation paragraph as a new section (duplicated, not nested-included — the engine has no nested-include support).
- [x] Grepped the four files for monolithic-baseline framings; the only "conventional 1 GWe"/"library default" mentions are the new prohibitions.

### Validation

**Static:**
- [x] `analysis_v2.md` renders without errors: `override_semantics` + `account_walkthrough` includes resolve, orientation present, no leftover `{{@config` token, no `CONFIG FILE NOT FOUND`.
- [x] `test_template_lint.py` — 6 passed (every substitution var resolves; no forbidden `Reuses:` / `# DEFAULT: framework value` / `result_1gw_native` strings in any `.md`, including the new snippet).
- [x] Reading `analysis_v2.md` (embeds the policy) → `account_walkthrough.md` (class-id step) → `output_template.md` §5b (condensed invariant + baseline) in the analysis agent's order, the analyst can state the headline invariant and the rationale baseline without opening the policy doc.

**What We Know Works After This Phase:** The analysis agent's next run is also reading the policy. Both sides of the artifact pipeline share one snippet.

---

## Phase 4: Update the reviewer and assessor prompts

### Goal
The reviewer and assessor each carry one explicit check that catches the modular-baseline violation and the value↔class mismatch. False-positive risk (legitimate monolithic-plant citations as literature comparables) is handled in the check's wording.

### Assumption Under Test
That an explicit "rationale baseline frame" check is enough to catch the violation without false-flagging concepts that cite ARC/STEP/etc. as literature comparables.

### Edit stencil
- `review.md` §4 ("Two-Knob Projection & Model Integrity") gains a sub-bullet — or a new §6 ("Override Frame Coherence"), design-call — for: "Every enabled relative override's rationale frames its baseline as the library's modular-fleet default (not a monolithic / 'conventional 1 GWe plant' baseline). Citing a monolithic plant as a literature comparable is fine; using it as the override's anchor baseline is a finding."
- `assessment.md` references the policy via `{{@config/override_semantics.md}}` so the assessor has the same vocabulary.
- `assessment_checklist.md` §2 (Override Discipline) gains the corresponding bullet.

### Changes Required

**Reference:** `spec.md` FR-8, FR-9.

- [x] `review.md` — **decision: extended §2 "Override Discipline"** (not a new §6): the check is fundamentally override-authoring, it keeps the "5 dimensions" narrative intact, and groups with the existing override checks (tighter per NFR). Added two bullets: rationale-baseline frame + value↔class consistency.
- [x] `assessment.md` — added an "Override Semantics" section with the full `{{@config/override_semantics.md}}` include (assessment.md IS `fill_template`'d, so it resolves) so the assessor shares the policy vocabulary.
- [x] `config/assessment_checklist.md` — added a bullet under "2. Override Discipline."
- [x] Both the review and checklist wording draw the literature-comparable vs anchor-baseline distinction explicitly.

### Validation

**Static:**
- [x] Read the review.md check cold. Flags "5% of a conventional 1 GWe plant's buildings" (named the finding); does NOT flag "this concept's published 1 GWe ARC comparable in Sorbom 2015 puts CAS21 at $X" (named legitimate). Both true.
- [x] `assessment.md` renders: `override_semantics` include resolves, checklist baseline bullet present, no leftover token, no `CONFIG FILE NOT FOUND`.
- [x] `test_template_lint.py` — 6 passed after Phase 4 edits.

> **Pre-existing test failures (out of scope, not caused by this work item):**
> `test_loop_wiring.py::test_costingfe_gate_accepts_helper_form` and
> `test_canonical_accounts.py::test_all_enums_match_library` fail due to library
> enum drift (`STEADY_FRC` added to `ConfinementConcept`). Both exercise Python
> validators/enums, not prompt templates; this work item touched only `.md` files
> (verified via `git status`: zero `.py` modifications). Flag to the modeling side.

**What We Know Works After This Phase:** A reviewer pass on a violating concept would produce a REVISE on the baseline-framing check.

---

## Phase 5: End-to-end verification on a fresh concept

### Goal
Confirm the policy lands in agent behavior by running one previously-affected concept fresh through analyze → model-setup → review and inspecting outputs.

### Assumption Under Test
That the prompt edits collectively shift agent output — not just the prompt text. This is the only phase that proves the work item.

### Concept selection
- Default: **24-dense-plasma-focus** (`P_native = 5 MWe`, the most-exposed concept in the research, multiple Class-S/U/P relative overrides). User picks; this is a recommendation.

### Steps
- [ ] User checks out a fresh branch off `main` (or current) for the run.
- [ ] User runs the concept fresh through the pipeline (analyze → model-setup → review) per the standard CLI.
- [ ] Inspect `analysis.md` Section 5b: every relative override entry's `rationale` names the modular-fleet baseline; none invoke "conventional 1 GWe plant" / monolithic framing.
- [ ] Inspect `model_setup.py`: every relative override's value-anchor matches its account's class per the snippet table (per-module M$ for sub-account anchors, whole-plant M$ for top-level anchors).
- [ ] Inspect `review.md`: the rationale-baseline check appears in the strategic-assessment narrative, and the verdict is PROCEED on that check (it may REVISE for other reasons — that's fine).
- [ ] Compare the headline LCOE against the prior run for the same concept. The number is allowed to change (the prior run's overrides were under the wrong baseline frame). Whatever it lands on, the rationale-to-value coherence is the success criterion, not numeric stability.

### Validation

**Manual:**
- [ ] User confirms the rationale prose reads cleanly against the policy.
- [ ] User confirms no class-vs-anchor mismatch in the override registry.
- [ ] User confirms the reviewer caught the right things (or, if no findings, that the rationale-baseline check appears explicitly in the narrative).

**What We Know Works After This Phase:** The policy reaches agent behavior on a fresh run. Confidence is high enough to move to the follow-up spec for re-authoring existing concepts.

---

## Environment Setup

**See CLAUDE.md for full environment rules** — `uv run python ...` for any pipeline command. Prompt edits don't need a venv.

---

## Risk Management

**Phase-Specific Mitigations:**
- **Phase 1**: Snippet fractures into per-class rules under length pressure. → Discipline test in Phase 1 validation: snippet is removable down to the invariant sentence and still teaches the rule; the class table is for authoring shape only.
- **Phase 2**: Inline example slips back into the C220101-anchored-to-CAS21 mismatch. → Pick the example shape up front (Phase 2 stencil offers two valid options) and write rationale in the modular-fleet frame.
- **Phase 3**: Wording drift between the snippet and the analysis-side prompts. → Use `{{@include}}` everywhere possible; quote the snippet verbatim where include doesn't work.
- **Phase 4**: Reviewer false-flags ARC/STEP literature citations. → The check's wording draws the distinction between "rationale baseline frame" and "literature comparable mention" explicitly.
- **Phase 5**: Concept run produces a wildly different LCOE and we second-guess the policy. → The success criterion is rationale-to-value coherence, not numeric stability. The prior run was under the wrong frame; the new number is the right one regardless of magnitude.

## Implementation Notes

**Implemented:** 2026-06-06 (Phases 1–4; Phase 5 is the user's run).

**Key cross-cutting finding — template engine has no nested includes.**
`templating.py:fill_template` resolves `{{@rel}}` in a single, non-recursive
`re.sub` pass (included text is not re-scanned). Consequences that shaped the
implementation:
- The snippet (`config/override_semantics.md`) must contain **no** `{{@...}}`.
- `config/account_walkthrough.md` is itself `{{@}}`-included into `analysis_v2.md`,
  so it can only **point to** the class table, not include it.
- `config/quality_standards.md` could not pull the orientation from
  `analysis_goals.md` — the paragraph is **duplicated** in both.
- `output_template.md` is read **raw** by the agent (`output_template_path`),
  never `fill_template`'d, so it carries a **condensed inline** statement, not an
  include. The full snippet therefore lives in `analysis_v2.md` (rendered) and
  `model_setup_costingfe.md` Rule 5 (rendered) — the two prompts both agents read,
  satisfying FR-11.

### Phase 1 Completion
Created `config/override_semantics.md`: invariant-first (`account = M × library 1
GWe fleet cost`), S/U/P class table with an **authoring-shape** column (no
"what-M-means" column), modular-fleet rationale baseline, storage-shape footnotes
(CAS80 top-level; CAS40/CAS70 not overridable per `#106`), and "what wrong looks
like" examples. Discipline test holds: the invariant alone answers
`0.70 * generic.costs.cas21`.

### Phase 2 Completion
`model_setup_costingfe.md`: rewrote the §2b `generic` gloss (writing frame +
`_scale_overrides` rescale reference + class-free headline invariant); fixed the
inline relative example from the documented bug (`C220101 → generic.costs.cas21`,
a U-sub-account anchored to an S-rollup) to `C220101 → generic.cas22_detail
["C220101"]` with a modular-fleet rationale; inserted the snippet include in Rule 5
and fixed the top-level pattern example to a matching account (`CAS24 →
generic.costs.cas24`). Render test: include resolves, no leftover tokens.

### Phase 3 Completion
`analysis_v2.md` Override Candidate Discovery now embeds the full snippet (deviation
from plan — see cross-cutting finding); `output_template.md` §5b carries the
condensed invariant + baseline + S/U/P gloss inline; `account_walkthrough.md` gains
a "identify cost class first" step pointing to the table; `analysis_goals.md` and
`quality_standards.md` each carry the "headline is the replicated 1 GWe fleet"
orientation paragraph. Renders clean; template lint 6/6.

### Phase 4 Completion
`review.md` §2 gains rationale-baseline-frame + value↔class-consistency checks with
the literature-comparable vs anchor-baseline distinction; `assessment.md` embeds the
snippet for shared vocabulary; `assessment_checklist.md` §2 gains the matching
bullet. Renders clean; template lint 6/6. Two pre-existing unrelated test failures
(library `STEADY_FRC` enum drift) noted in Phase 4 validation — not caused by this
work item (only `.md` files touched).

### Phase 5 Completion
**Run by user** on 24-dense-plasma-focus. Audit outcome: the policy reached the
analysis and assessment agents and the produced overrides were class-consistent and
in the modular-fleet frame (no monolithic-baseline violations; invariant verified
live on CAS26: `0.27 × fleet 128.1 = 34.6`). The original sub-account-anchored-to-
top-level-rollup bug was absent. The run's FAIL verdict was driven by non-policy
findings (C220102 enabled/count dispute — resolved by runtime probe `generic
C220102 = 0.0404 ≠ 0`; and an override-count/C220200 finding), not by the
baseline-framing checks.

**Two gaps surfaced by the audit and fixed (2026-06-06, post-Phase-5):**
1. **Edit-template gap (the important one).** Feedback/resume iterations render the
   model-setup agent from `model_setup_costingfe_edit.md` (loop.py:773), which was
   NOT in spec scope and so never got the policy — the iter-2 `model_setup_prompt`
   had 0 occurrences of the invariant. Added `{{@config/override_semantics.md}}` to
   the edit template (rendered via `fill_template`; include resolves). Now both the
   cold-start and feedback model-setup paths carry the policy.
2. **CAS80 listed as overridable.** CAS80 overrides are a silent no-op in the
   library (absolute and relative both leave the fleet value at the library default;
   consistent with the pinned CAS70/CAS80 no-op test). Updated the snippet to group
   CAS80 with CAS40/CAS70 as "taught but not overridable today" so agents don't
   author dead CAS80 overrides.

Both fixes validated: edit template renders with the include resolved; snippet has
no forbidden strings/stray tokens; `test_template_lint.py` 6/6.

**Still open (not a prompt issue):** the C220102 dispute should land as `enabled:
True` and the concept-dir model regenerated to clear the STALE marker and the
blocking finding — discussion pending with user.

### Phase 5 verification — clean re-run (2026-06-06, after the model-setup timeout fix)

Re-ran `analyze 24 --force --max-passes 2`; both iterations converged fast
(model-setup 222s / 88s), `model_ran=True / model_ok=True`, canonical model NOT
stale, headline LCOE 13.5 $/MWh.

**Policy success criteria — PASS:**
- Policy reached **all three** agents in **both** iterations (invariant present in
  every rendered analyze/model-setup/assess prompt — the edit-template include
  closed the iter-2 model-setup gap).
- `analysis.md` + `model_setup.py`: **zero** monolithic / "conventional 1 GWe plant"
  anchor-baseline violations; modular-fleet framing present in both; override counts
  consistent (4 = 4).
- Invariant holds live: CAS26 `0.26 × fleet` scales correctly; probe confirmed the
  Class-U overrides also reach the fleet (C220107 abs 0.30 → +60.11 = ×200; C220110
  rel 0.10×gen → −155.88 = ×200).
- The new **value↔class / baseline check fires** (assessment F-1) — the check is
  active, using the S/U/P vocabulary from the snippet.

**DEFECT found by verification — the value↔class check FALSE-POSITIVES.**
Assessment F-1 (blocking) flagged "Class-U overrides C220107/C220110 don't scale to
the fleet frame," reasoning from the CAS22 sub-account **detail rows** being identical
at native and 1 GWe. But that detail table shows **per-module M$ at all scales by
design**; the ×n_mod scaling lives in the C220000 / CAS22 rollup. Probe proves both
overrides scale correctly (above), so F-1 is a false positive — and a *blocking* one
that would send the model-setup agent to "fix" a non-bug (likely breaking correct
overrides). Root cause: the snippet's value↔class guidance (and the review/assessment
check wording) never tells the reviewer that the per-module detail row is *supposed*
to be constant across scales, and that fleet scaling must be checked in the
C220000/CAS22 rollup. **Fix applied (2026-06-06):** added a "Reading the output — how to verify a Class-U
override actually scaled" footnote to `override_semantics.md` (per-module detail
table is identical across scales by design; verify scaling in the `C220000`/`CAS22`
rollup, not the detail row), and folded the same caveat into the value↔class check
in `review.md` §2 and `assessment_checklist.md` §2. Validated: all four
policy-embedding templates render with the caveat; `test_template_lint.py` 6/6.

### Phase 5 verification — CONFIRMED via converging clean cold-start run (2026-06-06)

`analyze 24 --force --max-passes 2`: **iter-1 FAIL (3 findings) → iter-2 PASS (0
findings)**, model_ok=True both iters, canonical model not stale, LCOE 14.3 $/MWh.

- **No monolithic-baseline violations** in `analysis.md`/`model_setup.py` (the only
  "monolithic" hit is "monolithic tungsten" — an electrode material, not a cost frame).
- **Policy reached all three agents in both iterations.**
- **The F-1 false-positive pattern did NOT recur.** Instead the assessor used the S/U/P
  vocabulary correctly: iter-1 F-1 flagged that `0.40 * generic.cas22_detail["C220107"]`
  is **vacuous because the library zeros C220107 for DPF** (relative override on a zero
  baseline = 0), and explicitly distinguished it from the *harmless* C220101/C220102
  zeros. Probe confirms the catch was true (relative form → fleet Δ +0.07) and the
  applied fix (absolute `0.40`) is correct (fleet Δ +80.11 = 200 × 0.40).
- **Final model is genuinely correct, not papered over:** all 7 overrides
  class-consistent (Class-U sub-accounts → `cas22_detail` or absolute per-module;
  Class-S/P → `generic.costs.<rollup>`); the vacuous C220101/C220102 entries were
  removed per the finding; C220107 reaches the fleet.

**All spec success criteria met. Work item complete** (the residual F-2 "LCOE looks
low" is a domain-plausibility judgment the assessor weighed and passed — not a policy
issue). Defect A from the model-setup-timeout ticket remains the only open thread, and
it is tracked separately.

---

**Status:** Draft → **In Progress** (Phases 1–4 complete; Phase 5 pending user run)
