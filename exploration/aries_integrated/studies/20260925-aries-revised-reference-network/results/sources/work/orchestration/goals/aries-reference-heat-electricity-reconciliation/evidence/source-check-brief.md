# Review brief — source readings, consistency question and materiality budget

You are a fresh, independent reviewer with no prior context on this work. Do not load project instructions, goal trails or model code; read only the files named here. Budget: at most 14 tool calls and a 600-word return. Write your return to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/source-check-review.md` (paths relative to `/home/reid/1cfe/fusion-tea`). If you cannot establish a verdict within the budget, name the specific missing evidence and stop without a passing verdict.

## Exact question

Three things to check, each against the original page images (view the PNGs; do not rely on text extractions):

1. **Source readings.** In `evidence/reference-case-contract.md` (same directory as this brief), check every value graded `[SOURCE]` or `[SOURCE-FIG]` in sections 2, 3 and 4 against the page image it cites. Confirm or correct: Lyon Table IV (2436 fusion, 2916 thermal, 1253 gross, 1000 net) and the p708 text (170 + 27 + 55 = 253 MW); Lyon p703 text and Fig. 18 (80/20 split, 116%, 90% of pumps/BOP returned as thermal, 43%, 20%/80% of gross); Lyon p717 (55 MW = 50 balance of plant + 5 cryogenic); Raffray Table II (2496 blanket, 1444 PbLi net of 111, 1192 He including 141 friction + 111, 3261 kg/s, 156 MW, 386/430/456 °C, 451/738 °C); Raffray Table III (3 stages, 30 °C, 0.89, 0.93, 0.95, 15 MPa, 3.5, 0.045, 35 °C, 0.43, 0.39); Raffray Table V (573/700 °C, 186 MW including 23.6 alpha loss and 24 friction, 283 kg/s, ≈ 27 MW); Raffray Fig. 12 topology (series blanket-He exchanger, then parallel PbLi and divertor-He exchangers, cycle He 355 → 707 °C) and Fig. 14 caption (2365 MW).
2. **Consistency question Q1** (contract section 6). Check the arithmetic and the reasoning: can a counterflow network with the cycle helium entering at 355 °C and a heat-capacity rate of about 8.3 MW/K absorb ≈ 1150–1190 MW from blanket helium whose maximum temperature is 456 °C? State whether the claim "the published temperatures, duties and arrangement cannot all hold at once" follows from the page evidence, and whether the 90% returned-heat rule and the 43% constant are correctly characterised as systems-code constants rather than exchanger results.
3. **Materiality budget** (`evidence/materiality-budget.md`). Is each budget justified by the printed precision and purpose stated? Is any source ambiguity being hidden inside a tolerance rather than listed as a bounded item? Would a tired engineer accept these numbers as the line between "explained" and "still open"?

## Page images (view each once)

- `work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p708.png` — Lyon Table IV and p708 text
- `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/lyon-p703.png` — Lyon p703 text
- `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/lyon-p704.png` — Lyon Fig. 18
- `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/lyon-p717.png` — Lyon p717 text (50 + 5 MW)
- `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p734.png` — Raffray Table II
- `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p736.png` — Raffray Figs 12/13
- `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p737.png` — Raffray Table III, Fig. 14 and net-efficiency text
- `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/raffray-p741.png` — Raffray Table V

## Exclusions

Do not evaluate the SysML model or the generated package; do not run anything; do not judge whether the model should be changed. Do not read any other file.

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`, then numbered findings (each: what the page shows, what the contract says, severity: blocking / correct-before-use / note), then one paragraph each on Q1 and the budget. Sign as "fresh source-check reviewer, 2026-09-25".
