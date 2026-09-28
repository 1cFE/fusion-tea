# WI-098 independent numerical verification brief

Coordinator assignment, 2026-09-27. Owner endpoint is evidence/owner-brief.md. Requirements and design are work/active/WI-098_whole-plant-conversion-comparison/{spec,design,configuration}.md. The independent pre-implementation review is evidence/boundary-review.md; F1–F3 are under correction. Do not implement changed equations until the coordinator identifies the accepted revision.

## Ownership and immediate scope

You own exploration/whole_plant_conversion/verify.py, oracle_*.py, and WI-098/evidence/independent-verification/**. Conversion author owns models, native bodies/build/run, capture and development receipts. Coordinator owns studies/** and goal artifacts. You are not alone; preserve others' edits. Do not import production whole-plant bodies into the oracle or change predecessor files.

First port only the already verified conversion oracle and its name/binding machinery to the isolated namespace. Preserve arithmetic and record reversible namespace changes. Reuse valid prior evidence from exploration/component_alternatives/verify.py and oracle support plus the sealed 498-case record; do not rerun old baseline studies. Inspect the verifier contracts consumed by studies/oracle_entry.py. Return readiness and any required interface information. This initial assignment does not authorize the unreviewed new source/fuel/ledger equations.

## Scope released after design PASS

Independently derive every new calculation and constraint from the accepted design and original equations. Verify exact native 48 kA capture, conservative nuclear envelope, fixed inventory and repricing against original inputs/equations. Verify new full-source fuel/power/account/lifecycle outputs, predicates and conservation; expose evaluate, operand_bindings, comparison_catalog and absolute_tolerances contracts for stock study verification. Retain iteration diagnostics as explicitly excluded rather than falsely independent comparisons. Capital membership and event schedules need independent enumeration; no opaque copied total accepted as verification.

MR-7: selected capacities, quantities and quote bases stay supplied. Required tests cover insufficient/sufficient selected equipment and demand-only changes with capital invariant, fixed capture identity, heating/primary-work ownership, adverse source/current/domain/cooling/stock/processing/outage/net cases, integer lifetime and discount-zero endpoints. Reuse original independently derived thermal oracles with package namespace edits only. A material numerical discrepancy is a failure to investigate; never copy a native error or widen tolerance to pass it.

Use .codex-test/run for Python and native tools; read .project/codex-test-setup.md before execution. Retain receipts/scripts, exact commands and concise report in your evidence subtree. No commit needed; coordinator commits coherent increments with explicit paths. Budget: finish the bounded complete numerical verifier and relevant development checks; report a named missing interface promptly rather than inventing one.
