# ARIES comparison: readiness and proposed reveal procedure

**Historical snapshot:** September 17, 2026, describing r2 readiness. Superseded for execution by [r3 publication](replacement-r3/publication.md) and the [r3 execution prompt](execution-prompt.md). The results below retain their original date and scope; this document does not authorize reveal.

## Purpose and authority

[OWNER-VERBATIM] “Get a good defensible model that can reasonably be scaled/adapted to test against ARIES design points (physics and costing)” and “Then do the ARIES test.”

[OWNER] The initial conditional helium comparison scope is accepted, with unsupported coolant/blanket correspondence and affected downstream quantities retained as unresolved or incompatible. Source: [owner scope decision](../../../work/orchestration/goals/aries-fixed-point-comparison-readiness/readiness.md). The owner subsequently approved replacement freeze r2. Source: [publication and authorization record](replacement-r2/completion.json). Reveal remains a separate explicit owner act under the [quarantine protocol](../../../knowledge/holdout/aries-cs/PROTOCOL.md).

[AGENT] The reviewed evidence supports proceeding with that conditional comparison. The useful question is how well the frozen model transfers to the reference point, and where its predictions or applicability fail. Completing this comparison does not imply passing every acceptance criterion or qualifying a buildable plant.

## What is ready

[INHERITED: replacement-r2/evidence/final-review.md] R2 has an independent PASS for archive integrity and the specified reproduction checks: 1,498 indexed files, 97 passing extracted tests, 1,022 accounting checks and 219 supplied/held alias checks. Its 174 comparison rows retain 166 mapped quantities, five absent producers and three structural evidence requirements. All twenty raw model constraints remain visible. The manifest, accounting bridge, input-selection rules, synthetic rehearsal and executable freeze are complete; they are no longer proposed preparation tasks.

The execution references are:

| Reference | Purpose |
|---|---|
| [R2 freeze record](package/freeze/r2/freeze-record.json) and [independent review](replacement-r2/evidence/final-review.md) | Identify and verify the published archive |
| [Frozen procedure](package/freeze-procedure.md) | Restore, verify, execute and preserve the comparison |
| [Input rules and applicability](package/input-applicability.md) | Decide which reference quantities can be supplied and where correspondence is unsupported |
| [Manifest](package/manifest.json) and [accounting/normalization](package/accounting-normalization.md) | Define quantities, disjoint account boundaries and allowed conversions |
| [Reporting contract](package/reporting.md) | Assemble observations and produce the formal report |
| [Ratified acceptance specification](../../completed/20260821_demo-anchor-acceptance-spec/spec.md) | Define the formal axes and unchanged bands |

[INHERITED: package/freeze/r2/freeze-record.json] The r2 archive SHA256 is `fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21`. Execution uses the verified archive in an isolated checkout with its pinned runtime. The linked working-tree documents help navigation; the archived bytes define the frozen procedure.

## What the latest goal adds

[INHERITED: pre-reveal-feasible-neighborhood/answer.md and evidence/independent-review.md] The latest study found 103 passing cases among 334 selected native evaluations, including 43 of 45 neighborhood checks. These use the separately declared 1.01 conductor-inventory scenario. The field and divertor margins are narrow; the samples do not establish a continuous feasible region or physical qualification. See the [answer](../../../work/orchestration/goals/pre-reveal-feasible-neighborhood/answer.md) and [independent review](../../../work/orchestration/goals/pre-reveal-feasible-neighborhood/evidence/independent-review.md).

[INHERITED: same answer and r2 independent review] That study reproduced the frozen r2 controls exactly and left the comparison package unchanged. R2 keeps inventory multiplier 1.0; its existing forward and Table 5 control points retain current-boundary, pack-fit and divertor failures. The sampled passing neighborhood is separate evidence about the model. It does not replace the reference inputs or held assumptions used for the blind comparison.

[AGENT] No further pre-reveal physics campaign is proposed here. Archive verification and the documented reproduction checks are execution preparation; they do not require another design-space search.

## Proposed procedure

### 1. Confirm the frozen package and record reveal

