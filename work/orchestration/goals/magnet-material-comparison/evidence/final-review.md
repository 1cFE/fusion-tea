# T-008 final review: answer, narrative and figures against the sealed record

Reviewer: fresh agent, 2026-09-29, brief `evidence/briefs/t008-final-review.md`. I did none of the work reviewed. Ground truth: `exploration/magnet_materials/studies/20260929-magnet-material-comparison/` (record.md §§ 3–6, 13, 15, 17; `results/summary.json`; `results/cases.csv`; `results/case_aliases.json`) and `evidence/comparison-contract.md` r3 §§ 2–9. Nothing was modified, re-run or committed; Python was run only as `.codex-test/run python`. Line numbers below are in the reviewed files as of this review.

## Verdicts

| Artifact | Verdict |
|---|---|
| `answer.md` | **PASS WITH CORRECTIONS** — every quoted number traces to the record; the sign conclusion, the 11.25 USD/m break-even and the sensitivity table are right; nine wording or scope corrections, no blocking finding |
| `evidence/proposed-narrative.md` | **PASS WITH CORRECTIONS** — numbers trace; T1–T5 verdicts are supported except that the tests are mis-graded as the owner's; one factual inconsistency (16 T), one price-label slip, and five qualifications the record requires are missing |
| `evidence/figures/` (README, results-table, data CSVs, F1–F6) | **PASS WITH CORRECTIONS** — every value in every data CSV row and every results-table cell matches `cases.csv` exactly; aliases match `case_aliases.json`; F2–F4 draw supplied windings that fail fit without marking it, and F3 does not mark `green_extrapolated` |

No finding changes the answer's preference, its break-even price or its sign-flip condition.

## Findings

Severity: **blocking** (none) / **correction** (must change before the owner reads it as final) / **note** (worth fixing, does not mislead).

### answer.md

