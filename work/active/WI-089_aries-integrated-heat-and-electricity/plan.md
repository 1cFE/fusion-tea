# WI-089 executable plan

Status: implementing after independent design PASS
Created: 2026-09-22
Updated: 2026-09-22
Related Artifacts: spec.md; design.md

## Phase 1: Resolve design and source gate

- [x] Inspect actual WI-083/085/086/087 definitions, source images, typed completions and native build route; record roles, reuse, interfaces, equations and single assumption register.
- [x] Independent reviewer accepted corrected source interpretation, closure, roles and ledger. Gate: `work/orchestration/goals/aries-integrated-heat-electricity/evidence/design-review.md`; accepted source identities recorded there before implementation.

## Phase 2: Add one native assembly

- [x] Add only the two new SysML paths in design.md. Stage unchanged reused definitions and imported plasma case. Add domain-guarded generic typed completions for selector/partition, heat-driven closure/passive recuperator and electrical/plant ledgers; preserve named component ownership and all exposed outputs.
- [x] Generate `exploration/aries_integrated/aries_integrated` through `.codex-test/run sysml-codegen` after checking actual help. Install completions, regenerate with `--preserve-handwritten`, prove fixed-point identity, retain source/completion hashes and tracked staging root plus exactly one snapshot. Coordinator owns shared registries and integration packaging handoff.
- [x] Inspect generated parameter schema and graph: selector feeds both fuel and heat; turbine temperature comes from closure; ratings/UA/flows/ratios remain entries; no source output or caller-derived plant output substitutes for a calculation.

## Phase 3: Native executable evidence

- [x] Execute nominal source/calculated and literal source-input/accounting scenarios. Save all native heat/work/electric terms, source comparisons, support/definedness, capacity checks and residuals. Preserve unsuccessful attempts.
- [x] Verify independent energy identities, primary exchanger limits and monotonic closure. Check zero UA with positive selected fusion power, selected-zero-power refusal, recuperator bypass, invalid/nonfinite inputs, invalid mode/fractions, nonconvergent refusal, signed net/motor path, source accounting discrepancy and efficiency undefinedness at zero heat. Retain any cooling-only domain refusal for zero-UA integrated points; directly test the ledger's zero-heat branch when needed. Do not mirror the completion and claim independent physical validation.
- [x] Test insufficient/sufficient supplied heat, shaft, rejection, generator and fuel-processing capacities at fixed demand. Show hardware values unchanged and appropriate constraint transitions. Test a plasma-density perturbation with all equipment fixed and trace fuel/heat/cycle/net changes. Record inventory/cost as out of scope rather than implied tested.
- [x] Run scoped model validation and preservation manifest check. Report static limitations separately from actual native execution. Obtain consequential integrated-behavior review, including one upstream dependency trace and MR-7 verdict.

## Phase 4: Package and study handoff

- [ ] Provide accepted sealed package, snapshot/census, manifest/oracle, canonical scenario inputs and exact grouped entry-key mapping to coordinator. No promotion before applicable review.
- [ ] Coordinator runs native integration and one committed study under the goal round. Author repairs only scoped findings; semantic changes discovered by a study follow the reviewed disposition and subsequent round.
- [ ] Record report, supported boundaries, comparison classification, adverse/unsupported points and successor inventory/cost needs. Update this checklist as work completes. Formal closure remains owner-held.

## Implementation notes

2026-09-22: Forty native scenarios pass their stated expectations (30 evaluated, 10 refused); package fingerprint `469191fd32c624ccf70e0b4ebc1065b34920df8174c37a09e8f45ecfb241a7d7`. The calculated nominal has zero unmet heat and 423.106794 MW net output. Source-conditioned scenarios retain heat-removal failures. All eight selected capacity pairs switch correctly with demand unchanged. L1–L5 pass; L6 retains 182 identified EXPOSE diagnostics. Three harness-only failures and the initial syntax failure are preserved in evidence. Independent completion review PASS is in the goal evidence/implementation-review.md. Native goal integration/study remains the coordinator handoff; see report.md.

## T-007 integration prerequisite repair

- [x] Preserve first native integration refusal and reproduce exact smart-regeneration behavior in a scratch package.
- [x] Add typed public adapters with original module/body AST identity retained; update build to verify the integration producer's exact flags.
- [x] Verify all four native canonical scenarios match every old-seal output/input exactly; preserve original baseline and forty-case receipts.
- [ ] Obtain focused corrective review and retry native integration under the new executable fingerprint.

The normalized executable fingerprint is `cebe17fd3ca0dae4c5102365b384cc40635406b3c470c29dd7f55c086b9657bd`. Source/model identity is unchanged. The fourteen-file package diff consists of thirteen typed adapters and the package contract; see report.md and evidence/smart-normalization-verification.json.
