# Item 4: ARIES discount-rate investigation

Date: 2026-09-29. [AGENT] Focused source and financial-arithmetic investigation for the write-up. Strategy remains for owner discussion. No production model, sealed study, or historical goal record changed.

## Findings

**The reviewer correctly identified a published 4.35% real operating discount rate in the historical economic methodology. Our claim that ARIES does not publish its rate was too broad and should be corrected.** The supplied paper concerns a 1990 comparison, not the later ARIES-CS reference itself. The registered ARIES cost documentation independently confirms the rate in the ARIES methodology and distinguishes it from construction financing and the fixed-charge rate. The retained ARIES-CS source says it inherited the 1990s financing assumptions, but its exact calculation has not been reconstructed here.

**Changing only the rate in our calculation does not recreate $77.6/MWh.** It reduces the quoted diagnostic from $59.313 to $54.657/MWh. A broader financial-method alignment is needed before claiming that the published result is reproduced. The reviewer's reproduction may use that broader method; their worksheet was not supplied, so its inputs and arithmetic remain unverified.

## Source verification

### Reviewer-supplied source

J. G. Delene, *Updated Comparison of Economics of Fusion Reactors with Advanced Fission Reactors*, CONF-901007--2, presented October 7–11, 1990. [OSTI PDF](https://www.osti.gov/servlets/purl/6570291). Downloaded original SHA256: `7fd518a6942dd261faa09d6c332bfe0fd3a33282e8357d09ac61d8958c3e9032`.

Table 1 on PDF page 3 and its clearer repeated presentation table on PDF page 12 distinguish real rates (parentheses) from nominal rates. Visually verified [PDF page 12](discount-rate-evidence/delene-p12.png); [text extraction](discount-rate-evidence/delene-p12.md):

| Quantity | Nominal | Real, inflation-adjusted |
|---|---:|---:|
| Cost of money during construction | 11.35% | 6.05% |
| Effective cost of money / discount rate | 9.57% | 4.35% |

This comparison uses a 30-year levelization period, 1990 cost year and 75% availability. Those assumptions should not be copied wholesale into the later ARIES-CS comparison. The paper's discussion describes the operating cost of money as adjusted for tax deductibility of debt interest.

### Existing ARIES reference in this repository

L. Waganer, *ARIES Cost Account Documentation*, UCSD-CER-13-01. Registered at [SOURCE_INDEX](../../../../knowledge/SOURCE_INDEX.md:80). Original [PDF](https://aries.pppl.gov/LIB/REPORT/ARIES-ACT/UCSD-CER-13-01.pdf) downloaded for page verification; SHA256 `dbf5fe5b4607465301cf3abdd9f77b72d8924c7bba1963b9cc92d6e47e4706c5`, exactly matching the registered original.

Printed page 85, Table 31, explicitly lists 4.35% constant-dollar discount rate, 6.05% construction cost of money and 9.65% annual fixed-charge rate, with a 30-year economic life. The surrounding discussion covers ARIES II–IV through ARIES-AT and explains the tax/depreciation methodology. These are distinct financial quantities. Visually verified [page 85](discount-rate-evidence/waganer-p85.png); [text extraction](discount-rate-evidence/waganer-p85.md). The model's simpler capital-recovery formula does not reproduce that methodology merely by using its discount rate.

The retained [Lyon ARIES-CS page 709](../../../../work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p709.png) says the capital multiplier retains the high borrowed-capital interest rate assumed in ARIES 1990s studies. This supports pursuing the historical methodology; it does not independently specify all the inputs used for the later $77.6/MWh result. [Page 716](../../../../work/active/WI-088_aries-source-budget-cost-contribution/evidence/lyon-p716.png) confirms the published 77.6 and year-2004 cost basis.

## Financial diagnostic

The [calculation script](discount-rate-evidence/check_discount.py) reconstructs the existing discounted-cashflow arithmetic from the sealed study's `results/cases.json`. It first checks both our alternative and the supplied-source-capital comparison at each stored rate (0%, 3%, 5%, 8%, 10%): ten comparisons agree within `2.85e-14 USD2004/MWh`. It then evaluates 4.35%. [Machine-readable results](discount-rate-evidence/discount-diagnostic.json) include the input-file digest and limitations.

| Financial-only diagnostic | USD2004/MWh |
|---|---:|
| Existing quoted alternative, 5% for operations and construction | 59.313031 |
| Same calculation, 4.35% for operations and construction | 54.656691 |
| Same alternative, 4.35% operating and 6.05% construction rate | 56.522117 |
| Supplied source capital and 1000 MW, 5% operating rate | 53.058054 |
| Supplied source capital and 1000 MW, 4.35% operating rate | 49.542942 |

These are diagnostics, not newly executed native studies or independently reproduced ARIES costs. They retain the existing 47-year horizon, dated replacement schedule and other conventions. The split-rate calculation still uses our midpoint construction approximation. The supplied-source-capital branch adds no second construction charge. O&M in the quoted diagnostic is derived from 14% of the published $77.6 itself, which prevents calling agreement an independent reproduction. None of these cases implements the historical tax/depreciation fixed-charge method.

Replay from repository root:

```bash
.codex-test/run python .project/active/write-up/discount-rate-evidence/check_discount.py
```

## Recommended resolution

- [AGENT] Correct the source claim and acknowledge the missed reference. The registered ARIES financial documentation already contained the relevant distinction.
- [AGENT] Keep $59/MWh explicitly attached to our 5% convention if it remains in the article. If discussing a rate-only change, report about $55/MWh at 4.35% as a diagnostic, not a repaired ARIES reproduction.
- [AGENT] Replace the suggestion that an unknown rate explains the unresolved comparison with the actual remaining issue: different financial methods and incomplete reconstruction of the source calculation.
- [AGENT] Before asserting reproduction of $77.6/MWh, obtain the reviewer's calculation and compare capital scope, fixed-charge treatment, economic life, construction financing, O&M, replacements and denominator. A match that uses cost components inferred from $77.6 itself is not independent verification.

[AGENT] Wording ratified by owner, 2026-09-29:

> We get about $59/MWh using our assumed 5% discount rate. Historical ARIES costing uses 4.35%, though other financial assumptions also differ.

Decision: [AGENT] Editorial correction ratified by owner, 2026-09-29. Use the short wording above; retain the detailed reconciliation and $55 diagnostic in supporting notes. No further study is required for this correction. Article edit pending; exact reproduction of the published $77.6/MWh remains unverified.
