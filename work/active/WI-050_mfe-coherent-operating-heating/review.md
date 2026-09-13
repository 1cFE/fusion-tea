---
Verdict: fail
Created: 2026-09-11
Related Artifacts:
  Design: ./design.md
  Spec: ./spec.md
---

# WI-050 independent design review

## Summary

The operating-heating separation, signed-demand behavior and cost classification are coherent. The proposed efficiency assertion introduces a concrete consumer incompatibility: native generation and execution succeed, but the existing indicator and independent verification tools reject its compound predicate. Revise that interface before implementation; the two introduced Level 6 diagnostics are a separate, nonblocking checker limitation on the demonstrated native route.

Reviewed contract `spec.md@54a0725e`, design/prototype `8abebd1d`, and alignment `d621ef14`. This reviewer is a fresh non-author. A separate fresh agent checked project requirements and architecture and returned pass. The skill requests four parallel checks; a second supporting spawn failed with `agent thread limit reached`. Under the parent's explicit instruction, this reviewer completed the remaining convention and validation checks locally. No author reviewed their own work. Only this review was written; no production, design, source, historical or package artifact was changed and no commit was made.

## Findings

### R1 — Compound efficiency predicate breaks supported consumers

- **Severity:** critical; blocks implementation of the proposed assertion shape.
- **Status:** proposed disposition, awaiting parent; not owner-ratified.
- **Where:** `design.md`, Design decisions and elements item 6 and Implementation and verification plan; `prototype/operating.sysml:10`; `scripts/study/indicators.py:450`; `scripts/study/verify.py:208`.
- **Evidence:** The generated prototype contract entry `stellarator_09__stellaris__heating_efficiency_ok__e7d023b396814481` has root operator `and` and nested comparisons. Calling the actual indicator parser on that entry raises `IndicatorError: unsupported nested operator 'and'`. Calling the actual verifier raises `VerifyError: predicate IR is not a comparison this tool can re-derive (kind 'operator', operator 'and')`. These failures occur before operand lookup. Both were reproduced with `.codex-test/run python` against the retained scratch package, without regeneration or package mutation.
- **Impact:** Updating a verdict count to 15 and adding operand bindings will not repair these failures. MR-WI050-7 requires affected direct consumers to remain usable; MR-WI050-8 requires independent verification. The prototype's strict evaluator establishes generated execution, not compatibility with these tools.
- **Required change:** Design an efficiency-domain representation within the existing consumers' supported comparison semantics and prototype it through both tools. Preserve exact rejection for either invalid efficiency, including negative, zero and greater-than-one cases. If retaining compound predicates instead, an explicit tooling change and its ownership/validation must be resolved before dependent modeling implementation; this review grants no such scope. Re-derive the resulting verdict count from generation rather than assuming it stays 15.

### R2 — Make consumer and boundary coverage explicit in the implementation contract

- **Severity:** concern; verification coverage, not a second demonstrated model defect.
- **Status:** proposed disposition, awaiting parent.
- **Where:** `design.md`, Caller inventory and Implementation and verification plan; `prototype/boundaries.py`; `prototype/probe.py`.
- **Evidence:** The retained boundary fixture executes direct-only default behavior and five signed-demand cases. Mixed and all-zero generic defaults are described algebraically and planned, but not executed in the retained fixture. Invalid source efficiencies are executed; invalid coupling efficiencies and the valid upper endpoint 1.0 for both stages are not separately covered. The full-plant coupling case at 0.8 checks conversion while deliberately exceeding capacity.
- **Required change:** Carry these cases into named implementation tests and verify the revised domain representation through the indicator and verifier, including its equality endpoints. Name affected live consumers: `exploration/stellarator_e2e/verify_stellaris.py`, `run_stellaris_single.py:99`, `studies/oracle_entry.py:409`, and `studies/study_route.py:49`. Cover the associated count/binding/verification expectations in `tests/study/test_operand_bindings.py:94`, `test_verify.py:97`, `test_valid_empty.py:39` and `test_known_answers.py:145`. Re-derive operand occurrence counts and generated identifiers. Historical study records and their frozen interpretations remain preserved; a text search match is not permission to rewrite them.

### R3 — Retain the generic default with explicit Level 6 limitation

- **Severity:** suggestion; no implementation blocker on the tested native route.
- **Status:** reviewer recommends accepting the design's proposed disposition; parent decision pending.
- **Where:** `design.md`, Quality levels and limitations; `prototype/validation-diff.json`.
- **Evidence:** Level 6 increases 227 to 229 with `Unsupported operator '.'` and the unextractable numeric-default diagnostic for `p_operating_coupled_heat`. They are introduced findings, not inherited debt. The expression is a pure producer exposure, not inline arithmetic. Native generation and strict execution accept it; the default fixture executes the installed producer's value; the stellarator contract contains 247 parameters and no operating-demand input. This reviewer reran the retained assertions confirming that contract property.
- **Assessment:** These results directly refute the diagnostics' implication that this expression cannot execute on the native generator used here. Preserve the differential report and repeat it after production changes. Do not call Level 6 passing, suppress the two findings, or interpret this assessment as a general fix to the checker. This disposition does not address R1, which is an independently reproduced failure in different consumers.

## Requirement assessment

