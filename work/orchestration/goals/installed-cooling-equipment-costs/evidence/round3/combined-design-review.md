# Independent combined-design preimplementation review

Reviewer: `equipment_review`, 2026-09-18. Non-author review of WI-067 `combined-design.md` and T-008 `secondary-methods.md`, using the original source and candidate checks already completed. Inspected the current power-balance and cycle declarations. This is a review of the draft received, not later corrections. No model or implementation authored.

## Verdict

**Conditional HOLD pending the concrete fixes below.** The design's principal decomposition, source-based conceptual prices, capital ownership and lifecycle architecture are sufficient in scope to pursue R7.S3. No supplier qualification, complete routing or every-valve bill is required. The fixes concern reproducibility, physical meaning and honest operating-range treatment; they do not require a new research campaign or steam-cycle redesign.

## Must fix before release

### 1. Make the inventory quantities reproducible

The initial draft's “source-reference blanket/manifold residual” is not defined. Its proposed pipe geometry contains 125.420 m³ helium per circuit; adding the source IHX's 61.5 m³ gives 186.920 m³, already above 879/9 = 97.667 m³. Back-calculating a residual would give negative 89.253 m³/circuit. Do not clamp it or claim source-total agreement.

The coordinator's proposed correction is acceptable: price the calculated ex-vessel/IHX subset plus an explicitly assumed handling/operating reserve; mark in-vessel volume unresolved and report the mismatch. That narrower inventory treatment does not prevent R7.S3. A reserve is not recovered in-vessel geometry, and the resulting total is not a demonstrated whole-system lower bound. Specify the salt shell-void geometry, internals displacement, inventory density convention and chosen exact source price/year likewise. T-008's bulk/small-quantity distinction must appear in the adopted price assumption; a price is not selected merely by citing the source report.

### 2. Complete the salt-pump price and domain contract

The draft names Seider equations but omits their exact coefficients, type/drive factors and operating domains. Persist those from T-008, including the independent choice between fixed efficiencies and source efficiency fits; do not mix the T-008 sample prices with the draft's different fixed efficiencies.

T-008 identifies type factor 1.5 for 1800 rpm single-stage vertical-case-split pumps, with a 200 hp limit, and TEFC motor factor 1.3 through 250 hp. “VSC” is not evidence of a hot-salt cantilever shaft. At the draft's 40 m head and efficiencies 0.75/0.95, selected eighteen-circuit machine shaft/electric powers are approximately 193/203 hp. The r2 forward case is approximately 267/281 hp and exceeds those type/drive ranges. Define whether such cases produce an openly extrapolated diagnostic cost plus violated applicability screen, or use another sourced type/drive choice. Do not silently return an in-range/qualified flag because only the base size-factor or motor-polynomial range passes. Failed but evaluable cases may remain in the study; reference feasibility is not a release prerequisite.

Also specify the Darcy friction law and its laminar/transitional/turbulent treatment, use head-loss addition consistently across hot/cold legs and temperatures, and define exact nonfinite/zero-domain behavior. No detailed fitting/HX loss solution is required: the residual head can remain an explicitly unallocated allowance.

### 3. Correct the meaning of the inherited conversion fit

The existing cycle declares `T2_C` to be turbine-inlet temperature and derives 480 °C from 500 °C primary helium minus 20 K approach. Salt delivered at 465 °C cannot physically supply 480 °C steam. Retaining the efficiency fit as an inherited surrogate is acceptable for this scoped costing study, but calling the result a physically solved full-HITEC cycle would be false.

Explicitly distinguish the inherited **surrogate fit argument** from any actual salt/steam temperature, preserve the unresolved conversion-interface caveat in generated outputs/study interpretation, and retain the matched cost-only case for attribution. Do not change the fit input or add a new steam-temperature assumption silently. No new turbine design or steam-generator pricing is required to resolve this labeling/interface issue.

### 4. State the pump heat/pressure approximation and accounting identities

The proposed secondary electric and recovered-shaft-power terms have a consistent aggregate energy owner. However pressure work contributes to liquid enthalpy and is dissipated around the circuit; it is not all an instantaneous sensible-temperature rise at the pump. Label the return-temperature shift based on total shaft power as a lumped heat-equivalent approximation, or separate pump pressure work and local dissipation if physical point temperatures are claimed. The small temperature correction need not trigger a detailed loop solve.

Persist the exact energy sums used by the power balance, so salt electric draw and shaft heat each enter once and primary IHX duty does not recursively absorb secondary pump work. Specify that any secondary selector disables both these additions together. Preserve primary heat-flow/control comparisons independently of cost-selector changes.

## Accepted conceptual choices and residuals

