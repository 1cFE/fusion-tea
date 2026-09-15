# Absolute conductor-current margin

## Answer

The implemented estimate rejects the reference conductor under the selected default performance assumptions. At 20 K and an actual peak field of 24.9 T, estimated reference-conductor critical current is **29.65 kA** against **50.00 kA** operating current. Operating current is **1.687 times critical current**, above the selected allowable fraction of **0.80**. The allowable-current margin is **−26.28 kA**. This is a conditional engineering estimate with explicit construction transfer and field extrapolation; it does not qualify a manufactured cable.

WI-062 implements the native calculation, generated package, independent oracle and twentieth feasibility predicate. The native 295-case study is frozen at `e1f5516b`; all-point oracle comparison is complete. Source/design and implementation reviews passed; final frozen-study and goal review is pending. Formal goal closure and item archival remain owner-held. No merge or push.

## Reference result and feasibility

| Quantity | Reference result |
|---|---:|
| Operating temperature | 20 K |
| Actual peak field | 24.9 T; extrapolation enabled and reported |
| Tape construction scenario | 6 mm wide, 56 µm full composite thickness |
| Effective parallel tape count, reference conductor | 112.709 |
| Effective parallel tape count, set-average conductor | 113.739 |
| Estimated single-tape critical current at actual field | 263.04 A |
| Estimated reference-conductor critical current | 29.647 kA |
| Estimated set-average conductor critical current | 29.918 kA |
| Turn/conductor operating current | 50.000 kA |
| Reference operating fraction, operating / critical current | 1.68653 |
| Selected allowable operating fraction | 0.80 |
| Allowable reference-conductor current | 23.717 kA |
| Fraction margin, allowable − operating fraction | −0.88653 |
| Current margin, allowable current − operating current | −26.283 kA |
| Entering nineteen-predicate feasibility | Fail: divertor heat and winding-pack fit |
| New reference-conductor current predicate | Fail |
| Combined twenty-predicate feasibility | Fail: the same two failures plus current margin |

Nominal radial allocation stays 0.30 m. The conditional local fit screen still has **−120 mm radial margin** and **+21 mm transverse margin**. Reference physical tape length remains 36.579 million metres, tape procurement remains $731.57 million, and LCOE remains $144.74/MWh. No geometry, pricing or existing predicate was changed to recover a pass. Numerical digits support reproducibility; they are not measurement precision. [Native results](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/results/analysis.json), [reference preservation](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/results/native-reference-attribution.json).

## Evidence and applicability

The absolute normalization comes from the admitted Molodyk et al. REBCO dataset, *Scientific Reports* 11, 2084 (2021), DOI 10.1038/s41598-021-81559-z. Its production mean of 175 A at 77 K self-field and fitted 20 K, 20 T lift factor of 1.13 imply 197.75 A per 4 mm, rounded to **200 A per 4 mm**. This is a **statistical inference**, combining direct high-field measurements and measurements extrapolated from 12 T to 20 T. It is not a directly measured 200 A specimen matched to the modeled construction. Independent review checked original evidence and accepted this bounded use. [Source assessment](evidence/performance-research.md), [source/design review](evidence/source-design-review.md).

| Choice and provenance | Meaning and limit |
|---|---|
| [INHERITED: admitted source] 20 K, perpendicular field | Perpendicular is the measured minimum-performance orientation. The estimate uses the conductor family's evidence, without a local field-angle map. |
| [AGENT, source-derived] 200 A per 4 mm at 20 T | Statistical absolute normalization, independent of the desired design-point result. |
| [AGENT] Linear transfer from 4 to 6 mm width; exactly 56 µm full composite thickness | Matches the modeled inventory construction scenario. The production population is mostly 40 µm substrate, but no exact specimen/construction join establishes the complete modeled tape. |
| [AGENT, source-informed] Field dependence proportional to `(B_peak / 20 T)^−0.6` | Simple approximate empirical relation. The 20–24 T segment is not an exact measured curve or a published fit interval. Values above 24 T require explicit extrapolation permission. |
| [AGENT] Maximum supported scenario field 32 T | Engineering cutoff, not a measurement limit supported by the source. Inputs above it are refused. |
| [AGENT] Default material and orientation factors 1 | No performance enhancement is assumed at the reference. Orientation factors 2 and 3 are explicit sensitivity scenarios, not measured local angles or certified gains. |
| [AGENT] Default cabling, degradation and current-sharing retention each 1 | Idealized assembly retention; reductions are evaluated separately and together. These factors do not model stress/strain or weakest-tape statistics. |
| [AGENT, source-informed] Allowable operating fraction 0.80 | Explicit operating allowance, applied once. The source's graded-coil target motivates the scenario; it does not qualify the modeled conductor. |

