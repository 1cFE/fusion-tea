# Spec: 1costingFE Two-Knob Projection Support

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-30 11:53 PDT
**Complexity:** MEDIUM
**Branch:** downselect-study

---

## Work Item Summary

The concept-analysis rework projects every concept's cost to a common "1 GWe NOAK" basis using two of the costing library's scaling knobs together: `net_electric_mw` sizes the shared plant, and `n_mod` replicates the reactor island, with each module held at the design point's native operating point via `n_mod = 1000 / P_native`. Two things in `1costingFE` block this today: `n_mod` is constrained to integers, and the override-scaling path (`_scale_overrides`) computes its reference at the wrong module count, so per-module overrides are mis-scaled under the two-knob call. This work item makes both correct. "Done" means the rework's two-knob projection call produces correct, self-consistent results for every concept, and the existing single-knob behavior is unchanged.

## Why This Matters Now

This is the **first risk to de-risk** in the rework design (`concept-analysis-rework-design.md`): if the two `1costingFE` preconditions don't hold, the entire cost-projection invariant fails and the rework cannot put concepts on a common basis. Both changes are small and localized, but the second is a genuine correctness bug (not just a feature gap), so it must be specified and tested before the migration pilot rather than discovered during it.

## Key Bets / Constraints

- **Bet:** The two-knob mechanism (output power for the shared plant, module count for the reactor island) carries the entire cost projection — no parallel rollup, no ad-hoc scaling helpers. The library must support it cleanly.
- **Constraint:** Existing single-knob usage (`n_mod=1`, with or without `override_reference_mw`) MUST continue to produce identical results. The `costingfe-scaled-overrides` work (Complete, 2026-04-19) is in production and must not regress.
- **Constraint:** Changes are confined to the `1costingFE` repo (`/home/reid/1cfe/1costingfe`). No fusion-tea pipeline code is in scope here.
- **Non-goal:** No new archetypes, no new cost accounts, no change to which accounts are overridable, no change to the NOAK/FOAK flags.

---

## Business Goals

### Why This Matters

The rework's central promise — cross-concept comparison that is apples-to-apples *by construction* — rests on every concept reaching 1 GWe NOAK through the same mechanism. That mechanism is the two-knob `forward()` call. It cannot be used until the library accepts a fractional `n_mod` and interprets overrides correctly under it. Without these, the pipeline falls back to the current state where "1 GWe" means a different thing for each concept.

### Success Criteria

- [ ] The rework's two-knob projection call runs for any concept and any native power without error.
- [ ] A per-module reactor-island override given at the design point is honestly replicated to 1 GWe (not frozen, not double-scaled).
- [ ] A plant-total override given at the design point scales to 1 GWe by its own output-power law.
- [ ] Every existing `model_setup.py` and library example that uses the old single-knob pattern produces byte-identical cost results.

### Priority

P0 blocker for the concept-analysis rework migration. Nothing downstream (templates, pilot, batch regeneration) can proceed until this lands.

---

## Problem Statement

### Current State

1. **`n_mod` is integer-only.** `validation.py:90` declares `n_mod: int = Field(default=1, ge=1, strict=True)`. `strict=True` rejects floats outright. `n_mod = 1000 / P_native` is generally fractional, so the two-knob call is impossible without integer rounding (which pushes per-module power off the native design point).

2. **Override scaling uses the wrong reference module count.** `_scale_overrides` (`model.py:849–896`) runs its reference and target forwards with the *same* `n_mod` — the call's target `n_mod` is threaded into both (`model.py:418` passes `n_mod=n_mod`). For the two-knob call `forward(net=1000, n_mod=1000/P, override_reference_mw=P)`, the reference is therefore computed at `(net=P, n_mod=1000/P)`, giving per-module power `P²/1000` instead of the native `P`. A per-module override (stated as a single-module cost at the native design point) is then scaled by a wrong ratio. The result is silently incorrect — no error is raised.

### Desired Outcome

`forward(net_electric_mw=N, n_mod=M, cost_overrides=…, override_reference_mw=R)` accepts any positive real `M`, and interprets every override as a **single-module cost at reference power `R`**, scaling it to the target `(N, M)` by the account's own scaling law:
- per-module reactor-island accounts scale by the per-module power ratio (identity when the target per-module power equals `R`), then are replicated `×M` by the existing machinery;
- plant-total accounts scale by the output-power ratio `R → N`.

Existing single-knob behavior is a special case (`M = 1`) and is unchanged.

---

## Scope

### In Scope

- Relaxing the `n_mod` type/validation to accept any positive real value.
- Verifying (and testing) that all `n_mod`-dependent computations remain correct for fractional `n_mod`.
- Correcting `_scale_overrides` so the reference is computed at a single module (`n_mod = 1`), independent of the call's target `n_mod`, establishing the semantic "`override_reference_mw` = single-module reference power."
- Tests covering fractional `n_mod` end-to-end and correct two-knob override scaling for both per-module and plant-total accounts.
- A backward-compatibility check that single-knob results are unchanged.

