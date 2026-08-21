# Design: Explorer Slider Override Semantics

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-06-06
**Updated:** 2026-06-06
**Branch:** feat/concept-explorer-omit-list (work branch TBD)
**Commit at design:** 4b098c9e

## Overview

Implement option (c) from the spec: a single `apply_analyst_overrides` toggle (default on, hero block) that makes the headline, the slider recompute, and the tornado all describe the *same* LCOE function — the analyst-applied one by default, the library-bare one when toggled off — eliminating the −17.8% phantom discontinuity on first slider touch.

## Related Artifacts

- **Spec:** [`spec.md`](./spec.md) (option (c) settled; FR-SO7 inspection split to Item 2).
- **Epic:** [`../../backlog/epic_explorer_ux_v3.md`](../../backlog/epic_explorer_ux_v3.md) — EXPLORER-UX-V3, Phase 1, Item 1.
- **Research:** [`../../research/20260605-150329_concept-explorer-ux-user-journeys.md`](../../research/20260605-150329_concept-explorer-ux-user-journeys.md).
- **Successor:** Item 2 `explorer-override-inspection` (owns FR-SO7; hangs off this item's toggle/count).

## Research Findings

- **The registry and `P_native` are module-level globals.** Each costingfe `model_setup.py` exposes `model`, `overrides` (the registry list), `P_native`, and `result_1gw` at module scope (verified concept 01: `model_setup.py:33,36,56,124`). The server already imports the module in `_compute_cached` via the LRU-cached `_load_model_module` (`server.py:580`). So re-applying the registry on recompute needs **no new IO** — read `module.overrides` and `module.P_native`.
- **`enabled_overrides()` projects the registry** to the `{account: value}` dict `forward()` consumes, filtering disabled entries (`model_setup_helpers.py:75`). `run_native_and_1gw` already calls `forward(..., cost_overrides=enabled, override_reference_mw=p_native)` (`model_setup_helpers.py:147`) — the exact call shape the recompute path must mirror to reproduce `result_1gw`.
- **The compute path deliberately drops overrides today.** `_forward_with_overrides` (`server.py:143`) re-forwards from `result_1gw.params` with no `cost_overrides`; the params dict carries physics/financial scalars (incl. `net_electric_mw=1000`, `n_mod`, `availability`, `noak`) but never the registry. This is the root cause.
- **The tornado is built bare today.** `build_sensitivity_analysis` calls `model.sensitivity(result.params)` with `cost_overrides=None` (`extract_explorer_data.py:178,184`). The stored `cost_model.sensitivities` is therefore bare, while `headline` is applied — the documented mismatch.
- **Frontend data flow** (`concept_page.js`): the tornado is rendered once at init from `concept.cost_model.sensitivities` (`:462`); `cost_model.headline` is the delta baseline (`:323`); slider drag → `onSliderChange` → `POST /api/compute` → updates **sticky headline + CAS breakdown only** (`:434-448`). The tornado is *not* re-rendered on slider drag. `renderTornado` returns `{reset}` and derives its sliders/baselines from `sensitivities` at construction — there is no in-place "swap sensitivities" method (`tornado.js:12,74,206`).
- **State plumbing.** `ExplorerState` (`models.py:446`) is a single-concept snapshot (`current_concept_id`, `slider_overrides`, `comparison_set`); `/api/state` POST just echoes it back with a timestamp, nothing reads it into the UI (`server.py:406-414`). `ComputeRequest` (`models.py:456`) is `{concept_id, overrides}`. The LRU key is `(concept_id, frozenset(overrides.items()))` (`server.py:563`).
- **`overridden` signal.** `from_forward_result` reads `result["overridden"]` (a list of account codes) and sets `CASAccount.overridden` per account (`models.py:243,254,263`). Override accounts (e.g. `C220103`) are CAS22 sub-accounts. There is no enabled-override *count* in the payload today.
- **Freeform / fit-grade.** Freeform concepts have `sources.model_setup is None`; `/api/compute` already 422s for them (`server.py:607`). Concept 01 frontmatter carries `Comparison-Status: costingfe`, `P-Native: 233`, `Grounding-Confidence: high` — no explicit `Fit-Grade` field reaches the explorer, so the toggle's hide/disable decision must key off signals the explorer already has.

## Core Concept

There are two real LCOE functions for any costingfe concept — *library-bare* (the costing framework's answer for this architecture) and *analyst-applied* (bare with the override registry applied). Today the explorer shows the applied number as the headline but perturbs the bare one with sliders and explains the bare one with the tornado. The fix is to make **one flag select which function all three surfaces use**, and to make both functions cheaply available so the switch is instant.

The flag, `apply_analyst_overrides`, lives client-side on the concept page (default on) and rides every `/api/compute` call. Server-side it does one thing: when on, the recompute re-applies `enabled_overrides(module.overrides)` with `override_reference_mw=module.P_native` — exactly the call that produced `result_1gw` — so a no-op compute reproduces the stored headline (FR-SO1). The tornado needs no server round-trip to switch: the extractor precomputes **both** sensitivities into the payload, and the frontend picks the matching one. A toggle is therefore: one compute call (new headline + CAS) plus a client-side tornado re-render, applied together so no surface is briefly out of sync.

The key insight: the registry is already a module-level global the server has loaded, and the second sensitivity is a single extra `model.sensitivity(cost_overrides=...)` call. So "expose both functions" costs one re-applied forward and one precomputed sensitivity — not a new data model or a second model load.

## Key Bets & Decisions

**Bet 1 — Re-apply the registry from the live module, not from stored JSON.** `_compute_cached` already holds `module`; reading `module.overrides`/`module.P_native` is free and always in sync with the source of truth. *Not chosen:* serializing the registry values into the payload and re-applying from there — redundant with Item 2's narrative emission and adds a staleness surface. (Item 2 emits the registry *records* for **display**; that is a different read and does not feed recompute.)

**Bet 2 — Tornado swaps client-side from two precomputed sensitivities; headline/CAS come from `/api/compute`.** The tornado has no live dependency on a server round-trip, so toggling is instant for the bars; the headline and CAS (which depend on the re-applied forward) come from one compute call. *Not chosen:* storing a `headline_bare` to avoid the compute call — the compute call is already cached and sub-200 ms, and storing a parallel headline invites the two from drifting.

**Bet 3 — `sensitivities` holds *applied*; add `sensitivities_bare`.** The default-displayed and cross-concept-indexed sensitivity becomes the applied one (consistent with the headline). Adding `sensitivities_bare` as the alternate means existing readers (`models.py` validator `:371`, parameter-index build `:547`, `tornado.js:462`) keep working and silently become applied-based — which is the *correct* default. *Not chosen:* renaming `sensitivities`→`sensitivities_applied` everywhere (churn across readers for no behavioral gain) or deriving bare from applied (forbidden — `_scale_overrides` keeps a rescaled shape; spec watch-out).

**Bet 4 — Emit a lightweight `analyst_override_count`; defer records to Item 2.** The toggle label ("Apply analyst cost adjustments (N entries)") and the hide/disable decision need only the *count* of enabled overrides. Item 1 emits `analyst_override_count: int`; Item 2 adds the full `overrides: list[OverrideRecord]` and the count remains a cheap scalar (or becomes `len(...)`). This keeps Item 1 free of Item 2's schema work. *Not chosen:* counting `overridden` CAS flags client-side — hacky and conflates accounts with registry entries.

**Bet 5 — Toggle is client-side per-page state; `ExplorerState` carries the echo.** The concept page is single-concept, so per-concept-ness is automatic — each page owns its toggle, default on, sent on every compute. `ComputeRequest` gains the flag (load-bearing); `ExplorerState` gains it (FR-SO5 literal + the `/api/state` echo). No per-concept dict needed. *Open collision check (research Q):* future cross-page selection state is session-global; this toggle is page-local, so they do not collide.

**Decision A — On toggle, sliders return to baseline.** Toggling is treated as a mode switch: it re-renders the tornado with the new mode's elasticities (sliders at baseline) and shows that mode's baseline headline/CAS. Param baselines are identical across modes (only `cost_overrides` differ, not physics params), so nothing physical is lost. *Alternative (preserve drag positions across toggle):* requires `renderTornado` to accept injected current positions — more surface, deferred. Flagged for user confirmation.

## Architecture

Data flows in two phases — extract-time (precompute both functions' static parts) and compute-time (re-forward the selected function on demand):

```
EXTRACT (extract_explorer_data.py)
  enabled = enabled_overrides(module.overrides)
  sensitivities_applied = build_sensitivity_analysis(model, result, cost_overrides=enabled)   # NEW default
  sensitivities_bare    = build_sensitivity_analysis(model, result, cost_overrides=None)       # NEW alternate
  ConceptData.cost_model.sensitivities       = applied
  ConceptData.cost_model.sensitivities_bare  = bare
  ConceptData.analyst_override_count         = len(enabled)

COMPUTE (server.py /api/compute, per slider drag OR toggle)
  ComputeRequest{concept_id, overrides, apply_analyst_overrides}
  → _compute_cached(concept_id, frozenset(overrides), apply_analyst_overrides)   # LRU key extended
      module = _load_model_module(...)                # already cached
      if apply_analyst_overrides:
          cost_overrides = enabled_overrides(module.overrides); ref = module.P_native
      else:
          cost_overrides = None; ref = None
      _forward_with_overrides(model, result_1gw.params, overrides,
                              cost_overrides=cost_overrides, override_reference_mw=ref)

FRONTEND (concept_page.js)
  toggle.onChange → onSliderChange(currentOverrides) with apply flag
                  → in the compute response handler, together:
                       updateStickyHeadline + renderCASBreakdown + re-renderTornado(selectedSensitivities)
```

Integration points: the toggle control mounts in the hero block (`concept.html.j2` hero + `concept_page.js:renderHero`); the compute fetch (`concept_page.js:434`) gains the flag in its body; the tornado re-render reuses the existing `renderTornado` entry point with the toggle-selected sensitivity set.

## Required Invariants

- **INV-1 (FR-SO1):** `compute(concept_id, overrides={}, apply=True)` ≡ stored `cost_model.headline` within float tolerance. Guaranteed because the re-applied forward mirrors `run_native_and_1gw`'s call (`cost_overrides=enabled`, `override_reference_mw=P_native`, from `result_1gw.params`).
- **INV-2 (FR-SO2):** at any instant, the headline, the slider recompute, and the displayed tornado are sourced from the same `apply_analyst_overrides` value — never mixed.
- **INV-3:** `sensitivities` (applied) and `sensitivities_bare` are computed by independent `model.sensitivity(cost_overrides=...)` calls; neither is derived from the other.
- **INV-4 (FR-SO5):** the LRU cache key includes `apply_analyst_overrides`; identical (concept, overrides, flag) triples hit cache.
- **INV-5 (FR-SO6):** the toggle renders only when `sources.model_setup != null` **and** `analyst_override_count > 0`; disabled when model_setup present but count 0; absent for freeform.
- **INV-6:** for an empty registry, `sensitivities == sensitivities_bare` and the applied forward equals the bare forward (no behavior change).

## Component Overview

- **`extract_explorer_data.py`** — `build_sensitivity_analysis` gains a `cost_overrides` arg; `extract_costingfe` computes applied + bare, sets `analyst_override_count`. (Functions at `:178`, `:288`.)
- **`models.py`** — `CostModelData` gains `sensitivities_bare: SensitivityAnalysis | None`; `ConceptData` gains `analyst_override_count: int = 0`; `ComputeRequest` and `ExplorerState` gain `apply_analyst_overrides: bool = True`.
- **`server.py`** — `_forward_with_overrides` gains `cost_overrides`/`override_reference_mw` kwargs; `_compute_cached` and `compute` thread the flag; LRU key extended.
- **`concept.html.j2` + `concept_page.js`** — hero-block toggle (checkbox + label with inert `(N entries)` + subtitle), wired to re-issue compute and re-render headline/CAS/tornado atomically; hidden/disabled per INV-5.
- **`explorer.css`** — toggle + count-chip styling (low-emphasis, label-not-button).
- **Test** — FR-SO1 regression (concept 01) + FR-SO2 sweep sign check.

## Non-Goals

- The override-inspection panel, multi-site ★ triggers, and disabled-override display (Item 2).
- Per-account `generic`/`native`/`result_1gw` delta decomposition (future phase).
- Preserving slider drag positions across a toggle (Decision A; deferred).
- Any change to `model.sensitivity()` or `run_native_and_1gw`.
- The 12 old-shape concepts.

## Implementation Notes

- **Reproduce `result_1gw` exactly.** `_forward_with_overrides` already pulls `net_electric_mw`, `n_mod`, `availability`, `lifetime_yr`, `noak` from `base_params` (`server.py:156-166`). Adding `cost_overrides=enabled` + `override_reference_mw=P_native` must reproduce `result_1gw` when `overrides={}`. Verify the FR-SO1 tolerance against the live module, not a hardcoded 155.17.
- **`override_reference_mw` only bites when `n_mod ≠ 1`.** Concept 01 has `n_mod=round(1000/233)=4`. Pass `P_native` (233), not `None`, in the applied branch. Confirm the library `forward` signature accepts both kwargs (it does — `run_native_and_1gw` uses them).
- **`_FORWARD_NAMED`/`_FORWARD_SKIP`:** `cost_overrides` and `override_reference_mw` are passed explicitly, so ensure they never leak into the `**extra` kwargs (they aren't in `result_1gw.params`, so `extra` already excludes them — confirm).
- **Atomicity (INV-2):** do the three DOM updates (headline, CAS, tornado) inside the single compute-response handler, after the await resolves — never update the tornado optimistically before the headline returns.
- **`analyst_override_count`** = `len(enabled_overrides(module.overrides))` at extract time (enabled only — disabled entries don't move the LCOE and shouldn't inflate the label).
- **Parameter-index semantics shift:** because `sensitivities` becomes applied, `/api/parameter_index` (`server.py`/`models.py:547`) now indexes applied elasticities. This is intended (consistent with the headline) but is an observable change — note in the README addition.

## Potential Risks

| Risk | Mitigation |
|------|-----------|
| Re-applied forward doesn't reproduce `result_1gw` (param drift) | FR-SO1 regression test against the live module; assert tolerance, not a literal. |
| `sensitivities_applied` accidentally derived from bare | INV-3: two explicit `model.sensitivity` calls; code-review check. |
| Existing readers break on repurposed `sensitivities` | Field stays same name/type; only the *value* (applied vs bare) changes. Run full suite. |
| Toggle reads as broken before Item 2 makes count clickable | Style count as low-emphasis label, not a button (spec UX req). |
| Empty-registry concept renders an active no-op toggle | INV-5 / FR-SO6 disable rule; test a count-0 costingfe concept. |

## Integration Strategy

Additive to the existing concept page: the toggle is a new hero control; the compute contract gains one optional field (`apply_analyst_overrides`, default `True`, so old callers/tests are unaffected). The tornado, headline, and CAS rendering paths are reused — only their data source becomes flag-selected. No change to taxonomy, compare, or landing pages.

## Validation Approach

- **FR-SO1 regression** (new test): for concept 01, `compute(overrides={}, apply=True).headline.lcoe_per_mwh ≈ cost_model.headline.lcoe_per_mwh`; and `apply=False` differs by the registry magnitude (~−17.8%).
- **FR-SO4 test:** concept 01 payload has both `sensitivities` and `sensitivities_bare`, differing on ≥1 param.
- **FR-SO2 manual/scripted:** sweep `availability` 0.7→0.95; LCOE monotone; slope sign matches tornado elasticity sign in each toggle state.
- **FR-SO5 manual (browser-inspect):** toggle with sliders untouched → headline + CAS + tornado swap together; no partial frame; console clean.
- **FR-SO6 manual:** a freeform concept shows no toggle; an empty-registry costingfe concept (if any) shows it disabled with hover text.
- **Regression:** full `pytest` suite green; concept 01/17a/24 pages smoke-tested via the browser-inspect skill.

## Next-Stage Handoff

**Fixed:** option (c); hero placement; re-apply-from-module (Bet 1); two-precomputed-sensitivities + client-side swap (Bet 2); `sensitivities`=applied + `sensitivities_bare` (Bet 3); `analyst_override_count` (Bet 4); flag on `ComputeRequest`/`ExplorerState` + LRU key (Bet 5).

**Open (user confirmation before plan):**
- **Decision A** — toggle resets sliders to baseline (recommended) vs preserves drag positions (more work, deferred).
- **Bet 3 naming** — repurpose `sensitivities` to applied (recommended) vs introduce `sensitivities_applied` and deprecate `sensitivities`. Confirm the parameter-index semantics shift to applied is acceptable.

**De-risk first in the plan:** the FR-SO1 reproduction (re-applied forward ≡ `result_1gw`) — it's the load-bearing correctness claim; build and run that regression test before wiring any UI.

---
Next Step: After approval → `/_my_plan` (or `/_my_implement` for a small, well-bounded plan).
