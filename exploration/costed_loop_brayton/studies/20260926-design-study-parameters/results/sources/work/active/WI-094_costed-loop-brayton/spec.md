---
Status: active
Scale: standard
Epic: null
Owner: reid
Created: 2026-09-26
Updated: '2026-09-26'
---

# Costed loop-Brayton assembly

## Problem and intended use

[INHERITED: goal `design-study-parameters`, owner brief] The owner wants a fair performance-and-cost study of how cycle mass flow and compressor stage pressure ratio should be chosen together for the Stellaris helium-loop / ARIES Brayton combination (the WI-093 C-1 assembly). That assembly executes and passes every check at its starting point but carries no purchase, ledger, fuel or lifecycle part, so it cannot report an LCOE or cost contributions. This item builds a goal-owned costed variant of C-1 from existing definitions only, as the goal's fresh-reviewed comparison contract (`work/orchestration/goals/design-study-parameters/evidence/comparison-contract.md`, v2) specifies, so the study can read net electricity, the checks, the purchases and a conditional LCOE with its contributions on every point.

## Requirements

- R1 [NEED, brief item 3] Reuse existing equations and cost machinery: the assembly instantiates the C-1 physics unchanged and the ARIES 'Selected Equipment' / 'Selected Inventory Purchase' leaves for the five screened ratings and the exchanger, the fixed conversion-services budget, the fuel chain ('Fuel Cycle Flows', 'Selected Stock Atoms', 'Annual Selected Fuel', 'DT Fuel Cost') on a supplied fusion power, the capital chain ('Eight Amount Sum', 'Indirect Cost', 'Contingency Cost', 'Scaled Amount'), 'Annual OM Cost', 'Replacement Events', 'Equipment Cost Ledger', 'Levelized Annual Cost', 'Lifecycle Cashflow Accounts' and 'LCOE DCF', each bound as the ARIES assembly binds it. No new `calc def`, `part def`, `constraint def` or `port def`; no change to any reviewed completion body (a prefix-rewritten copy is reuse).
- R2 [NEED, contract § 3, § 6] The held-equal terms are supplied constants with their basis: the fusion power behind the supplied heat (2,652.5631770825056 MW, `[INHERITED: Stellaris baseline]`), the rest-of-plant capital (2,158,230,133.3333335 USD2004, `[ASSUMED]`, derived in the contract § 6), the replacement event scope (72,231,350 USD2004, `[ASSUMED]`), the ARIES fuel, O&M, consumables and finance conventions.
- R3 [NEED, MR-7] Every quantity's role is stated (chosen, calculated, requirement, installed capacity); purchases are computed from the selected ratings and area, never from demand; an inadequate selection stays a violated screen with its booked price; the loop's calculated flow is the disclosed inherited direction; the fixed machine efficiencies are model assumptions, not choices; no sizing rule is introduced.
- R4 [NEED, MR-4] Every value carries its source and grade (`[INHERITED: Stellaris]`, `[INHERITED: ARIES]` with the line range, `[ASSUMED]` with the reason).
- R5 [NEED, contract § 9] The five WI-093 C-1 cases replay on the costed package with every C-1 channel bit-exactly equal to its sealed value (the pre-change control); the electrical balance's exhaust-driven fuel term stays 0 as in C-1.
- R6 [NEED, brief items 5–6] The cost boundary is single-counted and the LCOE is reported with its eleven contributions and the annual net energy denominator; identities on stored outputs verify the purchases, the capital chain, the annual accounts and the contribution sum (the WI-087 pattern), not a second implementation.
- R7 [INFERRED] The package carries the study tooling the runbook route needs (route, interface record, manifest with the declared tolerance classes, executor, package-owned oracle with operand bindings, annex, discovery log) and obtains an integration CANDIDATE, so the goal's study can run on it.
- R8 [INFERRED] The new design directory is registered in `tests/model_families.py`; the package builds to a fixed point under stock regeneration with preserved handwritten bodies; the Stellaris, ARIES and combinations packages, the library and every live assembly are unchanged (goal preservation manifest).

## Scope and limits

In scope: `models/designs/costed_loop_brayton/costed_loop_brayton.sysml`, `exploration/costed_loop_brayton/` (build, package, snapshot, census, run, verify, studies tooling, evidence), the registry entry. Out of scope: any library or body change; the study itself (the goal's T-005); scientific qualification of any inherited value; the Stellaris side's own costs (held as the rest-of-plant constant); machine maps. Review: focused fresh design review before implementation (new bindings of the ARIES cost definitions onto a Stellaris-loop assembly; one part specialisation changed) and a fresh implementation review after.

## References

Goal `work/orchestration/goals/design-study-parameters/` (`goal.md`, `evidence/comparison-contract.md` v2, `evidence/contract-review.md`, `evidence/starting-configuration.md`, `evidence/screen-flow-ratio.md`); WI-093 (`work/completed/20260926_WI-093_combination-assemblies/{design,report}.md`); `models/designs/aries_cs_integrated/plant.sysml`; `modeling_project/REQUIREMENTS.md` MR-3, MR-4, MR-7; `exploration/combinations/build.py`; `exploration/aries_integrated/studies/` (route, oracle and executor patterns).
