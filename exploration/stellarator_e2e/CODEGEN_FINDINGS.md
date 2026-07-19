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
