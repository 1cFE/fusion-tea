# WI-089 executable plan

Status: design review pending
Created: 2026-09-22
Updated: 2026-09-22
Related Artifacts: spec.md; design.md

## Phase 1: Resolve design and source gate

- [x] Inspect actual WI-083/085/086/087 definitions, source images, typed completions and native build route; record roles, reuse, interfaces, equations and single assumption register.
- [ ] Independent reviewer accepts new source interpretation, heat-driven closure, parameter roles, support semantics and electrical ledger. Resolve findings before production implementation; coordinator records accepted candidate identity.

## Phase 2: Add one native assembly

- [ ] Add only the two new SysML paths in design.md. Stage unchanged reused definitions and imported plasma case. Add domain-guarded generic typed completions for selector/partition, heat-driven closure/passive recuperator and electrical/plant ledgers; preserve named component ownership and all exposed outputs.
- [ ] Generate `exploration/aries_integrated/aries_integrated` through `.codex-test/run sysml-codegen` after checking actual help. Install completions, regenerate with `--preserve-handwritten`, prove fixed-point identity, retain source/completion hashes and tracked staging root plus exactly one snapshot. Coordinator owns shared registries and integration packaging handoff.
- [ ] Inspect generated parameter schema and graph: selector feeds both fuel and heat; turbine temperature comes from closure; ratings/UA/flows/ratios remain entries; no source output or caller-derived plant output substitutes for a calculation.

## Phase 3: Native executable evidence

- [ ] Execute nominal source/calculated and literal source-input/accounting scenarios. Save all native heat/work/electric terms, source comparisons, support/definedness, capacity checks and residuals. Preserve unsuccessful attempts.
- [ ] Verify independent energy identities, primary exchanger limits and monotonic closure. Check zero UA with positive selected fusion power, selected-zero-power refusal, recuperator bypass, invalid/nonfinite inputs, invalid mode/fractions, nonconvergent refusal, signed net/motor path, source accounting discrepancy and efficiency undefinedness at zero heat. Retain any cooling-only domain refusal for zero-UA integrated points; directly test the ledger's zero-heat branch when needed. Do not mirror the completion and claim independent physical validation.
- [ ] Test insufficient/sufficient supplied heat, shaft, rejection, generator and fuel-processing capacities at fixed demand. Show hardware values unchanged and appropriate constraint transitions. Test a plasma-density perturbation with all equipment fixed and trace fuel/heat/cycle/net changes. Record inventory/cost as out of scope rather than implied tested.
- [ ] Run scoped model validation and preservation manifest check. Report static limitations separately from actual native execution. Obtain consequential integrated-behavior review, including one upstream dependency trace and MR-7 verdict.

## Phase 4: Package and study handoff

- [ ] Provide accepted sealed package, snapshot/census, manifest/oracle, canonical scenario inputs and exact grouped entry-key mapping to coordinator. No promotion before applicable review.
- [ ] Coordinator runs native integration and one committed study under the goal round. Author repairs only scoped findings; semantic changes discovered by a study follow the reviewed disposition and subsequent round.
- [ ] Record report, supported boundaries, comparison classification, adverse/unsupported points and successor inventory/cost needs. Update this checklist as work completes. Formal closure remains owner-held.
