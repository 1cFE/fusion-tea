# Round 1 review: goal `design-study-parameters` (fresh, bounded)

Fresh reviewer, 2026-09-26. Read only the brief's entry files; ran nothing.

**Verdict: FINDINGS** (one `correct-before-close`, the rest `note`). Owner gate G-001 stands as correctly raised and the seal is correctly parked; this verdict does not replace it.

## 1. Numbers

Checked over thirty figures in `answer.md` § 1–§ 4 against `readout.md` § 1–§ 3, § 5, § 6 and `record.md` § 4, § 6: the five named points (net, Δnet, unmet, LCOE, ΔLCOE, plant-side Δ), the S6 pair (671.624 / 991.070; 632.540), the −408 / −38 split, the S1–S5 ranges, the heater inlets and the 52-of-100 count. All stored values match.

- `correct-before-close` — Refused-edge split. `answer.md` § 3, `candidate-ledger.md` and the trail say 55 nonpositive-net points plus one precooler guard. `axis-plan.json` `refused_by_oracle_scan` has 56 keys: 27 nonpositive-net points and the 4,000 / 1.80 guard on each inventory (54 + 2). Fix the answer and ledger; `record.md` § 4 carries the same "55" and is immutable, so note the discrepancy in the trail.
- `note` — `answer.md` § 4 S2 "LCOE −57 to +208": register ×0.5 reaches −110 at the starting point (readout § 5). Should read −110 to +208.

## 2. Limiting check

Follows from record § 4, § 6 and readout § 3: heat removal is the lower edge at 2,000–3,500 kg/s, the compressor rating the upper edge at 2,250–3,000, refusals above 3,250–4,000, grid edges at 2,000 (upper) and 4,000 (lower).

- `note` — "Ridge one step on the failing side at every flow" is supported at 2,250–3,000 (ledger ridge nets exceed the best passing). At 4,000 the lower edge is the grid edge, so no failing step exists; at 2,000, 3,250, 3,500 the failing step's net is outside the named sections. Qualify: "where the boundary lies inside the grid".

## 3. Owner gate

Accurate: one channel, one case, 1.466e-9 relative, 5.32e-10 K absolute, no declared class (gate file and record § 13 agree). Contract § 9 and § 12 applied as written: no class added, `results/` untouched, seal parked, answer marked provisional.

- `note` — "No other deviation" rests on the coordinator's own comparison with no artifact path named (the verifier stopped at the first refusal, no summary file). Name it, or let the post-ruling re-verification stand as the check. The 1e-6 K class was sized with the result in view; the owner should judge it on the stated root-termination basis.

## 4. Scope and dispositions

No package, manifest, library, assembly or index change. The extra anchor is recorded at checkpoint C-001.r1 ("Changes") and declared in `axis-plan.json` `anchors.points.screen-best-passing` with its rule text. Rows #1–#8 in `DISCOVERY_LOG.md` have Home cells matching record § 15.

- `note` — Scope location drift, disclosed but not reconciled: `studies/flow_ratio_config.py` and `studies/study_support.py` (pre-existing) were modified, and the reporting and figure scripts sit at `studies/`, not the record's `results/` or goal `evidence/` as the scope states. One-line scope amendment in the trail.
- `note` — Sighting rows carry the finding summary in the "Disposition" column; joined disposition rows are still to be appended after this review, as the trail says.

## 5. Learnings

L-003, L-004, L-006, L-007 follow from the record and readout.

- `note` — L-001 "at every flow": same qualifier as § 2.
- `note` — L-002 "confirmed on 272 stored points" overreaches; S4–S6 vary numerator terms by design. It holds on the 200 grid points (overnight constant per inventory, readout § 6).
- `note` — L-005 states the remedy ("need declared absolute classes") while G-001 is unruled. Keep the observed fact; make the remedy conditional on the ruling.

## Missing evidence / uncertainty

- The comparison behind "exactly one deviation" has no named artifact in my entry files.
- Turbine inlets 735.8 / 708.0 K, annual energy 4.45 TWh, blanket 3,126 MW, purchases 461 / 812 MUSD and the +29 MUSD exchanger delta lie outside the named sections; the last three are arithmetically consistent with the named overnight figures.
- Physics, economics and package verification not evaluated (excluded by the brief).
