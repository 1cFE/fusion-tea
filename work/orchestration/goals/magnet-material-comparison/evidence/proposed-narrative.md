# Proposed narrative: REBCO against Nb₃Sn as a material-choice example

Created 2026-09-29 for goal `magnet-material-comparison`. [AGENT] Proposal for owner review; nothing in the article or its HTML is edited. Every number is from the sealed study `exploration/magnet_materials/studies/20260929-magnet-material-comparison/` (`7836424ca`); case ids are listed under each draft. The category tests T1–T5 are `[AGENT]` tests derived from the owner's article promises, from `.project/active/write-up/magnet-study-evaluation/evaluation.md` § 1.

## 1. Draft paragraph (main-post length)

> **Materials: REBCO at 20 K against Nb₃Sn at 4.5 K.** We gave the same magnet duty, a tokamak-class winding pack at 10 T carrying 87 kA per turn, to two different conductors: a REBCO tape whose performance we take from a measured 20 K field curve, and a Nb₃Sn strand described by the ITER strain-dependent law at 4.5 K. Each is a supplied winding: we choose how many tapes or strands go in, and the model checks current margin, fit in the pack, copper and steel allowances and refrigerator capacity, and prices what we chose. Both fit the pack and pass every check from 8 to 11 T. REBCO's 20 K operation cuts the cold-stage electrical input from 5.8 MW to 1.2 MW, but that is worth about 4 M USD a year, while the tape costs 3.5 G USD against 0.4 G USD of strand. At the 2021 market price of 80 USD/m the REBCO subsystem costs about six times as much per year; the two break even when tape reaches about 11 USD/m. Below that, and only there, REBCO wins. The result is bounded: it says nothing about fields above 14 T, where Nb₃Sn is outside its law and REBCO stands alone, and nothing about the rest of the plant.

Numbers: 87 kA, 5.8 / 1.2 MW, 3.5 / 0.4 G USD, 48.5 / 286.1 M USD/yr ("six times"), 11.25 USD/m from `D-10T-common-P-reference-none-reference-reference`; "8 to 11 T" from the `D-{8..11}T-common-P-reference-none-reference-reference` pairs (all rankable) and the 12 T pair (Nb₃Sn fit −179 mm²); "about 4 M USD a year" is the refrigeration capital and electricity difference (3.6 M USD/yr). "Above 14 T" is the record's status band (Nb₃Sn unsupported from 16 T; 14 T is law-only).

## 2. Draft for Part 4b-style depth (one figure, one table)

> The question a material choice asks is not "which conductor is better" but "at what price, and under which assumptions, does the choice flip." We held the duty fixed and varied one assumption at a time. The sign of the cost difference survived every conductor-law, construction, cryogenic and financing variant; it moved only with the REBCO tape price, and then only at 9–11 T when tape reaches 10 USD/m. The conductor laws matter in a different way: a Nb₃Sn strand at −0.6 % strain, or from a lower production grade, no longer meets its 1.5 K margin with the strands we supplied, so that winding is unranked until more strands are bought, and the break-even price at 10 T rises to 13–18 USD/m. The pack construction rule decides where Nb₃Sn stops fitting (it fails from 12 T in the DEMO envelope under the calibrated CICC rule, and from 18 T under a compact rule), which is why we do not report a Nb₃Sn field limit. Refrigeration, the reason 20 K operation is usually argued for, moves the break-even by less than 7 % at this duty.

Figure: [figures/f5_cost_breakeven.png](figures/f5_cost_breakeven.png) (cost difference and break-even against field, rankable pairs) and [figures/f6_sensitivities.png](figures/f6_sensitivities.png) (tornado at 10 T). Table: [figures/results-table.md](figures/results-table.md). Case ids for the sensitivities: `D-10T-common-P-{variant}-reference-reference` with `offer_kind` reference (fixed hardware) and variant-offer (re-offered); the list and values are in [../answer.md](../answer.md) § Which assumptions determine the preference.

## 3. Does it qualify as a component/material-choice example?

