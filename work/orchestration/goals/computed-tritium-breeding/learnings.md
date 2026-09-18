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

## L-003 — A bounded transport response can provide calculated breeding and design pushback

- **Evidence:** Audited model `d2e29237`; native study `5347d5a3`; `evidence/round2/table-release-review.md` and `final-review-and-grade.md`.
- **Scope:** The retained helium/PbLi conceptual torus supports thickness 0.60–1.00 m under its explicit material/source/opening and fixed-geometry assumptions. Five transport nodes and six withheld checks support the interpolation. Approximate independent integral experiments provide a separately limited physical consistency check.
- **Implication:** R2c.P3 is met without finding an adequate whole plant. Numerical validation does not establish actual stellarator qualification. Future geometry/material/source changes need new applicable transport evidence; clipping or extrapolating the table is not an extension of its evidence.
- **Supersedes:** L-001's implied current-plant method gap is resolved by a new transport route; its finding that the published HCLL surrogate cannot be directly transferred remains valid.
- **Accepted by:** Round 2 independent final review, 2026-09-18.

## L-004 — The stricter conditional fuel requirement changes the accepted build

- **Evidence:** Study `results/points.csv`, `oracle-all-points.json` and `report.md@5347d5a3`; final independent review.
- **Scope:** The retained design floor is 1.05; the stated fuel assumptions require 1.190. At 0.80 m, mean TBR is 1.198074 but the numerical lower estimate is 1.186146 and fails. The sampled 0.825 m case passes breeding but fails peak field. Costs and build change, and every studied case retains other plant failures.
- **Implication:** Keep gross production, breeder extraction, exhaust recovery, decay and reserve growth distinct. A cost-derived 0.99 recovery assumption does not establish physical isotope recovery. The numerical lower estimate is not a physical uncertainty bound. Supported conditional passes and unsupported applicability failures have different meanings.
- **Supersedes:** L-002's statement that achieved production is still uncomputed describes Round 1 only; its warning about the old floor remains valid.
- **Accepted by:** Round 2 independent final review, 2026-09-18.

## L-005 — Cost volume and transport breeder volume are distinct model quantities

- **Evidence:** Study `results/volume-accounting.json` and `report.md@5347d5a3`; final independent review.
- **Scope:** Baseline blanket-account volume is 1,013.406 m³, including full-shell first wall, breeder and reflector. Gross transport breeder is 742.036 m³ and its retained volume after the explicit opening is 719.775 m³. The neutron-energy multiplier remains held at 1.2.
- **Implication:** Thickness has real represented economic/build consequences, but those quantities do not prove a consistent installed material inventory or computed heat-production response. Preserve this declared seam until a separately scoped engineering account resolves it.
- **Supersedes:** none.
- **Accepted by:** Round 2 independent final review, 2026-09-18.
