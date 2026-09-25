# Learnings: ARIES reference heat-to-electricity reconciliation

Append-only, newest last. An entry is appended only after a round review accepts or corrects the delta the round result proposed.

## L-001 — The source-conditioned unremoved heat is a PbLi-stage limit set by the series exchanger order and the PbLi capacity rate, not by conductance

- **Evidence:** `exploration/aries_integrated/studies/20260925-aries-reference-heat-electricity-reconciliation/record.md@581e3c1a` § 3, § 6 and `results/cases.json` (original: helium and divertor unmet 0, PbLi unmet 158.726 MW; tenfold UA changes unmet heat by 6–12 MW); `evidence/parallel-network-scratch.txt` (first-principles check).
- **Scope:** the entry package `d13f4153…` with the published 2436 MW supplied; holds for every source-supported input combination tested at 1600 kg/s.
- **Implication:** a later strategy addresses the exchanger network (Fig. 12 parallel PbLi/divertor stages) rather than conductance, and treats cycle flow and recuperation jointly.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25.

## L-002 — Recuperation and cycle flow interact strongly; the source's 0.95 recuperation needs 1700–1800 kg/s on this package, while 0.8 at 1600 kg/s removes all heat at ≈ 0.345 efficiency

- **Evidence:** same record, `results/attribution.md` (forward one-at-a-time net deltas sum to −45.065 MW against combined +46.727 MW; `c2-cycle-flow-1700` 16.283 MW unremoved, `c2/c3-cycle-flow-1800` 0 with the assumed 1600 MW compressor rating exceeded; `oat-cycle-flow-1600`, `c2-minus-recuperator`, `c3-minus-recuperator` satisfy every evaluated check).
- **Scope:** the entry package and the series closure; the compressor rating is assumption A6, not a source value.
- **Implication:** attribution must be reported by stated change order with the combined case, never as a sum of one-at-a-time effects; a revised reference case must declare its cycle flow and any resized rating explicitly.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25.

## L-003 — The Lyon reference is a systems-constant chain (2916 MW → 43% → 1253 → −253 → 1000); the independently checked Q1 records an apparent inconsistency between the published duties, temperature spans and our interpretation of the exchanger arrangement, so part of the disagreement lies in what we cannot yet reconcile between the published description and our interpretation and implementation (amended 2026-09-25 at the owner's direction, `evidence/owner-supplement-r3.md`)

- **Evidence:** `evidence/reference-case-contract.md` § 3 and § 6 with `evidence/source-check-review.md` r1–r3 (page images `lyon-p703/p704/p708.png`, `raffray-p734/p736/p737.png`); accepted by the round-1 review as a source-reading claim, conditioned on the owner's reserved gate on Q1's scientific meaning.
- **Scope:** the Lyon systems paper and Raffray engineering paper as printed; not a statement about any other ARIES-CS document.
- **Implication:** agreement with 1253 MW gross is not a valid target for this model; the answer states the disagreement with its cause and asks the owner to rule on Q1's meaning.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25.

## L-004 — Source-supported replacements for inherited inputs are 0.95 recuperation, 283 kg/s divertor flow, partition 0.657/0.0469 and the 252 MW Lyon auxiliary itemisation; the inherited partition sends ≈ 218 MW too much to the divertor circuit and ≈ 198 MW too little to the blanket circuits; cycle flow 1595 kg/s is a derived cross-source convention

- **Evidence:** `evidence/reference-case-contract.md` § 5 and § 8 (source-check r2/r3); the study confirms the partition's effect only (`oat-source-partition`: Δnet −13.650 MW, PbLi unmet 177.693 MW).
- **Scope:** inputs of the entry package's assembly at 2436 MW; the deposition figures trace to the contract's reading, not to the study.
- **Implication:** the revised reference case carries these inputs; the divertor's ≈ 67 MW unlabelled share stays a bounded item until a divertor nuclear-heating term exists.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25.

## L-005 — The published series-then-parallel exchanger network removes the series-order PbLi limit (41 MW of the 151 MW C3 shortfall at unchanged hardware), but at 1600 kg/s with 0.95 recuperation the blanket-helium stage binds: the cycle helium enters it at 309 °C and reaches only 452 °C against the 456 °C helium hot inlet, leaving 107–114 MW unremoved at every split from 0.80 to 0.90; with the network 1700 kg/s suffices for complete removal at 0.95 recuperation and 1600 does not (threshold unbracketed); in series 1800 suffices and 1700 does not

- **Evidence:** `20260925-aries-revised-reference-network` `results/cases.json` (`network-c3-0.50…0.98`, `network-c3-1700-0.85`, `resized-compressor-1700-series`); record § 3 and § 6; round-2 review check 2.
- **Scope:** the WI-092 package at the C3 inputs; the split window 0.50–0.98; cycle flows 1600, 1700, 1800 kg/s only.
- **Implication:** a steady source-conditioned case at 0.95 recuperation needs more cycle flow than the inherited compressor rating admits; the choice between more flow (resized compressor) and lower recuperation is the owner's, not a model result.
- **Supersedes:** none; extends L-001.
- **Accepted by:** round 2 review, 2026-09-25.

