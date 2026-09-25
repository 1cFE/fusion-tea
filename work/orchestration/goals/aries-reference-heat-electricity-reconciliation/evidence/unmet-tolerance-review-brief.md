# Review brief — unmet-heat absolute tolerance declaration (fresh reviewer)

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 10 tool calls and a 350-word return written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/unmet-tolerance-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks, goal trails or other work items. Do not run the model or the verifier.

## Exact question

Is a declared absolute comparison tolerance of 1e-7 MW on the four unmet-heat channels justified by the solvers' termination tolerances, and does it conceal any real disagreement or any verdict difference?

## Entry files

1. `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/unmet-tolerance-declaration.md` — the declaration under review.
2. `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/t004-verify-attempt1.log` — the refusal.
3. `exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py` lines 80–100 — native termination; `exploration/aries_integrated/studies/oracle_entry.py` lines 125–135 — checker root finder.
4. `exploration/aries_integrated/studies/20260925-aries-revised-reference-network/results/cases.json` and `…/oracle-window-scan.json` — recompute for yourself, with one short Python one-liner, the largest absolute store-versus-oracle difference on `aries_integrated_plant__heat_exchangers__evaluate__{unmet_heat,he_unmet,pbli_unmet,divertor_unmet}` over the 27 cases, and list every stored unmet value that lies strictly between 0 and 1 MW (expected: none).
5. `exploration/aries_integrated/studies/manifest.json` — the existing `absolute_tolerances` entries (the precedent declaration for `residual_magnitude`).
6. `.project/active/study-residual-tolerance/review.md` first 12 lines — the precedent review.

## Expected checks

Termination tolerances support the claim that agreement is limited to order 1e-8 MW; the proposed 1e-7 MW exceeds every observed difference with margin and stays below the 1e-6 MW engineering tolerance; only four channels are named and none is a verdict operand within 1e-7 MW of its threshold; the declaration does not touch model inputs, points or package bytes.

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; numbered findings with severities (blocking / correct-before-use / note); the recomputed worst differences; what the review did not cover. Sign as "fresh tolerance reviewer, 2026-09-25".
