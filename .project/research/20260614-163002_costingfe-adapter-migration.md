---
date: 2026-06-14T16:30:02-07:00
researcher: Claude
topic: "Migrating model_setup.py invocation from CostModel.forward() to costingfe.adapter.run_costing()"
tags: [research, costingfe, adapter, model-setup, pipeline, migration]
status: complete
last_updated: 2026-06-15
---

# Research: Migrating to the `costingfe.adapter` invocation

> **UPDATE 2026-06-15 — prerequisite gap #1 is now CLOSED upstream.** Pulled
> `1costingfe@master` (commit `b9b0a4c`, 21 commits ahead of what this doc was
> first written against). Commit `74476c5 "Add override_reference_mw field to
> fusion-tea adapter"` added `override_reference_mw: float | None = None` to
> `FusionTeaInput` and wired it into both `CostingInput` validation
> (adapter.py:94) and `model.forward()` (adapter.py:127). Two new tests cover it
> (`test_adapter.py:210` scaling, `:231` identity-at-target) and all 12 adapter
> tests pass on the fresh pull. Related commits also exposed `power_cycle`,
> `pulsed_conversion`, and `laser_driver_type` through `FusionTeaInput` as
> strings — which makes the full string-based migration (Option B) more viable
> than when this doc was written. **The remaining gaps are #2 (flat-dict return
> shape) and #3 (always-on sensitivity); both are addressable fusion-tea-side or
> with a small further adapter tweak. See "Status after 2026-06-15 pull" below.**

**Date**: 2026-06-14T16:30:02-07:00
**Researcher**: Claude
**Research Type**: Integration / cross-repo

## Research Question

The sister repo `1costingfe` now ships a typed boundary,
`costingfe.adapter.run_costing(FusionTeaInput) -> FusionTeaOutput`, advertised
as "the single function fusion-tea calls." Fusion-tea currently reaches into
`CostModel(...).forward(...)` directly. The task:

1. Understand what changed in `1costingfe` (the new adapter).
2. Understand the difference between the OLD direct-`CostModel` invocation and
   the NEW adapter recommendation.
3. Find the simplest/cleanest way to modify `model_setup.py` files and/or the
   supporting libraries to use the adapter.

## Summary

- **The actual `forward()` call in fusion-tea is not in the 124 `model_setup.py`
  files — it lives in one shared library: `model_setup_helpers.py`.** Per-concept
  files only declare data (`spec`, `overrides`, `P_native`), construct
  `model = CostModel(concept, fuel)`, and call two helpers
  (`generic_reference`, `run_native_and_1gw`). The helpers own every
  `model.forward(...)`. **This means the migration is fundamentally a one-file
  change** (`model_setup_helpers.py`), not a 124-file change.

- **The adapter, as written today, cannot serve fusion-tea's three-forward
  contract.** Two hard gaps:
  1. **No `override_reference_mw`.** `FusionTeaInput` has no such field and
     `run_costing` never passes it to `forward()`. The 1 GWe projection
     (`result_1gw`) depends on per-account override scaling via
     `override_reference_mw`. Without it, the projection column is wrong for
     every concept that carries cost overrides.
  2. **Return shape mismatch.** `run_costing` returns `FusionTeaOutput` with
     flat dicts (`costs["CAS10"]`, `power_table["p_fus"]`), whereas the helper's
     `print_cas_breakdown` reads attribute objects (`result.costs.cas10`,
     `result.cas22_detail`, `result.costs.total_capital`).
  - **Conclusion: the adapter must be extended in `1costingfe` before fusion-tea
    can adopt it for the production pipeline.** This is the prerequisite, and
    it is small (~10 lines).

- **A third, softer gap: `run_costing` always computes `sensitivity` (JAX
  autodiff).** The three-forward pipeline calls three forwards per concept and
  never uses sensitivity in the inspection block. Routing all three through
  `run_costing` as-is would add three JAX sensitivity passes per concept where
  there are currently zero — a real perf regression across 36 concepts. The
  adapter should grow a `with_sensitivity=False` opt-out.