1. **correction** — `answer.md:72` "supplying them raises the break-even at most to 18.4 USD/m". 18.36 is the 10 T common-P value only. Over the 8 rankable variant-offer pairs of the −0.6 % strain variant (anchor D, 8–11 T, common-P and native) the break-even runs 12.82–23.13 USD/m; at 11 T it is 22.96 (common-P) and 23.13 (native). The sentence sits in the same clause as the all-field count "all 8 of that variant's rankable pairs", so it reads as an all-field maximum. Write "at most 18.4 USD/m at 10 T, 23.1 USD/m at 11 T" or restrict the clause to the reference point. `answer.md:7` ("raises the break-even to 13.1–18.4 USD/m") is correct for the reference point but should say so.
2. **correction** — `answer.md:64` Construction row: "Nb₃Sn steel allowance fails; unranked". At `D-10T-common-P-reference-steel_base_layer8_16.24-reference-reference` and `…-steel_no_field_scaling-reference-reference` both `nb3sn.steel_ok` and `rebco.steel_ok` are violated. Record § 4: REBCO steel violated in 16 (layer-8) and 26 (no field scaling) cases. Write "steel allowance fails (both materials)".
3. **correction** — `answer.md:44` "both fit under common-C, where all 36 pairs at 8–13 T are rankable and the break-even runs 8.81–17.31 USD/m". Anchor S common-C has 72 declared cases; 36 are rankable (the reference and generous element offers under all three rule families, 6 per field); the other 36 are the insufficient element offers and insufficient refrigerators, which fail by design. 8.81–17.31 is the range over the 6 reference-rule-family reference-offer pairs; over all 36 rankable pairs it is 8.32–20.20 USD/m. Write "36 of the 72 pairs (every reference and generous offer) are rankable; at the reference offers the break-even runs 8.81–17.31 USD/m".
4. **correction** — `answer.md:5` "worth about 3.6 M USD/yr; it is 1.5 % of the conductor purchase difference". 3.56 M USD/yr is 1.48 % of the *annualized* purchase difference (0.08 × 3.014 G = 241.1 M USD/yr) and 0.12 % of the purchase difference itself (3.014 G USD). Insert "annualized".
5. **correction** — `answer.md:5` and `:71` quote the 610-pair break-even range 6.62–24.63 USD/m without saying that 12 of those pairs are at 13 T (Nb₃Sn edge) and 6 at 14 T (Nb₃Sn law-only, `point_class` extension). The maximum 24.63 is `D-14T-common-C-both-temperature-none-reference-reference`, a 14 T extension point that contract § 2 says "has no Nb₃Sn comparator". Over the 592 supported-status pairs the range is 6.62–23.13; edge pairs 14.19–20.35; law-only 16.47–24.63. Either qualify the range or quote the supported-status range and note the rest.
6. **correction** — `answer.md:9` "Above 14 T only REBCO is evaluated". Nb₃Sn is evaluated at 16, 18 and 20 T with status unsupported (540 cases, no verdict); `answer.md:87` says so correctly. Write "supported".
7. **correction** — `answer.md:33–38` table: the 12 T and 13 T rows carry "(+310.4) (14.78)" and "(+345.5) (17.39)" with no legend for the parentheses. Contract § 2 gives a non-fitting design "no cost ranking and no break-even price"; § 8 defines preference only over rankable pairs. Add a legend line ("parenthesized values are recorded for the pair but carry no ranking, contract § 8") or replace them with "—". `results-table.md` already carries the equivalent note in its column key.
8. **correction** — `answer.md:44` and `:90` present the anchor S common-C ranking, and `:9` "ranking is possible only under the compact construction rule", without contract § 4's label for that pairing: common-C is "hypothetical for Nb₃Sn: protection at this copper level is not evaluated and is labelled". Carry the label wherever anchor S common-C results are quoted.
9. **note** — `answer.md:9` "Nb₃Sn needs 0.97–1.48 times as many element-metres (three times the conductor mass)". The length ratio is the 8–11 T range; the mass ratio 3.02 is the 10 T value, and runs 2.28–3.50 over 8–11 T. Give both as ranges or both at 10 T.
10. **note** — `answer.md:5` "inside the range both conductors support (8–11 T on the EU DEMO TF envelope)". Both laws are supported to 12 T (Nb₃Sn ≤ 12.2 T); 8–11 T is the rankable range under common-P because Nb₃Sn fails fit at 12 T. Say "where both fit and are supported".
11. **note** — `answer.md:5` "the cheaper subsystem under every checked assumption except the REBCO price". On fixed hardware eleven variants leave the 10 T pair with no ranking at all (acceptance, steel or capacity fails); the statement is true wherever the pair is rankable, which `:7` and `:72` explain. A four-word qualifier here would close the gap.
12. **note** — `answer.md:9` "on the Stellaris envelope neither material fits under common construction". Common-C is also a common construction; write "under the common CICC rule (common-P)".
13. **note** — Answer-contract coverage (check D). The contract's bounded assumptions (anchor D turn length 55.6 m and cold-load terms, contract § 2 and § 6; no layer grading, § 2; symmetric 0.7 K nuclear rise for REBCO, § 3) are not named as bounded in `answer.md`. The sensitivities that bound their effect are in the table (turn length −3 % to +5 %, cold load ×0.5/×2 −5 % to +7 %); one sentence in "What the comparison does and does not establish" naming them and pointing at those rows would satisfy "where a dimension is only bounded, the answer says so".

### proposed-narrative.md

