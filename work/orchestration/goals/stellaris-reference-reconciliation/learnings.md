# Learnings: Stellaris reference reconciliation

Accepted learning deltas will be appended after round review.

## L-001 — A global radial layer does not establish a local casing cavity

[AGENT, accepted by independent final review 2026-09-16] The inherited 300 mm coil layer is a generic full radial build. Original Fig.34's 250 mm magnet span ends at coil center and is an approximate average. Neither quantity supplies the minimum local cavity or manufactured envelope. Keep the raw declared-scenario fit failure separate from published-reference applicability. Evidence: `evidence/geometry-research.md`, `evidence/source-review.md`, `evidence/final-review.md`.

## L-002 — Exact source profiles change several residuals in different directions

[AGENT, accepted with correction by independent final review 2026-09-16] In the matched legacy scenarios, exact fuel/temperature exponents 0.35/1.2 reduce calculated operating auxiliary demand from 49.0796 to 45.1725 MW and divertor peak from 10.5178 to 10.2862 MW/m². Neither failed predicate recovers, and agreement with published fusion power and confinement time worsens. This is attribution, not general source-fit improvement. Evidence: committed study `a17f51f0`, `results/case-summary.csv` and `results/contrasts.json`; final review accepts the narrowed claim.

## L-003 — Source conditioning must preserve subsystem case and topology distinctions

[AGENT, accepted by independent final review 2026-09-16] Stellaris's water/PbLi breeder and helium first-wall circuits, local field-angle conductor calculation, and paired 500 MW divertor cases differ from the retained helium-primary/global-peak/generic-geometry forward model. Supplied source volume, field and peaks receive no independent prediction credit; held source TBR and multiplication remain conditional after topology/geometry changes. Explicit scenarios and applicability preserve these distinctions without filtering unknowns into a pass. Evidence: `reconciliation.md`, `evidence/predicate-applicability.json`, committed study `a17f51f0` and `evidence/final-review.md`.
