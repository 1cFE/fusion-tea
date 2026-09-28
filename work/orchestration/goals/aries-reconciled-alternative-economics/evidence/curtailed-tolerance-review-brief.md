# Brief — focused review of an absolute comparison tolerance declaration (T-004 retry)

You are a fresh non-author reviewer with no inherited conversation. Read only the files named here. Do not execute the package. Write exactly one file: `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/curtailed-tolerance-review.md`. Budget: six tool calls; a reply of at most 300 words. Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; if the budget cannot establish coverage, return the missing evidence without a passing verdict.

## The exact question

A study's all-point verification refused the channel `aries_integrated_plant__lifecycle_accounts__evaluate__curtailed_feed` because the stored value is exactly 0.0 and the independent oracle gives 6.8e-15 kg/year (relative deviation 1.0 against a 1e-9 relative rule; no absolute tolerance declared). The author proposes an absolute tolerance of 1e-9 kg/year on four channels (`curtailed_feed` and `external_shortfall` under `lifecycle_accounts__evaluate__` and `source_lifecycle_accounts__evaluate__`). Check: (1) that the difference is the floating-point evaluation-order class the declaration describes (a max(a − b, 0) of two equal ≈ 139 kg/year sums), by reading how each side computes it: the package's `exploration/aries_integrated/native_completions/equipment/annual_selected_fuel_impl.py` and the lifecycle completion under `exploration/aries_integrated/native_completions/` (find it with `grep -rl curtailed exploration/aries_integrated/native_completions/`), against the checker's `exploration/aries_integrated/studies/lifecycle_oracle.py` and `lifecycle_bindings.py`; (2) that 1e-9 kg/year is at or above the observed differences and below any accounting meaning, and that the declaration relaxes no other channel and no verdict; (3) that the four channels are the complete class (are there other max(·,0) difference channels of the same two quantities?); (4) that the basis text is accurate and the process (retain attempt 1, amend the manifests, re-run indicators and preflight, re-execute and compare bit-for-bit, verify) matches the reviewed precedent `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/unmet-tolerance-declaration.md` and its review `unmet-tolerance-review.md`.

## Entry files

- `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/curtailed-tolerance-declaration.md` (the proposal) and `t004-verify.log` (the refusal).
- The completions and oracle files named above.
- `exploration/aries_integrated/studies/manifest.json` § `absolute_tolerances` (the existing six entries' format).
- The precedent declaration and review named above.

## Exclusions

No model or package edits; no execution; no assessment of the study's economics.
