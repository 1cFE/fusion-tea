# Learnings: fusion-audit-remediation

Append-only, newest last. Entries are appended only after fresh round review accepts or corrects a proposed delta. No accepted learnings yet.

## L-001 — A satisfied efficiency-times-gain heuristic does not establish net generation

- **Evidence:** `work/active/WI-048_ife-operating-point-repair/audit.md@6a964967bc6d736c9efe99642ef01c79c92ff196`; `exploration/ife_e2e/studies/20260910-ife-operating-point/record.md@9f09f6971c8a1b5c558fbf66d5de1bc97568099e`, §§ 3–4, 13, 15 and cited case evidence.
- **Scope:** [AGENT] The audited IFE operating chain and its named ordinary and non-generating cases. This establishes neither engineering completeness nor a normalized financial comparison.
- **Implication:** Preserve the linked procurement/power/price inputs and the strict computed-net gate in later IFE changes. A satisfied heuristic cannot make a non-generating price sentinel eligible.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-11.

## L-002 — Reachable constraints can retain the same verdict throughout a sensitivity window

- **Evidence:** `exploration/ife_e2e/studies/20260910-ife-operating-point/synthesis.md@697b82287f0620208a8e5c15da72b7be42b295c4`, Framing verdict per axis and Constraint structure; its cited indicators and ordinary case results at `9f09f697`.
- **Scope:** [AGENT] Beam-energy and repetition-rate changes under this study's held gain, efficiencies and engineering assumptions. The coordinated diagnostic cases do not locate either ordinary axis's boundary.
- **Implication:** Read indicators as possible dependency paths and the executed points as bounded response evidence. Engineering limits and optima need additional evidence; these observations do not supply them.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-11.

## L-003 — Integration verification and study indicators consume expressions separately

- **Evidence:** `.project/active/ife-native-study-package/integration/integration_return.json@f0d2f67096a69c26add06d137f532d55bf3361d2`; `exploration/ife_e2e/studies/preparation/20260910-ife-operating-point-prerequisite.md@1bde8771`; `.project/active/study-indicator-multiplication/audit.md@adab59d9087f321c21a2a15f68151165a96579b7`.
- **Scope:** [AGENT] The existing IFE binary-multiplication predicate and the two independently certified consumer corrections. No general expression support follows from these repairs.
- **Implication:** A native integration candidate does not discharge the study's indicator step. Read each producer's actual outcome; separately scope any missing shared capability. The later indicator's coverage evidence does not rewrite the earlier integration gate's omission.
- **Supersedes:** none.
- **Accepted by:** Round 1 review, 2026-09-11.

## L-004 — A correct price ratio can conceal errors in discounted cost and energy

- **Evidence:** `work/analysis/20260911-141041_ife-zero-discount-assessment.md@692c9f94` and its numerical evidence at `cc0cd821`; `work/analysis/20260911-144931_audit_WI-049_ife-zero-discount-repair.md@c926a36d`; `exploration/ife_e2e/studies/20260911-ife-zero-discount/results/decimal-verification.json@a66f962d`.
- **Scope:** [AGENT] The IFE present-value calculation near zero discount. The original cost and energy errors partly cancel in their quotient. Independent dated sums and the bounded repaired cases establish numerical behavior, not the validity of financial assumptions.
- **Implication:** Verify discounted cost and energy separately against independent references before crediting the price quotient. Preserve exact non-generation exclusions alongside numerical accuracy checks.
- **Supersedes:** none.
- **Accepted by:** Round 2 review, 2026-09-11.

## L-005 — An oracle's coverage does not define the model's input domain

- **Evidence:** `work/active/WI-049_ife-zero-discount-repair/spec.md@165d2bbf`; `work/analysis/20260911-144931_audit_WI-049_ife-zero-discount-repair.md@c926a36d`; `.project/active/ife-zero-discount-study-package/audit.md@f04c0622`; `exploration/ife_e2e/studies/20260911-ife-zero-discount/synthesis.md@5fd978e7`.
- **Scope:** [AGENT] Existing Real-valued IFE durations and an annual-sum oracle restricted to positive integer durations. The model audit separately checks fractional algebra; the study samples only five construction and forty operating years. Neither supplies a new fractional-year timing convention or unrestricted Real-domain certification.
- **Implication:** Keep oracle refusal, model-domain policy and sampled study coverage distinct. Preserving fractional algebra needs its own numerical evidence; integer-only verification cannot silently narrow the model contract or claim fractional study coverage.
- **Supersedes:** none.
- **Accepted by:** Round 2 review, 2026-09-11.
