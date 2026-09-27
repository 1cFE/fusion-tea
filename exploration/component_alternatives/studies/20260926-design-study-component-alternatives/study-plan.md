# Proposed execution plan

[AGENT] This plan implements the reviewed fourth design. It is a proposal until the independent oracle scan fixes the executable window. No physical matching calculation belongs in the study harness.

## Comparison

Compare the selected steam offer with tested Brayton offers at the same reactor heat input, source hot temperature, required return temperature, source pressure and primary circulation law. Both branches receive the same calculated delivered heat, including recovered primary circulation work. Rank only cases that satisfy the implemented checks for the branch being compared. An invalid companion branch does not qualify a matched pair.

The objective is conversion-subsystem cost per net MWh in the common USD2025 scenario. Reactor equipment, fuel and upstream primary circulation are outside this boundary. Report their exclusion with the result. Show a separate common upstream present-value charge sensitivity to expose the different electricity denominators; this does not establish a fuel purchase price or whole-plant LCOE.

## Declared catalog for the oracle scan

| Choice | Values | Purpose |
|---|---|---|
| Reactor heat input | 2500, 2800, 3000 MW | Common source scenarios. These are chosen inputs. |
| Brayton flow | 1500, 1750, 2000, 2250, 2500 kg/s | Operating choice on held equipment. |
| Equal compressor stage ratios | 1.20, 1.35, 1.50, 1.65, 1.80 | Direct choices applied to all three stages. No ratio solve. |
| Cooler service offer | UA triples 25/25/20, 25/25/25, 25/25/40, 30/30/50, 40/40/60 MW/K | Explicit purchased alternatives, including failed matches. |
| Recuperator UA | 60 MW/K, except 80 MW/K with the 40/40/60 offer | Physical component of the selected service offer. |
| Service quote factor | 1, 1, 1, 1.25, 1.5, respectively | Hypothetical quotes paired with the declared offers. |
| Steam IHX circuits | 10, 11, 12, 14 | Independently chosen equipment count. Primary loops remain 14. |
| Salt pumps per IHX circuit | 2, 3, 4 | Independently chosen equipment count. |
| Salt pump design flow | 225, 250 kg/s | Offered pump design points. |
| Bypass flow rating | 2000 kg/s full offer; 500 kg/s adverse offer | Retain an explicit undersized controller failure. |

The first gas scan has 375 combinations before refusals. Hold the steam comparator at 14 circuits, four 250 kg/s pumps per circuit during this scan. Scan the steam circuit/pump catalog separately at a fixed gas operating choice; use a gas choice that passes at each source if the scan finds one. This separates available steam hardware choices from gas operating choices without inventing steam off-design behavior.

Native execution includes completed oracle cases with failed engineering predicates. Preserve body refusals, their full inputs and reasons in the scan record; they are excluded from a native study definition that requires every case to evaluate. Report both populations. Never turn an oracle refusal into a passing case by changing an input silently.

## Sensitivity proposals

Use the best tested passing gas choice at each common source and a supported selected steam hardware choice at that same source. Selection is from the declared discrete catalog. No interpolation, continuous optimization or inferred equipment sizing is proposed.

Show the steam result with the same 14-circuit connecting hardware across the common source range, and also report the least-cost passing steam connector offer at each source from the declared catalog. This makes any cost of holding the common hardware visible. The underlying steam turbine/generator offer remains the same; varying its connecting equipment does not establish an optimized steam-cycle technology. The gas result likewise names its chosen hardware and operating settings at each source.

- Apply the reviewed absolute efficiency offsets of −0.03 and +0.03 to applicable gas compressors/turbine and steam HP/LP turbines, within their input domains. Retain failures. These are hypothetical performance sensitivities on selected equipment, with no claim of validated off-design maps.
- Vary explicitly selected branch quote factors at 0.5 and 1.5 around the nominal scenario, holding all physical ratings fixed. Preserve the currency conversion and the distinction between hypothetical quotes and qualified procurement scope.
- Vary the nonfuel service and replacement allowance together at 0.5 and 1.5 of the nominal assumptions. Keep the separately scheduled salt machine and bundle replacements distinct.
- Report the exact model-produced break-even cost-correction frontier. Unknown installation, hydraulics and accessory scope cannot be qualified by choosing a finite multiplier.
- Test a common upstream present-value charge at declared illustrative levels after recording its authority as an agent-selected financial sensitivity under the owner's fuel-assumption request. It changes the reported denominator effect; it supplies no reactor or fuel model.

The original brief explicitly requests price and efficiency uncertainty and a fuel-assumption sensitivity. This is the owner authority for sensitivity framing if those axes have `no_constraint_response`. Record the corresponding missing physical/cost resistance as model-development findings. Do not treat that authority as a search permission on unresisted axes.

## Declined directions

Still declare and trace steam/reheat temperature, condenser temperature and salt head. The retained steam offer holds 445/445/42 °C; salt head changes its expected return condition. Preserve diagnostic refusals and explain why these controls do not provide a supported steam optimization range. This comparison cannot establish which technology would win under equally optimized designs.

## Release and evidence

Native implementation validation, complete oracle operand coverage, predeclared numerical tolerances, independent integration review and the stock integration seam must pass before the main study. Record all declared axes and their full entry-key groups, including declined directions. The oracle scan then fixes the executable point list. Every native point passes through stock StudyRunner and PreparedListStrategy.

Verify all cases if practical; otherwise stratify by every observed verdict combination under the stock verifier. Retain identity, constraint catalog, inputs, outputs, constraint verdicts, case identifiers, verification receipts, package archive and source digests. Figures identify failed cases and distinguish conditional comparisons from qualification. The final answer must state any remaining partial completion due to unknown equipment scope or unequal supported operating freedom.
