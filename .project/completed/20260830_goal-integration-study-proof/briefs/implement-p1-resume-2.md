# Resume 2 — rulings on your four questions (all execution-detail tier, orchestrator)

1. **T-002 does not return yet — it continues.** No "Done when" met, no "Stop when" fired, so
   there is no return to write at run 3. The headline re-pin is INSIDE T-002's scope as
   written: the scope authorizes "re-pin `exploration/stellarator_e2e/studies/manifest.json`";
   the three-field enumeration was the plan's 1b list, not the scope's limit. No T-003.
   T-002's eventual single return covers the whole arc: run 2 (clean gate), the 1b commit,
   run 3 (baseline_headline), the headline re-pin, run 4.
2. **Done and committed for you** at `cc249b89`: `baseline.headline.value` 275.2642200420774 →
   333.0670332813743, derived from your run-3 `baseline_result.json` (asserted present in the
   evidence before writing). The commit message records that the orchestrator performed the
   write at your recommendation.
3. **Re-pin ruled correct** — same class as the fixture re-derivation; the seam's independent
   oracle-verification and lineage gates answer the circularity concern. No separate
   derivation run needed; record the reasoning (and the alternative you offered) in the trail.
4. **Fast confirmation first, then the full battery once**: `tests/study/test_preflight_gates.py
   tests/study/test_integrate_success.py -q`, and if green run the full `tests/study -q`
   (both with the two --env-file flags, unpiped so you see the exit code).
5. **Evidence trimming accepted** — do not restore `_backup/`, `recaptured.snapshot.json`,
   `_work/`; record the trim as a deviation in the Phase 1 completion notes.

## Continue — finish Phase 1

- Run 4: fresh `--out-dir /tmp/integration-run-4`, same invocation, expect exit 0
  `class: "CANDIDATE"`. Copy (trimmed, same rule) to
  `work/orchestration/goals/p-pump-fence/evidence/integration-run-4/`.
- Batteries per ruling 4. Then the remaining plan Phase-1 validation items.
- Append `### T-002 return` — one return, whole arc, five decision fields, interruption note
  (cite briefs implement-p1-resume.md / -2.md and commits `8099217b`, `cc249b89`), and the
  goal-relevant fact worth the trail: all six baseline verdicts held `satisfied` at 195 MW at
  the manifest baseline point, recirc_ok included, while LCOE moved +21.0 % — cite run-3/run-4
  evidence paths.
- Tick the now-true plan Phase-1 checkboxes; fill Phase 0 and Phase 1 completion notes
  (deviations: the 600s timeout interruption; run-2 clean-gate refusal; orchestrator-performed
  1b and headline commits; the unenumerated fourth pin; the evidence trim;
  `.integration_workspace` cleanup).
- Hard rules unchanged: no commits; list touched files grouped by the plan's commit points;
  do not start Phase 2.

End with: run-4 class + pin + both fingerprints, battery tail lines, validation results, file list.