### Out of Scope

- The fusion-tea pipeline changes that *use* this (`model_setup.py` template, shared two-knob helper, override registry). Those are separate rework work items.
- Any change to which accounts are overridable, to NOAK/FOAK behavior, or to the per-account scaling exponents themselves.
- Machine-resizing / geometry-from-power-target modeling (explicitly not how scaling works; out of scope by design).

### Edge Cases & Considerations

- **`n_mod < 1`** (design point above 1 GWe): mathematically valid (a fractional de-rate); the multi-unit labor term `(1 + (n_mod−1)·0.92)` and `√n_mod` stay finite. Decide whether to allow silently or validate. *(Deferred to design — flagged, not decided here.)*
- **`ref_computed == 0`** in `_scale_overrides` (`model.py:890–894`): currently passes the override through unscaled. The rework's discipline is "no silent fallbacks." Decide whether to keep the passthrough or raise when an overridden account is structurally absent. *(Deferred to design — flagged.)*
- **`n_mod = 1` / `P_native = 1000`**: the two-knob call must collapse exactly to the single-module reference; `result` and `result_1gw` equal. This is the backward-compatibility anchor.
- **Internal `forward()` recursion in `_scale_overrides`**: the reference/target forwards run the bare model; if the bare model fails to converge at either power, scaling fails. Holding each module at native power (the rework's whole point) should keep both convergent, but the reference-`n_mod` change must not introduce a non-convergent reference operating point.

---

## Requirement Selection Notes

The normative requirements below cover only what must be true for the two-knob projection to be correct and for existing usage not to regress. The two flagged edge-case decisions (`n_mod < 1`, `ref_computed == 0`) are intentionally left as design questions — they are policy choices, not yet decisions. The per-account scaling exponents themselves are not restated as requirements; they are existing, trusted library behavior this work item relies on but does not change.

---

## Requirements

### Functional Requirements

> From the rework design's "1costingFE preconditions" unless marked [FROM INVESTIGATION].

1. **FR-1 — Non-integer `n_mod`.** The library MUST accept any positive real `n_mod`. `forward()` and input validation MUST NOT reject or silently coerce a fractional `n_mod`. (Relax `validation.py:90` from `int … strict=True` to a positive float, `gt=0`.)

2. **FR-2 — Continuity preserved.** [FROM INVESTIGATION] All `n_mod`-dependent computations MUST remain correct for fractional `n_mod` — per-module power (`net/n_mod`), reactor-island replication (`×n_mod`), multi-unit labor (`1 + (n_mod−1)·factor`), land (`√n_mod`), CAS72 replacement, and the LCOE denominator (`p_net·n_mod`). (All are continuous arithmetic today; this is a preservation requirement, verified by test, not new code.)

3. **FR-3 — Single-module reference semantics.** `override_reference_mw` MUST be interpreted as a **single-module** reference power. The reference forward inside `_scale_overrides` MUST use `n_mod = 1`, independent of the call's target `n_mod`.

4. **FR-4 — Correct two-knob override scaling.** Under `forward(net_electric_mw=N, n_mod=M, cost_overrides=…, override_reference_mw=R)`, each override MUST be scaled from the single-module reference at `R` to the target `(N, M)` by that account's own scaling law: per-module reactor-island accounts by the per-module power ratio (which is identity when the target per-module power `N/M` equals `R`), with replication to `×M` applied by the existing per-module machinery; plant-total accounts by the output-power ratio `R → N`.

5. **FR-5 — Replacement preserved.** An applied override MUST fully replace the computed value at its layer (per-module slot for reactor-island sub-accounts; total for top-level and plant-wide accounts), with no additive fudge factor. (Existing behavior; preserve.)

6. **FR-6 — Backward compatibility.** For `n_mod = 1`, results MUST be identical to current behavior, both with and without `override_reference_mw`. The `costingfe-scaled-overrides` integration MUST NOT regress.

### Non-Functional Requirements

- Test coverage MUST include: a fractional-`n_mod` end-to-end `forward()`; a per-module override correctly replicated under the two-knob call; a plant-total override correctly output-power-scaled under the two-knob call; and a backward-compatibility assertion against current single-knob results.

---

## Acceptance Criteria

### Core Functionality
- [ ] `forward(net_electric_mw=1000, n_mod=3.83, …)` runs and returns a valid `ForwardResult` (no validation error, no coercion).
- [ ] Two-knob per-module case: a coil override `C220103=V` stated per-module at `P_native`, called with `net=1000, n_mod=1000/P_native, override_reference_mw=P_native`, yields total coils ≈ `V × (1000/P_native)` (per-module ratio ≈ 1, replicated by `n_mod`).
- [ ] Two-knob plant-total case: a `CAS21=V` override at `P_native` scales to 1000 MWe by the buildings output-power law (ratio = `CAS21(1000)/CAS21(P_native)`), not by replication.
- [ ] `n_mod = 1` / `P_native = 1000`: `result` and `result_1gw` are equal.

### Quality & Integration
- [ ] Existing `1costingFE` test suite passes.
- [ ] Backward-compatibility test: representative single-knob calls (`n_mod=1`, with and without `override_reference_mw`) produce results identical to pre-change output.
- [ ] LCOE and overnight cost are continuous across a sweep of fractional `n_mod` (no discontinuity at integer boundaries).

---

## Next-Stage Handoff

**Settled in this spec:**
- The two library changes and their intent (FR-1 through FR-6).
- `override_reference_mw` means a single-module reference power; the fix is "reference forward at `n_mod=1`."
- Backward compatibility with single-knob usage is mandatory.
- The fusion-tea pipeline that consumes this is out of scope.

**Design must figure out:**
- The exact `_scale_overrides` change: thread a fixed `n_mod=1` into the reference forward while leaving the target forward on the call's `n_mod` (and confirm top-level vs per-module account lookups still use the right representation).
- Decision on `ref_computed == 0`: keep silent passthrough or raise.
- Decision on `n_mod < 1`: allow or validate (and any clamp/warning).
- The precise `validation.py` field change and whether any downstream type hints (`forward()` signature `n_mod: int`) should be updated for honesty.

**Watch-outs for design:**
- `_scale_overrides` runs the bare model twice; the reference-`n_mod` change must not create a non-convergent reference operating point.
- The per-module identity ratio relies on the target per-module power equaling `R`; if a caller ever uses the two-knob call with `N/M ≠ R`, per-module accounts will (correctly) scale — make sure tests pin the intended `N/M = R = P_native` case and document the general behavior.
- Keep the change minimal and reversible; this is the load-bearing precondition for the whole rework.

---

## Related Artifacts

- **Design concept (driver):** `.project/concepts/concept-analysis-rework-design.md` (Required Invariants → 1costingFE preconditions; First risk to de-risk)
- **Prior work (introduced `override_reference_mw`):** `.project/active/costingfe-scaled-overrides/` (Complete)
- **Diagnostic report (mechanics + the bug):** `.project/reports/2026-05-30-1gw-scaling-and-override-interpretation.md`
- **Library reference:** `.project/research/20260530-072832_1costingfe-and-pipeline-redesign-context.md`
- **Design:** `.project/active/costingfe-two-knob-projection/design.md` (to be created)

---

## Appendix — Verification detail (does not count toward main-body budget)

### A. The `_scale_overrides` reference-`n_mod` bug, worked

Call: `forward(net=1000, n_mod=1000/P, cost_overrides={…}, override_reference_mw=P)`.

`forward()` (`model.py:418`) invokes `_scale_overrides(cost_overrides, reference_mw=P, target_mw=1000, n_mod=1000/P, …)`. Inside (`model.py:865–870`):

```python
ref_result    = self.forward(net_electric_mw=P,    cost_overrides=None, **forward_kwargs)  # n_mod = 1000/P
target_result = self.forward(net_electric_mw=1000, cost_overrides=None, **forward_kwargs)  # n_mod = 1000/P
```

- ref per-module power = `P / (1000/P)` = `P²/1000` (e.g., 90 MWe for P=300) — **not native `P`**.
- target per-module power = `1000 / (1000/P)` = `P` (native).

A per-module override stated at native `P` is then scaled by `target_per_module / ref_per_module`, which is **not 1** for power-dependent per-module accounts — the override is inflated.

**Fix:** compute the reference at a single module:

```python
ref_kwargs = {**forward_kwargs, "n_mod": 1}
ref_result = self.forward(net_electric_mw=P, cost_overrides=None, **ref_kwargs)
```

Then ref per-module power = `P` (native) = target per-module power ⇒ per-module ratio = 1 ⇒ override rides `×n_mod`. Plant-total accounts: ref total at `P`, target total at `1000` ⇒ output-power ratio. Both correct.

### B. Why FR-2 needs no new code

Every `n_mod` use in the library is continuous (verified by grep — no `range(n_mod)`, `int(n_mod)`, indexing, or modulo):

| Use | Location |
|---|---|
| per-module power `net/n_mod` | `model.py:105` |
| reactor-island `× n_mod` + labor `(1+(n_mod−1)·0.92)` | `cas22.py:451–453` |
| land `√n_mod` | `costs.py:49` |
| BOP CAS23–26 `n_mod × …` | `costs.py:116/124/132/141` |
| CAS72 replacement `× n_mod` | `costs.py:306/335/348/370` |
| LCOE denominator `p_net × n_mod` | `economics.py:63/65` |

FR-2 is therefore a *preservation* requirement enforced by test, not new logic.
