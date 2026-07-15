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

## Confirmed still-present from WI-015

- **Finding 4 (cross-part capital rollup)**: `powercore/bop/direct/total = Σ subsystem.capital_cost` is a feature-chain in a CalcDef output — "not supported". Harness sums the per-account module outputs and re-runs contingency/indirect/LCOE (glue-2). In the staged model, `direct_capital`/`total_capital` were converted to plain inputs so the package emits.
- **SC-4 (name sanitizer)**: no longer needed — the package emits with no quoted/space names. The WI-015 sanitizer is dead code for this model.

## Reproduce

`source /home/reid/1cfe/fusion-tea/.env` (SYSIDE_LICENSE_KEY) → `sysml-codegen snapshot` → `uv run python bridge_v11_generate.py` (from the sysml-codegen dir) → run `run_stellaris.py` with the pipeline-spike exec venv. See the WI-018 codegen agent report for exact paths.
