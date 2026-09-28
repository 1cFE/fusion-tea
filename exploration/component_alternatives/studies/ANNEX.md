# Matched conversion comparison study annex

This package compares the selected steam offer with tested helium Brayton offers at matched source conditions. The metric is conversion-subsystem cost per net MWh. Model authority is the independently reviewed fourth design in `work/active/WI-096_matched-conversion-subsystems/design.md`; limitations and scope remain part of that authority.

## Package and execution

The generated package is `exploration/component_alternatives/component_alternatives_tea`. Its source assembly is `models/designs/component_alternatives/plant.sysml`; the reproducible input-model collection, build script, snapshot, census and development verification are in the parent exploration directory.

`study_route.py` uses the stock strict `ProvisionalPackageLoader`, `PreparedEvaluator`, `CandidateBridge`, `StudyRunner`, `PreparedListStrategy`, `StudyStore` and `StudyQuery`. It changes the existing costed-loop route's package identifiers only. It performs no physical calculation. The study chooses direct operating inputs and explicit equipment offers; all physical closure is inside the generated model's calculations. Glue ledger: none.

`execute_study.py` requires a matching successful native integration return, the clean package and a complete declared point list. It preserves completed points and failed evaluations in the native store, and refuses completion if any declared point did not evaluate. It refuses to overwrite an existing results directory.

## Baseline pin

The nominal development point chooses 2500 MW reactor heat, 2000 kg/s Brayton flow, three compressor ratios of 1.5, the 25/25/25 MW/K cooler offer and 60 MW/K recuperator UA. The steam side chooses 14 exchanger circuits and four 250 kg/s salt pumps per circuit. Both branches purchase the declared 2000 kg/s bypass-flow controller offer. These are independent selections, not outputs of a matching or sizing search.

`prepare_interface.py` discovers the complete input, numeric-output and executing-constraint catalogs from the generated contracts and an evaluated native receipt. It requires a clean package before writing `interface_data.py` or `manifest.json`. The manifest pins the actual receipt's complete inputs, headline and constraint verdicts, with predeclared numerical tolerance classes. A failed engineering predicate is recorded as failed; the manifest does not change its meaning.

The stock integration seam executes that exact baseline and checks package identity, regeneration fixed point, model-family coverage, source snapshot, manifest, read coverage and numerical verification. The returned candidate is the main study's required lineage evidence.

## Declared ties

Each declared axis names one independently chosen SysML attribute and its complete emitted entry-key set. `declare_axes.py` checks the names against the native metadata. This assembly emits the declared attributes once each in its plant input group. No extra physical identity between different attributes is inferred.

The proposal catalog may coordinate choices: equal selected compressor ratios, common financial conventions and a named cooler/recuperator/quote combination. These are explicit scenario choices, recorded in the point list. A service offer contains different physical quantities, so its cooler UA, recuperator UA and quote remain separately declared attributes even when a proposal changes them together. Common source heat and its operating state are shared through model bindings.

## Oracle

The package development verifier owns the independent equations and predicate operands. The study's `oracle_entry.py` exposes its `evaluate`, `comparison_catalog` and `operand_bindings` APIs without adding physical arithmetic. Numerical verification must distinguish independent calculations from translation parity that reuses a component body or property implementation. Reused values never become independent scientific evidence merely by appearing in an oracle response.

All executing predicates must be re-derived from the oracle's recorded operands and the sealed predicate IR. Near-zero convergence channels use the reviewed predeclared absolute tolerance classes; strict equipment/property inequalities keep their physical meanings. The final record lists what the verifier independently covered and what it reused.

## Candidate range and validity masks

The fourth design declares the source, flow, ratio, steam equipment and Brayton service catalogs before study execution. The oracle scans those choices directly, preserving full inputs and refusal reasons. It then fixes the executable list. There is no outer source-power, ratio, flow or equipment-sizing root in a study script.

Candidates that return numerical results with failed engineering checks remain eligible for native execution as failed cases. A body refusal is retained in the scan evidence and excluded from the native point list, whose contract requires every point to evaluate. Ranking requires the applicable physical checks to pass. A matched pair additionally requires both branches to pass at its shared source condition.

The window is engineered. It is not a sourced equipment operating envelope or a proof of a global optimum. The held steam offer does not establish supported variation of its 445/445/42 °C temperature conditions. Those proposed axes and salt-head changes still appear in the declaration and indicator record, with their refusal evidence and declined disposition.

## Accounting and claim limits

Each conversion subsystem includes its source exchanger, required conversion transport and machinery, controller, coolant pumping, heat rejection and declared capital/recurring/replacement accounts. Recovered primary circulation work is already present in delivered source heat; upstream primary electricity is context outside the conversion-subsystem metric. Both branches use the same source and finance convention.

Controller pressure service, gas aggregate pressure loss, low-grade loss cooling and site water service remain conditional assumptions. Machine maps, detailed valve/site hydraulics and complete installed-price coverage remain unqualified. Hypothetical quote factors and efficiency offsets test sensitivity; they do not establish those missing facts. Unknown cost scope is carried as a correction frontier. The study cannot claim equally optimized technologies, whole-plant LCOE or an unconditional procurement recommendation.
