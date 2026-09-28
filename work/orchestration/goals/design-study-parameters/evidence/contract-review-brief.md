# Review brief: comparison contract for the cycle-flow / pressure-ratio study (fresh, focused)

You are a fresh reviewer with no prior context. Do not orient yourself in the project: do not read trails, goal directories other than the two files named here, prior reviews or precedent collections; do not delegate; do not run test suites. Budget: about ten tool calls and a 400-word return (broadened from the default six and 300 because five questions are asked). If evidence named here is missing or the budget cannot establish coverage, return the specific missing evidence and your uncertainty without a passing verdict.

## The question

A goal is about to build a costed variant of an existing SysML assembly (a Stellaris helium primary loop feeding an ARIES helium Brayton cycle) and sweep two operating inputs on it. Before anything is built, review the comparison contract at `work/orchestration/goals/design-study-parameters/evidence/comparison-contract.md` (version 1) and answer its § 13 questions 1–5. Return a verdict of PASS, FINDINGS (with each finding marked correct-before-execution or note) or OWNER_GATE (a premise conflict that the owner must rule on), with the evidence you checked for each question.

## Entry files and sections

- The contract: `work/orchestration/goals/design-study-parameters/evidence/comparison-contract.md` (all sections).
- The starting-point statement and the screen reading: `work/orchestration/goals/design-study-parameters/evidence/starting-configuration.md` (§ 4–6), `work/orchestration/goals/design-study-parameters/evidence/screen-flow-ratio.md` (§ 3–5); the screen data `screen-flow-ratio.json` in the same directory (per-point `values`, `margins`, `verdicts`).
- The assembly the study starts from: `models/designs/combinations/combinations_loop_brayton.sysml` (bindings of the loop, cycle, compressors, exchangers, electrical balance, screens and checks).
- The reviewed bodies that define the arithmetic: `exploration/aries_integrated/aries_integrated/handwritten/integrated_heat_electricity/plant_electrical_balance_impl.py`; `exploration/aries_integrated/native_completions/network_heat_driven_closure_impl.py`; `exploration/aries_integrated/native_completions/equipment/equipment_cost_ledger_impl.py`; `exploration/aries_integrated/native_completions/lifecycle/lifecycle_cashflow_accounts_impl.py`; `exploration/aries_integrated/native_completions/equipment/selected_inventory_purchase_impl.py`; `exploration/aries_integrated/aries_integrated/handwritten/ideal_gas_brayton_components/ideal_gas_compressor_impl.py` and `ideal_gas_expander_impl.py` (fixed-efficiency ideal-gas stages).
- The ARIES assembly's cost bindings the contract copies: `models/designs/aries_cs_integrated/plant.sysml` lines 1595–1666 (fuel inventory) and 1951–2231 (direct, indirect, contingency, owner, O&M, replacement, ledger, finance, lifecycle, price).
- The original sealed channels behind the rest-of-plant constant: `exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/cases.json`, case `baseline-no-credit`, outputs `aries_integrated_plant__direct_source_scope__evaluate__total` and the seven `*__purchase__capital` / `conversion_services__purchase__cost` channels the contract § 6 names.
- The requirement the roles must satisfy: `modeling_project/REQUIREMENTS.md` § MR-7 (a supplied equipment choice stays the basis of its cost; no quantity is sized from demand; validity reported separately from adequacy).

## Expected checks

For each of the five questions: what you read, what you computed or compared, and the finding. For question 3, state whether any numerator term of the LCOE varies with the swept inputs within one inventory. For question 4, say whether the contract's statement of the fixed-efficiency assumption (§ 8 a) and its sensitivity S1 are an honest treatment or whether the operating claim must be narrowed before execution, and why. For question 5, recompute at least two I-A margins from `screen-flow-ratio.json` demands.

## Exclusions

Do not evaluate whether the study will find anything interesting; do not propose new physics; do not re-derive the Stellaris loop or the Brayton closure beyond what the questions need; do not read the owner brief or the goal trail.
