---
Verdict: PASS
Created: 2026-09-18
Criterion: R7.S
Grade: 3
Rubric Commit: dc0f0b6dc6512b29e1307da647f3a508a1f5356d
---

# Final independent Row7 structural and costing assessment

**R7.S = 3. The scoped technical target is met.** The exact unchanged row requires “Pumps, piping, heat exchangers as separately sized subaccounts.” General S3 requires independently sized children rolling through appropriate quantity, fabrication, installation, spares, replacement and maintenance logic. The implemented model and native study satisfy these tests. This assessment does not regrade Row7 physics or any other row, award S4, establish a feasible plant, or authorize formal goal closure or comparison replacement.

This is a non-author continuation of the original-source, design and implementation reviews in this goal. I inspected the actual native study outputs, matched proposals, corrected verification receipts, current answer and proposed study reading. I authored no source methods, implementation, study repairs or dispositions.

Primary evidence: [study record](../../../../../../exploration/stellarator_e2e/studies/20260918-installed-cooling-equipment-costs/record.md), [native cases](../../../../../../exploration/stellarator_e2e/studies/20260918-installed-cooling-equipment-costs/results/native-cases.json), [all-point comparison](../../../../../../exploration/stellarator_e2e/studies/20260918-installed-cooling-equipment-costs/results/oracle-all-points.json), [generic verification receipt](../../../../../../exploration/stellarator_e2e/studies/20260918-installed-cooling-equipment-costs/results/verification_summary.json), [integration return](integration-retry1/integration_return.json), [proposed study reading](study-reading.md), and [goal answer](../../answer.md).

## Criterion judgment

The canonical heat-transport structure exposes helium circulators, primary piping, helium-to-salt exchangers, salt pumps, salt piping, initial inventory and spares as separate cost children. The prior primary and intermediate power-law terms are replaced together at the sole cooling-cost consumer. Counts, flow, pressure rise or head and shaft duty size the machines. Declared pipe schedules produce steel mass. Exchanger duty and terminal approaches produce required area, while a separately declared source-scale geometry supplies installed area and component metal quantities. This is more than allocating an aggregate bill among named accounts.

Finished-component fabrication rates, machine purchase methods and installation allowances apply to those quantities. One initial spare of each machine type is priced. Explicit machine and bundle replacement events feed the actual CAS72 consumer. Inventory make-up feeds raw CAS71 expenses, while existing routine-service labor remains an explicit inherited coverage assumption. These boundaries satisfy general S3's appropriate lifecycle test. Source-based conceptual analogies are sufficient for this structural level; procurement qualification and validation against a matched engineered reference would be a stronger claim.

The sources and assumptions remain distinguishable: BNL supplies the helium price anchor and pressure/material-half duty relation; the power-supply scaling and target technology transfer are declared assumptions. ORNL27% installation uses its procurement-inclusive driver without charging procurement twice. ANL supplies the finished stainless fabrication/delivery basis and HX labor/material additions. Pipe field labor transfers the NETL ratio explicitly. Seider supplies liquid-pump/motor equations, material/type factors and retained source ranges. None establishes a vendor-qualified hot helium or salt package. Prior source reviews and [implementation assurance](implementation-review.md) carry the exact provenance and correction history.

## Independent numerical checks

I matched all34 retained native case inputs to their corresponding proposals and checked that each completed. For every case I independently reconciled the seven equipment child costs and the CAS71/CAS72 additions. I checked all twelve saved-reference mode rows against retained native outputs. The selected eighteen-circuit arithmetic is:

- New equipment cost is $8,205,336,787.917920 versus the legacy $205,073,391.404296. The matched CAS22 increase is $8,000,263,396.513624; the total-capital increase after inherited factors is $11,434,850,482.183619.
- Cost-only mode leaves net output1010.112286982139MW unchanged and raises LCOE from150.429542199135 to309.554789393816$/MWh. Selecting salt energy then reduces net output by3.386988135338MW and adds1.077873810369$/MWh. Full-mode LCOE is310.632663204185$/MWh.
- The ORNL installation denominator reproduces0.27×1.155×vendor. Exchanger purchase reconciles eighteen component masses with310USD2017/kg and the stated CPI conversion. The delivered shipping exclusion equals only the declared delivered initial supply amounts.
- Discounting machine events in years10/20 and the bundle event in year15 at7%, then annualizing over30years, independently reproduces $63,243,147.383642/year. First-design engineering and initial spares are not repeated. Removal is the disclosed labor proxy, not a measured dismantling price.

