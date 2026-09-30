# T-008 reporting brief — results table and figures from the sealed study

You are the reporting worker for goal `magnet-material-comparison` in `/home/reid/1cfe/fusion-tea`. You produce a compact results table and the figures from the **sealed, committed** study record only. Every number and every plotted point traces to a recorded case id. You do not interpret beyond labelling; the coordinator writes the answer.

## Inputs

- Record: `exploration/magnet_materials/studies/20260929-magnet-material-comparison/` — `record.md` (§ 3–6, 13, 15), `results/cases.csv` (one row per executed point with labels and every channel), `results/case_aliases.json` (declared case ids that map to the same executed point), `results/summary.json`, `snapshot.json`.
- Contract: `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` (r3) §§ 2, 5, 7, 8 for the meaning of statuses, pairings, rule families, offers and “rankable”.
- Chart guidance: read `references/palette.md`, `references/choosing-a-form.md` and `references/anti-patterns.md` under the dataviz skill directory (`/tmp/claude-1000/bundled-skills/2.1.283/8ff97f8fadd2b230568ca698c3568622/dataviz/`; if absent, find another `bundled-skills/*/dataviz`). Use its neutral palette; label units; no chart junk.

## Deliverables (you own exactly these new paths)

`work/orchestration/goals/magnet-material-comparison/evidence/figures/`:

1. `data/*.csv` — one CSV per figure with the plotted values **and the case_id of every row**; and `data/results-table.csv`.
2. `render_figures.py` — one script (matplotlib; run as `.codex-test/run python …/render_figures.py`) that reads only `results/cases.csv` (plus `case_aliases.json` if needed), writes the `data/*.csv` files and renders every figure to both SVG and PNG (150 dpi). Deterministic; no manual edits to outputs.
3. Figures (SVG + PNG), each with a title, axis labels with units, a legend, and a footer line naming the record id and the pairing/rule family/variant shown:
   - **F1 fit**: fit margin per turn (mm²) versus peak field, anchor D and anchor S as two panels, both materials, pairings common-P and native (and common-C for S); mark statuses (`edge`, `law-only`, `unsupported`) and the zero line. Reference offers, reference variant, reference rule family.
   - **F2 inventory**: superconducting element length (km) and superconductor purchase cost (USD2021) versus field, anchor D common-P reference offers, both materials.
   - **F3 refrigeration**: cold-stage load (kW) and cold-stage electrical input (MW) versus field, anchor D common-P reference offers, both materials; a second panel or table with installed rating and refrigerator capital.
   - **F4 margins**: operating fraction and temperature margin (Tcs − T_conductor, K) versus field for both materials, anchor D common-P reference offers, with the two rule thresholds drawn.
   - **F5 cost and break-even**: annualized cost difference (REBCO − Nb₃Sn, M USD/yr) and break-even REBCO tape price (USD/m, and USD/kA·m on a secondary axis or panel) versus field, for rankable pairs only, anchor D common-P and native and anchor S common-C; horizontal reference lines at 10, 30 and 80 USD/m and a shaded Nb₃Sn price band 5.4–13.5 USD/m (contract § 7). Non-rankable points shown hollow and labelled why (fit, status).
   - **F6 sensitivities**: tornado of the break-even REBCO price at anchor D, 10 T, common-P, reference rule family: one bar per variant, using the variant-offer case where the policy re-selected and the re-evaluated-reference case otherwise (state which in the data CSV); include the strand-grade, strain, margin-rule, REBCO shape/anchor/T*/degradation, steel, copper, efficiency, capital, cold-load, price, electricity, capital-recovery, turn-length and manufacturing variants.
4. `results-table.md` — a compact markdown table (anchor D, 8–13 T, common-P reference offers; and anchor S, 8–13 T, common-C) with per field: Nb₃Sn n, status, acceptance margin, fit margin, cold-stage MW, capital; the same for REBCO; rankable; cost difference; break-even USD/m; plus one line stating the counts by status and rankable pairs from `results/summary.json`. Every row carries its case id(s).
5. `figures/README.md` — what each figure shows, the exact data file, and the render command; note aliases (an executed point may serve several declared case ids).

## Rules

- Read only the record and the contract; do not re-run the model, the oracle or the study; do not modify any existing file; do not commit. Run Python as `.codex-test/run python …`.
- If a value you need is not in `results/cases.csv`, say so rather than deriving it another way.
- Return at most 300 words: what was rendered, the data files, any case labels that were ambiguous, and any figure you could not produce.
