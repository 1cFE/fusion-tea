# Executor synthesis — 20260925-aries-reference-heat-electricity-reconciliation

**Authorship:** written by the study executor (the goal coordinator), not by a cold-record administrator; every number below is in `results/cases.json`, `results/attribution.json` or `record.md`. Snapshot read: `dae3a4652ea16cbba42914e3d7174b27a9d112359a3c88307a316d1a573dba78`.

## What the study set out to do

Quantify, on the unchanged entry package, which inherited inputs account for the source-conditioned case's 158.7 MW unremoved heat and its 796 MW net against the Lyon reference's 1000 MW, one change at a time and combined, with reverse one-at-a-time and a cycle-flow bracket to expose interactions. No model change; no tuning to the published output.

## What it found

1. **The original failure is a PbLi-stage failure.** In `nominal-source-assumed` all 158.726 MW of unremoved heat is in the PbLi stage; the helium and divertor stages transfer everything. The PbLi capacity rate (26860 kg/s × 190 J/kg K = 5.10 MW/K) is below the cycle's (7.27 MW/K at 1400 kg/s), so PbLi cannot be cooled below the cycle helium entering its stage; in the series order that helium has already been heated by the divertor stage (PbLi-stage inlet 494.7 °C, PbLi return 498.8 °C against the published 451 °C).
2. **Conductance is not the limit.** Tenfold UA on all three stages changes unremoved heat by 11.9 MW from the original and 6.1 MW from C3.
3. **Recuperation and cycle flow interact strongly.** The source's 0.95 recuperation alone raises unremoved heat to 398.9 MW (helium stage now limiting too) for +11 MW net; cycle flow 1600 kg/s alone removes all heat for −22.5 MW net (turbine inlet 604 °C). Together with the source divertor flow they give net 877.1 MW with 126.4 MW still unremoved. Forward one-at-a-time net deltas sum to −45 MW; the combined C3 delta is +47 MW.
4. **Accounting alignment to Lyon costs net.** Lyon's itemisation (ignited plasma, 170 + 27 MW pumping, 50 + 5 MW balance of plant and cryogenic) gives auxiliary electricity 252.0 MW against the model's 232.7 MW: −18.3 MW net, +1.0 MW gross.
5. **The source-informed partition is adverse.** Moving ≈ 198 MW from the divertor circuit (700 °C) to the blanket circuits costs 13.7 MW net from the original and 16.8 MW from C2, and raises PbLi unremoved heat to 151.0 MW at C3.
6. **No case reaches the reference.** Largest gross 1128.4 MW (1700 kg/s, compressor rating exceeded, 16.3 MW unremoved) against 1253. The all-checks-satisfied source-conditioned points use 0.8 recuperation at 1600 kg/s: net 773.5 MW (original auxiliaries) or 759.9 MW (Lyon auxiliaries and partition), efficiency ≈ 0.345. At 0.95 recuperation, complete removal needs 1700–1800 kg/s, above the assumed 1600 MW compressor rating (an A6 assumption, not a source value).

## Framing verdict per axis

All eighteen axes were and remain sensitivity-framed. Heat-removal violations are located (0.95 recuperation below 1800 kg/s; every partition/accounting variant at 1600 kg/s) and compressor-rating violations at ≥ 1700 kg/s; these are facts about the run, not boundary claims.

## Constraint structure

Fourteen executing constraints; `heat_removal_ok` violated in 19 of 27 cases, `compressor_capacity` in 6, `balances_ok` in the retained Raffray control only; four cases satisfy every evaluated check.

## Findings carried forward

#7 (series-order PbLi limit; parallel-stage alternative is a model increment for the next round), #8 (0.95 recuperation needs ≥ 1700–1800 kg/s on this package), #10 (the published 43%/1253/1000 chain is a systems constant and the published network cannot deliver it with the published temperatures, per the independently checked Q1). #1–#6 are declared seams; #9 is a process note.

## What the record does not support

It does not support any claim that the reference 1000 MW is reachable or unreachable by this model in general: only that it is unreachable on this package over the studied inputs. It does not establish the physical adequacy of any hardware, the correctness of the partition beyond the source-informed reading, or an optimum cycle flow. It does not contain the topology alternative or the per-circuit Lyon-case comparison values.