The measured representative 4 mm samples span roughly 220–270 A at 20 K and 20 T, but have different constructions. Their 1.10 and 1.35 material-factor scenarios test transfer sensitivity. A production band of 700–1000 A/mm² supplies two other material scenarios; it is not a confidence interval for this conductor. The common high-field electric-field criterion is incomplete in the admitted record; the confirmed 1 µV/cm routine criterion applies to 77 K measurements. These limits survive the numerical pass/fail calculations. [Source assessment](evidence/performance-research.md).

Unsupported inputs are explicitly refused: temperature other than 20 K, width outside 4–6 mm, thickness other than 56 µm, actual peak field outside 20–32 T, extrapolation above 24 T without permission, invalid factors or invalid inventory/current values. A source-domain refusal is separate from a supported calculation whose margin is negative. Tests exercise both. [Native design](../../../active/WI-062_absolute-conductor-current-margin/design.md), [implementation report](../../../active/WI-062_absolute-conductor-current-margin/implementation.md).

## Tape inventory and current accounting

The inventory mapping uses physical tape length and physical conductor length from the same procurement model. Their ratio gives effective parallel tapes in a set-average conductor. The existing set/reference winding-fill ratio converts that value to the reference conductor. Tape counts are homogenized effective counts, not a manufacturing bill of integer tape stacks.

```text
N_set = physical tape length / physical conductor length
N_reference = N_set × set winding-fill fraction / reference winding-fill fraction
Ic_tape = I_reference_tape × (tape width / 4 mm)
          × (actual peak field / 20 T)^−0.6 × material factor × orientation factor
Ic_reference = N_reference × Ic_tape × cabling retention
               × degradation retention × current-sharing retention
operating fraction = turn current / Ic_reference
fraction margin = allowable fraction − operating fraction
current margin = allowable fraction × Ic_reference − turn current
reference_conductor_current_ok = current margin >= 0
```

Series length cancels in the tape/conductor-length ratio. Coil ampere-turns are never compared directly with tape critical current. A fixed ampere-turn inventory repartitioned into 40, 50 or 60 kA turns changes parallel tape count and conductor critical current proportionally, leaving the operating fraction unchanged at 1.68653. Total physical tape and procurement stay fixed in those cases. This is a consistency property of repartitioning series turns; it does not mean current or tape inventory cannot affect the margin. Actual field, inventory density and performance changes are independently exercised. [Interface derivation](evidence/interface-assessment.md), [native study analysis](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/results/analysis.json).

The predicate is explicitly **reference-conductor scope**. A set-average capacity is exposed as a diagnostic. Neither is a weakest-tape, worst-coil or complete graded-cable qualification. [Native calculation](../../../../models/library/analyses/mfe_conductor_current.sysml), [public interface](evidence/interface.json).

## Existing sizing law and selected-field predicate

The source distinguishes ungraded coil operating fractions of about 46.5–60.5% from a graded 80% target. Its spatial conductor alignment is absent from the uniform perpendicular, actual-peak-field scenario implemented here. The existing reference density and relative selected-field sizing law do not themselves establish an absolute critical-current normalization or hide the selected 80% allowance. The new current estimate therefore holds the inherited sizing law as a physical inventory scenario and applies the allowance once. Its adverse reference result is reported without altering density, normalization or geometry to obtain agreement with the source's coil result. [Sizing assessment](evidence/interface-assessment.md), [source review](evidence/source-design-review.md).

The **selected-field-envelope predicate remains an independent requirement**. It compares actual peak field with the selected design envelope. The new predicate compares turn current with capacity inferred from actual field and actual tape inventory. Neither implies the other:

- The reference passes the selected-field check at 24.9 T but fails current margin.
- The explicit `m000--orientation-3-independence` scenario passes current margin at an operating fraction of 0.51294 but fails the selected 20 T envelope because actual peak field is 24.9 T.

Keeping both avoids silently broadening the engineering acceptance claim. [Native predicate counterexamples](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/results/analysis.json).

## Bounded study

The study executed **295 unique native cases**, exported as 296 report aliases: 116 unique entering controls, 176 material/orientation/retention cases at sixteen anchors, two turn-current repartitions and one predicate-independence case. Anchors include the reference, all twelve entering nineteen-predicate passes and three historical nominal eighteen-predicate passes. Historical larger-cavity alternatives retain their own coordinates; the nominal cavity was not enlarged. This is a finite sensitivity study, with no optimization or continuous feasible-boundary claim. [Study record](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/record.md).