| Requirement | Design assessment | Evidence and implementation obligation |
|---|---|---|
| MR-WI050-1 | Pass | One inverse producer gives coupled demand, delivered demand divided by coupling, and electrical draw divided by both efficiencies. Retained numerical identities pass, including non-unit coupling. |
| MR-WI050-2 | Pass, subject to R1/R2 coverage | Positive, exact capacity equality, exact zero, insufficient and negative demand execute in the component fixture. Negative demand stays signed and violates burn hold; insufficient demand violates the upper bound without clipping. Zero produces exact zero operation with positive installed procurement. Invalid efficiencies produce violated domain or explicit division failure, never an accepted substitute point. |
| MR-WI050-3 | Pass at design stage | Binding ledger and patch route one operating producer into source heat, thermal balance, electrical recirculation and divertor heat. Loop input follows source heat. Independent conservation checks pass. Production tests must inspect bindings and loop responses as planned. |
| MR-WI050-4 | Pass | ECRH procurement remains `heat.p_delivered`, ceiling remains `heat.p_coupled`. The 100/120 MW reserve pair preserves operating heat, source/loop/gross/net/divertor operation and changes procurement from $264145000 to $316974000. Demand control preserves procurement. The installed diagnostic gets an explicit new divertor input so it does not collapse to required-minus-required. |
| MR-WI050-5 | Pass | Every affected direct thermal, gross, net and electrical cost operand is inventoried with current/proposed binding and reserve/demand response. Rollups, installation, contingencies, indirect costs, spares, supplementary allowances, replacements and both LCOEs are traced. No unclassified changed cost basis was identified. |
| MR-WI050-6 | Pass at design stage | Equipment power scaling is explicitly a design-point estimate; annual fuel/energy remain consumption over time. Reserve affects installed procurement and its capital dependents, not online energy. Availability-only operation is invariant. Explicit financial formula verification remains required; reconstructed finance attribution alone is not independent financial validation. |
| MR-WI050-7 | Fail on R1 | Generic direct semantics and single-module scope are preserved algebraically; family ownership excludes shared IFE foundations. Native production/twin regeneration and isolation tests remain pending. Compound predicate consumers demonstrably fail and require design revision. |
| MR-WI050-8 | Incomplete by stage, R1 blocks readiness | Corrected baseline and 73 changed scalar outputs are retained with both financial bridges. Baseline still violates divertor heat at 10.517841546 MW/m^2 against 10. Positive independent implementation audit is still required. No feasible-plant or accepted residual claim follows. |
| MR-WI050-9 | Pass at design stage | Library definitions, design wiring, plain Real units and existing Source/Ref/Basis citations comply. Held-efficiency approximation is explicit. Production comments need the planned refinement. No new source, engineering curve, finance convention or historical revision is proposed. |

## Cost and isolation assessment

The definition of a demand-only test holds heating installation, not every costed plant component. Thermal/gross/net aliases change the retained design-point equipment estimates. The design distinguishes these responses from procurement and annual operating energy. Generic direct delivered procurement may differ from operating delivered heat: the fixture deliberately retains 50 MW purchased delivery and 30 MW coupled capacity, deriving 40 MW operating delivery and 80 MW electrical draw at efficiencies 0.5/0.75. This preserves the prior separately supplied procurement and coupled-power semantics; it does not claim a technology dispatch allocation.

The full-plant demand case changes retained alpha fraction from 0.95 to 0.96. Fusion remains unchanged while retained alpha rises and auxiliary demand falls by the same amount. Thus divertor absorbed heat stays fixed; this is explained by the exact controls, not used as proof of a disconnected divertor binding. Source heat uses full D-T alpha and therefore changes with auxiliary demand. Pure isolated-demand response expectations remain separate fixture/test obligations.

Independent PR/AD support found no architecture or project-requirement violation in the library placement, financial preservation, CAS structure, provenance or documented assumptions. AD-001/003/004/006/007 and project MR-1 through MR-6 are respected by the proposed split. No new economic parameter invokes AD-002.

## Verification performed and limits

Read the retained prototype patch, stencils, native result records, boundary driver and Level 2/6 differential. Reran `check_results.py` through `.codex-test/run` with its output redirected to `/tmp/wi050-review-checks.json`, preserving author evidence. Conversion, thermal/electric/divertor conservation, reserve procurement/invariance, demand alpha compensation, availability invariance, efficiency rejection and the 247-input/no-demand-entry assertion passed. The baseline bridge reconstructs net 1013.931932554 MW and headline LCOE 224.269232884 $/MWh; this is prototype evidence, not a promoted package.

Those physical identities are independent algebraic/conservation assertions over native outputs. They are stronger than matching a translated direct runner, but do not independently recertify the underlying confinement, coolant, radiation or financial source relations. The finance bridge derives annualized capital from LCOE and annual cost, so it establishes attribution only; the design correctly requires explicit unchanged-formula checks in implementation.

Levels 1, 3, 4 and 5 are reported passing in the retained copied-family validation. Level 2 retains ten unchanged warnings. Level 6 is 229 with two introduced findings, assessed under R3. Broad validation/generation was not rerun because no prototype model change was made; the targeted consumer experiment was sufficient to establish R1. Mixed/all-zero fixture cases, additional efficiency endpoints, production regression, direct/native parity and fresh implementation audit remain outstanding as recorded above.

## Accepted changes

None yet. Parent disposition is required for R1–R3. Recommended action: revise the efficiency assertion and explicit verification coverage, then perform focused independent re-review of the changed design and consumer evidence before planning.

## Deferred items

None assigned by this reviewer. The existing Level 6 checker limitation is disclosed under R3, not silently classified as inherited or fixed. No owner-reserved source, scope, financial or residual decision was made.
