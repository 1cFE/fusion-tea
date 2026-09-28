# Assets for the Part 4, support 2 write-up (the ARIES test)

Figures for `../aries-model-transfer-outline.md` and its page `../aries-model-transfer-outline.html`, each with the script that renders it. No script evaluates the model: every value is read from a committed study or goal record.

## Figures the markdown uses

| Figure | Script | Source of the data |
|---|---|---|
| `parameter-pressure-ratio.png` / `.svg`, `parameter-flow-boundary.png` / `.svg`, with `parameter-figure-data.json` | `render_parameters.py` | `exploration/costed_loop_brayton/studies/20260926-design-study-parameters-b/results/readout.json` (hash recorded in the JSON) |
| `architecture-nominal-pair.png` / `.svg`, with `architecture-figure-data.json` | `render_architecture.py` | `work/orchestration/goals/design-study-exchanger-architecture/evidence/r3-data/reporting.json` (hash recorded in the JSON) |

These two scripts predate `../figure_style.py` and draw in matplotlib's default font. Run them from the repository root with the project's prescribed launcher, as their docstrings say: `.codex-test/run python docs/write-up/aries-study-assets/render_parameters.py`.

## Figures the HTML page adds or redraws

The page embeds these as inline SVG, drawn in the page's fonts through `../figure_style.py` at the width they are shown. `render_page_figures.py` writes them and then refreshes the copies inside the page, between its `<!-- inline:NAME -->` markers. The markdown's figures above are untouched.

| File | Page figure | Purpose | Source of the data |
|---|---|---|---|
| `page-field-range.svg` | Figure 3 | The field on the plasma axis and at the coils, ARIES against our run, with the conductor model's 20–32 T range | `.project/active/aries-comparison-preparation/post-reveal-investigation/field-audit/receipt.json` (our run); ARIES's 5.70 and 15.08 T as recorded in F-003 of that investigation's `findings.md` |
| `page-how-close.svg` | Figure 5 | Three panels: net electricity of the 891 MW case against ARIES's; its cost with all tritium bought, split into tritium and everything else, against ARIES's; and its cost on ARIES's tritium assumption and conventions at each stored discount rate, against ARIES's published figure | `exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/attribution.json` and `cases.json` (turbine inlet); ARIES's 708 °C as the reconciliation answer cites it |
| `page-pressure-ratio.svg`, `page-pressure-ratio-points.json` | Figure 6 | Redraw of `parameter-pressure-ratio.png`, keeping its rising x-axis so the caption's "right to left" stays true; one SVG group per point, and the JSON that drives the page's explore panel and fallback table | `parameter-figure-data.json` |
| `page-flow-boundary.svg` | Figure 7 | Redraw of `parameter-flow-boundary.png` | `parameter-figure-data.json` |
| `page-power-budget.svg` | Figure 8 | Redraw of the study's `power-budget.png`: electricity for sale, the conversion equipment's own use and the upstream loads of the four supported plants | `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion-b/results/presentation/matched-account-table.csv` |
| `page-cost-contributions.svg` | Figure 9 | Redraw of the study's `whole-cost-contributions.png`, with its eight accounts grouped into four; each group is the account's present value over the present value of exported energy, and the groups sum to the published LCOE (the script asserts it) | the same `matched-account-table.csv` |
| `page-conversion-sensitivity.svg` | Figure 10 | Condensed redraw of the study's `preference-sensitivity.svg`: Brayton's LCOE over steam's for every supported tested case, grouped by the study's own scenario families; threshold-bracket diagnostics and unsupported scenarios are left out | `…/results/presentation/native-ranking.csv` of the same study |
| `page-architecture-pair.svg` | Figure 12 | Redraw of `architecture-nominal-pair.png` | `architecture-figure-data.json` |

Run from the repository root: `uv run python docs/write-up/aries-study-assets/render_page_figures.py`. The page's Figures 1, 2, 4 and 11 are built in HTML inside the page and have no script. Figure 11 is the HTML version of the goal's `evidence/figures/r3-connections.png`; its cycle-helium temperatures are the `secondary_in` and `secondary_out` of cases 216 (series) and 254 (network) in the goal's `evidence/r3-data/thermal.csv`, with the turbine and recuperator-outlet temperatures from `evidence/r3-data/cases.csv`.

The categorical colors (blue, orange, green, and violet in Figure 9) were checked with the dataviz palette validator against the figure plate: every adjacent pair clears the colorblind-separation target. Orange sits below 3:1 contrast against the plate, so every orange mark carries a legend entry or a visible label.
