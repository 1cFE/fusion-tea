# Brief: spec for "Skill, Runbook, and Record Contract" (RUN-STUDY Item 2)

Work item home: `.project/active/run-study-contract/` — write `spec.md` there.

## Objective

Create the tracked `run-study` entry point and the exact executor-to-administrator artifact
contract, without duplicating rules (policy's job) or mechanical logic (tools' job).

## Governing sources (read in this order)

1. `.project/backlog/epic_run_study_capability.md` — Item 2 section is your scope contract.
2. `.project/concepts/run-study-skill-design.md` — ACCEPTED design ([OWNER] 2026-08-19). Its
   Core Model (skill/runbook/policy/tools/record sections), Design Principles, Required
   Invariants, and "How It Works" flows are settled; do not relitigate. Spec-detail still open
   (your job to pin): the record template's exact sections and which are mandatory per framing;
   which proof-of-life steps are universal vs stellarator-annex; the record snapshot's exact
   field list.
3. `.project/concepts/run-study-skill.md` — owner-verbatim intent (grades marked in-file).
4. `.project/active/demo-proof-of-life/plan.md` — validated procedural source for the runbook.
5. `.project/active/demo-study-parameterization-policy/policy.md` — the rulebook (Draft).

## Scope (from the epic — the deliverable set is fixed)

1. `.claude/skills/run-study/SKILL.md` — collaborative intake, explicit execute/administer mode
   selection; plus the narrow `.gitignore` negation (`!.claude/skills/run-study/` style — only
   this skill is newly admitted).
2. `.claude/skills/run-study/runbook.md` — universal ordered obligations: intake, declared
   groups, indicators and user rulings, mechanical gates, teax route choice, verification,
   named review outcomes, record commit, administration. Package annex is linked, never inlined.
3. `.claude/skills/run-study/record-template.md` — immutable record contract. MANDATORY in every
   capability-compliant record: LCOE objective and result; every executing constraint's qualified
   identity and `satisfied | violated | indeterminate` status; framing; axis groups with per-key
   provenance; indicators; compatibility tuples; verification; findings; resolved package facts
   snapshotted (never cited from mutable files). Synthesis is a SEPARATE file; executed evidence
   immutable; missing evidence reported, never inferred.
4. Package-annex link, discovery-log row format, `synthesis.md` convention, and the
   fresh-administrator acceptance check.
5. Route each proof-of-life lesson to exactly ONE home (skill | runbook | policy | tool) — e.g.
   stratified verification sampling → verify.py (tool, Item 4); window-scan-by-oracle → runbook
   step; H1 search-framing rescope → policy rule (Item 6 owns the policy edit — your spec only
   RECORDS the routing destination for policy-bound lessons, it does not edit the policy).

## Constraints (settled; provenance as marked)

- [OWNER] Indicators inform, never gate. No fixed per-study-type output contracts; `/show-me`
  is the weight referent (sections short, adaptive; only presence mandatory per framing).
- [OWNER] Policy stays Draft at its current path — Item 6 owns ratification and the move to
  `modeling_project/STUDY_POLICY.md`. The runbook cites the CURRENT path for now.
- [AGENT, ratified 2026-08-19] Records live at `exploration/<pkg>/studies/<study-id>/` beside
  the package, with per-package `DISCOVERY_LOG.md` as index (one line per finding: kind,
  record, disposition, home). One store per complete teax compatibility tuple; cross-fingerprint
  correlation stated in the record.
- Item 1 spike CONFIRMED the indicator vocabulary (`.project/active/run-study-reachability-spike/findings.md`):
  `no_constraint_response` is a sound negative; `constraints_reachable` positives are
  possible-path only; monotonicity/same-quantity identity/intra-module dependency are NOT
  derivable and every report says so. Use that vocabulary exactly.
- Two execution routes, runbook-selected: `teax-study` CLI (plain Cartesian grids, stock loader)
  or study-local direct-API (`StudyRunner` + `PreparedListStrategy`) for coordinated blocks and
  the adapter route. No generic runner. Tools never own execution.

## Out of scope (epic-fixed)

- Implementing indicators, preflight, verification, adapter, or a generic runner (Items 3–4).
- Ratifying or moving the policy (Item 6).
- Choosing the first A/B block or interpreting study results.
- NOTE (orchestrator): epic Item 5 (legacy cold-pickup exercise) is NOT in this run; its gap
  feedback lands later. Your record template must stand on the design's requirements alone.

## Success criteria (from the epic — your spec's acceptance section must cover these)

- Tracked skill supports goal-only execute intake and record-only administration.
- Runbook names obligations and outputs without encoding axis choice, framing verdicts, or
  result interpretation.
- Record contract makes LCOE and all named constraint outcomes mandatory; snapshots facts.
- Executed evidence immutable; synthesis separate; missing evidence reported, not inferred.
- `.gitignore` admits only `.claude/skills/run-study/` beyond existing tracked skills.

## Working voice

Follow `~/agentic-project-init/claude-pack/rules/working-voice.md` and capture-fidelity
provenance grades ([OWNER]/[AGENT]/[INFERRED]) in the spec.