- **The output contract is stdout text, and it is load-bearing.** The loop greps
  `LCOE:\s*([\d.]+)\s*\$/MWh` from `model_setup.py` stdout, and ~10 other scripts
  parse `model_output.txt` (`rerun_all_models.py`, `standardize_*.py`, the
  portfolio-audit probes). Any migration **must keep `print_cas_breakdown`'s
  stdout byte-identical.** This is satisfied trivially because
  `print_cas_breakdown` stays in the same helper file — only its internal field
  access changes (attribute → dict), not its `print()` formatting.

- **The structural contract validator pins the shape.**
  `validate_model_setup_contract(strict_helper_only=True)` requires module-level
  bindings `model`, `generic`, `native`, `result_1gw`, with `generic` bound via
  `generic_reference(...)` and `native, result_1gw` via `run_native_and_1gw(...)`
  (by function name, via AST). This is why the cleanest migration keeps those
  helper names and the `model` binding — it leaves the validator and templates
  untouched.

- **5 of 41 canonical files are "freeform" (concepts 02, 03, 16, 35, 38)** — they
  build bespoke dataclass models and never call costingfe. They are out of scope.
  The other **36 are costingfe-based**, all constructing
  `model = CostModel(concept=..., fuel=...)` on a single line, passing **only
  concept and fuel** (no `power_cycle` / `pulsed_conversion` /
  `laser_driver_type` to the constructor — those ride concept defaults today).

## Detailed Findings

### The new adapter (`1costingfe/src/costingfe/adapter.py`)

`run_costing(inp: FusionTeaInput) -> FusionTeaOutput` (adapter.py:64-179):

1. Maps strings → enums (`ConfinementConcept(inp.concept)`, `Fuel(inp.fuel)`,
   `PowerCycle(inp.power_cycle)`).
2. Validates customer inputs through `CostingInput(...)` — but **deliberately
   excludes** the engineering `overrides` from that validation (adapter.py:74-77),
   because they are partial; `forward()` re-validates after merging the YAML
   template. So partial specs are fine.
3. Loads `CostingConstants`, applies `costing_overrides` via `cc.replace(...)`.
4. Constructs `CostModel(concept, fuel, costing_constants, power_cycle,
   pulsed_conversion, laser_driver_type)`.
5. Calls `model.forward(net_electric_mw, availability, lifetime_yr, n_mod,
   construction_time_yr, interest_rate, inflation_rate, noak,
   cost_overrides, **inp.overrides)`.
6. **Does NOT pass `override_reference_mw`** (adapter.py:113-124).
7. Flattens `result.costs` → `costs` dict (CAS10..CAS90), then **merges
   `cas22_detail` into the same `costs` dict** (adapter.py:150-151) — so
   `FusionTeaOutput.costs` holds both `"CAS22"` and `"C220103"` keys.
8. **Always** calls `model.sensitivity(...)` (adapter.py:169).

`FusionTeaInput` fields (adapter.py:23-46): `concept, fuel, net_electric_mw,
availability, lifetime_yr, n_mod=1, construction_time_yr=6.0, interest_rate=0.07,
inflation_rate=0.02, noak=True, power_cycle="rankine", overrides={},
cost_overrides={}, pulsed_conversion="", laser_driver_type="",
costing_overrides={}`. **There is no `override_reference_mw` field.**

`FusionTeaOutput` fields (adapter.py:49-61): `lcoe, overnight_cost,
total_capital, costs (dict), power_table (dict), sensitivity (dict),
overridden (list)`.

Intended usage is confirmed by `1costingfe/tests/test_adapter.py`: string
concept/fuel, explicit `availability`/`lifetime_yr`, `overrides={...}` for
engineering knobs, asserts on `out.costs["CAS22"]`, `out.power_table["p_fus"]`,
`out.sensitivity["engineering"]["eta_th"]`.

### OLD vs NEW invocation — what actually differs

| Dimension | OLD (current fusion-tea) | NEW (adapter) |
|---|---|---|
| Entry point | `CostModel(concept, fuel)` + `model.forward(...)` | `run_costing(FusionTeaInput(...))` |
| Concept/fuel | enum (`ConfinementConcept.TOKAMAK`, `Fuel.DT`) | string (`"tokamak"`, `"dt"`) |
| Engineering spec | `**spec` splat into `forward()` | `overrides={...}` field |
| Cost overrides | `cost_overrides={CAS: M$}` | `cost_overrides={CAS: M$}` (same) |
| Per-unit overrides | `costing_constants=cc.replace(...)` by hand | `costing_overrides={field: value}` field |
| **Scaling** | **`override_reference_mw=...`** | **unsupported** |
| `n_mod` | `forward(n_mod=...)` | `FusionTeaInput.n_mod` |
| Return | `ForwardResult` (attr access, `.cas22_detail`) | `FusionTeaOutput` (flat dicts) |
| Sensitivity | only when explicitly called | computed every call |
| Validation | `forward()` internal | `CostingInput` up front + `forward()` internal |