[INHERITED: package/freeze-procedure.md and PROTOCOL §6] Verify r2's identity and restore the archived procedure. Before opening sealed papers, the owner explicitly triggers reveal and records the status, date and unsealed files under the quarantine protocol. Extraction belongs in `knowledge/holdout/aries-cs/extracted/`; comparison-derived material belongs in the designated comparison artifacts. Index registration is a separate recorded decision.

### 2. Extract the reference point and establish what corresponds

[INHERITED: package/input-applicability.md] Retain page/table citations, raw values and units, definitions, design revision, uncertainty, account scope and monetary/finance conventions. Apply the frozen source-priority rules. Preserve unresolved conflicts rather than choosing the value that agrees best with the model.

[INHERITED: same source] Only seven independently reported quantities may replace the blind defaults: major radius, minor radius, peak electron density, peak ion temperature, reference-coil ampere-turns, radial exterior coil allocation and transverse clear cavity. Exact keys and units are in [input-rules.json](package/input-rules.json). Missing inputs retain visibly held defaults and block dependent claims that the result represents the reference fixed point. Unsupported geometry, technology, coolant or account correspondence remains explicit.

### 3. Run the frozen forward model first

[INHERITED: package/freeze-procedure.md] Supply the permitted, source-supported inputs and calculate the model's outputs without tuning coefficients to improve agreement. R2's held assumptions include exact profile exponents 0.35/1.2, current-driven sizing with inventory multiplier 1.0, fourteen representative helium circuits, and its existing material, cycle, calendar and finance choices. Retain all outputs, twenty constraint verdicts, extrapolations and execution failures. A supplied quantity earns no independent prediction credit.

### 4. Review the mapping and publish the original comparison

[INHERITED: package/freeze-procedure.md and reporting.md] Map the model and reference quantities onto the complete manifest, then independently review the source-to-quantity correspondence before accepting verdicts. Preserve missing producers, missing reference values, unsupported scope and refused calculations. The reporter checks declared structure and arithmetic; a citation string alone cannot establish scientific equivalence.

[INHERITED: ratified acceptance specification B-2–B-8] Report structural correspondence, derived quantities and per-component costs separately. Derived model/reference ratios must lie within inclusive [1/3, 3]; component-cost ratios within inclusive [0.5, 2]. C220107 remains excluded or footnoted with its aggregate effects disclosed. LCOE is supporting information with no formal pass band. Unresolved essential axes cannot pass; an out-of-band result remains a finding. Preserve the first report immutably.

[INHERITED: package/accounting-normalization.md] Apply only the frozen conversion rules and keep raw observations beside any converted values. R2 freezes no monetary-year adjustment algorithm and permits no such adjustment to the formal verdict. Mixed-year costs remain disclosed. A later evidence-supported common-year or common-finance comparison is a separately labeled diagnostic, not a replacement verdict.

### 5. Use separate diagnostics to explain discrepancies

[INHERITED: package/freeze-procedure.md] After preserving the original result, existing supported input seams can supply selected reference outputs to examine downstream responses. Each conditioned run has a separate report and no independent blind credit. The fixed Table 5 seam is a Stellaris control, not a holdout geometry substitution. Post-reveal corrections, alternative technologies, normalization amendments and optional optimization are separately versioned work.

## Limits to carry into the report

[INHERITED: package/readiness.md and the latest goal answer] Passing the implemented screens does not establish breeding self-sufficiency, a qualified conductor/cavity design, a new magnetic equilibrium, source-faithful coolant performance or a complete installed price. Manufacturing and additional cooling installation remain partly unpriced. Financial and maintenance assumptions remain conditional. Sixteen native scalar channels remain outside the independent oracle mapping; the exact-current-boundary disagreement is retained explicitly.

[INHERITED: stellaris-plasma-power-balance/answer.md] Published source ignition remains unreproduced, with unresolved source energy/radiation implementation. The [reviewed plasma-balance answer](../../../work/orchestration/goals/stellaris-plasma-power-balance/answer.md) explains the quantified discrepancy. This limits the physical interpretation of power predictions; the preparation checks do not resolve it.

[AGENT] The proposed deliverable is the original fixed-point comparison with an evidence-backed account of agreement, failure and unresolved applicability. The conditional scope and r2 freeze are already approved. Explicit reveal is the remaining owner act before extraction; any change to the formal comparison requires a separately recorded amendment.
