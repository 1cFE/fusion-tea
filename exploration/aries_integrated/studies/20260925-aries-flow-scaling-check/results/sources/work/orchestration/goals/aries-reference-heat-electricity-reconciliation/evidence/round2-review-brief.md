# Round 2 review brief — fresh reviewer

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 18 tool calls and a 650-word return, written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/round2-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks or other goal directories. Do not run the model, the build, the seam or the study. Sign as "fresh round-2 reviewer, 2026-09-25".

## What you are reviewing

Round 2 of the goal in `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/`: `goal.md` (question, answered-when, invariants, limits, close rule), `trail.md` from the heading `## Round 2 — topology-increment` to the end (strategy, T-001–T-005 scopes/starts/returns, T-004 attempt 1, Round 2 result), `answer.md`, `evidence/discrepancy-ledger.md` (v2), and the study it committed: `exploration/aries_integrated/studies/20260925-aries-revised-reference-network/` (`record.md`, `synthesis.md`, `results/cases.json`, `results/attribution.md`, `results/attempt-comparison.json`, `results/verification_summary.json`, `snapshot.json`). Prior reviews you may cite but need not reread: `evidence/design-review.md`, `evidence/implementation-review.md`, `evidence/unmet-tolerance-review.md`.

## Checks (return one line per check with PASS / FINDING and the evidence you used)

1. **Native evidence by citation.** Pick at least four numbers the Round 2 result, the ledger or the answer cites (for example `network-c3-0.85` unmet 109.876 with helium 53.514 and PbLi 56.362 and net 879.693; `resized-compressor-1700-network-0.85` net 891.003 with every verdict satisfied; `combined-c3-partition` net 842.732 and unmet 151.002; interaction +7.552) and confirm them in `results/cases.json` (use short Python one-liners; do not print whole files). Confirm `results/attempt-comparison.json` reports zero differences and `verification_summary.json` outcome `pass` with 27 sampled rows.
2. **The helium-stage claim.** In `network-c3-0.85` check `aries_integrated_plant__heat_exchangers__evaluate__he_secondary_out` against `…__he_hot` and `…__he_transferred` against `aries_integrated_plant__he_coolant__evaluate__delivered_heat`; does the record's statement that the blanket-helium stage binds (cycle helium leaving within a few kelvin of the helium hot inlet, carrying less than its duty) hold?
3. **Goal and strategy fidelity.** Did the round do what the strategy revision declared and nothing the goal forbids: one package promoted and one study committed; the original failing case retained verbatim (bit-exact replay claimed in `record.md` § 10 and the WI-092 migration report); nothing tuned to 1000 MW; MR-7 design review before implementation; the resized-compressor cases labelled as a declared alternative and never as a reproduction; the inherited-rating adverse cases retained.
4. **Task scopes.** Did T-001–T-005 stay inside their written scopes? Note any drift (for example the manifest tolerance amendment: was it inside T-004's scope or honestly recorded as a deviation?).
5. **Retry classification.** The trail claims one retry in T-003 and one in T-004, each honestly classified; check the attempt narratives against the retained logs named in the trail.
6. **Tolerance discipline.** Was the 1e-7 MW absolute tolerance declared and independently reviewed before use, limited to the four unmet-heat channels, and was the materiality budget in `evidence/materiality-budget.md` left unchanged?
7. **Discovery rows.** Confirm the nine rows `20260925-aries-revised-reference-network#1`–`#9` exist in `exploration/aries_integrated/studies/DISCOVERY_LOG.md` with the dispositions `record.md` § 15 states, and that none is `unrouted`.
8. **Reading and dispositions.** Does `synthesis.md` follow from the record? Is the statement "once all heat is removed the arrangement has no effect" supported (compare `c3-minus-recuperator` with `network-c3-eps0.8-0.85`, and `resized-compressor-1800-series` with `-network-0.85`)?
9. **Learning delta.** For L-005–L-009 in the Round 2 result: accept, correct or reject each, with reason.
10. **Answer completeness and honesty.** Does `answer.md` contain every section the owner brief requires (source case definition, baseline and revised heat/electricity tables, quantitative attribution, remaining uncertainty, engineering statuses, reuse and model changes, independent reviews, Stellaris preservation, exact replay instructions, plain-language explanation), and does it assess the completion condition honestly (met / partially answered / unmet) without presenting a non-steady case or the resized alternative as a reproduction of the ARIES operating point?
11. **Claims not supported.** Name any statement in the Round 2 result, the synthesis, the ledger or the answer that the cited evidence does not carry.

## Exclusions

Do not re-run anything. Do not assess the scientific truth of the sources beyond what the record and the reference-case contract state. Do not open any other goal directory.

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; one line per check; numbered findings with severities (blocking / correct-before-use / note); the learning-delta rulings; what the review did not cover.