The user's NEW snippet (`concept="tokamak"`, no overrides, no scaling) is the
*minimal* adapter call. Fusion-tea's real call is heavier: it needs engineering
spec, cost overrides, **and `override_reference_mw`** for the projection.

### Where the invocation lives in fusion-tea

- `exploration/concept_analysis/scripts/lib/model_setup_helpers.py` — **the only
  place `model.forward()` is called.** Three functions:
  - `generic_reference(model, spec, p_native, *, noak=True)` (helpers.py:85-112)
    → one bare forward (overrides off).
  - `run_native_and_1gw(model, spec, overrides, p_native, *, noak=True)`
    (helpers.py:115-178) → two forwards: `native`
    (`net_electric_mw=p_native, n_mod=1, cost_overrides=enabled,
    override_reference_mw=p_native`) and `result_1gw`
    (`net_electric_mw=1000, n_mod=round(1000/p_native),
    override_reference_mw=p_native, cost_overrides=enabled`).
  - `print_cas_breakdown(generic, native, result_1gw, overrides, *,
    data_grounded=True)` (helpers.py:192-277) → the stdout inspection block,
    using `.costs.<attr>` and `.cas22_detail`.
- Per-concept file shape (e.g. `analyses/01-hts-compact-tokamak/model_setup.py`):
  `from costingfe import ConfinementConcept, CostModel, Fuel`; build `spec`;
  `P_native = ...`; `model = CostModel(...)`; `generic = generic_reference(...)`;
  `overrides = [...]`; `native, result_1gw = run_native_and_1gw(...)`;
  `print_cas_breakdown(...)`. **No `forward()` call in the file.**
- Library defaults sourced inside the helper (not hardcoded per file):
  `default_availability(model.concept)` and
  `CostingInput.model_fields["lifetime_yr"].default` (helpers.py:37-40, 108, 143).

### Consumption points (the contracts a migration must not break)

1. **stdout LCOE grep** — `loop.py:722` and `rerun_all_models.py:28`:
   `re.search(r"LCOE:?\s*([\d.]+)\s*\$/MWh", text)`. Emitted by
   `print_cas_breakdown` (helpers.py:225).
2. **`run_model`** (`lib/claude.py:485-525`) executes `uv run python
   model_setup.py` as a subprocess, requires non-empty stdout containing "lcoe",
   writes it to `model_output.txt`.
3. **`model_output.txt` text parsers** — `rerun_all_models.py`,
   `standardize_eta_th.py`, `standardize_mn.py`, `standardize_lifetime.py`,
   `test_portfolio_audit_*.py`, `test_template_lint.py`, etc. They parse the
   `print_cas_breakdown` text layout.
4. **Structural AST validator** —
   `validators.py:936 validate_model_setup_contract(strict_helper_only=True)`
   requires module-level `model`, `generic`, `native`, `result_1gw`; `generic`
   via `generic_reference`, `native, result_1gw` via `run_native_and_1gw`
   (validators.py:977, 995-996, 1015). Wired on in the loop via
   `select_model_setup_validator` (loop.py:661-665).
5. **Templates** — `prompt_templates/model_setup_costingfe.md` and
   `_edit.md` instruct Claude to emit exactly this shape (import `CostModel`,
   construct `model`, call the helpers). Future generations follow the template.

**Key consequence:** as long as the helper names (`generic_reference`,
`run_native_and_1gw`, `print_cas_breakdown`), the module-level binding names
(`model`, `generic`, `native`, `result_1gw`), and the stdout text are preserved,
**the validator, the templates, and all downstream parsers are untouched.** That
is the seam to migrate behind.

## Code References

- `1costingfe/src/costingfe/adapter.py:23-61` — `FusionTeaInput` /
  `FusionTeaOutput` (note: no `override_reference_mw`).
