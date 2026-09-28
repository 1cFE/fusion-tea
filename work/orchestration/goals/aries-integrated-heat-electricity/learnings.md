# Learnings: Integrated ARIES heat and electricity

Accepted claims are appended after round review.

## L-001 — The assumed calculated-plasma nominal closes the integrated heat/electricity calculation

- **Evidence:** `exploration/aries_integrated/studies/20260922-integrated-heat-electricity/@8e6fb2f2`, native candidate `evidence/integration-attempt3/integration_return.json@a8912fa4`.
- **Scope:** selected fusion flows through three heat paths to 423.106794 MW net electricity with zero unmet heat. This is the explicit calculated-plasma nominal with supplied profiles and assumed equipment, not the adverse source-conditioned nominal or scientific validation of the published plant.
- **Implication:** continue inventory/cost work from this single native assembly and preserve its explicit qualification and interfaces.
- **Supersedes:** none.
- **Accepted by:** independent round 1 review, 2026-09-22, with the calculated-plasma referent clarified.

## L-002 — Literal source points retain thermal and accounting discrepancies

- **Evidence:** `exploration/aries_integrated/studies/20260922-integrated-heat-electricity/record.md@8e6fb2f2`, exact cases in that record's `results/cases.json`.
- **Scope:** source-conditioned and literal source cases are thermally inadequate under the represented equipment; the Raffray case also retains a 182.03 MW source-energy discrepancy. These are model/configuration findings, not proof that the published plants are physically infeasible.
- **Implication:** preserve distinct source bases and adverse evidence; reconcile source accounting and thermal configuration before stronger published-plant claims.
- **Supersedes:** none.
- **Accepted by:** independent round 1 review, 2026-09-22.

## L-003 — Demand propagation and offered capacity remain independent

- **Evidence:** `exploration/aries_integrated/studies/20260922-integrated-heat-electricity/results/propagation-and-input-preservation.json@8e6fb2f2`, frozen native cases at the same commit; broader eight-capacity evidence in WI-089 `evidence/verification.json@71b2867a`.
- **Scope:** density perturbations hold every hardware input fixed while fuel, heat, cycle, auxiliary and net-electric outputs respond. Fuel/helium rating pairs change their own adequacy verdicts without changing demand or export. This verifies the represented roles; it does not qualify actual equipment or cost it.
- **Implication:** carry these independent choices into prompt 02. Price selected installed capability and retain inadequacy; do not turn calculated demand into hidden resizing or purchases.
- **Supersedes:** none.
- **Accepted by:** independent round 1 review, 2026-09-22.

## L-004 — Heat-transfer and compression choices have bounded observable effects

- **Evidence:** `exploration/aries_integrated/studies/20260922-integrated-heat-electricity/record.md@8e6fb2f2`, conductance and compressor-ratio cases in the frozen native results.
- **Scope:** helium UA of 5 MW/K leaves 47.118607 MW unmet heat; the 75 MW/K point accepts the nominal heat without increasing export beyond the nominal. First-stage compressor ratios 1.4 and 1.65 produce 470.897994 and 366.692730 MW net with all other selected inputs held fixed. These points do not establish global monotonicity, a feasible-region boundary or an optimum.
- **Implication:** use explicit equipment/interface sensitivity to investigate a named design question; qualify further thermal and machine behavior before expanding the claim.
- **Supersedes:** none.
- **Accepted by:** independent round 1 review, 2026-09-22.