The selected18 price is distinct from the authored default baseline, whose LCOE is270.82387460276726$/MWh. The answer and study correctly retain this distinction. Money figures use a2025 annual-CPI purchasing-power proxy for new equipment; they do not establish uniformly rebased whole-plant dollars.

## Verification and retry judgment

The retained integration retry1 return has all ten gates passing. The corrected study all-point receipt has12,206 scalar comparisons and680 exact predicate comparisons, with zero failures or strict-relative misses. The generic verifier receipt/log reports all34 sampled rows,29 checked channels,20 re-derived verdicts and worst relative difference5.56e−16. Its narrower channel check is distinct from the full359-channel independent map. The latest targeted boundary/equipment regression batch reports258 passes. The earlier six stale consumer-contract failures and the Level2/6 static diagnostics remain separately disclosed; no clean full-suite or green static-validator claim follows.

The first all-point check exposed six exact conductor-current predicate disagreements: tiny negative native margins versus zero in the algebraically simplified oracle. Those native adverse results remain unchanged. Commit450f4eab changes only oracle arithmetic order and related verification evidence, following the authored continuous sizing and inventory sequence. The independent expanded tape-volume calculation remains a relative1e−12 consistency check. This is a justified reproducibility correction, with reduced arithmetic-order diversity explicitly acknowledged; it is not a threshold waiver, rounded margin, native-output import or new physical evidence. Failed receipts remain part of the audit trail.

## Supported claim and limits

The evidence supports a separately sized conceptual estimate for the principal Row7 cooling equipment and its stated lifecycle. It does not support a complete installed-plant estimate or qualified equipment design. Fourteen circuits costs less under these assumptions but fails liquid-machine source ranges; twelve circuits also fails exchanger capacity and the retained loop-capacity predicate. All34 cases fail the current breeding predicate. None is an optimum or a recovered historical feasible design.

The retained480°C cycle-fit argument exceeds465°C salt supply. The full-energy scenario therefore remains an accounting sensitivity using an inherited conversion surrogate. Pipe routing, gross tubesheets, assumed wall thicknesses, unvalidated helium/salt construction transfers and field-installation analogies drive substantial uncertainty. The modeled helium volume exceeds the reference envelope by about1.91×. Initial inventories exclude unmeasured in-vessel and conversion volumes. Trace heating, drain/expansion equipment, cover gas, detailed valves, supports/insulation and other residual accessories remain unpriced; their significance is not established negligible. Service lives, routine maintenance coverage and coincident outages remain assumptions. The steam generator has one owner in Row8/CAS23, with its inclusion in the inherited price unverified. These limits are compatible with the scoped S3 structural result and must travel with every use of its cost numbers.

## Answer, dispositions and completion boundary

The inspected answer's quantities, costs, matched comparisons and source/accounting qualifications agree with the retained outputs and reviewed methods. Its pending-verification and pending-grade language may now be replaced by the scoped results above. No remaining technical must-fix was identified in this review.

Proposed dispositions for findings#1–4 are appropriate: retain adverse cost, source-range, layout/inventory and lifecycle results without silently scheduling semantic follow-up. Finding#5 should record the completed oracle correction and passing retry while preserving the original failures and native negative margins. Proposed L-007–009 are supported: the separate lifecycle accounts now meet R7.S3; equipment costing dominates the matched economic change; geometry and the salt/conversion mismatch remain material limitations. These are learned results and scoped acceptance, not new owner requirements or a qualification waiver.

This assurance permits concluding the technical goal after the study record, snapshot and final round result faithfully carry these outcomes. The final frozen-artifact/commit check can be a narrow addendum. Formal native goal closure, comparison reveal/replacement and broader physical-design refinement remain owner decisions.
