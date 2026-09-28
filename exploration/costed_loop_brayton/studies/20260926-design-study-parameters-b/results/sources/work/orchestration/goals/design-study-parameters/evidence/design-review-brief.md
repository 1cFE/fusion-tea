# Review brief: WI-094 costed loop-Brayton assembly design (fresh, focused)

You are a fresh reviewer with no prior context. Do not orient yourself in the project: do not read trails, goal directories other than the files named here, prior reviews or precedent collections; do not delegate; do not run test suites or the generator. Budget: about ten tool calls and a 400-word return. If evidence named here is missing or the budget cannot establish coverage, return the specific missing evidence and your uncertainty without a passing verdict.

## The question

A modeling work item is about to add purchase, fuel, ledger and lifecycle accounting to an existing SysML assembly (a Stellaris helium primary loop feeding an ARIES helium Brayton cycle) by instantiating existing ARIES definitions, so that a study can read a conditional LCOE on it. Review the design `work/active/WI-094_costed-loop-brayton/design.md` and its draft assembly text `work/active/WI-094_costed-loop-brayton/evidence/draft-costed_loop_brayton.sysml` against the four questions in the design's § 10. Return PASS, FINDINGS (each marked correct-before-implementation or note) or OWNER_GATE, with the evidence you checked per question.

## Entry files and sections

- The design: `work/active/WI-094_costed-loop-brayton/design.md` (§ 1–§ 7, § 10) and its spec `spec.md` (R1–R6).
- The draft assembly: `work/active/WI-094_costed-loop-brayton/evidence/draft-costed_loop_brayton.sysml` (the cost parts begin at `part fusion_source`; the C-1 parts above them are the unchanged WI-093 text except `part he_hx` and the package/root names).
- The C-1 original it extends: `models/designs/combinations/combinations_loop_brayton.sysml` (compare `part he_hx`, `part electrical`, `part checks`).
- The definitions bound: `models/library/analyses/integrated_equipment_costs.sysml` ('Selected Inventory Purchase', 'Exchanger Area Conductance', 'Selected Stock Atoms', 'Annual Selected Fuel', 'Replacement Events', 'Eight Amount Sum', 'Scaled Amount', 'Equipment Cost Ledger'), `models/library/analyses/integrated_lifecycle_costs.sysml` ('Lifecycle Cashflow Accounts'), `models/library/analyses/mfe_account_costs.sysml` ('Supplied Purchase Cost', 'Indirect Cost', 'Contingency Cost', 'Annual OM Cost', 'Levelized Annual Cost', 'DT Fuel Cost'), `models/library/analyses/mfe_lcoe_dcf.sysml` ('LCOE DCF'), `models/library/analyses/mfe_fuel_cycle.sysml` ('Fuel Cycle Flows'), `models/library/structure/integrated_equipment_parts.sysml` and `models/library/foundation/costed_component.sysml` ('Selected Equipment', `cas_code`, `capital_cost`).
- The ARIES assembly whose bindings are copied: `models/designs/aries_cs_integrated/plant.sysml` lines 110–141 (fuel), 709–749 (cost accounts, schedule, he_hx), 801–819 and 1050–1162 (purchase leaves), 1595–1666 (fuel inventory), 1951–2232 (capital chain, O&M, replacement, ledger, finance, levelization, lifecycle, price).
- The bodies whose formals the bindings must match: `exploration/aries_integrated/native_completions/equipment/{equipment_cost_ledger_impl.py, annual_selected_fuel_impl.py, replacement_events_impl.py}`, `exploration/aries_integrated/native_completions/lifecycle/lifecycle_cashflow_accounts_impl.py`, `exploration/aries_integrated/aries_integrated/handwritten/integrated_heat_electricity/plant_electrical_balance_impl.py`.
- The requirement: `modeling_project/REQUIREMENTS.md` § MR-7. The contract the design serves: `work/orchestration/goals/design-study-parameters/evidence/comparison-contract.md` § 3, § 5, § 6.

## Expected checks

Q1: for each cost part, that every `in` name exists as a formal of the named definition and the bound sibling attribute exists with the right units (MW, USD, kg, years, atoms/s); flag any self-named binding (a formal bound to an attribute of the same name in the same scope) that would shadow. Q2: that no rating, area, capacity or purchase is derived from a demand, and that the purchase leaves read the screens' `selected_rating` attributes, not the demands. Q3: that direct = rest_of_plant + the seven priced items + the tritium stock, with nothing counted twice (the seven items are subtracted from the rest-of-plant constant in the contract § 6), and that the loop's friction heat and pump electricity enter once each. Q4: whether the changes from C-1 (the `he_hx` specialisation to 'Selected Equipment' with a purchase calc added; the cost parts appended; `fuel_exhaust` kept at 0.0) can change any C-1 output channel's value; say yes or no with the reason.

## Exclusions

Do not evaluate the study design or the economics; do not propose new definitions; do not read the owner brief or the goal trail; do not run anything.
