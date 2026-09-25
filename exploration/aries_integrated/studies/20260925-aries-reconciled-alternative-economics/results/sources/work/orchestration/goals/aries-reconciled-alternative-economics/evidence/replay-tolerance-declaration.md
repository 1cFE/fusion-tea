# Replay tolerance declaration — T-001 (written before the replay runs)

[AGENT] 2026-09-25. The four sealed cases (`resized-compressor-1700-network-scaledflows-0.85` and `resized-compressor-1700-network-0.85` from `20260925-aries-flow-scaling-check@77098a41`; `nominal-calculated` and `nominal-source-assumed` from `20260925-aries-revised-reference-network@352ecee4`) are re-executed on the live package (executable `f739dbce…`) through the stock route from their exact stored input maps. Expected: bit-exact reproduction, because the package identity, TEAx revision and inputs are unchanged. Declared comparison rule, taken from the WI-092 migration report precedent and the reviewed unmet-heat allowance, and not relaxed afterwards:

| Channel class | Rule |
|---|---|
| Nonzero sealed value | relative deviation ≤ 1e-12 |
| Exactly-zero sealed value | absolute deviation ≤ 1e-12 |
| The four unmet-heat channels (`heat_exchangers__evaluate__unmet_heat`, `__he_unmet`, `__pbli_unmet`, `__divertor_unmet`) | absolute deviation ≤ 1e-7 MW (reviewed allowance, `…/aries-reference-heat-electricity-reconciliation/evidence/unmet-tolerance-review.md`) |
| Verdicts (14 per case) | identical status strings |

Any channel outside its rule is a replay discrepancy and is reported before dependent economic work (a strategy blocker for round 1).
