# Learnings: Winding-pack/casing fit

Append-only; claims are added after independent round review accepts the proposed delta.

## L-001 — Independent allocation exposes a nominal pack conflict

- **Evidence:** `exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/analysis.json@62e47730`; source/design review `06a19a3b`; final review in evidence/final-review.md.
- **Scope:** The declared centered, aligned local rectangle has a 0.30 m exterior radial allocation and a 0.36 m nominal reference pack. With stated walls and allowances the reference margin is −0.120 m, and all three original sampled eighteen-predicate passes fail fit. This is a conditional modeling conflict, not a measured Stellaris cavity failure.
- **Implication:** Keep available geometry independent of pack demand. Obtain actual limiting sections and insulation/tolerance conventions before interpreting a local screen as device-specific fit.
- **Supersedes:** none.
- **Accepted by:** Round 1 final independent review, fit_reviewer, 2026-09-15.

## L-002 — Separate predicate meanings distinguish screening from repricing

- **Evidence:** `exploration/stellarator_e2e/studies/20260915-winding-pack-casing-fit/results/comparison-entering.json@62e47730`; `results/geometry-isolation.json@62e47730` in the same record; final review in evidence/final-review.md.
- **Scope:** The screen preserves eighteen original predicates and matched entering quantities. Across this engineered sample, 45 old-predicate passes become twelve fit-inclusive passes. The cheapest retained alternative costs $145.02/MWh versus $143.35/MWh and uses a larger independent radial allocation. The screen itself adds no cost; the allocation changes existing geometric/economic dependencies. Insulation procurement, casing fabrication and structural/thermal qualification remain outside this conclusion.
- **Implication:** Compare old and fit-inclusive feasibility on identical cases. Keep allocation and geometry-assumption alternatives distinct from nominal results, and attribute increments against the entering package.
- **Supersedes:** none.
- **Accepted by:** Round 1 final independent review, fit_reviewer, 2026-09-15.