| Case group | Cases | Entering 19 predicates pass | Current predicate passes | Combined 20 pass |
|---|---:|---:|---:|---:|
| Entering controls, default performance | 116 | 12 | 0 | 0 |
| Orientation factor 2 | 16 | 12 | 1 | 0 |
| Orientation factor 3 | 16 | 12 | 16 | 12 |
| Orientation 3; three retentions each 0.9 | 16 | 12 | 4 | 1 |
| Orientation 3; three retentions each 0.8 | 16 | 12 | 0 | 0 |
| Each of four material scenarios, separately | 16 each | 12 each | 0 each | 0 each |
| Each single retention reduced to 0.8, separately | 16 each | 12 each | 0 each | 0 each |
| All unique study cases | 295 | 144 | 22 | 13 |

All thirteen combined passes depend on the assumed orientation factor of 3. Twelve have ideal assembly retention; one retains a pass with all three retention factors at 0.9, whose combined retention is 0.729. These results show the consequence of missing angle and cable evidence; they do not establish that such performance can be manufactured. None of the four material-only scenarios recovers a current pass at the sixteen anchors.

The old same-sample cheapest passing alternative, `alloc-oldpass1.2-0.5`, still costs $145.02/MWh but fails current margin under default performance: critical current 25.87 kA, operating fraction 1.93251. Its orientation-3 scenario passes at the same price because the model has no supplier performance premium. This is a conditional scenario, not a new cheapest qualified machine or a cost saving.

One preliminary endpoint diagnostic at major radius 11.43 m produced 32.0906 T, above the explicit 32 T domain. It was refused before native proposal execution and is retained as an unsupported-input diagnostic. It is not an ordinary predicate failure or an identified physical boundary. [Window review](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/reviews/window-selection.md).

## Attribution and numerical assurance

The entering package is `a45925ec066c2403c72c2702e323a965e2666a3c`. Current-package controls were captured before implementation at historical coordinates. The comparison does not imply rerunning an older native package off-reference.

- All 117 entering report aliases preserve 196 mapped prior channels and nineteen predicates: **22,932 scalar and 2,223 predicate comparisons** pass. The duplicate alias maps to the same native point. [Entering comparison](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/results/comparison-entering.json).
- The separate captured native reference preserves all **212 prior numeric outputs and nineteen predicates**. Across 177 performance-only pairs, all 212 old native outputs and nineteen predicates remain unchanged: **37,524 scalar and 3,363 predicate comparisons**. [Performance isolation](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/results/performance-isolation.json).
- All 295 cases agree with the independent oracle on **207 mapped channels and twenty predicates**: **61,065 scalar and 5,900 predicate comparisons**, maximum relative deviation approximately 2.48×10⁻¹². All eleven new outputs are mapped. Sixteen older native numeric outputs remain unmapped by the oracle. [All-point verification](../../../../exploration/stellarator_e2e/studies/20260915-absolute-conductor-current-margin/results/oracle-all-points.json).
- Native tests cover passing, exact-boundary and failing current margins, unsupported inputs, actual-field response, unequal reference/set inventory and series/current accounting. Independent implementation review passed 101 focused checks and separately reconstructed a mixed-factor 32 T case. All twenty-three pre-existing manual bodies and thirty-three canonical twins were preserved/synchronized within the reported checks. [Implementation review](evidence/implementation-review.md).
- All ten native integration gates pass at promoted pin `855a3a3b88c277e169aa3265db273c3d24686a6d762d7bd8437c0fd987c6160f`. The reviewed semantic and executable fingerprints are recorded in the [integration return](evidence/T-004_integration/integration_return.json).

Validation scope is explicit. Native L1/L3/L4/L5 pass; L2/L6 are non-green. Ten inherited literal-bound placeholder warnings remain. Twelve new pure-EXPOSE unsupported-dot scanner diagnostics raise the raw L6 count from 273 to 285, without new unbound model inputs. The integration manifest gate omits `assert_read_set_covered`; no other check is claimed to replace it. Final affected verifier tests report 23 passes and one unavailable historical-store skip. This is not a claim of a clean global suite or full native-validator success. [Implementation report](../../../active/WI-062_absolute-conductor-current-margin/implementation.md), [integration evidence](evidence/T-004_integration/integration_return.json).

## What is established and what remains

**Numerical consistency is established within the tested route and mapped outputs.** Procurement, fit and current capacity use the same physical inventory; the added predicate changes admissibility without changing the old cost or geometry calculations.

**Evidence supports an explicitly conditional performance estimate.** Absolute normalization is source-derived rather than fitted to pass. The modeled construction transfer, uniform orientation scenario and reference extrapolation remain visible, and the default result fails.

**Conductor qualification remains open.** It requires exact construction and production-lot performance, a common high-field measurement criterion, actual cable packing and current sharing, local field-angle and graded-coil distributions, manufacturing degradation and weakest-section evidence. Detailed stress/strain, quench protection, complete 3D angle mapping and new manufacturing cost models remain separate follow-ups under the owner's scope. No follow-up work is automatically authorized by this answer. [Finding dispositions](evidence/finding-dispositions.md).
