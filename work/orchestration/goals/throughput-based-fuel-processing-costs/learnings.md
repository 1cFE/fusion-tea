# Learnings: Throughput-based fuel-processing costs

Accepted learning entries follow round review.

## L-001 — Verified isotope flow is available, while price applicability needs a separate process premise

- **Evidence:** Native research reports and request runs@66548f14; evidence/interface-review.md, evidence/source-review-r2.md and evidence/current-r10s-grade.md in this goal's local evidence checkpoint.
- **Scope:** WI-069 supplies running plasma-exhaust isotope load. Larger conventional reactor-process design evidence supports a conditional ORNL cost-method transfer, not actual feed qualification, blanket-extraction coverage or a completed plant price.
- **Implication:** Resolve the explicit process/feed adoption decision before using the relation in plant costs. Preserve source conditions and remaining unpriced functions; historical-method arithmetic alone does not meet R10.S2.
- **Supersedes:** none.
- **Accepted by:** Round 1 coordinator review using independent evidence,2026-09-19; process adoption remains owner-held.

## L-002 — Processing price follows running exhaust, with source assumptions separate

- **Evidence:** WI-070 model/audit at `2a50d3ec`; twenty-case study at `2bae7fb7`; final-review-and-grade.md, R10.S = 2.
- **Scope:** The adopted four-row conventional aggregate consumes pre-loss running D+T exhaust. Burn and native plasma power change its demand; recovery and annual downtime do not change required running capacity at fixed plasma state. Capacity margin, price multiplier and containment expenditure year are separate sensitivity inputs, with no demonstrated reliability or procurement-confidence interpretation.
- **Implication:** Retain source-conditioned use and explicit qualification gaps. Study findings #1–4 remain declared limits, not optimized settings or instructions to fabricate new constraints.
- **Supersedes:** none.
- **Accepted by:** Independent Round 2 review and coordinator, 2026-09-19.

## L-003 — Matched accounting controls separate price changes from physical responses

- **Evidence:** Frozen study matched-account-deltas.json, legacy-burn-attribution.json and invariance-checks.json; independent attribution-checks.json; findings #5–6.
- **Scope:** Full C220500 replacement and contingency-loaded installation freight exclusion reach plant total once. Local package controls and supervisory controls have explicit separate owners; the inherited supervisory coefficient remains uncalibrated. Burn also changes recurring fuel. Physical recovery and recurring-price recovery remain separate inputs. Every sampled case retains plant failures.
- **Implication:** Use same-physics old/new controls for the method effect. A lower limited-scope estimate establishes neither actual savings, complete fuel-plant pricing nor whole-plant feasibility. No new recovery-cost coupling or loss assumption was adopted.
- **Supersedes:** none.
- **Accepted by:** Independent Round 2 review and coordinator, 2026-09-19.

## L-004 — Preserve proposal-admission failures separately from model results

- **Evidence:** Frozen study attempt-1 receipts, original/native stores, final-admission.json and finding #7.
- **Scope:** The stock route rejected five Boolean legacy switches before evaluation. Equivalent numeric zero passed the existing generated Boolean interface and runner; the same twenty points were re-scanned and executed in a new store.
- **Implication:** This execution is resolved. The shared-route Boolean allowlist gap remains for possible future tooling work; no shared route or physical model was changed. Preserve both rejected proposals and successful native cases rather than calling admission failures physical infeasibility.
- **Supersedes:** none.
- **Accepted by:** Independent Round 2 review and coordinator, 2026-09-19.
