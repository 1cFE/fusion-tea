# Round 2 review — fresh reviewer

HEAD reviewed: `53702a4b`. Verdict: **FINDINGS** (none blocking; three correct-before-use, two notes).

## Checks

1. Native evidence — PASS. `results/cases.json`: `network-c3-0.85` unmet 109.876 (He 53.514, PbLi 56.362), net 879.693; `resized-compressor-1700-network-0.85` net 891.003, 0 of 14 verdicts failing; `combined-c3-partition` net 842.732, unmet 151.002; `network-original-0.85` net 825.414; full-precision interaction 83.6874 − (46.7265 + 29.4088) = 7.552. `attempt-comparison.json`: 27 cases, 14,877 channels, worst absolute difference 0, inputs and verdicts equal. `verification_summary.json`: outcome `pass`, 27 sampled rows, 364 channels, 14 verdicts re-derived.
2. Helium stage — PASS. `he_secondary_out` 725.565 K against `he_hot` 729.15 K (3.585 K approach); `he_transferred` 1195.054 against `he_coolant` delivered 1248.568 (53.514 short, equal to `he_unmet`). The record's statement holds.
3. Goal and strategy fidelity — PASS. One package re-pin (`6828df18`) and one study (`352ecee4`); `nominal-source-assumed` stored at 796.005 / 158.726 with `full_numeric_map_equal` true on all 27 cases; migration report: 27 mode-0 replays all `verdicts_equal`, sampled entry 546/546 channels at relative 0; design review r2 PASS precedes T-002; resized cases labelled "declared alternative" in record, ledger and answer; `network-c3-1700/1800-0.85` retained with the compressor screen violated; ratings set to demand rounded up, nothing to 1000.
4. Task scopes — FINDING (F3). T-004's written scope says "no … live-manifest change"; the tolerance amendment to `studies/manifest.json` is recorded as a reviewed decision, not named as a scope deviation. T-003 starting before T-002's review carried a declared void condition; T-004's 1700 kg/s addition to the strategy's 1800 is inside its written scope.
5. Retry classification — PASS. `integration-attempt1.log`: BLOCKER, `undeclared dependency read: /packages/teax-simkit` (an empty TEAx root); attempt 2 CANDIDATE. `t004-verify-attempt1.log`: `c0009` = `network-c2-0.85`, `he_unmet` store 2.028448680648353 vs oracle 2.0284486773855406, relative 1.609e-9; both execute logs 27/27.
6. Tolerance discipline — PASS. Declaration → fresh review PASS → manifest amended (exactly six entries: two inherited plus the four unmet channels at 1e-7 MW) → re-execute and verify. `materiality-budget.md` has one commit (`581e3c1a`), no diff since, clean tree.
7. Discovery rows — PASS. `#1`–`#9` present (DISCOVERY_LOG lines 300–308), dispositions match record § 15; none `unrouted`.
8. Reading and dispositions — FINDING (F2). The synthesis follows the record. Plant-level channels (net, gross, turbine inlet, efficiency, `mixed_outlet` to 1e-10) are identical within the `c3-minus-recuperator` / `network-c3-eps0.8-0.85` pair and the two 1800 kg/s resized cases, but 19 of 551 outputs differ in each pair (divertor stream and secondary out, divertor hot, capabilities, terminal differences, `network_mode_used`).
9. Learning delta — see rulings.
10. Answer completeness — FINDING (F1). Every required section is present (§ 2–12; ledger by reference); neither the non-steady network case nor the resized alternative is presented as a reproduction; net 1000 is stated as not reached. But `answer.md` never states the completion condition's verdict in the goal's words (met / partially answered / unmet); only the trail does.
11. Unsupported claims — F2 and F4.

## Findings

- **F1 (correct-before-use)** — add the explicit completion-condition assessment to `answer.md`. On this evidence "partially answered" fits: unmet heat traced and bounded, net not reproduced, one owner-visible premise (Q1) open.
- **F2 (correct-before-use)** — record § 3 and § 6, finding #3, discovery row #3, the ledger's "identical to the series `c3-minus-recuperator`" and L-006 say "any plant output" / "identical channels". Restrict to plant-ledger and cycle-state outputs; exchanger-stage channels differ.
- **F3 (note)** — trail T-004 return: name the live-manifest amendment as outside T-004's written scope, not only as a decision.
- **F4 (correct-before-use)** — ledger row 2 and answer § 5 label the 158.7 MW discrepancy "corrected" in both parts. Mechanism 2 is removed by inputs the sources do not state (1700 kg/s with a 1700 MW rating, or 0.8 recuperation). Under the goal's four states that is "bounded by a missing-input range" (0 unmet at net 759.886–891.003), not "corrected through an evidence-supported input". The prose is transparent; the label is not.
- **F5 (note)** — "needs 1700 kg/s" (record § 6, L-005): only 1600 (insufficient) and 1700 (sufficient) were run; the threshold was not bracketed.

## Learning-delta rulings

- L-005: accept with F5 wording ("1700 kg/s suffices, 1600 does not; threshold unbracketed").
- L-006: correct per F2.
- L-007: accept (628.2 vs 708 °C; gross gap 109.987 equals the efficiency shortfall in `cases.json`).
- L-008: accept.
- L-009: accept (attempt-1 log consistent).

## Not covered

Nothing was run. Not opened: `attribution.json`, `constraint_catalog.json`, the WI-092 spec/design, the prior reviews' bodies, source images. Source science not assessed beyond the contract. Migration replay entries checked by `verdicts_equal` on all 27 and full channel count on one sampled entry only.

Signed: fresh round-2 reviewer, 2026-09-25.
