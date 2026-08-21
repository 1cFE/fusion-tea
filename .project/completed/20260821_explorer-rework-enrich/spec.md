# Spec: Explorer Rework Enrich (Ingest New Rework-Era Artifacts)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-06-05
**Complexity:** MEDIUM
**Branch:** TBD (single PR off `main`)
**Epic:** [`epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 10 (additive extension)
**Research:** [`20260605-081423_explorer-rework-dependency-gap-map.md`](../../research/20260605-081423_explorer-rework-dependency-gap-map.md)
**Depends on:** [`explorer-rework-unblock`](../explorer-rework-unblock/spec.md) landing first.

---

## Work Item Summary

The concept-analysis rework introduced a suite of new orchestrator-owned artifacts that today the explorer ignores: expanded frontmatter (`Archetype`, `Archetype-Fit`, `Comparables`, `Design-Point-*`, `Grounding-Confidence`), per-concept `design-points/baseline.yaml` (selection rationale + alternatives + primary sources), per-concept `critic_review_*.md` (model_critic findings), and four cross-concept tables under `exploration/concept_analysis/tables/` (`ontology.csv`, `archetype_fit.csv`, `comparables.csv`, `design_point.csv`). This work item extends the extractor to ingest the additive content selectively — wiring whichever sources cover semantic gaps that aren't already projected into frontmatter — and surfaces them as new optional fields on `ConceptData`. It does not change UI; UI work follows once both data-layer items have shipped.

## Why This Matters Now

`explorer-rework-unblock` restores extraction to the pre-rework feature surface. That gets the explorer running again, but it leaves a lot of post-rework richness on the floor: a Low fit-grade concept can show "Low" without explaining *why*, a comparison view can show comparables-by-ID without showing why they cluster, and the design-point selection (which plant is this concept actually modeling, and what was rejected and why) is invisible to the UI. The orchestrator already publishes this data deterministically; the cost of ingesting it now is one PR. Doing it now also locks in the data layer before any UI work is scoped — which is easier than retrofitting fields after the front-end starts depending on them.

## Key Bets / Constraints

- **Bet:** The orchestrator-owned data (tables + frontmatter + baseline.yaml + critic markdown) is the single source of truth. The explorer is a pure projection layer; it never overrides or re-derives.
- **Bet:** A small set of optional `ConceptData` fields keeps backward compatibility — old-shape concepts simply leave them null and the UI gracefully degrades.
- **Constraint:** No UI work. Adding the fields to `ConceptData` does NOT obligate any template or JS change in this PR. Frontend integration is a separate follow-up.
- **Constraint:** No LLM extraction. `critic_review_*.md` is ingested by parsing markdown structure as-is (header pattern, file modification time). Same with `baseline.yaml` (already structured).
- **Constraint:** Tables are read once at extraction time, indexed by `concept_id`, and joined onto each concept. They are not re-read on demand by the server.
- **Constraint:** `design_point.csv` is NOT consumed. Its content (`selection_rationale`, `alternatives_considered`, `primary_sources`) is already in per-concept `design-points/baseline.yaml`, which is richer and authored alongside the concept. Reading both would invite drift.
- **Non-goal:** UI updates to surface the new fields (concept page panels, asterisk styling tweaks, fit_rationale tooltips, etc.) — separate follow-up.
- **Non-goal:** Cross-table validation (e.g. "does `archetype_fit.csv` agree with frontmatter `Archetype-Fit`?"). The tables are upstream of frontmatter; if they disagree, the issue is in the orchestrator pipeline, not the explorer.
- **Non-goal:** Recomputing comparables, archetype fit, or any other orchestrator-owned decision. The explorer reads, the orchestrator decides.
- **Non-goal:** Regeneration of the 12 old-shape concepts (Item 11 of the rework epic).

---

## Business Goals

### Why This Matters

The rework's central claim — "every concept's `result_1gw` is reached by the same two-knob mechanism, so cross-concept comparison is apples-to-apples by construction" — is only half-useful without the surrounding context. Knowing concept 04 is Low-fit doesn't tell you why; the `fit_rationale` does. Knowing concept 01's comparables are 21/28/29/33 doesn't tell you why those four; the `derivation_signature` does. The critic's review of an analysis is signal that today is buried in the analyses directory. This work item brings that context into the explorer's data layer so subsequent UI work can surface it.

### Success Criteria

- [ ] `ConceptData` payload validates with the new optional fields populated where source data exists, and null/empty where it doesn't.
- [ ] All 28 rework-aligned concepts carry `archetype`, `archetype_fit`, `fit_rationale`, `design_point` (with name + maturity), `grounding_confidence`, and `comparables` with `derivation_signature` after extraction.
- [ ] All concepts that have a `critic_review_*.md` file carry a `critic_review` field referencing the latest iteration's content.
- [ ] The 12 old-shape concepts (and any future concept with sparse data) extract with the new fields set to null/empty, producing no fatal error and at most one warning per concept.
- [ ] `Grounding-Confidence: low` extends `asterisk_in_comparison = True` (currently triggered only by `Comparison-Status == costingfe-asterisked`).
- [ ] No regression in existing extractor and server tests.

### Priority

P1. Not blocking the explorer itself (that's `explorer-rework-unblock`). Blocking subsequent UI work on the comparison view and concept page that wants to surface fit rationale, design-point context, or critic findings.

---

## Problem Statement

### Current State

`ConceptData` carries only the field set that existed before the rework: `concept_id`, `name`, `confinement_family`, `company`, `status`, `illustration`, `has_cost_model`, `has_sensitivities`, `cost_model`, `parameter_metadata`, `narrative`, `sources`, `asterisk_in_comparison`. The richer orchestrator-owned context lives unread:

- **Frontmatter** (in `analysis.md`): `Archetype`, `Archetype-Fit`, `Comparables` (block list), `Design-Point-Name`, `Design-Point-Maturity`, `Grounding-Confidence`. Only `Confinement-Family`, `Comparison-Status`, `P-Native`, `Concept`, `Company`, and `Status` are read today.
- **Per-concept `design-points/baseline.yaml`**: `design_name`, `maturity_tier`, `grounding_confidence`, `p_native_mwe`, `primary_sources`, `selection_rationale`, `alternatives_considered`. Not read.
- **Per-concept `critic_review_*.md`**: model_critic findings (citation verification, override credibility, fit-grade sanity). Not read.
- **Cross-concept tables**:
  - `archetype_fit.csv`: `fit_rationale` per concept — explanation of why fit_grade is Low/Med/High. Not read.
  - `comparables.csv`: `derivation_signature` per concept — basis for the cluster (e.g. `"cluster=tokamak_family, fuel=DT, driver=magnetic-steady-state, conversion=thermal"`). Not read.
  - `ontology.csv`: `confinement_subfamily`, `driver_class`, `conversion_path`, `notes` — finer-grained taxonomy axes. Not read.
  - `design_point.csv`: redundant with `baseline.yaml`.

`asterisk_in_comparison` is set only when `Comparison-Status == "costingfe-asterisked"`. The Item 10 spec called for `Grounding-Confidence: low` to also trigger the asterisk — not yet wired.

### Desired Outcome

`ConceptData` carries a small, well-typed set of new optional fields that project the orchestrator's truth into the explorer's data layer. Each field is either present-with-content (rework-aligned concept, source data exists) or null-with-degraded-grace (old-shape concept, or freeform concept missing the relevant artifact). The frontend has everything it needs to render fit rationale, design-point context, comparables explanations, and critic findings whenever UI work picks them up.

---

## Scope

### In Scope

- **Frontmatter ingestion** in `extract_explorer_data.py`:
  - Read `Archetype`, `Archetype-Fit`, `Grounding-Confidence`, `Design-Point-Name`, `Design-Point-Maturity` from frontmatter.
  - Read `Comparables` block list (just the IDs at this stage; the rationale comes from the table join).
  - Extend `asterisk_in_comparison` to also be true when `Grounding-Confidence == "low"`.
- **Per-concept `design-points/baseline.yaml` ingestion**:
  - New `DesignPoint` Pydantic model: `name`, `maturity`, `grounding`, `p_native_mwe`, `selection_rationale`, `alternatives_considered` (list of `{design, reason_rejected, sensitivity_implication}`), `primary_sources` (list of repo-relative paths).
  - Wired onto `ConceptData.design_point` (optional).
- **Per-concept `critic_review_*.md` ingestion**:
  - New `CriticReview` Pydantic model: `iteration` (int from filename, e.g. `critic_review_iter-03.md` → 3, or 0 if unnumbered), `path` (repo-relative), `content` (raw markdown), `last_modified` (ISO string).
  - Wired onto `ConceptData.critic_review` (optional, picks the highest-iteration file when multiple exist).
- **Cross-concept table joins** at extraction time:
  - Read `exploration/concept_analysis/tables/archetype_fit.csv` once; index by `concept_id`; join `fit_rationale` onto each concept.
  - Read `exploration/concept_analysis/tables/comparables.csv` once; index by `concept_id`; join `derivation_signature` onto each concept.
  - Read `exploration/concept_analysis/tables/ontology.csv` once; index by `concept_id`; join `confinement_subfamily`, `driver_class`, `conversion_path`, `notes` onto each concept.
  - All as optional fields with sensible defaults; a concept absent from a table simply has the field null.
- **New `ConceptData` fields** (all optional):
  - `archetype: str | None`
  - `archetype_fit: str | None` (Low / Med / High / None)
  - `fit_rationale: str | None`
  - `grounding_confidence: str | None` (low / medium / high)
  - `design_point: DesignPoint | None`
  - `comparables: list[ComparableRef]` (default `[]`)
  - `critic_review: CriticReview | None`
  - `taxonomy: TaxonomyDetail | None` (subfamily, driver_class, conversion_path, notes)
- **`ComparableRef`**: `{concept_id, derivation_signature}` (one entry per comparable, derivation_signature shared across the cluster).
- **`asterisk_in_comparison`** semantics extended to OR `Grounding-Confidence: low`.
- Tests: new unit tests for table loading, frontmatter ingestion, baseline.yaml parsing, critic_review file selection. End-to-end test against concept 01.

### Out of Scope

- **Any frontend change.** Templates, JS, asterisk CSS, parameter cards, tornado chart, comparison view rendering — all untouched. Adding fields to `ConceptData` does not obligate any UI change in this PR.
- **`design_point.csv` ingestion** — per-concept `baseline.yaml` is the source.
- **LLM extraction from critic_review_*.md.** Parse the file as raw markdown; let the frontend render it.
- **Cross-table validation** (e.g. consistency between `archetype_fit.csv.fit_grade` and frontmatter `Archetype-Fit`).
- **Server-side compute changes.** This work item is extractor-only plus model definitions; the server inherits the new fields by virtue of loading the extracted JSON.
- **Regeneration of old-shape concepts** to backfill frontmatter or design-points/baseline.yaml.
- **A "what changed" diff endpoint** between iterations of `critic_review_*.md`. Latest only.

### Edge Cases & Considerations

- A concept absent from `archetype_fit.csv` (e.g. a freeform concept) has `fit_rationale=None`. Acceptable.
- Concept 39 (`spherical-tokamak-cs-free-p-b11`) is a recent addition (PR #39) — confirm it's in all four tables.
- A concept directory with `critic_review.md` (unnumbered, no `_iter-NN`) gets iteration=0. A concept with both `critic_review.md` and `critic_review_iter-03.md` picks the highest iteration.
- `Comparables` block list parser already exists (extractor uses `yaml.safe_load` on frontmatter; YAML block lists round-trip). Confirm no edge cases with single-element lists or trailing whitespace.
- `baseline.yaml` may be present without an `alternatives_considered` block (some concepts have a single forced choice). Make that field default to `[]`, not None.
- The four tables live under `exploration/concept_analysis/tables/`. If the directory is missing (clean-checkout edge case), extraction should warn and continue with the table-derived fields all null.

---

## Requirement Selection Notes

Requirements capture the data-layer additions only: which new fields exist on `ConceptData`, where they come from, how they degrade. Anything UI-visible (asterisk *rendering*, fit_rationale *display*, design-point *panel*) is intentionally left out so the UI work can be specced separately against the locked data shape. The one exception is `asterisk_in_comparison` — that field already exists; we're extending its trigger condition, which is a data-layer change with downstream visual effect, not a new field.

---

## Requirements

### Functional Requirements

1. **FR-B1**: `ConceptData` SHALL gain the optional fields: `archetype`, `archetype_fit`, `fit_rationale`, `grounding_confidence`, `design_point`, `comparables`, `critic_review`, `taxonomy`. Existing fields and field types SHALL NOT change.
2. **FR-B2**: The extractor SHALL read `Archetype`, `Archetype-Fit`, `Grounding-Confidence`, `Design-Point-Name`, `Design-Point-Maturity`, `Comparables` from `analysis.md` frontmatter when present.
3. **FR-B3**: When `concept_dir/design-points/baseline.yaml` is present, the extractor SHALL parse it into a `DesignPoint` model and assign to `ConceptData.design_point`.
4. **FR-B4**: When one or more files matching `critic_review*.md` exist in the concept directory, the extractor SHALL select the highest-iteration file (by filename) and populate `ConceptData.critic_review`.
5. **FR-B5**: At extraction startup, the extractor SHALL load `exploration/concept_analysis/tables/{archetype_fit,comparables,ontology}.csv` once and join the relevant columns onto each concept by `concept_id`. Concepts absent from a table SHALL have the corresponding fields null/empty without error.
6. **FR-B6**: `ConceptData.comparables` SHALL be a list of `ComparableRef` records carrying `{concept_id, derivation_signature}`. The IDs come from frontmatter; the signature comes from `comparables.csv`.
7. **FR-B7**: `asterisk_in_comparison` SHALL be true when either `Comparison-Status == "costingfe-asterisked"` OR `Grounding-Confidence == "low"`. (Logical OR; preserve the existing trigger.)
8. **FR-B8**: When source data is absent (no frontmatter, no baseline.yaml, no critic file, concept not in a table), the corresponding fields SHALL be null/empty and extraction SHALL succeed. At most one warning per concept may be emitted summarizing absent sources.

### Non-Functional Requirements

- Table CSV files SHOULD be loaded once per extraction run, not per concept. Per-concept lookup is dict-keyed.
- New Pydantic models SHALL be pure data — no methods that touch the filesystem or compute derived values.

---

## Acceptance Criteria

### Core Functionality

- [ ] FR-B1: ConceptData JSON schema validates with all 8 new fields present (most populated, some null) on concept 01.
- [ ] FR-B2: concept 01's extracted JSON carries `archetype="TOKAMAK"`, `archetype_fit="High"`, `grounding_confidence="high"`, `design_point.name="ARC 2015 Conservative Pilot phase (Sorbom et al.)"`.
- [ ] FR-B3: `design_point.alternatives_considered` for concept 01 has at least 3 entries (FNSF, Aggressive Pilot, SPARC, ARC 400 MWe).
- [ ] FR-B4: A concept with a `critic_review_iter-03.md` and `critic_review_iter-04.md` selects iter-04.
- [ ] FR-B5 + FR-B6: concept 01's `fit_rationale` matches `archetype_fit.csv` row; `comparables` has 4 entries, each carrying the same `derivation_signature`.
- [ ] FR-B7: A concept with `Grounding-Confidence: low` extracts with `asterisk_in_comparison=True` even if `Comparison-Status != costingfe-asterisked`.
- [ ] FR-B8: The 12 old-shape concepts extract with `archetype=None`, `design_point=None`, etc., and at most one warning each.

### Quality & Integration

- [ ] Existing test suite passes: `uv run python -m pytest exploration/concept_explorer/tests/ -v`.
- [ ] New tests cover: table loading (with missing file), baseline.yaml parsing (with and without alternatives), critic_review iteration selection, frontmatter ingestion of the 6 new fields, the OR semantics of `asterisk_in_comparison`.
- [ ] Server starts and `/api/concepts/01` returns the new fields in the payload (verifies in-memory load + serialization; no UI dependency).

---

## Next-Stage Handoff

**Settled in this spec:**
- The set of new `ConceptData` fields and their source mappings.
- `design_point.csv` is intentionally not consumed.
- `asterisk_in_comparison` semantics extended to OR `Grounding-Confidence: low`.
- No UI work, no LLM extraction, no cross-table validation.
- Latest-iteration selection rule for `critic_review_*.md`.

**Design must figure out:**
- Pydantic model naming and field naming convention for the new types (`DesignPoint`, `CriticReview`, `ComparableRef`, `TaxonomyDetail` are placeholders).
- Where the table-loading lives — top of `run_extraction`, a separate helper module, or inline inside each pathway. Recommend separate module for cleanliness.
- Whether `taxonomy` (the `ontology.csv` subfields) is its own nested model or flat optional fields on `ConceptData`.
- The single-warning rollup at FR-B8: what's the message format, what does it list, when does it suppress.
- Whether `archetype` and `archetype_fit` come exclusively from frontmatter (the orchestrator's projection) or whether to cross-check against `archetype_fit.csv` and warn on disagreement. Recommend frontmatter-only (the spec's "no cross-table validation" non-goal).

**Watch-outs for design:**
- The `Comparables` block list parser is already YAML-based; confirm it handles the edge cases (single-element list, empty list, leading/trailing whitespace) before adding the per-concept join.
- A concept's `critic_review` field carrying raw markdown can be large (~10-50 KB per file). Confirm this doesn't blow up the on-disk JSON or the in-memory server. If it does, the design should consider storing critic content out-of-band (e.g. a path reference instead of inlined content).
- `design-points/baseline.yaml` has free-form `selection_rationale` and per-alternative `sensitivity_implication` — these are multi-paragraph. Same concern as critic content; size them empirically before deciding storage strategy.
- Don't accidentally make any of the new fields *required*. Every one must default to null/empty so old-shape and freeform concepts extract cleanly.

---

## Related Artifacts

- **Epic:** [`.project/backlog/epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md) — Item 10 (this is the additive extension of Phases 3-5).
- **Research:** [`.project/research/20260605-081423_explorer-rework-dependency-gap-map.md`](../../research/20260605-081423_explorer-rework-dependency-gap-map.md) — full dependency inventory, gap matrix, and explanation of which tables fill which semantic gaps (§ Gap Matrix items 10-16).
- **Dependency:** [`.project/active/explorer-rework-unblock/spec.md`](../explorer-rework-unblock/spec.md) — must land first.
- **Prior spec (Phases 1-2):** [`.project/active/concept-rework-explorer-pilot/spec.md`](../concept-rework-explorer-pilot/spec.md).
- **Three-forward contract:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` docstring (lines 1-31).
- **Frontmatter contract:** `exploration/concept_analysis/scripts/lib/frontmatter.py:114-173`.
- **Source data:**
  - `exploration/concept_analysis/tables/archetype_fit.csv`
  - `exploration/concept_analysis/tables/comparables.csv`
  - `exploration/concept_analysis/tables/ontology.csv`
  - `exploration/concept_analysis/analyses/{id}/design-points/baseline.yaml`
  - `exploration/concept_analysis/analyses/{id}/critic_review*.md`
- **Design:** `.project/active/explorer-rework-enrich/design.md` (to be created).

**Next Steps:** After approval AND after `explorer-rework-unblock` lands, proceed to `/_my_design`.
