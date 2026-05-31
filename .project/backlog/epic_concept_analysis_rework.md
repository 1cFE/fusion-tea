# Epic: Concept-Analysis Pipeline Rework

**Epic ID**: CONCEPT-REWORK
**Status**: Draft
**Priority**: P0
**Created**: 2026-05-30
**Estimated Effort**: ~9–13 days

**Design**: [`.project/concepts/concept-analysis-rework-design.md`](../concepts/concept-analysis-rework-design.md)
**Touchpoints research**: [`.project/research/20260530-concept-rework-code-touchpoints.md`](../research/20260530-concept-rework-code-touchpoints.md)
**Companion docs**: [`.project/concepts/concept-analysis-rework.md`](../concepts/concept-analysis-rework.md), [`.project/research/20260509-1costingfe-enum-map.md`](../research/20260509-1costingfe-enum-map.md), [`.project/research/20260530-072832_1costingfe-and-pipeline-redesign-context.md`](../research/20260530-072832_1costingfe-and-pipeline-redesign-context.md)

---

## Executive Summary

The concept-analysis pipeline produces per-concept LCOE numbers that look comparable but aren't: each concept's `analysis.md` describes a different (often composite) plant, each `model_setup.py` re-derives library work and buries analyst judgment in code, and "1 GWe NOAK" is reached by a different mechanism for every concept. This epic splits the work into two crisp layers — **specify one named plant** per concept, **project its cost at one standardized scale** via a single two-knob mechanism — and reorganizes the per-concept setup files so the costing library carries the default story and every analyst departure is one accountable, toggleable, evidence-backed override.

**Critical Success Factor**: After rollout, every costingfe concept's `result_1gw` is reached by `forward(net_electric_mw=1000, n_mod=1000/P_native, override_reference_mw=P_native)`, and every cost departure from the library is a single registry entry with `account / value / enabled / provenance / source / rationale`.

---

## Why This Epic?

**Current State**:
- Within a single concept, geometry, performance, and cost anchors often describe three different plants stitched together; the unit the LCOE number describes does not exist as a coherent design anywhere.
- `model_setup.py` files re-pass dozens of library defaults as if deliberate, drifting from library updates and hiding which numbers are actually the analyst's judgment.
- "1 GWe NOAK" is reached differently per concept (native scale, single-knob output-power scaling, no scaling at all) under one label — comparison view is not apples-to-apples.
- Archetype mapping, comparables, and family classification are agent-judgment at runtime; every concept's review is subtly different.
- The critic only runs in-loop (`assess`, `review`), entangled with loop state — can't be applied to archived concepts.

**Future State**:
- Each `analysis.md` has one **Design Point block**: one named plant, its native scale, its source citations; every LCOE parameter on the page describes that unit.
- Each `model_setup.py` is a short, ordered four-step script: spec → native forward → override registry → 1 GWe NOAK forward. No re-passed library defaults.
- Every override is a six-field record (`account / value / enabled / provenance / source / rationale`); flipping `enabled: False` reverts that account to the library's answer.
- Archetype, archetype-fit grade, comparables, and the design-point selection (named plant, `P_native`) are pre-computed project-level tables — batch-populated and hand-verified before analyze runs — read by the orchestrator, not invented at runtime.
- `model_critic` is a standalone tool invokable against any concept directory at any time.
- `concept_explorer` reads each concept's `result_1gw` at exactly 1000 MWe, reached by the same two-knob mechanism — comparison is apples-to-apples by construction.

---

## Success Criteria

- [ ] 1costingFE accepts non-integer `n_mod > 0`; override scaling under the two-knob call is verified by test.
- [ ] Ontology, archetype-fit, comparables, and design-point tables exist as the single source of truth; consumed by orchestrator and prompts.
- [ ] All four tables are batch-populated and hand-verified before analyze runs; the design-point table fixes the named plant and `P_native` per concept, and `analyze` reads (does not choose) them.
- [ ] Every non-`None` fit-grade concept has a regenerated `analysis.md` with a Design Point block and a regenerated `model_setup.py` matching the four-step shape.
- [ ] Every regenerated `model_setup.py` exposes `model`, `result`, `result_1gw` at module level; `result_1gw` is reached by the two-knob call at `net_electric_mw=1000`.
- [ ] Override registry validator enforces six-field entries; AST validator enforces the module-level contract and the `net_electric_mw=1000` call shape.
- [ ] `model_critic` runs cleanly against an archived concept (no loop-state dependency).
- [ ] `concept_explorer` reads `result_1gw` from every costingfe concept with no fallback path; `Confinement-Family:` is read from frontmatter, not body prose.
- [ ] Toggling all overrides off in any `model_setup.py` produces the library's bare answer for that concept's specified plant (manual spot-check on the pilot set).

---

## Backlog Items

