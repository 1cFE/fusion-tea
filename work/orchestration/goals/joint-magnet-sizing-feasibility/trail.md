# Trail: Joint magnet sizing and feasibility

## Round 1 — inventory-derived-sizing

### Strategy revision — 2026-09-15

- **Approach:** Derive required inventory from actual-field tape capacity; express it through the existing physical inventory coordinate if sufficient, and compare resulting pack demand against independent allocations with every existing plant consequence.
- **Assumptions:** Existing fixed-construction inventory law may support coherent sizing without changing production equations. Default performance is held; enhanced scenarios remain separate.
- **Abandonment conditions:** An unmodeled dependency invalidates the intended comparison or the existing coordinate cannot represent one consistent inventory.
- **Intended model increment:** Only behavior required for coherent joint sizing; none if a reviewed study-level inversion of existing equations suffices.
- **Intended study question:** Does any bounded sampled default-performance geometry accommodate current-sized inventory and satisfy all existing predicates, and what limits/costs result?

### T-001 scope

- **Objective:** Map coupled requirements, variable roles, existing evidence and the simplest consistent sizing formulation.
- **Why now:** Separate historical fit and current failures do not answer joint sizing.
- **Scope:** Read current equations, original admitted evidence and prior records; derive interfaces and missing-dependency limits. No production changes or scientific sweep yet.
- **Inputs:** goal.md; entering current, fit, procurement, thermal/support and manufacturing models and their audited sources.
- **Done when:** A traceable map and reviewed formulation determine whether production changes are necessary.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-001 start — 2026-09-15

T-001 · existing model/evidence assessment · evidence/coupled-requirements.md.

### T-001 return — 2026-09-15

- **Outcome:** COMPLETE.
- **Evidence:** evidence/coupled-requirements.md; evidence/coupled-dependencies.md (assessment in progress); work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md, unpinned; no native digest yet.
- **Reading:** Existing allocation-first field calculation permits acyclic current sizing. A native derived-density selector is necessary to internalize inventory demand under STUDY_POLICY; no outer solve or new empirical law is needed.
- **Decision:** Missing current-driven inventory behavior · register WI-064 with optional sizing and mode0 preservation · execution detail · coordinator under owner autonomy · native item/spec. Scope selected-field ceiling remains24.9T in principal comparisons; historical30T cases are controls only.

### T-002 scope

- **Objective:** Implement and verify optional native current-driven tape/pack sizing with preserved entering behavior.
- **Why now:** T-001 identifies the missing causal calculation and acyclic insertion point.
- **Scope:** WI-064 native model/generated/oracle consumers, focused tests, affected regression, metadata and independent coupled audit; no acceptance changes or new material normalization.
- **Inputs:** goal.md; WI-064 spec; entering revision c4d720db886213de94bf2dc4c3131a3453dca690; T-001 map and inherited source reviews.
- **Done when:** Reviewed native/generated/oracle agreement and current-package preservation support integration.
- **Stop when:** Prerequisite, strategy blocker, owner gate or declared limit.

### T-002 start — 2026-09-15

T-002 · WI-064 · reviewed specification, implementation and independent audit; focused source/design reviewer dispatched before implementation.
