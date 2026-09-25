# Learnings: ARIES reconciled-alternative economics

Append-only, newest last. An entry is appended only after a round review accepts or corrects the delta the round result proposed (`work/orchestration/GOAL_RUNBOOK.md` § The fresh review). Each entry is one claim with its evidence, scope, implication, supersession and acceptance.

## L-001 — The 891 MW alternative's economics are decided by the tritium supply assumption, not by its changed equipment; the ranking against the 423 MW baseline reverses between the two supply scenarios

- **Evidence:** `exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/attribution.md@c0120c93` § A, § B, § D (no-credit 685.695 with tritium 627.323 = 91.5 %; feed100 238.028; baseline deltas −433.713 and +61.342; compressor price ±0.650; pump mapping 0.019); `evidence/equipment-cost-audit.md@e8a91dc7` (three changed purchases, +6.083 MUSD2004 direct).
- **Scope:** the WI-092 package at the canonical alternative and the WI-090/WI-091 conventions; the fixed calendar feed of F7.
- **Implication:** an economic comparison of ARIES-like alternatives is a comparison of tritium-supply assumptions unless the supply is modelled; report both scenarios and never present the fixed-feed ranking as physical (the supply-threshold effect of the design-studies goal, L-002/L-005 there).
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25.

## L-002 — The two capital conventions coincide (direct × 1.49 × 1.1576 against the source's × 1.93 inclusive: 0.27 USD2004/MWh apart), so after aligning fuel, O&M, life and replacement conventions the residual against the published 77.6 is the source's unprinted financing rate, with the three bounded costs excluded from the aligned case

- **Evidence:** same record § C (L1 capital-scope +0.267 / +0.236; L7 59.313 at 5 % real, 31.885–104.898 over 0–10 %; branch 53.058 and 30.659–83.404; the sign of the residual changes between 5 and 8 % on ours and 8 and 10 % on the branch; denominator −6.491 aligned); `evidence/comparison-basis.md@c0120c93` § 1 (the source's rate is not printed).
- **Scope:** the aligned ladder's labelled substitutions on the canonical case; the bounded costs (up to ≈ +16 on the ours band: recuperator +4.9, cycle side +9.3, PbLi ≈ +2.1) are not inside the aligned case.
- **Implication:** the comparison cannot be closed below tens of USD/MWh without the source's financing convention; report the residual at every swept rate and designate none as the match; the 109 MW output shortfall is worth −6.5 USD/MWh under source-like fuel accounting and −26 to −75 under ours.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25 (clause on the excluded bounded costs added by the reviewer).

## L-003 — Three costs of the alternative have no cost response in the WI-090 assembly: the 0.95 recuperator (no purchase, rating or screen), the fixed cycle-side allowances at 1700 kg/s and 1143 MW gross (a fixed purchase with no response, rating or screen), and PbLi pumping (a 0.01 MW placeholder); their declared bounds are +4.9 and +9.3 (capital, the same on any base) and +8.3 on the feed100 figure (a denominator effect: ≈ +2.1 on the aligned figure, ≈ 0 on the branch), material against 77.6 on their own base and immaterial to L-001

- **Evidence:** `evidence/equipment-cost-audit.md@e8a91dc7` items 1, 2, 6; record § D (`sens-conversion-services-6`, `sens-cycle-side-2.0`, `sens-pbli-pump-30MW-feed100`); `evidence/round1-review.md` (correct-before-use finding).
- **Scope:** the canonical alternative on the WI-090 cost bindings; the bounds are `[ASSUMED]` (NTU proxy, E4 corner, order-of-magnitude pumping).
- **Implication:** a recuperator hardware representation (selected rating, screen, purchase leaf) needs a reference price no source account supplies; until then the recuperator cost is reported as unresolved-bounded, never as a hardware claim.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25 (corrected by the reviewer: cycle-side allowances have a fixed purchase; the PbLi bound is feed100-based).

## L-004 — (process) The verifier's relative-only rule refuses an exact-zero difference channel when the package computes it in float64 and the oracle in Decimal (curtailed feed at feed = makeup: 0.0 against 6.8e-15 kg/year); the four-channel 1e-9 kg/year class is now in the live manifest, and a study with a feed-equals-makeup point must carry it

- **Evidence:** `evidence/curtailed-tolerance-declaration.md@c0120c93`, `curtailed-tolerance-review.md@c0120c93`; the record's `results-attempt1/verify-refused.log` and `results/attempt-comparison.json` (bit-identical re-execution).
- **Scope:** `scripts/study/verify.py` on the ARIES packages; the lifecycle comparison catalog.
- **Implication:** extends L-008 of the prior goal to a second class (float64 against Decimal at exact equality); declare before execution when a design sets feed equal to makeup.
- **Supersedes:** none; extends `aries-reference-heat-electricity-reconciliation` L-008.
- **Accepted by:** round 1 review, 2026-09-25.

## L-005 — (process) A fresh cost-audit brief that excludes the reference-case contract grades source-supported operating inputs as unbased; include the contract's grade table in such briefs

- **Evidence:** `evidence/equipment-cost-audit.md@e8a91dc7` § Missing evidence against the prior goal's `evidence/reference-case-contract.md@b03fa18e` § 2–3, § 5, § 8; trail T-002 return.
- **Scope:** bounded audit briefs for this model family.
- **Implication:** one reconciliation paragraph per audit if forgotten; a two-line pointer in the brief avoids it.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25.

## L-006 — A replacement life selected at one neutron power does not transfer to a configuration with +32.7 % neutron power; two applicability points (the fluence-scaled 3.767 FPY and the source cadence 2.907 FPY) cost +0.7 and +1.5 USD2004/MWh, and the E8 low end (2 FPY) +2.8

- **Evidence:** record § D (`sens-replacement-life-fluence-3.767-feed100`, `sens-replacement-life-2-feed100`) and § C0 (`diag-L5-source-cadence-47y-feed100`); `evidence/comparison-basis.md@c0120c93` § 4.
- **Scope:** the E8 selected-life convention on the canonical alternative; no damage model.
- **Implication:** the answer reports the points, not a bound; a materials/fluence model is the missing evidence.
- **Supersedes:** none.
- **Accepted by:** round 1 review, 2026-09-25 (wording corrected by the reviewer: points, not a bound).