## L-006 — Once all heat is removed, the exchanger arrangement has no effect on the plant-ledger and cycle-state outputs (net, gross, auxiliary, turbine inlet, efficiency, mixed outlet), because the turbine inlet then follows from the energy balance alone; exchanger-stage channels (stream outlets, capabilities, terminal differences) still differ, and the arrangement matters only where a stage is limited

- **Evidence:** `c3-minus-recuperator` against `network-c3-eps0.8-0.85` and `resized-compressor-1800-series` against `-network-0.85`: plant-level channels identical, 19 of 551 exchanger-stage channels differ (round-2 review F2); record § Addendum.
- **Scope:** the bounded ε-NTU closure of WI-089/WI-092 with fixed hardware.
- **Implication:** arrangement studies are informative only in the heat-limited regime; a steady point's plant outputs do not identify the arrangement.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-25.

## L-007 — At the best tested steady case the entire remaining gap to Lyon's 1253 / 1000 MW (110 / 109 MW) is the thermal-efficiency shortfall at the heat-limited turbine inlet (628 against 708 °C); our implementation of the published network with the published duties does not reach 708 °C at any split; whether that reflects the published design or our interpretation of it is unresolved (amended 2026-09-25 at the owner's direction, `evidence/owner-supplement-r3.md`)

- **Evidence:** `resized-compressor-1700-network-0.85` (gross 1143.013, efficiency 0.3907, turbine 901.351 K); split sweep (PbLi stream at most 731 °C while starving the divertor); `evidence/discrepancy-ledger.md` v2.1; round-2 review L-007 ruling (gross gap 109.987 equals the efficiency shortfall).
- **Scope:** the model's own cycle relation (WI-089) and the contract's Q1; not a statement about the actual ARIES design.
- **Implication:** the reconciliation stays open on the narrow question of why our heat-delivery and cycle model gives a lower turbine-inlet temperature and efficiency than the published calculation; round 3 checks the primary diagrams, definitions, cross-paper mapping and our cycle representation.
- **Supersedes:** none; extends L-003.
- **Accepted by:** round 2 review, 2026-09-25.

## L-008 — The verifier's relative-only rule (1e-9) fails on small difference channels of a root solve, such as unmet heat, at the solver's termination order (1e-8 MW); declare absolute tolerances at that order for those channels, with focused independent review, before verifying a study whose points can have small nonzero differences

- **Evidence:** `evidence/t004-verify-attempt1.log` (2.03 MW channel refused at 1.6e-9 relative, 3.3e-9 MW absolute); `evidence/unmet-tolerance-declaration.md` and `unmet-tolerance-review.md`; `results/attempt-comparison.json` (re-execution bit-identical).
- **Scope:** studies on the ARIES packages verified with `scripts/study/verify.py`; the manifest's `absolute_tolerances` list.
- **Implication:** the live manifest now carries 1e-7 MW on the four unmet-heat channels; future studies with other small difference channels should declare theirs before execution, not after a refusal.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-25.

## L-009 — The integration seam and the study commands must run under the launcher's own environment (`.codex-test/run …` or `.codex-test/run bash -c '…'` with the TEAx root expanded inside); an outer PYTHONPATH built from an unset `STOP_PARSER_TEAX_ROOT` puts `/packages/teax-simkit` on the path and trips the seam's read-coverage gate

- **Evidence:** `evidence/integration-attempt1.log` (BLOCKER: undeclared dependency read `/packages/teax-simkit`) against `integration-attempt2.log` (CANDIDATE); trail T-003 return.
- **Scope:** this checkout's `.codex-test/run` launcher and `scripts/integrate.py`.
- **Implication:** one wasted seam run per goal if forgotten; recorded in the trail's T-003 decision and here.
- **Supersedes:** none.
- **Accepted by:** round 2 review, 2026-09-25.

## L-010 — With Raffray's printed per-branch duties and temperatures, these published quantities cannot all hold under the stated heat-exchanger assumptions (qualified 2026-09-25 at the owner's direction, `evidence/owner-supplement-r4.md`); in every arrangement checked the cycle does not reach the printed 707 °C outlet: the blanket-helium loop (hot inlet 456 °C) carries 42% of the heat over 21% of the span and would need ≥ 11.8 MW/K at zero approach (16.8 at the printed 30 °C) against 8.0 MW/K for the whole cycle flow; Raffray's Fig. 12 inset ("Typical Fluid Temperatures in HX") draws one lumped hot leg 385 → 737 °C; a lumped-heater cycle calculation would be consistent with it but is a hypothesis until the cited source supports it; what the ARIES-CS cycle calculation actually did was pursued through Raffray's cited cycle references in round 4: the cited method takes the turbine inlet as an input from a single heat source or IHX and does not state how ARIES-CS combined its loops (L-013)

