# Answer — economics of the 891 MW reconciled alternative

Goal: `work/orchestration/goals/aries-reconciled-alternative-economics/` (grounded `0f24127c`; replay and interim checks `87e77241`; audit and comparison basis `e8a91dc7`; study sealed `<SEAL>`). Written by the round-1 coordinator on 2026-09-25; formal goal closure is reserved for the owner. Every number below is a stored native output of the sealed study `20260925-aries-reconciled-alternative-economics` (or of the two sealed prior studies it takes its canonical inputs from), a graded source value from the reviewed source boundary, or presentation arithmetic in the study's `results/attribution.md`; nothing is transcribed by hand.

## 1. The question and the short answer

<SHORT-ANSWER>

## 2. The configuration that was costed

[OWNER] The 891 MW configuration is a modeled alternative, not a reconstructed ARIES reference (owner ruling 2026-09-25). It is the stored case `resized-compressor-1700-network-scaledflows-0.85` of the prior goal's flow-scaling study (`exploration/aries_integrated/studies/20260925-aries-flow-scaling-check@77098a41`), replayed bit-exactly on the live `aries_integrated` package (executable `f739dbce…`, semantic `78dd23bf…`, TEAx `8d877460…`, the round-2 CANDIDATE at `4f5991a5`): 551 channels and 14 verdicts identical (`evidence/replay-alternative.json`). Its complete input map, selected equipment, operating demands, heat balance and checks are generated from the sealed store in `evidence/configuration-record.md`. In one paragraph: 2436 MW fusion supplied (source mode; earns no prediction credit); the published series-then-parallel exchanger network (WI-092, mode 1, split 0.85); 0.95 recuperation; 1700 kg/s cycle flow on an explicitly selected 1700 MW compressor rating (demand 1667.033 MW, margin 32.967); Raffray's primary flows and the He/PbLi pump capacities scaled by 2436/2365 as declared mapping values (3359 / 27,666 kg/s, capacities equal to the flows, a supplied choice); divertor flow 283 → 291.5 kg/s on the unchanged 500 kg/s pump; Lyon's auxiliary itemisation (170 + 27 + 55 MW) and ignited plasma; the source-informed deposition partition; every other rating, area, inventory, price and finance input at the WI-090/WI-091 values. Result: all heat removed, turbine inlet 628.2 °C, efficiency 0.3907, gross 1143.013, auxiliary 252.011, net 891.0017 MW, all 14 evaluated checks satisfied. The unscaled-mapping control (`resized-compressor-1700-network-0.85`, net 891.003, Raffray flows and capacities) is carried in every table. Equipment rating and operating power are distinct channels throughout (`configuration-record.md` § 4).

<NUMERIC-SECTIONS>

## 8. Reuse and model changes

