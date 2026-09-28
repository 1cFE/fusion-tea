# Round 1 review brief — fresh reviewer

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 16 tool calls and a 500-word return, written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/round1-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks, model code or any other goal.

## What you are reviewing

Round 1 of the goal in `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/`: `goal.md` (question, answered-when, invariants, limits), `trail.md` (strategy, T-001–T-004 scopes/starts/returns, Round 1 result), and the study it committed: `exploration/aries_integrated/studies/20260925-aries-reference-heat-electricity-reconciliation/` (`record.md`, `synthesis.md`, `results/cases.json`, `results/attribution.md`, `results/verification_summary.json`, `snapshot.json`). The evolving ledger is `evidence/discrepancy-ledger.md`.

## Checks (return one line per check with PASS / FINDING and the evidence you used)

1. **Native evidence by citation.** Pick at least three numbers the Round 1 result or the ledger cites (e.g. C3 net 842.727 MW and 151.002 MW unremoved; `oat-cycle-flow-1600` unremoved 0 and net 773.518; forward one-at-a-time sum −45.065 versus combined +46.727) and confirm them in `results/cases.json` or `results/attribution.json`. Confirm the snapshot sha256 in `record.md` § 16 matches `snapshot.json`'s digest (compute it).
2. **Goal and strategy fidelity.** Did the round do what the strategy revision declared, and nothing the goal's invariants forbid (no model change, no tuning to 1000 MW, original failing case retained verbatim, one study, no package promotion)?
3. **Task scopes.** Did each of T-001–T-004 stay inside its written scope? Note any drift.
4. **Retry classification.** Were there any retries, and were they honestly classified? (The trail claims none.)
5. **Discovery rows.** Confirm the ten rows `20260925-aries-reference-heat-electricity-reconciliation#1`–`#10` exist in `exploration/aries_integrated/studies/DISCOVERY_LOG.md` with the dispositions the record § 15 states, and that none is `unrouted`.
6. **Study reading and dispositions.** Does `synthesis.md`'s reading follow from the record? In particular: is "all unremoved heat is in the PbLi stage" true in `nominal-source-assumed` and `combined-c3-partition` (check `he_unmet`, `pbli_unmet`, `divertor_unmet` channels)? Is routing finding #7 to a topology model increment justified by the evidence, or could an input-level change on this package have removed it?
7. **Learning delta.** For L-001–L-004 in the Round 1 result: accept, correct or reject each, with reason.
8. **Materiality budget discipline.** Was any residual accepted by relaxing the budget in `evidence/materiality-budget.md`?
9. **Claims not supported.** Name any statement in the Round 1 result, synthesis or ledger that the cited evidence does not carry.

## Exclusions

Do not re-run the model or the study. Do not assess the scientific truth of the sources beyond what the record and contract state. Do not open any other goal directory.

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; the nine check lines; the accepted/corrected learning delta; remaining uncertainty; a one-sentence recommendation (close the goal, or the next strategy). Sign as "fresh round-1 reviewer, 2026-09-25".
