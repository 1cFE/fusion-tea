---
date: 2026-06-05T08:14:23-07:00
researcher: Claude
topic: "Concept-explorer extraction/server dependency map vs concept-analysis rework"
tags: [research, concept-explorer, concept-analysis-rework, extraction]
status: complete
last_updated: 2026-06-05
---

# Research: Concept-Explorer ↔ Concept-Analysis Rework Dependency Gap Map

**Date**: 2026-06-05
**Researcher**: Claude
**Research Type**: Integration / Interface audit

## Research Question

After the `concept-analysis-rework` epic (PR #44) and subsequent fixes (PR #39, #46), running `uv run python exploration/concept_explorer/extract_explorer_data.py` fails immediately on concept 01 with:

> `ERROR: 01: model_setup.py must define module-level 'model' and 'result'`

We need a complete inventory of every file, module-level name, frontmatter field, and on-disk artifact the **extractor** (`extract_explorer_data.py`) and the **server** (`server.py`, `/api/compute`) read — and for each, classify what the rework changed. This research is the input to a fix spec; **no fix is proposed here**.

## Summary

- **Immediate breakage**: both `extract_costingfe()` (`extract_explorer_data.py:301-306`) and `_compute_cached()` (`server.py:553-555`) require a module-level `result` object that the three-forward contract has deliberately removed. New-shape `model_setup.py` only exposes `model`, `generic`, `native`, `result_1gw`.
- **Item 10 was Phases 1-2 only.** The extractor already gained `result_1gw` awareness, `verify_two_knob()`, `Comparison-Status` routing, and the `pending-design-point` skip path. What was *deferred* (Phases 3-5) is exactly the `result`-removal cleanup, the `compute()`-endpoint adaptation, and the ingestion of the new orchestrator-owned frontmatter fields (`Archetype`, `Archetype-Fit`, `Grounding-Confidence`, design-point block).
- **`result.params` is load-bearing in two places** the extractor (sensitivity baselines via `build_sensitivity_analysis(model, effective_result)` — currently passes `result_1gw`, which is fine) and the server's compute endpoint (`model.forward(**result.params, **overrides)` — currently broken). Choosing the right `params` source under the new contract is a design decision, not a mechanical swap: `result_1gw.params` carries `n_mod = round(1000/P_native)` and `override_reference_mw=P_native`, which changes slider semantics.
- **12 "old shape" concepts** (04-12, 13, 18, 20a) have `review.md` instead of `analysis.md`. Their `model_setup.py` is already three-forward (PR #39 refreshed all 38), so frontmatter is the only thing missing. Extractor's `discover_concepts` will still find them (via `model_setup.py`), but every frontmatter field comes back empty.
- **Rich new artifacts are unconsumed**: `design-points/baseline.yaml` (design-point selection rationale + alternatives), `critic_review_*.md` (model_critic findings), and the four upstream tables under `exploration/concept_analysis/tables/` (`ontology`, `archetype_fit`, `comparables`, `design_point`). None of these flow into the explorer JSON today.

---

## Detailed Findings

### 1. `extract_explorer_data.py` — what it reads/imports/parses

#### 1a. From the analyses directory (per-concept)

| Dependency | Location | Status | Note |
|---|---|---|---|
| `concept_dir / "model_setup.py"` | line 299 | **CHANGED** | Imported via `load_module_from_path` with stdout suppressed (helper's `print_cas_breakdown` runs at import time). |
| Module-level `model` | line 301 | NO_CHANGE | Still defined by every concept (`model = CostModel(...)`). |
| Module-level `result` | line 302 | **REMOVED by rework** | Three-forward contract drops `result` entirely. Concept 01 / 04 / 15 / 17a etc. now have only `generic`, `native`, `result_1gw`. **This is the immediate breakage.** Documented in `epic_concept_analysis_rework.md` success-criteria #4 and `model_setup_helpers.py:1-31` docstring. |
| Module-level `result_1gw` | line 308 | **NEW** | Already required when present. `verify_two_knob()` (line 104) asserts `params["net_electric_mw"] == 1000` and `params["n_mod"] == round(1000/P_native)`. |
| `model.sensitivity(result.params)` | line 178 (via `build_sensitivity_analysis`) | CHANGED | Currently called with `effective_result = result_1gw` (line 324). `result_1gw.params` carries the projection's n_mod & override_reference_mw — needs verification that sensitivity baselines are interpreted correctly downstream. |
| `dataclasses.asdict(effective_result)` | line 336 | NO_CHANGE | `ForwardResult` shape (`costs` / `power_table` / `cas22_detail` / `overridden` / `params`) appears unchanged. The library's `total_capital`, `lcoe`, `overnight_cost` keys still flow. |
| `concept_dir / "analysis.md"` | line 875 | CHANGED (partial) | The 12 still-old-shape concepts have `review.md` instead. Extractor reads only `analysis.md`; for those concepts `frontmatter == {}` and Status defaults to in-progress, name defaults to dir name. |
| `concept_dir / "model_metadata.yaml"` | line 673 | NO_CHANGE in schema. Per-concept yaml schema unchanged. None currently exist in the repo (audit note in 20260227 research). |
| `concept_dir / "model_output.txt"` | line 791 (in `extract_narrative`) | NO_CHANGE | Now consistently emitted by `print_cas_breakdown` (helper-owned format) but the consumer just reads it as text. |

#### 1b. From the frontmatter (when `analysis.md` exists)

The orchestrator now writes a much richer frontmatter (see `scripts/lib/frontmatter.py:make_frontmatter` and 01's analysis.md):

```
ID, Concept, Company, Status, Created, Approved-Date,
Confinement-Family, Archetype, Archetype-Fit, Comparison-Status,
Comparables (block list),
Design-Point-Name, Design-Point-Maturity, P-Native, Grounding-Confidence,
Review-Iterations, Last-Review, Review-Status
```

Extractor's current reads (`extract_costingfe` lines 346-349, `extract_standalone` lines 635-638, dispatcher lines 880-918):

| Field | Read by | Status |
|---|---|---|
| `Concept` | `name` (line 346, 635) | NO_CHANGE |
| `Company` | `company` (line 347, 636) | NO_CHANGE |
| `Status` | `parse_status` (line 145) | NO_CHANGE |
| `Confinement-Family` | `_to_confinement_family` (line 349, 638) | NO_CHANGE (already moved from body-prose to frontmatter — old audit at `.project/research/20260405-concept-explorer-data-model-audit.md` flagged this; the regex is gone). |
| `Comparison-Status` | line 880; routing checks at 904-918 | **NEW**, already wired. Handles `costingfe`, `costingfe-asterisked`, `freeform-deferred`, `pending-design-point`. |
| `P-Native` | line 320 in `extract_costingfe` | **NEW**, already wired. Used by `verify_two_knob`. |
| `Archetype` | — | **NEW / UNCONSUMED** |
| `Archetype-Fit` | — | **NEW / UNCONSUMED** (relevant to asterisk semantics — Item 10 spec wanted low-grounding asterisk; fit_grade=None already asterisked via routing) |
| `Comparables` | — | **NEW / UNCONSUMED** (curated comparison set; explorer comparison view is freeform today) |
| `Design-Point-Name`, `Design-Point-Maturity` | — | **NEW / UNCONSUMED** |
| `Grounding-Confidence` | — | **NEW / UNCONSUMED**. Item 10 spec's explicit success criterion: low-grounding rows should asterisk. Not implemented. |
| `Review-Iterations`, `Last-Review`, `Review-Status` | — | NEW / UNCONSUMED (probably not explorer-relevant) |

#### 1c. From outside the per-concept directory

| Dependency | Location | Status |
|---|---|---|
| `exploration/concept_explorer/data/parameter_display_registry.yaml` | line 33, loaded once at module-import via `_DISPLAY_REGISTRY` | NO_CHANGE |
| `costingfe.CostModel`, `ConfinementConcept`, `Fuel` | indirect (via concept `model_setup.py`) | NO_CHANGE in import surface; per Item 4 the library accepts non-integer `n_mod` and exposes `override_reference_mw`. |
| `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` | indirect (every concept's `model_setup.py` imports it) | **NEW**. Provides `generic_reference`, `run_native_and_1gw`, `print_cas_breakdown`. The helper is on `sys.path` only because each concept's `model_setup.py` walks up to find `scripts/` (lines 12-17 of every regenerated file). Extractor never references the helper directly, but its presence shapes everything imported. |
| **Four upstream tables** under `exploration/concept_analysis/tables/` — `ontology.csv`, `archetype_fit.csv`, `comparables.csv`, `design_point.csv` | — | **NEW / UNCONSUMED** by extractor. These are read by the analyzer/orchestrator. They are the canonical source for `Archetype-Fit`, `P-Native`, `Comparables`, `Grounding-Confidence`. Explorer currently has no path to them. |

#### 1d. Per-concept new artifacts (not yet consumed)

| Artifact | Present in | Content | Status |
|---|---|---|---|
| `design-points/baseline.yaml` | All rework-aligned concepts (01, 04-39 except freeform) | `design_name`, `maturity_tier`, `p_native_mwe`, `grounding_confidence`, `primary_sources` (citation paths), `selection_rationale` (multi-paragraph), `alternatives_considered` (other design points + sensitivity implications) | **NEW / UNCONSUMED** — would be valuable on the concept page. |
| `design-points/baseline.md` | Same | Markdown render of the yaml | **NEW / UNCONSUMED** |
| `critic_review_*.md` | 21 concepts (PR #44/#46), `iter-N` versions for some | model_critic findings against the analysis — assessment of override credibility, citation verification, fit-grade sanity | **NEW / UNCONSUMED** |
| `iter-N/` sub-dirs | Most concepts | Intermediate analyzer iterations; final versions are at concept root | **NEW shape, UNCONSUMED**. Extractor only looks at concept root. |

### 2. `server.py` — what it reads at runtime

#### 2a. At startup (`lifespan` → `_load_data`)

| Dependency | Location | Status |
|---|---|---|
| `data/*.json` (concept files, excluding `manifest.json`, `parameter_index.json`, `concept_registry.json`, `decision_tree.json`) | `server.py:219-237` | NO_CHANGE in structure; produced by extractor. |
| `data/concept_registry.json`, `data/decision_tree.json` | `server.py:261-284` (taxonomy, optional) | NO_CHANGE. Both produced by separate scripts (`seed_registry.py`). |
| `templates/*.j2`, `dist/` | `_render_templates`, line 292 | NO_CHANGE. |

#### 2b. At compute time (`/api/compute` → `_compute_cached`)

| Dependency | Location | Status |
|---|---|---|
| `concept.sources.model_setup` (path to concept's `model_setup.py`) | line 545 | NO_CHANGE — path still meaningful. |
| `_load_model_module(path)` (re-imports model_setup.py with stdout suppressed) | line 549 | NO_CHANGE in mechanism. The module's import-time `print_cas_breakdown` cost is paid on first compute per concept; LRU-cached after. |
| Module-level `model` | line 550 | NO_CHANGE. |
| Module-level `result` | line 553-555 | **REMOVED by rework** — same breakage as extractor. The `compute()` endpoint is fully broken on all rework-aligned concepts, not just the extractor. |
| `result.params` as `base_params` for `_forward_with_overrides` | line 557 | **CHANGED**. Under the new contract, candidates are `result_1gw.params` (carries n_mod=round(1000/P_native), override_reference_mw=P_native) or `native.params` (n_mod=1, override_reference_mw=P_native). Both differ from the pre-rework `result.params` semantics. The choice has user-visible consequences: a slider that moves `net_electric_mw` from 1000 → 500 must decide whether to keep `n_mod` constant (number of modules fixed) or rescale it (1 GWe scaled down) — that decision used to be ambiguous because there was no two-knob mechanism. |
| `_FORWARD_NAMED` (derived from `CostModel.forward` signature via introspection) | `server.py:77-107` | NO_CHANGE in mechanism. New `forward()` parameters from Item 4 (`override_reference_mw`, expanded `cost_overrides`) are automatically picked up via `inspect.signature`. Fallback hardcoded set (line 96-107) might be stale — needs a look. |
| `_FORWARD_SKIP = {"fuel", "concept"}` | line 113 | Verify still correct under new forward(). Probably NO_CHANGE — these remain model-instance properties. |
| `_forward_with_overrides` (`server.py:141-165`) | line 141 | **CHANGED** — the function constructs the new `forward()` call with `noak=True`, `n_mod=int(...)`, etc. Under the rework, `n_mod` is sometimes non-integer (the two-knob mechanism uses fractional `n_mod` internally; the helper rounds for `result_1gw.params`). Line 159's `int(float(params.get("n_mod", 1)))` is a possible mismatch — Item 4 explicitly made the library accept non-integer `n_mod`. |
| `concept.cost_model.sensitivities` (baseline, preserved from extract-time JSON) | line 566 | NO_CHANGE in mechanism. |

### 3. Data shapes (`models.py`)

| Type | Field source | Status |
|---|---|---|
| `ConceptData` | Constructed by `extract_costingfe`/`extract_standalone` | Field set unchanged by rework. New frontmatter fields don't yet map to ConceptData fields. **Candidate additions** (not yet present): `archetype`, `archetype_fit`, `grounding_confidence`, `design_point` (name/maturity/sources), `comparables` (curated list), `critic_findings` (parsed from critic_review_*.md). |
| `ConceptData.asterisk_in_comparison` | Set from `Comparison-Status == "costingfe-asterisked"` | NO_CHANGE in name; semantics need extension to also include `Grounding-Confidence: low` per Item 10 spec. |
| `CostModelData.from_forward_result` | `dataclasses.asdict(ForwardResult)` shape (`costs.cas10..cas90 + lcoe + overnight_cost + total_capital`, `power_table.{p_net,q_eng,capacity_factor,availability}`, `cas22_detail.{C220101..C220700}`, `overridden`, `params`) | NO_CHANGE in expected shape (verified against helper-generated `print_cas_breakdown` and library docstrings). |
| `SensitivityAnalysis.engineering` / `.financial` | `model.sensitivity()` return dict | NO_CHANGE in mechanism. Under the new two-knob baseline the elasticities are computed at `(net=1000, n_mod=round(1000/P_native), override_reference_mw=P_native)` — analytically meaningful but **different** from the pre-rework baseline. Tornado interpretation changes accordingly. |
| `ParameterMetadata` (per-concept yaml schema) | NO_CHANGE — none of the rework-regenerated concepts produce a `model_metadata.yaml`. |
| `NarrativeData` | LLM extraction from analysis.md text | NO_CHANGE in schema; rework doesn't touch this. |
| `ConceptManifest` / `ParameterIndex` | Built in-memory from concept JSONs at server start | NO_CHANGE in shape. |

### 4. Old-shape (`review.md`) concepts

Twelve concepts still carry `review.md` instead of `analysis.md`: **04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 18, 20a**. PR #39 already moved them onto the three-forward `model_setup.py` shape, so the cost-model side is uniform. What they lack is the rework-era `analysis.md` frontmatter — Comparison-Status, P-Native, Archetype, Confinement-Family, etc. all come back empty.

Effect on extractor today:
- `discover_concepts` discovers them (via `model_setup.py`).
- `frontmatter = {}` → `Confinement-Family` → NONSTANDARD; `name` → directory name; `Status` → in_progress; `Comparison-Status` → empty.
- Routing check at line 904 is gated on `Comparison-Status in {"costingfe", "costingfe-asterisked"}`, so the empty-status case falls through to "import-based detection" (text-grep for `CostModel` + `from costingfe`). Those concepts will be classified `is_costingfe = True`.
- `extract_costingfe` then requires `result_1gw` (line 308). Their model_setup.py exposes `result_1gw` (PR #39 shape) — so they'd pass *that* check.
- But the next check (line 301-306) requires `result`. Same failure as for fully-rework-aligned concepts.
- `verify_two_knob` is skipped (line 321: `if p_native is not None`).

Net: the old-shape vs new-shape distinction is mostly orthogonal to the extractor breakage. The breakage is uniform across all 40 concepts.

### 5. Pre-existing related research (do not redo)

- `.project/research/20260227-074139_extraction-pipeline-redesign-integration.md` — older integration design.
- `.project/research/20260405-concept-explorer-data-model-audit.md` — data-model audit (predates rework but useful for the Pydantic model surface).
- `.project/research/20260406-model-setup-extraction-interface-gap.md` — diagnoses the original "`model` / `result` not always present" mismatch between LLM-authored `model_setup.py` and the extractor. The rework **superseded** this — the helper enforces the contract — but the extractor wasn't updated to match.

## Code References

- `exploration/concept_explorer/extract_explorer_data.py:301-306` — the line that breaks extraction. Requires `result`.
- `exploration/concept_explorer/extract_explorer_data.py:308-315` — already requires `result_1gw` (Item 10 Phase 1-2 work).
- `exploration/concept_explorer/extract_explorer_data.py:320-322` — `verify_two_knob` gated on `P-Native` frontmatter presence (Item 10 work).
- `exploration/concept_explorer/extract_explorer_data.py:880-918` — `Comparison-Status` routing and four-state handling (Item 10 work).
- `exploration/concept_explorer/server.py:553-555` — second occurrence of the `result` requirement; `/api/compute` is also broken.
- `exploration/concept_explorer/server.py:141-165` — `_forward_with_overrides`; needs review for non-integer `n_mod` and `override_reference_mw`.
- `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:1-31` — three-forward contract docstring (canonical reference).
- `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:115-178` — `run_native_and_1gw`, defines the `native` / `result_1gw` shape and the `n_mod = max(1, int(round(_PROJECTION_NET_MWE / p_native)))` clamp.
- `exploration/concept_analysis/scripts/lib/frontmatter.py:114-173` — `make_frontmatter`, defines the full frontmatter key set under the rework.
- `exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_setup.py:36-128` — canonical new-shape model_setup.py.
- `exploration/concept_analysis/analyses/01-hts-compact-tokamak/analysis.md:1-22` — canonical new-shape frontmatter.
- `exploration/concept_analysis/analyses/01-hts-compact-tokamak/design-points/baseline.yaml` — new unconsumed artifact (full content per concept).
- `.project/active/concept-rework-explorer-pilot/spec.md` — Item 10 spec; section "Current State" and "Success Criteria" explicitly list what should change in the explorer.
- `.project/backlog/epic_concept_analysis_rework.md` — Items 10, 11 status; Item 10 noted as "Phases 1-2 complete, Phases 3-5 deferred".

## Gap Matrix (consolidated)

| # | Dependency | Site | Status | Note |
|---:|---|---|---|---|
| 1 | Module-level `result` | extractor, server compute | **REMOVED** | Hard breakage on both. Three-forward contract dropped it. |
| 2 | Module-level `result_1gw` | extractor | **NEW (already wired)** | Item 10 Phase 1-2. |
| 3 | Module-level `result_1gw` | server compute | **NEW (NOT wired)** | Server still reads `result`. |
| 4 | `effective_result` selection | extractor | CHANGED | Currently `result_1gw`. Verify sensitivity baseline interpretation. |
| 5 | `base_params` for slider recompute | server compute | **CHANGED (unwired)** | Decide between `result_1gw.params` and `native.params`; reconsider slider semantics. |
| 6 | `n_mod` integer cast in forward call | server `_forward_with_overrides:159` | CHANGED | Library accepts non-integer `n_mod` post Item 4. Cast may quantize the slider. |
| 7 | `override_reference_mw` in forward call | server `_forward_with_overrides` | **NEW** | Not passed today. Required for overrides to scale correctly through the two-knob mechanism. |
| 8 | `Comparison-Status` routing | extractor dispatcher | **NEW (wired)** | Four states handled. |
| 9 | `P-Native` frontmatter | extractor | **NEW (wired)** | Used for `verify_two_knob`. |
| 10 | `Archetype` / `Archetype-Fit` | — | **NEW / UNCONSUMED** | Could inform asterisk + comparison filter. |
| 11 | `Grounding-Confidence` | — | **NEW / UNCONSUMED** | Item 10 spec wanted low-grounding asterisk; not implemented. |
| 12 | `Comparables` (block list) | — | **NEW / UNCONSUMED** | Could replace freeform comparison choices. |
| 13 | `Design-Point-Name`, `Design-Point-Maturity` | — | **NEW / UNCONSUMED** | Headline context for concept page. |
| 14 | `design-points/baseline.yaml` | — | **NEW / UNCONSUMED** | Rich selection rationale + alternatives + sources. |
| 15 | `critic_review_*.md` | — | **NEW / UNCONSUMED** | Could power a "critic findings" panel. |
| 16 | Upstream tables (`tables/*.csv`) | — | **NEW / UNCONSUMED** | Canonical source for archetype/fit/comparables/design-point. Not on the explorer's data path today. |
| 17 | `review.md` (old shape) | 12 concepts | UNCHANGED requirement | Extractor only reads `analysis.md`. Those 12 concepts have empty frontmatter today; orthogonal to the immediate `result` breakage. |
| 18 | `iter-N/` directories | — | **NEW / UNCONSUMED** | Out of scope for the explorer per Item 10. |
| 19 | `print_cas_breakdown` import-time stdout | extractor + server (both already use `redirect_stdout`) | NO_CHANGE | Confirmed safe. |
| 20 | `_FORWARD_NAMED` introspection on `CostModel.forward` | server | NO_CHANGE in mechanism | New args (e.g. `override_reference_mw`) are auto-picked. Fallback hardcoded set may be stale. |

## Open Questions (for the fix spec)

1. **What is the cost-model surface the explorer reads?** Two clean choices:
   - "Native" view (`native.params`, `native.costs`) — the concept's actual modeled plant at its native scale.
   - "1 GWe NOAK" view (`result_1gw.params`, `result_1gw.costs`) — the cross-concept comparison number.
   - The extractor currently uses `result_1gw` (line 324). Document this explicitly and make the server's compute path match.
2. **Slider semantics under the two-knob mechanism.** If the explorer's headline is `result_1gw`, what does dragging `net_electric_mw` from 1000 → 700 mean? Re-scale `n_mod` to keep modules-at-design-point fixed? Or keep `n_mod` fixed and accept a de-rated plant? The Item 10 spec doesn't fully answer this.
3. **Should we surface both `generic`, `native`, `result_1gw` in the ConceptData payload** (so the UI can show "override effect" and "replication effect" separately, as `print_cas_breakdown` does), or just one?
4. **Old-shape `review.md` concepts**: ingest with empty frontmatter (today's behavior), or fail-loud and require they be regenerated through the bulk pipeline first?
5. **Are the upstream tables (`tables/*.csv`) on the explorer's data path** going forward, or do we keep reading everything from per-concept frontmatter (which is already a deterministic projection of those tables)?

## Recommendations (for the next step, not this one)

This research suggests the fix spec is best scoped as **two work items** rather than one:

- **A (minimal, unblocks extraction):** Land Item 10 Phases 3-5 strictly. Drop `result` requirement in extractor + server; switch server compute path to `result_1gw.params` (or `native.params`); fix `n_mod` integer cast; pass `override_reference_mw`. Single-PR, behavior-preserving for already-extractable concepts.
- **B (additive, optional):** Ingest new artifacts — design-point block, grounding-confidence asterisk, critic findings, curated comparables. Each adds a ConceptData field and a small UI panel. Independent of A.

Recommend doing A first as the immediate unblock, then sequencing B items as separate work.

## Out of Scope

- Actually fixing the bug.
- Re-spec'ing slider semantics.
- The 12 review.md → analysis.md migration (separate from this).
- Item 11 bulk regeneration of those 12.
