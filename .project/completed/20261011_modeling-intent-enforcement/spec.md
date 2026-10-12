# Enforce design-choice preservation

[OWNER] Implement the recommendations for making the modeling pattern binding on goal and modeling agents, then provide a goal-agent prompt to fix existing violations. Source: September 20, 2026 conversation on branch `fix/modeling-intent-after-reveal`.

[OWNER-VERBATIM] “As soon as you start introducing ‘sizing’, then you are basically pre-defining which design parameters are ‘free’ and which are ‘derived’. this is explicitly what we wanted to avoid.”

[AGENT, ratified by the owner's implementation request] Put one authoritative requirement in `modeling_project/REQUIREMENTS.md`; connect agent entry instructions, goal grounding/strategy review and model design/acceptance to it. Require source-level binding review and meaningful behavior tests. Clarify prospective depth-rubric interpretation without rewriting the frozen rubric or historical results. Preserve provenance and distinguish the physical/performance model from analysis-specific design-selection policy.

Acceptance: an agent following either run-goal or the modeling process encounters the requirement before changing variable roles; design reviews must inspect actual bindings; completion requires evidence that selected design quantities are not silently overwritten; supported-domain refusals remain distinct from engineering failures. The repair prompt must name the affected subsystems, require an exhaustive inventory within the stellarator model, preserve the original experiment and prevent reference-agreement tuning. This task changes instructions, not physics models or empirical validity ranges.
