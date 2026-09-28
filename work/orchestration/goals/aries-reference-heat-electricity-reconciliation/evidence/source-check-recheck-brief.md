# Recheck brief r2 — corrective diff and one new reading (same reviewer)

Same reviewer as `source-check-brief.md`; same exclusions. Budget: at most 8 tool calls and a 300-word return, appended to `evidence/source-check-review.md` under a heading `## Recheck r2 — 2026-09-25`.

1. **Corrective diff.** In `evidence/reference-case-contract.md` and `evidence/materiality-budget.md` every change made in response to r1 is marked `[r1]`. Confirm each of your findings 1–9 is addressed or say which is not.
2. **New reading, contract § 8 (addendum).** Check against `work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p708.png` (Table IV: alpha heating 462, radiated 365, SOL 97.0, divertor 98.1 MW), `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/lyon-p704.png` (Fig. 18) and `.../evidence/raffray-p741.png` (Table V). Is the source-informed divertor deposition ≈ 167 MW (98.1 charged + 68.8 nuclear, before friction) and the derived partition setting f_rad = 0.657, exchange fraction 0.0469, a fair reading with its carried approximation stated? Is the model's inherited 385 MW divertor deposition correctly characterised as ≈ 218 MW above the source-informed value?
3. **Study inputs.** The diagnostic study will supply cycle flow 1600 kg/s (a `[DERIVED]` comparison convention from 2916 MW over the 352 K Fig. 12 span at cp 5193, bracketed 1500–2000) and divertor primary flow 283 kg/s (`[SOURCE]` Table V). State whether either is mis-graded.

Return `PASS` or `FINDINGS` with numbered items and severities as before.