- `1costingfe/src/costingfe/adapter.py:113-124` — `forward()` call, no scaling.
- `1costingfe/src/costingfe/adapter.py:150-151` — `cas22_detail` merged into
  `costs`.
- `1costingfe/src/costingfe/adapter.py:169` — unconditional `sensitivity`.
- `1costingfe/tests/test_adapter.py:1-60` — intended usage.
- `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:85-178` — the
  three forwards (the migration target).
- `exploration/concept_analysis/scripts/lib/model_setup_helpers.py:192-277` —
  `print_cas_breakdown` (attribute access to rewrite for dict access).
- `exploration/concept_analysis/scripts/lib/validators.py:936-1053` — structural
  contract.
- `exploration/concept_analysis/scripts/lib/claude.py:485-525` — `run_model`
  subprocess executor.
- `exploration/concept_analysis/analyses/01-hts-compact-tokamak/model_setup.py` —
  representative per-concept file.
- Prior research: `.project/research/20260530-072832_1costingfe-and-pipeline-redesign-context.md`
  (full library + pipeline reference), `.project/research/20260419-costingfe-scaled-overrides-integration.md`.

## Architecture Insights

- The three-forward contract (`generic` / `native` / `result_1gw`) is a
  fusion-tea invention layered on top of `forward()`. The adapter was designed
  for a *single* `run_costing` call (one plant, one scale) — the
  test file and the user's snippet both make one call. **The adapter and the
  three-forward contract are not yet shape-compatible**; closing that gap (the
  `override_reference_mw` field) is unavoidable for a faithful migration.
- `override_reference_mw` is the load-bearing difference. Per the 2026-05-30
  research (§A.6), it runs `forward()` twice without overrides at ref and target
  MW, takes per-account ratios, and rescales each override — per-account scaling,
  not a single exponent. Dropping it would silently mis-scale every
  override-carrying concept's 1 GWe column.
- Routing through the adapter buys a **stable typed boundary**: fusion-tea stops
  depending on `CostModel`'s constructor and `forward()` signature, depending
  instead on `FusionTeaInput`/`FusionTeaOutput`. That is the whole point of the
  adapter and the reason to migrate even though `forward()` works today.

## Feasibility Assessment

**Feasible, with one mandatory upstream change in `1costingfe` first.**

**Prerequisite (1costingfe, ~10 lines, blocks everything):**
1. Add `override_reference_mw: float | None = None` to `FusionTeaInput`; thread
   it into the `forward()` call in `run_costing`.
2. Add `with_sensitivity: bool = True` to `FusionTeaInput` (or a second arg to
   `run_costing`); skip the `model.sensitivity(...)` call when false, returning
   `sensitivity={}`. Avoids three wasted JAX passes per concept.
3. (Optional but tidy) expose `cas22_detail` as its own dict on
   `FusionTeaOutput` instead of only merging into `costs`, so the consumer
   doesn't have to re-split by key prefix.

**Risk / friction:**
- If the adapter extension is skipped, the only faithful path is to keep calling
  `forward()` directly — i.e., not migrate. There is no way to express the 1 GWe
  projection through today's adapter.
- The freeform concepts (02, 03, 16, 35, 38) never touch costingfe and are not
  part of this migration.
- Numerical regression check is cheap and decisive:
  `uv run python exploration/concept_analysis/scripts/rerun_all_models.py`
  re-runs all 36 costingfe models and reports LCOE deltas. Post-migration LCOEs
  must match pre-migration (the adapter wraps the *same* `forward()`), so any
  delta is a migration bug.

## Status after 2026-06-15 pull

| Gap (as first written) | Status now |
|---|---|
| **#1 — no `override_reference_mw`** (blocked the 1 GWe projection) | **CLOSED.** Field added + wired into validation and `forward()`; scaling + identity tests pass (commit `74476c5`). |
| **#2 — flat-dict return shape** (`costs["CAS10"]` vs `result.costs.cas10`; `cas22_detail` merged into `costs`) | **Still open.** Unchanged in the adapter. Handled entirely fusion-tea-side by rewriting `print_cas_breakdown` for dict access — no upstream change needed. |
| **#3 — `run_costing` always computes `sensitivity`** (3 wasted JAX passes per concept) | **Still open.** No opt-out flag yet (adapter.py:174). Either add `with_sensitivity=False` upstream, or accept the cost (it's correctness-neutral, only speed). |

