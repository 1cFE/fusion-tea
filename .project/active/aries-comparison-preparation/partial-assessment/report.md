# Partial assessment with the original inputs

**The assessment now continues past the conductor refusal. It exposes additional equipment and model limitations, but it does not establish plant feasibility or a supported LCOE.** This is a new diagnostic run of the same three reference inputs and 701 held inputs. All 704 effective inputs match the original failed attempt exactly. No equipment, current, geometry, equation or empirical range was changed.

The calculation still reaches 56.61785714285713 T and the conductor model still refuses it. The [field audit](../post-reveal-investigation/field-audit/audit.md) finds that the field approximation is unqualified for this transferred geometry. That number remains diagnostic arithmetic, not an established field prediction or proof of an impossible magnet.

## What was recovered

| Item | Result |
|---|---|
| Native numeric outputs | 1,341 retained; 11 unavailable |
| Engineering checks | 51 native satisfied, 15 native violated, 1 unavailable |
| Comparison rows | All 276 preserved; 267 have raw arithmetic, 1 lacks its calculation, 8 need structural evidence |
| Model-definedness | 17 row values suppressed by existing model guards and their downstream dependencies |
| Field finding | 103 rows unaffected by this finding; other rows carry field-dependency or unresolved structural labels |
| Supported comparison predictions | None claimed; source correspondence and other scientific limits remain unresolved |

The 15 native “violated” statuses are not 15 established physical failures. Some checks include “this evaluation is defined” in their condition, so they return false when the model does not support the case. The [interpretation supplement](evidence/predicate-interpretation.json) preserves all 67 original statuses and explains their meaning.

## Findings that do not depend on the field calculation

Three native equipment checks are violated without a dependency on the field approximation:

| Check | Supplied equipment versus calculated requirement |
|---|---|
| Cold-stage cooling | 21,933.902 W supplied; 22,583.370 W required; 649.468 W short |
| Intercept-stage cooling | 41,599.954 W supplied; 41,975.690 W required; 375.736 W short |
| Winding-pack fit | Minimum geometric clearance margin is −0.120 m |

These are meaningful failures of the selected equipment under the existing model assumptions. They do not qualify the cryogenic-load model, geometry representation or equipment offers. They describe our held design at the transferred point, not a reconstructed ARIES magnet. Cooling units and bindings are recorded at `models/library/structure/mfe_plant_systems.sysml:486` and `:498`.

## Findings that need a different interpretation

- **Breeding is undefined at this geometry.** The raw zero carrier is not a prediction of zero breeding. The same limitation affects the modeled fuel inventory and conservatively blocks its dependent cost interpretation.
- **Four helium-equipment checks are outside supported equipment conditions.** Their native `defined_in=0` accompanies positive numerical capacity margins. Those statuses do not establish insufficient capacity. The implementation compares operating conditions with the supplied offer conditions; it does not supply an off-design machine-performance map.
- **Fuel-processing capacity is not cleared.** Its native check is satisfied, but its demand passes through the inventory module whose definedness flag is zero. The dependency rule conservatively withholds interpretation of all affected module outputs. A finer mathematical dependency analysis could recover some of them; this assessment does not claim that analysis.
- **Six other native violations remain field-unqualified.** These concern conductor strain, facility geometry, peak field, recirculating power, plasma sustainment and winding-pack stress. The dependency labels operate at module granularity. A module's individual output may depend on fewer inputs, so the labels deliberately withhold more rather than claim independence without evidence.
- **The facility-occupancy check crosses a strict boundary by approximately −4.55×10⁻¹³.** Preserve the violated verdict. This warrants a numerical-boundary review, not a claim of a demonstrated material occupancy shortage. No tolerance was changed.
- **Conductor-current adequacy remains unavailable.** Its calculation refused the field input; it was not converted into a satisfied or violated engineering result.

Fifty other native satisfied checks remain visible without engineering acceptance. Together with the categories above, these account for every one of the 67 checks.

## Electricity cost

There is still no supported LCOE. The raw arithmetic contains $2,381.916/MWh in the discounted-cash-flow calculation and $2,334.243/MWh in the other LCOE convention. Both depend on the unqualified field calculation and on inputs affected by undefined breeding/fuel inventory. Both are suppressed in the diagnostic-value and supported-prediction columns. These are retained calculation carriers, not usable plant-price estimates or comparison results.

## What to do next

The next scientific task is to qualify the field calculation for the intended coil family using actual geometry, current distribution and winding-pack behavior. The audit identifies missing information; it does not provide a corrected field. Widening the conductor interval or substituting the published reference field would not resolve that task.

The partial assessment also identifies separate work on breeding-geometry coverage, helium off-design equipment support, and the selected cooling/pack-fit deficiencies. Preserve these findings before choosing another design or expanding a supported domain. Scientific support and design selection are separate decisions; changing equipment to make this case pass is not part of this run.

## Evidence and reproduction

- [Native diagnostic and immutable attempt receipt](attempts/diagnostic-1/receipt.json), [complete row/predicate report](attempts/diagnostic-1/report.json), [field dependency paths](attempts/diagnostic-1/field-qualification.json), [model guard propagation](attempts/diagnostic-1/model-definedness.json).
- [Adopted runtime and runner identity](adoption.json), [independent preflight](evidence/review-preflight.md), [exact reporting-only replay](evidence/reporting-replay.json), [findings log for the write-up](findings.md).
- [Replay instructions](replay.md). Replay rebuilds the reporting from retained evidence without another physical evaluation.

The [final independent review](evidence/review-final.md) passes for this scoped result, including the readable interpretation. Twenty-two focused tests passed and were independently repeated. The [preservation receipt](evidence/preservation-after.json) verifies 876 historical/model files unchanged. Existing native-runtime tests were reused with their previously reviewed scope; this task did not rerun the full model regression suite because model equations and the reviewed runtime implementation did not change.

This runner uses the reviewed diagnostic runtime explicitly. The original failed comparison, frozen archive and ordinary shared runtime remain unchanged. No full comparison registration, reference-field substitution, push or merge occurred.
