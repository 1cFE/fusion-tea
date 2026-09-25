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

## L-003 — The Lyon reference is a systems-constant chain (2916 MW → 43% → 1253 → −253 → 1000), and the independently checked Q1 shows the published temperatures, duties and series-first arrangement cannot all hold, so part of the disagreement is a property of the published description

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