Net effect: the one *mandatory* upstream prerequisite is done. The migration is
now a fusion-tea-side change (Option A or B below), with gap #3 as an optional
upstream nicety.

## Recommendations

Migrate **behind the helper seam**, in the supporting library — do **not** touch
the 124 per-concept files. Two staged options; **Option A is the recommended
"simplest/cleanest" path.**

### Step 0 — extend the adapter in `1costingfe`

**DONE for the required part (as of 2026-06-15):** `override_reference_mw` is
added and tested. The only remaining optional upstream tweak is a
`with_sensitivity=False` flag on `FusionTeaInput`/`run_costing` to skip the JAX
sensitivity pass the three-forward pipeline doesn't use (gap #3). Not a blocker —
do it only if the rerun perf matters.

### Option A — route the helpers through `run_costing`, keep everything else (RECOMMENDED)

Change exactly **one fusion-tea file**: `model_setup_helpers.py`.

- `generic_reference` / `run_native_and_1gw`: keep their current signatures
  (they still receive the `model` object). Internally, **build a
  `FusionTeaInput` and call `run_costing`** instead of `model.forward`. Read
  concept/fuel/config off the passed model:
  `concept=model.concept.value`, `fuel=model.fuel.value`,
  `power_cycle=model.power_cycle.value`, etc. — so any constructor settings a
  concept used are preserved transparently. Pass `override_reference_mw=p_native`
  and `with_sensitivity=False`.
- `print_cas_breakdown`: change attribute access to dict access
  (`generic.costs.cas10` → `generic.costs["CAS10"]`,
  `generic.cas22_detail` → the cas22 sub-keys of `generic.costs`, or the new
  `cas22_detail` dict if added in Step 0). Keep every `print(...)` format string
  byte-identical.
- **Untouched:** all 124 `model_setup.py` files, the contract validator, both
  templates, every downstream parser. The per-concept files still construct
  `model = CostModel(...)` — but that object is now just a typed carrier of
  concept/fuel/config; the actual costing runs through `run_costing`.

Pros: smallest possible diff (one file), zero risk to the validated contract and
templates, trivial regression check. Cons: per-concept files still import and
construct `CostModel`, so the `CostModel` *constructor* dependency isn't fully
severed (only the `forward()` dependency is).

### Option B — full adoption (sever `CostModel` from per-concept files)

Only if the goal is to eliminate `CostModel` from fusion-tea entirely:

- Per-concept files: replace `from costingfe import ConfinementConcept,
  CostModel, Fuel` + `model = CostModel(...)` with string constants
  (`CONCEPT = "tokamak"`, `FUEL = "dt"`); pass strings to the helpers. Mechanical
  and scriptable across the 36 costingfe files, but it is 36 edits.
- Helper signatures change to take `(concept, fuel, ...)` strings.
- Update `validate_model_setup_contract` required-name set (drop/replace the
  `model` binding requirement) and the inline-forward branch.
- Update `model_setup_costingfe.md` and `_edit.md` templates so future
  generations emit the string form.

Pros: fully adopts the adapter's string interface; no `CostModel` import
anywhere in fusion-tea. Cons: touches 36 files + validator + 2 templates;
larger blast radius for no numerical benefit over Option A.

### Suggested sequencing

1. Do Step 0 in `1costingfe` (+ test).
2. Implement Option A; run `rerun_all_models.py`; confirm zero LCOE deltas.
3. Decide whether the extra purity of Option B is worth the churn. If the
   medium-term plan is to drop the direct `CostModel` dependency, schedule
   Option B as a follow-on mechanical pass on top of A.

## Open Questions

- **Is `override_reference_mw` intentionally absent from the adapter** (deprecated
  in favor of some other scaling story), or simply not yet ported? This decides
  whether Step 0 is "add the field" or "rethink projection scaling." Worth a
  one-line confirmation with the costingfe side before implementing.
- **Should the 1 GWe projection's `n_mod` (= round(1000/P_native)) also flow
  through `FusionTeaInput.n_mod`?** It already maps cleanly (the field exists), so
  this is expected to be a non-issue — flagged only for the regression check.
- **Option A vs B** is a product decision (minimal diff now vs. fully severing
  `CostModel`). Recommendation is A now, B later if desired.
</content>
</invoke>
