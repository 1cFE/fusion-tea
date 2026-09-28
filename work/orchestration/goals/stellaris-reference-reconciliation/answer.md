# Stellaris reference reconciliation — technical answer

[OWNER] Goal closed on 2026-09-17 following independent PASS, on the conditional-reconstruction and explained-unresolved-deviations outcome. See the closure entry in [trail.md](trail.md).

[AGENT] The current reference does **not** reproduce one coherent published Stellaris plant. It combines published anchors with generic geometry, a perpendicular-field conductor reconstruction, forward plasma/divertor calculations and an alternative helium-primary cooling system. The reconciliation corrects source attribution and implements explicit reconstruction scenarios. It explains the remaining failures; it does not establish published-reference feasibility.

## What changed

- Corrected false HCLL source attribution: the paper uses a water/PbLi breeding blanket and a separate helium-cooled first wall. The existing helium circuit stays an explicit alternative. Its held TBR and neutron multiplication remain conditional source-case transfers.
- Identified the 300 mm coil layer as inherited generic radial geometry, not a published local cavity. Preserved the raw fit failure and unknown source applicability.
- Implemented source-exact profile scenarios using fuel/temperature exponents 0.35/1.2, with a separate Table 5 plasma-conditioned scenario at R = 12.74 m, V = 425 m³ and B = 9 T. The latter uses a declared derived current adjustment; it is not a source magnet prediction. Historical defaults and fixed magnet anchors remain.
- Added three missing public-input oracle mappings. No physical equation, numerical default, predicate or acceptance limit changed. All 20 raw predicates and their source applicability are retained in machine-readable form.

The [source-to-model table](reconciliation.md) distinguishes prescribed inputs, published predictions, calibration anchors, deliberate alternatives and forward replacements. [Independent original-page review](evidence/source-review.md) checked the consequential interpretations before implementation.

## What the native comparisons show

Eight targeted cases complete with **zero all-predicate passes**. These are sensitivity and attribution cases, not a feasible-region search. [Native study report](../../../../exploration/stellarator_e2e/studies/20260916-stellaris-reference-reconciliation/report.md).

| Legacy-inventory case | Operating auxiliary MW | Divertor peak MW/m² | LCOE $/MWh |
|---|---:|---:|---:|
| Entering digitized profiles | 49.0796 | 10.5178 | 144.7474 |
| Exact published profiles | 45.1725 | 10.2862 | 144.6160 |
| Table 5 plasma conditioning | 44.0038 | 10.2438 | 144.6565 |

The Table 5-conditioned case still computes fusion power 2,603.4 MW, stored energy 513.0 MJ and confinement time 1.5774 s, versus the published 2,700 MW, 504.65 MJ and 1.46 s. Exact inputs do not eliminate the reduced-model/source closure discrepancy. Fusion-power and confinement-time agreement worsens, even as operating heating and divertor peak decrease.

These cases still fail divertor heat, conductor current and pack fit. Exact profiles explain part of the power discrepancy but do not recover the paper's Point-A ignition or close the retained 10 MW/m² divertor screen. The source's 500 MW divertor cases remain separate: paired capture/peak values reconstruct 49.5/48.5 MW deposited and 0.5/1.5 MW uncaptured. Their supplied peaks earn accounting credit only.

The nominal −120 mm fit margin is a failure of the declared 250 mm cavity versus 370 mm required envelope. Published local cavity and manufacturing/tolerance data remain missing. The paper's conductor result uses local field-angle capacity; equivalence to the model's assumed tape construction is unestablished. The scalar model's failed current screen does not refute that source calculation.

Current-driven sizing **plus a 1% inventory reserve** recovers the raw current predicate by increasing reference-effective tapes from 112.709 to 239.984. At the entering profile it worsens fit margin to −285.309 mm and raises LCOE to $163.1942/MWh. Tape procurement rises from $731.57 million to $1,557.69 million under the assumed $20/tape-metre price. No whole-plant pass follows. The historical exact selected mode with zero added reserve is preserved separately, including its near-zero current-boundary discrepancy; it is not relabeled a new verified pass.

The two off-reference checks retain failures: increasing R by 2% raises required heating to 55.6634 MW against 50 MW installed and adds a sustainment failure; increasing a by 2% raises peak field to 24.96798 T against 24.9 T and adds a peak-field failure. They check reduced-model scaling, not engineering transfer. Water-cooling equipment, missing local geometry/conductor qualification and complete manufacturing remain unpriced; account price years differ.

## Verification and limits

Native integration passes all ten gates. Every new case agrees across the native package and independent oracle: 1,808 mapped scalar and 160 predicate comparisons pass. Sixteen native scalar outputs remain outside the oracle map. The comment-only correction preserves executable tokens; regeneration changes no package bytes. Thirteen model-family checks, 151 focused mapping/refusal checks and four strengthened propagation tests pass.

The historical exact selected diagnostic retains 224/226 strict relative scalar matches and 19/20 oracle predicate matches, with two signed near-zero current-margin differences. Eight broader consumer-test failures were reproduced with the entering mapping and remain disclosed. Existing static L2/L6 limitations and the native integration read-set omission remain; no clean full-suite or engineering-qualification claim is made.

Final independent assurance is recorded in [final-review.md](evidence/final-review.md). The original conductor-dataset request remains queued after two native extraction failures; no unregistered material law was installed. The scientific continuation used clean original sources after the precautionary coordinator handoff recorded in the protocol; this is not a claim that the entire parent session was free of exposure.

## Before a new blind-comparison freeze

The existing archive is unchanged: SHA256 `fdf6e14572f10c9254df1e297394f9eccb0060e3947283ea0f8cf569fc63f533`. No reveal, merge or push occurred. A replacement freeze must explicitly choose its plasma profile/geometry and current-sizing mode, preserve the exact boundary diagnostic, include the repaired oracle map and applicability report, and rerun its input/accounting/execution checks. It cannot inherit a claim of published-reference feasibility from this work.

A source-faithful plant qualification requires dimensioned local pack/casing/manufacturing data, exact conductor construction and local field-angle capacity, supported divertor geometry/transport transfer, and separate water-blanket/helium-first-wall thermal and hydraulic circuits. Those capabilities are essential for that stronger claim; explained unresolved deviations satisfy this goal's permitted outcome.
