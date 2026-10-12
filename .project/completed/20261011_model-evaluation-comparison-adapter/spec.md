# Model evaluation comparison adapter

Status: design review pending. Owner: T-003 author. Created: 2026-09-20.

[NEED] Prepare a usable, versioned comparison adapter against the repaired evaluator using only synthetic fixtures and model defaults. Preserve the original comparison criteria and accounting, retain unsuccessful first attempts, and report unresolved scientific mappings. Authority: `work/orchestration/goals/model-evaluation-domain-readiness/goal.md`, T-003 author brief.

[INHERITED] MR-7 and WI-074–080 require independently supplied hardware and operating choices. The adapter must not restore retired sizing switches, choose turns from ampere-turns, resize equipment, or reprice an upgrade from running demand.

[INFERRED] The preparation interface accepts six compatible historical input quantities and two explicitly supplied current magnet controls. This is a proposed model-compatible selection contract, not an adopted replacement for the historical seven-input reference contract. Reference-coil ampere-turns alone are insufficient to choose installed turns and operating current. That request is refused pending a separate scientific mapping decision.

[INFERRED] A strict versioned request declares synthetic preparation, maps exact units and definition identifiers, and labels every unsupplied parameter held at the identified package default. All new reference comparison execution remains outside this preparation adapter. Missing reference-like quantities may use held defaults, but block a fully specified claim. Unknown, ambiguous, incompatible and retired inputs are refused before evaluation.

[NEED] Exercise native success, missing input, incompatible definition, unsupported-domain refusal and failed-first-attempt preservation. Completion means the native evaluator produced all expected outputs and verdicts; it never means scientific acceptance or authorization to compare/publish.

[INFERRED] Reserve an exclusive first-attempt record before decoding or running. Every subsequent attempt gets a separate directory and identifies the immutable first attempt. An interrupted first attempt remains reserved and incomplete. A later success cannot become the first result. Retain request bytes, native stores, tracebacks, selection, exports and package/adapter identities.