> Each item below names the files touched and the general success criteria only. Mechanism, data shapes, and any cross-cutting design decisions are deferred to that item's own `spec.md` / `design.md`.
>
> **Sequencing principle**: the high-risk bets in this rework are agent-driven (Design Point extraction, override honesty, critic acuity), not coding. Phase 0 front-loaded a cheap throwaway probe (Item 1) that exercised those bets *before* any plumbing was built, so bet failure would be caught on day 2, not day 7.
>
> **Phase 0 status (2026-05-31)**: Item 1 is complete and did its job — its biggest output was the *design change* it motivated, moving design-point selection upstream behind a human-verified gate (folded into Item 5). That change converted the top agent-driven risk (selection coherence) from a silent-failure mode into a graceful-degradation one, which retired the rationale for the follow-on probes. Items 2 and 3 are therefore **superseded**, not pending: their residual signal is recovered downstream (Item 5's per-row verification gate; the Item 10 pilot; on-demand `model_critic`) at no extra cost. Phase 0 is effectively done at Item 1. The one carried-forward obligation is the "reshape, do not copy" note on the Item 1 prompts (see Items 8 and 9).

---

## Phase 0 — De-risk the agent-driven bets (~1 day; Item 1 only — Items 2 & 3 superseded)

### Item 1: End-to-End Manual Prototype (one concept) — ✅ COMPLETE (2026-05-30)

**Type**: Research / Throwaway
**Effort**: ~1 day (actual: ~1 day)
**Dependencies**: None.
**Deliverable**: [`.project/active/concept-rework-prototype/findings.md`](../active/concept-rework-prototype/findings.md) (commit 1f21630)

**What this is**: a hand-driven walkthrough of the rework on a single concept, with everything stubbed or hand-written. No helpers, no validators, no template files, no CLI subcommands. Goal is signal, not artifacts.

**Key bets this exercises** (the rework rests on all six; the prototype is how we find out which hold):

1. **Two-knob mechanism produces sensible numbers** — `forward(net=1000, n_mod=1000/P, override_reference_mw=P)` gives comparable per-account values once overrides scale through.
2. **Library carries the default story** — for most concepts at most accounts, the bare library answer (given good spec inputs) is close enough that the override registry stays small. If a real concept needs 30 overrides, the framing collapses.
3. **Agent can identify a Design Point from a dossier** — one named plant, native scale, source-cited, *coherently*. (Stability across re-runs was originally Item 2's job — now superseded, since selection moved behind the human-verified gate; this item tested "can it do it once".)
4. **Agent populates overrides honestly** — `value`, `provenance`, `source`, `rationale` actually trace to company-stated numbers, not LLM dressing-up of library defaults.
5. **`model_critic` finds real issues** — looking at the artifacts, the critic surfaces things worth acting on, not generic boilerplate. (Acuity against *existing* artifacts was originally Item 3's job — now superseded, since the critic is cheap on-demand; this item tested it against the prototype's freshly-made artifacts.)
6. **Determinism-upstream is worth the up-front cost** — having the archetype-fit and comparables rows pre-populated noticeably tightens the analyze and critic prompts. If we don't feel the difference, the table layer needs re-justification.

**Activities**:
- Pick one concept with a clean dossier and a likely-High archetype fit.
- Hand-write the archetype-fit row and a tiny comparables stub (just the rows needed for this concept). [Exercises bet #6.]
- Hand-draft the new analyze prompt and run it one-shot (`claude -p`) against the dossier. Read the Design Point block and override candidates by eye. [Exercises bets #3, #4.]
- Hand-write the four-step `model_setup.py` using current 1costingFE; run it. Inspect `result` and `result_1gw` per-account values; verify against current-pipeline numbers for the same concept. [Exercises bets #1, #2; empirically de-risks Item 4's library precondition before formal test work.]
- Hand-draft the `model_critic` prompt and run it against the artifacts. Read its output. [Exercises bet #5.]
- Write a short findings doc.

**Success Criteria**:
- [x] Findings doc enumerates each of the six bets above with a verdict: **held / wobbled / broke**, with a one-paragraph "what we saw" per bet.
- [x] If bet #1 (override scaling under two-knob) held empirically, Item 4 scope shrinks to "formalize as test"; if it broke, Item 4 scope grows and the fix is informed by what we saw. *(Wobbled — Item 4 scope grew, see below.)*
- [x] Hand-drafted prompts (analyze, model_setup discipline note, critic) are saved as the starting point for Items 8 and 9.

**Kill switch**: if bet #3 (Design Point extraction is incoherent) or bet #4 (overrides come back as dressed-up library defaults with no real provenance) breaks, **stop and rethink** before committing to Phase 1. *(Neither broke — proceed to Phase 1.)*

**Outcomes — six-bet verdicts** (full write-up in `findings.md`):

| Bet | Verdict | Implication |
|---|---|---|
| 1. Two-knob override scaling | wobbled | `_scale_overrides` runs its reference forward at the caller's `n_mod`, inflating C220101/C220106 overrides ~47%. Item 4 must land the fix, not just write a test (mechanical ~5-line change). |
| 2. Library carries default story | held | Library-bare 1 GWe LCOE = 146 $/MWh (at P_native=233) — defensibly NOAK-range. Override count for High fit was 4 — within rubric. |
| 3. Design Point extraction | held | Sonnet correctly picked ARC 2015 233 MWe over SPARC and the 2025 400 MWe target on its first attempt, citing the design's stated selection rule. |
| 4. Override honesty | wobbled (bidirectional) | LLM honest on provenance but used wrong account-code namespace and underproposed; operator hand-write over-claimed `direct` for derived values. A `provenance` validator + cross-artifact consistency check (new finding for Item 7) covers both directions. |
| 5. Critic acuity | held strongly | Independent critic (cold, no session context) caught the very `P_native` mismatch the operator introduced (analysis.md 233 vs model_setup.py 400), plus three other specific issues. Not boilerplate. |
| 6. Determinism upstream | held (mild signal, single-concept) | Single-concept evidence only. With Item 2 superseded, this bet is now confirmed in-flight during Item 5 (the design-point/comparables tables on Med/Low-fit concepts) and the Item 10 pilot, rather than by a standalone probe. |

**Knock-on scope adjustments to Phase 1**:
- **Item 4** scope grows: "formalize as test" → "fix `_scale_overrides` + test" (still ~0.25–0.5 d).
- **Item 7** absorbs a new cross-artifact-consistency validator: `P_native` and `provenance` labels must match between `analysis.md` and `model_setup.py`.
- **Item 8** unchanged effort but the starting prompt needs canonical 1costingFE account-code schema injection (~2h) and an explicit per-account walk-through pass (~2h).
- **Item 9** unchanged effort but the starting prompt needs an explicit scope boundary (artifact review, not source review — the critic raised a sourcing concern that wasn't actionable from the artifacts alone).

**Deliverables produced**:
- `.project/active/concept-rework-prototype/findings.md` — six-bet verdicts + self-review
- `.project/active/concept-rework-prototype/prompts/{analyze_v2,model_critic}.md` — Item 8 / Item 9 starting points
- `.project/active/concept-rework-prototype/tables/{archetype_fit,comparables}.csv` — upstream-table seeds (one row each for concept 01)
- `.project/active/concept-rework-prototype/artifacts/{analysis.md, model_setup.py, model_output.txt, critic_review.md, probe_override_scaling.{py,txt}}`

(Stored under `.project/active/` rather than `/tmp/` so the prototype survives the session and stays inspectable while Phase 1 specs are being written.)

> ⚠ **Item 1 prompts: reshape, do not copy.** The `analyze_v2.md` draft conflates design-point *selection* with quantitative *extraction* (it chose `P_native=233` itself). Under the post-2026-05-31 design these are two surfaces: a design-point **proposal** prompt (Item 5, feeds the human-verified table) and an **extraction** analyze prompt that reads `P_native` as a fixed input (Item 8). The `model_critic.md` draft likewise predates the artifact-vs-source scope boundary the findings flagged (Item 9). Use these drafts as *content* starting points; do not productionize their structure as-is. This is the one obligation carried forward from the superseded Items 2 & 3.

---

### Item 2: Prompt-Stability Probe — ⊘ SUPERSEDED (2026-05-31)

**Why superseded**: This probe was designed for the *old* workflow, where `analyze` chose the design point and its run-to-run selection stability was a Phase 1 go/no-go. The design-point-selection-upfront decision (folded into Item 5 on 2026-05-31) moved selection into a batch-proposed, **human-verified** upstream table — so selection can no longer fail silently; it degrades gracefully (a weak proposal just means more human effort at the gate, caught on every row). The residual bet — quantitative-extraction stability *given a fixed design point* — is lower-risk (pinning the plant makes extraction easier, not harder) and is exercised for free during Item 5's batch-populate-then-hand-verify and the Item 10 pilot, which spans High/Med/Low fit. There is no remaining failure mode a standalone Phase 0 probe catches more cheaply than those two gates.

Equally decisive: the Item 1 hand-drafted analyze prompt *conflates* selection and extraction (it chose `P_native` itself). Running this probe against that prompt as-is would test the old shape; reshaping it first to the selection/extraction split is Item 8 work. Doing a throwaway split here just to run a low-value probe is the half-measure this decision rejects.

**Net**: cancelled. The signal it would have produced is recovered downstream (Item 5 verification gate; Item 10 pilot) at no extra cost. See the "Item 1 prompts: reshape, do not copy" note on Item 8.

---

### Item 3: Critic Acuity Probe (against existing artifacts) — ⊘ SUPERSEDED (2026-05-31)

**Why superseded**: Item 1 already cleared the critic-acuity bet (#5) with *strong* signal — run cold with no session context, the critic caught the very `P_native` mismatch the operator introduced plus three other specific issues, not boilerplate. The remaining delta this item would have added (critic vs. *existing un-regenerated* concepts) is near-zero-cost to discover just-in-time: `model_critic` is standalone and on-demand by design, so if it underperforms in the wild you find out the first time you run it — with no plumbing committed and nothing to roll back. The "catch it cheaply before building" rationale doesn't apply to a tool that's already cheap to run after building.

Also, like Item 2, this probe would run the Item 1 critic prompt as-is, which predates the selection/extraction split and lacks the artifact-vs-source scope boundary the findings flagged. Reshaping it is Item 9 work.

**Net**: cancelled. Critic acuity is covered by Item 1's strong signal plus on-demand use from Item 9 onward. See the "Item 1 prompts: reshape, do not copy" note on Item 9.

---

## Phase 1 — Build the plumbing (informed by Phase 0)

### Item 4: 1costingFE Library Preconditions — ✅ COMPLETE (2026-05-31)

**Type**: Code/Integration
**Effort**: 0.25–0.5 day (Phase 0 has already traced the root cause; this is a small mechanical fix + tests). *Actual: ~0.25 day.*
**Dependencies**: Item 1 (root cause traced and reproduced in Phase 0).
**Spec**: [`.project/active/costingfe-library-preconditions/spec.md`](../active/costingfe-library-preconditions/spec.md)
**Commit**: `1costingfe a2153ad` on branch `fix/scale-overrides-reference-frame`.

**Files touched** (in `~/1cfe/1costingfe/`):
- `src/costingfe/validation.py:90` — change `n_mod: int = Field(default=1, ge=1, strict=True)` to a positive float field.
- `src/costingfe/model.py:849-896` — `_scale_overrides`: change the reference forward to use `n_mod=1` (see bugfix below).
- Library tests covering both changes.

**Bugfix (from Phase 0 findings)**:

`_scale_overrides` currently runs its reference forward at `(net=override_reference_mw, n_mod=caller_n_mod)`. This makes per-module power in the reference run equal `override_reference_mw / caller_n_mod` instead of `override_reference_mw`. For accounts with thermal-power dependence (e.g. structure, vacuum vessel), the ratio used to scale the user's override is computed against the wrong reference, silently inflating per-module overrides.

Concrete example from Phase 0 (ARC, P_native=400, n_mod=2.5): per-module C220101 override inflated 47% (caller wrote $349M intending "structure cost for one 400 MWe module"; library scaled it as if it meant "structure cost for one 160 MWe module"). At corrected P_native=233, n_mod=4.29, the same bug applies with a different ratio.

Change the reference forward to:

```python
reference_result = self.forward(net=override_reference_mw, n_mod=1, ...)
```

So the reference frame matches what the analyst writes the override against — one module at the design-point native power.

**Success Criteria**:
- [x] `n_mod` accepts any positive real value. *(validation.py:90 widened to `float`, `gt=0`.)*
- [x] `_scale_overrides` reference forward uses `n_mod=1`; per-module reactor-island overrides pass through unchanged at native per-module power (ratio = 1.0 for power-dependent accounts when target per-module power = reference per-module power). *(model.py:865 — `dict(forward_kwargs, n_mod=1)`.)*
- [x] Regression test reproduces the Phase 0 prototype's two-knob call for at least one per-module power-dependent account and one plant-aggregate account; asserts correct scaling. *(4 new tests in test_model.py: C220101 power-dependent passthrough, C220103 no-power-term passthrough, CAS27 per-module passthrough, CAS22 plant-aggregate scaling.)*
- [x] Library version pinned for downstream consumption. *(Fusion-tea uses editable local install; no version bump required — fix is live.)*

**Spot finding folded into the spec**: Phase 0's probe table labeled CAS27 as plant-aggregate, but its default `cas27_special_materials(cc, pt.p_net, ...)` reads `pt.p_net` which is per-module. CAS27 is therefore per-module and passes through unchanged under the fix. CAS22 is the actual plant-aggregate account (its default already sums `per_module_equipment * n_mod + labor + plant_wide`); the plant-aggregate regression test uses CAS22 instead of CAS27.

---

### Item 5: Deterministic Project Tables + Comparables Sanity-Check

**Type**: Implementation
**Effort**: 1.5–2 days (up from 1–1.5: adds the design-point table and the batch-populate-then-hand-verify gate across four tables).
**Dependencies**: Item 1 (Phase 0 findings sanity-check the table schemas before all rows are populated). Parallel with Item 4.

**What this is**: build the four upstream project-level tables that the rest of the pipeline reads as the single source of truth, **batch-populate** them, and **hand-verify each** before any concept's `analyze` stage runs. The four tables are *not* populated the same way — the method follows how much of each is deterministic vs. judgment. Do not apply one uniform "batch-LLM then verify" pass to all four; two of them have a different correct path.

**The four tables and their population methods**:

1. **Ontology table** — confinement type, fuel, taxonomy traits. *Method:* batch agent extraction, then hand-verify against the dossier. Mostly factual / cross-checkable; low judgment. **Populated first** — comparables derives from it.
2. **Archetype-fit table** — `ConfinementConcept` enum value + fit grade (`High` / `Med` / `Low` / `None`). *Method:* **reshape** the existing hand-authored enum-map ([`enum-map`](../research/20260509-1costingfe-enum-map.md)) — re-pin to the current 1costingFE commit and re-grade its Rank 1/2/3 ranking into the four-grade vocabulary. Rank 2 ("notable architectural strain") splits across Med and Low per concept; that split is the judgment hand-verification settles. **Not** a from-scratch batch pass — re-batching discards existing hand judgment.
3. **Comparables table** — comparable-concept set per concept. *Method:* **deterministic derivation** from the ontology table (a script, not an agent); hand-verify the derivation, not per-row LLM judgment. An LLM batch pass here reintroduces the runtime nondeterminism the rework exists to remove.
4. **Design-point table** (new — folds in the design-point-selection-upfront decision) — the *selection* of the one named plant per concept: design name, maturity tier, `P_native`, primary source citations, one-line selection rationale. *Method:* batch agent proposal from each dossier, then **hand-verify each row**. This is the most judgment-heavy table and the gate matters most here — `P_native` drives `n_mod = 1000/P_native` and the entire cost projection (Phase 0: ARC at 233 vs 400 MWe moved 1 GWe LCOE from 668 to 403 $/MWh).

**Selection vs. extraction seam**: the design-point table carries only the *selection* (which plant, `P_native`, sources). The full quantitative description (geometry / physics / performance) is still extracted downstream by `analyze`, against the plant the table has fixed. `analyze` reads the named plant and `P_native` as inputs and never chooses or re-derives them — the same contract as `Comparables:`.

**Population order (a DAG, not four independent passes)**:
```
ontology (batch-extract + verify) ──> comparables (derive + verify)
archetype-fit (reshape enum-map + re-grade + verify)      [independent]
design-point (batch-propose + verify each row)            [independent]
```

**Files touched** (locations pinned in `.project/active/concept-rework-tables/spec.md`):
- `exploration/concept_analysis/tables/ontology.csv` — 8 columns; ontology vocab extended with `electrostatic-steady-state` (Orbitron/Polywell) and `mechanical-pulsed` (GF/MIF Tech).
- `exploration/concept_analysis/tables/archetype_fit.csv` — reshaped from [`enum-map`](../research/20260509-1costingfe-enum-map.md); Rank-2 split decisions recorded in `fit_rationale`.
- `exploration/concept_analysis/tables/comparables.csv` — generated by `scripts/derive_comparables.py`; idempotent; v1 rule clusters `{tokamak, spherical-tokamak}`.
- `exploration/concept_analysis/tables/design_point.csv` — 12 columns including new `grounding_confidence` and `trace_path`; one row per non-`None` concept that has a published `P_native` (any quality).
- `exploration/concept_analysis/tables/design_point_freeform_routes.md` — auto-appended log for concepts with literally no `P_native` published anywhere.
- `exploration/concept_analysis/tables/README.md` — column dictionary, v1 derivation rule, vocab extensions, gate log.
- `exploration/concept_analysis/scripts/derive_comparables.py` — deterministic comparables derivation.
- `exploration/concept_analysis/scripts/ingest_design_point_proposals.py` — YAML→CSV ingestion with schema validation; installs per-concept trace artifacts; `--only` merges into existing CSV preserving gate metadata.
- `exploration/concept_analysis/scripts/sanity_check_comparables.py` — outlier-flag sanity-check; pure-function core smoke-tested.
- `exploration/concept_analysis/prompt_templates/design_point_proposal.md` — selection-only proposal prompt (carved from Item 1 `analyze_v2.md` draft); emits trace + structured YAML row in one document; enforces phase-naming, multi-module rule (`P_native` is per-module), plant-stitching-forbidden, and `grounding_confidence` honesty.
- `.project/active/concept-rework-tables/run_proposal_batch.py` — `claude -p` batch runner; saves trace, extracts YAML block, strips LLM preamble.
- `exploration/concept_analysis/analyses/{cid}/design-points/baseline.{md,yaml}` — per-concept reasoning trace + YAML row, first-class artifacts living alongside `analysis.md` / `model_setup.py`. The trace carries the source-walking, candidate enumeration, and directional sensitivity implications for each rejected alternative.

**Success Criteria**:
- [ ] All four tables exist and cover every concept.
- [ ] Each table is batch-populated by its correct method (factual extraction / enum-map reshape / deterministic derivation / dossier proposal) and hand-verified; the verification gate is documented per table.
- [ ] Design-point table fixes one named plant and `P_native` per non-`None` concept that has any published `P_native`, with primary sources, selection rationale, and `grounding_confidence` (high/medium/low); every row is human-signed-off.
- [ ] Every `design_point.csv` row has a corresponding trace artifact at `analyses/{cid}/design-points/baseline.md` (full reasoning, candidate enumeration, directional sensitivity surfaces) and `baseline.yaml` (machine-readable row).
- [ ] Concepts with literally no published `P_native` anywhere are routed to freeform via `design_point_freeform_routes.md` — distinct from the architecture-mappability `fit_grade=None` freeform route.
- [ ] Comparables are derived deterministically from the ontology (no runtime LLM judgment).
- [ ] Sanity-check script produces structured output for an LLM reviewer (not a verdict) on a hand-fed pair of concepts. (This is the *downstream* result-review surface — distinct from the upstream table-verification gate above.)

**Surprise finding folded into design** (discovered during the pilot batch on 2026-05-31): architecture-mappability (`fit_grade`) and design-point grounding (`grounding_confidence`) are *orthogonal* — Cortex (#03) is a Low-fit concept with no published engineering plant; Helion (#08) is a Low-fit concept with a well-documented Orion target. A concept can be cost-mappable but data-poor (asterisked in comparison view, runs through costingfe normally) or data-rich but architecturally bespoke (freeform branch). The `grounding_confidence` field carries this honesty; Item 6's orchestrator must consume both axes (see Item 6 below).

---

### Item 6: Pipeline Glue — Frontmatter, `concepts.py`, CLI Subcommands — ✅ COMPLETE (2026-05-31)

**Type**: Code/Integration
**Effort**: 1–1.5 days
**Dependencies**: Item 5.

**Implementation**: `.project/active/concept-rework-pipeline-glue/` (spec/design/plan). Landed in 5 phases; 289 passed / 5 skipped in `exploration/concept_analysis/scripts/`. See `plan.md` Implementation Notes for per-phase detail. Design amended the epic's two-state routing to **four** states (`costingfe` / `costingfe-asterisked` / `freeform-deferred` / `pending-design-point`) — `pending-design-point` distinguishes "Item 5 batch hasn't reached this row yet" from judged-freeform.

> **Open scope nuance (needs a call):** success criterion 3 below mentions emitting *a reference to the per-concept trace* (`analyses/{cid}/design-points/baseline.md`) as a frontmatter field. The Item 6 **spec** (field block, spec.md §"Frontmatter field block") and **design** scoped the design-point frontmatter to Name / Maturity / `P-Native` / `Grounding-Confidence` only — they did **not** include a trace-path field. Implemented to spec, so `make_frontmatter` does not emit it. The `design_point.csv:trace_path` column exists, so adding a `Design-Point-Trace:` line is a one-line change if wanted — deferred pending confirmation rather than added beyond the approved spec.

**Files touched** (in `exploration/concept_analysis/scripts/`):
- `lib/concepts.py` (replace hard-coded archetype mapping with table read).
- `lib/frontmatter.py` (new fields + `Reuses` → `Comparables` rename; design-point selection fields — named plant, maturity tier, `P_native` — emitted from the design-point table).
- `lib/loop.py` (minimal — drop dependence on dropped validators).
- `run_analysis.py` (new subcommands: regenerate-concept, init-tables).
- Knock-on `Reuses` renames across `lib/`.

**Success Criteria**:
- [x] Archetype routing reads the table; freeform vs costingfe routing consumes **both** `fit_grade` and `design_point.csv` membership: *(table-driven `get_model_path` (fit-grade-only, FR-1) + four-state `get_comparison_status`; low-grounding → `costingfe-asterisked`.)*
  - `fit_grade = None` → freeform (architecture has no ENUM analog).
  - `fit_grade != None` AND no `design_point.csv` row (concept in `design_point_freeform_routes.md`) → freeform (architecture mappable but no `P_native` exists anywhere).
  - `fit_grade != None` AND `design_point.csv` row present → costingfe, with `grounding_confidence` carried into frontmatter; low-grounding rows are **asterisked** in the comparison view.
- [x] New frontmatter fields emitted and pre-populated from the upstream tables: design-point selection (named plant, maturity tier, `P_native`) + `grounding_confidence`; all orchestrator-owned, not analyzer-editable. *(`Reuses:`→`Comparables:`; `Confinement-Family`/`Archetype`/`Archetype-Fit`/`Comparison-Status` added.)* **Trace-path reference field NOT emitted** — scoped out by the Item 6 spec/design (see nuance note above).
- [x] Regenerate-concept and init-tables subcommands run end-to-end on a dry-run target. *(`init-tables` exits 0 on the repo; `regenerate-concept --dry-run` prints the stage sequence and refuses non-runnable concepts with state-specific reasons.)*

---

### Item 7: Shared `model_setup` Helpers + Validator Rework

**Type**: Implementation
**Effort**: 1–1.5 days
**Dependencies**: Items 1 (prototype informs the helper API shape), 4, 5.

**Files touched** (in `exploration/concept_analysis/scripts/`):
- `lib/model_setup_helpers.py` (new shared utility module).
- `lib/validators.py` (drop the regex-on-LLM-markdown validators; add new contract checks for `model_setup.py` and the override registry).

**Success Criteria**:
- [ ] A regenerated `model_setup.py` can be written as a short, ordered script against the shared helpers, with no per-concept duplication of the two-knob forward pattern or the override-registry → `cost_overrides` translation.
- [ ] Validators enforce the design's module-level contract (`model`, `result`, `result_1gw` at module level; `result_1gw` reached at `net_electric_mw=1000`) and the override-registry shape; fragile regex validators are removed.
- [ ] Validators enforce design-point coherence: `P_native` agrees three ways — the design-point table row, the `analysis.md` Design Point block, and `model_setup.py` — and each shared override's `provenance` label matches between `analysis.md` and `model_setup.py`. (Phase 0 self-review surfaced both as real, AST-checkable drift modes — operator picked `P_native=400` against an analysis that said 233, and mislabeled `derived` overrides as `direct`.)
- [ ] Loop runs cleanly on a dry-run without the dropped validators.

---

### Item 8: Prompt Template Rework

**Type**: Implementation
**Effort**: 1–1.5 days (down from 1.5–2: Phase 0's hand-drafts are the content starting point).
**Dependencies**: Items 1 (**reshapes — does not copy** — the Phase 0 hand-drafts: split selection out to Item 5's proposal prompt, keep extraction here; see the reshape note on Item 1), 5, 6, 7.

**Files touched** (in `exploration/concept_analysis/prompt_templates/`):
- `analysis_v2.md` + `output_template.md`.
- `model_setup_costingfe.md` + `model_setup_costingfe_edit.md`.
- `assessment.md` + `review.md` + `config/feedback_format.md` + `config/assessment_checklist.md`.
- `config/analysis_goals.md`, `config/quality_standards.md`, `config/scoring_framework.md`.
- `synthesis.md`, `score.md` (rename leak-through only).

**Out of Scope**: `model_setup_freeform*.md` (deferred per design non-goal).

**Success Criteria**:
- [ ] Dry-run on one concept produces an `analysis.md` containing the Design Point block and a `model_setup.py` matching the four-step shape.
- [ ] `analysis_v2.md` prompt takes the design-point *selection* (named plant, maturity tier, `P_native`, primary sources) as a fixed input from the design-point table / frontmatter — it does **not** choose or re-derive the plant. Its job is the quantitative *extraction* for that fixed plant.
- [ ] `analysis.md`'s Design Point block carries the *full* specification of the target design point — every field downstream needs (name, maturity tier, `P_native`, geometry/physics/performance values, override provenance per account) is explicit and source-cited. The selection fields match the design-point table row; the geometry/physics/performance values are the extracted quantitative description. Nothing required downstream is left implicit.
- [ ] `model_setup_costingfe.md` prompt instructs the agent to **start by identifying the target design point from `analysis.md`** — reading `P_native`, the spec kwargs, and override provenance labels directly from the Design Point block rather than re-deriving them from the dossier.
- [ ] `analysis_v2.md` prompt pins override `account` identifiers to the canonical 1costingFE namespace (`C220101`, `C220103`, `CAS27`, etc.) by injecting the account-code list as a schema. (Phase 0 finding: LLM defaulted to `CAS22.1.3`-style codes that would silently miss in the `cost_overrides` dict.)
- [ ] `analysis_v2.md` prompt walks override discovery as an explicit per-account checklist over the canonical CAS accounts ("does the dossier name a quantity, mass, or unit cost for this account?") rather than open-ended discovery. (Phase 0 finding: open-ended discovery underproposed — analyze step surfaced 2 of 4 findable overrides for ARC.)
- [ ] `model_setup_costingfe.md` prompt forbids overriding values that 1costingFE handles via defaults (`availability`, `lifetime_yr`, `interest_rate`, `inflation_rate`, `eta_th`, `eta_de`, and others). These are not per-concept analyst choices; the library defaults apply uniformly across all concepts.
- [ ] Sweep / what-if text output remains allowed in `model_output.txt`; `result` and `result_1gw` remain the standardized baseline consumed by the explorer.
- [ ] Assess/review output is parse-robust under the new validators (no reliance on the dropped regex paths).
- [ ] Quality-standards doc reflects the new discipline (no re-passing of library defaults; every parameter describes the design point).

---

### Item 9: `model_critic` Standalone Tool

**Type**: Code/Integration
**Effort**: 0.5–1 day (down from 1: Phase 0's hand-drafted critic prompt is the content starting point).
**Dependencies**: Items 1 (**reshapes — does not copy** — the Phase 0 critic prompt: add the artifact-vs-source scope boundary the findings flagged; see the reshape note on Item 1), 5.

**Files touched** (in `exploration/concept_analysis/`):
- `scripts/agents/model_critic.py` (new).
- `prompt_templates/model_critic.md` (new).
- `scripts/run_analysis.py` (new subcommand).

**Success Criteria**:
- [ ] `model_critic` runs against active **and** archived concept directories with no loop-state dependency and writes one review document next to the artifacts.
- [ ] The critic prompt scopes the review to the *artifacts* (analysis.md, model_setup.py, results), not the dossier sources — Phase 0 surfaced an out-of-scope sourcing critique that wasn't actionable from the artifacts alone.

---

---

## Phase 2 — Pilot + bulk rollout

### Item 10: Explorer Adapter + Pilot Regeneration

**Type**: Code/Integration + Execution
**Effort**: 1.5–2 days
**Dependencies**: Items 4, 6, 7, 8, 9.

**Files touched**:
- `exploration/concept_explorer/extract_explorer_data.py` (frontmatter read; drop `result_1gw` fallback; fractional `n_mod` verification; narrative-extraction prompt).
- New artifacts under `exploration/concept_analysis/analyses/` for 3–5 pilot concepts spanning High / Med / Low archetype-fit.
- `pilot_report.md` in the work-item directory.

**Success Criteria**:
- [ ] Explorer reads every pilot concept without a fallback path; family field resolves from frontmatter.
- [ ] Every pilot `result_1gw` is at exactly `net_electric_mw=1000` via the two-knob mechanism.
- [ ] Human-entered content (`review.md` and any other known human-authored artifact) is preserved before regeneration.
- [ ] Concepts with `grounding_confidence: low` are visually asterisked in the comparison view (existing asterisk pattern already used for `fit_grade=None`); the user can tell at a glance which numbers are well-grounded vs poorly-grounded without reading the trace.
- [ ] Pilot set spans the **two-axes grid**: High/Med/Low `fit_grade` × high/medium/low `grounding_confidence`. At minimum: one High-fit-high-grounding (e.g. ARC), one Low-fit-medium-grounding (e.g. Helion Orion), one Low-fit-low-grounding (e.g. Cortex, if it has any `P_native` at all). This exercises the asterisk path and confirms the orchestrator's two-axes routing from Item 6.
- [ ] Pilot report enumerates issues found and any fixes folded back into templates/helpers/validators before bulk rollout.

---

### Item 11: Bulk Regeneration

**Type**: Execution
**Effort**: 1–1.5 days
**Dependencies**: Item 10.

**Files touched**:
- Regenerated artifacts under `exploration/concept_analysis/analyses/` for every non-`None` fit-grade concept.
- Snapshots of any User-Decisions worth preserving (to `.project/`) before deletion.
- Per-batch logs in the work-item directory.

**Out of Scope**: freeform concepts — both `fit_grade=None` (architecture has no enum analog) and the new `fit_grade != None`-but-no-`P_native` route (architecture mappable but no published plant). Both are asterisked in the explorer and not regenerated here.

**Success Criteria**:
- [ ] Every non-`None` concept has fresh artifacts conforming to the new contract; validators pass.
- [ ] Cross-concept comparison view shows uniform `result_1gw @ 1000 MWe` semantics across all non-freeform concepts.

---

## Phase 3 — Aspirational

### Item 12: Native-Scale Projection (per-family, where defensible)

**Type**: Research + Implementation
**Effort**: TBD (~1–2 days for DT tokamak alone; scope grows per additional family).
**Dependencies**: Item 11 (replication-floor baseline shipped first).

**Status**: Aspirational. Does **not** block the rework's main delivery. The replication floor stays as the apples-to-apples cross-concept reference number; this item adds a *second*, family-conditional projection alongside it.

**Why**: replication-floor numbers can read as damningly high to a reader who doesn't internalize the framing. Where the family's physics-of-scale-up is mature enough to defend a single-machine 1 GWe design (DT tokamak with 1costingFE is the clear case; most other families much less so), publishing both numbers — the conservative ceiling and the optimistic native-scale — gives reviewers a defensible **range**, and the two projections sanity-check each other.

**Files touched**:
- `prompt_templates/analysis_v2.md` — new "Scaling Story" section: what does 1costingFE and the literature say about how this family scales a single machine to 1 GWe? Document the physics-of-scale-up, regime limits, and what's known vs unknown. For families where native scaling isn't defensible, the section explicitly says so and explains why.
- `prompt_templates/model_setup_costingfe.md` — when the scaling story supports it, attempt an additional `forward()` call producing `result_1gw_native` at `(net=1000, n_mod=1)` with the family-appropriate physics scaling. Gated on the Scaling Story's defensibility judgment.
- `exploration/concept_explorer/extract_explorer_data.py` and views — present `result_1gw` (replication floor) and `result_1gw_native` (where it exists) as a range; asterisk concepts where only the floor is available.

**Out of Scope**:
- Modifying the replication-floor projection or its role as the comparable cross-concept reference.
- Inventing physics-of-scale-up where the literature doesn't support it.
- Freeform / archetype-fit-`None` concepts.

**Success Criteria**:
- [ ] At least one well-understood family (likely DT tokamak) has both `result_1gw` and `result_1gw_native` populated across its concepts, with a documented scaling rationale in each `analysis.md`.
- [ ] For families where native scaling isn't defensible, the Scaling Story section documents the literature and explicitly states why scaling isn't attempted.
- [ ] Explorer presents the two numbers as a range where both exist; reviewers can see the floor and the native-scale projection side by side.

---

## Dependencies

**External**:
- 1costingFE library (Item 1 modifies it; downstream items pin the updated version).
- Claude CLI / agentic-mbse for pipeline execution.

**Internal**:
- None — this epic owns the rework end-to-end.

**Item Dependency Graph**:
```
Phase 0 — De-risk
  Item 1 (E2E manual prototype) ✅ COMPLETE
     │   ↳ motivated the design-point-upfront change (folded into Item 5)
     │   ⊘ Item 2 (prompt-stability) SUPERSEDED — selection now human-gated
     │   ⊘ Item 3 (critic acuity)   SUPERSEDED — Item 1 cleared bet #5; critic is on-demand
     │
     │   [Phase 0 effectively complete at Item 1 — proceed to Phase 1]
     ▼
Phase 1 — Plumbing
  Item 4 (library prereqs)   Item 5 (4 tables + design-point gate + sanity check)
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                          Item 6      Item 7       Item 9
                          (glue)      (helpers      (critic
                                       + valid.)    productionized)
                              ▲           ▲
                              └─────┬─────┘
                                    ▼
                              Item 8 (prompts productionized)

Phase 2 — Rollout
  Item 10 (explorer adapter + pilot 3–5 concepts)
        │
        ▼
  Item 11 (bulk regenerate)
        │
        ▼  [aspirational, non-blocking]
Phase 3 — Aspirational
  Item 12 (native-scale projection, per-family)
```

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Agent can't reliably extract a coherent Design Point from a dossier | **High** — specification layer never settles; whole rework rests on this | Item 1 probed this (bet #3, held). Design-point *selection* is now a batch-proposed, **human-verified** upstream table (Item 5), so a bad selection is caught at the gate before any expensive stage runs — it degrades gracefully (more human effort), not silently. This is why Item 2's stability probe was superseded. |
| Agent populates overrides as dressed-up library defaults rather than honest provenance | **High** — accountability story is theater | Item 1 inspected override provenance by hand (bet #4, wobbled-bidirectional — held on direction). Item 7's `provenance` validator + cross-artifact consistency check now enforces it both ways (LLM over-claiming and operator over-claiming). |
| `model_critic` rubber-stamps rather than finds issues | High — independent-review story collapses | Item 1 cleared this (bet #5, held strongly — caught the operator's real `P_native` mismatch cold). `model_critic` is on-demand by design, so any in-the-wild weakness surfaces the first time it runs, at no committed cost — which is why Item 3 was superseded rather than gated. |
| 1costingFE override-scaling under the two-knob call doesn't behave as design assumes | High — invalidates the cost-projection invariant | Item 1 exercised it empirically (bet #1, wobbled — root cause traced); Item 4 lands the `_scale_overrides` fix + test. |
| New prompt structure produces lower-quality `analysis.md` than current free-form template | Med — pilot exposes; bulk regen amplifies | Item 8 dry-run on one concept gates shape; Item 10 (pilot) spans High/Med/Low fit before bulk. (The standalone stability probe that would have caught this earlier was superseded; the pilot is the surviving gate.) |
| Snapshot of preserved User-Decisions misses content | Med — analyst rework lost | Item 10 documents the snapshot procedure; Item 11 follows it mechanically. |
| Dropped regex validators leave silent contract gaps | Med — bad shapes ship | New `model_setup.py` and override-registry checks in Item 7 cover the structural invariants; structured assess/review output in Item 8 covers the rest. |
| Bulk regeneration cost (LLM tokens) blows past expectations | Low — budget known | Pilot establishes per-concept cost; user is not cost-sensitive per project memory. |

---

## Timeline

**Total Effort**: ~9.5–13.5 days (Phase 0 ~1 d done, Phase 1 ~6.5–9.5 d, Phase 2 ~2.5–3.5 d)

| Item | Effort | Phase | Dependencies |
|------|--------|-------|--------------|
| Item 1: E2E manual prototype | ~1 d | 0 | — *(✅ complete)* |
| ~~Item 2: Prompt-stability probe~~ | — | 0 | ⊘ superseded — selection now human-gated |
| ~~Item 3: Critic acuity probe~~ | — | 0 | ⊘ superseded — Item 1 cleared bet #5; critic on-demand |
| Item 4: Library preconditions | 0.5–1 d | 1 | Item 1 — *(✅ complete, ~0.25 d actual)* |
| Item 5: Tables (×4) + sanity check | 1.5–2 d | 1 | Item 1 (parallel with Item 4) |
| Item 6: Pipeline glue | 1–1.5 d | 1 | Item 5 |
| Item 7: Helpers + validators | 1–1.5 d | 1 | Items 1, 4, 5 |
| Item 8: Prompt rework | 1–1.5 d | 1 | Items 1, 5, 6, 7 |
| Item 9: model_critic | 0.5–1 d | 1 | Items 1, 5 |
| Item 10: Explorer + pilot | 1.5–2 d | 2 | Items 4, 6, 7, 8, 9 |
| Item 11: Bulk regeneration | 1–1.5 d | 2 | Item 10 |
| Item 12: Native-scale projection (aspirational) | ~1–2 d per family | 3 | Item 11 |

**Phase 0 gate**: passed. Item 1's findings cleared the kill-switch bets (#3, #4, #5) and motivated the design-point-upfront change. Items 2 & 3 are superseded (see Phase 0 status note). Proceed to Phase 1.

**Phase 3 status**: aspirational. Does not block Phase 2 sign-off. Effort is per-family and scales with how many families we want to publish native-scale numbers for.

Items 4 and 5 can run in parallel; Items 7 and 9 can run in parallel after their deps; Item 8 is the pacing gate before pilot.

---

## Lessons Learned (Post-Completion)

*Fill in after epic is complete*

**What Went Well**: TBD
**What Could Improve**: TBD
**Surprises**: TBD

---

**Last Updated**: 2026-05-31
**Next Action**: Item 4 complete (2026-05-31; `1costingfe a2153ad`). Item 5 — Phases A through D complete (tables populated, design-point batch run: 31 of 36 non-`None` concepts in `design_point.csv`, 5 freeforms pending operator decision, $27.20 actual batch cost). Per-row verification gate (Phase E) and close-out (Phase F) remaining. Verification gate inputs: (1) decide each of 5 freeforms — 17b Focused Energy, 19 Zephyr orbital dipole, 27 EMC2 Polywell, 28 Energy Singularity, 39 ENN — for accept-freeform vs hand-author `low`-grounded row; (2) review 31 CSV rows for concept-identity caveats flagged in spec (notably #22 First Light pre-pivot architecture, #33 ARIES-ACT1 substituted for Chinese state programs, #06 Pale Blue operator-authored notional); (3) decide disposition of pathological-P_native rows (#13 Orbitron 5 kWe, #03 Cortex 300 kWe, #26/#30/#31 super-1GWe inverting the replication-floor framing). Surprise finding folded into Item 5's design and Item 6's routing requirements: architecture-mappability and design-point grounding are orthogonal axes; `grounding_confidence: low` rows run through costingfe with asterisks in the comparison view, distinct from architecture-bespoke freeform-deferred concepts.
