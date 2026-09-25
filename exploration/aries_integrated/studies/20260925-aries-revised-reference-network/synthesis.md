# Executor synthesis — 20260925-aries-revised-reference-network

[AGENT] Executor reading by the round-2 coordinator; not an independent administrator reading. Every number is a native output in `results/cases.json`; the ledger `results/attribution.md` is presentation arithmetic on those outputs.

## What the study set out to do

Run the revised source-conditioned reference cases on the WI-092 package, which represents the published exchanger network (blanket-helium stage first, PbLi and divertor-helium stages in parallel on a supplied split) while reproducing the original series closure bit-exactly as mode 0. Keep the original failing case and the round-1 series cases as controls, measure the network step at every position in the change order, sweep the supplied split, test the steady candidates at 0.8 recuperation, bracket cycle flow, and study a separately named resized-compressor alternative.

## What it found

- The network fixes the mechanism round 1 identified (series order feeding the PbLi stage pre-heated helium): at C3 it removes 41.1 MW of the 151.0 MW shortfall with no hardware change, and at C2 48.9 MW. It does not remove the rest at the 1600 kg/s convention with 0.95 recuperation, because the blanket-helium stage then binds: the whole cycle flow enters that stage at 309 °C and can only be heated to 452 °C against a 456 °C helium hot inlet, so 53.5 MW of the helium duty and 56.4 MW of the PbLi duty stay unremoved at the 0.85 split, and no split between 0.5 and 0.98 does better than 107.2 MW (0.90).
- Steady, all-checks-satisfied source-conditioned cases exist in two families only: 0.8 recuperation at 1600 kg/s (net 759.886 MW, either arrangement, identical outputs because with all heat removed the arrangement no longer matters), and the declared resized-compressor alternative at 0.95 recuperation with 1700 kg/s and the network (net 891.003 MW, gross 1143.013, efficiency 0.3907, turbine inlet 628 °C; compressor demand 1667 MW on a 1700 MW rating). The series arrangement needs 1800 kg/s for the same (net 803.563). These are declared operating or hardware choices the source does not state.
- Nothing reaches the reference. The best steady point is 110 MW gross and 109 MW net short of 1253 / 1000, and at that point every megawatt of the gap is the thermal-efficiency difference (0.391 against 0.43), which is the turbine-inlet difference (628 against 708 °C). With the published duties the network cannot reach 708 °C at any split: the PbLi stream leaves at 655 °C at the 0.85 split and mixes with a cooler divertor stream; even starving the divertor caps the PbLi stream at 731 °C while leaving 149 MW unremoved. This quantifies, inside the model, the source-reading Q1 that the published temperatures, duties and arrangement cannot all hold.
- Attribution from the original 796.005 MW: input corrections +46.7 MW (C3), the network +29.4 MW alone or +37.0 MW on C3 (order interaction +7.6 MW), combined +83.7 MW to 879.693 MW, still not steady; the steady choice then costs −119.8 MW (0.8 recuperation) or gains +11.3 MW (resized compressor at 1700 kg/s).

## Framing verdict per axis

All axes stay sensitivity-framed as declared. No boundary was searched and no optimum is claimed; the split's broad low between 0.80 and 0.90 is a sampled observation, and the 0.85 default was fixed at design time and is not the best sampled value.

## Constraint structure

Seven of 27 points satisfy every evaluated check. `heat_removal_ok` fails in 18 (every 0.95-recuperation case at 1600 kg/s in either arrangement, the two controls, one starved-divertor case and the series 1700 kg/s case); the compressor screen fails only in the two inherited-rating cases at 1700 and 1800 kg/s, retained as adverse points and not relabelled. The resized-compressor cases pass because their rating was declared, not because anything was sized automatically.

## Findings carried forward

#1 (helium-stage bound is the remaining thermal mechanism), #2 (resized 1700 kg/s network alternative is the best steady point; a declared hardware change), #6 (the remaining 110 MW is the efficiency shortfall at a heat-limited turbine inlet; the published state is unattainable with the published duties, Q1), #5 (order interaction accounted), #3 (arrangement is irrelevant once all heat is removed). #4, #8, #9 are declared seams; #7 is a process note on the verifier's relative rule for difference channels.

## What the record does not support

Reproduction of the ARIES operating point; an optimum split, flow or recuperation; any hydraulic or control statement for the branches; a cost conclusion for the resized alternative; prediction credit for the supplied fusion power, arrangement or split.

[AGENT correction, 2026-09-25, round-2 review] "the arrangement no longer matters" and "identical outputs" apply to the plant-ledger and cycle-state outputs; exchanger-stage channels differ between the arrangements. "Needs 1700 kg/s" means 1700 suffices and 1600 does not; the threshold between them was not bracketed. Mechanism 2 of the unmet heat is bounded by a missing-input range, not corrected.
