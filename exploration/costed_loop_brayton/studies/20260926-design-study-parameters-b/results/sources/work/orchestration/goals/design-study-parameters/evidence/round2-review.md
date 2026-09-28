# Round 2 review — goal `design-study-parameters` (fresh, bounded)

Fresh reviewer, 2026-09-26. Read only the brief's entry files; eight tool calls; nothing executed except a read-only `sha256sum` of `snapshot.json` (disclosed here).

**Verdict: FINDINGS.** One `correct-before-close` (a ledger statistic disagrees with the check file it cites); the answer itself holds on all five questions.

## 1. Directions applied

All five are applied in substance. (1) The answer's status line names the 1e-6 K class a verification tolerance on three calculated margins, re-verified on every point with every verdict re-derived; the record addendum carries the owner's "never permission" wording. (2) No "lever" phrasing survives in answer, ledger or passage; § 2, § 3 and § 6 state the ruled conclusion. (3) The § 2 table orders net, Δnet, nonfuel, tritium, total; the prose leads with +171 MW and −38 USD/MWh, names −408 as the assumed price spread over more electricity, and prices "74 MW" as 0.95 USD/MWh of added capital contribution (§ 3, § 6, passage). (4) § 4 resolves the condition as missing as a check, with source and leading cases. (5) § 1 keeps 426.6 MW (C-1) distinct from 423.1 MW (ARIES nominal); the only other "423" is a temperature.

## 2. Numbers

Checked over 30 cells of the § 2 table against readout § 2, § 6 and the check file. All six rows' net, Δnet, unmet, total, tritium and residual match at the stated rounding. Nonfuel = total − tritium − deuterium − supply reproduces 133.1, 95.0, 95.5, 98.6, 91.6, 85.1 and agrees with the readout's plant-side column. Δtritium (−408.0, −403.0, −369.3, −445.0, −520.4), the § 1 breakdown (7.5 = 3.274 + 1.685 + 1.574 + 1.270 − 0.254), +40 % and −29 % all recompute. The electricity-only best's 981.3 and S6's 85.1 are derived, since those cases are absent from § 6, and are consistent with their totals.

## 3. Return condition

§ 4 states the condition (return at `T_comp_in` 561.9 K so the 573.15 K blanket inlet holds), its source (`stellarator_plant.sysml:1257-1260`, Moscato) and its status (missing as a check, not waived), as the check file does. Residuals +48.8 / +0.7 / +8.6 / +13.6 / −0.5 / +3.0 K and bypass fractions 18.8 / 0.3 / 3.9 / 6.0 / 1.4 % match. "163 of 163" is quoted as found. The addendum does not mention the condition; the trail's disposition (§ 15 immutable; answer § 4 and L-008) explains that.

## 4. Seal

The addendum states pass on 272 cases, 244 channels, 9 verdicts under `verification-manifest.json` = executed manifest plus the three classes only, executed manifest unchanged, snapshot sha256 `d84c7dac2fea…74c1`. Trail T-006 quotes the same prefix. `snapshot.json` exists, `study_id` is `20260926-design-study-parameters`, and its on-disk digest equals the addendum's full digest.

## 5. Scope

By the trail's own statements: T-006 additions only (new record files, addendum, three classes on the live manifest, evidence script); T-007 evidence only; T-008 goal artifacts only; the native-state check reports no committed `results/` edit and preservation exact. Not verified against git.

## Findings

- `correct-before-close` — `candidate-ledger.md` line 23 says the passing I-R residual "runs 0.4–125 K (median 41 K)"; its cited `return-condition-check.md` says min 0.70 K, median 67.0 K, max 125.4 K. Trail T-007 also says "median … 40.8 K". Align the ledger and trail to the check file, or correct the check file if its `.json` shows it is the one in error.
- `note` — "0.95 USD/MWh" and "+29 MUSD / 87.5 MUSD" (answer § 3, § 6, passage) are not in readout § 2 or § 6; scaling the § 6 overnight difference (43.45 MUSD) by the starting point's capital contribution gives about 0.92. Cite the channel behind 0.95.
- `note` — the § 2 Checks cell for the electricity-only best reads "heat_removal_ok"; the readout lists that as the failed check. Write "fails heat_removal_ok".
- `note` — the ledger's title still says "round 1" though it carries the round-2 addition.

## Missing evidence / uncertainty

The 3.18 → 4.45 TWh annual energy and the 0.95 USD/MWh figure are outside the named sections; the TWh pair is consistent with one capacity factor (0.851). Scope rests on the trail's self-report and the cited preservation check, not a diff. I did not read the check's `.json`, so I cannot say which side of the median discrepancy is right.
