# Goal-agent prompt: repair model design-choice violations

Prepared for the owner to send to a new agent. Preparing this file does not start the goal or authorize a new reference comparison. The instruction below becomes the task when the owner sends it for execution.

---

Use the run-goal skill to ground and pursue `preserve-model-design-choices`. That slug is supplied by this prompt; no additional slug confirmation is needed. The objective is to repair violations of MR-7 across the current stellarator model and its shared dependencies, while preserving physical relationships, explicit validity limits, and the ability to evaluate a supplied design without silently choosing different equipment. Complete the technical work through the native workflow, including independent reviews and relevant regression/integration evidence. Formal goal closure remains owner-held.

## Context and authority

Work on `fix/modeling-intent-after-reveal`, branched from verified pre-reveal checkpoint `86712a0d080d745802c1bcc57a30d3eca00458c3`. Do not reset the branch or discard subsequent enforcement commits. Inspect actual HEAD and worktree state. Preserve unrelated staged and unstaged work, especially `docs/write-up/sysml-codegen-model-evaluation.md`. Use explicit file lists for any authorized commits; no push, merge or replacement of published comparison archives is included.

Follow AGENTS.md, CLAUDE.md and the required bounded project-context reads. Read `.project/codex-test-setup.md` and `.agentic-mbse/codex.md` before Python/model commands. Use the prescribed runtime. Use native work-item/goal operations where the project requires them; avoid manually rewriting modeling registries.

Read these controlling records:

- `modeling_project/REQUIREMENTS.md`, especially MR-7; the owner-originated principle and the implementation interpretation have different provenance.
- `modeling_project/MODELING_PROCESS.md`, including MR-7 evidence and independent review obligations.
- `work/orchestration/GOAL_RUNBOOK.md` and the run-goal skill; use the native goal templates and explicit limits.
- `.project/active/demo-depth-rubric/application-policy.md`; historical depth scores are not proof of MR-7 compliance.
- `.project/active/modeling-intent-enforcement/spec.md`.
- `.project/active/aries-comparison-preparation/current-readiness/revealed-results/post-reveal-repair-results-note.md`.
- `work/analysis/20260920-184131_design-choice-assignment-audit.md`, if present. It is an initial source-level audit, not an exhaustive inventory or settled design. If absent, the starting surfaces below are sufficient; do not fetch reference-derived material to replace it.

The historical protocol at the restored baseline says sealed. The results note records that reveal occurred. This work is post-reveal repair from pre-reveal code, not a new blind experiment. Keep model-facing implementation based on the architectural requirement and independently supported relationships. Do not open extracted reference papers, numerical observations or the original reference request, including by checking out later evidence commits. Do not use agreement with reference outputs to choose equations, domains, design inputs or defaults. Preserve the experiment through its existing evidence branch and commits. This restriction limits further influence; it does not claim the task was selected before reveal.

## What to repair

The problem is not the word “sizing” or the existence of calculated outputs. It is a physical/equipment model silently deciding which design quantities are chosen and which must follow a demand or adequacy policy. Changing terminology, adding a multiplier or documenting an automatic choice is not sufficient remediation when the intended design cannot be evaluated independently of that choice.

Start by inventorying every affected public design quantity and binding across the stellarator instance, shared components, generated interfaces, study routes and cost consumers. For each, record the physical relationship, units, current variable roles, policy assumptions, actual binding paths, intended supported choices, and evidence for compliant/violated/unverified status. Distinguish geometry identities, operating-point closures, demand calculations, installed hardware, automatic design selection and cost proxies. Use whole-model traversal plus targeted code inspection; keyword search alone is insufficient.

Known starting surfaces, to verify rather than blindly adopt:

1. Magnet winding side derived from current/current density; field-grade conductor enlargement; current-driven inventory selection feeding installed winding geometry and cost. Inspect `models/library/cost_structure/mfe_power_core.sysml`, `mfe_magnet_field.sysml`, `mfe_conductor_grade.sysml` and `mfe_conductor_current.sysml` under `models/library/analyses/`. Turning off current-driven mode does not by itself restore design choice because the older geometry rule also fixes a variable assignment.
2. Facilities capacity mode that binds allocated storage positions to calendar demand and resizes buildings. Inspect `mfe_facilities.sysml`, its executable implementation and the stellarator instance. Existing fixed-capacity mode is useful evidence, not proof that every facility choice is preserved.
3. Fuel-processing capacity set to running exhaust times a margin constrained to at least one, then used for installed equipment cost. Inspect `mfe_fuel_cycle.sysml`, `mfe_plant_systems.sysml` and `fuel_processing_cost_impl.py`.
4. Primary helium and secondary salt flow/pump calculations and costs. Distinguish calculated required flow from installed pump ratings. Preserve genuine exchanger installed-area versus required-area checks.
5. Matched steam and cooling-water operating-point closures, cryogenic and turbine cost proxies, and their part bindings. Do not call derived operating flow installed capacity without a supported relationship. Do not invent missing equipment performance data merely to complete a table.
6. Fuel inventories and maintenance policy. Determine whether these are valid derived stocks/policies for a stated scenario or remove intended choices; do not classify every derived stock or calendar result as a hardware-sizing violation.

