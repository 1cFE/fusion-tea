# Learnings: magnet-coil-realism

What this run now knows. Goal directory `work/orchestration/goals/magnet-coil-realism/`.

Append-only, newest last, ISO dates, never edited in place. An entry is appended **only after** a round review has accepted or corrected the delta the round result proposed (`GOAL_RUNBOOK.md` § The fresh review). Mechanical failures produce no learning.

Each entry is one claim.

### L-001 — Bore pricing leaves the sampled feasible minor radius unchanged — 2026-09-15

[AGENT] At the winding-length pin, the cheap transects still have exactly one point satisfying all eighteen predicates, at `a = 1.7 m`; their unconstrained price minima move from 2.2 to 2.1 m and violate the burn and loop predicates. The design-column price minimum stays at 2.0 m and violates four predicates. A price minimum and a feasible minimum must therefore be reported separately.

- **Evidence:** study `results/a-minima.json@8ad7e913`; passed C-001.r2 reading at `7d2e1da0`.
- **Scope:** these three transects at pin `2a89b163…`, with their held transport, wall-peak and heating assumptions; before values are entering-pin oracle references. The plant-closure window and the older minor-radius goal's own columns were not rerun.
- **Implication:** later chain changes must report both minima and their predicate sets; this result does not settle the window optimum.
- **Supersedes:** none; corrects proposed L-001 before acceptance.
- **Accepted-by:** this fresh Round 1 review, 2026-09-15.

### L-002 — Historical fixed-bore radius sweeps carry the retired winding dependence — 2026-09-15

[AGENT] The retired major-radius form and the bore form agree only when their normalized bore and major-radius ratios agree. The fixed 1.85 m radial stack prevents fixed aspect ratio alone from ensuring this. At `a = 1.3 m`, the WI-058 replacement changes magnet capital by approximately −$371.0M at `R = 15.7 m` and +$157.0M at `R = 11.43 m`, relative to the entering form.

- **Evidence:** WI-058 audit § 1 and final recheck at `a6286a55`; study `results/R-invariance.json`, `preparation/before-entering-pin-oracle-transects.csv` at `8ad7e913`; signed differences independently recounted in C-001.r2.
- **Scope:** the quoted amounts belong to this entering-to-WI-058 comparison. Earlier fixed-bore radius readings using the retired form between WI-036 and this replacement carry that dependence, with amounts determined by their own pins. The sign of new-minus-old at the design bore is opposite to `R − 12.7`.
- **Implication:** reinterpret an earlier radius sweep using its actual winding basis and pin; do not transplant these dollar corrections or infer fixed-aspect-ratio equivalence.
- **Supersedes:** none; clarifies proposed L-002 before acceptance.
- **Accepted-by:** this fresh Round 1 review, 2026-09-15.

### L-003 — Store verification does not establish an export's joins — 2026-09-15

[AGENT] Checking native store values does not establish that a derived export associated those values with the correct study coordinates. This record's corrected analysis joins by coordinates and compares every exported point with the oracle; the reported earlier label-join defect is not independently reproducible because its export was overwritten.

- **Evidence:** study record § 10 and Addendum items 6–7 at `e44d5e5f`; `execution/analyze.py`, `results/points.csv` and `results/oracle-all-points.json@8ad7e913`; synthesis § 5 finding #5 at `8056ef20`.
- **Scope:** this study's export path; the reported 45 bad joins are executor testimony. The log's runbook-step proposal remains a candidate.
- **Implication:** assess the exported coordinate/value association separately when trusting a derived report. This accepted learning does not edit the runbook or create a universal publication requirement.
- **Supersedes:** none; corrects proposed L-003 before acceptance.
- **Accepted-by:** this fresh Round 1 review, 2026-09-15.

### L-004 — Explicit thermal inventory remains small in the nominal plant budget — 2026-09-15

[AGENT] Explicit current-lead, radiation and support heat raises nominal refrigeration from 0.864 MW to 2.138 MW. It remains below 1% of recirculating demand at the design and sampled cheap anchors under the declared nominal scenario.

- **Evidence:** final study anchor and nuclear-proxy rows, stage accounting and verification at 77bcc96e; independent interpretation review in evidence/T-007_postexecution_review.md.
- **Scope:** nominal declared thermal geometry, refrigeration efficiency and zero structure nuclear deposition; the proxy sensitivity is not an upper bound.
- **Implication:** refrigeration is small in these nominal plant budgets. This does not bound actual structure deposition or unqualified hardware heat loads.
- **Supersedes:** none.
- **Accepted-by:** independent reviewer /root/round1_review, evidence/final-mechanical-review.md final Round 3 assurance, 2026-09-15.

### L-005 — Total-support pricing raises cost without changing the sampled nominal geometry — 2026-09-15

[AGENT] The Eq. 56 total-support scenario raises baseline support cost from $54.4M to $209.1M at the inherited $18/kg rate. The implemented inventory/structure increment raises the cheap-point price while leaving the sampled nominal geometry unchanged.

- **Evidence:** final study entering comparison and support costs at 77bcc96e; independently checked nominal feasible minima and six dispositions in evidence/T-007_postexecution_review.md.
- **Scope:** zero predicate flips across the 159 immediate-entering comparison rows, with the held physics in answer.md. Assumption rows have no corresponding before rows. Older-package results remain references.
- **Implication:** this sampled window supports a cost increment without a changed nominal feasible choice. It does not establish invariance under other inputs or qualified geometry outside the window.
- **Supersedes:** none.
- **Accepted-by:** independent reviewer /root/round1_review, evidence/final-mechanical-review.md final Round 3 assurance, 2026-09-15.