- **Evidence:** `evidence/q1-thermal-cycle-review.md` (fresh thermal-cycle reviewer, checks (a)–(e)); `work/active/WI-086_aries-dual-blanket-heat-accounting/evidence/raffray-p736.png` (Fig. 12 with its inset; Fig. 13); contract § 6a; round-3 review F1 (inset attribution).
- **Scope:** the printed per-branch description in Raffray Tables II, III and V and Fig. 12; our per-branch representation on the WI-092 package.
- **Implication:** supersedes the wording of L-003 and L-007 on this point, not their numbers: the disagreement is a source-internal inconsistency that survives independent review; it does not establish what the actual design could achieve (owner framing, `evidence/owner-supplement-r3.md`).
- **Supersedes:** L-003 and L-007 wording on the arrangement claim.
- **Accepted by:** round 3 review, 2026-09-25.

## L-011 — The cross-paper mapping must scale the primary flows with the duties: holding Raffray's flows while scaling duties by 1.030 pinches the PbLi cold end and is worth ≈ 34 MW on the PbLi stage at 1600 kg/s, of which ≈ 20 MW migrates to the helium stage, so the total shortfall changes by only ≈ 14 MW and the steady 1700 kg/s result is unchanged to 1e-3 MW

- **Evidence:** `20260925-aries-flow-scaling-check` `results/attribution.md` (`network-c3-0.85` against `network-c3-scaledflows-0.85` and `-pbli-only-0.85`; the two 1700 kg/s cases); contract § 6a rule amendment.
- **Scope:** the WI-092 package at the C3 inputs, 1600–1700 kg/s, split 0.85–0.90.
- **Implication:** the contract's § 8 mapping now scales flows with duties; earlier rounds' unscaled convention is retained and both are quantified.
- **Supersedes:** none.
- **Accepted by:** round 3 review, 2026-09-25.

## L-012 — (process) A per-branch model shortfall can migrate between stages when one input is corrected; attribute by stage and by total, never by a single stage's change

- **Evidence:** round-3 review check 6: `he_unmet` 53.514 → 73.604 while `pbli_unmet` 56.362 → 22.077 under the flow scaling.
- **Scope:** any multi-stage heat-driven closure with bounded stages.
- **Implication:** ledger rows report per-stage and total unmet heat side by side.
- **Supersedes:** none.
- **Accepted by:** round 3 review, 2026-09-25.

## L-013 — The ARIES-CS Brayton cycle method (Raffray Ref. 15, Schleicher, Raffray and Wong 2000/2001; expressions from Malang, Schnauder and Tillack 1998) takes the turbine inlet temperature as an independent input from a single heat source: Schleicher draws the heat source as a boundary "to/from in-reactor components or IHX" and makes the return temperature a dependent variable of the compression ratio; Malang states both terminals of one lithium-to-helium IHX and takes the turbine inlet from its helium outlet; in the obtained sources the method was never extended to several primary loops at different temperature levels, so a branch-level inconsistency like Q1 would not surface in that calculation; whether ARIES-CS combined its three loops in a single hot leg is inferred, not stated

- **Evidence:** `evidence/ref15-reading.md` and `ref15-reading-review.md`; `evidence/malang98-reading.md` and `malang98-reading-review.md`; contract § 6a `[r4]`; round-4 review ruling (Schleicher alone makes Tout dependent).
- **Scope:** the two registered sources and Raffray 2008 Tables II–III and Fig. 12; not the paywalled Ref. 13.
- **Implication:** the answer's remaining gap stays a source-internal inconsistency under the stated heat-exchanger assumptions; the lumped-heater reading of the Fig. 12 inset is consistent with the cited method and remains an inference (owner framing).
- **Supersedes:** wording of L-010 on what the cited references say; none of its numbers.
- **Accepted by:** round 4 review, 2026-09-25.

## L-014 — (process) A citation named by a reviewer or a summary must be verified against the reference list and a citation-marker scan, with each marker's context checked, before it is pursued: the round-3 "p737 Ref. 7" was Lyon's retained systems paper, the cycle references were Refs. 15 and 13, and Raffray's p745 markers are off by one (the conclusion's markers belong to Ref. 16), so they do not corroborate the cycle attribution

- **Evidence:** trail round-4 T-001 return (citation scan); `evidence/raffray-p745.png`, `raffray-p746.png`; round-4 review finding 4.
- **Scope:** any pursuit of a cited source from a retained paper.
- **Implication:** one wasted request per misattribution if skipped; the scan takes minutes.
- **Supersedes:** none.
- **Accepted by:** round 4 review, 2026-09-25.