[AGENT] Against the five tests of evaluation.md § 1 (agent-derived from the owner's article promises):

| Test | Verdict | Evidence |
|---|---|---|
| T1 Categorical: different definitions with their own properties, equations or limits | **Pass** | Two conductor definitions in `models/library/analyses/magnet_conductor_alternatives.sysml`: Nb₃Sn ITER-form Jc(B, T, ε) with strain, supply 4.5 K, temperature-margin rule, validity bands; REBCO measured 20 K field shape with exponential temperature law, supply 20 K, operating-fraction rule. Different laws, temperatures, rules and domains, not one law with changed inputs (goal invariant "Comparison"). |
| T2 Matched: same held design, same basis | **Pass** | Same anchor envelope (turns, coils, turn length, turn area), same turn current at each field, same construction rule under common-P and common-C, same cold-load inventory, same refrigerator list, same price year and annualization (contract §§ 2, 4, 6, 7). |
| T3 Designer choice (MR-7): supplied designs evaluated as given | **Pass** | Element counts, areas and refrigerator ratings are inputs; insufficient and generous offers are evaluated alongside and fail or pass as expected (0 of 144 insufficient offers pass acceptance per material). The offer policy is a declared search outside the model; every evaluated design is a fixed input row in `results/cases.csv`. |
| T4 Part 4b fit: uses the combined Stellaris/ARIES library to answer Question 2 | **Fail** | The study runs on an isolated package (`exploration/magnet_materials/`), on an EU DEMO TF envelope, with new library definitions. It does not exercise the combined library, and its Stellaris envelope results are rankable only under the compact construction rule. |
| T5 New to the reader | **Pass** | Part 2 shows one tape, sized and re-sized. This shows two materials, a price at which the choice flips, and refrigeration failing to move it. |

[AGENT] **Assessment: it is a defensible material-choice example, but not a Part 4b Question 2 example.** It passes the categorical, matched, designer-choice and novelty tests with independently checked numbers and retained failures. It does not belong in Part 4b § 4.2 as written, because that slot promises a study on the combined library after the reveal and repair, and this study is not that. Two honest placements:

1. **Main post, "categorical decisions" claim** (`archive/write-up/main-post-draft.md:45,68`, "Material A vs B"): the § 1 paragraph is direct evidence for that claim and can stand next to, or replace, the narrowed conversion paragraph. The conversion comparison remains the combined-library example for Part 4b.
2. **Part 2, after § 2.7.1**: as the material-choice companion to the sizing story, with the § 2 depth draft and the two figures. This is where "the model pushes back" already lives, and the unranked-until-re-offered behaviour continues that theme.

[AGENT] Qualifications the prose must carry, whichever placement is chosen:

- The duty is a tokamak-class envelope (EU DEMO TF), not Stellaris. On the Stellaris turn area, Nb₃Sn under the CICC rule does not fit at any field; a common-construction comparison there is possible only under the compact rule, which the contract labels hypothetical for Nb₃Sn (protection at that copper level is not evaluated).
- The 12 T fit boundary is a construction-rule result. No Nb₃Sn field limit is claimed.
- Economics cover the winding and its refrigeration only; conductor manufacturing is a variant, and joints, leads, structure and power supplies are unpriced.
- Prices are 2021 market figures (Nb₃Sn 8 USD/m, REBCO 80 USD/m) with declared target and volume scenarios; the break-even is the reportable quantity, not the sign.
- The refrigerator cost law is used outside its fitted range at 11 T and above on the DEMO envelope (flagged in the record); its effect on the preference is small.
- Every turn is sized at the peak field with no layer grading, for both materials; a real graded pack needs less superconductor than either offer (contract § 2, record finding #4).
- A pass is a screening pass, not a qualified design: stress, quench beyond the copper allowance, irradiation, AC loss and joint/lead design are not evaluated (contract § 9).
- Forced-flow circulator work and helium inventory are excluded from the cold load and the electricity bill, and the exclusion favours Nb₃Sn; the "5.8 MW to 1.2 MW" sentence is the cold-stage input without them (contract § 6).
- The anchor D turn length (55.6 m) and the cold-load terms are bounded assumptions that scale the totals; the 45/60 m and ×0.5/×2 sensitivities bound their effect on the break-even at under 2 % and −4 % to +7 % (contract §§ 2, 6).
- The 0.7 K nuclear temperature rise is applied to REBCO as a bounded symmetric assumption (contract § 3).

[AGENT] What would make it a Part 4b example: re-anchoring on a combined-library magnet (the WI-098 48 kA capture or the Stellaris reference under a construction rule both materials fit) and executing through that library's package rather than the isolated one. That is a second round with its own pin, not an edit.