Use independently chosen installed heating compared against sustainment demand, and exchanger installed area compared against required area, as useful existing examples. They are examples, not a requirement to force every subsystem into identical interfaces.

## Architecture before implementation

Define the supported design-variable choices and evaluate them against MR-7 before editing production bindings. Separate physical/performance relationships from any study-specific sizing/search policy. A selected design must be executable and costed without rerunning an automatic selection policy. Record how calculation direction is selected and represented; do not replace one hidden fixed assignment with another. Do not infer a requirement to build a universal acausal solver. If the intended capability needs a new execution mechanism, prototype the smallest uncertain capability and obtain independent architectural review before relying on it.

The existing requirement authorizes restoring design-choice preservation. Routine implementation and verified fixes may proceed. Surface genuinely unresolved choices about the intended variable freedoms, new physical approximations or unsupported source interpretation to the owner before dependent work; do not manufacture approval gates for routine edits or silently settle those scientific choices.

Obtain a fresh non-author review of the proposed variable roles, actual binding plan and acceptance tests before dependent implementation. The brief must include MR-7 and the owner's quoted intent, not merely the author's proposed solution. Reuse that reviewer for changed lines and integrated behavior where valid; preserve review findings and dispositions. Decompose into native work items when warranted and respect the run-goal limits rather than treating this list as one unbounded round.

## Acceptance evidence

For each repaired capacity/fit path, demonstrate through the supported native route:

- A supplied insufficient design remains unchanged and produces the appropriate failed constraint within the performance model's supported domain.
- A supplied sufficient design remains unchanged and produces the expected constraint result; represented inventory and cost follow that supplied design.
- Where the agreed interface permits holding hardware fixed while varying operating demand, the change affects demand/margins without silently changing equipment quantities or prices that depend only on installed hardware.
- An unsupported empirical condition remains explicitly unsupported, distinct from physical infeasibility. The conductor field restriction belongs to conductor performance; do not remove it or widen its range to force execution. Broader source-supported performance coverage is separate work if needed.
- Optional automatic selection, if explicitly authorized for a study, produces a separately identified design that can be evaluated without that policy. The component cannot require auto-selection as its only execution path.

For geometry identities, operating policies and cost proxies where these tests do not apply, give a specific reason and check their declared meaning instead. Independently review those dispositions. Test units, actual public inputs, generated bindings, downstream propagation and relevant boundary cases; do not replace native behavioral checks with assertions that an input field exists.

Update stale consumers and tests when their old expected behavior encoded the violation. Preserve historical packages, results and replay semantics; do not rewrite old evidence to make it agree with the repaired model. Changed numerical results need a physical or policy explanation. Passing every plant constraint or reducing LCOE is not a success criterion.

The technical objective is met only when the scoped inventory is complete, every confirmed violation is repaired through the model and consumers, the applicable tests pass, and independent review supports MR-7 compliance. Unverified or deferred violations remain open with a concrete blocker; a completed audit or high depth score alone does not complete remediation. Report bounded negative results honestly if the available performance relationships cannot support the intended evaluation.

## Delivery and record

Keep the native goal/work trail current and produce an answer with the before/after design choices, affected interfaces, independently checked evidence, remaining scientific limits and exact commits. Local commits for authorized work are permitted; preserve unrelated staged files. If changing a supported interface breaks historical study use, explain the versioned migration rather than silently editing frozen packages. Keep execution scratch outside the repository using the existing cleanup conventions.

Do not rerun the reference comparison, adopt a replacement comparison freeze, or declare a restored blind test. Those are separate owner decisions. End with a concise account of what choices the repaired model now preserves, what it still cannot evaluate, and whether the technical completion criteria are actually met.