- Full replacement of both C220200 terms by independently exposed children avoids adding explicit equipment atop the old allowance. Row 7 ending at the salt supply/return interface is acceptable; Row 8 steam-generator price coverage remains explicitly unverified. This qualifies complete-plant economics without defeating Row 7 decomposition.
- The representative main/branch schedule and source-total length allocation are declared assumptions. The large calculated volume discrepancy is a warning about that representative layout, not permission to disguise it. Fixed primary hydraulics remain a disclosed calibration seam.
- ANL finished-component rates and installation, BNL machine/power-supply/first-design scope, and explicitly transferred piping/pump installation analogies remain acceptable with their reviewed uncertainty. Procurement assigned to CAS30 is a permissible ownership assumption; reproduce ORNL's installation denominator without adding procurement twice.
- Excluding only the direct delivered amount from CAS50 shipping is an explicit partial normalization. Report the inherited residual shipping on contingency/other capital; do not claim all empirical shipping duplication has been eliminated. Exclude initial delivered equipment/spares only, not future replacements or field labor, and ensure the resulting shipping base remains meaningful rather than silently clamped.
- Routine service labor assigned to existing CAS71, separate consumable make-up and dated major replacement costs provide meaningful lifecycle coverage. Coincident outages and chosen service lives can remain assumptions. Unknown lifting/waste/removal detail may qualify costs; it does not require qualified outage scheduling. Define which installation line is repeated for removal labor so material charges are not accidentally doubled.
- Valve selection, local support/insulation detail, pump hot-salt construction extras, cover-gas and freeze-protection hardware may remain residual scope with explicit ownership/omission status. Their significance is not proved negligible. Do not label an unpriced startup/trace-heating requirement as zero energy or imply that normal-operation temperature alone resolves shutdown freeze protection.

## Verification and study adequacy

The proposed legacy/new-cost-only/full-secondary comparisons, four retained cases, matched circuit-count/demand/layout interventions and lifecycle/construction scenarios are appropriate. Before execution persist exact cases, ranges, mode defaults and expected account/energy identities. Regenerated producer/manual/oracle agreement and original-source reconstruction remain separate evidence. Include strict-horizon replacement counts, spare-versus-replacement ownership, shipping exclusion, positive HX approach/area screens and all pump subrange checks. Keep inherited breeding/current/divertor/fit failures and new applicability/head failures visible. No optimization claim is supported or required.

After the listed draft fixes and exact T-008 method choices are recorded, a short corrective review can release implementation. It need not repeat completed source research. Final R7.S3 remains contingent on implemented, verified child and lifecycle rollups; the present production grade remains R7.S2.

## Corrective review and scoped implementation release

Reviewed the amended combined design and final T-008 report on 2026-09-18. The draft now explicitly prices only ex-vessel helium inventory with a reserve and exposes the source-volume mismatch; records exact pump/motor equations, separate efficiencies and failing type/drive domains; retains 480 °C only as a surrogate conversion-fit argument with an exported 15 K incompatibility and failed physical-interface screen; and identifies the salt temperature shift as a lumped heat-equivalent. These amendments resolve the material source, scope and physical-meaning findings above.

**RELEASE implementation of the stated Row 7 conceptual equipment and lifecycle design.** This supersedes the initial conditional hold. It is not approval of a complete installed plant estimate, a qualified salt/steam operating point or an achieved R7.S3 grade. Source-range failures and the conversion-interface failure must survive into results and prevent a claim that all physical screens pass.

Unpriced drain/expansion construction, trace heating, cover-gas equipment and local accessory detail do not by themselves prevent S3 once the principal independently sized equipment and lifecycle rollup are implemented. Keep their economic/operational significance unresolved rather than asserting negligible cost or zero startup heat. Existing CAS71 ownership of routine inspection, service labor and chemistry management is an acceptable explicit coverage assumption; separate consumable make-up and major replacements provide incremental lifecycle accounting. This is adequate conceptual coverage without a newly sourced maintenance percentage or qualified service schedule.

The implementation plan should settle the remaining routine numerical conventions before their corresponding code: smooth-pipe friction law and transition policy; salt void/displacement and fill-density definition; representative helium inventory temperature; removable-internals scope; the labor-only removal charge; and exact secondary-mode energy sums. These are documented choices within the released design, not grounds for another owner approval cycle. Review/testing must check that shipping exclusions cover only initial delivered purchases/spares, that all package and annual costs have one owner, and that legacy mode reconstructs its entering accounts.

One source transcription needs correction during that routine cleanup: the registered Minneapolis annual CPI table reports **2021 = 271.0**, not 270.97. Use the registered value or explicitly cite an alternative more precise series; do not describe 270.97 as copied from this table. The source pump table calls its 200 hp column “maximum motor Hp”; interpreting this as motor shaft rating for the pump-type screen must remain distinct from electrical consumption used by the motor purchase equation and TEFC range.

No further source-acquisition or mechanical-qualification gate is imposed. Final structural grading requires canonical model children, generated execution, source/quantity/account/lifecycle checks and the declared matched study. Until that evidence exists, the prior production R7.S2 remains the current grade.
