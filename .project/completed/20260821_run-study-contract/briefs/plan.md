# Brief: plan for "Skill, Runbook, and Record Contract" (RUN-STUDY Item 2)

Work item home: `.project/active/run-study-contract/` — spec.md and design.md are ACCEPTED
(design carries all review fixes MF1-7 + SF; read its Next-Stage Handoff for what is fixed
vs open). Write plan.md: phased execution with checkboxes.

The implement stage that follows writes the actual documents:
`.claude/skills/run-study/SKILL.md`, `runbook.md`, `record-template.md`, and the one-line
`.gitignore` negation. Plan the phases so each is verifiable:

- Honor the design's "De-risk first": the skeleton dry run against the proof-of-life facts
  (fill the template from `exploration/stellarator_e2e/study/` + demo-proof-of-life plan.md;
  list sections with no source) comes BEFORE finalizing the template.
- Include the design's Validation Approach as explicit plan checks: grep gates (zero package
  names, zero STUDY_POLICY.md refs), `git check-ignore` behavior, deposit completeness
  (two-way runbook<->template check), spec-coverage remap after writing.
- The snapshot.json full field list must be written against Item 3's design
  (`.project/active/run-study-indicators/design.md` — schema versions, manifest fields,
  axis_declaration block) — cite exact field names from there, do not invent.
- Keep phases small with acceptance per phase; note what each phase commits.
