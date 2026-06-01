# Design: Prompt Template Rework (Concept-Analysis Rework, Item 8)

**Status:** Implemented (2026-05-31 — Phases 1–5 complete; see plan.md + pilot_report.md)
**Owner:** Reid W
**Created:** 2026-05-31
**Branch:** `concept-analysis-rework`
**Commit at draft:** `9cc9675`
**Spec:** [`spec.md`](./spec.md)
**Epic:** [`epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 8

---

## Overview

Rewrite the analyze / model-setup / assess / review prompt templates so the new pipeline contract (one named design point per concept, library-as-default story, six-field override registry, two-knob 1 GWe NOAK projection) is expressed in prose the LLMs actually follow. In the **same atomic change**, swap the live-loop parsers that today read the old assess/review/proposed-actions format to read the new format (preserving the signatures and return shapes pinned in `signal_contract.md`), wire Item 7's output-gate validators into the model-setup three-branch validator selection in `loop.py` (all three branches, not just edit-pass) with `strict_helper_only=True`, wire the coherence checks into the assess surface, drop the four regex constants the rewritten parsers replace, and discharge Item 7's deferred FR-9. The atomicity is load-bearing: the loop must never observe a "new prompt + old parser" pairing, because that pairing breaks verdict, model-category, and PA-action signals — which is exactly the seam Item 7's hybrid design was built around.

## Related Artifacts

- **Spec:** [`spec.md`](./spec.md)
- **Concept doc:** [`../../concepts/concept-analysis-rework.md`](../../concepts/concept-analysis-rework.md) (`override_reference_mw` correction landed in this session)
- **Design doc (epic-level):** [`../../concepts/concept-analysis-rework-design.md`](../../concepts/concept-analysis-rework-design.md)
- **Item 7 signal contract (REQUIRED input — pins return shapes for the four rewritten parsers):** [`../concept-rework-helpers-validators/signal_contract.md`](../concept-rework-helpers-validators/signal_contract.md)
- **Item 7 design (the hybrid that handed this work to Item 8):** [`../concept-rework-helpers-validators/design.md`](../concept-rework-helpers-validators/design.md)
- **Phase 0 reference (read for inspiration; do NOT lift):** [`../concept-rework-prototype/`](../concept-rework-prototype/)
- **Item 5 selection prompt (out of scope):** `exploration/concept_analysis/prompt_templates/design_point_proposal.md`
- **Item 6 frontmatter writer:** `exploration/concept_analysis/scripts/lib/frontmatter.py:146-169`
- **Library account namespace:** `~/1cfe/1costingfe/src/costingfe/layers/{costs.py,cas22.py}`
- **Item 7 helper signature:** `scripts/lib/model_setup_helpers.py::run_native_and_1gw` — `run_native_and_1gw(model, spec, overrides, p_native, *, noak=True) → (result, result_1gw)`
- **Item 7 output-gate validators (resolve by symbol; Item 7's working tree is moving):** `validators.py::validate_model_setup_contract` (with `strict_helper_only` switch), `validators.py::validate_override_registry`, `validators.py::validate_design_point_coherence`, `validators.py::check_override_count_vs_fit_grade`
- **Wire points being swapped (resolve by symbol):** `lib/loop.py` model-setup output-gate selection (today: lines 632–644, three branches; resolve by reading the `# --- Validator selection ---` comment), `lib/loop.py::_run_assess`, `lib/iteration.py::parse_verdict_from_feedback`, `lib/validators.py::has_model_category_findings`, `lib/sources.py::parse_proposed_actions`

---

## Research Findings

### Template engine and substitution surface

The template engine (`lib/templating.py:11-47`) is a thin `{{var}}` / `{{#if var}}…{{/if}}` / `{{@config/partial.md}}` substitutor. No loops, no conditionals beyond `#if`. So any "per-account walkthrough" rendering has to be pre-rendered into a string by the orchestrator before substitution — it cannot loop inside the template.

### Common variables already built per stage

`run_analysis.py:_build_common_vars` (lines 384–423) hands the analyze prompt: `concept_id`, `concept_name`, `company`, `dossier_path`, `source_paths`, `brief_path`, `schema_path`, `exemplar_paths`, `approved_analyses`, `output_template_path`, `analysis_path`, `memory_context`, `concept_landscape`.

`loop.py:build_model_vars` (lines 685–748) hands the model-setup prompt: `concept_name`, `company`, `analysis_path`, `example_path`, `defaults_path` (empty), `readme_path`, `costing_constants_path`, `costingfe_concept`, `costingfe_fuel`, `mapping_notes` (empty), `output_path`, `model_feedback`, `prior_model_path`.

The empty `defaults_path` / `mapping_notes` placeholders (loop.py:721–725) are explicit Item 6→8 handoff hazards — the design ships their removal alongside the prompt rewrite.

The orchestrator already reads frontmatter for routing decisions (`get_comparison_status`); the analyze and model-setup prompts can be passed selection fields as substitution variables instead of being asked to re-read frontmatter from the analysis file. The frontmatter writer (`frontmatter.py:166-169`) emits exactly the fields we need: `Design-Point-Name`, `Design-Point-Maturity`, `P-Native`, `Grounding-Confidence`.

### 1costingFE account namespace

The library exposes accounts as a stable set of code strings: `CAS21` (buildings), `CAS22` (reactor plant — composed of `C220101`…`C220112`), `CAS23–CAS28`, `CAS29` (contingency). Each lives in a `layers/*.py` function with a docstring + `docs/account_justification/*.md` reference. The per-archetype default values are auto-loaded by the library from the `ConfinementConcept` enum (`costingfe/defaults.py`); not every archetype touches every account (e.g. laser-IFE concepts use `C220107` not `C220103` for the driver).

This means **the canonical-account schema for the analyze prompt is archetype-conditional** — passing a laser-IFE concept the full tokamak account list would invite wrong overrides. The schema must filter per `ConfinementConcept`.

### What `ConfinementConcept` enums exist

From the library: `TOKAMAK, STELLARATOR, MIRROR, DIPOLE, LASER_IFE, ZPINCH, HEAVY_ION, MAG_TARGET, PLASMA_JET, PULSED_FRC, MAGLIF, THETA_PINCH, DENSE_PLASMA_FOCUS, STAGED_ZPINCH, ORBITRON, POLYWELL` (16 enums). The fusion-tea concept set spans most of these — so per-archetype filtering is a real per-archetype concern, not a nominal one.

### Existing helpers and where the new helper lives

`lib/concepts.py:get_costingfe_library_hints` already does archetype lookup against `ENUM_LIBRARY_HINTS` (concepts.py:39-44) — same pattern. A new `get_canonical_accounts(enum)` helper belongs alongside it, returning a per-archetype list of `(account, one_line_what_it_costs)` tuples that the orchestrator renders into a markdown block.

### Validator status (Item 7 territory)

`lib/validators.py` is 920 lines today; Item 7 owns its rework. The Item 8 design treats it as: "produce a shape Item 7 can check." Specifically, Item 7's known incoming validators (per epic Item 7 SC) are: AST contract (`model`, `result`, `result_1gw` at module level; `net_electric_mw=1000` call shape), override-registry six-field validator, `P_native` cross-artifact (analysis ↔ model_setup ↔ design_point.csv), `provenance` label cross-artifact match. The prompts must make all four trivially checkable.

### Item 1 prototype prompt — what survives, what doesn't

- **Survives as inspiration:** the canonical-account-schema discipline, the per-account walkthrough discipline, the fit-grade-keyed override count band, the `direct` vs `derived` provenance discipline with arithmetic-in-rationale, the YAML override block structure, the explicit anti-pattern list.
- **Does NOT survive:** Section 1's design-point selection logic (now upstream); the conflation of selection and extraction; the open-ended "pick a plant" framing; the prototype's specific account codes (it produced `CAS22.1.3` — exactly the bug Item 8 is correcting).

---

## Core Concept

The new prompts express *one* contract: the design point is fixed upstream, the library is the default story, and every analyst departure is a six-field registry entry justified by company data. The prompts don't enforce that contract through prose alone — they *factor* the contract into the substitution variables. The orchestrator pre-renders the things the prompt would otherwise have to derive (design-point selection, canonical-account schema, fit-grade-keyed override-count band, comparables list), so the LLM's job collapses to extraction and judgment, not search and choice.

The key insight: **make the contract structurally impossible to violate.** If the canonical account list is in the prompt with one-line descriptions, the LLM cannot invent `CAS22.1.3`. If the per-account walkthrough is rendered into the prompt as a checklist, the LLM cannot underpropose by skipping accounts silently. If `P_native` is a substitution variable and the prompt is told "you do not choose this," the LLM cannot mix in a different plant's power. The prompt rewrite isn't about clever wording; it's about *removing the surface area on which the LLM could go wrong*.

This is why the design adds a small amount of orchestration code (one helper, one new config partial, three new common_vars keys) rather than packing everything into prose. The discipline lives at the variable boundary; the prompts just consume it.

---

## Key Bets & Decisions

### Bet 1: Schema and walkthrough live in orchestration code — but the schema is a hand-maintained fusion-tea constant, validated against the library

The canonical 1costingFE account list and the per-account walkthrough are *rendered* by the orchestrator and passed into the prompt as substitution variables. The prompt itself contains the *discipline* ("for each account, ask…"); the *data* (which accounts apply per archetype, what each one costs in one line) comes from a hand-maintained fusion-tea constant. A small validator imports `costingfe` and asserts that every account our constant names exists as a referenced code in the library — so the constant cannot silently outlive a library rename.

**Why hand-maintained rather than library-derived:** the library does not expose an enum→accounts map or per-account docstring registry. Applicability is *control flow*: e.g. `cas22.py:189` is `defaults = _COIL_DEFAULTS.get(concept); if defaults is None: c220103 = 0.0`. There is no machine-readable "this archetype touches these accounts" surface to extract from. The original Bet-1 (b) plan — `account → docstring` extraction — cannot be built without modifying the library, which is out of scope.

The hand-maintained constant is small: 16 enums × ~10 relevant accounts each, each row holding `(account_code, one_line_description, applies_when_clause_or_None)`. The applicability rules are *judgment* the analyst writes once and reads many times — exactly the kind of fusion-tea-owned interpretation of the library that earns a fusion-tea-side file.

**Alternatives considered:**
- (a) **Hand-maintained fusion-tea constant** with a library-existence cross-check. ~150 LOC of data + ~30 LOC of validator. Drift-detected, not drift-prevented; the cost of a library rename is a one-line constant update, caught loudly at next pipeline run.
- (b) **Library-derived at runtime** via introspection. Infeasible — no introspection surface; would require modifying 1costingFE.
- (c) **Generated frozen JSON pinned into the repo.** Same problem as (b) for the generation step; no win over (a).

**Decision: (a).** The constant lives in `lib/canonical_accounts.py` as `_PER_ARCHETYPE_ACCOUNTS: dict[str, list[AccountRow]]` plus `validate_against_library() -> list[str]` which the test-suite calls. The render function reads the constant directly. The validator is run in CI and on every fresh pipeline session — a missing or renamed library account surfaces as a loud failure, not a silent prompt regression.

### Bet 2: Override Candidates emitted as a single fenced YAML block under one section

In the regenerated `analysis.md`, override candidates emit as a single fenced YAML block under a dedicated section — "## Section 5b: Override Candidates" — positioned immediately after Section 5 ("Design Point Parameters"). The canonical section list is owned by `output_template.md` (see Component Overview); the override block sits where the quantitative design-point description has just been spelled out, so the LLM has the per-account context in immediate scope when writing each override.

**Alternatives considered:**
- (a) **One fenced YAML block.** Trivially parseable; round-trips with the `model_setup.py` registry.
- (b) **One YAML fence per entry.** Reads better in raw markdown; harder for Item 7's validator to ingest as a single structure.
- (c) **Markdown table + JSON sidecar.** Most reader-friendly. Two sources of truth — exactly the antipattern.

**Decision: (a).** Item 7's validator will diff this block's entries against the `overrides` list in `model_setup.py` to catch `provenance` drift; matching shapes on both sides keeps that check trivial.

### Bet 3: Per-account walkthrough is a config partial included via `{{@…}}`

The discipline ("for each canonical account, ask the dossier whether it names a quantity / unit cost / company-published $ figure for this account; only propose an override if yes") lives in `config/account_walkthrough.md`, included into `analysis_v2.md` via the existing `{{@config/…}}` mechanism. The orchestrator-rendered per-archetype account list is *separate* from this partial and is passed in as a substitution variable.

**Why split:** the discipline is concept-agnostic; the account list is archetype-conditional. Splitting keeps the partial reusable and the substituted block thin.

### Bet 4: Selection block at top, quantitative description embedded in Section 5

The Design Point splits across two locations in `analysis.md`, by purpose:

- **Top of body — "## Design Point" selection block.** Small. Five fields (name, maturity, P_native, grounding, primary sources). Pure read-only render of the orchestrator-fixed selection — the prompt copies these from substitution variables and is forbidden to edit them. Purpose: the reader's first question ("what plant is this?") gets the first answer.
- **Section 5 — "Design Point Parameters" (renamed from "LCOE-Relevant Parameters").** The full extracted quantitative description (geometry / physics / performance) of the named plant lives here as the parameter table. Purpose: enforce the concept-doc's "parameters *are* the design point's quantitative description and must match it 1:1" property by physical adjacency.

**Why split:** the selection is orchestrator-owned, immutable, and short — it earns its top-of-body slot for discoverability. The quantitative description is LLM-extracted, longer, and exists *to be coupled with* the parameters; that's exactly Section 5. Putting both in one place either buries the selection under Section 1–4 (loses the first-answer property) or bloats the top of the file with a parameter table (loses skimmability).

**Duplication risk:** the selection fields appear in three places — frontmatter (canonical, orchestrator-written), top-of-body block (rendered from substitution variables, read-only), and Section 5 header context. Invariant #1 forbids the LLM from editing any of them; Item 7's cross-artifact validator checks the rendered block against frontmatter; the Section 5 header just *references* the named plant rather than re-stating fields.

**Alternatives considered:**
- (a) **Top-of-body only.** Discoverable but separates the named plant from the parameter table that describes it.
- (b) **Section-5-adjacent only.** Matches the concept-doc directive literally; "what plant is this?" only surfaces past Section 4.
- (c) **Both** (chosen). Selection at top (discoverability), quantitative description at Section 5 (1:1 coupling).

**Decision: (c).** Concept-doc's 1:1 coupling property is preserved at Section 5; reader's first-answer property is preserved at the top. The "third place" is read-only render from frontmatter and is checked structurally by Item 7.

### Bet 5: Two `analysis | model` categories on findings — no third category

Per spec FR-19. Cross-artifact failures (P_native mismatch, provenance drift, account-namespace miss) route to whichever artifact's fix would correct them.

### Bet 6: Assess and review parse a stable structural shape, not regex

The assessment prompt emits a markdown block with explicit anchored headings (`### F-N: <title>`, `**Target:** …`, `**Category:** …`, etc., per `feedback_format.md`) and a verdict line that is the first non-blank line of the body (`VERDICT: PASS` / `VERDICT: FINDINGS`). The four rewritten parsers (per spec FR-25 / `signal_contract.md`) read this with simple line-anchored parsing. The legacy regex constants (`FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE`, `PROPOSED_ACTION_RE`) and their direct uses are deleted in the same change.

### Bet 7: Generated `model_setup.py` uses Item 7's `run_native_and_1gw` helper — not an inline two-knob `forward()`

Item 7 ships `run_native_and_1gw(model, spec, overrides, p_native, *, noak=True) → (result, result_1gw)` and a `strict_helper_only=True` switch on `validate_model_setup_contract` that rejects the inline form. The model-setup prompt emits the helper-call form. Step 4 of the four-step structure is a one-liner: `result, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`. This is what makes FR-10 and Item 7's contract validator agree.

**Why the helper rather than inline:** the helper centralises the `availability` / `lifetime_yr` library-default sourcing and the `override_reference_mw=p_native` discipline. Every generated file calling the helper inherits the same call shape; the contract validator's strict mode is what *enforces* that uniformity. Inline two-knob forwards across 36+ regenerated files would drift; the helper is the single chokepoint that keeps them honest.

### Bet 8: Atomic swap — no transient "new prompt + old parser" state

Per spec FR-29. The prompts, parsers, helper-form generation, validator wiring, regex deletion, and FR-9 discharge all land in a single merge unit. The reasoning: Item 7 was a pure library layer precisely because no individual sub-step in this swap is forward-compatible with the previous step (new format breaks old parsers; new parsers break old prompts; new generated files break the un-wired validator). The atomicity is what lets the loop stay green across the swap.

---

## Architecture

### Data flow

```
upstream tables (Item 5)  →  frontmatter (Item 6)  →  common_vars (Item 8 + existing)
                                                            ↓
                                                     template render
                                                            ↓
                                                       LLM stage
                                                            ↓
                                  structured artifacts (analysis.md / model_setup.py / feedback.md)
                                                            ↓
                                                ┌───────────┴──────────────┐
                                                ↓                          ↓
                              output-gate validators (Item 7,        rewritten parsers (Item 8,
                              wired across 3 branches — Item 8)       iteration.py/validators.py/sources.py)
                                                ↓                          ↓
                                                └────────── loop control flow ─────────┐
                                                                                       ↓
                                                                        downstream readers (Item 10)
```

### What changes vs. today

**A. Prompts (template-level rewrite — Bet 1–6)**

1. **`_build_common_vars`** (`run_analysis.py:384`) gains four substitution keys:
   - `design_point_block` — pre-rendered markdown of the selection fields (read from frontmatter)
   - `canonical_accounts` — pre-rendered markdown table of per-archetype account codes + one-line descriptions
   - `comparables_block` — pre-rendered text of the `Comparables:` list (the value already exists in frontmatter; we just render it into the prompt)
   - `fit_grade_band` — one-line rubric string keyed off `Archetype-Fit` — sourced from **one shared constant** (e.g. `FIT_GRADE_OVERRIDE_BAND` in `lib/canonical_accounts.py` or `lib/concepts.py`) that is also consumed by Item 7's `check_override_count_vs_fit_grade` and referenced by name in the rewritten `assessment.md` prompt. Three-place duplication of `High → 0–4 / Med → 3–8 / Low → 6–12` would drift; one source.
2. **`build_model_vars`** (`loop.py:685`) drops `defaults_path` and `mapping_notes` (already empty placeholders); the rewritten `model_setup_costingfe.md` no longer references them. Adds `design_point_block` and `canonical_accounts` for the model-setup prompt's read-the-Design-Point step.
3. **New helper:** `lib/canonical_accounts.py` (one file, ~150 LOC of data + ~30 LOC of code) carrying:
   - `_PER_ARCHETYPE_ACCOUNTS: dict[str, list[AccountRow]]` — hand-authored per-`ConfinementConcept` constant
   - `get_canonical_accounts(enum: str) -> list[AccountRow]`
   - `render_account_block(accounts: list[AccountRow]) -> str` — markdown block consumed by the analyze prompt
   - `validate_against_library() -> list[str]` — imports `costingfe` and confirms every named account code appears in the library; called by a unit test and by CI
4. **New config partial:** `prompt_templates/config/account_walkthrough.md` — concept-agnostic discipline language for the per-account walkthrough.
5. **Rewritten templates** (per spec FR list): `analysis_v2.md`, `output_template.md`, `model_setup_costingfe.md`, `model_setup_costingfe_edit.md`, `assessment.md`, `review.md`, `config/feedback_format.md`, `config/assessment_checklist.md`, `config/analysis_goals.md`, `config/quality_standards.md`. `model_setup_costingfe.md` instructs the LLM to emit the helper-form step 4 (Bet 7).
6. **Rename leak-through:** `synthesis.md`, `score.md` — `Reuses:` → `Comparables:` only.

**B. Parsers (internal rewrite — Bet 6 / FR-25)**

7. **`parse_verdict_from_feedback`** (`iteration.py::parse_verdict_from_feedback`) — internals swap from `FEEDBACK_VERDICT_RE` / `FINDING_HEADER_RE` to line-anchored parse of the new format. Signature unchanged; returns `tuple[str, int]`.
8. **`has_model_category_findings`** (`validators.py::has_model_category_findings`) — internals re-read the new `**Category:** analysis | model` block. Returns `bool`; uncategorized stays conservative `True`. **Note:** this function is on the *model-setup generation* route (called at `loop.py:635` to pick the feedback-pass validator chain) — *not* a verdict-parsing concern. Its rewrite plus the deletion of `FINDING_HEADER_RE` couples to the model-setup output-gate change in §11; both must land in the atomic-swap unit.
9. **`validate_feedback_verdict`** and **`validate_review_verdict`** (`validators.py`) — internals re-read; tokens `PASS`/`FAIL` and `PROCEED`/`REVISE` preserved; existing `ValidationResult` shape preserved.
10. **`parse_proposed_actions`** (`sources.py::parse_proposed_actions`) — internals re-read PA-N blocks under the new format; returns `list[dict]` with the same nine keys.

**C. Loop wiring (Item 7-deferred — Bet 8 / FR-26, FR-27, FR-28)**

11. **`loop.py` model-setup output gate — all three branches.** The current validator selection at lines 632–644 is three-way (edit-pass-with-model-findings at :637, edit-pass-analysis-only at :640, cold-start at :644). Item 8 composes a *single new* validator chain — `validate_model_setup_contract(strict_helper_only=True)` + `validate_override_registry` — and applies it in **all three** branches (not just edit-pass). The cold-start path is where the very first `model_setup.py` lands; without gating there, a malformed cold-start file escapes the contract validator entirely. The three branches' existing validators (`make_file_modified_validator`, `validate_python_syntax`) chain into the new contract checks via `chain_validators`.
12. **Assess surface — net-new construction.** `_run_assess` at `loop.py:751` currently builds `assess_vars` from `common_vars` only; there is no existing flag-feed surface from validators into the assess prompt (`comparables_sanity_check.py` is a standalone script never imported by `loop.py`). Item 8 *adds* this surface from scratch: extend `_run_assess` to (a) accept or read the concept's `design_point.csv` row and the cold/iter `analysis.md` text, (b) call `validate_design_point_coherence(concept_id, model_setup_text, design_point_row, analysis_md_text)` and `check_override_count_vs_fit_grade(fit_grade, enabled_count)` against them, and (c) render their `details` payloads into a new substitution key (e.g. `coherence_flags`) that the rewritten `assessment.md` includes for the LLM reviewer to interpret. The checks compute and flag; they do not gate. **Effort risk:** treat this as net-new construction in the plan estimate.
13. **Regex deletion** — remove `FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE`, `PROPOSED_ACTION_RE` and their direct uses. Discharges Item 7's FR-9.

### Why this shape

- **One helper, one partial, four new common_vars keys** is the minimum machinery that makes the contract structural rather than prose-only. Anything smaller (no helper) reverts to prose-only discipline that Phase 0 demonstrated breaks. Anything larger (one helper per artifact concern) duplicates work the existing `_build_common_vars` / `build_model_vars` pattern already does well.
- **The prompts stay readable.** No more than one new `{{@config/…}}` include per rewritten template; the discipline is small and well-named.
- **Item 7 and Item 8 decouple cleanly.** Item 7 validates structural shape; Item 8 produces it. If Item 7 lands first, Item 8 templates against its helper APIs by reference. If Item 8 lands first, Item 7 builds against the shapes the templates already emit.

---

## Required Invariants

1. **Selection is read, not chosen.** Every analyze invocation receives `Design-Point-Name`, `Design-Point-Maturity`, `P-Native`, `Grounding-Confidence` as substitution variables sourced from frontmatter; the prompt forbids overriding any of them.
2. **Canonical account codes only.** Every override `account` field emitted by the analyze step (and consumed by the model-setup step) is a string drawn from `get_canonical_accounts(concept.archetype_enum)`. No `CAS22.1.3`-style codes.
3. **Six-field override entries.** Every entry in both `analysis.md`'s Override Candidates YAML and `model_setup.py`'s `overrides` list contains all six fields (`account / value / enabled / provenance / source / rationale`). Missing fields are a validator-rejection.
4. **Four-step `model_setup.py` shape — helper form only.** Spec dict + `P_native` → `model = CostModel(...)` → six-field override list → `result, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)`. `model`, `result`, `result_1gw` at module level. `validate_model_setup_contract(..., strict_helper_only=True)` is the structural enforcer; inline two-knob `forward()` is rejected.
5. **No re-passed library defaults in `spec`.** `availability`, `lifetime_yr`, `interest_rate`, `inflation_rate` MUST NOT appear in the generated `spec` dict. The helper sources `availability` / `lifetime_yr` from the library internally. Archetype-default-but-physics-overridable fields (`eta_th`, `eta_de`) appear only when the design point cites a physics-grounded distinct value.
6. **Cross-artifact coherence is testable.** `P_native` in the analysis Design Point block, `P_native` in the model_setup constants, and `P_native` in `design_point.csv` are identical strings post-prompt-rewrite. The same override `account` appears in both the analysis YAML and the model_setup `overrides` list with the same `provenance` label. `validate_design_point_coherence` checks all three legs at assess time.
7. **Frontmatter is orchestrator-owned.** No prompt edits, adds, or removes a frontmatter field. (Already an Item 6 invariant; restated here because the rewritten analyze prompt is the most likely place to violate it.)
8. **Parser return shapes are fixed by `signal_contract.md`.** The four rewritten parsers preserve their existing signatures and return shapes row-for-row. Call sites named in spec FR-25 do not move.
9. **Atomic swap.** Prompts, parsers, helper-form generation, validator wiring, and regex deletion land in a single merge unit. No intermediate commit produces a runnable but format-mismatched pipeline.

---

## Component Overview

### `prompt_templates/analysis_v2.md` (rewritten)

The analyze prompt. Three modes (cold-start / feedback-pass / self-advance) preserved. Cold-start reads pre-rendered `design_point_block` (top-of-body selection render), `canonical_accounts`, `comparables_block`, `fit_grade_band` from substitution. Includes `config/account_walkthrough.md`. Emits an `analysis.md` body containing the canonical section list pinned in `output_template.md` (see below).

### `prompt_templates/output_template.md` (rewritten — owns the canonical section list)

The single source of truth for section ordering. Pins the canonical list (numbered sections; "Section Xb" sub-sections allowed only where named here) so the prompt and the parsers cannot disagree:

1. **Top-of-body — "## Design Point"** (selection block, rendered from frontmatter; not numbered) — *placed before Section 1, per Bet 4(c)*
2. **Section 1: Availability of Data**
3. **Section 2: Challenges in Capturing System Function**
4. **Section 3: Maturity of Key Subsystems**
5. **Section 4: Key Materials and Supply Chain**
6. **Section 5: Design Point Parameters** (renamed; the quantitative description of the named plant, per Bet 4(c))
7. **Section 5b: Override Candidates** (single fenced YAML block, six-field entries, canonical account codes — per Bet 2)
8. **Section 6: Data Gap Inventory**
9. **Section 7: Family-Delta vs Comparables** (replaces old "Cross-Concept Notes")
10. **Section 8: Sources**

Bet 2's "right after the Design Point block" is corrected here to "right after Section 5 (which describes the design point quantitatively)" — Override Candidates as Section 5b. The output_template.md and the rewritten parsers both reference this list by section title; the analyze prompt embeds it verbatim.

### `prompt_templates/model_setup_costingfe.md` (rewritten)

The model-setup prompt. Instructs the LLM to start by reading the Design Point block + Override Candidates from `analysis.md`; emit the four-step script with literal canonical structure; forbid `# DEFAULT: …` comments; enforce module-level `model` / `result` / `result_1gw`; emit step 4 as `result, result_1gw = run_native_and_1gw(model, spec=spec, overrides=overrides, p_native=P_native)` and forbid the inline two-knob `forward()` form (Bet 7). References `costingfe_concept` / `costingfe_fuel` / `example_path` (existing common_vars keys) and `design_point_block` / `canonical_accounts` (new).

### `prompt_templates/model_setup_costingfe_edit.md` (rewritten)

Feedback-pass variant. Edits an existing four-step `model_setup.py` against assessment findings; preserves the structure.

### `prompt_templates/assessment.md` (rewritten)

In-loop assessment. Reads the regenerated `analysis.md` + (if present) `model_setup.py`. Emits `F-N` findings with `Category: analysis | model` and a verdict line, anchored to the new artifact shape. Uses `fit_grade_band` from common_vars to check override count.

### `prompt_templates/review.md` (rewritten)

Post-loop review. Emits PROCEED / REVISE with PA-N (proceed minor fixes) or F-N (revise findings). Strategic dimensions updated for the new contract (design-point coherence, override discipline, family-delta against fixed comparables, two-knob invariants).

### `prompt_templates/config/feedback_format.md` (rewritten)

Defines the structural shape of `F-N` findings (line-anchored, not regex-anchored). Updated `Category` enum reaffirmed as `analysis | model`.

### `prompt_templates/config/assessment_checklist.md` (rewritten)

Per-section checks against the new artifact shape: Design Point coherence, override discipline (count vs fit grade, provenance honesty), family-delta concreteness, two-knob projection correctness.

### `prompt_templates/config/analysis_goals.md` (rewritten)

Acknowledges that family / archetype / comparables / design-point selection are *upstream-fixed*. The analyzing agent's job is family-delta articulation, parameter extraction, and override-candidate discovery.

### `prompt_templates/config/quality_standards.md` (rewritten)

Library-is-default discipline; six-field overrides; honest provenance; no `# DEFAULT:` re-passing.

### `prompt_templates/config/account_walkthrough.md` (new)

The per-account-walkthrough discipline, concept-agnostic. Included by `analysis_v2.md` via `{{@…}}`.

### `prompt_templates/synthesis.md`, `prompt_templates/score.md` (rename leak-through only)

Replace `Reuses:` references with `Comparables:`. No other change.

### `scripts/lib/canonical_accounts.py` (new, ~50 LOC)

```python
def get_canonical_accounts(enum: str) -> list[dict]:
    """Per-archetype account list. Each dict: account, what_it_costs, applies_when."""
    ...

def render_account_block(accounts: list[dict]) -> str:
    """Render the list as a markdown block consumed by analysis_v2.md."""
    ...
```

Imports `costingfe`; pulls account-function docstrings; filters per `ConfinementConcept`. Tested by a small fixture per archetype.

### `scripts/run_analysis.py:_build_common_vars` (extended)

Adds four substitution keys (`design_point_block`, `canonical_accounts`, `comparables_block`, `fit_grade_band`) by reading frontmatter for the concept and calling `canonical_accounts.render_account_block(…)`. No other behavior change.

### `scripts/lib/loop.py:build_model_vars` (extended)

Drops `defaults_path` and `mapping_notes`; adds `design_point_block` and `canonical_accounts`. The two retired placeholders disappear from `model_setup_costingfe.md` simultaneously.

### `scripts/lib/iteration.py::parse_verdict_from_feedback` (internals rewritten)

Internals re-read the new line-anchored verdict + finding-count format. Signature unchanged: `(feedback_text: str) → tuple[str, int]`. The "PASS" / "FAIL" + count tuple is the contract documented in `signal_contract.md`.

### `scripts/lib/validators.py::has_model_category_findings` (internals rewritten)

Internals re-read `**Category: analysis | model**` lines under each `### F-N` block. Returns `bool`. Uncategorized findings stay conservative `True` (per `signal_contract.md` — Item 8 must not change this bias).

### `scripts/lib/validators.py::{validate_feedback_verdict, validate_review_verdict}` (internals rewritten)

Internals re-read the new `VERDICT: PASS|FINDINGS` / `VERDICT: PROCEED|REVISE` line. Existing `ValidationResult` shape preserved. The legacy regex constants (`FEEDBACK_VERDICT_RE`, `REVIEW_VERDICT_RE`) are removed.

### `scripts/lib/sources.py::parse_proposed_actions` (internals rewritten)

Internals re-read PA-N blocks under the new prompt format. Returns `list[dict]` with the nine documented keys (`id, description, category, severity, location, finding, proposed_fix, decision, user_notes`). `PROPOSED_ACTION_RE` removed.

### `scripts/lib/loop.py` model-setup output gate — all three branches (lines 632–644)

Compose `validate_model_setup_contract(strict_helper_only=True)` + `validate_override_registry` into the validator picked by **each** of the three branches (edit-pass-with-model-findings, edit-pass-analysis-only, cold-start). Today the three branches assign different validators (`chain_validators(make_file_modified_validator, validate_python_syntax)`, `validate_python_syntax`, `validate_python_syntax`); Item 8 chains the two new contract gates onto each so a cold-start `model_setup.py` is held to the same contract as a feedback-pass file.

### `scripts/lib/loop.py::_run_assess` (extended — net-new flag-feed surface)

Today `_run_assess` only forwards `common_vars`. Item 8 extends it to: (a) accept or read the concept's `design_point.csv` row + the `analysis.md` text; (b) call `validate_design_point_coherence` + `check_override_count_vs_fit_grade`; (c) render their `details` into a new `coherence_flags` substitution key consumed by the rewritten `assessment.md`. **This is new construction, not a pattern-match of an existing surface** — `comparables_sanity_check.py` exists but is not currently wired into `_run_assess`.

---

## Non-Goals

- **Modifying Item 7's helper/validator *signatures and return contracts***. Item 8 *uses* `run_native_and_1gw`, `validate_model_setup_contract`, `validate_override_registry`, `validate_design_point_coherence`, `check_override_count_vs_fit_grade`, `enabled_overrides` — and wires them — but does not change their public APIs.
- **Modifying the four parsers' signatures or return shapes** — only their internals change (per `signal_contract.md`).
- Reworking the freeform branch (`model_setup_freeform*.md`) — deferred per epic non-goal.
- Reworking `model_critic.md` — Item 9.
- Reworking `design_point_proposal.md` — Item 5, already shipped.
- Changing the `_build_common_vars` / `build_model_vars` skeleton beyond adding the four new keys and retiring two empty ones.
- Adding a third finding `Category` (spec FR-19).
- Rendering the per-account walkthrough as a loop inside the template (the engine has no loop primitive; rendering happens in code).
- Adding new modes to `analysis_v2.md` beyond the existing three (cold-start, feedback-pass, self-advance).
- Touching `scoring_framework.md` content.

---

## Implementation Notes

### Account schema rendering — the one thing not to over-engineer

`get_canonical_accounts(enum)` reads the library; `render_account_block(accounts)` produces ~20 lines of markdown. The temptation to add per-account-applicability rules, version-pinning, or a JSON sidecar is the temptation to recreate the existing `defaults.py` machinery in the prompt layer. Resist. The block exists to anchor the LLM's account-code choice; the *values* still come from the library at `forward()` time.

### Design Point shape across the body (per spec FR-3, Bet 4)

**Top-of-body selection block:**

```
## Design Point

- Name: {{Design-Point-Name}}
- Maturity: {{Design-Point-Maturity}}
- P_native: {{P-Native}} MWe
- Grounding: {{Grounding-Confidence}}
- Primary sources: <bullet list — extracted from dossier; must agree
  with the design-point table's trace artifact>

(Selection fields are orchestrator-fixed from the design-point table.
 The analysis prompt copies them from substitution and is forbidden
 to edit them. The quantitative description of this plant is in
 Section 5.)
```

**Section 5 — "Design Point Parameters":**

```
## Section 5: Design Point Parameters

Every value below describes {{Design-Point-Name}} at its native scale
(P_native = {{P-Native}} MWe). Parameters from a different design or
scale must not appear here.

| Parameter | Value | Source | Confidence | Note |
| --- | --- | --- | --- | --- |
| R0 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |
```

The list of parameter rows is concept-conditional but at minimum: `R0`, `a` (plasma_t), `elon`, `B0`, `B_peak`, `fusion_power_MW`, `net_electric_MWe`, `p_input_MW`, and any concept-distinctive knob (e.g. compression ratio for MIF, target gain for IFE).

### Override Candidates YAML schema (per spec FR-4)

```yaml
overrides:
  - account: C220103
    value: 6901.0          # plain number OR expression like 260.0 * 1.34
    enabled: true
    provenance: derived    # one of: direct, derived
    source: "arc-reactor-specifications.md §6"
    rationale: |
      Sorbom 2015 published 156 t HTS × ~$44k/kg (2024 CPI-adjusted)
      = $6,901M at design-point per-module. Library default of $X is computed
      from coil geometry alone and misses HTS unit cost.
```

`value` accepts expressions per spec FR-14. The YAML is parsed at model_setup.py write-time; the prompt's job is to emit it syntactically clean.

### Four-step `model_setup.py` literal (per spec FR-10) — helper form

The model-setup prompt shows the LLM the four-step canonical structure as a single template comment block — not a fragmented "step 1 do X / step 2 do Y" set of instructions. Step 4 is a one-liner against the helper:

```python
# 1. Specification — design-point inputs, native scale.
spec = dict(R0=..., plasma_t=..., elon=..., ...)   # geometry/physics only
P_native = ...                                      # MWe — from analysis.md

# 2. Model.
model = CostModel(concept=ConfinementConcept.TOKAMAK, fuel=Fuel.DT)

# 3. Override registry — six fields per entry.
overrides = [
    {"account": "C220103", "value": 6901.0, "enabled": True,
     "provenance": "derived", "source": "...", "rationale": "..."},
    ...
]

# 4. Both forwards via the helper.
result, result_1gw = run_native_and_1gw(
    model, spec=spec, overrides=overrides, p_native=P_native,
)
```

The inline two-knob `forward()` form is forbidden. `validate_model_setup_contract(..., strict_helper_only=True)` is the structural enforcer.

### Mode handling in `analysis_v2.md`

Three modes (cold-start, feedback-pass, self-advance) preserved via `{{#if cold_start}}` / `{{#if feedback_pass}}` / `{{#if self_advance}}` as today. The orchestrator's mode-switch logic (run_analysis / loop.py) is unchanged. Cold-start gets the full instruction set; feedback-pass and self-advance get a compact instruction set ("preserve the Design Point block selection fields; targeted edits only") with the same `design_point_block` / `canonical_accounts` substitution.

### Renames

A single sweep over the in-scope file list for `Reuses:` → `Comparables:`. Validate by grepping the post-rewrite tree.

### Item 7 sequencing — code on disk, not committed

As of design draft, Item 7's code exists in the working tree (`validators.py` modified; `model_setup_helpers.py`, `signal_contract.md`, the Item 7 spec/design/plan all unstaged) but the last commit is `9cc9675` (Item 6). Item 8 does **not** assume "Item 7 already merged."

Two reconciliations on FR-29 ("single merge unit"):

- **Option A — Item 7 commits first, Item 8 follows.** Item 7's library work merges as a self-contained commit with its own green tests (the helper, validators, coherence checks, signal_contract.md). Item 7's commit changes *nothing* in loop control flow (its design Decision 1) so the loop stays green. Item 8 then lands as a second commit — the atomic swap — that wires Item 7's already-merged surfaces into the loop. FR-29's "single merge unit" applies to *Item 8's* changes (prompts + parsers + wiring + regex deletion), not to "Items 7 + 8 together."
- **Option B — Items 7 and 8 land as one commit.** A larger merge unit; tighter atomicity (no transient state where Item 7 surfaces exist un-wired); harder to review.

**Recommendation: Option A.** Item 7 was designed as a pure library layer to make exactly this two-commit sequence safe — the loop stays green between the two commits. Option B's only marginal advantage is review-time atomicity, which is more cleanly served by a stacked PR. The plan owns the final call; the design records the bias.

Item 8 *consumes* Item 7's surfaces — templates written against the helper-form generated `model_setup.py`; loop wiring assumes the validators exist; parser rewrite assumes `signal_contract.md` is the authoritative return-shape contract. There is no "helper-free fallback" path.

---

## Potential Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Atomic-swap window is large (10 templates + 4 parsers + 2 wiring sites + 4 regex deletions in one merge unit) | High — the seam is exactly what Item 7 designed around; a "new prompt + old parser" intermediate state breaks loop control flow | Plan-stage de-risk: parser-rewrite tests against hand-crafted "new format" files land first, *behind a feature flag or branch only*; the prompt rewrite + the regex deletion only land once the parser tests are green. Full-loop dry-run on ARC is the final gate before merge. |
| Parser internals re-write subtly changes a return shape | High — silent loop-control regression | `signal_contract.md` is normative input; design pins each shape; unit tests in the parser-swap stage assert row-for-row against the contract |
| Prompt bloat — `analysis_v2.md` gains schema + walkthrough + Design Point instructions, may exceed practical token budget | Med — degrades LLM attention; can manifest as ignored discipline | Bet 3 splits the walkthrough out to a partial; canonical_accounts block is archetype-filtered; Phase 0 ran at $0.15/run with a similar-sized prompt — within budget |
| Operator drift between `analysis.md` and `model_setup.py` (Phase 0 surfaced) | High — silent cross-artifact incoherence | `validate_design_point_coherence` (three-leg, wired into assess this item) catches `P_native` drift; structural diff between analysis YAML and `model_setup.py` overrides list catches provenance drift |
| `get_canonical_accounts` becomes drift-prone if the library reshapes its account namespace | Low — library is stable | Helper imports the library directly; library reshape breaks the helper loudly at next render |
| Three-mode handling in `analysis_v2.md` grows the file past comprehensible | Med | Compact-instruction blocks per non-cold mode; mode-switch logic untouched in the orchestrator |
| YAML parse fragility in Override Candidates | Med | Single fenced block + line-anchored expectations; Item 7's validator owns the strict parse |
| Asterisked (`grounding_confidence: low`) concepts produce poor extraction under the same prompt | Med — they still go through costingfe | Prompt does not branch on grounding; the asterisk is downstream-only (explorer view). If extraction is too weak we revisit; Item 10 pilot covers a low-grounding row |
| Reuses → Comparables rename misses a non-listed template | Low | Grep-driven sweep + a CI check (existing) catches stray `Reuses:` |

---

## Integration Strategy

This work integrates with Item 5 (tables), Item 6 (frontmatter + glue), and Item 7 (helpers + validators) along three seams: the substitution-variable seam (orchestrator → prompt), the artifact-shape seam (prompt output → validator), and the signal seam (LLM output → parser → loop control flow).

- **Upstream of Item 8:** Item 5 owns the design-point table; Item 6 owns the orchestrator-populated frontmatter; Item 7 owns the helper + validator + coherence-check library and the `signal_contract.md` handoff doc. Item 8 reads all three as fixed contracts.
- **Sequenced after Item 7 (which has shipped):** Item 7 deliberately left the live-loop regex parsers in place because the *current* prompts still emit the old format. Item 8 is the swap. The hybrid was designed around this seam; the spec's atomicity requirement (FR-29) preserves it.
- **Downstream of Item 8:** Item 9 (`model_critic`) reads the new artifact shape and consumes the wired-in coherence-check outputs; Item 10 (pilot) re-runs the pipeline against ARC and 2–4 other concepts spanning High/Med/Low × high/med/low. Item 11 bulk-regenerates.

The change has two layers: an additive prompt/helper layer (new templates, new `canonical_accounts.py`, four new substitution keys) and a *substitutive* loop-control layer (parser internals swap, regex constants delete, validator chain extends). The substitutive layer is what makes atomicity mandatory.

---

## Validation Approach

### Unit-level

- `lib/canonical_accounts.py` — small fixture per ConfinementConcept enum (one per representative archetype, ~5 total covering tokamak / stellarator / mirror / laser_ife / pulsed_frc); assert account-list shape and renders.

### Prompt-level

- Lint sweep: no template references `Reuses:`, `# DEFAULT: framework value`, `result_1gw_native`, `CAS22.1.<digit>`-style fake account codes.
- Substitution-variable inventory: confirm every `{{var}}` in each rewritten template resolves from `_build_common_vars` or `build_model_vars`.

### Library cross-check (Bet 1)

- `lib/canonical_accounts.py::validate_against_library()` runs as a unit test and in CI. Asserts that every account code named in `_PER_ARCHETYPE_ACCOUNTS` is referenced somewhere in `costingfe/layers/{costs.py,cas22.py}`. A library rename or removal fails the test loudly with the offending code.

### Design-point row plumbing (FR-27 prerequisite)

`_run_assess` currently has no access to the concept's `design_point.csv` row. Plumbing it in is a sub-task of the assess wiring: either (a) `_build_common_vars` reads the row and passes it via `common_vars`, or (b) `_run_assess` reads `design_point.csv` directly. Plan picks one; design notes only that the wiring exists *and is net-new*. The `analysis.md` text leg is already available — `_run_assess` already has `analysis_path` and can read it.

### Parser-swap unit tests (pre-atomic-swap)

Before any prompt is changed, each rewritten parser is exercised against (a) hand-crafted "new format" example files (one PASS, one FINDINGS-mixed-categories, one REVISE-with-PA-actions) and asserted against the `signal_contract.md` return-shape table; and (b) a stale old-format file, asserted to *fail loudly* (the parsers must reject the old format unambiguously, not silently misparse).

### Loop-wiring unit tests

- `validate_model_setup_contract` with `strict_helper_only=True` accepts a hand-crafted helper-form `model_setup.py` and rejects a hand-crafted inline-`forward` `model_setup.py`.
- `validate_override_registry` accepts a conformant six-field list and rejects each of the obvious malformations (missing field, duplicate `account`, unknown `provenance`).
- `validate_design_point_coherence` flags `P_native` drift across the three legs.
- `check_override_count_vs_fit_grade` returns the right flag for each fit-grade × count combination.

### End-to-end (dry-run gates per spec)

1. **Analyze dry-run on concept 01 (ARC, High fit, well-grounded).** Inspect the generated `analysis.md` against acceptance criteria: Design Point block selection matches frontmatter; quantitative table describes the named plant; Override Candidates YAML has six-field entries with canonical account codes; family-delta against the comparables list is concrete; no leftover `Reuses:` references.
2. **Model-setup dry-run on the same regenerated `analysis.md`.** Inspect the generated `model_setup.py`: four-step structure literally present; step 4 calls `run_native_and_1gw(...)` (no inline `forward()`); `model`, `result`, `result_1gw` at module level; no `# DEFAULT:` comments; `spec` dict contains only design-point-specified inputs; `availability` / `lifetime_yr` / `interest_rate` / `inflation_rate` absent. `validate_model_setup_contract(..., strict_helper_only=True)` accepts.
3. **Assessment dry-run on the regenerated pair.** Verdict parses cleanly via the rewritten parser; findings reference design-point coherence and override discipline; override count band check + design-point coherence check flag into the LLM reviewer as expected.
4. **Full-loop dry-run on ARC, green end-to-end.** The atomic-swap acceptance gate. New prompts + rewritten parsers + wired contract validators + `strict_helper_only=True` + coherence checks. Loop runs continue/stop decisions correctly through verdict tokens; PA-action ingest still produces the nine-key dicts; no references to removed regex constants remain. Discharges Item 7's FR-9.
5. **Comparison-view dry-run.** Feed the dry-run `model_setup.py` to `concept_explorer/extract_explorer_data.py`. `result_1gw` is at exactly 1000 MWe; `Confinement-Family:` resolves from frontmatter; no fallback paths exercised.

### Manual

- Visual inspection of the new `analysis_v2.md` and `model_setup_costingfe.md` to confirm the contract is *legible to a human analyst*, not just machine-parseable.
- Walk one operator (or a fresh Claude session) through the new prompts to confirm a cold reader can produce a conforming artifact without prior context.

---

## Next-Stage Handoff

### Fixed (treat as decided)

- The four new substitution keys (`design_point_block`, `canonical_accounts`, `comparables_block`, `fit_grade_band`) — names, sources, sites of injection.
- One helper file (`lib/canonical_accounts.py`), one new config partial (`config/account_walkthrough.md`), the ten-or-so rewritten templates, the two rename-only files.
- Override Candidates: single fenced YAML block under one section; six-field entries; canonical account codes only.
- Design Point block placement: top-of-body selection block + Section 5 quantitative description (Bet 4(c)).
- Two finding Categories (`analysis | model`); no third.
- The four parsers' return shapes per `signal_contract.md`; their call sites do not move.
- Step 4 of generated `model_setup.py` = `result, result_1gw = run_native_and_1gw(...)`; inline two-knob `forward()` is rejected by `strict_helper_only=True`.
- Atomic swap (FR-29): single merge unit; no intermediate "new prompt + old parser" state.

### Open (plan-stage decisions)

- Exact prose of each rewritten template — phrasing, ordering of instruction blocks, mode-specific instruction compactness.
- Exact set of canonical accounts surfaced for each `ConfinementConcept` enum (the helper's per-archetype filter rule). Plan should land a fixture per archetype confirming the right accounts surface for at least the five Item-10 pilot archetypes.
- Whether `account_walkthrough.md` reads as a single prose block or as an enumerated for-each-account checklist (cosmetic; design has no preference).
- Plan-level sequencing across the ten templates (single sweep vs analyze-then-model-then-assess phases) — recommend phasing alongside Item 7 sequencing so dry-runs are useful gates.

### Highest-risk thing to de-risk first in the plan

Two co-equal risks; the plan should de-risk both before mass template work.

1. **Canonical-accounts helper end-to-end.** Land `lib/canonical_accounts.py` + render the canonical-accounts block into a hand-edited (not LLM-edited) `analysis_v2.md`. Analyze dry-run on ARC. If the block is wrong (wrong accounts surfaced, library import unstable, render too verbose), every downstream prompt rewrite is built on sand.
2. **Parser-rewrite return-shape contract.** Before swapping any prompt, write the new line-anchored parsers against hand-crafted "new format" example feedback files (one PASS, one FINDINGS-with-mixed-categories, one REVISE-with-PA-actions) and assert their outputs match the `signal_contract.md` row-by-row table. Then run the existing loop against existing artifacts to confirm the parsers are *backward-failing-loudly* (so a "stale old-format artifact" is rejected cleanly, not silently mis-parsed). This proves the atomic swap can land safely before any production artifact is touched.

If either gate fails, the atomic swap (FR-29) is unsafe — fix before continuing.

---

## Appendix: Files touched (full inventory)

**New:**
- `exploration/concept_analysis/scripts/lib/canonical_accounts.py`
- `exploration/concept_analysis/prompt_templates/config/account_walkthrough.md`

**Rewritten:**
- `exploration/concept_analysis/prompt_templates/analysis_v2.md`
- `exploration/concept_analysis/prompt_templates/output_template.md`
- `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`
- `exploration/concept_analysis/prompt_templates/model_setup_costingfe_edit.md`
- `exploration/concept_analysis/prompt_templates/assessment.md`
- `exploration/concept_analysis/prompt_templates/review.md`
- `exploration/concept_analysis/prompt_templates/config/feedback_format.md`
- `exploration/concept_analysis/prompt_templates/config/assessment_checklist.md`
- `exploration/concept_analysis/prompt_templates/config/analysis_goals.md`
- `exploration/concept_analysis/prompt_templates/config/quality_standards.md`

**Extended (common-var assembly):**
- `exploration/concept_analysis/scripts/run_analysis.py` (`_build_common_vars` adds four keys)
- `exploration/concept_analysis/scripts/lib/loop.py` (`build_model_vars` drops two, adds two)

**Extended (parser internals rewritten — signatures preserved per `signal_contract.md`):**
- `exploration/concept_analysis/scripts/lib/iteration.py` (`parse_verdict_from_feedback`)
- `exploration/concept_analysis/scripts/lib/validators.py` (`has_model_category_findings`, `validate_feedback_verdict`, `validate_review_verdict`; regex constants `FEEDBACK_VERDICT_RE`, `FINDING_HEADER_RE`, `REVIEW_VERDICT_RE` deleted)
- `exploration/concept_analysis/scripts/lib/sources.py` (`parse_proposed_actions`; `PROPOSED_ACTION_RE` deleted)

**Extended (loop wiring):**
- `exploration/concept_analysis/scripts/lib/loop.py` model-setup output-gate (the `# --- Validator selection ---` block) — chain `validate_model_setup_contract(..., strict_helper_only=True)` + `validate_override_registry` onto **all three** branch validators (edit-pass-with-model-findings, edit-pass-analysis-only, cold-start)
- Assess surface (`loop.py::_run_assess`, `run_analysis.py` assess CLI path) — wire `validate_design_point_coherence` + `check_override_count_vs_fit_grade` as LLM-reviewer flag inputs

**Rename leak-through only:**
- `exploration/concept_analysis/prompt_templates/synthesis.md` (`Reuses:` → `Comparables:`)
- `exploration/concept_analysis/prompt_templates/score.md` (`Reuses:` → `Comparables:`)

**Out of scope (not touched):**
- Item 7 helper/validator *public APIs* (signatures and return contracts of `run_native_and_1gw`, `validate_model_setup_contract`, `validate_override_registry`, `validate_design_point_coherence`, `check_override_count_vs_fit_grade`, `enabled_overrides`)
- The four parsers' signatures and return shapes (only their internals change — `signal_contract.md`)
- `lib/model_setup_helpers.py` body (helper is used as-is)
- `prompt_templates/model_setup_freeform*.md` (epic non-goal)
- `prompt_templates/model_critic.md` (Item 9)
- `prompt_templates/design_point_proposal.md` (Item 5)
- `prompt_templates/{address_review,calibrate,gap_check,research,resurface,source_integration}.md` and `prompt_templates/feedback/*` (not in Item 8 scope)
- `prompt_templates/config/scoring_framework.md`

---

**Next Step:** After approval → `/_my_plan` to phase the rewrite (recommend de-risk-helper-first sequencing per Next-Stage Handoff).
