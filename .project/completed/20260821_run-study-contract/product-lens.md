# Product-Lens — run-study-contract (RUN-STUDY Item 2)

Epic: RUN-STUDY (`.project/backlog/epic_run_study_capability.md` — epic gate CLEAR as of the 2026-08-19 corrected Stage 3 scope entry)

## spec — 2026-08-19 — rev drafted Item 2 contract (`.project/active/run-study-contract/spec.md`)

Point (re-derived): The Item 2 contract must make the next study reach the proof-of-life floor from a goal-only prompt and make its record readable cold — preflight and verification recorded, indicators non-gating with the user ruling on any axis nothing resists, that no-resistance case filed as a model-development finding, LCOE and named constraint outcomes always present, and every lesson landing in exactly one home. [source: `.project/concepts/run-study-skill.md` (Success Criteria 1–5, Owner's Words); `.project/concepts/run-study-skill-design.md` (Core Model, Required Invariants); `.project/concepts/study-driven-model-development.md` (LCOE + constraint-violation focus, discovery log); `.project/backlog/epic_run_study_capability.md` Item 2, grade: owner]

Falsifier: A record can satisfy this spec in full and still leave a fresh administrator unable to see that the study's mechanical gates ever ran or passed, and leave an axis the model does not resist recorded as a ruling with no model-development finding attached.

Findings:
- `spec-F1` [DO] Preflight results are not mandatory record content. The mandatory list omits the outcomes of the baseline gate, declared-group validation, and manifest-fingerprint match; the snapshot carries the pinned baseline *value* and the git-clean *result* but no gate outcome. The accepted design lists "preflight results" as required record content (`run-study-skill-design.md:129`), the owner's criterion is "preflight checks recorded and passing" (`run-study-skill.md:33`), and the epic's short-prompt criterion says "recorded preflight results". The runbook step exists but deposits nothing the contract requires. — `.project/concepts/run-study-skill.md` SC-1 (owner); `.project/backlog/epic_run_study_capability.md` Success Criteria (owner) — disposition: BLOCK
- `spec-F2` [DO] A `no_constraint_response` axis owes only the user's ruling, not the model finding. The spec requires the indicator, the disclosure, and the ruling before any point runs — but nothing requires the record to state what should push back and isn't modeled. The owner's criterion pairs the two: the record says so before execution, the choice returns to the user, **and** "a model-development finding (what should push back and isn't modeled) is filed in the study record" (`run-study-skill.md:35`; design Goal, `run-study-skill-design.md:34`). The generic Findings section does not make this case mandatory, and this item owns the record contract, so the obligation has no other home. — `.project/concepts/run-study-skill.md` SC-3 (owner) — disposition: BLOCK
- `spec-F3` [DO] Grade demotion on skill weight. The owner graded the skill's shape "fairly lightweight, referencing a runbook.md ... and tools; the study policy is its rulebook" (`run-study-skill.md:26`, `[OWNER]`); the spec carried it as `[INFERRED]`, which under the absorb mapping should be `[NEED]`. The same line also recast the skill as "the referent for 'lightweight'"; the concept's `[REFERENT]` is `/show-me`, and it governs output weight, not the skill file. Substance preserved elsewhere, so a provenance defect, not a lost requirement. — `.project/concepts/run-study-skill.md` Owner's Words (owner) — disposition: NOTE

Smells:
- Constraint outcomes are recorded per study, not per region. Record item 2 requires `satisfied | violated | indeterminate` per executing constraint; the owner's framing is "when it happens and what the constraint is" (`study-driven-model-development.md:31`). Under search framing the spec recovers the "where" (active constraint, boundary, constrained optimum); under sensitivity framing a violation can be recorded with no location in the swept space. Inherited from the epic's own F2-fix wording, not introduced here.
- The routing table sent "Plan/framing critique before any point runs" to a runbook step with no record deposit, while the design requires each runbook step to name what it produces in the record (`run-study-skill-design.md:110`).
- One lesson is routed to "no durable home" (LCOE masking where `net_positive` is violated). It is disclosed and argued as study-specific presentation judgment, which is honest against Principle 5, but it is the single exception to this item's own "exactly one named home" criterion.

Resolves:
- `spec-F1`: FIXED — authority: owner (`run-study-skill.md` SC-1) — basis: **Preflight results** added as mandatory record section 7, requiring a stated pass/fail per gate (declared-group validation, suffix-sibling warnings, baseline gate, fingerprint match, package cleanliness); **Execution route** added as section 8; a matching success criterion now names recorded gate outcomes.
- `spec-F2`: FIXED — authority: owner (`run-study-skill.md` SC-3) — basis: record section 5 now requires, for every `no_constraint_response` axis, a model-development finding naming what should push back and is not modeled, indexed in the discovery log as `kind: model`; the ruling alone explicitly does not discharge it. A dedicated success criterion states the pairing.
- `spec-F3`: FIXED — authority: owner — basis: the skill-weight requirement is re-graded `[NEED]` and carries the owner's words; the mis-stated referent claim is deleted (the `/show-me` `[REFERENT]` remains where it belongs, on record-section weight).
- Smell (framing critique deposits nothing): FIXED — the routing table row now names its record deposit, and record section 11 states the pre-execution framing critique is one of the named review outcomes.
- Smell (per-study vs per-region constraint outcomes): CARRIED — inherited from the epic's ratified wording; not narrowed here. Design may sharpen the sensitivity-framing section to locate violations in the swept space.
- Smell (one lesson with no durable home): ACCEPTED — recorded in the spec as an explicit exception with its reason, rather than forced into a home it does not fit.

Gate: CLEAR

## design — 2026-08-19 — rev draft design (`.project/active/run-study-contract/design.md`)

*Run inline by the design reviewer against the same SOURCES (concept, concept-design, epic, spec), not as a subagent. Point re-derived independently of the design's own framing.*

Point (re-derived): A study run from a goal-only prompt must leave one committed directory from which a second agent with no execution memory recovers the framing per axis, the LCOE result, every named constraint outcome, and every finding — each traced to a committed artifact — and every process lesson must land in exactly one home. [source: `.project/concepts/run-study-skill.md` (Owner's Words, SC-1/SC-3/SC-5); `.project/concepts/run-study-skill-design.md` (Principles 3 and 5, Core Model — record); `.project/backlog/epic_run_study_capability.md` Critical Success Factor, grade: owner]

Falsifier: A record can satisfy every rule this design states and still leave the administrator unable to tell whether it is complete — because the completeness rule is stated relative to a file the administrator is forbidden to read.

Findings:
- `design-F1` [DO] The snapshot's completeness rule ("every fingerprint the manifest declares, by the manifest's own name", `design.md:231`) is not executable from inside the record. The administrator reads nothing outside the record directory (`design.md:249`), so the set the rule quantifies over is unavailable to the only reader who audits it. — `.project/concepts/run-study-skill-design.md:129` "never cites a live file"; `:107` administrator boundary (owner-ratified) — disposition: FIX (field addition, not rework)
- `design-F2` [DO] A cross-fingerprint A/B — the epic's first consumer (Item 6) and the case D4 exists for — cannot be expressed in the snapshot shape drawn at `design.md:212-227`: study definition, strategy, window, and effective executable fingerprint are all study-scoped scalars, while the concept's store rule makes them arm-scoped whenever the tuple differs. — `.project/concepts/run-study-skill-design.md:129` A/B store rule (owner-ratified) — disposition: FIX
- `design-F3` [NOTE] The carried spec-hop smell (locate a sensitivity-framed constraint violation in the swept space) was handed to the design (`product-lens.md:26`) and is not addressed: `design.md:203` gives the sensitivity section the observed response and a no-boundary-claim statement only. — `.project/concepts/study-driven-model-development.md:31` (owner) — disposition: NOTE

Smells:
- *Consumer compensating for a producer guarantee* — examined, did not fire structurally. D2 keeps the invariant with the executor and states the rule plainly; what is missing is the reader's ability to check it. Recorded as `design-F1`, fixable by copying the declared name list into the snapshot. Not escalated to Rework.
- *Changed invariant ownership without saying so* — examined, did not fire. The values/arguments split is stated as the design's core concept and its consequences are drawn explicitly.

Gate: CLEAR-WITH-FIXES (`design-F1`, `design-F2` are must-fix in the design review; neither is a rework trigger)
