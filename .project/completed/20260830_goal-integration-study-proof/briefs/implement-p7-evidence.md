# Resume 11 — Phase 7: epic evidence and full regressions

State since your last leg, all committed: round 1 closed (`### Round 1 result`), fresh review
FINDINGS with answer upheld + learnings appended (4bf5d709), goal CLOSED by owner ruling
[OWNER 2026-08-29] with the annex edit ratified and the CAS10 guard minted as WI-034
(5d740688), runbook integrate row flipped native (c4c7d723), route equivalence complete —
same contract on all five dimensions, identical native identity, findings F-1..F-4
(.project/active/goal-integration-study-proof/route_equivalence.md, cb417e5e). Read the
route_equivalence.md and the trail's close section before writing.

## This leg — plan § Phase 7, every checkbox

1. Run the full Regression Stencil (plan § Phase 7) exactly — canonical battery with both
   env files, tests/models with the set -a sourcing, tests/research, validate models/,
   source_registry verify. Quote outputs verbatim in epic_evidence.md. Any unexplained red
   is a stop.
2. Author `.project/active/goal-integration-study-proof/epic_evidence.md`:
   - Map each of the seven epic § Item 6 success criteria to its evidence (paths + commits
     that resolve). Add spec criterion 8.
   - Honest-limits section, each its own line: the research seam's request/return bookkeeper
     (`scripts/research_seam.py`) has never run end-to-end (write-door evidence only);
     `assert_read_set_covered` has never run at gate 6 (reported not-run by the 3 of 5 seam
     invocations that reached gate 6's reporting — per the round review's correction — and
     exercised by nothing else); the route-equivalence declared limit (study.execute
     fixture-substituted).
   - Observed failures / carve-outs for the hardening rule (epic SC 7): F-1..F-4 from
     route_equivalence.md with their fix homes; the 600s-timeout interruption arc (resumed
     cleanly from native facts — evidence the prose route held); the harness kill of the
     first hand-route launch (environment incident); the stale-expectation class (five
     artifacts, four mechanisms — cite the trail Amendment and learnings L-001).
   - SC 7 walk: enumerate what this item added and confirm none of it is control-plane
     machinery (ADR-003); no promotion requested.
3. Tick plan Phase 7 checkboxes; fill `### Phase 7 Completion` (and Phase 2-6 completion
   note stubs if any are still empty — from the committed record, briefly).

Hard rules unchanged: no commits; end with the battery tail lines verbatim, the criterion→
evidence map summary (one line each), and the file list.
