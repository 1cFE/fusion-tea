# WI-092 report — ARIES parallel exchanger network alternative

[AGENT] Closed 2026-09-25 at the owner's direction ("Close WI-092 separately, provided its implementation acceptance criteria are met", `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/owner-supplement-r6.md`). This report checks each acceptance criterion of [spec.md](spec.md) against the native evidence. Implementation checkpoint `49668453`; re-pin `6828df18`; reviews accepted `4f5991a5`; first study on the package sealed `352ecee4` (record completed `b6d24a64`); second study `77098a41`.

## Acceptance criteria

| ID | Observable acceptance (spec) | Evidence | Met |
|---|---|---|---|
| R1 | The published series-then-parallel network is an explicit alternative closure selectable per case. | `models/library/analyses/integrated_heat_electricity.sysml` `calc def 'Network Heat Driven Closure'` (mode 0 series, mode 1 network, supplied `pbli_split_in`); assembly `heat_exchangers` rebound with `network_mode` (default 0) and `pbli_split_fraction`; mode 1 executed in `exploration/aries_integrated/studies/20260925-aries-revised-reference-network/` (17 mode-1 points) and `…/20260925-aries-flow-scaling-check/`. | yes |
| R2 | With mode 0 every canonical case and the 27 points sealed at `581e3c1a` reproduce all numeric outputs and verdicts. | `evidence/migration-report.json`: 27 sealed points and the four canonical maps replayed, worst relative 0, every verdict equal, 546 → 551 numeric outputs with none removed; fresh implementation review confirmed ("bit-exact per the replay"). | yes |
| R3 | MR-7: the split is a supplied operating choice; no other quantity changes role. | `design.md` § MR-7 role table; fresh design review r2 PASS (`work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/design-review.md`); fresh implementation review PASS, MR-7 compliant on executed evidence (`work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/implementation-review.md`): direction triple at fixed hardware, zero-area case reports unmet heat, rating change moves no thermal output. | yes |
| R4 | Preservation manifest unchanged; isolated Stellaris replay exact; no shared-file edit. | `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/preservation-check-wi092.json` and `preservation-check-delivery.json` (18,725 files unchanged); `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/wi092-stellaris-regression-receipt.json` and `delivery-stellaris-regression-receipt.json` (1,352 outputs and 68 responses exact; original package byte-preserved); only ARIES-only files edited (`build-hashes.json`). | yes |
| R5 | Native graph outputs; stock-route regeneration to a fixed point; live manifest re-pinned; one integration CANDIDATE. | `evidence/generation.log`, `completion-generation.log`, `fixed-point-generation.log`, `census-generation.log`; re-pin `6828df18` (executable `f739dbce…`, semantic `78dd23bf…`; `interface_data.py`, `manifest.json`); `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json` CANDIDATE, all ten gates. | yes |
| R6 | Monotone root problem in mode 1 with bracket, residual and iterations exposed; refusals retained. | `native_completions/network_heat_driven_closure_impl.py` asserts bracket signs, converges within the existing tolerances and cap, exposes `closure_residual` and `iterations`; `evidence/development-cases.json` records the refusals `refuse-split-0`, `refuse-split-1`, `refuse-mode-2` and the zero-area definedness case; oracle self-check worst relative 2.4e-10 (`oracle-self-check.json`). | yes |

## Validation

Scoped validation: L2 105 → 105 diagnostics; L6 493 → 498, the five additions being the pre-existing "unsupported operator" diagnostic on the five new pass-through attributes (`evidence/validation-comparison.json`, `validation-complete.log`).

## Reviews and notes

Design review r1 FINDINGS → r2 PASS; implementation review PASS with four notes, dispositioned in `evidence/implementation-review-notes.md` (the "line for line" wording in the sealed completion docstring and calc-def doc comment is scheduled for the next package edit, not a wording-only rebuild).

## What this item does not claim

No reproduction of the ARIES operating point (goal answer: partially answered); no optimum split; no hydraulic law for the branches; the resized-compressor cases in the studies are modeled alternatives, not a revised ARIES reference (owner ruling, `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/owner-supplement-r6.md`).
