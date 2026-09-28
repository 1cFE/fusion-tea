# Codegen findings — stellarator concept-09 end-to-end (2026-07-13)

Findings from running the MFE stellarator model through `sysml-codegen` (V11) → teax, beyond the 7 recorded in WI-015 (`work/completed/20260705_WI-015_ife-end-to-end-demo/findings.md`). The canonical `models/` were left untouched; all adaptations live in the staged copies under `exploration/stellarator_e2e/`. These are candidates to file upstream against `sysml-codegen`.

**Outcome: the chain closed.** Every teax-executed channel matches the pure-Python oracle (`verify_stellaris.py`) bit-exactly (rel dev < 1e-9), reproducing the WI-018 forward pass: V=564 m³, fusion 2700 MW, net 575 MWe, LCOE $250.95/MWh, total capital $9.783B, magnet-dominated.

## Finding 8 (new) — EXPOSE alias wires inconsistently by binding name

A plant attribute aliasing a calc output (`attribute p_th : Real = pb.p_th;`) wires to the `pb` module output **only when the consuming calc input has the same name** (`in p_th = p_th` — the volume-scaled accounts, correctly rescued by self-named binding). The four BOP accounts bind `in power = p_the` / `in power = p_et` (a different name than the alias), and the alias→`pb` edge is not formed: codegen emits a **dangling `mfe_plant__MFE_Power_Plant__p_*` reference that V11 does not flag**, teax rejects it at validation, and it plants required-but-unminted fields in the `SystemDesign` schema.

- **Impact**: silent — passes codegen, fails at teax. A V11 coverage blind spot.
- **Harness workaround (glue-1)**: repoint the 4 BOP `power` inputs to the real `pb` output channels; fill the spurious schema fields.
- **Upstream fix candidate**: V11 should flag dangling EXPOSE-alias references, and alias wiring should be by source, not by matching consumer-input name.

## Finding 9 — strict-mode `assert constraint` now aborts (vs WI-015 finding 6/7)

Newer codegen strict mode (INV-2) actively **resolves** `assert constraint` actuals and **aborts** when an actual is a plain design attribute (e.g. `beta_ok.beta`), rather than silently dropping the constraint as in WI-015. Constraint execution is Stage-4 scope (needs the constraint-execution epic), so the staged copies have the 5 `assert constraint` blocks commented out to emit.

- **Status**: constraints not emitted (as expected for Stage 2), but now **fatal-if-present** rather than ignored.
- **Note**: this is the seam the constraint-execution epic fills — once constraints execute, these blocks come back and produce verdicts as data (demo Stage 4 / Success Criterion 2).

### Addendum (2026-07-19, WI-027) — the constraint-exec epic does NOT close #9 for this package. **File upstream to sysml-codegen.**

WI-027 tried to un-strip the five asserts and regenerate at `constraint-exec-epic @ 512786c` (the branch the IFE acceptance ran). Two distinct gates block it; the IFE package hit neither because its constraint operands are calc outputs / free no-default inputs and it has no cross-part capital-rollup bridge.

