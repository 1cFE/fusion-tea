# Spec: Prompt Template Rework (Concept-Analysis Rework, Item 8)

**Status:** Complete (2026-05-31 — all ACs validated by the ARC Phase-5 pilot)
**Owner:** Reid W
**Created:** 2026-05-31
**Complexity:** MEDIUM
**Branch:** `concept-analysis-rework`
**Epic:** [`epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 8

---

## Work Item Summary

Rework the concept-analysis prompt-template suite (`analysis_v2.md`, `output_template.md`, `model_setup_costingfe*.md`, `assessment.md`, `review.md`, and their `config/` includes) so the new pipeline contract — one named design point per concept, library-as-default story, six-field override registry, two-knob 1 GWe NOAK projection — flows through every prompt. **In the same atomic change**, rewrite the internals of the four named parsers that today read the old assess/review/proposed-actions format (so they read the new format while preserving their return shapes per [`signal_contract.md`](../concept-rework-helpers-validators/signal_contract.md)), wire Item 7's output-gate validators into the model-setup three-branch validator selection in `loop.py` (all three branches, not just edit-pass) with `strict_helper_only=True`, wire its coherence checks into the assess surface, and discharge Item 7's FR-9 ("loop runs cleanly without the dropped validators"). Phase 0's hand-drafts in `.project/active/concept-rework-prototype/prompts/` are read for inspiration but **not lifted**; they were written in a hurry against an earlier shape and predate Item 5's move of design-point *selection* upstream. The pipeline's "downstream of selection" prompts — extract, set up the model, assess, review — are rewritten from the new contract directly, and the live-loop parsers swap formats in lockstep with the prompts so the loop never observes a "new prompt + old parser" mismatch.

## Why This Matters Now

Item 8 is the pacing gate before the Item 10 pilot and Item 11 bulk regen. Item 4 (library preconditions) and Item 6 (frontmatter / orchestrator) have landed; Item 5 (upstream tables) and Item 7 (helpers + validators) are in flight. Until the prompts speak the new contract, no concept can be regenerated to the four-step `model_setup.py` shape, and the cross-concept `result_1gw @ 1000 MWe` invariant fails by construction. Phase 0 also surfaced concrete prompt-level defects that the current templates would silently ship at scale:

- the analyze step picks an `account` namespace (`CAS22.1.3`) that doesn't match the library's canonical codes (`C220103`) — a typo-class bug that would make `cost_overrides` silently miss
- open-ended override discovery underproposes (Phase 0 surfaced 2 of 4 legitimate ARC overrides)
- operator-vs-LLM cross-artifact drift (`P_native` mismatch, `provenance` label drift) is a recurring failure mode the prompts can pre-empt by making the contract explicit

## Key Bets / Constraints

- **Bet:** Most of the discipline lives in the *prompt*, not the validator. Validators (Item 7) catch shape violations; the prompt is what keeps the LLM from producing nonsense in the first place. A schema-injected canonical account list, a per-account walkthrough checklist, and an explicit "read `P_native` from frontmatter — do not choose" instruction are higher-leverage than after-the-fact regex.
- **Constraint:** `model`, `result`, `result_1gw` module-level contract for `concept_explorer` is preserved.
- **Constraint:** `result_1gw` is reached by the two-knob call `forward(net_electric_mw=1000, n_mod=1000/P_native, override_reference_mw=P_native, …)` — no other mechanism produces it.
- **Constraint:** Design-point *selection* (`Design-Point-Name`, `Design-Point-Maturity`, `P-Native`, `Grounding-Confidence`) is owned by Item 5's table and reaches the analyze step via orchestrator-populated frontmatter. The analyze prompt **does not choose** the plant.
- **Constraint:** [`signal_contract.md`](../concept-rework-helpers-validators/signal_contract.md) pins the return shapes the four rewritten parsers must preserve. Item 8 changes parser *internals* (the format they read); call sites and signatures do not move.
- **Constraint:** The generated `model_setup.py` uses Item 7's `run_native_and_1gw(model, spec, overrides, p_native, *, noak=True) → (result, result_1gw)` helper. This is the form Item 7's `validate_model_setup_contract(..., strict_helper_only=True)` accepts; the inline two-knob `forward()` form is rejected once the switch flips.
- **Non-goal:** `model_setup_freeform*.md` — deferred per epic non-goal.
- **Non-goal:** `model_critic.md` — Item 9.
- **Non-goal:** `design_point_proposal.md` — Item 5, already shipped.
- **Non-goal:** Modifying Item 7's *helper* or *validator* APIs (`run_native_and_1gw`, `validate_model_setup_contract`, `validate_override_registry`, `validate_design_point_coherence`, `check_override_count_vs_fit_grade`, `enabled_overrides`). Item 8 *wires* and *uses* them; it does not change their signatures. New tests for the wired-in behaviour belong to Item 8.
- **Non-goal:** Restructuring `synthesize` and `score`; touched for the `Reuses:` → `Comparables:` rename only.

---

## Business Goals

### Why This Matters

Cross-concept LCOE comparison is only honest if every concept is processed against the same contract: one named plant specified up front, library carrying the default story, overrides as accountable six-field entries, projection at 1 GWe via the same two-knob call. The prompts are where that contract is articulated to the analyzing and model-setup agents. The Item 1 prototype proved the contract works on one concept when the prompts are right; Item 8 productionizes "the prompts are right" so the pilot (Item 10) and bulk regen (Item 11) can run.

### Success Criteria

- [ ] A dry-run of the new `analysis_v2.md` against one concept (ARC, concept 01) produces an `analysis.md` with a complete Design Point block — selection fields matching the frontmatter row, plus an extracted quantitative description (geometry / physics / performance) that all describes that one plant.
- [ ] A dry-run of the new `model_setup_costingfe.md` against the same concept's regenerated `analysis.md` produces a `model_setup.py` matching the four-step shape: `spec` + `P_native`, native `forward(net=P_native, n_mod=1, …)`, override registry list-of-dicts, two-knob `forward(net=1000, n_mod=1000/P_native, override_reference_mw=P_native, …)`. `model`, `result`, `result_1gw` are at module level.
- [ ] Override-registry entries emitted by the analyze step pin `account` to a canonical 1costingFE code (drawn from a schema injected into the prompt) — not `CAS22.1.3`-style codes.
- [ ] Override discovery is an explicit per-account walkthrough; the prompt forces the LLM to consider each canonical account against the dossier rather than discover ad-hoc.
- [ ] Assess/review prompts emit findings that parse robustly under the new artifact shape (no reliance on dropped regex paths) and use the `Archetype-Fit` grade from frontmatter as the expected-override-count baseline.

### Priority

P0 within the epic. Blocks Items 10 and 11. Can run in parallel with Item 7 (helpers + validators) — the two interlock at the artifact-shape level but neither depends on the other's internals.

---

## Problem Statement

### Current State

- `analysis_v2.md` drives an 8-section narrative with no Design Point block, no override-candidate emission, and no awareness that selection is now upstream-determined. It assumes the LLM will pick what to model.
- `model_setup_costingfe.md` instructs the LLM to re-pass library defaults with `# DEFAULT: framework value` comments, to use `override_reference_mw` only conditionally (the "Dual-Result Pattern" branches on whether `P_native == 1000`), and frames cost overrides as ad-hoc inline `cost_overrides={…}` dicts rather than a six-field registry. It explicitly tells the LLM that "framework defaults with `# DEFAULT: …` comments" are acceptable for unknowns — the exact antipattern the rework exists to remove.
- `assessment.md` / `review.md` / `feedback_format.md` use a verdict regex and `F-N` format that the loop validators currently parse via fragile patterns. The new prompts have to emit a shape that survives without those regex paths.
- `config/quality_standards.md` and `config/assessment_checklist.md` predate the rework; they don't reference `Comparables:` (still `Reuses:`-flavoured), the design-point discipline, or override accountability.
- `synthesis.md` and `score.md` reference `Reuses:` indirectly through the frontmatter convention; they need a leak-through rename only.

### Desired Outcome

Every prompt in scope speaks the new contract natively. The analyze prompt reads selection as fixed input and extracts a complete quantitative description for that fixed plant. The model-setup prompt starts from the Design Point block (not the dossier), emits the four-step shape, and forbids re-passing library defaults. The assess/review prompts use frontmatter as ground truth, check override count against fit grade, and emit findings tied to the new artifact shape.

---

## Scope

### In Scope

**Prompt templates** in `exploration/concept_analysis/prompt_templates/`:

- **Analyze (extraction):** `analysis_v2.md`, `output_template.md`
- **Model setup:** `model_setup_costingfe.md`, `model_setup_costingfe_edit.md`
- **In-loop review:** `assessment.md`, `review.md`
- **Config includes:** `config/feedback_format.md`, `config/assessment_checklist.md`, `config/analysis_goals.md`, `config/quality_standards.md`
- **Rename leak-through only:** `synthesis.md`, `score.md` (`Reuses:` → `Comparables:` references; no structural change)

**Parser internals** (rewrite to read the new format; preserve signatures + return shapes per `signal_contract.md`):

- `scripts/lib/iteration.py::parse_verdict_from_feedback` — returns `tuple[str, int]`
- `scripts/lib/validators.py::has_model_category_findings` — returns `bool`; uncategorized findings stay conservative `True` (note: on the model-setup *generation* route — `loop.py` calls it to pick the feedback-pass validator chain — not just an assess-time concern)
- `scripts/lib/validators.py::{validate_feedback_verdict, validate_review_verdict}` — return existing `ValidationResult` shape; verdict tokens `PASS`/`FAIL` and `PROCEED`/`REVISE` preserved
- `scripts/lib/sources.py::parse_proposed_actions` — returns `list[dict]` with the nine keys (`id, description, category, severity, location, finding, proposed_fix, decision, user_notes`)

**Loop control-flow wiring** (Item 7's already-shipped validators):

- Wire `validate_model_setup_contract` + `validate_override_registry` into **each** of the three model-setup output-gate validators selected by `loop.py`'s `# --- Validator selection ---` block (edit-pass-with-model-findings, edit-pass-analysis-only, cold-start) — not only the edit-pass branch
- Flip `strict_helper_only=True` on `validate_model_setup_contract` so the generated `model_setup.py` cannot regress to an inline two-knob `forward()`
- Wire `validate_design_point_coherence` (three-leg, including `analysis.md`) and `check_override_count_vs_fit_grade` into the assess surface as LLM-reviewer flag inputs, matching the pattern `comparables_sanity_check.py` already uses
- Drop the regex paths that the rewritten parsers replace (named constants `FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE`, `PROPOSED_ACTION_RE` and their direct uses); discharge Item 7's deferred FR-9

**Common-var assembly** (extensions per design):

- `scripts/run_analysis.py::_build_common_vars` — add substitution keys the new templates consume
- `scripts/lib/loop.py::build_model_vars` — drop empty placeholders (`defaults_path`, `mapping_notes`); add the new keys

### Out of Scope

- `model_setup_freeform.md`, `model_setup_freeform_edit.md` — deferred branch (epic non-goal)
- `model_critic.md` — Item 9
- `design_point_proposal.md` — Item 5, already shipped
- `address_review.md`, `calibrate.md`, `feedback/*`, `gap_check.md`, `research.md`, `resurface.md`, `source_integration.md`, `agents/source_reader.md` — not listed in Item 8; touched only if a structural change in an in-scope file breaks them (in which case the breakage gets a minimal repair, not a rework)
- `config/scoring_framework.md` — content out of scope; rename leak-through only
- **Item 7's validator/helper *signatures and return contracts*** — `validate_model_setup_contract`, `validate_override_registry`, `validate_design_point_coherence`, `check_override_count_vs_fit_grade`, `run_native_and_1gw`, `enabled_overrides`. Item 8 wires and uses them; their public APIs are fixed
- **The four parsers' *signatures and return shapes*** — Item 8 rewrites only the internals per `signal_contract.md`; the call sites (enumerated in `signal_contract.md`; re-resolve by symbol at plan time, since validators.py is actively changing under Item 7) do not move

### Edge Cases & Considerations

- **Item 7 sequencing.** Item 8 depends on Item 7 for helper API and validator contracts. If Item 8 lands first, the prompts template against the raw four-step shape; if Item 7 lands first, the prompts can reference helpers like `build_overrides_dict(overrides)`. Either order works — the prompts target the *contract*, not the helper internals.
- **`Confinement-Family` vs `confinement_family`.** Frontmatter is `Confinement-Family:` post-Item-6; prompt templating must match the orchestrator's field-name convention.
- **Iter-N feedback mode in `analysis_v2.md`.** The current template has three modes (cold-start, feedback-pass, self-advance). The new prompt preserves the three modes, but cold-start now reads frontmatter for selection fields; feedback-pass/self-advance edit an already-conforming Design Point block (do not re-write it).
- **Asterisked concepts (`Comparison-Status: costingfe-asterisked`).** Per Item 6 these go through costingfe with `grounding_confidence: low`. Same prompt path as full-grounding concepts; no prompt branching needed in Item 8.
- **`override_reference_mw` correction propagated to the concept doc.** Concept doc `concept-analysis-rework.md` previously said "`override_reference_mw` is not used"; corrected in this session to "`override_reference_mw=P_native` IS passed" — the design doc was already correct.

---

## Requirement Selection Notes

The normative requirements below cover the contract-level shape every prompt in scope must speak: design-point selection as fixed input, canonical account schema, per-account walkthrough, six-field override entries, the four-step model_setup structure, the two-knob projection call, the no-library-default-re-passing discipline, and parse-robust review output. Everything below that — exact section ordering inside `analysis.md`, the precise rendering of the override walkthrough, the prose of the per-prompt feedback templates, whether Item 7's helper API is referenced by name — is deferred to design.md. The spec does not pin one prompt's prose against another's; it pins the contract.

The single judgment call settled here that could have lived in design: **`spec`-dict discipline for fields that have library defaults** (e.g. `eta_th`). Stated explicitly in FR-7 because it is the easiest place for the new pipeline to silently regress to the old "re-pass everything" antipattern.

---

## Requirements

### Functional Requirements

> Requirements below derive from Item 8's success criteria, the concept and design docs, and Item 1's findings. `[INFERRED]` marks requirements the operator did not state explicitly but follow directly from the contract.

#### Analyze (`analysis_v2.md` + `output_template.md`)

1. **FR-1:** The analyze prompt MUST read the design-point selection fields (`Design-Point-Name`, `Design-Point-Maturity`, `P-Native`, `Grounding-Confidence`) and the `Comparables:`, `Confinement-Family`, `Archetype`, `Archetype-Fit` fields from the concept's orchestrator-populated frontmatter, and MUST treat them as fixed inputs.
2. **FR-2:** The analyze prompt MUST NOT choose, re-derive, or override the design-point selection. If the dossier appears to contradict the selection, the prompt instructs the LLM to *note the contradiction in the analysis prose* and proceed against the fixed selection (it does not write a different `P_native` into the output).
3. **FR-3:** The analyze prompt MUST emit a **Design Point block** as a structured section in `analysis.md`, carrying both the *selection* fields (copied from frontmatter) and the *quantitative description* (geometry, physics, performance) extracted from the dossier for that fixed plant. Every LCOE-relevant parameter in the analysis body MUST describe the unit named in the Design Point block.
4. **FR-4:** The analyze prompt MUST emit an **Override Candidates** section as a YAML registry block. Each entry MUST contain all six fields: `account`, `value`, `enabled`, `provenance`, `source`, `rationale`. `account` MUST be drawn from the canonical 1costingFE account namespace (e.g. `C220101`, `C220103`, `CAS27`).
5. **FR-5:** The analyze prompt MUST inject the canonical 1costingFE account schema (the list of valid `account` codes plus a one-line "what does each account cost" description) into the prompt body, scoped to the concept's `ConfinementConcept` archetype. The schema is a **hand-maintained fusion-tea constant** in `lib/canonical_accounts.py` (the library exposes no introspection surface that would support runtime derivation); a CI/test-time `validate_against_library()` check asserts every account code in the constant appears in `costingfe/layers/`.
6. **FR-6:** The analyze prompt MUST drive override discovery as an explicit per-account walkthrough: for each canonical account, the LLM is asked whether the dossier names a quantity, unit cost, or company-published $ figure for that account. Open-ended "what overrides are needed" framing is forbidden.
7. **FR-7:** The analyze prompt MUST enforce override provenance discipline: `direct` means the company published the exact $ figure (or a quantity × stated unit price both directly stated); anything assembled by the analyst from a published quantity plus an analyst-sourced unit price is `derived`, and the arithmetic MUST appear in `rationale`. CPI inflation factors MUST be shown explicitly in `rationale` when applied.
8. **FR-8:** The analyze prompt MUST set the expected override-count rubric from the `Archetype-Fit` grade read from frontmatter: `High` → 0–4, `Med` → 3–8, `Low` → 6–12. The LLM is told the rubric and asked to flag if its output falls outside the band.

#### Model setup (`model_setup_costingfe.md` + `model_setup_costingfe_edit.md`)

9. **FR-9:** The model-setup prompt MUST instruct the LLM to **start by reading the Design Point block from `analysis.md`** — pulling `P_native`, the design-point spec inputs, and the override registry directly from there. The dossier is a fallback for spec inputs the analysis step did not extract, not the primary source.
10. **FR-10:** The model-setup prompt MUST emit the four-step structure literally, in this order: (1) `spec` dict + `P_native` constant; (2) `model = CostModel(...)`; (3) `overrides` list-of-six-field-dicts; (4) a single call to Item 7's helper: `result, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`. The inline two-knob `forward()` form is forbidden — it is rejected by `validate_model_setup_contract(..., strict_helper_only=True)` once wired (FR-26). `noak=True` is the helper default; do not re-pass it.
11. **FR-11:** `model`, `result`, and `result_1gw` MUST be module-level variables in the generated `model_setup.py` (the prompt explicitly states this).
12. **FR-12:** The model-setup prompt MUST forbid re-passing library defaults via `# DEFAULT: …` comments. The `spec` dict carries only design-point-specified inputs. Specifically: financial / operating-economics parameters that apply uniformly across all fusion concepts — `availability`, `lifetime_yr`, `interest_rate`, `inflation_rate` — MUST NOT appear in `spec`. The library defaults are authoritative.
13. **FR-13:** For parameters that have library defaults per `ConfinementConcept` archetype but represent a *physics characteristic* (e.g. `eta_th`, `eta_de`), the model-setup prompt MUST instruct: include in `spec` only when the concept's design point has a legitimately different value backed by archetype-specific physics (e.g. Helion direct conversion → non-thermal cycle); a company-published "optimistic" value MUST NOT be passed as a `spec` override of the library default. The discipline test: "does 1costingFE's archetype default fail to represent this concept's physics?" — if yes, override; if it's just "we think we'll do better," do not.
14. **FR-14:** Override `value` MAY be (a) a plain number, (b) a constant arithmetic expression that documents its own derivation (e.g. `260.0 * 1.34` for a CPI-inflated published cost), or (c) — for a *relative* override defined as a fraction of the library's own computation — an expression over the **native `result`** (e.g. `0.70 * result.costs.cas21`, "70% of the library's value because the company states a 30% prefab reduction"). The relative form is the correct one for relative overrides; a frozen literal there goes stale when the library updates. The expression MUST reference the native `result` (the `n_mod=1` / `P_native` frame), **not** `result_1gw`. The registry does not constrain `value` to a bare literal; legitimacy is enforced by `provenance`/`source`/`rationale` (and the critic), not by value syntax — a rule on the value's form cannot tell an evidence-backed relative override from an un-evidenced fudge. (Matches the design-doc Override Entry and Item 7's `validate_override_registry`, which accepts these forms and rejects `result_1gw` references.)
15. **FR-15:** The model-setup prompt's feedback-pass variant (`model_setup_costingfe_edit.md`) MUST apply targeted edits against an existing four-step `model_setup.py`, preserving the structure. It MUST NOT restructure conforming code.
16. **FR-16:** Sweep / sensitivity / what-if `print()` output remains allowed in `model_setup.py` stdout (consumed by `model_output.txt`). Only `result` and `result_1gw` are the standardized baseline.

#### Assess / review (`assessment.md`, `review.md`, `config/feedback_format.md`, `config/assessment_checklist.md`)

17. **FR-17:** The assessment prompt MUST consume `analysis.md`'s Design Point block and Override Candidates block, and `model_setup.py`'s `overrides` list, as structured artifacts — without relying on the dropped FINDING/VERDICT regex paths in the validator. Findings parse from a markdown structure stable under prompt-template iteration (specific format owned by design.md).
18. **FR-18:** The assessment prompt MUST check override count against the `Archetype-Fit` grade read from frontmatter, and flag inconsistencies: `High` with > 4 enabled overrides → flag; `Low` with 0 → flag.
19. **FR-19:** The assessment prompt MUST keep the existing two-category `analysis | model` `Category` tag on each finding. The new contract's *registry / design-point* failure modes (P_native mismatch, provenance drift, account-namespace miss) fall under `analysis` when the fix is in `analysis.md` and `model` when the fix is in `model_setup.py`. A third category is NOT introduced.
20. **FR-20:** The review prompt (`review.md`) MUST preserve the `PROCEED | REVISE` verdict and the PA-N / F-N finding formats, but its `Strategic Assessment Dimensions` MUST be updated to reflect the new contract: design-point coherence replaces "modeling approach" framing; override discipline replaces "CAS mapping defensibility"; `Comparables:` (frontmatter-fixed) replaces "cross-concept consistency" with "is the family-delta prose against the fixed comparables list specific and right."

#### Config and rename leak-through

21. **FR-21:** `config/quality_standards.md` MUST reflect the new discipline: library is the default story; every analysis parameter describes the design point; no re-passing of library defaults; six-field override entries with honest provenance.
22. **FR-22:** `config/assessment_checklist.md` MUST be rewritten against the new contract (design-point coherence, override discipline, family-delta against fixed comparables, two-knob projection invariants).
23. **FR-23:** `config/analysis_goals.md` MUST acknowledge that positioning, nearest-neighbor selection, and archetype mapping are *upstream-fixed* (orchestrator-populated) — the analyzing agent's job is family-delta articulation, not family discovery.
24. **FR-24:** `synthesis.md` and `score.md` MUST be updated for the `Reuses:` → `Comparables:` rename leak-through. No structural change beyond field-name updates.

#### Parser rewrite + loop wiring (Item 7-deferred work)

25. **FR-25:** The internals of the four parsers named in `signal_contract.md` (`parse_verdict_from_feedback`, `has_model_category_findings`, `validate_feedback_verdict` + `validate_review_verdict`, `parse_proposed_actions`) MUST be rewritten to read the new assess/review/proposed-actions format. Each MUST preserve its existing signature and the return shape pinned in `signal_contract.md`:
    - `parse_verdict_from_feedback → tuple[str, int]` with `"PASS" | "FAIL"` and the finding count
    - `has_model_category_findings → bool`; uncategorized findings remain conservative `True`
    - `validate_feedback_verdict`, `validate_review_verdict → ValidationResult` (existing shape); tokens `PASS`/`FAIL` and `PROCEED`/`REVISE` preserved
    - `parse_proposed_actions → list[dict]` carrying the nine required keys (`id, description, category, severity, location, finding, proposed_fix, decision, user_notes`)
26. **FR-26:** `validate_model_setup_contract(strict_helper_only=True)` and `validate_override_registry` MUST be chained into the model-setup output-gate validator picked by **each** of the three branches in `loop.py`'s `# --- Validator selection ---` block (today: edit-pass-with-model-findings, edit-pass-analysis-only, cold-start — all three currently use different validators and none of them today gates the contract). A cold-start `model_setup.py` MUST be held to the same contract as a feedback-pass file.
27. **FR-27:** `validate_design_point_coherence` (three-leg: `design_point.csv` row + `model_setup.py` text + `analysis.md` text) and `check_override_count_vs_fit_grade` MUST be wired into the `assess` surface as flag inputs to the LLM reviewer. This is **net-new construction** in `_run_assess` (no existing flag-feed surface; `comparables_sanity_check.py` exists as a standalone script but is not currently wired into the assess path). Plumbing the `design_point.csv` row to `_run_assess` is a sub-requirement. The LLM reviewer assesses; the checks do not gate.
28. **FR-28:** The regex constants the rewritten parsers replace (`FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE`, `PROPOSED_ACTION_RE`) and their direct uses MUST be removed in the same change. Item 7's deferred FR-9 ("loop runs cleanly without the dropped validators") is discharged here.
29. **FR-29:** Item 8's prompt rewrite, parser rewrite, loop wiring, and regex removal MUST land atomically as a single merge unit. The loop MUST NOT, at any point in Item 8's change history, observe a "new prompt + old regex parser" pairing or "new helper-form `model_setup.py` + un-wired contract validator" pairing. Item 7's library changes (helper, validators, coherence checks, signal_contract.md) MAY land as a separate commit *immediately preceding* Item 8 (Option A in design.md "Item 7 sequencing"); Item 7 is by-design a no-op on loop control flow, so this two-commit sequence keeps the loop green between commits. Items 7 + 8 in one merge (Option B) is also acceptable.

### Non-Functional Requirements

- **NFR-1:** The reworked prompts SHOULD be small enough to run cleanly under Sonnet 4.6 with the dossier and frontmatter loaded; Phase 0 demonstrated Sonnet handles the analyze prompt at ~$0.15/run. Opus is reserved for fall-back on quality issues, not as a default.
- **NFR-2:** The canonical 1costingFE account schema injected into the analyze prompt SHOULD be derived from the library at template-render time (not hand-pasted), so the schema cannot drift from the library. Design.md decides the exact injection mechanism.

---

## Acceptance Criteria

### Core Functionality

- [ ] **Analyze dry-run (ARC, concept 01) emits a complete Design Point block.** Selection fields match the frontmatter row; geometry / physics / performance values are extracted from the dossier and describe one named plant at native scale. (FR-1, FR-2, FR-3)
- [ ] **Analyze dry-run emits a YAML Override Candidates block** with all six fields per entry, `account` codes drawn from the canonical 1costingFE namespace, and CPI / arithmetic chains visible in `rationale` for `derived` entries. (FR-4, FR-5, FR-7)
- [ ] **Analyze prompt forces per-account walkthrough.** A reviewer reading the prompt can name the discipline: "for each canonical account, is there company data that justifies an override." (FR-6)
- [ ] **Override count band check.** Analyze output for ARC (High fit) lands 0–4 enabled overrides; if it lands outside the band the prompt's flag-mechanism surfaces it. (FR-8)
- [ ] **Model-setup dry-run (ARC) emits a four-step `model_setup.py`** that calls `result, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`; `model`, `result`, `result_1gw` are at module level. `validate_model_setup_contract` accepts the file with `strict_helper_only=True`. (FR-9, FR-10, FR-11, FR-26)
- [ ] **No re-passed library defaults.** No `# DEFAULT: …` comments in the generated `model_setup.py`; `spec` dict carries only design-point-specified inputs; `availability` / `lifetime_yr` / `interest_rate` / `inflation_rate` absent from `spec`. (FR-12)
- [ ] **`eta_th` discipline holds.** ARC's `model_setup.py` does not pass `eta_th` unless the design point cites a physics-grounded distinct value; "Helion direct conversion → custom `eta_th`" is allowed under FR-13. (FR-13)
- [ ] **Override `value` accepts expressions.** A constant-expression entry (`value: 260.0 * 1.34`) and a relative entry over the native result (`value: 0.70 * result.costs.cas21`) both survive the prompt → generated `model_setup.py` round-trip and pass `validate_override_registry`; a `result_1gw`-referencing value is rejected (frame error). (FR-14)
- [ ] **Assess / review against new artifacts.** Assessment prompt run against ARC's regenerated artifacts emits findings keyed to design-point coherence, override discipline, and fit-grade band-check; verdict and findings parse cleanly without the dropped regex paths. (FR-17, FR-18, FR-19, FR-20)
- [ ] **`Reuses:` → `Comparables:` rename complete.** No `Reuses:` references remain in any in-scope prompt template. (FR-24)

### Quality & Integration

- [ ] **End-to-end loop dry-run on the ARC concept lands green** with the new prompts + rewritten parsers + wired-in contract validators + `strict_helper_only=True` + coherence checks wired into assess — and zero references to the removed regex constants remain in the tree (`FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE`, `PROPOSED_ACTION_RE`). Discharges Item 7's FR-9. (FR-25, FR-26, FR-27, FR-28, FR-29)
- [ ] The four rewritten parsers' return shapes match `signal_contract.md` row-for-row; existing call sites are unchanged. (FR-25)
- [ ] No prompt references `Reuses:`, `result_1gw_native`, or `# DEFAULT: framework value` patterns.
- [ ] No generated `model_setup.py` contains an inline two-knob `forward()` call — the helper form is the only accepted shape. (FR-10, FR-26)

---

## Next-Stage Handoff

**Settled in this spec:**

- The contract every in-scope prompt must speak (design-point selection as fixed input from frontmatter; canonical-account schema; per-account walkthrough; six-field overrides; four-step model_setup; two-knob projection with `override_reference_mw=P_native`; no re-passed library defaults; `eta_th`-class discipline distinction; expressions allowed in `value`; two `analysis | model` categories on findings).
- File list in scope and out of scope.
- The Phase 0 prompts are reference-only — not lifted.

**Design must figure out:**

- Exact section ordering and prose inside the new `analysis_v2.md` (cold-start / feedback-pass / self-advance mode handling).
- Exact structure of the Design Point block inside `output_template.md` — fields, table vs prose, placement relative to Section 5.
- Exact mechanism for injecting the canonical 1costingFE account schema (template-rendered from library? hand-maintained constant? Item 7 helper?). NFR-2 prefers library-derived but defers the call.
- The structural shape of the Override Candidates YAML block in `analysis.md` (fenced YAML? sub-section per entry? table?), with the constraint that Item 7's validator can parse it cleanly.
- The exact `model_setup_costingfe.md` instruction sequence (how the prompt walks the LLM from "read Design Point block" to "emit four-step script"), and how it interacts with Item 7's helper API if that lands first.
- Whether the assess / review prompts need any new field in the F-N format (the spec says no third Category; design decides if any sub-field is added).
- How the per-account walkthrough is rendered in the prompt (checklist, table, prose for-each).

**Watch-outs for design:**

- **Prompt size.** The canonical-account schema + per-account walkthrough + Design Point block instructions + mode branches risks bloating `analysis_v2.md`. Keep the schema injection minimal and consider moving the per-account checklist into a `config/account_walkthrough.md` partial.
- **Mode confusion.** Cold-start / feedback-pass / self-advance in `analysis_v2.md` already have three sets of instructions; the new contract adds more discipline. Make sure each mode is independently coherent — Phase 0's hand-draft conflated them, and the new prompt must not.
- **Item 7 helper coupling.** If Item 7's helper API is referenced by name in the model-setup prompt, the prompt fails until Item 7 lands. Prefer instruction patterns that work with or without the helpers — the helpers are a convenience, not a contract.
- **`Confinement-Family` casing.** The frontmatter is hyphen-cased post-Item-6; the prompt templating substitution variables in lower-snake_case. Don't conflate.
- **Operator-vs-LLM cross-artifact drift.** Phase 0 surfaced this as bidirectional. The prompts can't catch operator drift directly (the operator edits the file after the LLM runs) — that's Item 7 validator territory — but the prompts SHOULD make the cross-artifact contract visible enough that operator drift is hard to introduce by accident.

---

## Related Artifacts

- **Epic:** [`.project/backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 8
- **Concept doc:** [`.project/concepts/concept-analysis-rework.md`](../../concepts/concept-analysis-rework.md) (note: `override_reference_mw` corrected in this session)
- **Design doc:** [`.project/concepts/concept-analysis-rework-design.md`](../../concepts/concept-analysis-rework-design.md)
- **Phase 0 prototype findings:** [`.project/active/concept-rework-prototype/findings.md`](../concept-rework-prototype/findings.md)
- **Phase 0 hand-drafted prompts (reference only — do NOT lift):** [`.project/active/concept-rework-prototype/prompts/`](../concept-rework-prototype/prompts/)
- **Item 5 design-point proposal prompt (selection — out of scope here):** `exploration/concept_analysis/prompt_templates/design_point_proposal.md`
- **Item 6 frontmatter conventions:** `exploration/concept_analysis/scripts/lib/frontmatter.py`
- **Sibling specs (parallel Phase 1 work):** [`.project/active/concept-rework-helpers-validators/`](../concept-rework-helpers-validators/) (Item 7, if present)
- **Next:** `design.md` in this directory

---

**Next Steps:** After spec approval, proceed to `/_my_design`. Design.md will pin the per-prompt structure, the canonical-account schema mechanism, and the assess/review parse format.
