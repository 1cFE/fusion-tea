# Figures and results table for goal `magnet-material-comparison` (T-008)

Everything in this directory is rendered from the sealed study record `exploration/magnet_materials/studies/20260929-magnet-material-comparison/` (committed at `7836424ca` on `goal/magnet-material-comparison`). Nothing here re-runs the model, the oracle or the study, and nothing interprets: labels, units, statuses and case ids only. The coordinator writes the answer.

## Render

From the repository root:

```
.codex-test/run python work/orchestration/goals/magnet-material-comparison/evidence/figures/render_figures.py
```

The script reads only `results/cases.csv` (every declared case, every channel and verdict) and `results/case_aliases.json` (used only to assert that grouping cases by `candidate_id` reproduces the record's alias list). It writes `data/*.csv` and every figure as SVG and PNG (150 dpi). Output is deterministic (fixed SVG hash salt, no dates in metadata): two runs give byte-identical files. Do not edit the outputs by hand; change the script and re-render.

Unit changes are scale factors only: W to kW or MW, m to km, USD to M USD. Colours and chrome follow the dataviz reference palette (Nb₃Sn blue, REBCO orange; pairings in F5 blue, aqua, violet).

## Aliases

522 of the 2832 declared case ids map to an executed point that another declared case id also names (economics-only variants whose variant offer equals the re-evaluated reference, and variants whose value equals the pairing's reference; record § 15 finding #7). Every data CSV carries `candidate_id` (the executed point) and `aliases` (the other declared case ids that name the same point, `;`-separated, empty when none). Every native-pairing reference case plotted here, for example, also serves the two `cu_density_material_93.4_100` cases of that field. The rows of `data/results-table.csv` have no aliases.

## Figures

Each figure carries a title, axis labels with units, a legend, and a footer naming the record id and the pairing, rule family and variant shown. Nb₃Sn status marker shapes are shared: circle supported, triangle edge (12.2–13.5 T), diamond law-only (13.5–14.5 T). REBCO is supported everywhere. A hollow marker means the point carries no verdict or fails a check: in F1 an unsupported evaluation; in F2, F3 and F4 a supplied winding that does not fit the envelope (`fit_pass` = 0 in the CSV; the footer names the fields, Nb₃Sn 12 T and above and REBCO 13 T and above on anchor D common-P); in F5 a non-rankable pair; in F6 a non-rankable bar (none occur).

| Figure | Files | Data file | What it shows |
|---|---|---|---|
| F1 fit | `f1_fit.svg` / `.png` | `data/f1_fit.csv` | Fit margin per turn (envelope − gross area, mm²) versus peak field for both materials, reference offers, reference variant and rule family. Both panels show the pairings common-P, native and common-C (left anchor D, right anchor S). Series are material × construction, because Nb₃Sn on P is the same evaluation under common-P and native, and REBCO on C is the same under native and common-C (the CSV keeps every pairing row); anchor D common-C therefore adds one Nb₃Sn-on-C series and no new REBCO series. Zero line drawn. On anchor D the three Nb₃Sn points below −5000 mm² (18 T −7,976 on P; 20 T −29,328 on P and −14,071 on C; all unsupported) are drawn at the axis floor with their value and construction (`drawn_at_axis_floor` = 1). |
| F2 inventory | `f2_inventory.svg` / `.png` | `data/f2_inventory.csv` | Superconducting element length (km) and superconductor purchase cost (M USD2021) versus field, anchor D common-P reference offers, both materials. Hollow markers: the supplied winding fails fit (CSV `fit_pass`, `fit_margin_mm2`). |
| F3 refrigeration | `f3_refrigeration.svg` / `.png` | `data/f3_refrigeration.csv` | Cold-stage load (kW), cold-stage electrical input (MW), capital-equivalent rating `R_equiv` (kW) and refrigerator capital (M USD2021) versus field, anchor D common-P reference offers. The installed cold-stage rating is not a `cases.csv` channel; `R_equiv_kW` is what the record stores (equal to the installed rating for the 4.5 K plant and rating × 0.2132 for the 20 K plant at the reference capital basis, contract § 6). Hollow markers: the supplied winding fails fit. The shaded field range on the electrical-input, R_equiv and capital panels is where the recorded `green_extrapolated` flag is 1 (anchor D, 11 T and above, both materials: the listed 50 kW rating lies outside the Green fit range 0.01–35 kW, so efficiency and capital there extrapolate the fitted laws); the footer names the fields. The CSV also carries `capacity_margin_kW`, `p_in_shield_MW`, `p_in_total_MW`, `eta_cold`, `green_extrapolated`, `fit_pass` and `fit_margin_mm2`. |
| F4 margins | `f4_margins.svg` / `.png` | `data/f4_margins.csv` | Operating fraction I/Ic(B, T_conductor) and temperature margin Tcs − T_conductor (K) versus field, anchor D common-P reference offers, with the fraction rule (0.8) and temperature rule (1.5 K) drawn. Hollow markers: the supplied winding fails fit. The CSV carries Tcs, T_conductor, both rule margins, `fit_pass` and `fit_margin_mm2`. |
| F5 cost and break-even | `f5_cost_breakeven.svg` / `.png` | `data/f5_cost_breakeven.csv` | Annualized cost difference REBCO − Nb₃Sn (M USD2021/yr), break-even REBCO price (USD2021/m, with reference lines at 10, 30 and 80 USD/m and the shaded Nb₃Sn strand price range 5.4–13.5 USD/m) and break-even price per kA·m, versus field 8–14 T, for anchor D common-P, anchor D native and anchor S common-C reference offers. Rankable pairs filled; non-rankable pairs hollow, with the failed checks listed in the top panel (`non_rankable_reason` per row). The anchor D native series lies almost on top of common-P (within 0.17 USD/m and 1.0 M USD/yr at every plotted field, computed in the script and stated in the legend) and is drawn on top with a smaller marker. |
| F6 sensitivities | `f6_sensitivities.svg` / `.png` | `data/f6_sensitivities.csv` | Tornado of the break-even REBCO price at anchor D, 10 T, common-P, reference rule family (baseline 11.25 USD/m): one bar per variant (36 variants plus the two symmetric rule families), sorted by size of change. For each variant the bar uses the variant-offer case where the policy re-selected (distinct executed point) and the re-evaluated-reference case where the variant offer is an alias of it; `case_basis` in the CSV states which, and `other_case_id` names the case not used. |

In F2, F3 and F4 the Nb₃Sn evaluations at 16–20 T (status unsupported, no verdict) are not drawn; their rows are in the CSVs with `plotted` = 0. In F5 the 16–20 T extension points, where Nb₃Sn is unsupported and no pair is rankable, are likewise in the CSV with `plotted` = 0. F1 draws every field including the unsupported points, as the brief asks.

## Results table

`results-table.md` is the compact table (anchor D common-P and anchor S common-C, 8–13 T, reference offers). Its numbers are copied from `data/results-table.csv`; its **n** column (elements per turn) is the one value not in `cases.csv` and comes from `results/summary.json` § `reference_offer_pairs`; its counts line is from `results/summary.json`.

## Values not in `cases.csv`

- Elements per turn n (reported in `results-table.md` from `summary.json`; absent from the figures' CSVs, which record element length and mass instead).
- Installed cold-stage refrigerator rating (F3 plots the recorded `R_equiv_kW`; `capacity_margin_kW` is also recorded).
