# Brief: audit "Skill, Runbook, and Record Contract" (RUN-STUDY Item 2)

Audit the completed implementation in `.project/active/run-study-contract/` (spec.md,
design.md, plan.md with phase notes) against the delivered files:
`.claude/skills/run-study/SKILL.md`, `runbook.md`, `record-template.md`, the `.gitignore`
negation, and the committed evidence (`dry-run.md`, `coverage.md`).

Standard audit: find gaps between plan claims and reality — unticked-but-claimed work,
placeholder/TODO text, unreplaced `<...>` tokens presented as content (the template's typed
placeholder tokens are BY DESIGN — flag only tokens outside the template or malformed ones),
spec requirements with no implementation, invariant violations.

Check specifically (from the design's Required Invariants):
1. All 17 template sections present, in order, headings verbatim per the design's table.
2. Every runbook step's Deposits line names a real template section; every template section
   has a producing step or is header/nil material (two-way).
3. No judgment sentences in obligations (read for it); no package names (grep for it).
4. Explicit-nil rule: conditional sections carry the Applies/nil convention; the design's
   list (framing-conditional, glue "none", no-adapter, correlation) all covered.
5. The five recorded deviations in the plan's phase notes: each genuinely within design scope
   (esp. glue_ledger moved arm-scope — check it against design MF2's one-line rule) and none
   silently weakened a spec [HARD]/[NEED].
6. The snapshot appendix field list in record-template.md against Item 3's accepted design
   field names (`.project/active/run-study-indicators/design.md`) — every copied name real.
7. The spec's three declared splits/deviations are stated, not silent.

Write findings to `.project/active/run-study-contract/audit.md` with verdict PASS,
PASS-WITH-FIXES (list, smallest fix each), or FAIL. Do not edit the deliverables yourself.