14. **correction** — `proposed-narrative.md:3` and `:19` "The category tests T1–T5 are the owner's" / "Against the owner's five tests". In `.project/active/write-up/magnet-study-evaluation/evaluation.md` § 1 the table is introduced "[AGENT] From these, a component example must pass five tests", derived from the owner's article text. The tests are agent-graded; the promises they were derived from are the owner's. Regrade: "[AGENT] tests derived from the owner's article promises (evaluation.md § 1)".
15. **correction** — `proposed-narrative.md:13` "decides where Nb₃Sn stops fitting (12 T in the DEMO envelope under the calibrated CICC rule; 16 T under a compact rule)". Under P, Nb₃Sn fits through 11 T and first fails at 12 T (−178.6 mm²). Under C it fits through 16 T (+1042.2 mm²) and first fails at 18 T (−1822.9 mm²). The two numbers use opposite conventions. Write "fails from 12 T under the CICC rule and from 18 T under the compact rule" (or "fits to 11 T / to 16 T").
16. **correction** — `proposed-narrative.md:13` "the break-even price rises to 13–18 USD/m" is the 10 T common-P range (13.07–18.36); at 11 T it reaches 23.1 (finding 1). Add "at 10 T".
17. **correction** — `proposed-narrative.md:7` "At today's 80 USD/m". The contract label is "80 USD/m, the 2021 market", and the narrative's own qualification at `:39` says "2021 market figures". Write "at the 2021 market price of 80 USD/m".
18. **correction** — `proposed-narrative.md:36` "the fair comparison there needs the compact rule for both materials". Contract § 4 labels common-C hypothetical for Nb₃Sn (protection at this copper level not evaluated). "Fair" overstates; write "a common-construction comparison there is possible only under the compact rule, which the contract labels hypothetical for Nb₃Sn".
19. **correction** — § 3 qualifications list (`:34–40`) is missing five the record or contract requires: (a) every turn sized at peak field, no layer grading, conservative and equal for both, real graded packs need less superconductor (contract § 2 stated limits; record finding #4); (b) a pass is a screening pass, not a qualified design: stress, quench beyond the copper allowance, irradiation, AC loss and joint/lead design are not evaluated (contract § 9); (c) forced-flow circulator work and helium inventory are excluded and the exclusion favours Nb₃Sn (contract § 6), which bears directly on the "5.8 MW to 1.2 MW" sentence; (d) anchor D turn length and cold-load terms are bounded assumptions that scale totals, bounded by the 45/60 m and ×0.5/×2 sensitivities (contract § 2, § 6); (e) the 0.7 K nuclear rise applied to REBCO is a bounded symmetric assumption (contract § 3).
20. **note** — `proposed-narrative.md:7` "Below that, and only there, REBCO wins" is true at the 10 T reference point the paragraph describes; across pairs the break-even runs 6.62–24.63 USD/m. Fine as written if the paragraph stays anchored at 10 T.
21. **note** — T1–T5 table: T1, T2, T3 and T4 verdicts are supported by the cited evidence (contract §§ 2–7; record § 1 names the isolated package `magnet_materials_tea` at `exploration/magnet_materials/`; 0 of 144 insufficient offers pass acceptance per material, verified). T5 depends on Part 2's content, which I did not read.

### figures

22. **correction** — F2, F3, F4 draw Nb₃Sn common-P at 12, 13 and 14 T (fit fails: −178.6, −788.3, −1495.6 mm²) and REBCO common-P at 13 and 14 T (−385.1, −883.9 mm²) with status markers only. Nothing on the figure says these supplied windings do not fit the envelope; contract § 2 calls such a design "not a winding that exists at this duty", and record § 3 marks every such pair non-rankable. Add a fit-fail marker (hollow or crossed) or a footer line naming the fields, as F5 does with hollow markers and listed reasons.
23. **correction** — F3: `green_extrapolated` = 1 for both materials at 11 T and above on anchor D (rating 50 kW, outside the Green fit range 0.01–35 kW; record finding #6). The flag is in `data/f3_refrigeration.csv` but not on the figure, whose efficiency and capital panels are exactly the extrapolated quantities. Mark those points or state it in the footer.
24. **note** — F1 omits anchor D common-C (README says left panel is common-P and native). `answer.md:44` and `:86` cite anchor D common-C fit (both through 14 T; Nb₃Sn to 16 T), which no figure shows.
25. **note** — F4 left panel: the "fraction rule" label is overdrawn by the REBCO series. F5: the anchor D native series lies under common-P (values differ by ≤ 0.17 USD/m) and is not visible; F5's "REBCO 10 USD/m (volume)" label overlaps the shaded strand-price band. Cosmetic.
26. **note** — `results-table.md` counts paragraph and every number in the twelve rows match `summary.json` and `cases.csv` (see computations). The README's alias statement (every native reference case also serves the two `cu_density_material_93.4_100` cases of its field) is verified.

## Computations for the derived numbers

All from `results/cases.csv`, case `D-10T-common-P-reference-none-reference-reference` unless stated. Channel prefix `magnet_subsystem__subsystem__` omitted.

| Quoted | Computation | Result | Verdict |
|---|---|---|---|
| 237.6 M USD/yr difference | 286,144,339.73 − 48,522,166.95 | 237,622,172.78 | matches `pair__cost_difference` |
| annualized = 0.08 × capital + electricity | Nb₃Sn 0.08 × 490,688,948.81 + 9,267,051.05; REBCO 0.08 × 3,485,025,997.11 + 7,342,259.96 | 48,522,166.95; 286,144,339.73 | matches both `annualized_cost` channels |
| capital = superconductor + materials + manufacturing + refrigerator | Nb₃Sn 442.6 + 15.7 + 0 + 32.3 M; REBCO 3456.2 + 17.0 + 0 + 11.8 M | 490.7 M; 3485.0 M | matches `capital_total` |
| electricity = p_in_total × 8760 × 0.8 × 60 | 22.039 MW; 17.462 MW | 9.267 M; 7.342 M USD/yr | matches `annual_electricity` |
| "about 3.6 M USD/yr" refrigeration advantage | 0.08 × (32,337,873 − 11,841,874) + (9,267,051 − 7,342,260) = 1,639,680 + 1,924,791 | 3,564,471 USD/yr | 3.6 ✓ |
| "4.6 MW" cold-stage advantage | 5,795,259 − 1,217,655 W | 4.578 MW | ✓ ; × 8760 × 0.8 × 60 = 1.925 M USD/yr, equal to the electricity difference (shield stage is common) |
| "20.5 M USD" refrigerator capital | 32.338 − 11.842 | 20.496 M | ✓ |
| "1.5 % of the conductor purchase difference" | purchase difference 3,456,202,752 − 442,636,800 = 3,013,565,952; annualized 0.08 × that = 241,085,276; 3,564,471 / 241,085,276 | 1.48 % of the annualized difference; 0.12 % of the difference itself | finding 4 |
| "3.46 G at 80 USD/m; 0.44 G at 8 USD/m" | `sc_cost` / `element_length`: 3,456,202,752 / 43,202,534 = 80.0; 442,636,800 / 55,329,600 = 8.0 | prices confirmed | ✓ |
| break-even 11.25 USD/m | p = ((ann_Nb₃Sn − elec_REBCO)/0.08 − (capital_REBCO − sc_REBCO)) / element_length_REBCO = ((48,522,167 − 7,342,260)/0.08 − 28,823,245) / 43,202,534 | 11.2476 | matches `pair__breakeven_rebco_price_per_m` |
| 31.7 USD/kA·m | 11.2476 / (ic_tape_op 354.83 A / 1000) | 31.699 | matches `pair__breakeven_rebco_price_per_kAm` (basis: tape Ic at the operating point, not turn current) |
| "about six times" | 286,144,340 / 48,522,167 | 5.90 | ✓ |
| "0.97–1.48 times as many element-metres" | Nb₃Sn / REBCO `element_length` at 8, 9, 10, 11 T | 0.967, 1.107, 1.281, 1.483 | ✓ (12 T 1.745, 13 T 2.086) |
| "three times the conductor mass" | `element_mass` ratio at 8–11 T | 2.28, 2.61, 3.02, 3.50 | 10 T only; finding 9 |
| "55.3 million strand-metres (260 t), 43.2 million tape-metres (86 t)" | element_length 55,329,600 / 43,202,534 m; element_mass 260,055 / 86,129 kg | ✓ | |
| 87.17 kA at 10 T; 126.3 km | 104.95 × 10 / 12.04 = 87.168; 142 × 16 × 55.6 = 126,323 m | matches `turn_current` 87,167.8 A and `conductor_length` 126,323.2 m | ✓ |
| anchor S 21.753 m | `conductor_length` / (48 × 308) | 21.7532 | ✓ |
| 30 kW refrigerator both sides | Nb₃Sn `R_equiv_kW` 30.0; REBCO 6.396 / 0.2132 | 30.0 kW | ✓ |
| "totals 22.0 and 17.5 MW; common 16.2 MW" | `p_in_total_MW` 22.039, 17.462; `p_in_shield` 16.244 MW both | ✓ | |
| "cold loads 29.9 vs 29.5 kW; nuclear 16.8 kW" | `q_cold` 29,911 / 29,483 W; `q_nuclear` 16,819 W both | ✓ | |
| sensitivity percentages (table, `answer.md:52–67`) | (be_variant / 11.2476 − 1) for every D-10T common-P variant case, fixed-hardware and variant-offer | all 36 variants and both rule families reproduce the table's values and rounded percentages; rankability and failing checks match, except finding 2 | ✓ |
| "less than 7 %" cryogenic/CRF | largest: cold load ×2 re-offered 11.98 (+6.5 %); crf 0.05 +3.0 %, 0.11 −1.4 % | ✓ | |
| "−30 % to +63 %" Nb₃Sn price / manufacturing | 7.92 (−29.6 %), 18.29 (+62.6 %), 14.55 (+29.3 %) | ✓ | |
| "13.1–18.4 USD/m" after re-offer (10 T) | 13.07, 13.56, 14.51, 16.47, 18.36 | ✓ at 10 T; finding 1 for other fields | |
| "−18 % to −1 %" REBCO-side flips | 9.23 (−18.0 %), 11.15 (−0.9 %), 10.02 (−10.9 %) | ✓ | |
| "26 of 32 cases per variant; all 8 rankable pairs removed" | reference-offer cases per Nb₃Sn strain/grade variant: 32 of 32 fail acceptance (6 already unsupported at 16–20 T); rankable 8 → 0; variant offers restore 8 | consistent with record § 6 wording | ✓ |
| "0 of 144" insufficient offers / refrigerators; generous | insufficient element offers passing acceptance 0/144 per material; insufficient refrigerators passing capacity 0/144; generous offers passing acceptance Nb₃Sn 117/144 (= supported, edge, law-only count), REBCO 144/144 | ✓ | |
| "2222 of 2832 unranked"; "12 of 610 Nb₃Sn dearer" | 2832 − 610; `summary.json` `nb3sn_dearer_cases` = the 12 REBCO-10 USD/m cases at 9, 10, 11 T, common-P and native (6 stored points, one alias each) | ✓ | |
| "at 8 T REBCO stays dearer even at 10 USD/m" | `D-8T-common-P-…price_rebco_10_volume…` +2.097 M; native +1.702 M USD/yr | ✓ | |
| both-rule-family counts | n = `element_length` / `conductor_length`: both-temperature REBCO 293, break-even 13.13; both-fraction Nb₃Sn 403, 10.43 | ✓ | |
| n column of `results-table.md` | `summary.json` `reference_offer_pairs` n equals `element_length` / `conductor_length` for all 48 pairs | ✓ | |
| anchor S common-P fit | Nb₃Sn −57.5 … −625.2; REBCO −48.0 … −532.1 mm² at 8–13 T | ✓ | |
| REBCO native on D "≥ +2237 mm²" | minimum 2237.0 at 20 T | ✓ | |
| common-C on D | both fit at 14 T (+2132.9, +2837.9); Nb₃Sn +1042.2 at 16 T, −1822.9 at 18 T | ✓ | |
| status bands | `status_by_anchor_field`: D 8–12 T supported, 13 T edge, 14 T law-only, 16–20 T unsupported; S 8–12 T supported, 13 T edge; REBCO supported 2832 | ✓ | |
| `green_extrapolated` | 1187 Nb₃Sn, 1129 REBCO; = 1 at D 11 T and above at reference offers | ✓ | |

## Figure spot-checks (check E)

Every row of every data CSV was compared with `cases.csv` by case id and channel (unit scale factors W→kW/MW, m→km, USD→M USD): 76 F1 rows, 20 each F2–F4, 26 F5, 38 F6, 12 results-table rows, 0 mismatches at 1e−9 relative. Named spot rows, five per figure: F1 `D-12T-common-P` Nb₃Sn −178.6 / REBCO +87.8; `D-18T-common-P` Nb₃Sn −7976.1 (drawn at floor, unsupported); `S-8T-common-P` Nb₃Sn −57.5; `S-13T-common-C` Nb₃Sn +119.8 (edge); `D-20T-native` REBCO +2237.0. F2 8 T Nb₃Sn 29,307 km / 234.46 M; 10 T REBCO 43,203 km / 3456.2 M; 11 T Nb₃Sn 75,668 km; 14 T Nb₃Sn 202,243 km (law-only); 16 T Nb₃Sn plotted = 0. F3 8 T Nb₃Sn q_cold 28.16 kW, p_in_cold 5.456 MW, R_equiv 30, capital 32.34 M; 11 T Nb₃Sn R_equiv 50, green = 1; 10 T REBCO R_equiv 6.396; 13 T Nb₃Sn 5.655 MW; 20 T REBCO 1.483 MW (20 T Nb₃Sn plotted = 0). F4 8 T Nb₃Sn fraction 0.7744, Tcs 6.7107; 10 T Nb₃Sn margin 1.5084; 10 T REBCO fraction 0.7981, margin 4.961; 13 T REBCO 0.7998; 14 T Nb₃Sn 0.623. F5 `D-8T-common-P` +171.88 / 9.135 / 22.57; `D-12T-common-P` rankable 0, reason "Nb₃Sn fit"; `D-13T-common-P` reason "Nb₃Sn fit; REBCO fit"; `S-13T-common-C` +203.22 / 17.31; `D-16T-native` plotted 0, reason "Nb₃Sn unsupported". F6 `nb3sn_strain_-0.6pct` variant-offer 18.36 (basis: distinct point); `price_nb3sn_5.4` 7.92 (basis: re-evaluated reference, variant offer is an alias); `cold_load_x2` variant-offer 11.98 with the reference case marked non-rankable in `other_case_rankable`; `rule family both-temperature` 13.13; `steel_base_layer8_16.24` 11.25 with reference case non-rankable. `case_basis` agrees with candidate-id identity for all 38 rows. Aliases in all 212 CSV rows agree with grouping by `candidate_id` and with `case_aliases.json`.

Axis labels, units, legends and footers on F1–F6 PNGs match the plotted channels and the README. F5 marks non-rankable pairs hollow with reasons; F6 has no non-rankable bar (all 38 rows rankable). F2–F4 and F3 issues are findings 22–23.

`results-table.md`: all six anchor D rows and the 8, 10 and 13 T anchor S rows checked cell by cell (n, status, acceptance margin, fit margin, cold-stage MW, capital, rankable and reason, Δ cost, break-even); every cell rounds correctly from the recorded value, including the edge cases 9.1353 → 9.14, 1348.52 → 1,348.5, 5.7953 → 5.80, 359.45 → 359.5, 4118.55 → 4,119, 5.6551 → 5.66, 5558.50 → 5,558. The counts paragraph matches `summary.json` (status 1760/352/180/540; rankable 610 = D 574 + S 36 = common-P 266 + native 266 + common-C 78 = matched 592 + edge 12 + extension 6; 598/12; −12.18…+483.44 median 206.36; 6.62–24.63 median 11.25).

## Contract and invariant discipline (check C)

- (a) Nb₃Sn field limit: none claimed; `answer.md:86` and `proposed-narrative.md:13,37` disclaim it. Finding 15 is an internal inconsistency, not a limit claim.
- (b) Plasma, reactor redesign, plant LCOE: none claimed; `answer.md:88` excludes them.
- (c) Fit failure or unsupported status as a material verdict: none; both files name the construction rule and the law's validity flags. F5 lists "Nb₃Sn unsupported" as a non-rankable reason without a fit verdict, consistent with contract § 2.
- (d) Agent choice as owner decision: finding 14 (T1–T5 mis-graded as the owner's). Every other paragraph in both files carries `[AGENT]`.
- (e) Ranking a non-rankable pair: none ranked. Parenthesized values in the answer table (finding 7) and the inclusion of 6 extension-point pairs in the 610-pair range (finding 5) are the two places to tighten.
- (f) Price labels: `answer.md` uses 80 market / 30 target / 10 volume and Nb₃Sn 8, band 5.4–13.5 throughout. `proposed-narrative.md:7` "today's 80 USD/m" is finding 17.

## Not checked

- The SVG files (PNGs viewed only) and `render_figures.py` (not executed; the data CSVs were verified against `cases.csv` instead).
- The source checks (`check-nb3sn.md`, `check-rebco-cryo-cost.md`, `contract-review.md`) and the oracle verification (record § 13) are taken as recorded, not re-run.
- Record § 4 counts other than those the answer quotes (26/32, 0/144, 117/144, steel 32/16 and 20/26, capacity 32 and 60 m 4/2, rankable counts) were not recomputed.
- The conductor-definition constants (`answer.md:17–18`) and construction-rule constants (`:86`) were checked against contract §§ 3–4, not against the SysML or the sources.
- Whether Part 2 already shows what the narrative calls new (T5), and whether `main-post-draft.md:45,68` reads as the narrative describes.
- `results/cases.json`, `oracle_scan.json`, `results/native/` and `snapshot.json` (machine-local or not needed for the checks above).
- Nothing under `knowledge/holdout/` (except nothing needed there) and none of the barred paths in the clean-room screen were opened.

## Recheck — 2026-09-29 (after corrections to answer.md, proposed-narrative.md and figures/)

Same reviewer, same rules. Only the changed material was rechecked; the sections above are unchanged. Every re-rendered data CSV row (F1 96 rows including the new anchor D common-C series, F2–F4 20 rows each with the new `fit_pass`/`fit_margin_mm2` columns, F5 26 rows) was compared again with `cases.csv`: 0 mismatches at 1e−9, aliases unchanged and correct. F6 and `results-table.csv` are byte-unchanged. F1, F3 and F5 PNGs viewed; F2, F4 and F6 PNGs not re-viewed (their CSVs and the README description were checked instead).

### Findings 1–19 (answer and narrative)

| # | Resolved | New wording checked against the record |
|---|---|---|
| 1 | yes | `answer.md:74` "at most 18.4 USD/m at 10 T and 23.1 USD/m at 11 T (12.8–23.1 over the variant's eight re-offered pairs at 8–11 T)": the −0.6 % strain variant-offer pairs give 12.82, 12.99, 15.11, 15.28, 18.36, 18.52, 22.96, 23.13 USD/m; correct. `:7` now says "at the 10 T reference point"; correct. |
| 2 | yes | "steel allowance fails (both materials)"; matches `nb3sn.steel_ok` and `rebco.steel_ok` violated at both 10 T steel-variant reference cases. |
| 3 | yes, one note | "36 of the 72 declared pairs … 8.81–17.31 at the reference offers … (8.32–20.20 over all 36)": counts and both ranges correct. Note: the 36 rankable pairs are the 18 reference element offers with the reference refrigerator plus the 18 generous offers; the 18 reference element offers paired with the insufficient refrigerator are non-rankable, so "every reference and generous offer" reads loosely. The parenthetical "insufficient offers fail by design" covers it if "offers" is read to include refrigerators. |
| 4 | yes | "1.5 % of the annualized conductor purchase difference (… 241 M USD/yr at 0.08)": 0.08 × 3,013.6 M = 241.1 M USD/yr; 3.564 / 241.1 = 1.48 %; correct. |
| 5 | **partly — one correction remains** | `answer.md:5`: "across the 592 rankable pairs where Nb₃Sn is inside its law's supported band the break-even price runs 6.62–23.13 USD/m, **median 11.25**". The range is correct (592 pairs, min 6.62, max 23.13). The median of those 592 pairs is **11.13** USD/m; 11.25 is the median of all 610 (`summary.json`). Second clause, "(6.62–24.63 over all 610 rankable pairs, the highest values being the 13 T edge and 14 T law-only pairs under common-C)": only two pairs exceed 23.13, both 14 T law-only common-C (`D-14T-common-C-both-temperature-…-reference-reference` 24.63 and `…-generous-reference` 24.49); the 12 edge pairs (13 T, anchors D and S, common-C) run 14.19–20.35 and lie inside the supported-status range. Write "median 11.13" and "the values above 23.13 are two 14 T law-only common-C pairs". `answer.md:73` ("6.62–24.63 including the 13–14 T edge and law-only common-C pairs") is correct as an inclusion statement. |
| 6 | yes | "Above 14 T only REBCO is supported" (`:9`); `:89` "evaluated at 16–20 T so that its unsupported status is recorded". |
| 7 | yes | Legend line `:40` cites contract §§ 2 and 8; § 2 says a non-fitting design "gets no cost ranking and no break-even price", § 8 defines preference over rankable pairs only. Correct. |
| 8 | yes | `:9`, `:46`, `:93` carry "hypothetical for Nb₃Sn (protection at that copper level is not evaluated)", matching contract § 4. |
| 9 | yes | "2.3–3.5 times the conductor mass over 8–11 T": 2.28, 2.61, 3.02, 3.50; correct. |
| 10 | yes | "where both conductors are supported and fit the envelope (8–11 T … under common construction)". |
| 11 | yes | "under every checked assumption that leaves the pair rankable, except the REBCO price". |
| 12 | yes | "under the common CICC rule (common-P)". |
| 13 | yes | New bullet "Bounded, not measured" (`:92`): turn length 45/60 m "less than 2 %" (+1.5 %, −0.5 % fixed, +0.5 % re-offered) and "60 m fails capacity until re-offered" (both capacity checks violated at fixed hardware) correct; cold load ×0.5/×2 "−4 % to +7 %" (−2.5/−3.6 %, +5.0/+6.5 %) correct; 0.7 K rise cites § 3 (contract § 3 REBCO temperatures, "bounded assumption, applied symmetrically") correct; no layer grading cites § 2 (stated limits) correct; circulator exclusion favouring Nb₃Sn cites § 6 correct; screening-pass list cites § 9 and matches its "not evaluated" list. Four items are counted and four are listed. |
| 14 | yes | `proposed-narrative.md:3` and `:19` now "[AGENT] tests derived from the owner's article promises", matching evaluation.md § 1's own grade. |
| 15 | yes | "fails from 12 T … and from 18 T under a compact rule": first failing fields under P and C on anchor D (−178.6 at 12 T; −1822.9 at 18 T, +1042.2 at 16 T). Correct and now on one convention. |
| 16 | yes | "the break-even price at 10 T rises to 13–18 USD/m" (13.07–18.36). |
| 17 | yes | "At the 2021 market price of 80 USD/m", the contract § 7 label. |
| 18 | yes | `:36` "possible only under the compact rule, which the contract labels hypothetical for Nb₃Sn". |
| 19 | yes | Five qualifications added (`:41–45`): no layer grading (contract § 2, record finding #4) correct; screening pass with the § 9 list correct; circulator/helium exclusion favouring Nb₃Sn and tied to the 5.8 → 1.2 MW sentence (§ 6) correct; turn length and cold-load terms bounded, "under 2 % and −4 % to +7 %" (§§ 2, 6) correct per finding 13; 0.7 K rise symmetric (§ 3) correct. |

### Findings 22–25 (figures)

| # | Resolved | Check |
|---|---|---|
| 22 | yes | F2–F4 CSVs carry `fit_pass` and `fit_margin_mm2` matching `area__fit_pass` / `area__fit_margin` for every row; plotted rows with `fit_pass` = 0 are Nb₃Sn 12–14 T and REBCO 13–20 T on anchor D common-P, as the README and footers state. F3 PNG shows hollow markers at exactly those points with the legend entry "hollow: supplied winding does not fit the envelope". F2 and F4 PNGs not re-viewed. |
| 23 | yes | F3 PNG shades 11 T and above on the electrical-input, R_equiv and capital panels (not the load panel, correctly), labelled `green_extrapolated = 1`, with the footer naming the fields and the Green range 0.01–35 kW; matches `refrigeration__green_extrapolated` = 1 for both materials at D 11 T and above. |
| 24 | yes | F1 PNG now draws Nb₃Sn on C for anchor D (dashed blue; +2132.9 at 14 T law-only, +1042.2 at 16 T hollow, −1822.9 at 18 T hollow, 20 T at the floor labelled −14,071 (Nb₃Sn/C)); README updated to three floor points. CSV has 96 rows over six anchor × pairing groups, all matching. Cosmetic: the three floor labels crowd each other at 16–20 T. |
| 25 | yes | F5: the native series is drawn over common-P with a smaller marker and the legend states the closeness; the recorded differences at plotted fields are ≤ 0.165 USD/m and ≤ 1.014 M USD/yr, so "within 0.17 USD/m and 1.0 M USD/yr" is a rounding of 1.014 (say "about 1.0" if exactness matters). The "REBCO 10 USD/m (volume)" label now sits outside the band. F4 PNG not re-viewed. |

Spot-checked re-rendered rows (five): F1 `D-20T-common-C` Nb₃Sn −14,070.9 mm², unsupported, `fit_pass` 0, floor 1; F1 `D-14T-common-C` Nb₃Sn +2,132.9, law-only, `fit_pass` 1; F2 `D-12T-common-P` Nb₃Sn `fit_pass` 0, −178.55 mm², 103,837.7 km; F3 `D-11T-common-P` REBCO `fit_pass` 1, `green_extrapolated` 1, 1.1163 MW, R_equiv 10.660 kW; F4 `D-13T-common-P` REBCO `fit_pass` 0, −385.10 mm², fraction 0.79975. All equal the `cases.csv` channels.

### Final verdicts

| Artifact | Verdict |
|---|---|
| `answer.md` | **PASS WITH CORRECTIONS** — one remaining correction, finding 5 as restated above (`answer.md:5`: median of the 592 supported-status pairs is 11.13, not 11.25; only the two 14 T law-only pairs exceed 23.13, the 13 T edge pairs do not). Everything else applied correctly. |
| `evidence/proposed-narrative.md` | **PASS** — all corrections applied and verified. |
| `evidence/figures/` | **PASS** — data and rendered marking now match the record; the two cosmetic notes above are not corrections. |
