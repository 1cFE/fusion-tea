# Brief — Phase 3 administrator — study 20260829-p-pump-fence

You are a FRESH administrator session. You did not execute this study and have no memory of
its run. Your entire input is ONE committed record directory:

    exploration/stellarator_e2e/studies/20260829-p-pump-fence/

Invoke the `run-study` skill in **administer** mode against that path.

## The contract (run-study SKILL/runbook + plan Phase 3)

- Confirm the path is a record directory before reading it as one.
- Read ONLY that directory. Do not read the goal directory, any trail, any brief, any other
  study's record (following the record's own citations to other records IS permitted where
  the record cites them), or any seam evidence. A fact not in the record is reported as
  **MISSING**, never recovered from elsewhere.
- Write `synthesis.md` into the record directory. Append NOTHING to DISCOVERY_LOG.md — the
  administrator never writes the log.
- No git commits.

## Deliverable

`synthesis.md` per the runbook's administer contract: what was asked, what was assumed/held,
what came out, what the evidence establishes, what none of it supports, and your assessment
of each § 15 finding (sound / overstated / understated, with the record's own numbers).
End your final message with the synthesis's headline reading (answered / adverse /
inconclusive and why) and the list of MISSING facts, if any.
ARTIFACT: exploration/stellarator_e2e/studies/20260829-p-pump-fence/synthesis.md