**Gate A — INV-2 refuses literal-valued design-attribute actuals (the original #9, unfixed at 512786c).** `beta_ok`/`tbr_ok`/`wall_load_ok` bind design attributes carrying literal defaults (`beta = 0.0276`, `beta_limit = 0.05`, `wall_load_limit = 4.05`, `tbr = 1.074`, `tbr_floor = 1.05`) directly as constraint actuals. The strict resolver synthesizes no entry point for a literal-valued design attribute → `dependency_backtracker.py:62` hard-aborts `capture_snapshot` before any snapshot is written (`constraint_lowering.py:290 resolve_actual`). Evidence: `.orchestrate-logs/wi027_probe/probeA.log`.
- *Workable in-model fix (owner-ruled 2026-07-19, representation-only):* route each literal-valued design attribute through a passthrough calc (`calc def 'Scalar Value' { in v; out value = v; }`, `calc beta_val : 'Scalar Value' { in v = beta; }`, assert reads `beta_val.value`). **Proven to resolve Gate A** — a deferred capture then carries all five facts with the rewired actuals correct (`.orchestrate-logs/wi027_probe/probeA_deferred.snapshot.json`, 5 usages). This is a model rewiring, not an upstream fix; recorded for the demo.

**Gate B — constraint lowering is architecturally incompatible with the V11 capital-rollup bridge (new; the real upstream item).** Even with Gate A fixed, the package cannot both emit constraints and use the sanctioned V11-bridge deferred-placeholder pattern (finding 4). Two sub-facts, both proven:
- `extend_graph_with_constraints` runs a **whole-graph** V11 coverage check (`constraint_lowering.py:1350`) that hard-fails on the 3 unrelated capital-rollup keys (`contingency__direct_subtotal`, `indirect__direct_cost`, `lcoe_calc__total_capital`) — the exact keys `bridge_v11_generate.py` fills at *generation*, not capture. So lowering-ON capture aborts (`V11 coverage violations in extended graph: [...]`). Filling those 3 placeholders on the graph does clear coverage (`uncovered AFTER placeholder fill: []`, `.orchestrate-logs/wi027_probe/probe_forcelower.py`) — but there is no capture-time bridge hook, and the from-snapshot lowering (`graph_rebuild.py:211`) also runs *before* the bridge fills placeholders.
- A lowering-OFF capture succeeds and carries the facts, but stamps `grandfathered_off` and records **no occurrence table**; a later offline force-lower then dies `FrozenOccurrenceIndexCorruptionError` ("owner ... absent from the frozen occurrence table"). The occurrence table and V11 coverage are only produced together during a *fully-covered, lowering-ON* capture — which the bridge pattern structurally prevents.
- *Upstream fix candidate:* scope the constraint-lowering V11 check to the constraint-added inputs only (beta/tbr/wall_load — all covered), not a re-check of pre-existing unrelated offenders the harness bridges; or run the check after entry-point bridging. Until then, a whole-plant package that relies on the V11 bridge cannot emit constraints.
- *In-repo alternatives, both out of WI-027's scope:* give `direct_capital`/`total_capital` placeholder defaults in the model so the graph is V11-covered at capture (touches the finding-4 capital-rollup region, spec Out-of-Scope), or fix the cross-part feature-chain rollup upstream (finding 4 itself).

## Confirmed still-present from WI-015

- **Finding 4 (cross-part capital rollup)**: `powercore/bop/direct/total = Σ subsystem.capital_cost` is a feature-chain in a CalcDef output — "not supported". Harness sums the per-account module outputs and re-runs contingency/indirect/LCOE (glue-2). In the staged model, `direct_capital`/`total_capital` were converted to plain inputs so the package emits.
- **SC-4 (name sanitizer)**: no longer needed — the package emits with no quoted/space names. The WI-015 sanitizer is dead code for this model.

## Reproduce

`source /home/reid/1cfe/fusion-tea/.env` (SYSIDE_LICENSE_KEY) → `sysml-codegen snapshot` → `uv run python bridge_v11_generate.py` (from the sysml-codegen dir) → run `run_stellaris.py` with the pipeline-spike exec venv. See the WI-018 codegen agent report for exact paths.

## Finding 10 (2026-09-07, WI-044) — a preserved AUTO_IMPLEMENTED stencil goes stale when only its expression and inputs change

`sysml-codegen generate --smart-regen --preserve-handwritten` decides whether to keep a `handwritten/<pkg>/<calc>_impl.py` by its **output** signature. When a calc def's `out` set changes (WI-044: `'MFE Radial Build'` +`r_coil_centre`, `'Plasma Geometry'` +`A`), the stencil is regenerated (`Regenerated: 2`, a `handwritten/backup/` dir created and sealed in). When a calc def's **expression and input set change but its outputs do not** (`'Conductor Peak Field'`: four new formals, three new intermediates, `B_peak = B_axis_in * peak_ratio_in * bore_norm`), the old stencil is reported `Preserved` and kept verbatim — its body still `return (inputs.B_axis_in * inputs.peak_ratio_in)`, silently ignoring the new inputs. The module wrapper's "Calculation Specification" docstring shows the new expression; the impl the wrapper calls computes the old one. Nothing fails: the package seals, executes, and returns the pre-change number.

- **Impact**: silent wrong arithmetic after an interface-preserving expression change. Caught at WI-044 only because the design predicted the off-design values before execution and the plan asked for the generated body to be read (design risk 1).
- **Harness handling (WI-044 phase 3)**: delete the stale stencil and regenerate (`New: 1, Preserved: 69, Regenerated: 0`); a checker over every AUTO_IMPLEMENTED impl compares its "SysML Expressions" block to its module's "Calculation Specification" (48 checked, 0 stale after the third pass). Not hand-patched: the stencil is the tool's content.
- **Upstream fix candidate**: preservation should key on the expression digest (or the full interface, inputs included), not the output signature alone; and `--preserve-handwritten` should never apply to AUTO_IMPLEMENTED stencils at all — they carry no hand-written content to preserve.
- **Evidence**: `work/active/WI-044_magnet-chain-sees-coil-bore/evidence/regen_output{,_2,_3}.txt`; plan § Phase 3 record.

## Finding 11 (2026-09-08, WI-047) — an unbound defaulted formal takes a bound formal's parameter name by slot position

On the exact route, a calc def whose formals are `(a_in, b_in, k_B_in = <default>, p_exhaust_in)` — an **unbound defaulted** formal declared *before* bound ones — renders two distinct inputs to one parameter name and generation refuses:

```
SI_RENDERING_COLLISION: distinct inputs on 'stellarator_09__stellaris__vacuum' render to one parameter name
```

A monkeypatched projection showed why: the unbound defaulted formal `k_B_in`, declared fourth of six, was matched **by slot** and took the name of the bound formal `p_exhaust_in`. The refusal is the good case. The bad case is the one this class of bug threatens — a projection that matches by position rather than by name can silently bind a value to the wrong parameter wherever the slots happen to line up and the names never collide.

- **Impact**: refused generation here; silent parameter aliasing is the latent risk. Every landed calc in this package happens to keep its defaulted formals last, which is why no predecessor hit it.
- **Harness handling (WI-047 phase 1, deviation 4)**: `k_B_in` moved to the last formal position; generation then succeeds (91 module wrappers, 76 stencils). The convention "defaulted formals last" is now load-bearing and is stated in the calc's model text.
- **Upstream fix candidate**: match formals to bound arguments by **name**, never by declaration slot; and if a slot match is kept as a fallback, refuse when a slot match and a name match disagree rather than preferring the slot.
- **Evidence**: `work/active/WI-047_fuel-divertor-vacuum-flows/plan.md` § Phase 1 record, deviation 4; the scratch generation probe recorded there.

## Finding 12 (2026-09-13, model-viz) — `calc_expressions` is documented as preserved as-is but carries the doc comment appended as its last entry

The snapshot's `calc_expressions` list is documented as the calc's expression lines "preserved as-is" (`sysml-codegen/src/sysml_codegen/extraction/data_models.py:80`), but the extractor appends the doc comment to the list (`extraction/extractor.py:175-180`): as `"\nDocumentation:\n" + doc_comment` when formula lines exist (64 of 65 non-empty lists on the stellarator snapshot) and as `"See documentation:\n" + doc_comment` when none do (1, `calendar`). The same text is also serialized in `doc_comment`. A consumer that renders both fields shows the documentation twice, and a consumer that counts formula lines over-counts by one.

- **Impact**: display only; no generated number is affected. The model-viz viewer (`.project/active/model-viz/design.md` D7) compensates by recognising a last entry that ends with the doc comment and labelling it as a repeat, rather than dropping it. That compensation is a workaround for this defect, not a contract the viewer should rely on.
- **Upstream fix candidate**: stop appending the doc comment to `calc_expressions`; keep it only in `doc_comment`. If a rendered "Documentation:" block is wanted for some consumer, put it in a separate field. After the fix, the viewer's repeat note simply never fires.
- **Evidence**: `.project/active/model-viz/design-review.md` DR-M3 and the fixture probe in `design.md` Appendix A (SHA-256 `c9f6e2a5…ce393`).
