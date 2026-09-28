# ARIES comparison: results and remaining limits

**The selected model does not pass the original ARIES comparison.** The radial layers appear in the required order, but the plant lacks a separate liquid-metal heat-removal circuit present in ARIES. Numerical component comparisons also expose scope and technology differences. We can report those differences now without waiting for coil geometry. We cannot establish a supported full-plant LCOE.

This assessment uses the existing partial run. It changes no design input, equipment purchase, model equation or scientific range. The run transferred three reference inputs and held the remaining 701 choices. It therefore evaluates our selected design at that point; it does not reconstruct the complete ARIES plant. All 276 comparison rows and the original attempt records remain preserved.

## The original rubric and this assessment

| Original criterion | Result | Evidence |
|---|---|---|
| Recognizable subsystems with no first-order omission | **Fail.** Broad plant functions are present, but the separate ARIES PbLi blanket heat-removal branch is absent. | [Subsystem mapping](structure.md) |
| Radial layers in the same sequence | **Pass at the prescribed qualitative level.** Plasma, clearance, first wall, blanket, shield, vessel and coil order corresponds. This does not validate shell thicknesses or clearances. | [Radial mapping](structure.md#radial-build-ordering) |
| Cost-account coverage and correspondence | **Unresolved.** Broad families exist; vacuum, manifolds, cryostat and indirect-cost allocations cannot all be reconciled. | [Account crosswalk](structure.md#cost-account-coverage-and-crosswalk) |
| Derived quantities within model/reference [1/3,3] | **Not established.** The reviewed quantities lack matching definitions or independent prediction status. Two selected pack dimensions have descriptive ratios within the band. | [35 quantity dispositions](quantities.md) |
| Component costs within model/reference [0.5,2] | **Not established.** Twenty-one raw price pairs can be shown, but common dollar basis, scope or technology is unresolved. | [35 cost dispositions](costs.md) |
| Overall comparison | **Does not pass.** Structural failure is established; numerical accuracy is not established. | [Complete register](evidence/comparison-rows.csv) |

The separate depth assessment's 23/23 targets concern represented engineering detail. They do not override these comparison findings. No new depth score is awarded here.

## What we learned

**1. The plant architecture differs in a major heat-removal path.** ARIES uses liquid PbLi and helium blanket circuits, with a distinct PbLi exchanger branch. The selected model has primary helium and an intermediate HITEC circuit. The ARIES engineering paper assigns 1,444 MW to PbLi heat removal in its illustrated case, which establishes the importance of that branch. This is evidence of architecture, not a claim that every engineering-paper number equals the final systems-study point. The model also uses steam Rankine conversion where ARIES uses helium Brayton conversion. [Source images and bindings](structure.md).

**2. Similar pack area does not establish similar magnets.** Model pack dimensions are 0.360 × 0.369 m; the reference lists 0.194 × 0.743 m. Their nominal area ratio is 0.922, but the selected model pack is almost square and the reference pack is elongated. The model still has a −0.120 m radial fit margin. These are consequences of different selected geometries; they do not validate field, conductor capability or independent sizing predictions. [Dimension definitions](quantities.md).

**3. Several apparent cost matches are selected-price or account-boundary comparisons.** Waste treatment is nominally close ($6.482 million versus $6.655 million), but the model prices a selected plant class rather than calculating waste-processing demand. Turbine cost is a supplied steam-package amount compared with a Brayton plant. The reference vacuum account includes a cryostat, while the model vessel account is narrower. A ratio inside the band cannot resolve those differences. [Account findings](costs.md).

**4. The large nominal differences identify useful future audit targets.** Model/reference nominal ratios are 8.93 for blanket cost, 8.51 for magnets and 148.37 for winding operations. These are raw price comparisons across unresolved dates and equipment boundaries, not formal accuracy failures. The winding figure in particular points to the transferred manufacturing allowance and its boundary as a future audit target. The recorded result is the difference and its known basis limits, not a fitted correction. [Values and producer ownership](costs.md).

## What the arithmetic can and cannot establish

Of 276 rows, 103 are unaffected by the field finding. Twenty-four of those are supplied or held information. The remaining rows include 35 calculated quantities, 35 calculated costs and nine diagnostics. One of the nine diagnostics is breeding, which is undefined for a separate reason. The final register therefore classifies eight as retained diagnostics and breeding as blocked by the model domain. The machine-readable register preserves the original labels and applies a separate current disposition; its mutually exclusive counts should not be confused with the original overlapping qualifications.

All 35 quantity rows and all 35 cost rows received explicit review. Twenty-one cost rows have raw source values; fourteen do not. Eight nominal cost ratios lie in [0.5,2], three below and ten above. These counts include the excluded power-supply account and overlapping parents/children. They are not a pass rate. No cost has been converted to a common money year; conversion from printed millions of dollars to dollars is the only numerical price conversion.

The [full CSV](evidence/comparison-rows.csv) is the compact disposition list. The [JSON](evidence/comparison-rows.json) contains each unchanged original row, the new disposition and the detailed quantity/cost review. Blocked field-dependent and undefined model results remain visible. No rows were dropped to improve agreement.

## Engineering results remain separate

The partial run reports selected cold-stage cooling 649.468 W short, intercept-stage cooling 375.736 W short, and radial winding-pack clearance −0.120 m. Those calculations do not depend on the field finding, under the existing model assumptions. They concern the selected equipment, not a verified reconstruction of ARIES. Breeding is undefined at this geometry; some helium checks reject unsupported operating conditions. These must not be recast as demonstrated ARIES failures. [Retained interpretation](../partial-assessment/report.md).

The 56.618 T field arithmetic remains scientifically unqualified for the transferred geometry, and conductor capability remains unavailable. Full-plant costs and electricity depend on additional unsupported or undefined calculations. No supported LCOE is reported.

## Acceptance rules and source discipline

The original ratio endpoints remain unchanged. The original specification's approximate logarithmic wording does not replace [1/3,3]. C220107 power supplies remains excluded or footnoted, including its contribution to parent accounts; no artificially clean aggregate is constructed. Original failed executions remain original; these are post-reveal findings, not a new blind test.

Cost-account numbers vary even between the reference papers. Najmabadi p663 labels heat rejection 26 and special materials 27; Lyon p707 labels them 27 and 26 respectively. The maps use account meaning and cited table, not an assumed universal number.

B-7's existing [provenance receipt](../package/provenance-check.md) is reused: it checked the local raw-PDF table and separately recorded the inherited AACE 18R-97 scope caveat. The factor-of-two cost band is this project's criterion, not AACE certification or established 80% uncertainty coverage. No fresh external-standard verification is claimed.

## Review, preservation and reproduction

[Independent review](evidence/review.md) checks the source/model correspondence, interpretations and reporting. [Preservation receipt](evidence/preservation-after.json) verifies the protected baseline. Reproduction commands are in [replay.md](replay.md); they rebuild reporting only. No plant run, model change, push or merge was made.

The assessment can be written up with the stated findings and limits. Field-model repair, extended scientific support and a comparable dated equipment estimate remain future development work; they are not prerequisites for honestly reporting this comparison result.
