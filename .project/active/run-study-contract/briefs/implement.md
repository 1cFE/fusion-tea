# Brief: implement "Skill, Runbook, and Record Contract" (RUN-STUDY Item 2)

Execute `.project/active/run-study-contract/plan.md` phase by phase. Spec, design, and plan
are ACCEPTED (Status headers say so). Tick checkboxes as you complete phases; add per-phase
completion notes; run each phase's check stencil before ticking.

Orchestrator ruling resolving the plan's open seam (Phase 3): the
`manifest.content_used.fingerprint_names` list is DERIVED AT SNAPSHOT TIME from Item 3's
manifest `fingerprints` block, flattened to dotted-path names (`indicator_inputs`,
`recorded_provenance.executable_fingerprint`, `recorded_provenance.semantic_fingerprint`).
No Item 3 manifest change. The plan's "awaiting owner confirmation" marker is resolved by
this ruling — implement accordingly and note it in the phase completion.

Item 3's design is Accepted (not Draft — headers updated); still re-check every copied field
name against `.project/active/run-study-indicators/design.md` at implement time as the plan
requires. Item 3's implementation runs in parallel with yours — read its DESIGN, not its
work-in-progress code.

Commit at each phase boundary with a message leading with what the phase delivered.
Do not edit files outside: `.claude/skills/run-study/`, `.gitignore`,
`.project/active/run-study-contract/`. (The dry run WRITES its findings to
`.project/active/run-study-contract/dry-run.md`; it reads the proof-of-life directory
read-only.) End with ARTIFACT: <plan path> and a one-paragraph summary of deviations if any.
