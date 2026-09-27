# Independent verifier readiness: conversion port

[AGENT] The reversible conversion-oracle port is ready. New whole-plant equations remain unimplemented pending the coordinator's explicit accepted-design release. This is not a complete whole-plant verifier or an independent design approval.

## Owned artifacts

- `exploration/whole_plant_conversion/verify.py` — predecessor authored-binding evaluator and predicate verification, with isolated package/model/result paths and namespace-safe relative imports.
- `oracle_gas.py` — predecessor gas/primary arithmetic with the package prefix changed only.
- `oracle_cooling.py`, `oracle_matched_cycle.py`, `oracle_matched_cycle_properties.json`, `oracle_thermal.py` — byte-exact predecessor copies.
- `conversion-port-manifest.json` — every source/target SHA256 and declared transformation.
- `check_conversion_port.py` and `conversion-port-check.json` — reversible-source comparison, import/API checks and isolated gas-oracle arithmetic comparison.

[AGENT] Verification command: `.codex-test/run python work/active/WI-098_whole-plant-conversion-comparison/evidence/independent-verification/check_conversion_port.py`. All six files reconstruct the exact predecessor bytes when their declared namespace/import edits are reversed. All source hashes remain unchanged. The inherited gas oracle returns116 channels bit-exactly after prefix remapping at the retained input defaults. Python compilation and API import checks pass. No native package or old study was executed; this narrow check does not replace the retained498-case numerical evidence or qualify new whole-plant bindings.

## Retained evidence and contracts

[INHERITED] Numerical authority for unchanged conversion equations remains `exploration/component_alternatives/studies/20260926-design-study-component-alternatives-b/record.md`, its sealed498-case results, and predeclared `numerical-tolerances.json`. This port does not revise oracle arithmetic or numerical tolerances. Iteration diagnostics remain excluded from numerical comparisons.

[AGENT] The module exports `evaluate(point)`, `operand_bindings()`, `comparison_catalog()` and `absolute_tolerances()`. The predecessor `studies/oracle_entry.py` exports only the first three; the new coordinator-owned adapter should explicitly export all four. The stock verifier consumes the comparison catalog and binding map; the new study manifest must retain the declared absolute classes. `comparison_catalog()` currently requires a generated package and fully implemented accepted calc interfaces, so it must not be treated as ready for the new full assembly yet.

[AGENT] The evaluator reads flat named `part` occurrences and authored `calc` input bindings from `models/designs/whole_plant_conversion/plant.sysml`; generated inputs provide chosen values; pipeline metadata supplies constraint operand locations only. No native numerical body is imported. Anticipated prefix is `whole_plant_conversion__plant__`; package is `whole_plant_conversion_tea`. Author was informed to preserve existing named conversion occurrences and provide final new calc names/formals/outputs. Unsupported new calculation names deliberately raise an error instead of silently omitting verification.

## Release dependencies

[AGENT] Await accepted design/configuration identity and final new calc interfaces before independently deriving source/fuel/power/cost/events/DCF equations. The finance-key migration must reject inconsistent legacy branch values and map them to the single shared finance part; the current port does not invent this migration. Exact48kA capture, conservative nuclear-envelope calculation, monetary repricing breakdown and native selected-capability receipts are also required for the subsequent independent capture check. Missing interfaces will be reported, not inferred from native implementation arithmetic.