- **Reused unchanged:** the WI-092 package and its identity; the WI-090 equipment leaves, screens and the linear selected-quantity law; the WI-091 lifecycle chain and convention F1–F9 (5 % real, six-year midpoint financing once, 40 calendar years, 0.85 availability, dated replacements without the reserve, terminal 10 % and salvage 2 % at year 40, overhaul 5 % at year 20, constant USD2004); the fuel boundary (99 % exhaust recycle inside the loop; `annual_recovery` = new usable feed); the stock study tooling (indicators, preflight, oracle, verifier, executor); the reconciliation composer; the live manifest and the round-2 integration CANDIDATE, reused without re-pin because the package identity is unchanged.
- **Changed:** nothing in the model, the package, the assembly or the library. Two thin study modules (`alternative_economics_support.py`, `alternative_economics_reporting.py`) and one study record were added; the live manifest gained four reviewed absolute comparison tolerances (1e-9 kg/year on the curtailed-feed and external-shortfall channels; `evidence/curtailed-tolerance-declaration.md` and `curtailed-tolerance-review.md`), with the pin, fingerprints and every point unchanged.
- **MR-7:** no quantity became an installed capacity or was derived from demand; the compressor rating and the two pump capacities are supplied choices (the pump capacities equal the operating flows by the mapping's declaration and are disclosed as such); the under-rated compressor and the under-capacity pump stay visible failures in the study; the fixed-budget estimate mode is the disclosed nonresponse, not a hardware-cost law. The recuperator, the cycle-side transport at 1700 kg/s and PbLi pumping have no purchase, rating or screen; they are reported as unresolved costs bounded by declared sensitivities, not represented by invented leaves (audit `evidence/equipment-cost-audit.md`; trail T-002 decision). A recuperator hardware representation (a selected rating with a screen and a carved-out purchase leaf) is a possible follow-up item for the owner; it needs a reference price that no source account supplies.

## 9. Independent reviews

| Review | Verdict | File |
|---|---|---|
| Equipment and cost binding audit (fresh worker, T-002) | 25 items graded; six inconsistencies named with proposed corrections (none applied); no binding change required | `evidence/equipment-cost-audit.md` |
| Pre-execution review of the comparison basis and configuration (fresh, C-001) | r1 FINDINGS (three correct-before-execution, four notes) → r2 PASS on the diff | `evidence/pre-execution-review.md` |
| Curtailed-feed tolerance declaration (fresh, T-004 retry) | <TOL-VERDICT> | `evidence/curtailed-tolerance-review.md` |
| Round-1 review (study reading, dispositions, learnings) | <ROUND-REVIEW> | `evidence/round1-review.md` |

## 10. Stellaris preservation

The entry preservation manifest (`evidence/preservation-entry.json`, 19,552 protected files at `b03fa18e`) passes at entry (`preservation-entry-check.json`) and at delivery (`preservation-check-delivery.json`); the isolated Stellaris diagnostic baseline replays exactly at entry and at delivery (`entry-stellaris-regression-receipt.json`, `delivery-stellaris-regression-receipt.json`: 1,352 outputs and 68 responses, original package byte-preserved). The two prior sealed studies, the WI-092 package, the six shared library files and every frozen record are unchanged; unrelated workspace edits present at entry (`evidence/entry-state.txt`) were not committed.

## 11. Exact replay instructions

All commands from the repository root through the prescribed launcher; the seam and study commands must run under the launcher's own environment (no outer `PYTHONPATH`).

```bash
# Identity: the sealed study at commit <SEAL>
sha256sum exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/snapshot.json   # <SNAPSHOT>

# Replay the canonical configuration and three controls from their sealed input maps (bit-exact expected)
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python work/orchestration/goals/aries-reconciled-alternative-economics/evidence/replay-alternative.py --work /tmp/replay --out /tmp/replay-alternative.json'

# Re-verify every stored point of the sealed store against the package-owned oracle
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m scripts.study.verify --package exploration/aries_integrated/aries_integrated --manifest exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/manifest.json --identity exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/preparation/package_identity.json --store exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/native/20260925-aries-reconciled-alternative-economics.db --sample-size 64 --out /tmp/reverify.json'

# Re-execute the 64 declared points into a fresh record (copy config.json to a new record directory <NEW> with study_id changed accordingly)
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m exploration.aries_integrated.studies.alternative_economics_support prepare --record <NEW> --config <NEW>/config.json'
.codex-test/run bash -c '... alternative_economics_support baseline --record <NEW>'
.codex-test/run bash -c '... python scripts/study/preflight.py gates --package exploration/aries_integrated/aries_integrated --manifest <NEW>/manifest.json --groups <NEW>/axes.json --identity <NEW>/preparation/package_identity.json --baseline-result <NEW>/preparation/baseline_result.json --out <NEW>/preparation/preflight_results.json'
.codex-test/run bash -c '... alternative_economics_support execute --record <NEW> --integration-return work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/integration-attempt2/integration_return.json'
uv run python -m exploration.aries_integrated.studies.alternative_economics_reporting <NEW>

# Interim checks (scratch) and the Stellaris baseline in isolation with the entry preservation manifest
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python work/orchestration/goals/aries-reconciled-alternative-economics/evidence/interim-checks.py --work /tmp/interim --out-dir /tmp'
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python work/orchestration/goals/aries-reconciled-alternative-economics/evidence/stellaris-regression-delivery.py'
.codex-test/run python work/orchestration/goals/aries-reconciled-alternative-economics/evidence/check-preservation.py --output /tmp/preservation.json
```

## 12. Plain-language explanation for the write-up

<PLAIN>

## 13. Completion assessment, owner gates and next actions

<CLOSING>
