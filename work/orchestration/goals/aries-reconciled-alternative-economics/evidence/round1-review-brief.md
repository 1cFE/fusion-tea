# Brief — fresh review of round 1 of `aries-reconciled-alternative-economics`

You are a fresh non-author reviewer with no inherited conversation. Read the goal's `goal.md`, `trail.md` (round 1 in full) and `answer.md`, and the evidence they cite, under `work/orchestration/goals/aries-reconciled-alternative-economics/`. Do not read other goals except the cited paths. Do not execute the model package; you may run `uv run python` to read JSON and check arithmetic. Write exactly one file: `work/orchestration/goals/aries-reconciled-alternative-economics/evidence/round1-review.md`. Budget: about 25 tool calls; a reply of at most 700 words. Verdict: `PASS`, `FINDINGS` (each marked correct-before-use or note) or `OWNER_GATE`.

## What to check (the runbook's closure list)

1. **Native evidence by citation.** Pick at least eight figures from `answer.md` § 1, § 3, § 5 and § 6 (the two headline LCOEs, overnight and financed capital, the tritium contribution, the baseline deltas, the ladder's combined value and one discount rung, the capital-scope and denominator effects, two sensitivity deltas) and confirm each against the sealed study's `exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/attribution.json` or `results/cases.json` (case names are the keys; channels carry the prefix `aries_integrated_plant__`). Confirm `results/verification_summary.json` outcome `pass` with 64 sampled rows, `results/attempt-comparison.json` `identical: true`, and `evidence/replay-alternative.json` `passed: true`.
2. **Goal and strategy fidelity.** Did the round pursue the strategy revision it declared? Did any case tune toward 77.6? Is every substitution of a published quantity labelled a diagnostic and kept out of the independent assessment?
3. **Task scopes.** Read each `T-00N scope` and the corresponding return; name any work outside scope. The T-004 return records a deliberate deviation (the live manifest's tolerance list amended); judge whether it is recorded honestly.
4. **Retry classification.** T-004's retry: were task, inputs, scope and meaning identical, and was the machinery fix (a declared, reviewed tolerance) genuinely mechanical?
5. **Discovery rows.** Every id `20260925-aries-reconciled-alternative-economics#1`–`#11` must appear in `exploration/aries_integrated/studies/DISCOVERY_LOG.md` and in the record's § 15 with a disposition and a home; none `unrouted`.
6. **Cited-ref liveness.** `git log --oneline -3 -- exploration/aries_integrated/aries_integrated models` must show no commit after `352ecee4` (package identity unchanged); the manifest's recorded fingerprints must equal the study snapshot's.
7. **MR-7.** From `evidence/configuration-record.md`, `equipment-cost-audit.md` and the record § 4: no quantity became an installed capacity or was derived from demand; the adverse controls remain failures; the demand-matched pump capacities are disclosed as supplied choices. Record MR-7 as compliant, violated or unverified for this round's scope.
8. **The learning delta.** Accept, correct or reject each of L-001–L-006 proposed in the round result, against the evidence.
9. **Completion honesty.** `answer.md` § 13 assesses the completion condition as "met as a conditional assessment". Judge whether that is honest against the owner brief's completion condition (`evidence/owner-brief.md` § Completion condition), in particular its sentence "An unsupported material cost that prevents a useful comparison is grounds for a partially answered result": do the three bounded costs prevent a useful comparison? State your view as a finding if you disagree.
10. **Constraints carried forward** and whether a round 2 is needed.

## Exclusions

Do not re-derive the physics (net 891 MW is fixed by the prior goal). Do not assess whether the published ARIES economics are right. Do not propose price data.
