# Spec: Explorer Slider Override Semantics

**Status:** Implementation Complete (all 3 phases — backend compute-path, dual-sensitivity data layer, hero toggle UI — implemented, tested, and browser-validated 2026-06-06)
**Owner:** Reid W
**Created:** 2026-06-05
**Updated:** 2026-06-06
**Complexity:** MEDIUM
**Branch:** TBD
**Epic:** EXPLORER-UX-V3 (Phase 1, Item 1) — `.project/backlog/epic_explorer_ux_v3.md`
**Depends on:** [`explorer-rework-unblock`](../explorer-rework-unblock/spec.md) (landed).

---

## Work Item Summary

When a user drags any slider in the concept explorer, the recomputed LCOE drops the analyst's `cost_overrides` registry, so the displayed number jumps from the analyst-set figure (the JSON's headline) to the library-bare figure — with no input from the user. Under the pre-rework analysis pipeline this was a small effect; under the rework it is a structural one because the override registry is now where analyst judgment lives. This work item **implements option (c)**: a single `apply_analyst_overrides` toggle (default on, in the hero block) that drives slider recompute, tornado source, and the headline in lockstep, plus a precomputed second sensitivity (`sensitivities_applied`) so the tornado describes whichever LCOE function the toggle selects.

The direction (option (c) vs (a)/(b)) was an open decision in the original draft of this spec; it is now **settled at the epic level** (see EXPLORER-UX-V3, Phase 1 Decisions). The option analysis is retained below as rationale. The override **inspection affordance** (originally FR-SO7 here) is **split out to Item 2** (`explorer-override-inspection`) so this item is one cohesive theme — *make the slider/tornado/headline cohere* — and Item 2 is *explain the overrides*. This item ships the toggle with an **inert** "(N entries)" count; Item 2 makes that count a clickable panel trigger.

## Why This Matters Now

