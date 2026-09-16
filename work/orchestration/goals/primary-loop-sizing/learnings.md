# Learnings: Explicit primary-loop cooling-system sizing

No learning delta accepted yet.

## L-001 — Sixteen averaged loops clear the informative flow screen while the divertor still fails

- **Evidence:** `exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/record.md@75772eba`, results/analysis.json and exact entering-control checks at the same revision.
- **Scope:** Existing helium, temperature rise, source heat and representative pressure-loss model. This is the adopted nominal-flow screen, not qualified hardware capacity. The current reference requires fourteen loops; none of twenty sampled cases passes all predicates.
- **Implication:** Treat loop accommodation and combined feasibility separately; keep the remaining divertor and magnet failures visible.
- **Supersedes:** none.
- **Accepted by:** Round 1 independent review, 2026-09-16, `evidence/final-review.md`.

## L-002 — Power-scaled coolant cost does not price the added loop equipment

- **Evidence:** `evidence/entering-cost-account.md@df41ea97`, `evidence/cost-research.md@df41ea97`, `evidence/cost-review.md@df41ea97`, and study results/analysis.json at `75772eba`.
- **Scope:** The informative fourteen-to-sixteen-loop comparison has $48.068 million/year of conditional annual cost headroom. It is not an installed price or capex estimate. The registered source points to unacquired internal report EFDA_D_2NSZ4M and omits large-pipe cost; quote boundary/currency/year remain unknown.
- **Implication:** Acquire an applicable equipment/installation price and avoid double counting aggregate accounts before adopting an economic benefit. Account for reliability/availability consequences separately.
- **Supersedes:** none.
- **Accepted by:** Round 1 independent review, 2026-09-16, `evidence/final-review.md`.

## L-003 — Nominal heterogeneous circuits support a conditional count comparison, not a qualified geometry transfer

- **Evidence:** `evidence/hydraulic-source-account.md@df41ea97`, original Moscato tables and `evidence/source-review.md@df41ea97`; frozen study `75772eba`.
- **Scope:** The source uses three inboard and six outboard circuits. The current model averages their flow/resistance. Two circulators and one IHX per representative loop are conditional quantities; calculated IHX duty is a requirement. Routing, flow allocation, exchanger/compressor maps and drive efficiency remain unresolved. External area enlargement has no supported transfer law here.
- **Implication:** A later hardware-sizing result needs those geometry/performance inputs; increasing an averaged loop count alone does not provide them.
- **Supersedes:** none.
- **Accepted by:** Round 1 independent review, 2026-09-16, `evidence/final-review.md`.
