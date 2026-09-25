# Round 4 review brief — fresh reviewer

You are a fresh, independent reviewer with no prior context. Read only the files named here (paths relative to `/home/reid/1cfe/fusion-tea`). Budget: at most 16 tool calls and a 550-word return, written to `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/evidence/round4-review.md`. Do not load CLAUDE.md, AGENTS.md, runbooks or other goal directories. Do not run anything. Sign as "fresh round-4 reviewer, 2026-09-25".

## What you are reviewing

Round 4 of the goal in `work/orchestration/goals/aries-reference-heat-electricity-reconciliation/`: `evidence/owner-supplement-r4.md` (the owner's direction and two qualifications, verbatim), `trail.md` from the heading `## Round 4 — cited-cycle-reference` to the end, `answer.md` § 1, § 5, § 6, § 9, § 12, § 13, `evidence/discrepancy-ledger.md` (v2.3) and `evidence/reference-case-contract.md` § 6a (the `[r4]` paragraphs), the two readings `evidence/ref15-reading.md` and `evidence/malang98-reading.md` with their reviews `evidence/ref15-reading-review.md` and `evidence/malang98-reading-review.md` (judge how the reviews were applied; do not redo them), the two research returns `evidence/research-acquire-r4-return.md` and `evidence/research-acquire-r4b-return.md`, and the two request files under `knowledge/research/requests/REQ-ARIES-CYCLE-HX-01.json` and `-02.json` with their `return.json` under `knowledge/research/requests/runs/`.

## Checks (one line each, PASS / FINDING, with the evidence used)

1. **Owner direction.** Was the cited reference pursued through the prescribed research route (request files, run records, registry) rather than by ad-hoc fetching; were the current calculations preserved (no model, package, manifest or study change in round 4); was the missing reference not assumed to resolve the issue; is the lumped-heater explanation still stated as not established (an inference consistent with the sources) everywhere it appears in `answer.md`, the ledger and the contract? Quote any sentence that treats it as established.
2. **The two qualifications.** Does every restatement say the published quantities cannot all hold under the stated heat-exchanger assumptions rather than that no arrangement can work, and is 891 MW kept as a modeled alternative whose flow and rating need cost evaluation before economic comparison? Search `answer.md`, the ledger, the contract § 6a and `learnings.md` L-010 for "no arrangement", "no counterflow arrangement", "upper bound", "reconstructed".
3. **Citation correction.** Is the round-3 "p737 Ref. 7" correction supported by `evidence/raffray-p745.png` (view it: Ref. 7 is Lyon et al., Ref. 15 Schleicher et al., Ref. 13 Wang et al.) and consistently applied (answer, contract, ledger, the appended note on `evidence/q1-thermal-cycle-review.md`)?
4. **Source-check application.** Were the correct-before-use findings of both source checks applied in the readings (Ref. 15: equation citation to Malang, Table III mapping, 737 − 30, Tout materials caveat, inference split; Malang: "natural inheritance" reworded)?
5. **Bounded result.** Is the round's bounded result (the cited method takes the turbine inlet as an input from a single heat source or IHX; never extended to several loops in the obtained sources; does not resolve the branch inconsistency; does not state how ARIES-CS handled it) stated the same way in the trail, the answer, the ledger and the contract, and does the answer still assess the completion condition as partially answered?
6. **Scopes and limits.** Did T-001 to T-005 stay inside their written scopes; were the request limits respected per the returns; any retries?
7. **Learning delta.** For L-013, L-014, L-015 in the Round 4 result: accept, correct or reject each, with reason.
8. **Claims not supported.** Name any statement in the Round 4 result, the answer, the ledger or the contract that the cited evidence does not carry.

## Exclusions

Do not re-run anything. Do not re-derive the source readings' physics or re-read the registered sources beyond checking that the reviews were applied. Do not open any other goal directory or anything under `knowledge/holdout/`.

## Return format

Verdict `PASS`, `FINDINGS` or `OWNER_GATE`; one line per check; numbered findings with severities (blocking / correct-before-use / note); the learning-delta rulings; what the review did not cover.
