# Brief — pre-execution review of the comparison basis and study configuration (T-004)

You are a fresh non-author reviewer with no inherited conversation. Read only the files named here. Do not load the goal runbook, the trail or other goals. Do not execute the package. Do not edit anything except your one output file: `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/pre-execution-review.md`. Budget: about 12 tool calls; a reply of at most 400 words. Verdict: `PASS`, `FINDINGS` (list each as correct-before-execution or note) or `OWNER_GATE` (a decision only the owner can make). If named evidence is missing or the budget cannot establish coverage, return the specific missing evidence and uncertainty without a passing verdict.

## The exact question

A study of the economics of a modeled 891 MW fusion-plant alternative is about to execute on a frozen model package. Before it does, check that its comparison basis against the published ARIES-CS economics, its declared tolerances, and its configuration are sound and honest:

1. **Source fidelity.** `evidence/comparison-basis.md` § 1 states the published accounting basis (currency year, net/gross, availability, lifetime, financing, capital scope, fuel, O&M, replacements, decommissioning). Check each `[SOURCE]` cell against the reviewed source boundary `exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/source-evidence/source-boundary.md` and, where that file cites a page, against the page images `work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p707.png`, `lyon-p709.png`, `lyon-p716.png` (view them; they are the original evidence). Report any cell the source does not support as stated.
2. **Derivations.** Check the `[DERIVED]` arithmetic: 40 full-power years / 0.85 = 47.06 → 47 (integer required); event count at 40 and 47 calendar years with life 2.907407 FPY at 0.85 (interval 3.42048 years; the WI-091 rule is n = max(0, ceil(N / interval) − 1)); the event price factor 75,000,000 / 72,231,350; O&M 77.6 × 0.14 × 7,446,000 = 80,893,344; the fluence-scaled life 5 × 1468.361 / 1948.8 = 3.7673; the recuperator bound (balanced counterflow NTU = ε/(1 − ε): 0.8 → 4, 0.95 → 19; capacity rate × 1700/1400).
3. **Tolerances and materiality.** § 3 must be fixed before execution and phrased so it cannot be relaxed to accept an observed residual. Say whether it is.
4. **Configuration honesty.** `exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/config.json` (`axes` and `designs`): every design that substitutes a published quantity (the ladder `diag-L*`) must be labelled a diagnostic; no design may tune toward 77.6 USD2004/MWh; every axis must be sensitivity-framed; no axis may set installed equipment from operating demand (the model requirement MR-7: a supplied equipment choice stays supplied; an inadequate selection is reported as a failed check, never resized); the adverse controls (`adverse-*`) must stay in the set; the sensitivity values must match § 4 of the comparison basis. Report any mismatch.
5. **Comparison discipline.** The independent alternative (`alt-canonical-*`, `alt-unscaled-*`) must never take a published electricity or cost total; the only substitution route is the labelled `source_finance` branch (`source_net_power` axis) and the ladder. Confirm or report.

## Entry files

- `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/comparison-basis.md` (all sections).
- `exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/config.json`.
- `exploration/aries_integrated/studies/20260922-aries-integrated-lcoe/source-evidence/source-boundary.md` and the three page images above.
- `work/completed/20260922_WI-091_aries-integrated-lifecycle-cost/design.md` § "Exact financial convention and equations" (event-count rule, CRF, noncapital composition).
- `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/equipment-cost-audit.md` § "Inconsistencies and proposed smallest corrections" (origin of the recuperator, cycle-side and PbLi bounds).
- `modeling_project/REQUIREMENTS.md` § MR-7 (the requirement text).

## Exclusions

Do not assess scientific feasibility, Q1 or the physical result (net 891 MW is fixed by a replay you are not asked to redo). Do not propose new price data. Do not run anything.
