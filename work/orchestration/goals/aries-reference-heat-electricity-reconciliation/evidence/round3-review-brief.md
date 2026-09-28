# Round 3 review brief — fresh reviewer

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 16 tool calls and a 550-word return, written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/round3-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks or other goal directories. Do not run anything. Sign as "fresh round-3 reviewer, 2026-09-25".

## What you are reviewing

Round 3 of the goal in `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/`: `evidence/owner-supplement-r3.md` (the owner's direction, verbatim), `trail.md` from the heading `## Round 3 — q1-thermal-cycle-check` to the end, `evidence/q1-thermal-cycle-review.md` (the fresh thermal-cycle review; do not redo it, judge how it was used), `answer.md` § 1, § 3 (the round-3 table), § 5, § 6, § 12, § 13, `evidence/discrepancy-ledger.md` (v2.3), `evidence/reference-case-contract.md` § 6a, and the study committed: `exploration/aries_integrated/studies/20260925-aries-flow-scaling-check/` (`record.md`, `synthesis.md`, `results/cases.json`, `results/attribution.md`, `results/verification_summary.json`).

## Checks (one line each, PASS / FINDING, with the evidence used)

1. **Owner framing.** The owner wrote that the evidence supports "we cannot reconcile the published thermal description with our interpretation and implementation" and does not establish "the actual published design could not achieve its stated efficiency". After the thermal-cycle review returned SURVIVES, does every restatement in `answer.md`, the ledger and the contract § 6a stay within what that review establishes (no exchanger arrangement of the printed per-branch sources delivers 707 °C; our representation is not the cause; the source's own cycle treatment is undetermined) and stop short of the claim the owner rejected? Quote any sentence that crosses the line.
2. **The two reporting details.** Is the 110 MW residual stated as split between the helium stage and the PbLi stream wherever it is characterised, and is 891 MW stated as the best tested steady case rather than an upper bound?
3. **Native evidence by citation.** In `results/cases.json` confirm: `network-c3-scaledflows-0.85` unmet 95.681 (helium 73.604, PbLi 22.077) and net 892.449; `network-c3-scaledflows-pbli-only-0.85` unmet 95.940; `resized-compressor-1650-network-0.85` unmet 42.715 with `heat_removal_ok` violated; both 1700 kg/s cases with every verdict satisfied and net 891.003 / 891.002. Confirm `verification_summary.json` outcome `pass` with 12 sampled rows.
4. **Study fidelity and MR-7.** Were the scaled flows and pump capacities declared values of the mapping (stated in `config.json` bases and the record) rather than sized from demand? Was anything tuned to 1000 MW? One study, no package or manifest change?
5. **Scope and count.** Did T-001 and T-002 stay inside their written scopes (note the point-count amendment)?
6. **Migration claim.** Does the record's reading that ≈ 20 MW of the PbLi artefact migrates to the helium stage follow from the stored channels (compare `he_unmet` and `pbli_unmet` between `network-c3-0.85` and the scaled cases)?
7. **Learning delta.** For L-010, L-011, L-012 in the Round 3 result: accept, correct or reject each, with reason.
8. **Discovery rows.** Confirm `20260925-aries-flow-scaling-check#1`–`#4` exist in `exploration/aries_integrated/studies/DISCOVERY_LOG.md` with the record § 15 dispositions; none `unrouted`.
9. **Claims not supported.** Name any statement in the Round 3 result, the record, the ledger or the answer that the cited evidence does not carry.

## Exclusions

Do not re-run anything. Do not re-derive the thermal-cycle review's physics beyond checking that its verdict and limits are quoted faithfully. Do not open any other goal directory.

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; one line per check; numbered findings with severities (blocking / correct-before-use / note); the learning-delta rulings; what the review did not cover.
