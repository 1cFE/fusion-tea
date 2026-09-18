# Learnings: computed tritium breeding

Accepted claims will be appended after round review.

## L-001 — A published executable HCLL surrogate exists, but its domain excludes the current blanket

- **Evidence:** Native research report `knowledge/research/pending/20260918-130310_computed-tritium-breeding-methods.md`; original source registration and `evidence/hcll-surrogate-assessment.md`, `hcll-original-cpp-verification.json`, `method-review.md` (unpinned at review; no native digest for review files).
- **Scope:** The recovered example reproduces its own C++ calculation and responds to source-domain material/build choices. The final-module discrepancy, example-network uncertainty and transfer to current stellarator remain unresolved.
- **Implication:** A new transport installation is not necessary merely to evaluate this research model. Current-plant integration needs a validated domain/mapping or a declared, justified redesign; clipping inputs is not validation.
- **Supersedes:** none.
- **Accepted by:** Round 1 independent review, 2026-09-18.

## L-002 — Passing the held breeding floor does not establish fuel self-sufficiency

- **Evidence:** Current model at e78099cb93ab36b57debf70045cc9c4e7bcfcdd8, traced in `evidence/current-trace.md`; `evidence/threshold-check.json` and independent `method-review.md` (unpinned at review; no native digest for new evidence).
- **Scope:** The current physical-reading recovery scenario gives a requirement exceeding the held production. The recovery value is not validated isotope evidence; actual blanket production remains uncomputed.
- **Implication:** Keep production, recycled-exhaust recovery, breeder extraction, decay and stock growth distinct. A justified design floor and a conditional atom-balance requirement need explicit semantics before combined feasibility claims.
- **Supersedes:** none.
- **Accepted by:** Round 1 independent review, 2026-09-18.