Verified on concept 01 with the current `_compute_cached` mechanism: `result_1gw.costs.lcoe = 155.17 $/MWh` (the JSON headline, with the analyst's $1.03B C220103 magnet override applied). The first time a user touches *any* slider, recompute runs `model.forward(**result_1gw.params, **slider_overrides)` *without* the analyst's `cost_overrides`, and LCOE collapses to `127.53 $/MWh` (−27.6 $/MWh, −17.8%). The user did not change anything material — `availability` moved by half a percent — but the headline number jumped because the registry vanished. This makes every slider untrustworthy until the user understands the mechanic, and the mechanic isn't visible anywhere in the UI.

The same mechanism existed pre-rework, but it mattered less: most concepts had small or no override registries, so the slider's effect dominated the registry's disappearance. The rework deliberately moved cost weight into the registry (one analyst-defensible override per CAS departure, six fields each, with provenance and rationale). Concept 01's magnet override alone moves LCOE by ~$28/MWh. Every other concept with non-trivial fit-grade follows the same pattern. The discontinuity is now a first-order UX failure.

## Key Bets / Constraints

- **Bet:** This is a UX correctness issue, not a numerical one. The library and the helper are doing the right thing; the recompute pathway is silently changing the question the slider is asking.
- **Constraint:** Whatever the slider computes has to be consistent with how `model.sensitivity()` computes the tornado baselines. As shipped, `build_sensitivity_analysis` calls `model.sensitivity(result.params)` with `cost_overrides=None` (extract_explorer_data.py:184) — so the **current tornado is library-bare**, not overrides-applied. The library's `sensitivity()` accepts an optional `cost_overrides` arg, so the extractor emits both flavors cheaply. Under option (c) the slider and tornado must always be sourced from the *same* LCOE function as the headline — selected by the toggle.
- **Constraint:** The library exposes `override_reference_mw` so that overrides scale correctly when `n_mod ≠ 1`. Re-applying the registry on recompute must pass `override_reference_mw=P_native` (i.e. revive the work FR-A4 was meant to do, with a real motivating example this time).
- **Non-goal:** A redesigned slider UI. The toggle is the only new control; beyond it, slider visuals are unchanged.
- **Non-goal:** Touching `model.sensitivity()` or the tornado's baseline computation. The discrepancy is at the slider-recompute path; the second sensitivity is produced by *calling* `model.sensitivity(cost_overrides=...)`, not by changing it.
- **Non-goal:** Letting the user *edit* the analyst's registry from the UI. The registry is analyst-authored, version-controlled, and source-cited; it is not a runtime knob.
- **Non-goal (this item):** The override-inspection panel and its multi-site triggers — owned by Item 2 (`explorer-override-inspection`). This item renders the "(N entries)" count as inert text only.

---

## Business Goals

### Why This Matters

The explorer's slider is the primary mechanism by which the user develops intuition for how a concept's LCOE responds to engineering and financial assumptions. If the first slider movement produces a discontinuity unrelated to the slider, the tool teaches the wrong intuition — and silently undermines the analyst's hard-won override work. Resolving this is small surface, large credibility. The toggle additionally becomes a *teaching* surface: flip it and watch the registry's contribution to LCOE (~$28/MWh on concept 01) appear and disappear — the cleanest possible illustration of "what is the analyst's judgment worth here?"

### Success Criteria

- [ ] Sliders perturb the **toggle-selected** LCOE function (analyst-applied by default), never silently a different one. The chosen semantics are documented in an inline doc comment and/or the explorer README.
- [ ] At default UI state (`apply_analyst_overrides=True`, slider untouched) the recomputed headline equals the stored JSON headline modulo the *intentional* slider effect — no spurious discontinuity attributable to the override registry.
- [ ] The headline ↔ slider ↔ tornado triple always agree about which LCOE function is being shown, in either toggle state, with no partial-update frame.
- [ ] The toggle is hidden or visibly disabled for concepts where it has no effect (empty registry, freeform, `fit_grade=None`) — never a dead control.

### Priority

P1. Lands first in EXPLORER-UX-V3 Phase 1, ahead of Item 2 (the inspection surface hangs off this item's toggle/count). The discontinuity is visible the first time anyone uses the explorer post-unblock, so it is the right place to start.

---

## Problem Statement

### Current State

`server.py:_forward_with_overrides` (the function the slider's `/api/compute` endpoint calls) is documented to *not* re-apply `cost_overrides`:

> "cost_overrides are not re-applied; this is consistent with how `model.sensitivity()` works (it also omits cost_overrides)."

That comment is technically true and was a defensible decision pre-rework. The deeper structural reason it works that way: `result.params` carries the physics/financial scalars `forward()` consumes, but **the override registry is a separate argument** that is consumed once and only leaves a trace in the output cost values — it is not in `params`. So the server, which models a recompute as "perturb `params`, call `forward()` again," has no way to re-apply the registry without being given new access to it.

Post-rework this produces three observable inconsistencies:

1. **Headline ↔ first slider value mismatch.** Stored `cost_model.headline.lcoe_per_mwh` is computed with overrides on; the first compute response is computed with overrides off. They disagree by the magnitude of the registry, which on rework-aligned concepts is non-trivial.
2. **Tornado ↔ headline axis mismatch.** As shipped, the tornado bars are elasticities of the **library-bare** LCOE (`model.sensitivity(result.params)` with `cost_overrides=None`). The stored headline is the **overrides-applied** LCOE. So the tornado claims to explain "how this LCOE moves with each parameter," but it's explaining a different LCOE than the one in the hero number. The slider, also library-bare today, happens to agree with the tornado — and both disagree with the headline.
3. **Analyst attribution erased.** The rework's whole point was to make every cost departure from the library a single accountable, sourced, toggleable registry entry. The slider silently throws all of them out, and the tornado never sees them.

A subtlety that matters for implementation: the with-overrides sensitivity is **not** just the bare sensitivity with overridden accounts zeroed out. `_scale_overrides` propagates an override from its reference frame to the target frame by a library-computed ratio that itself depends on the physics params. So overrides replace the library's *level* for an account while keeping a (rescaled) version of the library's *shape*. The elasticities under "with overrides" can move either direction relative to bare, including in magnitude rank. `sensitivities_applied` must therefore be computed by an honest `model.sensitivity(..., cost_overrides=enabled)` call — never derived from `sensitivities_bare` by post-hoc adjustment. The UI must be honest about which sensitivity it is showing.

### Desired Outcome

The slider's recomputed LCOE, the tornado bars, and the headline are all sourced from the toggle-selected LCOE function. With the toggle on (default), all three reflect the analyst-applied LCOE with the registry scaled correctly under the two-knob mechanism; with it off, all three reflect the library-bare LCOE. The headline ↔ slider ↔ tornado triple agrees about which question is being answered, and toggling swaps all three atomically.

---

## Scope

### In Scope

- Implementation of option (c): the `apply_analyst_overrides` toggle and its lockstep wiring across slider recompute, tornado source, and headline.
- The data-layer changes that enforce it: `_forward_with_overrides` re-applying the registry (with `override_reference_mw=P_native`) under the toggle, LRU cache key shape, `_FORWARD_NAMED` / `_FORWARD_SKIP` adjustments, and the extractor emitting `sensitivities_bare` + `sensitivities_applied`.
- The hero-block toggle UI (checkbox + label with inert "(N entries)" count + plain-language subtitle), hidden/disabled per FR-SO6.
- `apply_analyst_overrides` added to `ExplorerState` (per-concept) and threaded through `/api/compute` and tornado selection.
- Tests asserting headline-↔-first-recompute consistency under the toggle.
- A short README addition (or inline doc comment) explaining the chosen semantics so the next reader doesn't re-derive them.

### Out of Scope

- The override-inspection affordance (panel + multi-site ★ triggers + disabled-override display) — owned by **Item 2** (`explorer-override-inspection`). This item renders only the inert "(N entries)" count.
- Per-account `generic`/`native`/`result_1gw` delta decomposition (future EXPLORER-UX-V3 phase).
- Editing the registry from the UI.
- Changes to `model.sensitivity()` or to the helper's `run_native_and_1gw`.
- The 12 old-shape concepts. Their `analysis.md` regen is Item 11 of the rework epic; their slider behavior is whatever this spec lands.

### Decision: Option (c) (settled)

Three options were on the table; option (c) is adopted. The analysis is retained so the next reader sees why.

- **(a) Preserve current behavior; label the divergence in the UI.** Slider recompute stays overrides-off; the UI badges the slider output as "library-bare projection." *Rejected:* the user has to mentally hold two LCOE numbers per concept; the tornado-↔-headline mismatch remains; analyst attribution stays invisible.
- **(b) Re-apply the registry on recompute; pass `override_reference_mw`.** Slider recompute always applies the registry; the tornado is regenerated overrides-on. *Rejected:* the explorer would then only ever show the analyst's LCOE; the library-bare baseline — a genuinely useful interpretive object — disappears entirely.
- **(c) Expose both LCOE functions; user toggles between them. ADOPTED.** A single checkbox controls *both* the slider recompute and the tornado source. **Checked (default)** → analyst-applied LCOE everywhere (slider, headline, tornado). **Unchecked** → library-bare LCOE everywhere. The toggle is the UI surface of an affordance the registry already encodes (every override has an `enabled` field; the registry is designed to be reversible).

**Rationale for (c):** the two LCOE functions are genuinely different objects, both interpretively useful — the library-bare answer says "what does the costing framework predict for this architecture," and the analyst-applied answer says "what is the accountable cost story including company-stated departures." Forcing a single answer hides one. The toggle is the smallest honest surface that lets the user see both, the second sensitivity is cheap (~ms in `model.sensitivity`), and it is pedagogically aligned with the rework's framing. Under (c) the data-layer change subsumes (b)'s; choosing (c) is "(b) + a flag + a precomputed second sensitivity + the toggle UI."

### Edge Cases & Considerations

- A concept with an empty override registry: behavior is unchanged; the toggle is hidden/disabled (FR-SO6).
- Freeform concepts (no `cost_overrides`): unaffected; toggle hidden.
- Disabled overrides (`enabled: False`): the helper's `enabled_overrides()` already filters these out; whatever the server reads from the concept module gets the filtered set. (Their *display* is Item 2's concern.)
- `cost_overrides` are stored only in the concept's `model_setup.py` (the `overrides` list before `enabled_overrides()` projection). Reading them at compute time means re-evaluating the module-level expressions, which already happens in `_load_model_module`. No new IO.

---

## Requirements

### Functional Requirements

1. **FR-SO1**: The recomputed `CostModelData` returned by `POST /api/compute` for a concept at **default UI state** (`apply_analyst_overrides=True`) with `overrides == {}` (slider untouched) SHALL produce a headline `lcoe_per_mwh` equal (within floating-point tolerance) to the same concept's stored `cost_model.headline.lcoe_per_mwh`. No spurious discontinuity on first slider touch.
2. **FR-SO2**: The slider's response curve (the locus of recomputed LCOE as a single sensitivity parameter sweeps its range) SHALL be consistent with the tornado's elasticity for that parameter, in whichever toggle mode the user is in (signs agree; small-perturbation slopes agree to leading order). The slider and the tornado SHALL be sourced from the same LCOE function at any given moment — never one from each.
3. **FR-SO3**: The chosen behavior SHALL be documented in the spec, the design, or an inline doc comment in `_forward_with_overrides` so the next reader does not re-derive it from runtime behavior.
4. **FR-SO4**: The extractor SHALL emit two precomputed `SensitivityAnalysis` payloads per costingfe concept: `sensitivities_bare` (= `model.sensitivity(result.params, cost_overrides=None)`) and `sensitivities_applied` (= `model.sensitivity(result.params, cost_overrides=enabled_overrides(...))`). The frontend selects between them based on the toggle state. For concepts with empty registries, the two payloads are equal and only one need be stored.
5. **FR-SO5**: A single boolean `apply_analyst_overrides` (default `True`) SHALL be added to `ExplorerState` and threaded through `/api/compute` and the tornado source selection. The LRU cache key for `_compute_cached` SHALL be extended to `(concept_id, frozenset(overrides), apply_analyst_overrides)` so cache hits remain correct under the toggle.
6. **FR-SO6**: For concepts with an empty registry, no `model_setup.py`, or `fit_grade=None` (freeform), the toggle SHALL be hidden or visibly disabled — never rendered as an active control with no effect.
7. **FR-SO7** *(RELOCATED → Item 2, `explorer-override-inspection`)*: The discoverable override-inspection affordance — surfacing each entry's `account`, `value`, `provenance`, `source`, and `rationale` (plus disabled-override display) — is **out of scope for this item** and owned by Item 2. This item renders the toggle's "(N entries)" count as inert text; Item 2 makes it the clickable trigger. The identifier is retained here so the epic's reference resolves.

### Non-Functional Requirements

- No measurable regression in `/api/compute` p95 latency (200 ms p95 ceiling is the rule of thumb).
- LRU cache hit rate for repeated identical slider positions SHALL remain ≥ pre-change rate (i.e. the cache key extension is sound).

---

## Acceptance Criteria

### Core Functionality

- [ ] FR-SO1: for at least three rework-aligned concepts spanning fit-grade tiers (e.g. 01 High, 17a Low, 24 Low-pB11), the no-op slider call (`overrides={}`) at default UI state returns `lcoe_per_mwh` matching the stored JSON's headline.
- [ ] FR-SO2: a sweep of `availability` from 0.7 to 0.95 in 0.05 steps produces a monotone LCOE curve whose slope sign matches the tornado's `availability` elasticity sign — verified separately in each toggle state.
- [ ] FR-SO3: the chosen semantics are written down somewhere version-controlled and discoverable.
- [ ] FR-SO4: for concept 01 (registry size ≥ 1), `sensitivities_bare` and `sensitivities_applied` differ for at least one parameter and both are present in the extracted JSON.
- [ ] FR-SO5: toggling the checkbox between states without moving any slider swaps the headline LCOE, the slider baseline, and the tornado bars in lockstep — no partial-update state where one view has updated and another has not.
- [ ] FR-SO6: a freeform concept (e.g. concept 03 Cortex or another `fit_grade=None`) renders the concept page with no toggle visible; a costingfe concept with an empty registry (if any exist) renders the toggle in a disabled state with hover explanation.

### Quality & Integration

- [ ] Existing test suite passes.
- [ ] New regression test for FR-SO1 against concept 01.
- [ ] Slider performance not visibly degraded in manual smoke (open concept page, drag a slider, observe no new lag).

---

## UX Requirements for the Design Phase

Design MUST resolve the following before implementation. Listed here so they cannot be silently dropped. (The override-inspection view, formerly in this section, has moved to Item 2.)

### Checkbox placement and behavior

- **Where:** **hero block, next to the LCOE number** (settled). Rationale: it makes the user read "*this number* is the analyst's" first — the headline is the thing whose trustworthiness is in question. Design need not re-litigate placement, only the exact layout within the hero.
- **Default state:** checked (analyst overrides applied). This is what makes FR-SO1 hold.
- **Persistence:** per-concept (lives in `ExplorerState`, keyed by concept id) so a user comparing two concepts can see one in each mode side by side.
- **State transitions:** toggling MUST update the headline LCOE, the slider's baseline, and the tornado bars atomically. No animation order in which one view briefly disagrees with another.

### Labeling

- The label must teach what the toggle does on first read. Bad: "Use overrides." Better: "Apply analyst cost adjustments (N entries)." The `N` makes the registry's presence visible and gives the toggle weight when N is large. (The count is inert text in this item; Item 2 makes it the inspection trigger.)
- For concepts with N = 0: the toggle is hidden or disabled (FR-SO6); no need to label it.
- A secondary line or tooltip beneath the label MUST clarify what "applied" / "unapplied" means in plain terms — e.g. "On: the analyst's accountable cost story. Off: the costing library's bare answer for this architecture."

### Inert count, visible at rest

- Render the "(N entries)" count visible at rest in low-emphasis styling (not hidden behind hover) so the registry's presence is discoverable. Style it as a *label*, not a button — it is not yet clickable in this item, and must not read as broken. Item 2 upgrades it to the panel trigger.

---

## Next-Stage Handoff

**Settled before design:**
- The discontinuity is real, large, and worth fixing.
- Direction = option (c) (settled at epic level). Under (c) the data-layer change subsumes (b)'s.
- Toggle placement = hero block; default checked; persistence per-concept.
- The inspection affordance (FR-SO7) is split to Item 2.

**Design must figure out:**
- Where the registry lives at compute time — re-imported from the concept's `model_setup.py` (cheapest; already done via `_load_model_module`'s LRU cache) or stored in the extracted JSON. (Recommend re-import; Item 2 separately emits the registry *narrative* into the JSON for display, which is a different read.)
- LRU cache key shape. Current key is `(concept_id, frozenset(overrides.items()))`; FR-SO5 adds the toggle bool.
- `P_native` provisioning to `_forward_with_overrides` — derived from `result_1gw.params` (`net_electric_mw / n_mod`) or read from frontmatter. Pick one.
- Exact toggle label/subtitle wording and hero layout.
- The exact text of any inline doc comment or README addition explaining the chosen semantics.
- How the frontend selects between `sensitivities_bare` / `sensitivities_applied` and rebinds the tornado atomically with the headline on toggle.

**Watch-outs for design:**
- The slider must remain interactive. A 200 ms p95 ceiling is the right rule of thumb.
- Do not accidentally re-introduce the `result` symbol; the unblock work item removed it deliberately.
- `override_reference_mw` only matters when overrides are non-empty and `n_mod ≠ 1`. Don't accidentally pass it as `None` to a library version that doesn't tolerate it (verify forward signature — current library accepts None as default).
- The *with-overrides sensitivity* is not just the bare sensitivity with overridden accounts zeroed out — `_scale_overrides` keeps a rescaled version of the library's shape for overridden accounts. Do not derive `sensitivities_applied` from `sensitivities_bare`; call `model.sensitivity(...)` honestly with `cost_overrides=enabled`.

---

## Related Artifacts

- **Epic:** [`.project/backlog/epic_explorer_ux_v3.md`](../../backlog/epic_explorer_ux_v3.md) — EXPLORER-UX-V3, Phase 1.
- **Item 2 (successor):** `.project/active/explorer-override-inspection/` — the override-inspection surface (owns FR-SO7); triggers off this item's toggle/count.
- **Driving research:** [`.project/research/20260605-150329_concept-explorer-ux-user-journeys.md`](../../research/20260605-150329_concept-explorer-ux-user-journeys.md).
- **Predecessor:** [`.project/active/explorer-rework-unblock/spec.md`](../explorer-rework-unblock/spec.md) — where this issue was identified and deferred.
- **Three-forward contract:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:1-31`.
- **Override registry shape:** `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:46-83` (`Override` TypedDict, `enabled_overrides`).
- **Sensitivity baseline computation:** `costingfe.model.CostModel.sensitivity` (called via `build_sensitivity_analysis` in extract_explorer_data.py:178).
- **Concrete evidence of the discontinuity:** concept 01, verified 2026-06-05 — `result_1gw.costs.lcoe = 155.17 $/MWh` vs library-bare re-forward `= 127.53 $/MWh`.

**Next Steps:** Proceed to `/_my_design` to lock the LRU cache key shape, `P_native` provisioning, registry-at-compute-time source, and the atomic toggle/sensitivity-rebind mechanism.
